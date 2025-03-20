import requests
import time
import signal
import sys
import subprocess
from bs4 import BeautifulSoup
from db import image_exists
from config import config
from celery_app import download_image

headers = {
    "Authorization": f"Bearer {config.token}"
}

def start_celery_workers():
    worker_command = [
        "celery",
        "-A", "celery_app",
        "worker",
        "--queues=images"
    ]
    subprocess.Popen(worker_command)

def start_redis_manual():
    try:
        redis_process = subprocess.Popen(["redis-server"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(2)
        print("Init redis manually")
        return redis_process
    except Exception as e:
        print(f"Error on init redis {e}")
        return None

def signal_handler(sig, frame):
    print("\nProgram interrupted. Exiting...")
    subprocess.Popen(["celery -A celery_app control shutdown"])
    subprocess.Popen(["killall celery"])
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def download_images_from_target(targets):
    start_redis_manual()
    start_celery_workers()
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
            print('Downloading images...')
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




