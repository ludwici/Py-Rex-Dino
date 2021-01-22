from enum import Enum
from typing import Tuple

import pygame
from IslandPy.Render.ARenderObject import ARenderObject
from IslandPy.Scenes.AScene import AScene

from Obstacle import Obstacle


class DinoState(Enum):
    ON_IDLE = 0,
    ON_GROUND = 1,
    ON_JUMPING = 2,
    ON_FAILING = 4


class Dino(ARenderObject):
    def __init__(self, scene: AScene, position: Tuple[int, int], size: Tuple[int, int] = (0, 0)) -> None:
        super().__init__(scene, size, position=position)
        self.__images = [pygame.image.load("res/dino.png").convert_alpha(),
                         pygame.image.load("res/dino_left.png").convert_alpha(),
                         pygame.image.load("res/dino_right.png").convert_alpha(),
                         pygame.image.load("res/dino_right_down.png").convert_alpha(),
                         pygame.image.load("res/dino_left_down.png").convert_alpha()]

        self.__body = self.__images[0]
        self.rect = self.__body.get_rect()
        self.set_position(position)
        self.__bottom_pos_y = self.rect.bottom
        self.rect.w, self.rect.h = self.__body.get_rect().w, self.__body.get_rect().h

        self.__current_state = DinoState.ON_IDLE
        self.__velocity = 12
        self.__gravity = 12
        # self.speed = 6
        self.__jump_count = 0
        self.__c = 0
        self.__current_index = 0
        self.__index_modifier = 1

        self.behaviour = {DinoState.ON_IDLE: lambda: self.__idle(),
                          DinoState.ON_GROUND: lambda: self.__on_ground(),
                          DinoState.ON_JUMPING: lambda: self.__on_jumping(),
                          DinoState.ON_FAILING: lambda: self.__on_failing()}

    def __idle(self) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.__body, self.rect)

    def __change_image(self, index: int) -> None:
        self.__body = self.__images[index]
        self.rect.w, self.rect.h = self.__body.get_rect().w, self.__body.get_rect().h
        self.rect.bottom = self.__bottom_pos_y

    def __on_ground(self) -> None:
        self.__current_index += self.__index_modifier
        self.__change_image(self.__current_index)
        self.reset()

    def __on_jumping(self) -> None:
        self.rect.bottom -= self.__velocity
        if self.rect.topleft[1] <= 20:
            self.__current_state = DinoState.ON_FAILING

    def __on_failing(self) -> None:
        self.rect.bottom += self.__gravity
        if self.rect.bottom > self.__bottom_pos_y:
            self.rect.bottom = self.__bottom_pos_y
            self.__current_state = DinoState.ON_GROUND

    def start(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.__current_state = DinoState.ON_GROUND
        self.__gravity = 12

    def __jump(self) -> None:
        self.__current_state = DinoState.ON_JUMPING
        self.__change_image(0)
        self.__jump_count += 1
        if self.__jump_count % 60 == 0:
            Obstacle.speed += 1
            print(Obstacle.speed)

    def update(self, dt) -> None:
        self.__c += dt
        self.__current_index = (int(self.__c / 200) % 2)
        self.behaviour[self.__current_state]()

    def handle_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                if self.__current_state == DinoState.ON_GROUND:
                    self.__jump()

            if event.key == pygame.K_DOWN:
                if self.__current_state == DinoState.ON_JUMPING or self.__current_state == DinoState.ON_FAILING:
                    self.__gravity = 20
                    self.__current_state = DinoState.ON_FAILING
                    self.__index_modifier = 3

                if self.__current_state == DinoState.ON_GROUND:
                    self.__index_modifier = 3

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                if self.rect.topleft[1] < 200:
                    self.__current_state = DinoState.ON_FAILING

            if event.key == pygame.K_DOWN:
                self.__index_modifier = 1
