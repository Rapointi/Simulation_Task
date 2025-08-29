# Distributed Task Simulator

A **resource-aware discrete-event simulation** for distributed task execution.  
It models CPU, RAM, and network constraints as well as task dependencies and scheduling logic.  
The simulator is built with **Python and SimPy** and includes testing via **Pytest**.

---

## Features
- Multi-host simulation with CPU, RAM, and network resources  
- Task dependencies and queuing logic  
- Performance evaluation of distributed workloads  
- Configurable scenarios via CSV input files  
- Unit tests with pytest for reliability  

---

## Tech Stack
- **Python 3.13**  
- **SimPy** – discrete-event simulation library  
- **pytest** – automated testing framework  

---

## Getting Started

### Setup environment
```bash
conda create -n simenv python=3.13
conda activate simenv
pip install -r requirements.txt


## Run Simulation

```bash
python -m src.main [path_to_csv_file]

Preset:

```bash
python -m src.main data/2_simple_multicore.csv
python -m src.main data/3_simple_dependencies.csv
python -m src.main data/4_networked_dependencies.csv
python -m src.main data/5_ping_pong.csv
python -m src.main data/6_long_sleep.csv


## Run Tests
pytest tests


## Input files
The tasks are described in the `*.csv` input files located in the `data` folder of this repository.
The files contain one task per line, in the following format:

| `TASK_NAME`  | `TASK_HOST` | `TASK_INITIAL_SLEEP_TIME` | `TASK_RUN_TIME` | `TASK_RAM` | `TASK_NETWORK_TIME` | `TASK_DEPENDENCY` |
|--------------|-------------|---------------------------|-----------------|------------|---------------------|-------------------|
| TASK_0       | HOST_0      | 0                         | 1000            | 1000       | 500                 |                   |
| TASK_1       | HOST_1      | 0                         | 1000            | 2000       | 0                   | TASK_0            |
| TASK_2       | HOST_1      | 500                       | 1000            | 2000       | 0                   | TASK_1            |

- `TASK_NAME`: The name of the task
- `TASK_HOST`: The host where the task shall run, either `HOST_0` or `HOST_1`
- `TASK_INITIAL_SLEEP_TIME`: The amount of time (in units) the task will sleep after the simulation starts.
- `TASK_RUN_TIME`: The amount of time (in units) for which the task will occupy one CPU core after it has started executing. The task can only start executing if at least one CPU core is available.
- `TASK_RAM`: The amount of RAM (in units) consumed by the task while it is running. The task can only start executing if this amount of RAM is available.
- `TASK_NETWORK_TIME`: The amount of time required to transmit network data produced by this task to its dependent tasks on the other host.
- `TASK_DEPENDENCY`: The dependency of this task.


## Explanation of concepts

### Initial sleep time
`TASK_INITIAL_SLEEP_TIME` describes the amount of time (in units) a task will sleep after the simulation starts. After this time, the task will become ready once
its dependencies have concluded (or immediately, if the task has no dependency).

### Task run time
The amount of time (in units) for which the task will occupy one CPU core after it has started executing.
A task will become ready under the following circumstances:
- If the task has no dependency, it becomes ready `TASK_INITIAL_SLEEP_TIME` time units after the simulation starts,
- If the task has a dependency on the same host, it becomes ready at the point in time where the dependency task concludes.
- if the task has a dependency on a different host, it becomes ready after the dependency task has finished its run-time,
and the network between the two hosts has transferred the output between the dependency task's host and this task's host.

A task can only execute if a CPU core is available and the task is ready.
After a task has begun executing, it will execute until completion without being interrupted.

### Task RAM
The amount of RAM consumed by the task while it is running. The task can only start executing it is ready and the requested amount of RAM is available.
Otherwise, the task has to wait until such amounts of RAM are available.

### Task network time
The amount of time required to transmit data from a dependency task to the current task after the run-time of the dependency task has concluded.

### Task dependency
Tasks may depend on each other. If, e.g., `TASK_1` has `TASK_0` as its dependency,
if both tasks run on the same host. If the two tasks reside on different hosts, `TASK_1` can only start after the run-time of
`TASK_0` has concluded, and the network has transferred the output of `TASK_0` from `TASK_0`s host to `TASK_1`s host, which requires a free
network link and `TASK_NETWORK_TIME` time units.


# 3. Examples

## Example 1:

Assume the following tasks:

| `TASK_NAME`  | `TASK_HOST` | `TASK_INITIAL_SLEEP_TIME` | `TASK_RUN_TIME` | `TASK_RAM` | `TASK_NETWORK_TIME` | `TASK_DEPENDENCY` |
|--------------|-------------|---------------------------|-----------------|------------|---------------------|-------------------|
| TASK_0       | HOST_0      | 0                         | 1000            | 0          | 0                   |                   |
| TASK_1       | HOST_0      | 500                       | 1000            | 0          | 0                   |                   |

`HOST_0` is a host with 5000 units of RAM, and a single CPU core.

- At `t=0`, the start of simulation, both tasks become ready.
- Since `TASK_0` does not sleep, while `TASK_1` does, `TASK_0` begins running.
- At `t=500` `TASK_1` becomes ready, however, since the single CPU core Of `HOST_0` is occupied, it can't begin execution.
- At `t=1000` `TASK_0` finishes executing. Since the CPU of `HOST_0` is now free, `TASK_1` can start executing.
- At `t=2000` `TASK_1` finishes executing. The simulation concludes.

## Example 2:

Assume the following tasks:

| `TASK_NAME` | `TASK_HOST` | `TASK_INITIAL_SLEEP_TIME` | `TASK_RUN_TIME` | `TASK_RAM` | `TASK_NETWORK_TIME` | `TASK_DEPENDENCY` |
|-------------|-------------|---------------------------|-----------------|------------|---------------------|-------------------|
| TASK_0      | HOST_0      | 0                         | 1000            | 1000       | 0                   |                   |
| TASK_1      | HOST_0      | 500                       | 1000            | 3000       | 0                   |                   |
| TASK_2      | HOST_0      | 1000                      | 1000            | 3000       | 0                   |                   |

`HOST_0` is a host with 5000 units of RAM, and **two** CPU cores.

- At `t=0`, the start of simulation, all tasks become ready.
- Since `TASK_0` does not sleep, while `TASK_1` and `TASK_2` do, `TASK_0` begins running, occupying one CPU core and 1000 units of RAM
- At `t=500` `TASK_1` becomes ready and begins executing, occupying one CPU core and 3000 units of RAM. In total, 4000 units of RAM and two CPU cores are now occupied.
- At `t=1000` `TASK_0` finishes executing, releasing one CPU core and 1000 units of RAM. `TASK_2` becomes ready and, since `HOST_0` has two CPU cores, could start executing.
However, only 2000 units of RAM are available, while `TASK_2` requires 3000 units. Therefore, `TASK_2` can not begin execution.
- At `t=1500` `TASK_1` finishes executing, releasing one CPU core and 3000 units of RAM. As 5000 units of RAM are now available, `TASK_2` can begin executing.
- At `t=2500` `TASK_2` finishes executing. The simulation concludes.

## Example 3:

Assume the following tasks:

| `TASK_NAME` | `TASK_HOST` | `TASK_INITIAL_SLEEP_TIME` | `TASK_RUN_TIME` | `TASK_RAM` | `TASK_NETWORK_TIME` | `TASK_DEPENDENCY` |
|-------------|-------------|---------------------------|-----------------|------------|---------------------|-------------------|
| TASK_0      | HOST_0      | 0                         | 1000            | 1000       | 0                   |                   |
| TASK_1      | HOST_0      | 500                       | 1000            | 3000       | 0                   | TASK_0            |

`HOST_0` is a host with 5000 units of RAM, and **two** CPU cores.

- At `t=0`, the start of simulation, all tasks become ready.
- Since `TASK_0` does not sleep, while `TASK_1` does, `TASK_0` begins running, occupying one CPU core and 1000 units of RAM.
- At `t=500` `TASK_1` stops sleeping. However, since `TASK_0` has not finished executing, it is not ready.
- At `t=1000` `TASK_0` finishes executing. `TASK_1` becomes ready and starts executing, occupying one CPU core and 3000 units of RAM.
- At `t=2000` `TASK_1` finishes executing. The simulation concludes.

## Example 4:

Assume the following tasks:

| `TASK_NAME` | `TASK_HOST` | `TASK_INITIAL_SLEEP_TIME` | `TASK_RUN_TIME` | `TASK_RAM` | `TASK_NETWORK_TIME` | `TASK_DEPENDENCY` |
|-------------|-------------|---------------------------|-----------------|------------|---------------------|-------------------|
| TASK_0      | HOST_0      | 0                         | 1000            | 1000       | 500                 |                   |
| TASK_1      | HOST_1      | 0                         | 1000            | 3000       | 0                   | TASK_0            |

`HOST_0` and `HOST_1` are hosts with 5000 units of RAM, and **two** CPU cores, each.

- At `t=0`, the start of simulation, all tasks become ready.
- Since `TASK_0` does not sleep and has no dependencies, `TASK_0` begins running, occupying one CPU core and 1000 units of RAM on `HOST_0`. Since `TASK_0` has not finished executing and network communication has not concluded, `TASK_1` is not ready.
- At `t=1000` `TASK_0` finishes executing. The network link between `HOST_0` and `HOST_1` becomes busy and begins transmitting the outputs of `TASK_0`. Since network communication
has not finished, `TASK_1` remains not ready.
- At `t=1500` the network link between `HOST_0` and `HOST_1` finishes transmission of the outputs of `TASK_0` and is therefore released. `TASK_1` becomes ready and starts executing, occupying one CPU core and 3000 units of RAM.
- At `t=2500` `TASK_1` finishes executing. The simulation concludes.
