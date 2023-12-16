import base64
import json
import logging
import os
import time
import numpy as np

import redis

from glob import glob
from dotenv import load_dotenv
from io import BytesIO
from PIL import Image

from model import style_transfer

load_dotenv()

db = redis.StrictRedis(host=os.environ.get("REDIS_HOST", "localhost"))
QUEUE_NAME = "job_queue"


def decode_base64_to_pil(base64_string):
    if base64_string.startswith("data:image"):
        _, base64_string = base64_string.split(",", 1)
    image_data = base64.b64decode(base64_string)
    image_bytesio = BytesIO(image_data)
    pil_image = Image.open(image_bytesio)
    return pil_image


def pil_to_base64_with_data_uri(pil_image):
    image_bytesio = BytesIO()
    pil_image.save(image_bytesio, format="JPEG")
    base64_encoded = base64.b64encode(image_bytesio.getvalue()).decode("utf-8")
    data_uri = f"data:image/jpeg;base64,{base64_encoded}"
    return data_uri


def main():
    style_dir = "./style_images/"

    while True:
        try:
            with db.pipeline() as pipe:
                pipe.lrange(QUEUE_NAME, 0, 1)
                pipe.ltrim(QUEUE_NAME, 1, -1)
                queue, _ = pipe.execute()

            for job in queue:
                job_dict = json.loads(job.decode("utf-8"))

                db.set(job_dict["id"], json.dumps({"status": "processing", "image": None}))

                image = decode_base64_to_pil(job_dict["image"])
                style = job_dict["style"]

                style_filenames = glob(os.path.join(style_dir, style, '*'))
                style_filename = np.random.choice(style_filenames)
                style_image = Image.open(style_filename)

                logging.info('Style Transfer processing started...')
                result = style_transfer(image, style_image)
                logging.info('Style Transfer processing finished.')
                db.set(job_dict["id"], json.dumps({"status": "finished", "image": pil_to_base64_with_data_uri(result)}))
        except Exception as e:
            logging.error(str(e))
            db.set(job_dict["id"], json.dumps({"status": "failed", "image": None}))

        time.sleep(0.1)


if __name__ == "__main__":
    main()
