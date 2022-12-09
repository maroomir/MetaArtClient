import os.path
import json
import warnings
from datetime import datetime

from PIL.Image import Image

import ui
import client

from ui import UIEvent

PRESET_SETTING = './setting.json'
PRESET_IP = '127.0.0.1'
PRESET_TEST = 'health'
PRESET_DALLE = 'dalle'
PRESET_RESULT_PATH = '../../Downloads/MetaArtClient/'
RESULTS = []


class TestEvent(UIEvent):

    def to_do(self, **kwargs):
        client.health(host=PRESET_IP, echo=PRESET_TEST)


class GoEvent(UIEvent):

    def to_do(self, num_images: int, text: str, debug_mode=False, **kwargs):
        global RESULTS
        RESULTS = client.dalle(host=PRESET_IP, num_images=num_images, text=text, echo=PRESET_DALLE)
        if not isinstance(RESULTS, list):
            warnings.warn(f'{text} is not generated!')
        if debug_mode:
            client.show_image(RESULTS)
        return client.combine_image(RESULTS)


class SaveEvent(UIEvent):
    def to_do(self, title: str, **kwargs):
        if isinstance(RESULTS, list):
            for i, img in enumerate(RESULTS):
                if isinstance(img, Image):
                    impath = os.path.join(PRESET_RESULT_PATH,
                                          f'{title}_{datetime.today().strftime("%m%d%H%M%S")}_{i}.jpg')
                    img.save(impath, 'JPEG')


if __name__ == "__main__":
    if os.path.exists(PRESET_SETTING):
        with open(PRESET_SETTING, 'r') as file:
            setting = json.load(file)
        PRESET_IP, PRESET_TEST, PRESET_DALLE = setting['ip'], setting['test'], setting['dalle']
        PRESET_RESULT_PATH = setting['result_path']
    test_event, go_event, save_event = TestEvent(), GoEvent(), SaveEvent()
    ui.init(10, 30, 1280, 480, 0.7, events={'test': test_event, 'go': go_event, 'save': save_event})
