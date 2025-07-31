import simpy

from interview_simulator_task.network import Network
from interview_simulator_task.logger import EventLogger

class DummyHost:
    def __init__(self, name, env=None):
        self.name = name
        self.env = env


def test_network_send_result():
    env     = simpy.Environment()
    logger  = EventLogger()
    network = Network(env, logger=logger)

    source_host = DummyHost("Host0", env)
    target_host = DummyHost("Host1")

    dummy_event = env.event()

    task = {
        "id": "TASK_NETWORK",
        "network_time": 2000,
    }

    env.process(network.send_result(
        task=task,
        source_host=source_host,
        target_host=target_host,
        event_to_trigger=dummy_event
    ))

    env.run()

    log_df = logger.to_dataframe()

    assert "SEND_START" in log_df["event"].values
    assert "SEND_END"   in log_df["event"].values

    send_start_time = log_df[log_df["event"] == "SEND_START"]["time"].values[0]
    send_end_time   = log_df[log_df["event"] == "SEND_END"]["time"].values[0]

    assert send_end_time - send_start_time == 2000
    assert dummy_event.triggered
