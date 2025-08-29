class Network:
    def __init__(self, env, logger):
        self.env    = env
        self.logger = logger


    def send_result(self, task, source_host, target_host, event_to_trigger):
        delay = task["network_time"]
        self.logger.log(self.env.now, "Network", "SEND_START", task["id"], f"{source_host.name} to {target_host.name} ({delay})")
        yield self.env.timeout(delay)
        self.logger.log(self.env.now, "Network", "SEND_END",   task["id"], f"to {target_host.name}")

        if not event_to_trigger.triggered:
            event_to_trigger.succeed()