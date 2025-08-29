HARDWARE_MAP = {
    "simple": {
        "host_0": {"cores": 1, "ram": 5000},
        "host_1": {"cores": 1, "ram": 5000},
    },
    "simple_multicore": {
        "host_0": {"cores": 2, "ram": 5000},
        "host_1": {"cores": 2, "ram": 5000},
    },
    "simple_dependencies": {
        "host_0": {"cores": 1, "ram": 5000},
        "host_1": {"cores": 1, "ram": 5000},
    },
    "networked_dependencies": {
        "host_0": {"cores": 1, "ram": 3000},
        "host_1": {"cores": 1, "ram": 5000},
    },
    "ping_pong": {
        "host_0": {"cores": 1, "ram": 3000},
        "host_1": {"cores": 1, "ram": 3000},
    },
    "long_sleep": {
        "host_0": {"cores": 1, "ram": 3000},
        "host_1": {"cores": 1, "ram": 3000},
    },
}
