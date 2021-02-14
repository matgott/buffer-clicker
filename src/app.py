import sys
import multiprocessing
from gui.gui import Gui


def main():
    gui = Gui()
    gui.run()


if __name__ == "__main__":
    multiprocessing.freeze_support()

    try:
        main()
    except Exception as e:
        print(e)
        sys.exit()
