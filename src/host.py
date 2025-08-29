import simpy

class Host:
    def __init__(self, env, name, num_cores, ram_capacity, logger):
        self.env = env
        self.name = name
        self.cpu = simpy.Resource(env, capacity=num_cores)
        self.ram = simpy.Container(env, init=ram_capacity, capacity=ram_capacity)
        self.logger = logger


    def run_task(self, task, dependency_events, dependent_tasks, host_map, network):
        """
        Controlled execution flow of a task:

        1. Wait for the predecessor task to complete (if any).
        2. Wait until the tasks defined start time.
        3. Request CPU access.
        4. Acquire required RAM, run the task, then release the RAM.
        5. Notify dependent tasks, possibly via the network.
        """

        yield from self._wait_for_dependencies(task, dependency_events)
        yield from self._wait_for_start_time(task)
        
        with self.cpu.request() as req:
            yield req

            yield from self._execute_task_with_ram(task)

            self.logger.log(self.env.now, self.name, "END", task["id"])

            yield from self._notify_dependents(task, dependency_events, dependent_tasks, host_map, network)
            

    def _wait_for_dependencies(self, task, dependency_events):
        if task["dependency"]:
            event = dependency_events.get(task["dependency"])
            if event:
                yield event
                self.logger.log(self.env.now, self.name, "WAIT_FOR_TASK", task["id"], f"Dependency: {task['dependency']}")


    def _wait_for_start_time(self, task):
        yield self.env.timeout(max(0, task["start_time"] - self.env.now))
        self.logger.log(self.env.now, self.name, "START", task["id"])


    def _execute_task_with_ram(self, task):
        if self.ram.level < task["ram_required"]:
                self.logger.log(self.env.now, self.name, "WAIT_FOR_RAM", task["id"], f"Available: {self.ram.level} / Needed: {task['ram_required']}")

        yield self.ram.get(task["ram_required"])
        yield self.env.timeout(task["run_time"])
        yield self.ram.put(task["ram_required"])


    def _notify_dependents(self, task, dependency_events, dependent_tasks, host_map, network):
        if not dependent_tasks.get(task["id"]):
            if task["id"] in dependency_events and not dependency_events[task["id"]].triggered:
                dependency_events[task["id"]].succeed()
        else:
            for dependent_task in dependent_tasks.get(task["id"], []):
                target_host = host_map[dependent_task["id"]]
                if target_host != self:
                    yield self.env.process(
                        network.send_result(task, self, target_host, dependency_events[task["id"]])
                    )
                else:
                    if not dependency_events[task["id"]].triggered:
                        dependency_events[task["id"]].succeed()

    