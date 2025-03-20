import requests
import time
import signal
import sys
import redis
import subprocess
import multiprocessing
from bs4 import BeautifulSoup
from db import image_exists
from config import config
from celery_app import download_image

r = redis.StrictRedis(host='localhost', port=6379, db=0)

headers = {
    "Authorization": f"Bearer {config.token}"
}

def start_celery_workers():
    worker_command = [
        "celery",
        "-A", "celery_app",
        "worker",
        "--queues=images",
        "--loglevel=ERROR"
    ]
    worker_process =  subprocess.Popen(worker_command)

    time.sleep(10)
    try:
        while True:
            if is_queue_empty():
                print("The queue is empty")
                stop_workers(worker_process)
                break
            else:
                time.sleep(5)
    except KeyboardInterrupt:
        print("Process interrupted")
    finally:
        stop_workers(worker_process)


def is_queue_empty():
    queue_length = r.llen('images')
    return queue_length == 0

# Función para detener los workers de Celery
def stop_workers(worker_process):
    print("Queue empty. Stopping workers...")
    worker_process.send_signal(signal.SIGTERM)

def start_redis_manual():
    try:
        redis_process = subprocess.Popen(["redis-server"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(2)
        print("Init redis manually")
        return redis_process
    except Exception as e:
        print(f"Error on init redis {e}")
        return None

def download_images_from_target(targets):
    start_redis_manual()
    worker_process = multiprocessing.Process(target=start_celery_workers)
    worker_process.start()

    print("Press Ctrl + C for safety exit")
    for target in targets:
        print(f'Acquiring endpoints for {target}')
        endpoint = config.endpoints[target]
        try:
            response = requests.get(endpoint)
        except requests.exceptions.RequestException as e:
            print(f"Error on target {target} endpoint")
            return False

        if response.status_code == 200:
            print('Parsing images links')
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('li')
            print('Sending endpoint links to the workers...')
            for link in links:
                id = link.get('id')
                if id:
                    galery = requests.get(f"{config.galeria}{id}", headers=headers)
                    json_data = galery.json()
                    for object in json_data:
                        for key, value in object.items():
                            if "urlImatgeGaleria" == key:
                                if not image_exists(target, value):
                                    download_image.delay(value, target)
        else:
            print(f"Error trying to acquire {target} pictures. Review the endpoints")

    worker_process.join()
    print('All downloaded. Exiting...')
