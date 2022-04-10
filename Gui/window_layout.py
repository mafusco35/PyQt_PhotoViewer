from PyQt5 import QtWidgets, QtCore
import sys

# from PIL import Image, ImageQt

from . import photo_viewer as viewer

# from logging_functions import BlankLogger


class WindowLayout(QtWidgets.QMainWindow):
    def __init__(
        self,
        screen: QtWidgets.QApplication.primaryScreen = None,
        parent=None,
    ):
        super().__init__(parent=parent)
        top = 0
        left = 0
        #        height = 750
        #        width = 750
        if screen is None:
            self.width, self.height = (750, 750)
        else:
            self.width = int(screen.size().width() * 0.85)
            self.height = int(screen.size().width() * 0.85)

        self.setWindowTitle("Photo Viewer")
        self.setGeometry(top, left, self.width, self.height)
        self.photo_file = None
        self.photo_list = []
        self.photo_number = -1
        self.init_ui()

    def init_ui(self):

        self._create_widgets()
        self._create_menu_actions()
        self._create_menu_bar()
        self._create_toolbars()
        self._create_layout()

        # self._connect_widgets()
        # self._connect_menu_actions()

        self.showMaximized()
        # self.set_photo(None)

    def _create_widgets(self):
        self.lb_name = QtWidgets.QLabel()
        self.lb_name.setText("Set Image Name (Will update filename)")
        self.et_name = QtWidgets.QLineEdit()

        self.lb_people = QtWidgets.QLabel()
        self.lb_people.setText("Tag People. Use commas to separate")
        self.et_people = QtWidgets.QLineEdit()

        self.lb_tags = QtWidgets.QLabel()
        self.lb_tags.setText("Set Image Tags")
        self.et_tags = QtWidgets.QLineEdit()

        self.bt_move = QtWidgets.QPushButton()
        self.bt_move.setText("Move Image File")

        self.bt_close = QtWidgets.QPushButton()
        self.bt_close.setText("Close Program")

        self.viewer = viewer.PhotoViewer(parent=self, screen=(self.width, self.height))

    def _create_layout(self):
        v_layout = QtWidgets.QVBoxLayout()
        h_layout = QtWidgets.QHBoxLayout()

        v_layout.addWidget(self.lb_name)
        v_layout.addWidget(self.et_name)

        v_layout.addWidget(self.lb_people)
        v_layout.addWidget(self.et_people)

        v_layout.addWidget(self.lb_tags)
        v_layout.addWidget(self.et_tags)

        v_layout.addWidget(self.bt_move)
        v_layout.addWidget(self.bt_close)

        wid = QtWidgets.QWidget(self)
        self.setCentralWidget(wid)

        # Add image scene to h_layout
        h_layout.addWidget(self.viewer)
        h_layout.addLayout(v_layout)

        wid.setLayout(h_layout)

    def _create_menu_bar(self):
        # Menu bar
        self.menu = QtWidgets.QMenuBar(self)
        self.setMenuBar(self.menu)

        self.menu_dict = {}
        # Creating menus using a QMenu object
        self.menu_dict["File"] = QtWidgets.QMenu("&File", self)
        self.menu_dict["Open"] = QtWidgets.QMenu("&Open...", self)
        self.menu.addMenu(self.menu_dict["File"])
        self.menu_dict["File"].addMenu(self.menu_dict["Open"])
        self.menu_dict["File"].addAction(self.action_dict["File"]["Exit"])
        self.menu_dict["Open"].addAction(self.action_dict["Open"]["File"])
        self.menu_dict["Open"].addAction(self.action_dict["Open"]["Folder"])
        self.menu_dict["Open"].addAction(self.action_dict["Open"]["TagSearch"])
        # Creating menus using a title
        edit_menu = self.menu.addMenu("&Edit")
        self.menu.addMenu(edit_menu)
        help_menu = self.menu.addMenu("&Help")
        self.menu.addMenu(help_menu)

    def _create_menu_actions(self):
        self.action_dict = {
            "File": {},
            "Open": {},
            "Edit": {},
            "Help": {},
            "Photo": {},
        }
        self.action_dict["Open"]["File"] = QtWidgets.QAction(
            self.style().standardIcon(QtWidgets.QStyle.SP_FileIcon),
            "&Open File",
            self,
        )
        self.action_dict["Open"]["Folder"] = QtWidgets.QAction(
            self.style().standardIcon(QtWidgets.QStyle.SP_DialogOpenButton),
            "&Open Folder",
            self,
        )
        self.action_dict["Open"]["TagSearch"] = QtWidgets.QAction(
            self.style().standardIcon(QtWidgets.QStyle.SP_FileDialogContentsView),
            "&Open By Photo Tags",
            self,
        )
        self.action_dict["File"]["Exit"] = QtWidgets.QAction(
            self.style().standardIcon(QtWidgets.QStyle.SP_DialogCloseButton),
            "&Exit",
            self,
        )
        self.action_dict["Photo"]["Next_Photo"] = QtWidgets.QAction(
            self.style().standardIcon(QtWidgets.QStyle.SP_ArrowRight),
            "&Next Photo",
            self,
        )
        self.action_dict["Photo"]["Prev_Photo"] = QtWidgets.QAction(
            self.style().standardIcon(QtWidgets.QStyle.SP_ArrowLeft),
            "&Previous Photo",
            self,
        )

    def _create_toolbars(self):
        self.toolbar_dict = {
            "Main": QtWidgets.QToolBar("Main", self),
            "Photo": QtWidgets.QToolBar("Photo", self),
        }
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolbar_dict["Main"])
        self.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolbar_dict["Photo"])

        self.toolbar_dict["Main"].addAction(self.action_dict["Open"]["File"])
        self.toolbar_dict["Main"].addAction(self.action_dict["Open"]["Folder"])
        self.toolbar_dict["Main"].addAction(self.action_dict["Open"]["TagSearch"])

        self.toolbar_dict["Photo"].addAction(self.action_dict["Photo"]["Prev_Photo"])
        self.toolbar_dict["Photo"].addAction(self.action_dict["Photo"]["Next_Photo"])


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("Photo Viewer")

    app.setStyle("Fusion")
    screen = app.primaryScreen()

    # logger = BlankLogger()
    window = WindowLayout(screen=screen)  # , logger=logger)
    window.show()

    sys.exit(app.exec_())
