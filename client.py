import base64
from io import BytesIO

import requests
from PIL import Image
import matplotlib.pyplot
import numpy


def health(host: str, echo='health'):
    res = requests.get(f'{host}/{echo}')
    if 200 <= res.status_code < 300:
        print(f'=> Receive({echo}) : {res.text}')


def dalle(host: str, num_images: int, text: str, echo='dalle'):
    data = {'num_images': num_images,
            'text': text}
    res = requests.post(f'{host}/{echo}', json=data)
    if 200 <= res.status_code < 300:
        return decode_image(res.json())


def decode_image(data: dict):
    res = []
    for i, img_encode in enumerate(data):
        print(f'=> Receive({i}) : {img_encode}')
        res.append(Image.open(BytesIO(base64.b64decode(img_encode))))
    return res


def combine_image(imgs: list, default_size=10):
    if not isinstance(imgs, list) or len(imgs) == 0:
        return numpy.zeros((default_size, default_size))
    else:
        return numpy.concatenate(imgs, axis=1)


def show_image(imgs: list, width=50, height=10):
    if not isinstance(imgs, list) or len(imgs) == 0:
        return
    matplotlib.pyplot.figure(figsize=(width, height))
    matplotlib.pyplot.imshow(combine_image(imgs))
    matplotlib.pyplot.show()


if __name__ == "__main__":
    import json
    with open('setting.json', 'r') as file:
        item = json.load(file)
    health(item['ip'], item['test'])
    images = dalle(item['ip'], 4, 'spaceship truck', item['dalle'])
    show_image(images)
