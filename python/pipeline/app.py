from fastapi import FastAPI, status
from fastapi.responses import FileResponse
from pydantic import BaseModel

from classes import *

app = FastAPI()
pipeline = Pipeline()  # initialize pipeline

# TODO: Figure out a testing suite for each endpoint

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse('favicon.ico')

# Inherit from BaseModel because this will be sent as a body from fastapi (probably)
class Request(BaseModel):
    requestID: int
    datasetSource: str
    numImages: int
    modelSource: str
    requestOwner: str # address
    bid: int # in wei probably
    consensusType: str # unsure if relevant still
    result: list # the labels
    participation: dict[str, float]

    # Overload comparison operators for priority queue
    def __lt__(self, other):
        return (self.bid * -1) < (other.bid * -1) # negate so it's a max heap

# a data structure for labels
class Labels(BaseModel):
    requestID: int
    userAddress: str
    labels: list # same as result in Request

@app.get("/")  # default root
async def root():
    return {"message": "API is working"}

# Receive a new Request
# TODO: Some kind of callback back to chainlink and then smart contract
#  honestly probably not a callback and instead just some transaction since we have a request id
@app.post("/newRequest", status_code=status.HTTP_200_OK)
async def newRequest(req: Request):
    # TODO: turn Request into PipelineRequest and add to pipeline's priority queue
    return {"message": "Request received"} # Probably won't be used, just look at the status code

# Client GET a new Batch
# Query parameter is the worker's address.
# This is the endpoint that the worker will hit to get their batch
# First prompts batchmaker to generate the batch if not already generated
@app.get("/batch", status_code=status.HTTP_200_OK)
async def giveBatch(address: str) -> BatchItem:
    # TODO: don't return dummy data
    return BatchItem(modelUrl="https://example.com/model", 
                 datasetUrl="https://example.com/dataset", 
                 indexTuple=(0, 100), requestID=1)

# Client POST labels
# Will also check consensus after each label post. See the checkRequest method in Pipeline
@app.put("/labels", status_code=status.HTTP_202_ACCEPTED)
async def postLabels(labels: Labels):
    # TODO: Give the labels to the consensus 
    return {"message": "Labels received"} # again probably won't be used   