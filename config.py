import json
import os

class Config:

    def __init__(self):
        with open('data/conf.json', 'r') as c:
            info = json.load(c)
        self.endpoints = info['endpoints']
        self.token = info['token']
        self.galeria = info['galeria']
        self.output = os.path.expanduser("~/Pictures")
        self.default = os.path.expanduser("~/Pictures")

    def save(self):
        data = {
            "endpoints": self.endpoints,
            "token": self.token,
            "galeria": self.galeria
        }
        with open('data/conf.json', 'w') as c:
            json.dump(data, c, indent=4)

    def get_output(self, target):
        if self.output == self.default:
            return os.path.join(self.output, target)
        return self.output

config = Config()