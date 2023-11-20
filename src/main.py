import os

from preditor.preditor import Preditor


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    p = Preditor()
    # p.fit()
    # p.predict()


if __name__ == "__main__":
    main()
