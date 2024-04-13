from classes import *
import pytest

@pytest.fixture
def sample_request():
    return Request(requestID=1, datasetSource="dataset.zip", numImages=5, modelSource="model.pt", requestOwner="0x1234", bid=100)

@pytest.fixture
def pipeline_request(sample_request):
    return PipelineRequest(sample_request)

def test_worker_equality():
    worker1 = Worker("0x1234")
    worker2 = Worker("0x1234")
    worker3 = Worker("0x5678")
    assert worker1 == worker2
    assert worker1 != worker3

def test_pipeline_request_init(sample_request):
    pipeline_request = PipelineRequest(sample_request)
    assert pipeline_request.requestID == sample_request.requestID
    assert pipeline_request.datasetSource == sample_request.datasetSource
    assert pipeline_request.numImages == sample_request.numImages
    assert pipeline_request.modelSource == sample_request.modelSource
    assert pipeline_request.requestOwner == sample_request.requestOwner
    assert pipeline_request.bid == sample_request.bid
    assert pipeline_request.workers == []

def test_pipeline_request_add_worker(pipeline_request):
    worker = Worker("0x1234")
    pipeline_request.add_worker(worker)
    assert len(pipeline_request.workers) == 1
    assert pipeline_request.workers[0] == worker

def test_pipeline_request_get_batch(pipeline_request):
    batch = pipeline_request.get_batch()
    assert isinstance(batch, BatchItem)
    assert batch.modelUrl == pipeline_request.modelSource
    assert batch.datasetUrl == pipeline_request.datasetSource
    assert batch.requestID == pipeline_request.requestID

def test_pipeline_request_add_labels_check_done(pipeline_request):
    worker1 = Worker("0x1234")
    worker2 = Worker("0x5678")
    worker3 = Worker("0x9abc")
    pipeline_request.add_worker(worker1)
    pipeline_request.add_worker(worker2)
    pipeline_request.add_worker(worker3)

    data1 = LabelReturnItem(requestID=1, userEthAddress="0x1234", labels=[1, 2, 3, 4, 5])
    data2 = LabelReturnItem(requestID=1, userEthAddress="0x5678", labels=[1, 2, 3, 4, 5])
    data3 = LabelReturnItem(requestID=1, userEthAddress="0x9abc", labels=[1, 2, 3, 4, 5])

    assert pipeline_request.add_labels_check_done(data1) is None
    assert pipeline_request.add_labels_check_done(data2) is None
    assert pipeline_request.add_labels_check_done(data3) == [1, 2, 3, 4, 5]

def test_pipeline_request_add_labels_check_done_invalid(pipeline_request):
    worker = Worker("0x1234")
    pipeline_request.add_worker(worker)

    data1 = LabelReturnItem(requestID=2, userEthAddress="0x1234", labels=[1, 2, 3, 4, 5])
    data2 = LabelReturnItem(requestID=1, userEthAddress="0x5678", labels=[1, 2, 3, 4, 5])
    data3 = LabelReturnItem(requestID=1, userEthAddress="0x1234", labels=[1, 2, 3, 4])

    with pytest.raises(ValueError):
        pipeline_request.add_labels_check_done(data1)
    with pytest.raises(ValueError):
        pipeline_request.add_labels_check_done(data2)
    with pytest.raises(ValueError):
        pipeline_request.add_labels_check_done(data3)

def test_pipeline_init():
    pipeline = Pipeline()
    assert pipeline.reqPQ == []
    assert pipeline.currentRequest is None

def test_pipeline_add_request():
    pipeline = Pipeline()
    req1 = PipelineRequest(Request(requestID=1, datasetSource="dataset1.zip", numImages=5, modelSource="model1.pt", requestOwner="0x1234", bid=100))
    req2 = PipelineRequest(Request(requestID=2, datasetSource="dataset2.zip", numImages=10, modelSource="model2.pt", requestOwner="0x5678", bid=200))

    pipeline.add_request(req1)
    pipeline.add_request(req2)

    assert len(pipeline.reqPQ) == 2
    assert pipeline.reqPQ[0] == req2
    assert pipeline.reqPQ[1] == req1

def test_pipeline_add_request_duplicate():
    pipeline = Pipeline()
    req1 = PipelineRequest(Request(requestID=1, datasetSource="dataset1.zip", numImages=5, modelSource="model1.pt", requestOwner="0x1234", bid=100))
    req2 = PipelineRequest(Request(requestID=1, datasetSource="dataset1.zip", numImages=5, modelSource="model1.pt", requestOwner="0x1234", bid=100))

    pipeline.add_request(req1)
    with pytest.raises(ValueError):
        pipeline.add_request(req2)

def test_pipeline_get_curr_req_and_set_next_req():
    pipeline = Pipeline()
    req1 = PipelineRequest(Request(requestID=1, datasetSource="dataset1.zip", numImages=5, modelSource="model1.pt", requestOwner="0x1234", bid=100))
    req2 = PipelineRequest(Request(requestID=2, datasetSource="dataset2.zip", numImages=10, modelSource="model2.pt", requestOwner="0x5678", bid=200))

    pipeline.add_request(req1)
    pipeline.add_request(req2)

    assert pipeline.get_curr_req() == req2
    assert pipeline.get_curr_req() == req2
    pipeline.set_next_req()
    assert pipeline.get_curr_req() == req1
    pipeline.set_next_req()
    assert pipeline.get_curr_req() is None

def test_image_label_consensus():
    consensus = ImageLabelConsensus()

    data = {
        "client1": [1, 2, 3, 4, 5],
        "client2": [1, 2, 3, 4, 6],
        "client3": [1, 2, 7, 4, 5]
    }

    consensus.receiveData(data)
    assert consensus.responseData() == [1, 2, 3, 4, 5]

def test_pipeline_request_comparison():
    req1 = PipelineRequest(Request(requestID=1, datasetSource="dataset1.zip", numImages=5, modelSource="model1.pt", requestOwner="0x1234", bid=100))
    req2 = PipelineRequest(Request(requestID=2, datasetSource="dataset2.zip", numImages=10, modelSource="model2.pt", requestOwner="0x5678", bid=200))
    assert req2 < req1

def test_pipeline_get_curr_req_empty():
    pipeline = Pipeline()
    assert pipeline.get_curr_req() is None

def test_image_label_consensus_empty():
    consensus = ImageLabelConsensus()
    assert consensus.responseData() == []

def test_image_label_consensus_single_client():
    consensus = ImageLabelConsensus()
    data = {"client1": [1, 2, 3, 4, 5]}
    consensus.receiveData(data)
    assert consensus.responseData() == [1, 2, 3, 4, 5]

def test_image_label_consensus_tie_breaking():
    consensus = ImageLabelConsensus()
    data = {
        "client1": [1, 2, 3, 4, 5],
        "client2": [6, 2, 3, 4, 5],
        "client3": [6, 2, 3, 4, 5]
    }
    consensus.receiveData(data)
    assert consensus.responseData() == [6, 2, 3, 4, 5]

def test_worker_lt_comparison():
    worker1 = Worker("0x1234")
    worker2 = Worker("0x5678")
    worker1.participation = 0.5
    worker2.participation = 0.7
    assert worker1 < worker2

    worker1.participation = 0.7
    worker2.participation = 0.7
    assert worker1 < worker2  # Based on address comparison