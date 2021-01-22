from IslandPy.RenderWindow import RenderWindow

from DinoScene import DinoScene


def main():
    r = RenderWindow(bg_color=(32, 33, 36))
    r.fps = 75
    ds = DinoScene("Dino Scene")
    r.start(ds)


if __name__ == '__main__':
    main()
