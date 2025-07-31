import simpy

from interview_simulator_task.host import Host
from interview_simulator_task.logger import EventLogger


def test_run_simple_task():
    env    = simpy.Environment()
    logger = EventLogger()
    host   = Host(env, name="TestHost0", num_cores=1, ram_capacity=2000, logger=logger)

    task = {
        "id":              "T1",
        "start_time":      0,
        "run_time":        1000,
        "ram_required":    1000,
        "dependency":      "",
        "network_traffic": 0
    }

    dependency_events = {}
    dependent_tasks   = {}
    host_map          = {}
    network           = None

    env.process(host.run_task(task, dependency_events, dependent_tasks, host_map, network))
    env.run()

    df = logger.to_dataframe()
    events = df["event"].tolist()

    assert events == ["START", "END"]


def test_wait_for_ram():
    env    = simpy.Environment()
    logger = EventLogger()
    host   = Host(env, name="TestHost0", num_cores=1, ram_capacity=500, logger=logger)
 
    task = {
        "id":              "T1",
        "start_time":      0,
        "run_time":        1000,
        "ram_required":    1000,
        "dependency":      "",
        "network_traffic": 0
    }

    dependency_events = {}
    dependent_tasks   = {}
    host_map          = {}
    network           = None

    env.process(host.run_task(task, dependency_events, dependent_tasks, host_map, network))
    env.run()

    df = logger.to_dataframe()
    assert "WAIT_FOR_RAM" in df["event"].values


def test_task_with_dependency():
    env    = simpy.Environment()
    logger = EventLogger()
    host   = Host(env, name="TestHost0", num_cores=1, ram_capacity=2000, logger=logger)

    task1 = {
        "id":              "T1",
        "start_time":      0,
        "run_time":        1000,
        "ram_required":    500,
        "dependency":      "",
        "network_traffic": 0
    }

    task2 = {
        "id":              "T2",
        "start_time":      0,
        "run_time":        1000,
        "ram_required":    500,
        "dependency":      "T1",
        "network_traffic": 0
    }

    dependency_events = {"T1": env.event()}
    dependent_tasks   = {"T1": [task2]}
    host_map          = {"T1": host, "T2": host}
    network           = None

    env.process(host.run_task(task1, dependency_events, dependent_tasks, host_map, network))
    env.process(host.run_task(task2, dependency_events, dependent_tasks, host_map, network))

    env.run()

    df = logger.to_dataframe()
    assert "WAIT_FOR_TASK" in df[df["task_id"] == "T2"]["event"].values


def test_ram_blocking():
    env    = simpy.Environment()
    logger = EventLogger()
    host   = Host(env, name="TestHost0", num_cores=2, ram_capacity=2000, logger=logger)

    task1 = {
        "id":              "T1",
        "start_time":      0,
        "run_time":        1000,
        "ram_required":    1500,
        "dependency":      "",
        "network_traffic": 0
    }

    task2 = {
        "id":              "T2",
        "start_time":      0,
        "run_time":        1000,
        "ram_required":    1500,
        "dependency":      "",
        "network_traffic": 0
    }

    dependency_events = {}
    dependent_tasks   = {}
    host_map          = {"T1": host, "T2": host}
    network           = None

    env.process(host.run_task(task1, dependency_events, dependent_tasks, host_map, network))
    env.process(host.run_task(task2, dependency_events, dependent_tasks, host_map, network))

    env.run()

    df = logger.to_dataframe()
    assert "WAIT_FOR_RAM" in df["event"].values

