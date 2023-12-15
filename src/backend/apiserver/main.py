import base64
import json
import os
import time
import uuid

import redis
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()

app = FastAPI()
db = redis.StrictRedis(host="localhost")

origins = [
    "http://localhost:3000",  # Add your frontend URL here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Reqeust(BaseModel):
    style: str
    image: str


@app.post("/submit_job/")
async def create_item(req: Reqeust):
    req_dict = req.dict()
    job_id = str(uuid.uuid4())
    job_dict = {"id": job_id, "image": req_dict["image"], "style": req_dict["style"]}
    db.rpush("job_queue", json.dumps(job_dict))
    data = {"status": "submitted", "id": job_id}
    return data


@app.get("/job/")
async def read_item(job_id: str):
    output = db.get(job_id)
    if output is not None:
        output_dict = json.loads(output.decode("utf-8"))
        # db.delete(job_id)
        return {"status": "finished", "image": output_dict["image"]}
    else:
        return {"status": "processing"}
