from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import logging
from PIL import Image, ImageQt

from . import window_layout

import helper_functions
import config

from logging_functions import BlankLogger


# class BlankLogger:
#     def __init__(self):
#         pass

#     def info(self, message):
#         print(message)

#     def warning(self, message):
#         print(message)

#     def __str__(self):
#         return "Blank logging class to allow for testing without logging thread"


class WindowFunctionality(window_layout.WindowLayout):
    def __init__(
        self,
        screen: QtWidgets.QApplication.primaryScreen = None,
        parent=None,
        logger: logging.Logger = BlankLogger(),  # BlankLogger(),
    ):
        super().__init__(screen=screen, parent=parent)
        self.logger = logger
        self.init_functionality()

    def init_functionality(self):

        self._connect_widgets()
        self._connect_menu_actions()

    def _connect_widgets(self):
        self.et_name.returnPressed.connect(self.rename_photo)
        self.et_people.returnPressed.connect(self.set_people_tags)
        self.et_tags.returnPressed.connect(self.set_other_tags)
        self.bt_move.clicked.connect(self.move_photo_file)
        self.bt_close.clicked.connect(self.close_program)

        # photo viewer connections
        self.viewer.right_arrow.connect(self.next_photo)
        self.viewer.left_arrow.connect(self.previous_photo)

    def _connect_menu_actions(self):
        self.action_dict["Open"]["File"].triggered.connect(self.open_file)
        self.action_dict["Open"]["Folder"].triggered.connect(self.open_file_directory)
        self.action_dict["File"]["Exit"].triggered.connect(self.close_program)

        self.action_dict["Photo"]["Next_Photo"].triggered.connect(self.next_photo)
        self.action_dict["Photo"]["Prev_Photo"].triggered.connect(self.previous_photo)

    def open_file(self):
        # options = QtWidgets.QFileDialog.options()
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Open Image File",
            # "C:\\",
            config.TEST_IMAGE_DIRECTORY,
            "Image files (*.jpg *.gif *.jpeg *.tif);;All Files (*)",
            # options=options,
        )
        if not file_name:
            self.logger.info("No image selected")
            return
        self.file_name = file_name
        self.logger.info("Set file name")
        photo = helper_functions.load_photo(self.file_name)
        self.set_photo(photo)

    def open_file_directory(self):
        dir_name = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            "Open Directory of Images",
            config.TEST_IMAGE_DIRECTORY,
            # "C:\\",
        )
        if not dir_name:
            self.logger.info("No directory selected")
            return

        self.dir_name = dir_name
        self.logger.info("Set directory name")
        self.photo_list = helper_functions.load_images_from_directory(self.dir_name)
        self.photo_number = -1
        self.next_photo()

    @QtCore.pyqtSlot()
    def close_program(self):
        self.close()

    @QtCore.pyqtSlot()
    def rename_photo(self):
        if not self.check_for_photo:
            return
        # new_name = self.lb_name.text().replace(" ", "")

    @QtCore.pyqtSlot()
    def set_people_tags(self):
        if not self.check_for_image:
            return

    @QtCore.pyqtSlot()
    def set_other_tags(self):
        if not self.check_for_image:
            return

    @QtCore.pyqtSlot()
    def move_photo_file(self):
        if not self.check_for_photo:
            return

    def check_for_photo(self):
        if self.photo_file is None:
            # Error message popup - no image file loaded
            return False
        return True

    def photo_clicked(self, pos: float):
        if self.viewer.dragMode() == QtWidgets.QGraphicsView.NoDrag:
            pass

    def next_photo(self):
        if len(self.photo_list) == 0:
            self.logger.info("No photo list to flip through")
            return

        self.photo_number += 1
        if self.photo_number >= len(self.photo_list):
            self.photo_number = 0

        self.logger.info(f"Photo number: {self.photo_number}")
        self.set_photo(self.photo_list[self.photo_number])

    def previous_photo(self):
        if len(self.photo_list) == 0:
            self.logger.info("No photo list to flip through")
            return

        self.photo_number -= 1
        if self.photo_number < 0:
            self.photo_number = len(self.photo_list) - 1

        self.logger.info(f"Photo number: {self.photo_number}")
        self.set_photo(self.photo_list[self.photo_number])

    def set_photo(self, image: Image.Image):
        if self.viewer.has_photo():
            self.viewer.remove_photo()

        self.image = ImageQt.ImageQt(image)
        self.pixmap = QtGui.QPixmap.fromImage(self.image)
        self.logger.info("Created QPixmap")
        self.pixmap = self.pixmap.transformed(QtGui.QTransform().rotate(90))
        self.viewer.set_photo(self.pixmap)
        self.logger.info("Set photo to viewer")


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("Photo Viewer")

    app.setStyle("Fusion")
    screen = app.primaryScreen()

    # logger = BlankLogger()
    window = WindowFunctionality(screen=screen)  # , logger=logger)
    window.show()

    sys.exit(app.exec_())
