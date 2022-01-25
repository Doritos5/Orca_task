# Home assignment
# Dor Mordechai

# os imports
from multiprocessing import Lock, Manager
from time import time

# 3d party imports
from fastapi import FastAPI, Request

# Internal imports
from orca.core_functions import who_can_attack, initiate_server

# Global variables
WORKERS_LOCK = Lock()
TOTAL_RESPONSE_TIME = 0

stat_dict = Manager().dict()
stat_dict.update({"vm_count": 0,
                  "request_count": 0})

# Initiate server instance with pre-loaded data
initiate_server(stats_dict=stat_dict)

# FastAPI instance
app = FastAPI()


@app.get("/api/v1/attack/{vm_id}")
def get_potential_attackers(vm_id: str) -> set:
    potential_attacks = who_can_attack(vm_id=vm_id)
    return potential_attacks


@app.get("/api/v1/stats")
def get_stats():
    global stat_dict, TOTAL_RESPONSE_TIME, WORKERS_LOCK
    return {
            **stat_dict,
            "average_response_time": round(TOTAL_RESPONSE_TIME / stat_dict["request_count"], ndigits=5)
            }


@app.middleware("http")
def calc_request(request: Request, call_next):
    global TOTAL_RESPONSE_TIME, stat_dict

    start_time = time()
    with WORKERS_LOCK:
        stat_dict["request_count"] += 1
    response = call_next(request)
    process_time = time() - start_time
    with WORKERS_LOCK:
        TOTAL_RESPONSE_TIME += process_time

    return response
