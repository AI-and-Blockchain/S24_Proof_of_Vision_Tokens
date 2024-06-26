# FastAPI Pipeline Server

This repository contains a FastAPI pipeline server that handles requests, batches, and labels for a machine learning pipeline.

## Organization
* app.py: The FastAPI application that defines the API endpoints.
* classes.py: Where all the classes are defined.
    * The exception is the consensus class, which is defined in ImageLabelConsensus.py
* test_app.py: The tests for the FastAPI application.
* test_classes.py: The tests for the classes.
* server.py: A small script that cyclic runs to start the server.


## Deployment

The website is hosted at https://dull-scrubs-bee.cyclic.app/. You can view all the available endpoints and interact with the API using the Swagger UI at https://dull-scrubs-bee.cyclic.app/docs. For testing, please use a local version so the hosting state doesn't get messed up.

## Installation and Setup

If you want to run this locally, follow these steps:
1. Clone the repository:
   ```
   git clone https://github.com/your-username/your-repo.git
   ```

2. Install the required dependencies:
   ```
   pip install fastapi uvicorn pydantic pytest httpx
   ```

3. Navigate to the server directory:
   ```
   cd python/pipeline/
   ```

4. Run the server:
   ```
   uvicorn app:app --reload
   ```

5. Access the API:
   - Open your web browser and go to the URL displayed in the terminal, which is likely `http://127.0.0.1:8000`.
   - You should see the message "API is working".
   - To view the Swagger UI documentation, append `/docs` to the URL, e.g., `http://127.0.0.1:8000/docs`.

If everything is done correctly, you will see this UI when going to the docs:
![image](https://github.com/AI-and-Blockchain/S24_Proof_of_Vision_Tokens/assets/75578919/55c8d98d-efbc-4313-b438-60cf1ce0de18)


## Example Usage with Dummy Data
These steps can be done locally or on the hosted website, however the hosted website might not have the same data as the local version so local is recommended. It's reccomended to use the Swagger UI to interact with the API. Note that these steps don't necessarily have to be done in order except for the first newRequest call. You can also just play around, as the error messages should be descriptive enough to guide you.

1. Create a new request using /newRequest with the following dummy data. To do this on the docs, select "POST /newRequest", click "Try it Out", paste this in, and click "Execute". The response will be under "Server Response".
```
{
  "requestID": 1,
  "datasetSource": "https://drive.google.com/file/d/1P6kHVYGYd7xUTa6bW_37rdY4QHb9NDYa/view?usp=sharing",
  "numImages": 3,
  "modelSource": "https://huggingface.co/spaces/ayaanzaveri/mnist/resolve/c959fe1db8b15ed643b91856cb2db4e2a3125938/mnist-model.h5",
  "requestOwner": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
  "bid": 10
}
```
Example with sucessful response:![image](https://github.com/AI-and-Blockchain/S24_Proof_of_Vision_Tokens/assets/75578919/4ce9a94e-b53c-4ace-a6b5-2978aef5669d)

2. Call /batch using any address that is formatted correctly. If this is not the first time, make sure that a different address is supplied each time.
3. Call /label. Edit the given structure to fit the call, ensuring that the requestID and address are the same as previous calls. Here is a template based off of the example object for newRequest:
```
{
  "requestID": 1,
  "userEthAddress": "<Same address as the one that was called at /batch",
  "labels": [
    1, 2, 3
  ]
}
```
5. Repeat steps 2 and 3 until the batch is complete. For testing, this is currently hard coded to require 3 sets of labels. It will return the consensus label from the /label call.
    * You can also just provide all /batch calls and then all /label calls, which can be easier.

Example consensus reach:
![image](https://github.com/AI-and-Blockchain/S24_Proof_of_Vision_Tokens/assets/75578919/010eddd0-19d9-4695-9b79-c41b1d6985c7)

For information, call /showlabels or /showreq for the current labels and the current active request. 

## Running Tests

To run the tests for the API endpoints, follow these steps:

1. Make sure you have the required dependencies installed (see the "Installation and Setup" section above).

2. Navigate to the tests directory:
   ```
   cd python/pipeline
   ```

3. Run the tests using pytest:
   ```
   pytest
   ```

Example run:
![image](https://github.com/AI-and-Blockchain/S24_Proof_of_Vision_Tokens/assets/75578919/3ee48e53-a335-4218-9a9c-9cd507e8ff0f)
