import base64
import json
import os
import time
import uuid

import redis
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

load_dotenv()

app = FastAPI()
db = redis.StrictRedis(host=os.environ.get("REDIS_HOST"))


class Reqeust(BaseModel):
    image: str
    style: str


@app.post("/submit_job/")
async def create_item(req: Reqeust):
    req_dict = req.dict()
    job_id = str(uuid.uuid4())
    job_dict = {"id": job_id, "image": req_dict["image"], "style": req_dict["style"]}
    db.rpush(os.environ.get("IMAGE_QUEUE"), json.dumps(job_dict))
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
