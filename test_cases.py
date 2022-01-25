# os imports
from os import environ
import pathlib

# 3d imports
from jsonschema import validate

file_path = pathlib.Path(__file__).parent.resolve()
environ["JSON_PATH"] = f"{file_path}/test_files/input-2.json"
from fastapi.testclient import TestClient

# Local imports
from orca.server import app

client = TestClient(app)


def test_validate_stats():
    schema = {
        "properties": {
            "vm_count": {"type": "number"},
            "request_count": {"type": "number"},
            "average_response_time": {"type": "number"},
        },
    }
    
    response = client.get("/api/v1/stats")
    res_json = response.json()

    assert response.status_code == 200
    assert validate(res_json, {"maxItems": 3}) is None
    assert validate(res_json, schema) is None
    assert res_json["request_count"] == 1
    assert res_json["vm_count"] == 5
    assert res_json["average_response_time"] >= 0

    for _ in range(9):
        response = client.get("/api/v1/stats")
    assert response.json()["request_count"] == 10


def test_validate_attack():

    response = client.get("/api/v1/attack/vm-a3ed2eed23")
    res_json = response.json()

    assert response.status_code == 200
    assert validate(res_json, {"maxItems": 5}) is None
    assert isinstance(res_json, list)
    assert len(res_json) == 5
    assert sorted(res_json) == ['vm-2ba4d2f87',
                                'vm-7d1ff7af47',
                                'vm-a3ed2eed23',
                                'vm-b35b501',
                                'vm-ec02d5c153']



