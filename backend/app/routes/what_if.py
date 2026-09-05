from datetime import date, time

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.database.database import SessionLocal
from app.models.optimized_block import OptimizedBlock
from app.models.optimization_run import OptimizationRun
from app.models.train import Train
from app.models.goods_forecast import GoodsForecast


router = APIRouter(
    prefix="/api/what-if",
    tags=["What-If Simulation"],
)


class WhatIfRequest(BaseModel):
    corridor_id: str
    unavailable_date: date
    start_time: time
    duration_hours: float
    scenario_type: str


def time_to_minutes(value: time) -> int:
    return value.hour * 60 + value.minute


def minutes_to_time(minutes: int) -> time:
    return time(
        hour=minutes // 60,
        minute=minutes % 60,
    )


@router.post("/analyze")
def analyze_what_if(request: WhatIfRequest):

    if request.duration_hours <= 0:
        raise HTTPException(
            status_code=400,
            detail="Duration must be greater than 0 hours",
        )

    db = SessionLocal()

    try:
        # ---------------------------------------------------------
        # 1. Calculate unavailable time window
        # ---------------------------------------------------------

        unavailable_start = time_to_minutes(
            request.start_time
        )

        unavailable_duration = int(
            request.duration_hours * 60
        )

        unavailable_end = (
            unavailable_start + unavailable_duration
        )

        if unavailable_end > 24 * 60:
            raise HTTPException(
                status_code=400,
                detail="Unavailable period cannot extend beyond midnight",
            )

        # ---------------------------------------------------------
        # 2. Get latest optimization run
        # ---------------------------------------------------------

        latest_run = (
            db.query(OptimizationRun)
            .order_by(
                OptimizationRun.optimization_run_id.desc()
            )
            .first()
        )

        if latest_run is None:
            return {
                "scenario": {
                    "corridor_id": request.corridor_id,
                    "unavailable_date": request.unavailable_date,
                    "start_time": request.start_time.strftime(
                        "%H:%M"
                    ),
                    "duration_hours": request.duration_hours,
                    "end_time": minutes_to_time(
                        unavailable_end
                    ).strftime("%H:%M"),
                    "scenario_type": request.scenario_type,
                },
                "affected_blocks": [],
                "affected_block_count": 0,
                "alternative_slots": [],
                "alternative_slot_count": 0,
                "recommendation": (
                    "No optimization run is available."
                ),
            }

        # ---------------------------------------------------------
        # 3. Get optimized blocks from latest run
        # ---------------------------------------------------------

        blocks = (
            db.query(OptimizedBlock)
            .filter(
                OptimizedBlock.optimization_run_id
                == latest_run.optimization_run_id,
                OptimizedBlock.corridor_id
                == request.corridor_id,
                OptimizedBlock.block_date
                == request.unavailable_date,
            )
            .all()
        )

        # ---------------------------------------------------------
        # 4. Find affected blocks
        # ---------------------------------------------------------

        affected_blocks = []

        for block in blocks:

            block_start = time_to_minutes(
                block.start_time
            )

            block_end = time_to_minutes(
                block.end_time
            )

            # Overlap condition:
            #
            # Block starts before unavailable period ends
            # AND
            # Block ends after unavailable period starts

            if (
                block_start < unavailable_end
                and block_end > unavailable_start
            ):
                affected_blocks.append(
                    {
                        "optimized_block_id": (
                            block.optimized_block_id
                        ),
                        "start_time": (
                            block.start_time.strftime("%H:%M")
                        ),
                        "end_time": (
                            block.end_time.strftime("%H:%M")
                        ),
                        "duration_hours": (
                            block.duration_hours
                        ),
                        "department_count": (
                            block.department_count
                        ),
                        "optimization_score": (
                            block.optimization_score
                        ),
                    }
                )

            # 5. Find and rank intelligent alternative slots
        alternative_slots = []

        required_duration = unavailable_duration

        planning_start = 6 * 60
        planning_end = 22 * 60

        # Existing optimized blocks
        occupied_windows = []

        for block in blocks:
            block_start = time_to_minutes(block.start_time)
            block_end = time_to_minutes(block.end_time)

            occupied_windows.append(
                (block_start, block_end)
            )

        # Scenario's unavailable window
        occupied_windows.append(
            (
                unavailable_start,
                unavailable_end,
            )
        )

        # --------------------------------------------------------
        # Fetch operational data
        # --------------------------------------------------------

        trains = (
            db.query(Train)
            .filter(
                Train.corridor_id == request.corridor_id,
                Train.date == request.unavailable_date,
            )
            .all()
        )

        goods_forecasts = (
            db.query(GoodsForecast)
            .filter(
                GoodsForecast.corridor_id == request.corridor_id,
                GoodsForecast.date == request.unavailable_date,
            )
            .all()
        )

        current = planning_start

        while (
            current + required_duration <= planning_end
        ):

            candidate_start = current
            candidate_end = (
                current + required_duration
            )

            # ----------------------------------------------------
            # 1. Existing block conflict
            # ----------------------------------------------------

            occupied_conflict = any(
                candidate_start < occupied_end
                and candidate_end > occupied_start
                for occupied_start, occupied_end
                in occupied_windows
            )

            if occupied_conflict:
                current += 30
                continue

            # ----------------------------------------------------
            # 2. Train conflicts
            # ----------------------------------------------------

            candidate_start_time = minutes_to_time(
                candidate_start
            )

            candidate_end_time = minutes_to_time(
                candidate_end
            )

            train_conflicts = [
                train
                for train in trains
                if (
                    candidate_start_time < train.end_time
                    and train.start_time < candidate_end_time
                )
            ]

            # Train conflicts remain HARD constraints.
            if train_conflicts:
                current += 30
                continue

            # ----------------------------------------------------
            # 3. Goods forecast impact
            # ----------------------------------------------------

            goods_conflicts = [
                forecast
                for forecast in goods_forecasts
                if (
                    candidate_start_time < forecast.end_time
                    and forecast.start_time < candidate_end_time
                )
            ]

            expected_goods_trains = sum(
                getattr(
                    forecast,
                    "expected_goods_trains",
                    0,
                ) or 0
                for forecast in goods_conflicts
            )

            # ----------------------------------------------------
            # 4. Operational impact score
            # ----------------------------------------------------

            goods_penalty = (
                len(goods_conflicts) * 10
                + expected_goods_trains * 5
            )

            operational_score = max(
                0,
                100 - goods_penalty
            )

            # ----------------------------------------------------
            # 5. Temporal suitability
            # ----------------------------------------------------

            distance_from_requested = abs(
                candidate_start - unavailable_start
            )

            time_penalty = min(
                20,
                distance_from_requested / 60
            )

            final_score = max(
                0,
                round(
                    operational_score
                    - time_penalty,
                    2,
                )
            )

            # ----------------------------------------------------
            # 6. Slot classification
            # ----------------------------------------------------

            if final_score >= 85:
                status = "Recommended"
            elif final_score >= 70:
                status = "Good"
            else:
                status = "Moderate"

            alternative_slots.append(
                {
                    "start_time": candidate_start_time.strftime(
                        "%H:%M"
                    ),
                    "end_time": candidate_end_time.strftime(
                        "%H:%M"
                    ),
                    "score": final_score,
                    "status": status,
                    "train_conflicts": 0,
                    "goods_conflicts": len(
                        goods_conflicts
                    ),
                    "expected_goods_trains": (
                        expected_goods_trains
                    ),
                }
            )

            current += 30

        # --------------------------------------------------------
        # Rank best alternatives first
        # --------------------------------------------------------

        alternative_slots.sort(
            key=lambda slot: slot["score"],
            reverse=True,
        )

        # Keep top 7 recommendations
        alternative_slots = alternative_slots[:7]
                # ---------------------------------------------------------
        # Operational impact analysis
        # ---------------------------------------------------------

        affected_trains = [
            train
            for train in trains
            if (
                request.start_time < train.end_time
                and train.start_time
                < minutes_to_time(unavailable_end)
            )
        ]

        affected_goods_forecasts = [
            forecast
            for forecast in goods_forecasts
            if (
                request.start_time < forecast.end_time
                and forecast.start_time
                < minutes_to_time(unavailable_end)
            )
        ]

        expected_affected_goods_trains = sum(
            getattr(
                forecast,
                "expected_goods_trains",
                0,
            ) or 0
            for forecast in affected_goods_forecasts
        )

        # Determine operational risk
        if (
            len(affected_trains) >= 5
            or expected_affected_goods_trains >= 15
        ):
            operational_risk = "High"
        elif (
            len(affected_trains) > 0
            or expected_affected_goods_trains > 0
        ):
            operational_risk = "Medium"
        else:
            operational_risk = "Low"

        operational_impact = {
            "affected_trains": len(affected_trains),
            "goods_forecast_conflicts": len(
                affected_goods_forecasts
            ),
            "expected_goods_trains": (
                expected_affected_goods_trains
            ),
            "risk_level": operational_risk,
        }

        # ---------------------------------------------------------
        # 6. Generate recommendation
        # ---------------------------------------------------------

        affected_count = len(
            affected_blocks
        )
        # ---------------------------------------------------------
        # 6. Generate recommendation
        # ---------------------------------------------------------

        affected_count = len(
            affected_blocks
        )

        if affected_count == 0:

            recommendation = (
                "No existing optimized blocks are affected "
                "by this unavailability scenario."
            )

        elif alternative_slots:

            recommendation = (
                f"{affected_count} optimized block(s) "
                "are affected. Alternative maintenance "
                "windows are available."
            )

        else:

            recommendation = (
                f"{affected_count} optimized block(s) "
                "are affected, but no feasible alternative "
                "window was found."
            )

        # ---------------------------------------------------------
        # 7. Return simulation result
        # ---------------------------------------------------------

        return {
            "scenario": {
                "corridor_id": request.corridor_id,
                "unavailable_date": (
                    request.unavailable_date
                ),
                "start_time": (
                    request.start_time.strftime("%H:%M")
                ),
                "duration_hours": (
                    request.duration_hours
                ),
                "end_time": minutes_to_time(
                    unavailable_end
                ).strftime("%H:%M"),
                "scenario_type": (
                    request.scenario_type
                ),
            },
            "affected_blocks": affected_blocks,
            "affected_block_count": affected_count,
            "operational_impact": operational_impact,
            "alternative_slots": alternative_slots,
            "alternative_slot_count": (
                len(alternative_slots)
            ),
            "confidence": (
                90
                if affected_count > 0 and alternative_slots
                else 70
                if affected_count == 0
                else 40
            ),
            "recommendation": recommendation,
        }

    finally:
        db.close()