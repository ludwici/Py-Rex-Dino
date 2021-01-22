from typing import Tuple
import random
import pygame
from IslandPy.Render.ARenderObject import ARenderObject
from IslandPy.Scenes.AScene import AScene


class Obstacle(ARenderObject):

    speed = 8

    def __init__(self, scene: AScene, size: Tuple[int, int] = (0, 0)):
        super().__init__(scene, size)
        self.images = []
        for i in range(1, 6):
            self.images.append(pygame.image.load(f"res/cactus{i}.png").convert_alpha())

        self._body = self.images[0]
        self.rect = self._body.get_rect()
        self.__start_pos_y = 0
        self.is_started = False
        self.hide()

    def update(self, dt) -> None:
        if self.is_started:
            self.rect.x -= Obstacle.speed

    def change_image(self) -> None:
        b = self.rect.bottom
        self._body = random.choice(self.images)
        self.rect.w, self.rect.h = self._body.get_rect().w, self._body.get_rect().h
        self.rect.bottom = b

    def start(self) -> None:
        self.show()
        self.is_started = True

    def draw(self, surface: pygame.Surface) -> None:
        if self.is_draw:
            surface.blit(self._body, self.rect)
