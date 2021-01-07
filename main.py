from IslandPy.RenderWindow import RenderWindow

from DinoScene import DinoScene


def main():
    r = RenderWindow()
    ds = DinoScene("Dino Scene")
    r.start(ds)


if __name__ == '__main__':
    main()
