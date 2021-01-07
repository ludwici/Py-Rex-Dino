from typing import Tuple

import pygame
from IslandPy.Render.ARenderObject import ARenderObject
from IslandPy.Scenes.AScene import AScene


class Dino(ARenderObject):
    def __init__(self, scene: AScene, position: Tuple[int, int], size: Tuple[int, int] = (0, 0)) -> None:
        super().__init__(scene, size, position=position)
        self.__start_pos_y = position[1]
        self.__body = pygame.image.load("dino.png").convert_alpha()
        self.rect.w, self.rect.h = self.__body.get_rect().w, self.__body.get_rect().h

        self.__on_ground = True
        self.__on_jumping = False
        self.__on_failing = False
        self.__speed = 3

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.__body, self.rect)

    def reset(self) -> None:
        self.__on_ground = True
        self.__on_jumping = False
        self.__on_failing = False
        self.__speed = 3

    def __jump(self):
        self.__on_ground = False
        self.__on_jumping = True

    def update(self, dt) -> None:
        if self.__on_jumping:
            self.rect.y -= self.__speed
            if self.rect.topleft[1] <= 50:
                self.__on_jumping = False
                self.__on_failing = True
        elif self.__on_failing:
            self.rect.y += self.__speed
            if self.rect.y == self.__start_pos_y:
                self.__on_failing = False
                self.__on_ground = True

    def handle_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if self.__on_ground:
                    self.__jump()
