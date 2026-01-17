import sys
from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def run():
    return "server working"
