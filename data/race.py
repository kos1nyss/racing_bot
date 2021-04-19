from .all_models import *
from PIL import Image, ImageDraw
from random import randint


class Race:
    size = 40, 200
    car_w, car_h = 10, 20
    padding = 5
    pos_xs = [padding, size[0] - padding - car_w]

    def __init__(self, c1: Car, c2: Car):
        self.cars = [c1, c2]
        self.result = []
        self.content = [[], []]
        self.winner = None

    def clear(self) -> None:
        self.winner = None
        self.result.clear()
        self.content = [[], []]

    def execute(self, length: int) -> None:
        delta_time = 0.1
        lengths, speeds, times = [0, 0], [0, 0], [0, 0]
        images = [[], []]
        while list(filter(lambda x: x < length, lengths)):
            for i in range(2):
                if lengths[i] < length:
                    if speeds[i] < self.cars[i].max_speed:
                        speeds[i] += self.cars[i].acceleration * delta_time
                    if lengths[i] > length / 2:
                        speeds[i] += self.cars[i].turbo * delta_time
                    lengths[i] += speeds[i]
                    if not self.winner and lengths[i] >= length:
                        self.winner = self.cars[i]

            for i in range(2):
                image = Image.new('RGBA', self.size, color='white')
                draw = ImageDraw.Draw(image, 'RGBA')
                colors = ['green', 'red'] if i == 0 else ['red', 'green']
                draw.rectangle(((0, self.size[1] - 5),
                                (self.size[0], self.size[1])),
                               fill='blue')
                for j in range(2):
                    x, y = self.pos_xs[j], self.size[1] * lengths[j] / length * (
                            self.size[1] - self.car_h) / self.size[1]
                    draw.rectangle(((x, y), (x + self.car_w, y + self.car_h)),
                                   fill=colors[j])
                images[i].append(image)
        filenames = []
        for i, imgs in enumerate(images):
            cov, *imgs = imgs
            fn = f'gif{i}.gif'
            cov.save(fp=fn, format='GIF', append_images=imgs, save_all=True, loop=0)
            filenames.append(fn)
        self.content = filenames

    def get_winner(self) -> Car:
        return self.winner

    def get_content(self) -> list:
        return self.content
