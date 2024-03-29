from fastapi import FastAPI

app = FastAPI()  # initialize fast api server

@app.get("/")  # default root
async def root():
    return {"message": "Hello World"}
