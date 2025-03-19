import requests
import os
from bs4 import BeautifulSoup
from config import config
from db import image_exists, insert_image

headers = {
    "Authorization": f"Bearer {config.token}"
}

def download_images_from_target(targets):
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
                                    name = os.path.basename(value)
                                    download_image(value, target, name)

        else:
            print(f"Error trying to acquire {target} pictures. Review the endpoints")


def download_image(url, target, filename):
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



