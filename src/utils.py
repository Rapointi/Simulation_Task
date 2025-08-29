import os

def prepare_dataframe(input_df):
    mapping = {
        "TASK_NAME":                "id",
        "TASK_INITIAL_SLEEP_TIME":  "start_time",
        "TASK_RUN_TIME":            "run_time",
        "TASK_RAM":                 "ram_required",
        "TASK_NETWORK_TIME":        "network_time",
        "TASK_DEPENDENCY":          "dependency",
        "TASK_HOST":                "host"
    }

    expected = ["id", "start_time", "run_time", "ram_required", "network_time", "dependency", "host"]

    df_clean = (
        input_df
        .rename(columns=mapping)
        .reindex(columns=expected)
    )

    defaults = {
        "start_time":      0,
        "run_time":        0,
        "ram_required":    0,
        "network_time":    0,
        "dependency":      "",
        "host":            "HOST_0"
    }

    df_clean = df_clean.fillna(defaults)

    df_clean["ram_required"]    = df_clean["ram_required"].astype(int)
    df_clean["dependency"]      = df_clean["dependency"].astype(str).str.strip()
    df_clean["host_preference"] = df_clean["host"].str.lower().str.strip()

    return df_clean


def extract_experiment_key(csv_path):
    base = os.path.basename(csv_path)              
    name = os.path.splitext(base)[0]               
    parts = name.split("_", 1)
    
    return parts[1] if len(parts) > 1 else parts[0]