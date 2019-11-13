from pathlib import Path

import yaml


class Config:
    GPIO = 'gpio'
    LED_STRIP = 'led_strip'

    def __init__(self, config: dict):
        self.config = config

    def __getitem__(self, key):
        return self.config[key]

    @staticmethod
    def read(path: Path):
        with path.open('r') as f:
            return Config(yaml.load(f, Loader=yaml.FullLoader))

    def get(self, key, default):
        return self.config.get(key, default)
