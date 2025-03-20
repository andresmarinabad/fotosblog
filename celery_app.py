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

app.conf.update(
    worker_log_format='%(message)s',
    worker_task_log_format='%(message)s',
    worker_redirect_stdouts_level='ERROR',
    worker_redirect_stdouts=True
)

app.conf.task_routes = {"celery_app.download_image": {"queue": "images"}}

@app.task
def download_image(url, target):
    filename = os.path.basename(url)
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        output = os.path.join(config.get_output(target), filename)
        os.makedirs(config.get_output(target), exist_ok=True)
        with open(output, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        print(f'Downloaded {output}')

        insert_image(target, url)
        return True
    except Exception as e:
        print(f'Error: Cannot download image {filename}')
        return False
