
from pathlib import Path
import pandas as pd


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

RAW_DIR = PROJECT_ROOT / "data" / "raw"

TMS_DIR = RAW_DIR / "tms"
SMMS_DIR = RAW_DIR / "smms"
TDMS_DIR = RAW_DIR / "tdms"
COA_DIR = RAW_DIR / "coa"
BDMS_DIR = RAW_DIR / "bdms"


# ============================================================
# EXPECTED COUNTS
# ============================================================

EXPECTED_COUNTS = {
    "tms/assets.csv": 100,
    "tms/maintenance.csv": 150,
    "tms/defects.csv": 60,

    "smms/assets.csv": 100,
    "smms/maintenance.csv": 150,
    "smms/defects.csv": 60,

    "tdms/assets.csv": 100,
    "tdms/maintenance.csv": 150,
    "tdms/defects.csv": 60,

    "coa/corridors.csv": 5,
    "coa/trains.csv": 1000,
    "coa/goods_forecast.csv": 600,

    "bdms/block_requests.csv": 300,
}


EXPECTED_DEPARTMENTS = {
    "ENG",
    "SNT",
    "TRD",
}

EXPECTED_CORRIDORS = {
    "C001",
    "C002",
    "C003",
    "C004",
    "C005",
}


# ============================================================
# LOAD DATA
# ============================================================

def load_data():
    files = {
        "tms_assets": TMS_DIR / "assets.csv",
        "tms_maintenance": TMS_DIR / "maintenance.csv",
        "tms_defects": TMS_DIR / "defects.csv",

        "smms_assets": SMMS_DIR / "assets.csv",
        "smms_maintenance": SMMS_DIR / "maintenance.csv",
        "smms_defects": SMMS_DIR / "defects.csv",

        "tdms_assets": TDMS_DIR / "assets.csv",
        "tdms_maintenance": TDMS_DIR / "maintenance.csv",
        "tdms_defects": TDMS_DIR / "defects.csv",

        "corridors": COA_DIR / "corridors.csv",
        "trains": COA_DIR / "trains.csv",
        "goods_forecast": COA_DIR / "goods_forecast.csv",

        "block_requests": BDMS_DIR / "block_requests.csv",
    }

    data = {}

    print("\n" + "=" * 70)
    print("LOADING DATA")
    print("=" * 70)

    for name, path in files.items():

        if not path.exists():
            print(f"❌ MISSING: {path}")
            continue

        df = pd.read_csv(path)
        data[name] = df

        print(f"✓ {name:<22} {len(df):>5} rows")

    return data


# ============================================================
# BASIC INSPECTION
# ============================================================

def inspect_basic(data):

    print("\n" + "=" * 70)
    print("1. BASIC DATA INSPECTION")
    print("=" * 70)

    for name, df in data.items():

        print(f"\n--- {name} ---")

        print(f"Rows    : {len(df)}")
        print(f"Columns : {len(df.columns)}")

        print("Columns:")
        print(list(df.columns))

        print("\nData types:")
        print(df.dtypes.to_string())


# ============================================================
# ROW COUNT CHECK
# ============================================================

def inspect_counts(data):

    print("\n" + "=" * 70)
    print("2. ROW COUNT VALIDATION")
    print("=" * 70)

    passed = True

    for path_key, expected in EXPECTED_COUNTS.items():

        name = path_key.replace("/", "_").replace(".csv", "")

        matching_key = None

        for key in data:
            if path_key.endswith(key.replace("_", "/") + ".csv"):
                matching_key = key

        # Explicit mapping
        mapping = {
            "tms/assets.csv": "tms_assets",
            "tms/maintenance.csv": "tms_maintenance",
            "tms/defects.csv": "tms_defects",

            "smms/assets.csv": "smms_assets",
            "smms/maintenance.csv": "smms_maintenance",
            "smms/defects.csv": "smms_defects",

            "tdms/assets.csv": "tdms_assets",
            "tdms/maintenance.csv": "tdms_maintenance",
            "tdms/defects.csv": "tdms_defects",

            "coa/corridors.csv": "corridors",
            "coa/trains.csv": "trains",
            "coa/goods_forecast.csv": "goods_forecast",

            "bdms/block_requests.csv": "block_requests",
        }

        matching_key = mapping[path_key]

        if matching_key not in data:
            print(f"❌ {path_key}: file missing")
            passed = False
            continue

        actual = len(data[matching_key])

        if actual == expected:
            print(f"✓ {path_key:<30} {actual}")
        else:
            print(
                f"❌ {path_key:<30} "
                f"expected={expected}, actual={actual}"
            )
            passed = False

    return passed


# ============================================================
# MISSING VALUES
# ============================================================

def inspect_missing_values(data):

    print("\n" + "=" * 70)
    print("3. MISSING VALUE CHECK")
    print("=" * 70)

    passed = True

    for name, df in data.items():

        missing = df.isnull().sum()
        missing = missing[missing > 0]

        if len(missing) == 0:
            print(f"✓ {name}: no missing values")
        else:
            passed = False
            print(f"\n❌ {name} has missing values:")

            for column, count in missing.items():
                percentage = count / len(df) * 100
                print(
                    f"   {column}: {count} "
                    f"({percentage:.2f}%)"
                )

    return passed


# ============================================================
# DUPLICATE CHECK
# ============================================================

def inspect_duplicates(data):

    print("\n" + "=" * 70)
    print("4. DUPLICATE ID CHECK")
    print("=" * 70)

    id_columns = {
        "tms_assets": "asset_id",
        "smms_assets": "asset_id",
        "tdms_assets": "asset_id",

        "tms_maintenance": "task_id",
        "smms_maintenance": "task_id",
        "tdms_maintenance": "task_id",

        "tms_defects": "defect_id",
        "smms_defects": "defect_id",
        "tdms_defects": "defect_id",

        "corridors": "corridor_id",
        "trains": "train_id",
        "goods_forecast": "forecast_id",
        "block_requests": "block_request_id",
    }

    passed = True

    for name, id_column in id_columns.items():

        if name not in data:
            continue

        df = data[name]

        duplicate_count = df[id_column].duplicated().sum()

        if duplicate_count == 0:
            print(f"✓ {name}: no duplicate {id_column}")
        else:
            passed = False
            print(
                f"❌ {name}: "
                f"{duplicate_count} duplicate {id_column}"
            )

            print(
                df[
                    df[id_column].duplicated(keep=False)
                ][[id_column]].to_string(index=False)
            )

    return passed


# ============================================================
# DEPARTMENT CHECK
# ============================================================

def inspect_departments(data):

    print("\n" + "=" * 70)
    print("5. DEPARTMENT VALIDATION")
    print("=" * 70)

    passed = True

    for name, df in data.items():

        if "department" not in df.columns:
            continue

        invalid = set(df["department"].dropna()) - EXPECTED_DEPARTMENTS

        if not invalid:
            print(f"✓ {name}: valid departments")
        else:
            passed = False
            print(
                f"❌ {name}: invalid departments -> "
                f"{invalid}"
            )

        print(
            df["department"]
            .value_counts()
            .sort_index()
            .to_string()
        )

    return passed


# ============================================================
# CORRIDOR CHECK
# ============================================================

def inspect_corridors(data):

    print("\n" + "=" * 70)
    print("6. CORRIDOR VALIDATION")
    print("=" * 70)

    passed = True

    for name, df in data.items():

        if "corridor_id" not in df.columns:
            continue

        invalid = (
            set(df["corridor_id"].dropna())
            - EXPECTED_CORRIDORS
        )

        if not invalid:
            print(f"✓ {name}: valid corridors")
        else:
            passed = False
            print(
                f"❌ {name}: invalid corridors -> "
                f"{invalid}"
            )

        print(
            df["corridor_id"]
            .value_counts()
            .sort_index()
            .to_string()
        )

    return passed


# ============================================================
# ASSET RELATIONSHIPS
# ============================================================

def inspect_asset_relationships(data):

    print("\n" + "=" * 70)
    print("7. ASSET RELATIONSHIP VALIDATION")
    print("=" * 70)

    passed = True

    for department, prefix in [
        ("ENG", "tms"),
        ("SNT", "smms"),
        ("TRD", "tdms"),
    ]:

        assets = data[f"{prefix}_assets"]
        maintenance = data[f"{prefix}_maintenance"]
        defects = data[f"{prefix}_defects"]

        asset_ids = set(assets["asset_id"])

        invalid_tasks = set(
            maintenance["asset_id"]
        ) - asset_ids

        invalid_defects = set(
            defects["asset_id"]
        ) - asset_ids

        if invalid_tasks:
            print(
                f"❌ {department}: maintenance references "
                f"unknown assets: {invalid_tasks}"
            )
            passed = False
        else:
            print(
                f"✓ {department}: all maintenance assets valid"
            )

        if invalid_defects:
            print(
                f"❌ {department}: defects reference "
                f"unknown assets: {invalid_defects}"
            )
            passed = False
        else:
            print(
                f"✓ {department}: all defect assets valid"
            )

    return passed


# ============================================================
# MAINTENANCE RELATIONSHIP
# ============================================================


def inspect_maintenance_relationships(data):

    print("\n" + "=" * 70)
    print("8. MAINTENANCE RELATIONSHIP VALIDATION")
    print("=" * 70)

    overall_passed = True

    for prefix in ["tms", "smms", "tdms"]:

        assets = data[f"{prefix}_assets"]
        maintenance = data[f"{prefix}_maintenance"]

        # Create asset lookup using asset_id
        asset_lookup = assets.set_index("asset_id")

        department_passed = True

        for _, task in maintenance.iterrows():

            task_id = task["task_id"]
            asset_id = task["asset_id"]

            # ------------------------------------------------
            # Check that asset exists
            # ------------------------------------------------

            if asset_id not in asset_lookup.index:

                print(
                    f"❌ {task_id}: "
                    f"asset {asset_id} does not exist"
                )

                department_passed = False
                overall_passed = False
                continue

            asset = asset_lookup.loc[asset_id]

            # ------------------------------------------------
            # Check department
            # ------------------------------------------------

            if task["department"] != asset["department"]:

                print(
                    f"❌ {task_id}: department mismatch "
                    f"(task={task['department']}, "
                    f"asset={asset['department']})"
                )

                department_passed = False
                overall_passed = False

            # ------------------------------------------------
            # Check department name
            # ------------------------------------------------

            if task["department_name"] != asset["department_name"]:

                print(
                    f"❌ {task_id}: department_name mismatch "
                    f"(task={task['department_name']}, "
                    f"asset={asset['department_name']})"
                )

                department_passed = False
                overall_passed = False

        if department_passed:

            print(
                f"✓ {prefix}: all maintenance tasks "
                f"correctly reference their assets"
            )

    return overall_passed



    print("\n" + "=" * 70)
    print("8. MAINTENANCE RELATIONSHIP VALIDATION")
    print("=" * 70)

    passed = True

    for prefix in ["tms", "smms", "tdms"]:

        assets = data[f"{prefix}_assets"]
        maintenance = data[f"{prefix}_maintenance"]

        asset_lookup = assets.set_index("asset_id")

        for _, task in maintenance.iterrows():

            asset_id = task["asset_id"]

            if asset_id not in asset_lookup.index:
                continue

            asset = asset_lookup.loc[asset_id]

            if task["corridor_id"] != asset["corridor_id"]:

                print(
                    f"❌ {task['task_id']}: "
                    f"corridor mismatch"
                )

                passed = False

            if task["department"] != asset["department"]:

                print(
                    f"❌ {task['task_id']}: "
                    f"department mismatch"
                )

                passed = False

        if passed:
            print(
                f"✓ {prefix}: maintenance relationships valid"
            )

    return passed


# ============================================================
# BLOCK REQUEST RELATIONSHIPS
# ============================================================

def inspect_block_requests(data):

    print("\n" + "=" * 70)
    print("9. BLOCK REQUEST VALIDATION")
    print("=" * 70)

    passed = True

    requests = data["block_requests"]

    all_assets = pd.concat([
        data["tms_assets"],
        data["smms_assets"],
        data["tdms_assets"],
    ])

    all_tasks = pd.concat([
        data["tms_maintenance"],
        data["smms_maintenance"],
        data["tdms_maintenance"],
    ])

    asset_lookup = all_assets.set_index("asset_id")
    task_lookup = all_tasks.set_index("task_id")

    for _, request in requests.iterrows():

        request_id = request["block_request_id"]
        task_id = request["task_id"]
        asset_id = request["asset_id"]

        # Task exists
        if task_id not in task_lookup.index:
            print(
                f"❌ {request_id}: "
                f"unknown task {task_id}"
            )
            passed = False
            continue

        task = task_lookup.loc[task_id]

        # Asset exists
        if asset_id not in asset_lookup.index:
            print(
                f"❌ {request_id}: "
                f"unknown asset {asset_id}"
            )
            passed = False
            continue

        asset = asset_lookup.loc[asset_id]

        # Task -> asset
        if task["asset_id"] != asset_id:
            print(
                f"❌ {request_id}: "
                f"task/asset mismatch"
            )
            passed = False

        # Asset -> corridor
        if request["corridor_id"] != asset["corridor_id"]:
            print(
                f"❌ {request_id}: "
                f"corridor mismatch"
            )
            passed = False

        # Department
        if request["department"] != asset["department"]:
            print(
                f"❌ {request_id}: "
                f"department mismatch"
            )
            passed = False

        # Location
        if request["location_km"] != asset["location_km"]:
            print(
                f"❌ {request_id}: "
                f"location mismatch"
            )
            passed = False

        # Duration
        start = pd.to_datetime(
            request["start_time"],
            format="%H:%M"
        )

        end = pd.to_datetime(
            request["end_time"],
            format="%H:%M"
        )

        calculated_duration = (
            end - start
        ).total_seconds() / 3600

        if calculated_duration != request["duration_hours"]:

            print(
                f"❌ {request_id}: "
                f"duration mismatch "
                f"(expected {calculated_duration}, "
                f"got {request['duration_hours']})"
            )

            passed = False

    if passed:
        print("✓ All block request relationships are valid")

    return passed


# ============================================================
# COORDINATION SCENARIO
# ============================================================

def inspect_coordination_scenario(data):

    print("\n" + "=" * 70)
    print("10. COORDINATION SCENARIO")
    print("=" * 70)

    requests = data["block_requests"]

    expected = {
        "BR-0001": {
            "department": "ENG",
            "corridor_id": "C001",
            "asset_id": "ENG-A001",
            "task_id": "ENG-T001",
            "start_time": "10:00",
            "end_time": "12:00",
        },

        "BR-0002": {
            "department": "SNT",
            "corridor_id": "C001",
            "asset_id": "SNT-A001",
            "task_id": "SNT-T001",
            "start_time": "10:30",
            "end_time": "11:30",
        },

        "BR-0003": {
            "department": "TRD",
            "corridor_id": "C001",
            "asset_id": "TRD-A001",
            "task_id": "TRD-T001",
            "start_time": "11:00",
            "end_time": "13:00",
        },
    }

    passed = True

    for request_id, expected_values in expected.items():

        row = requests[
            requests["block_request_id"] == request_id
        ]

        if row.empty:
            print(f"❌ Missing {request_id}")
            passed = False
            continue

        row = row.iloc[0]

        for column, expected_value in expected_values.items():

            actual_value = row[column]

            if actual_value != expected_value:

                print(
                    f"❌ {request_id}: "
                    f"{column} expected={expected_value}, "
                    f"actual={actual_value}"
                )

                passed = False

        if passed:
            print(f"✓ {request_id} correct")

    # Check overlapping windows
    print("\nExpected coordination:")

    print(
        "ENG: 10:00–12:00"
        "\nSNT: 10:30–11:30"
        "\nTRD: 11:00–13:00"
    )

    print(
        "\nThese three requests overlap and should later "
        "be considered by the optimizer for consolidation."
    )

    return passed


# ============================================================
# DATE VALIDATION
# ============================================================

def inspect_dates(data):

    print("\n" + "=" * 70)
    print("11. DATE VALIDATION")
    print("=" * 70)

    passed = True

    date_columns = {
        "tms_assets": [
            "installation_date",
            "last_maintenance_date",
            "next_maintenance_date",
        ],
        "smms_assets": [
            "installation_date",
            "last_maintenance_date",
            "next_maintenance_date",
        ],
        "tdms_assets": [
            "installation_date",
            "last_maintenance_date",
            "next_maintenance_date",
        ],
        "tms_maintenance": [
            "scheduled_date",
        ],
        "smms_maintenance": [
            "scheduled_date",
        ],
        "tdms_maintenance": [
            "scheduled_date",
        ],
        "block_requests": [
            "requested_date",
        ],
        "trains": [
            "date",
        ],
        "goods_forecast": [
            "date",
        ],
    }

    for name, columns in date_columns.items():

        if name not in data:
            continue

        df = data[name]

        for column in columns:

            if column not in df.columns:
                continue

            parsed = pd.to_datetime(
                df[column],
                errors="coerce"
            )

            invalid = parsed.isna().sum()

            if invalid == 0:
                print(
                    f"✓ {name}.{column}: valid dates"
                )
            else:
                print(
                    f"❌ {name}.{column}: "
                    f"{invalid} invalid dates"
                )
                passed = False

    return passed


# ============================================================
# TIME VALIDATION
# ============================================================

def inspect_times(data):

    print("\n" + "=" * 70)
    print("12. TIME VALIDATION")
    print("=" * 70)

    passed = True

    if "block_requests" in data:

        df = data["block_requests"]

        for column in ["start_time", "end_time"]:

            parsed = pd.to_datetime(
                df[column],
                format="%H:%M",
                errors="coerce"
            )

            invalid = parsed.isna().sum()

            if invalid == 0:
                print(
                    f"✓ block_requests.{column}: valid"
                )
            else:
                print(
                    f"❌ block_requests.{column}: "
                    f"{invalid} invalid times"
                )
                passed = False

    return passed


# ============================================================
# CRITICALITY / SEVERITY
# ============================================================

def inspect_risk_values(data):

    print("\n" + "=" * 70)
    print("13. RISK / CRITICALITY DISTRIBUTION")
    print("=" * 70)

    for name, df in data.items():

        if "criticality" in df.columns:

            print(f"\n{name} criticality:")

            print(
                df["criticality"]
                .value_counts()
                .sort_index()
                .to_string()
            )

        if "severity_score" in df.columns:

            print(f"\n{name} severity:")

            print(
                df["severity_score"]
                .describe()
                .to_string()
            )


# ============================================================
# CORRIDOR DISTRIBUTION
# ============================================================

def inspect_distribution(data):

    print("\n" + "=" * 70)
    print("14. DATA DISTRIBUTION")
    print("=" * 70)

    for name in [
        "tms_assets",
        "smms_assets",
        "tdms_assets",
        "block_requests",
    ]:

        if name not in data:
            continue

        df = data[name]

        print(f"\n{name} by corridor:")

        print(
            df["corridor_id"]
            .value_counts()
            .sort_index()
            .to_string()
        )


# ============================================================
# TRAIN DATA CHECK
# ============================================================

def inspect_trains(data):

    print("\n" + "=" * 70)
    print("15. TRAIN DATA VALIDATION")
    print("=" * 70)

    if "trains" not in data:
        return False

    df = data["trains"]

    passed = True

    # Unique train IDs
    if df["train_id"].is_unique:
        print("✓ Train IDs are unique")
    else:
        print("❌ Duplicate train IDs")
        passed = False

    # Corridors
    invalid = set(df["corridor_id"]) - EXPECTED_CORRIDORS

    if not invalid:
        print("✓ Train corridors valid")
    else:
        print(
            f"❌ Invalid train corridors: {invalid}"
        )
        passed = False

    # Train types
    if "train_type" in df.columns:

        print("\nTrain type distribution:")

        print(
            df["train_type"]
            .value_counts()
            .to_string()
        )

    return passed


# ============================================================
# GOODS FORECAST
# ============================================================

def inspect_goods_forecast(data):

    print("\n" + "=" * 70)
    print("16. GOODS FORECAST VALIDATION")
    print("=" * 70)

    if "goods_forecast" not in data:
        return False

    df = data["goods_forecast"]

    passed = True

    invalid = set(df["corridor_id"]) - EXPECTED_CORRIDORS

    if invalid:
        print(
            f"❌ Invalid corridors: {invalid}"
        )
        passed = False
    else:
        print("✓ Forecast corridors valid")

    # Expected 4 windows per corridor per day
    if "time_window" in df.columns:

        windows = df["time_window"].nunique()

        print(
            f"✓ Unique time windows: {windows}"
        )

        print("\nTime window distribution:")

        print(
            df["time_window"]
            .value_counts()
            .sort_index()
            .to_string()
        )

    print("\nForecast by corridor:")

    print(
        df["corridor_id"]
        .value_counts()
        .sort_index()
        .to_string()
    )

    return passed


# ============================================================
# FINAL REPORT
# ============================================================

def run_inspection():

    data = load_data()

    if not data:
        print("\n❌ No data found.")
        return

    results = {}

    inspect_basic(data)

    results["row_counts"] = inspect_counts(data)
    results["missing_values"] = inspect_missing_values(data)
    results["duplicates"] = inspect_duplicates(data)
    results["departments"] = inspect_departments(data)
    results["corridors"] = inspect_corridors(data)
    results["asset_relationships"] = inspect_asset_relationships(data)
    results["maintenance_relationships"] = (
        inspect_maintenance_relationships(data)
    )
    results["block_requests"] = inspect_block_requests(data)
    results["coordination"] = inspect_coordination_scenario(data)
    results["dates"] = inspect_dates(data)
    results["times"] = inspect_times(data)

    inspect_risk_values(data)
    inspect_distribution(data)

    results["trains"] = inspect_trains(data)
    results["goods_forecast"] = inspect_goods_forecast(data)

    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    print("\n" + "=" * 70)
    print("FINAL DATA QUALITY REPORT")
    print("=" * 70)

    for check, result in results.items():

        status = "PASS ✓" if result else "FAIL ❌"

        print(
            f"{check:<30} {status}"
        )

    passed = sum(results.values())
    total = len(results)

    print("\n" + "-" * 70)

    print(
        f"Checks passed: {passed}/{total}"
    )

    if passed == total:

        print(
            "\n🎉 DATASET PASSED ALL QUALITY CHECKS"
        )

        print(
            "The dataset is ready for the database phase."
        )

    else:

        print(
            "\n⚠ DATASET REQUIRES CORRECTIONS"
        )

        print(
            "Do NOT move to the database phase until "
            "the failed checks are resolved."
        )


if __name__ == "__main__":
    run_inspection()

