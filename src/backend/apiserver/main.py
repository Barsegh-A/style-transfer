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
db = redis.StrictRedis(host=os.environ.get("REDIS_HOST", "localhost"))
QUEUE_NAME = "job_queue"

origins = ["*"]

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
    db.rpush(QUEUE_NAME, json.dumps(job_dict))
    queue_length = db.llen(QUEUE_NAME)
    data = {"status": "submitted", "id": job_id, "queue_length": queue_length}
    return data


@app.get("/job/")
async def read_item(job_id: str):
    output = db.get(job_id)
    if output is not None:
        output_dict = json.loads(output.decode("utf-8"))
        # db.delete(job_id)
        return {"status": output_dict["status"], "image": output_dict["image"]}
    else:
        return {"status": "queued", "image": None}
