from pydantic import BaseModel
from batchmaker import Batchmaker
from ImageLabelConsensus import ImageLabelConsensus
import heapq # for priority queue

class BatchItem(BaseModel):
    modelUrl: str
    datasetUrl: str
    indexTuple: tuple[int, int]
    requestID: int

class Worker():
    def __init__(self, address: str):
        self.address = address
        self.participation = 0 # Starts at 0. Will get updated when they participate in a request by the consensus algorithm

    def __lt__(self, other):
        return self.participation < other.participation
    
class PipelineRequest():
    def __init__(self, requestID: int, datasetSource: str, numImages: int, modelSource: str, requestOwner: str, bid: int, result: list, participation: dict[Worker, float]):
        self.requestID = requestID
        self.datasetSource = datasetSource
        self.numImages = numImages
        self.modelSource = modelSource
        self.requestOwner = requestOwner
        self.bid = bid
        self.result = result
        self.participation = participation # TODO: How are we calculating this again? 

        self.workers = [] # List of Workers

        # TODO: Make sure these classes are correctly implmented
        self.consensusObj = ImageLabelConsensus() # The consensus object that will be used to consolidate the labels
        self.batchMaker = Batchmaker(dataset_url=datasetSource, model_url=modelSource, total_images=numImages) # The batchmaker object that will be used to generate the batches. Unsure about the num clients thing

    def addWorker(self, worker: Worker):
        '''
        Called by Pipeline when GET /batch is called.
        '''
        self.workers.append(worker)

class Pipeline():
    def __init__(self):
        self.req_pq = [] # priority queue for requests
        self.currentRequest = None # the current PipelineRequest being worked on

    def addRequest(self, req: PipelineRequest):
        """
        Add a PipelineRequest to the priority queueq
        """
        pass

    def checkRequest(self):
        '''
        Called by Pipeline when POST /labels is called after the consensus algorithm does their thing

        Checks if the current request is done. If so:
            1. Send the result to the smart contract
            2. Set the currentRequest to the next request in the priority queue
        '''
        pass