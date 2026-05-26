import time
from fastapi import FastAPI, Request, Depends

app = FastAPI(title="Notes API")

@app.get("/")
def root():
    return {"message": "Notes API"}
