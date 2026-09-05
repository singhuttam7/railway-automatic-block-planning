from pathlib import Path

import pandas as pd
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models import (
    Department,
    Corridor,
    Asset,
    MaintenanceTask,
    Defect,
    Train,
    GoodsForecast,
    BlockRequest,
)


# =========================================================
# PROJECT PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parents[3]

DATA_DIR = BASE_DIR / "data" / "raw"


# =========================================================
# CSV LOADER
# =========================================================

def load_csv(path: Path) -> pd.DataFrame:
    """Load a CSV file."""

    if not path.exists():
        raise FileNotFoundError(
            f"CSV file not found: {path}"
        )

    return pd.read_csv(path)


# =========================================================
# LOAD DATA
# =========================================================

def load_data(db: Session):

    print("\n🚂 Starting railway dataset loading...\n")


    # =====================================================
    # 1. DEPARTMENTS
    # =====================================================

    departments = [
        {
            "department_id": "ENG",
            "department_name": "Engineering",
        },
        {
            "department_id": "SNT",
            "department_name": "Signal & Telecommunication",
        },
        {
            "department_id": "TRD",
            "department_name": "Traction Distribution",
        },
    ]

    department_count = 0

    for data in departments:

        if not db.get(
            Department,
            data["department_id"]
        ):

            db.add(
                Department(**data)
            )

            department_count += 1

    db.commit()

    print(
        f"✅ Departments loaded: {department_count}"
    )


    # =====================================================
    # 2. CORRIDORS
    # =====================================================

    corridors_df = load_csv(
        DATA_DIR / "coa" / "corridors.csv"
    )

    corridor_count = 0

    for _, row in corridors_df.iterrows():

        corridor_id = row["corridor_id"]

        if not db.get(
            Corridor,
            corridor_id
        ):

            db.add(
                Corridor(
                    corridor_id=corridor_id,
                    corridor_name=row["corridor_name"],
                    start_km=float(
                        row["start_km"]
                    ),
                    end_km=float(
                        row["end_km"]
                    ),
                )
            )

            corridor_count += 1

    db.commit()

    print(
        f"✅ Corridors loaded: {corridor_count}"
    )


    # =====================================================
    # 3. ASSETS
    # =====================================================

    asset_count = 0

    for department in [
        "tms",
        "smms",
        "tdms",
    ]:

        file_path = (
            DATA_DIR
            / department
            / "assets.csv"
        )

        df = load_csv(file_path)

        for _, row in df.iterrows():

            asset_id = row["asset_id"]

            if not db.get(
                Asset,
                asset_id
            ):

                db.add(
                    Asset(
                        asset_id=asset_id,

                        department_id=row[
                            "department"
                        ],

                        asset_type=row[
                            "asset_type"
                        ],

                        corridor_id=row[
                            "corridor_id"
                        ],

                        location_km=float(
                            row["location_km"]
                        ),

                        description=row[
                            "description"
                        ],

                        criticality=int(
                            row["criticality"]
                        ),

                        installation_date=pd.to_datetime(
                            row["installation_date"]
                        ).date(),

                        last_maintenance_date=pd.to_datetime(
                            row[
                                "last_maintenance_date"
                            ]
                        ).date(),

                        next_maintenance_date=pd.to_datetime(
                            row[
                                "next_maintenance_date"
                            ]
                        ).date(),

                        status=row["status"],
                    )
                )

                asset_count += 1

        db.commit()

    print(
        f"✅ Assets loaded: {asset_count}"
    )


    # =====================================================
    # 4. MAINTENANCE TASKS
    # =====================================================

    task_count = 0

    for department in [
        "tms",
        "smms",
        "tdms",
    ]:

        file_path = (
            DATA_DIR
            / department
            / "maintenance.csv"
        )

        df = load_csv(file_path)

        for _, row in df.iterrows():

            task_id = row["task_id"]

            if not db.get(
                MaintenanceTask,
                task_id
            ):

                db.add(
                    MaintenanceTask(
                        task_id=task_id,

                        asset_id=row[
                            "asset_id"
                        ],

                        task_type=row[
                            "task_type"
                        ],

                        # Priority will be calculated
                        # later by the AI engine.
                        priority=0,

                        due_date=pd.to_datetime(
                            row["due_date"]
                        ).date(),

                        estimated_duration_hours=float(
                            row[
                                "estimated_duration_hours"
                            ]
                        ),

                        status=row["status"],
                    )
                )

                task_count += 1

        db.commit()

    print(
        f"✅ Maintenance tasks loaded: {task_count}"
    )


    # =====================================================
    # 5. DEFECTS
    # =====================================================

    defect_count = 0

    for department in [
        "tms",
        "smms",
        "tdms",
    ]:

        file_path = (
            DATA_DIR
            / department
            / "defects.csv"
        )

        df = load_csv(file_path)

        for _, row in df.iterrows():

            defect_id = row["defect_id"]

            if not db.get(
                Defect,
                defect_id
            ):

                db.add(
                    Defect(
                        defect_id=defect_id,

                        asset_id=row[
                            "asset_id"
                        ],

                        defect_type=row[
                            "defect_type"
                        ],

                        severity=row[
                            "severity"
                        ],

                        severity_score=int(
                            row[
                                "severity_score"
                            ]
                        ),

                        detected_date=pd.to_datetime(
                            row[
                                "detected_date"
                            ]
                        ).date(),

                        target_resolution_date=pd.to_datetime(
                            row[
                                "target_resolution_date"
                            ]
                        ).date(),

                        estimated_repair_hours=int(
                            row[
                                "estimated_repair_hours"
                            ]
                        ),

                        safety_risk=int(
                            row[
                                "safety_risk"
                            ]
                        ),

                        operational_impact=int(
                            row[
                                "operational_impact"
                            ]
                        ),

                        status=row["status"],
                    )
                )

                defect_count += 1

        db.commit()

    print(
        f"✅ Defects loaded: {defect_count}"
    )


    # =====================================================
    # 6. TRAINS
    # =====================================================

    trains_df = load_csv(
        DATA_DIR / "coa" / "trains.csv"
    )

    train_count = 0

    for _, row in trains_df.iterrows():

        train_id = row["train_id"]

        if not db.get(
            Train,
            train_id
        ):

            db.add(
                Train(
                    train_id=train_id,

                    corridor_id=row[
                        "corridor_id"
                    ],

                    train_number=str(
                        row["train_number"]
                    ),

                    train_type=row[
                        "train_type"
                    ],

                    date=pd.to_datetime(
                        row["date"]
                    ).date(),

                    # CSV:
                    # arrival_time
                    #
                    # Database:
                    # start_time
                    start_time=pd.to_datetime(
                        row["departure_time"]
                    ).time(),

                    # CSV:
                    # departure_time
                    #
                    # Database:
                    # end_time
                    end_time=pd.to_datetime(
                        row["arrival_time"]
                    ).time(),
                )
            )

            train_count += 1

    db.commit()

    print(
        f"✅ Trains loaded: {train_count}"
    )


    # =====================================================
    # 7. GOODS FORECAST
    # =====================================================

    forecast_df = load_csv(
        DATA_DIR
        / "coa"
        / "goods_forecast.csv"
    )

    forecast_count = 0

    for _, row in forecast_df.iterrows():

        forecast_id = row["forecast_id"]

        if not db.get(
            GoodsForecast,
            forecast_id
        ):

            # ---------------------------------------------
            # Parse time_window
            #
            # Example:
            # "06:00-10:00"
            #
            # becomes:
            # start_time = 06:00
            # end_time   = 10:00
            # ---------------------------------------------

            time_window = str(
                row["time_window"]
            ).strip()

            start_time_str, end_time_str = (
                time_window.split("-")
            )

            start_time = pd.to_datetime(
                start_time_str.strip(),
                format="%H:%M"
            ).time()

            end_time = pd.to_datetime(
                end_time_str.strip(),
                format="%H:%M"
            ).time()

            db.add(
                GoodsForecast(
                    forecast_id=forecast_id,

                    corridor_id=row[
                        "corridor_id"
                    ],

                    date=pd.to_datetime(
                        row["date"]
                    ).date(),

                    start_time=start_time,

                    end_time=end_time,

                    expected_goods_trains=int(
                        row[
                            "expected_goods_trains"
                        ]
                    ),
                )
            )

            forecast_count += 1

    db.commit()

    print(
        f"✅ Goods forecasts loaded: {forecast_count}"
    )


    # =====================================================
    # 8. BLOCK REQUESTS
    # =====================================================

    block_df = load_csv(
        DATA_DIR
        / "bdms"
        / "block_requests.csv"
    )

    block_count = 0

    for _, row in block_df.iterrows():

        block_request_id = row[
            "block_request_id"
        ]

        if not db.get(
            BlockRequest,
            block_request_id
        ):

            db.add(
                BlockRequest(
                    block_request_id=block_request_id,

                    task_id=row[
                        "task_id"
                    ],

                    corridor_id=row[
                        "corridor_id"
                    ],

                    location_km=float(
                        row["location_km"]
                    ),

                    requested_date=pd.to_datetime(
                        row[
                            "requested_date"
                        ]
                    ).date(),

                    start_time=pd.to_datetime(
                        row["start_time"]
                    ).time(),

                    end_time=pd.to_datetime(
                        row["end_time"]
                    ).time(),

                    duration_hours=float(
                        row[
                            "duration_hours"
                        ]
                    ),

                    reason=row[
                        "reason"
                    ],

                    status=row[
                        "status"
                    ],
                )
            )

            block_count += 1

    db.commit()

    print(
        f"✅ Block requests loaded: {block_count}"
    )


    # =====================================================
    # COMPLETION
    # =====================================================

    print(
        "\n🎉 DATA LOADING COMPLETED!\n"
    )


# =========================================================
# MAIN
# =========================================================

def main():

    db = SessionLocal()

    try:

        load_data(db)

    except Exception as e:

        db.rollback()

        print(
            "\n❌ DATA LOADING FAILED"
        )

        print(
            f"Error: {e}"
        )

        raise

    finally:

        db.close()


# =========================================================
# ENTRY POINT
# =========================================================

if __name__ == "__main__":
    main()