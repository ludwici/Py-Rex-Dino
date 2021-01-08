import pygame
from IslandPy.Render.UI.TextLabel import TextLabel
from IslandPy.Scenes.AScene import AScene
from pygame import Color

from Dino import Dino
from Obstacle import Obstacle


class DinoScene(AScene):
    def __init__(self, name: str) -> None:
        super().__init__(name)

        self.dino = Dino(scene=self, position=(300, 250))
        self.objects.append(self.dino)
        # TODO: Use TextLabel.copy_style_from()
        self.__no_internet_label = TextLabel(self, font_size=22, text="Нет подключения к Интернету",
                                             color=Color(154, 160, 166), font_name="segoeui", bold=True,
                                             position=(self.dino.get_position()[0], self.dino.rect.bottom + 20))
        self.__text1 = TextLabel(self, font_size=14, text="Попробуйте сделать следующее:", color=Color(154, 160, 166),
                                 font_name="segoeui", position=(self.__no_internet_label.get_position()[0],
                                                                self.__no_internet_label.rect.bottom), bold=True)
        self.__text2 = TextLabel(self, font_size=14, text="• Проверьте сетевые кабели, модем и маршрутизатор.",
                                 color=Color(154, 160, 166), font_name="segoeui", bold=True,
                                 position=(self.__text1.get_position()[0] + 20, self.__text1.rect.bottom))
        self.__text3 = TextLabel(self, font_size=14, text="• Подключитесь к сети Wi-Fi ещё раз.",
                                 color=Color(154, 160, 166), font_name="segoeui", bold=True,
                                 position=(self.__text2.get_position()[0], self.__text2.rect.bottom))
        self.__text4 = TextLabel(self, font_size=14, text="ERR_INTERNET_DISCONNECTED", bold=False,
                                 color=Color(154, 160, 166),
                                 position=(self.__text1.get_position()[0], self.__text3.rect.bottom + 20))

        self.__is_running = False

        self.__ground_chunk1 = pygame.image.load("res/ground1.png").convert_alpha()
        self.__ground_chunk2 = pygame.image.load("res/ground1.png").convert_alpha()

        self.__ground_chunk1_rect = self.__ground_chunk1.get_rect()
        self.__ground_chunk2_rect = self.__ground_chunk2.get_rect()

        self.__ground_chunk1_rect.bottom = self.__ground_chunk2_rect.bottom = self.dino.rect.bottom
        self.__ground_chunk1_rect.x = 0
        self.__ground_chunk2_rect.x = self.__ground_chunk1_rect.right

        self.__points = 0
        self.__high_score = 0
        self.__point_label = TextLabel(self, 30, text="00000", color=Color(154, 160, 166),
                                       position=(pygame.display.get_window_size()[0] - 300, 50))

        self.__cactus = Obstacle(self)
        self.__cactus.set_position((pygame.display.get_window_size()[0] * 2, self.dino.rect.y))

        self.__cactus2 = Obstacle(self)
        self.__cactus2.set_position((pygame.display.get_window_size()[0], self.dino.rect.y))

    def draw(self, surface: pygame.Surface) -> None:
        if self.__is_running:
            surface.blit(self.__ground_chunk1, self.__ground_chunk1_rect)
            surface.blit(self.__ground_chunk2, self.__ground_chunk2_rect)
        super(DinoScene, self).draw(surface)

    def update(self, dt) -> None:
        super(DinoScene, self).update(dt)
        if self.__is_running:
            print(Obstacle.speed)
            self.__ground_chunk1_rect.x -= Obstacle.speed
            self.__ground_chunk2_rect.x -= Obstacle.speed
            self.__points += 1
            self.__point_label.text = f"{int(self.__points/10):05d}"

            if self.__ground_chunk1_rect.right < 0:
                self.__ground_chunk1_rect.x = self.__ground_chunk2_rect.right
            if self.__ground_chunk2_rect.right < 0:
                self.__ground_chunk2_rect.x = self.__ground_chunk1_rect.right

    def reset_game(self):
        self.__is_running = False
        self.__high_score = max(self.__points, self.__high_score)
        self.__points = 0
        self.dino.reset()

    def __start_game(self) -> None:
        self.__is_running = True
        self.__no_internet_label.hide()
        self.__text1.hide()
        self.__text2.hide()
        self.__text3.hide()
        self.__text4.hide()
        self.__cactus.start()
        self.__cactus2.start()

    def handle_events(self, event: pygame.event.Event) -> None:
        super(DinoScene, self).handle_events(event)
        if not self.__is_running:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.__start_game()
