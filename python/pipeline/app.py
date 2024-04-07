from fastapi import FastAPI, status
from fastapi.responses import FileResponse

from classes import *

app = FastAPI()
pipeline = Pipeline()  # initialize pipeline

# TODO: Figure out a testing suite for each endpoint

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse('favicon.ico')

# a data structure for labels
class Labels(BaseModel):
    requestID: int
    userAddress: str
    labels: list # same as result in Request

@app.get("/")  # default root
async def root():
    return {"message": "API is working"}

@app.post("/newRequest", status_code=status.HTTP_200_OK)
async def NewRequest(req: Request):
    '''
    Receive a new Request
    TODO: Some kind of callback back to chainlink and then smart contract
     honestly probably not a callback and instead just some transaction since we have a request id  

    TODO: turn Request into PipelineRequest and add to pipeline's priority queue  
    '''
    return {"message": "Request received"} # Probably won't be used, just look at the status code


@app.get("/batch", status_code=status.HTTP_200_OK)
async def GiveBatch(address: str) -> BatchItem:
    '''
    Client GET a new Batch
    Query parameter is the worker's address.
    This is the endpoint that the worker will hit to get their batch
    First prompts batchmaker to generate the batch if not already generated

    TODO: don't return dummy data
    '''
    return BatchItem(modelUrl="https://example.com/model", 
                 datasetUrl="https://example.com/dataset", 
                 indexTuple=(0, 100), requestID=1)


@app.put("/labels", status_code=status.HTTP_202_ACCEPTED)
async def PostLabels(labels: Labels):
    '''
    Client POST labels
    Will also check consensus after each label post. See the check_request method in Pipeline
    
    TODO: Give the labels to the consensus 
    '''
    return {"message": "Labels received"} # again probably won't be used   