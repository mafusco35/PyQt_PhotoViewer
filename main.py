import sys
from PyQt5 import QtWidgets

import Gui.window_functionality as wf


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("Photo Viewer")

    app.setStyle("Fusion")
    screen = app.primaryScreen()

    # logger = BlankLogger()
    window = wf.WindowFunctionality(screen=screen)  # , logger=logger)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    pass
