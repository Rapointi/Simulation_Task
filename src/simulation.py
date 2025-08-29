import simpy

from interview_simulator_task.host import Host
from interview_simulator_task.network import Network
from interview_simulator_task.logger import EventLogger
from interview_simulator_task.hardware_config import HARDWARE_MAP


def run_simulation(df, experiment_name):

    hw = HARDWARE_MAP[experiment_name]
    h0 = hw["host_0"]
    h1 = hw["host_1"]

    env               = simpy.Environment()
    logger            = EventLogger()
    dependency_events = {task_id: env.event() for task_id in df["id"]}
    host_map          = {}
    dependent_tasks   = {}


    host1 = Host(env, "Host0", num_cores=h0["cores"], ram_capacity=h0["ram"], logger=logger)
    host2 = Host(env, "Host1", num_cores=h1["cores"], ram_capacity=h1["ram"], logger=logger)

    network = Network(env, logger=logger)


    host_dict = {
        "host_0": host1,
        "host_1": host2
    }

    for _, row in df.iterrows():
        # Assign each task to exactly one host.
        task_id = row["id"]

        host = host_dict.get(row["host_preference"])
        host_map[task_id] = host


        # If task has dependency, enter it as successor
        dep = row["dependency"]
        if dep:
            dependent_tasks.setdefault(dep, []).append(row)

        env.process(host.run_task(row, dependency_events, dependent_tasks, host_map, network))

    env.run()
    return logger.to_dataframe()
