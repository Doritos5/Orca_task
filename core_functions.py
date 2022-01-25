import os
from os import path, R_OK
from collections import defaultdict
from typing import Union
from json import load
from multiprocessing import Lock

# Global variables
RULES = dict()
VMS = dict()
WORKERS_LOCK = Lock()


def get_rules():
    return RULES


def load_json(file_path: str) -> dict:
    with open(file_path) as json_reader:
        content = load(fp=json_reader)

    return content


def load_input_json(input_json: Union[dict, str],
                    stats_dict: dict) -> None:
    global RULES
    src_dst_mapping = defaultdict(set)

    # In case input json is a path to the JSON file and not the JSON itself
    if isinstance(input_json, str):
        input_json = load_json(file_path=input_json)

    for r in input_json["fw_rules"]:
        src_tag = r["source_tag"]
        dst_tag = r["dest_tag"]
        RULES[src_tag] = {"can_attack": set()}
        RULES[dst_tag] = {"can_attack": set()}

        src_dst_mapping[src_tag].add(dst_tag)

    for vm in input_json["vms"]:
        stats_dict["vm_count"] += 1
        vm_id = vm["vm_id"]
        VMS[vm_id] = {"name": vm["name"],
                      "tags": vm["tags"]}
        for tag in vm["tags"]:
            if not src_dst_mapping[tag]:  # No Firewall rule exists
                continue
            for attack in src_dst_mapping[tag]:
                RULES[attack]["can_attack"].add(vm["vm_id"])


def who_can_attack(vm_id: str) -> set:
    global RULES, VMS
    can_attack = set()

    for tag in VMS[vm_id]["tags"]:
        can_attack.update(RULES.get(tag, {}).get("can_attack", {}))

    return can_attack


def validate_input(file_path: str) -> None:
    if not path.exists(file_path):
        raise OSError(f"File path [{file_path}] was not found")
    if not path.isfile(file_path):
        raise OSError(f"File path [{file_path}] is not a file")
    if not R_OK:
        raise OSError(f"Unable to open file at [{file_path}]")


def initiate_server(stats_dict: dict):

    json_path = os.environ.get("JSON_PATH")
    if not json_path:
        raise RuntimeError(f"Please supply a valid JSON path environment variable using JSON_PATH='<path>")

    validate_input(file_path=json_path)

    load_input_json(input_json=json_path,
                    stats_dict=stats_dict)
