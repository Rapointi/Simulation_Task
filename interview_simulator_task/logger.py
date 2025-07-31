import pandas as pd
import logging


def setup_logging():
    logging.basicConfig(
        filename="simulation.log",
        filemode="w",
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s - %(name)s - %(message)s',
    )


class EventLogger:
    def __init__(self):
        self.events = []
        self.logger = logging.getLogger("event_logger")


    def log(self, timestamp, host, event, task_id, details=""):
        self.events.append({
            "time": timestamp,
            "host": host,
            "event": event,
            "task_id": task_id,
            "details": details
        })

        self.logger.info(
            f"Event: {event:<15} | Host: {host:<8} | Task: {task_id:<8} | Time: {timestamp:<8} | Details: {details}" )

    def to_dataframe(self):
        return pd.DataFrame(self.events)