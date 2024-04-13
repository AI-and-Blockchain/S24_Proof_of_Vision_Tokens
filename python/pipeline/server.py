import uvicorn
from app import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8181)


'''
This is for running the FastAPI server on Cyclic and can be ignored if you are running the server locally.
'''