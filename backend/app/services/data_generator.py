
"""
Synthetic Railway Data Generator
================================

Generates realistic synthetic data for the
Railway Automatic Block Planning prototype.

Simulated source systems:

    TMS  -> Engineering assets, maintenance and defects
    SMMS -> S&T assets, maintenance and defects
    TDMS -> TRD assets, maintenance and defects
    COA  -> Corridor data, train timetable and goods forecast
    BDMS -> Maintenance block requests

All generated datasets maintain valid relationships
between assets, tasks, defects, corridors and block requests.
"""

from pathlib import Path
from datetime import date, datetime, timedelta
import random

import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

SEED = 42

random.seed(SEED)

PROJECT_ROOT = Path(__file__).resolve().parents[3]

RAW_DATA = PROJECT_ROOT / "data" / "raw"

TMS_DIR = RAW_DATA / "tms"
SMMS_DIR = RAW_DATA / "smms"
TDMS_DIR = RAW_DATA / "tdms"
COA_DIR = RAW_DATA / "coa"
BDMS_DIR = RAW_DATA / "bdms"


# ============================================================
# DATASET SIZE
# ============================================================

NUM_ASSETS_PER_DEPARTMENT = 100
NUM_MAINTENANCE_PER_DEPARTMENT = 150
NUM_DEFECTS_PER_DEPARTMENT = 60

NUM_TRAINS = 1000
NUM_BLOCK_REQUESTS = 300

START_DATE = date(2026, 9, 5)
NUM_DAYS = 30


# ============================================================
# REFERENCE DATA
# ============================================================

DEPARTMENTS = {
    "ENG": "Engineering",
    "SNT": "Signal & Telecommunication",
    "TRD": "Traction Distribution",
}


CORRIDORS = [
    {
        "corridor_id": "C001",
        "corridor_name": "Corridor A",
        "start_station": "Station A",
        "end_station": "Station B",
        "start_km": 100.0,
        "end_km": 125.0,
    },
    {
        "corridor_id": "C002",
        "corridor_name": "Corridor B",
        "start_station": "Station B",
        "end_station": "Station C",
        "start_km": 125.0,
        "end_km": 150.0,
    },
    {
        "corridor_id": "C003",
        "corridor_name": "Corridor C",
        "start_station": "Station C",
        "end_station": "Station D",
        "start_km": 150.0,
        "end_km": 175.0,
    },
    {
        "corridor_id": "C004",
        "corridor_name": "Corridor D",
        "start_station": "Station D",
        "end_station": "Station E",
        "start_km": 175.0,
        "end_km": 200.0,
    },
    {
        "corridor_id": "C005",
        "corridor_name": "Corridor E",
        "start_station": "Station E",
        "end_station": "Station F",
        "start_km": 200.0,
        "end_km": 225.0,
    },
]


ASSET_TYPES = {
    "ENG": [
        "Track",
        "Bridge",
        "Culvert",
        "Turnout",
        "Level Crossing",
    ],
    "SNT": [
        "Signal",
        "Point Machine",
        "Axle Counter",
        "Interlocking System",
        "Telecommunication Equipment",
    ],
    "TRD": [
        "OHE",
        "Transformer",
        "Section Insulator",
        "Circuit Breaker",
        "OHE Mast",
    ],
}


MAINTENANCE_TYPES = [
    "Preventive",
    "Corrective",
    "Inspection",
]


MAINTENANCE_TASK_TYPES = {
    "ENG": [
        "Track Inspection",
        "Track Repair",
        "Bridge Inspection",
        "Turnout Maintenance",
        "Level Crossing Inspection",
    ],
    "SNT": [
        "Signal Inspection",
        "Signal Maintenance",
        "Point Machine Maintenance",
        "Axle Counter Inspection",
        "Telecommunication Maintenance",
    ],
    "TRD": [
        "OHE Inspection",
        "OHE Maintenance",
        "Transformer Inspection",
        "Circuit Breaker Maintenance",
        "Section Insulator Inspection",
    ],
}


DEFECT_TYPES = {
    "ENG": [
        "Track Crack",
        "Rail Wear",
        "Ballast Defect",
        "Bridge Defect",
        "Turnout Defect",
    ],
    "SNT": [
        "Signal Failure",
        "Point Machine Failure",
        "Axle Counter Failure",
        "Interlocking Fault",
        "Communication Failure",
    ],
    "TRD": [
        "OHE Damage",
        "Transformer Fault",
        "Insulator Damage",
        "Circuit Breaker Fault",
        "OHE Mast Damage",
    ],
}


# ============================================================
# DIRECTORY CREATION
# ============================================================

def create_directories():
    """Create all required source-system directories."""

    directories = [
        TMS_DIR,
        SMMS_DIR,
        TDMS_DIR,
        COA_DIR,
        BDMS_DIR,
    ]

    for directory in directories:
        directory.mkdir(
            parents=True,
            exist_ok=True,
        )


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def random_date(start: date, days: int) -> date:
    """Generate a random date within the specified range."""

    return start + timedelta(
        days=random.randint(0, days)
    )


def minutes_to_time(minutes: int) -> str:
    """Convert minutes since midnight to HH:MM."""

    minutes = minutes % (24 * 60)

    hour = minutes // 60
    minute = minutes % 60

    return f"{hour:02d}:{minute:02d}"


def random_corridor():
    """Return a random corridor."""

    return random.choice(CORRIDORS)


def random_location(corridor):
    """Generate a random KM location inside a corridor."""

    return round(
        random.uniform(
            corridor["start_km"],
            corridor["end_km"],
        ),
        1,
    )


# ============================================================
# CORRIDOR GENERATION
# ============================================================

def generate_corridors():
    """
    Generate corridor reference data.

    This becomes an explicit COA input dataset.
    """

    rows = []

    for corridor in CORRIDORS:

        rows.append(
            {
                "corridor_id": corridor["corridor_id"],
                "corridor_name": corridor["corridor_name"],
                "start_station": corridor["start_station"],
                "end_station": corridor["end_station"],
                "start_km": corridor["start_km"],
                "end_km": corridor["end_km"],
                "length_km": round(
                    corridor["end_km"]
                    - corridor["start_km"],
                    1,
                ),
                "electrified": True,
                "status": "Operational",
            }
        )

    return pd.DataFrame(rows)


# ============================================================
# ASSET GENERATION
# ============================================================

def generate_assets(department: str):
    """
    Generate assets for a department.

    The first asset of every department is deliberately placed
    on C001. This guarantees the multi-department coordination
    scenario required by the optimizer demonstration.
    """

    rows = []

    for i in range(
        1,
        NUM_ASSETS_PER_DEPARTMENT + 1,
    ):

        # ----------------------------------------------------
        # Guarantee one C001 asset per department
        # ----------------------------------------------------

        if i == 1:
            corridor = CORRIDORS[0]

            # Put coordination assets near each other.
            coordination_locations = {
                "ENG": 120.0,
                "SNT": 120.5,
                "TRD": 121.0,
            }

            location_km = coordination_locations[
                department
            ]

        else:
            corridor = random_corridor()

            location_km = random_location(
                corridor
            )

        asset_id = f"{department}-A{i:03d}"

        asset_type = random.choice(
            ASSET_TYPES[department]
        )

        criticality = random.randint(
            4,
            10,
        )

        installation_date = (
            START_DATE
            - timedelta(
                days=random.randint(
                    365,
                    3650,
                )
            )
        )

        last_maintenance_date = (
            START_DATE
            - timedelta(
                days=random.randint(
                    10,
                    180,
                )
            )
        )

        next_maintenance_date = (
            last_maintenance_date
            + timedelta(
                days=random.randint(
                    30,
                    180,
                )
            )
        )

        status = random.choices(
            [
                "Operational",
                "Under Maintenance",
                "Failed",
            ],
            weights=[
                90,
                7,
                3,
            ],
        )[0]

        rows.append(
            {
                "asset_id": asset_id,
                "department": department,
                "department_name": DEPARTMENTS[
                    department
                ],
                "asset_type": asset_type,
                "corridor_id": corridor["corridor_id"],
                "location_km": location_km,
                "description": (
                    f"{asset_type} at KM "
                    f"{location_km}"
                ),
                "criticality": criticality,
                "installation_date": installation_date,
                "last_maintenance_date": (
                    last_maintenance_date
                ),
                "next_maintenance_date": (
                    next_maintenance_date
                ),
                "status": status,
            }
        )

    return pd.DataFrame(rows)


# ============================================================
# MAINTENANCE GENERATION
# ============================================================

def generate_maintenance_tasks(
    department: str,
    assets_df: pd.DataFrame,
):
    """Generate maintenance tasks linked to valid assets."""

    rows = []

    for i in range(
        1,
        NUM_MAINTENANCE_PER_DEPARTMENT + 1,
    ):

        # ----------------------------------------------------
        # Guarantee first maintenance task is linked to the
        # C001 coordination asset.
        # ----------------------------------------------------

        if i == 1:
            asset = assets_df.iloc[0]

        else:
            asset = assets_df.iloc[
                random.randrange(
                    len(assets_df)
                )
            ]

        task_id = f"{department}-T{i:03d}"

        task_type = random.choice(
            MAINTENANCE_TASK_TYPES[department]
        )

        maintenance_type = random.choice(
            MAINTENANCE_TYPES
        )

        created_date = random_date(
            START_DATE - timedelta(days=30),
            20,
        )

        due_date = (
            created_date
            + timedelta(
                days=random.randint(
                    2,
                    30,
                )
            )
        )

        duration = random.choice(
            [
                1.0,
                1.5,
                2.0,
                2.5,
                3.0,
                4.0,
            ]
        )

        required_team = {
            "ENG": "Engineering Maintenance Team",
            "SNT": "S&T Maintenance Team",
            "TRD": "TRD Maintenance Team",
        }[department]

        required_equipment = {
            "ENG": random.choice(
                [
                    "Inspection Vehicle",
                    "Track Machine",
                    "Maintenance Tools",
                ]
            ),
            "SNT": random.choice(
                [
                    "Signal Testing Kit",
                    "Electrical Testing Equipment",
                    "S&T Maintenance Tools",
                ]
            ),
            "TRD": random.choice(
                [
                    "OHE Tower Wagon",
                    "Electrical Testing Equipment",
                    "TRD Maintenance Tools",
                ]
            ),
        }[department]

        status = random.choices(
            [
                "Pending",
                "Scheduled",
                "Completed",
            ],
            weights=[
                65,
                20,
                15,
            ],
        )[0]

        rows.append(
            {
                "task_id": task_id,
                "department": department,
                "department_name": DEPARTMENTS[
                    department
                ],
                "asset_id": asset["asset_id"],
                "task_type": task_type,
                "maintenance_type": maintenance_type,
                "created_date": created_date,
                "due_date": due_date,
                "estimated_duration_hours": duration,
                "required_team": required_team,
                "required_equipment": required_equipment,
                "status": status,
            }
        )

    return pd.DataFrame(rows)


# ============================================================
# DEFECT GENERATION
# ============================================================

def generate_defects(
    department: str,
    assets_df: pd.DataFrame,
):
    """Generate defects linked to valid assets."""

    rows = []

    for i in range(
        1,
        NUM_DEFECTS_PER_DEPARTMENT + 1,
    ):

        asset = assets_df.iloc[
            random.randrange(
                len(assets_df)
            )
        ]

        defect_id = f"{department}-D{i:03d}"

        severity = random.choices(
            [
                "Low",
                "Medium",
                "High",
                "Critical",
            ],
            weights=[
                20,
                35,
                30,
                15,
            ],
        )[0]

        severity_score = {
            "Low": 3,
            "Medium": 5,
            "High": 8,
            "Critical": 10,
        }[severity]

        detected_date = random_date(
            START_DATE - timedelta(days=20),
            20,
        )

        target_resolution_date = (
            detected_date
            + timedelta(
                days=random.randint(
                    1,
                    10,
                )
            )
        )

        rows.append(
            {
                "defect_id": defect_id,
                "department": department,
                "department_name": DEPARTMENTS[
                    department
                ],
                "asset_id": asset["asset_id"],
                "defect_type": random.choice(
                    DEFECT_TYPES[department]
                ),
                "severity": severity,
                "severity_score": severity_score,
                "detected_date": detected_date,
                "target_resolution_date": (
                    target_resolution_date
                ),
                "estimated_repair_hours": random.choice(
                    [
                        1.0,
                        2.0,
                        3.0,
                        4.0,
                    ]
                ),
                "safety_risk": min(
                    10,
                    max(
                        1,
                        severity_score
                        + random.randint(
                            -2,
                            1,
                        ),
                    ),
                ),
                "operational_impact": random.randint(
                    3,
                    10,
                ),
                "status": random.choices(
                    [
                        "Open",
                        "Under Investigation",
                        "Resolved",
                    ],
                    weights=[
                        55,
                        25,
                        20,
                    ],
                )[0],
            }
        )

    return pd.DataFrame(rows)


# ============================================================
# TRAIN GENERATION
# ============================================================

def generate_trains():
    """Generate synthetic COA timetable records."""

    rows = []

    train_types = [
        "Express",
        "Passenger",
        "Goods",
        "Special",
    ]

    for i in range(
        1,
        NUM_TRAINS + 1,
    ):

        corridor = random_corridor()

        train_type = random.choice(
            train_types
        )

        start_minutes = random.randint(
            5 * 60,
            22 * 60,
        )

        duration = {
            "Express": random.randint(
                20,
                45,
            ),
            "Passenger": random.randint(
                25,
                60,
            ),
            "Goods": random.randint(
                40,
                90,
            ),
            "Special": random.randint(
                20,
                60,
            ),
        }[train_type]

        departure = minutes_to_time(
            start_minutes
        )

        arrival = minutes_to_time(
            start_minutes + duration
        )

        priority = {
            "Express": "High",
            "Passenger": "Medium",
            "Goods": "Low",
            "Special": "High",
        }[train_type]

        rows.append(
            {
                "train_id": f"TR-{i:04d}",
                "train_number": random.randint(
                    10000,
                    99999,
                ),
                "train_name": f"Train {i:04d}",
                "train_type": train_type,
                "corridor_id": corridor["corridor_id"],
                "date": random_date(
                    START_DATE,
                    NUM_DAYS - 1,
                ),
                "arrival_time": arrival,
                "departure_time": departure,
                "direction": random.choice(
                    [
                        "UP",
                        "DOWN",
                    ]
                ),
                "priority": priority,
            }
        )

    return pd.DataFrame(rows)


# ============================================================
# GOODS FORECAST GENERATION
# ============================================================

def generate_goods_forecast():
    """
    Generate synthetic goods-train forecasts.

    5 corridors × 30 days × 8 time windows = 1200? No.

    This implementation deliberately uses 4 windows per day:

        06:00-10:00
        10:00-14:00
        14:00-18:00
        18:00-22:00

    Therefore:

        5 × 30 × 4 = 600 rows
    """

    rows = []

    forecast_counter = 1

    time_windows = [
        ("06:00", "10:00"),
        ("10:00", "14:00"),
        ("14:00", "18:00"),
        ("18:00", "22:00"),
    ]

    for corridor in CORRIDORS:

        for day in range(
            NUM_DAYS
        ):

            current_date = (
                START_DATE
                + timedelta(days=day)
            )

            for start_time, end_time in time_windows:

                expected_goods = random.randint(
                    0,
                    5,
                )

                if expected_goods >= 4:
                    traffic_level = "High"

                elif expected_goods >= 2:
                    traffic_level = "Medium"

                else:
                    traffic_level = "Low"

                confidence = round(
                    random.uniform(
                        0.75,
                        0.98,
                    ),
                    2,
                )

                rows.append(
                    {
                        "forecast_id": (
                            f"GF-{forecast_counter:05d}"
                        ),
                        "corridor_id": (
                            corridor["corridor_id"]
                        ),
                        "date": current_date,
                        "time_window": (
                            f"{start_time}-{end_time}"
                        ),
                        "expected_goods_trains": (
                            expected_goods
                        ),
                        "traffic_level": (
                            traffic_level
                        ),
                        "forecast_confidence": (
                            confidence
                        ),
                    }
                )

                forecast_counter += 1

    return pd.DataFrame(rows)


# ============================================================
# BLOCK REQUEST GENERATION
# ============================================================

def generate_block_requests(
    all_assets: pd.DataFrame,
    all_maintenance: pd.DataFrame,
):
    """
    Generate synthetic BDMS block requests.

    The first three requests form a guaranteed
    multi-department coordination scenario:

        ENG -> C001 -> 10:00-12:00
        SNT -> C001 -> 10:30-11:30
        TRD -> C001 -> 11:00-13:00

    The relationship is:

        Block Request
             ↓
        Maintenance Task
             ↓
           Asset
             ↓
         Corridor
    """

    random.seed(SEED)

    requests = []

    # --------------------------------------------------------
    # Build lookup tables
    # --------------------------------------------------------

    asset_lookup = (
        all_assets
        .set_index("asset_id")
        .to_dict("index")
    )

    maintenance_lookup = (
        all_maintenance
        .set_index("task_id")
        .to_dict("index")
    )

    # --------------------------------------------------------
    # Guaranteed coordination tasks
    #
    # First asset and first task for each department were
    # deliberately created on C001.
    # --------------------------------------------------------

    coordination_tasks = {}

    for department in [
        "ENG",
        "SNT",
        "TRD",
    ]:

        department_tasks = all_maintenance[
            all_maintenance["department"]
            == department
        ]

        c001_tasks = department_tasks[
            department_tasks["asset_id"].map(
                all_assets.set_index(
                    "asset_id"
                )["corridor_id"]
            ) == "C001"
        ]

        if c001_tasks.empty:
            raise ValueError(
                f"No C001 maintenance task found "
                f"for department {department}."
            )

        coordination_tasks[department] = (
            c001_tasks.iloc[0]
        )

    # --------------------------------------------------------
    # Coordination times
    # --------------------------------------------------------

    coordination_times = {
        "ENG": ("10:00", "12:00"),
        "SNT": ("10:30", "11:30"),
        "TRD": ("11:00", "13:00"),
    }

    for department in [
        "ENG",
        "SNT",
        "TRD",
    ]:

        task = coordination_tasks[
            department
        ]

        asset = asset_lookup[
            task["asset_id"]
        ]

        start_time, end_time = (
            coordination_times[
                department
            ]
        )

        start_dt = datetime.strptime(
            start_time,
            "%H:%M",
        )

        end_dt = datetime.strptime(
            end_time,
            "%H:%M",
        )

        duration_hours = (
            end_dt - start_dt
        ).seconds / 3600

        requests.append(
            {
                "block_request_id": (
                    f"BR-{len(requests) + 1:04d}"
                ),
                "task_id": task["task_id"],
                "department": department,
                "department_name": DEPARTMENTS[
                    department
                ],
                "asset_id": task["asset_id"],
                "corridor_id": asset[
                    "corridor_id"
                ],
                "location_km": asset[
                    "location_km"
                ],
                "requested_date": (
                    START_DATE.isoformat()
                ),
                "start_time": start_time,
                "end_time": end_time,
                "duration_hours": (
                    duration_hours
                ),
                "reason": (
                    "Coordinated multi-department "
                    "maintenance"
                ),
                "status": "Pending",
            }
        )

    # --------------------------------------------------------
    # Exclude coordination tasks from random requests
    # --------------------------------------------------------

    coordination_task_ids = {
        task["task_id"]
        for task in coordination_tasks.values()
    }

    remaining_tasks = all_maintenance[
        ~all_maintenance["task_id"].isin(
            coordination_task_ids
        )
    ]

    # --------------------------------------------------------
    # Generate remaining requests
    # --------------------------------------------------------

    remaining_count = (
        NUM_BLOCK_REQUESTS
        - len(requests)
    )

    selected_tasks = remaining_tasks.sample(
        n=min(
            remaining_count,
            len(remaining_tasks),
        ),
        random_state=SEED,
    )

    for _, task in selected_tasks.iterrows():

        asset = asset_lookup[
            task["asset_id"]
        ]

        request_date = (
            START_DATE
            + timedelta(
                days=random.randint(
                    0,
                    NUM_DAYS - 1,
                )
            )
        )

        start_hour = random.randint(
            6,
            18,
        )

        duration = float(
            task[
                "estimated_duration_hours"
            ]
        )

        start_dt = datetime.combine(
            request_date,
            datetime.min.time(),
        ) + timedelta(
            hours=start_hour
        )

        end_dt = (
            start_dt
            + timedelta(
                hours=duration
            )
        )

        # Prevent crossing midnight.
        if end_dt.date() != request_date:

            end_dt = datetime.combine(
                request_date,
                datetime.min.time(),
            ) + timedelta(
                hours=23
            )

        duration_hours = (
            end_dt - start_dt
        ).seconds / 3600

        requests.append(
            {
                "block_request_id": (
                    f"BR-{len(requests) + 1:04d}"
                ),
                "task_id": task["task_id"],
                "department": task[
                    "department"
                ],
                "department_name": DEPARTMENTS[
                    task["department"]
                ],
                "asset_id": task["asset_id"],
                "corridor_id": asset[
                    "corridor_id"
                ],
                "location_km": asset[
                    "location_km"
                ],
                "requested_date": (
                    request_date.isoformat()
                ),
                "start_time": (
                    start_dt.strftime("%H:%M")
                ),
                "end_time": (
                    end_dt.strftime("%H:%M")
                ),
                "duration_hours": round(
                    duration_hours,
                    2,
                ),
                "reason": (
                    "Maintenance block request"
                ),
                "status": random.choice(
                    [
                        "Pending",
                        "Pending",
                        "Approved",
                        "Under Review",
                    ]
                ),
            }
        )

    return pd.DataFrame(requests)


# ============================================================
# SAVE FUNCTION
# ============================================================

def save_dataframe(
    dataframe: pd.DataFrame,
    directory: Path,
    filename: str,
):
    """Save a DataFrame as CSV."""

    directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    path = directory / filename

    dataframe.to_csv(
        path,
        index=False,
    )

    print(
        f"Created: {path} "
        f"({len(dataframe)} rows)"
    )


# ============================================================
# VALIDATION
# ============================================================

def validate_data(
    all_assets: pd.DataFrame,
    all_maintenance: pd.DataFrame,
    all_defects: pd.DataFrame,
    block_requests: pd.DataFrame,
    trains: pd.DataFrame,
    goods_forecast: pd.DataFrame,
    corridors: pd.DataFrame,
):
    """
    Validate relationships and important constraints.
    """

    print("\nRunning data validation...")

    # --------------------------------------------------------
    # Basic row-count validation
    # --------------------------------------------------------

    assert len(all_assets) == (
        NUM_ASSETS_PER_DEPARTMENT * 3
    ), "Unexpected asset count."

    assert len(all_maintenance) == (
        NUM_MAINTENANCE_PER_DEPARTMENT * 3
    ), "Unexpected maintenance count."

    assert len(all_defects) == (
        NUM_DEFECTS_PER_DEPARTMENT * 3
    ), "Unexpected defect count."

    assert len(trains) == NUM_TRAINS, (
        "Unexpected train count."
    )

    assert len(goods_forecast) == 600, (
        "Goods forecast should contain 600 rows."
    )

    assert len(block_requests) == (
        NUM_BLOCK_REQUESTS
    ), "Unexpected block request count."

    # --------------------------------------------------------
    # Unique ID validation
    # --------------------------------------------------------

    assert all_assets["asset_id"].is_unique, (
        "Duplicate asset IDs found."
    )

    assert all_maintenance[
        "task_id"
    ].is_unique, (
        "Duplicate maintenance task IDs found."
    )

    assert all_defects[
        "defect_id"
    ].is_unique, (
        "Duplicate defect IDs found."
    )

    assert trains[
        "train_id"
    ].is_unique, (
        "Duplicate train IDs found."
    )

    assert goods_forecast[
        "forecast_id"
    ].is_unique, (
        "Duplicate forecast IDs found."
    )

    assert block_requests[
        "block_request_id"
    ].is_unique, (
        "Duplicate block request IDs found."
    )

    # --------------------------------------------------------
    # Valid corridor IDs
    # --------------------------------------------------------

    valid_corridors = {
        corridor["corridor_id"]
        for corridor in CORRIDORS
    }

    assert set(
        all_assets["corridor_id"]
    ).issubset(
        valid_corridors
    ), "Invalid corridor in assets."

    assert set(
        trains["corridor_id"]
    ).issubset(
        valid_corridors
    ), "Invalid corridor in trains."

    assert set(
        goods_forecast["corridor_id"]
    ).issubset(
        valid_corridors
    ), "Invalid corridor in goods forecast."

    assert set(
        block_requests["corridor_id"]
    ).issubset(
        valid_corridors
    ), "Invalid corridor in block requests."

    # --------------------------------------------------------
    # Asset relationships
    # --------------------------------------------------------

    asset_ids = set(
        all_assets["asset_id"]
    )

    invalid_maintenance_assets = (
        set(all_maintenance["asset_id"])
        - asset_ids
    )

    invalid_defect_assets = (
        set(all_defects["asset_id"])
        - asset_ids
    )

    assert not invalid_maintenance_assets, (
        "Invalid asset IDs found in maintenance."
    )

    assert not invalid_defect_assets, (
        "Invalid asset IDs found in defects."
    )

    # --------------------------------------------------------
    # Block request → task validation
    # --------------------------------------------------------

    maintenance_task_ids = set(
        all_maintenance["task_id"]
    )

    request_task_ids = set(
        block_requests["task_id"]
    )

    invalid_request_tasks = (
        request_task_ids
        - maintenance_task_ids
    )

    assert not invalid_request_tasks, (
        "Invalid task IDs found in block requests."
    )

    # --------------------------------------------------------
    # Block Request → Task → Asset → Corridor
    # --------------------------------------------------------

    asset_lookup = (
        all_assets[
            [
                "asset_id",
                "corridor_id",
                "location_km",
            ]
        ]
        .set_index("asset_id")
        .to_dict("index")
    )

    maintenance_lookup = (
        all_maintenance[
            [
                "task_id",
                "asset_id",
                "department",
            ]
        ]
        .set_index("task_id")
        .to_dict("index")
    )

    for _, request in block_requests.iterrows():

        request_id = request[
            "block_request_id"
        ]

        task_id = request[
            "task_id"
        ]

        task = maintenance_lookup[
            task_id
        ]

        asset_id = task[
            "asset_id"
        ]

        asset = asset_lookup[
            asset_id
        ]

        expected_corridor = asset[
            "corridor_id"
        ]

        actual_corridor = request[
            "corridor_id"
        ]

        assert (
            expected_corridor
            == actual_corridor
        ), (
            f"Corridor mismatch for "
            f"{request_id}: "
            f"expected {expected_corridor}, "
            f"got {actual_corridor}"
        )

        expected_location = asset[
            "location_km"
        ]

        actual_location = request[
            "location_km"
        ]

        assert (
            expected_location
            == actual_location
        ), (
            f"Location mismatch for "
            f"{request_id}: "
            f"expected {expected_location}, "
            f"got {actual_location}"
        )

    # --------------------------------------------------------
    # Coordination scenario validation
    # --------------------------------------------------------

    coordination = block_requests[
        block_requests[
            "block_request_id"
        ].isin(
            [
                "BR-0001",
                "BR-0002",
                "BR-0003",
            ]
        )
    ]

    assert len(coordination) == 3, (
        "Coordination scenario is incomplete."
    )

    assert set(
        coordination["department"]
    ) == {
        "ENG",
        "SNT",
        "TRD",
    }, (
        "Coordination scenario must contain "
        "ENG, SNT and TRD."
    )

    assert set(
        coordination["corridor_id"]
    ) == {
        "C001"
    }, (
        "Coordination scenario must be on C001."
    )

    # --------------------------------------------------------
    # Exact coordination times
    # --------------------------------------------------------

    expected_times = {
        "ENG": ("10:00", "12:00"),
        "SNT": ("10:30", "11:30"),
        "TRD": ("11:00", "13:00"),
    }

    for _, row in coordination.iterrows():

        department = row[
            "department"
        ]

        expected_start, expected_end = (
            expected_times[department]
        )

        assert row[
            "start_time"
        ] == expected_start

        assert row[
            "end_time"
        ] == expected_end

    # --------------------------------------------------------
    # Goods forecast structure
    # --------------------------------------------------------

    expected_forecast_rows = (
        len(CORRIDORS)
        * NUM_DAYS
        * 4
    )

    assert len(goods_forecast) == (
        expected_forecast_rows
    ), (
        "Unexpected goods forecast structure."
    )

    # --------------------------------------------------------
    # Date validation
    # --------------------------------------------------------

    assert all(
        pd.to_datetime(
            block_requests[
                "requested_date"
            ]
        ).dt.date
        >= START_DATE
    ), (
        "Block request date before planning period."
    )

    # --------------------------------------------------------
    # Success
    # --------------------------------------------------------

    print(
        "✓ Asset → Maintenance relationships valid"
    )

    print(
        "✓ Asset → Defect relationships valid"
    )

    print(
        "✓ Block Request → Task relationships valid"
    )

    print(
        "✓ Block Request → Asset relationships valid"
    )

    print(
        "✓ Block Request → Corridor relationships valid"
    )

    print(
        "✓ C001 multi-department scenario valid"
    )

    print(
        "✓ Train timetable data valid"
    )

    print(
        "✓ Goods forecast data valid"
    )

    print(
        "Data validation successful."
    )


# ============================================================
# MAIN GENERATION FUNCTION
# ============================================================

def generate_all_data():

    print("=" * 65)
    print("RAILWAY AUTOMATIC BLOCK PLANNING")
    print("Synthetic Data Generator")
    print("=" * 65)

    print(
        f"Project root : {PROJECT_ROOT}"
    )

    print(
        f"Random seed  : {SEED}"
    )

    create_directories()

    # ========================================================
    # TMS
    # ========================================================

    print(
        "\n[1/5] Generating TMS data..."
    )

    eng_assets = generate_assets(
        "ENG"
    )

    eng_maintenance = (
        generate_maintenance_tasks(
            "ENG",
            eng_assets,
        )
    )

    eng_defects = generate_defects(
        "ENG",
        eng_assets,
    )

    save_dataframe(
        eng_assets,
        TMS_DIR,
        "assets.csv",
    )

    save_dataframe(
        eng_maintenance,
        TMS_DIR,
        "maintenance.csv",
    )

    save_dataframe(
        eng_defects,
        TMS_DIR,
        "defects.csv",
    )

    # ========================================================
    # SMMS
    # ========================================================

    print(
        "\n[2/5] Generating SMMS data..."
    )

    snt_assets = generate_assets(
        "SNT"
    )

    snt_maintenance = (
        generate_maintenance_tasks(
            "SNT",
            snt_assets,
        )
    )

    snt_defects = generate_defects(
        "SNT",
        snt_assets,
    )

    save_dataframe(
        snt_assets,
        SMMS_DIR,
        "assets.csv",
    )

    save_dataframe(
        snt_maintenance,
        SMMS_DIR,
        "maintenance.csv",
    )

    save_dataframe(
        snt_defects,
        SMMS_DIR,
        "defects.csv",
    )

    # ========================================================
    # TDMS
    # ========================================================

    print(
        "\n[3/5] Generating TDMS data..."
    )

    trd_assets = generate_assets(
        "TRD"
    )

    trd_maintenance = (
        generate_maintenance_tasks(
            "TRD",
            trd_assets,
        )
    )

    trd_defects = generate_defects(
        "TRD",
        trd_assets,
    )

    save_dataframe(
        trd_assets,
        TDMS_DIR,
        "assets.csv",
    )

    save_dataframe(
        trd_maintenance,
        TDMS_DIR,
        "maintenance.csv",
    )

    save_dataframe(
        trd_defects,
        TDMS_DIR,
        "defects.csv",
    )

    # ========================================================
    # COMBINE SOURCE DATA
    # ========================================================

    all_assets = pd.concat(
        [
            eng_assets,
            snt_assets,
            trd_assets,
        ],
        ignore_index=True,
    )

    all_maintenance = pd.concat(
        [
            eng_maintenance,
            snt_maintenance,
            trd_maintenance,
        ],
        ignore_index=True,
    )

    all_defects = pd.concat(
        [
            eng_defects,
            snt_defects,
            trd_defects,
        ],
        ignore_index=True,
    )

    # ========================================================
    # COA
    # ========================================================

    print(
        "\n[4/5] Generating COA data..."
    )

    corridors = generate_corridors()

    trains = generate_trains()

    goods_forecast = (
        generate_goods_forecast()
    )

    save_dataframe(
        corridors,
        COA_DIR,
        "corridors.csv",
    )

    save_dataframe(
        trains,
        COA_DIR,
        "trains.csv",
    )

    save_dataframe(
        goods_forecast,
        COA_DIR,
        "goods_forecast.csv",
    )

    # ========================================================
    # BDMS
    # ========================================================

    print(
        "\n[5/5] Generating BDMS data..."
    )

    block_requests = (
        generate_block_requests(
            all_assets,
            all_maintenance,
        )
    )

    save_dataframe(
        block_requests,
        BDMS_DIR,
        "block_requests.csv",
    )

    # ========================================================
    # VALIDATION
    # ========================================================

    validate_data(
        all_assets,
        all_maintenance,
        all_defects,
        block_requests,
        trains,
        goods_forecast,
        corridors,
    )

    # ========================================================
    # SUMMARY
    # ========================================================

    print(
        "\n" + "=" * 65
    )

    print(
        "DATA GENERATION COMPLETED SUCCESSFULLY"
    )

    print(
        "=" * 65
    )

    print(
        f"Engineering assets : {len(eng_assets)}"
    )

    print(
        f"S&T assets         : {len(snt_assets)}"
    )

    print(
        f"TRD assets         : {len(trd_assets)}"
    )

    print(
        f"Total assets       : {len(all_assets)}"
    )

    print(
        f"Total maintenance  : "
        f"{len(all_maintenance)}"
    )

    print(
        f"Total defects      : "
        f"{len(all_defects)}"
    )

    print(
        f"Total corridors    : "
        f"{len(corridors)}"
    )

    print(
        f"Total trains       : "
        f"{len(trains)}"
    )

    print(
        f"Goods forecasts    : "
        f"{len(goods_forecast)}"
    )

    print(
        f"Block requests     : "
        f"{len(block_requests)}"
    )

    print(
        "\n✓ All relationships validated."
    )

    print(
        "✓ Synthetic railway dataset is ready."
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    generate_all_data()

