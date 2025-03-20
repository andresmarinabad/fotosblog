import requests
import os
from config import config
from db import insert_image, image_exists
from celery import Celery

app = Celery(
    "image_downloader",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@app.task
def download_image(url, target):
    if not image_exists(target, url):
        filename = os.path.basename(url)
        try:
            print(f'Downloading {filename}')
            response = requests.get(url, stream=True)
            response.raise_for_status()

            output = os.path.join(config.get_output(target), filename)
            os.makedirs(config.get_output(target), exist_ok=True)
            with open(output, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            print(f'Saved in {output}')

            insert_image(target, url)
            return True
        except Exception as e:
            print(f'Error: Cannot download image {filename}')
            return False
    return False

app.conf.task_routes = {"celery_app.download_image": {"queue": "images"}}