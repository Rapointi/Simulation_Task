import pandas as pd
import argparse

from interview_simulator_task.logger     import setup_logging
from interview_simulator_task.simulation import run_simulation
from interview_simulator_task.utils      import prepare_dataframe, extract_experiment_key


if __name__ == "__main__":

    setup_logging()

    parser = argparse.ArgumentParser(
        description = "Start the Interview-Simulation-Task."
    )
    parser.add_argument(
        "csv_file",
        nargs="?",
        default="data/1_simple.csv",
        help="Path to csv (Default: 1_simple.csv)"
    )
    args = parser.parse_args()

    experiment = extract_experiment_key(args.csv_file)
    print(f"Start experiment: {experiment}")
    
    df_input = pd.read_csv(args.csv_file)
    df_clean = prepare_dataframe(df_input)

    log_df = run_simulation(df_clean, experiment)
    print(log_df)