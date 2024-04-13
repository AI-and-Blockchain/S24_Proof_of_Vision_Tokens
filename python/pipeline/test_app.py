from fastapi.testclient import TestClient
from app import app, pipeline
from classes import Request, BatchItem, LabelReturnItem, Worker, PipelineRequest

client = TestClient(app)

def setup_function():
    pipeline.reqPQ.clear()
    pipeline.currentRequest = None

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API is working"}

def test_new_request_and_batch():
    request_data = {
        "requestID": 1,
        "datasetSource": "https://example.com/dataset.zip",
        "numImages": 100,
        "modelSource": "https://example.com/model.h5",
        "requestOwner": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
        "bid": 10
    }
    response = client.post("/newRequest", json=request_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Request received"}

    response = client.get("/batch?address=0xD693853b55b0DACe3eD82B26B36A2F12AE914F8a")
    assert response.status_code == 200
    assert response.json() == {
        "modelUrl": "https://example.com/model.h5",
        "datasetUrl": "https://example.com/dataset.zip",
        "requestID": 1
    }

def test_new_request_duplicate_id():
    request_data = {
        "requestID": 1,
        "datasetSource": "https://example.com/dataset.zip",
        "numImages": 100,
        "modelSource": "https://example.com/model.h5",
        "requestOwner": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
        "bid": 10
    }
    response = client.post("/newRequest", json=request_data)
    assert response.status_code == 200

    response = client.post("/newRequest", json=request_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Request ID already in the queue"}

def test_batch_invalid_address():
    request_data = {
        "requestID": 2,
        "datasetSource": "https://example.com/dataset.zip",
        "numImages": 100,
        "modelSource": "https://example.com/model.h5",
        "requestOwner": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
        "bid": 10
    }
    response = client.post("/newRequest", json=request_data)
    assert response.status_code == 200

    response = client.get("/batch?address=invalid_address")
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid Ethereum address"}

def test_batch_no_requests():
    response = client.get("/batch?address=0xD693853b55b0DACe3eD82B26B36A2F12AE914F8a")
    assert response.status_code == 404
    assert response.json() == {"detail": "No requests available"}

def test_labels_valid():
    request_data = {
        "requestID": 3,
        "datasetSource": "https://example.com/dataset.zip",
        "numImages": 5,
        "modelSource": "https://example.com/model.h5",
        "requestOwner": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
        "bid": 10
    }
    response = client.post("/newRequest", json=request_data)
    assert response.status_code == 200

    response = client.get("/batch?address=0x1234567890123456789012345678901234567890")
    assert response.status_code == 200
    response = client.get("/batch?address=0x0987654321098765432109876543210987654321")
    assert response.status_code == 200

    label_data1 = {"requestID": 3, "userEthAddress": "0x1234567890123456789012345678901234567890", "labels": [1, 2, 3, 4, 5]}
    label_data2 = {"requestID": 3, "userEthAddress": "0x0987654321098765432109876543210987654321", "labels": [1, 2, 3, 4, 5]}

    response1 = client.put("/labels", json=label_data1)
    assert response1.status_code == 202
    assert response1.json() == {"message": "Labels received, waiting on consensus"}

    response = client.get("/showlabels")
    assert response.status_code == 200
    assert response.json() == {"0x1234567890123456789012345678901234567890": [1, 2, 3, 4, 5], "0x0987654321098765432109876543210987654321": []}


def test_labels_invalid_request_id():
    request_data = {
        "requestID": 4,
        "datasetSource": "https://example.com/dataset.zip",
        "numImages": 5,
        "modelSource": "https://example.com/model.h5",
        "requestOwner": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
        "bid": 10
    }
    response = client.post("/newRequest", json=request_data)
    assert response.status_code == 200

    response = client.get("/batch?address=0x1234567890123456789012345678901234567890")
    assert response.status_code == 200

    label_data = {"requestID": 5, "userEthAddress": "0x1234567890123456789012345678901234567890", "labels": [1, 2, 3, 4, 5]}
    response = client.put("/labels", json=label_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Request IDs do not match"}

def test_labels_invalid_num_labels():
    request_data = {
        "requestID": 5,
        "datasetSource": "https://example.com/dataset.zip",
        "numImages": 5,
        "modelSource": "https://example.com/model.h5",
        "requestOwner": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
        "bid": 10
    }
    response = client.post("/newRequest", json=request_data)
    assert response.status_code == 200

    response = client.get("/batch?address=0x1234567890123456789012345678901234567890")
    assert response.status_code == 200

    label_data = {"requestID": 5, "userEthAddress": "0x1234567890123456789012345678901234567890", "labels": [1, 2, 3]}
    response = client.put("/labels", json=label_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Number of labels does not match the number of images"}

def test_labels_no_requests():
    label_data = {"requestID": 6, "userEthAddress": "0x1234567890123456789012345678901234567890", "labels": [1, 2, 3, 4, 5]}
    response = client.put("/labels", json=label_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "No requests available"}

def test_show_labels_no_requests():
    response = client.get("/showlabels")
    assert response.status_code == 404
    assert response.json() == {"detail": "No requests available"}

def test_show_req_no_requests():
    response = client.get("/showreq")
    assert response.status_code == 404
    assert response.json() == {"detail": "No requests available"}