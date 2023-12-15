import base64
import json
import os
import time

import redis
from dotenv import load_dotenv
from io import BytesIO
from PIL import Image

load_dotenv()

db = redis.StrictRedis(host=os.environ.get("REDIS_HOST"))


def decode_base64_to_pil(base64_string):
    if base64_string.startswith("data:image"):
        _, base64_string = base64_string.split(",", 1)
    image_data = base64.b64decode(base64_string)
    image_bytesio = BytesIO(image_data)
    pil_image = Image.open(image_bytesio)
    return pil_image


def main():
    while True:
        with db.pipeline() as pipe:
            pipe.lrange(os.environ.get("IMAGE_QUEUE"), 0, 1)
            pipe.ltrim(os.environ.get("IMAGE_QUEUE"), 1, -1)
            queue, _ = pipe.execute()

        for job in queue:
            job_dict = json.loads(job.decode("utf-8"))
            image = decode_base64_to_pil(job_dict["image"])
            style = job_dict["style"]
            # TODO: add model predict on image and style
            db.set(job_dict["id"], json.dumps({"image": None}))

        time.sleep(0.1)


if __name__ == "__main__":
    main()
