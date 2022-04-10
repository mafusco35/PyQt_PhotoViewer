from PyQt5 import QtWidgets, QtGui, QtCore
import typing


class PhotoViewer(QtWidgets.QGraphicsView):
    right_arrow = QtCore.pyqtSignal()
    left_arrow = QtCore.pyqtSignal()

    def __init__(
        self,
        parent: QtWidgets.QMainWindow = None,
        screen: typing.Tuple[int, int] = None,
    ):
        super().__init__()
        # def create_photo_scene(self):
        self._zoom = 0
        self._empty = True
        self._scene = QtWidgets.QGraphicsScene(self)
        self._photo = QtWidgets.QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        self.setScene(self._scene)
        if screen is None:
            self.setMinimumSize(500, 650)
        else:
            self.setMinimumSize(screen[0] * 0.85, screen[1] * 0.85)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(30, 30, 30)))
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

    def has_photo(self) -> bool:
        return not self._empty

    def fitInView(self, scale: bool = True):
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.has_photo():
                unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                view_rect = self.viewport().rect()
                scene_rect = self.transform().mapRect(rect)
                factor = min(
                    view_rect.width() / scene_rect.width(),
                    view_rect.height() / scene_rect.height(),
                )
                self.scale(factor, factor)
            self._zoom = 0

    def remove_photo(self):
        for item in self._scene.selectedItems():
            self._scene.removeItem(item)
        self._scene.addItem(self._photo)
        self._scene.update()

    def set_photo(self, pixmap: QtGui.QPixmap = None):
        self._zoom = 0
        if pixmap and not pixmap.isNull():
            self._empty = False
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
            self._photo.setPixmap(pixmap)
            # self._scene.addItem(self._photo)
            self._scene.update()
        else:
            self._empty = True
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self._photo.setPixmap(QtGui.QPixmap())
            # self._scene.addItem(self._photo)
            self._scene.update()
        self.fitInView()

    def wheelEvent(self, event: QtGui.QWheelEvent):
        if self.has_photo():
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.fitInView()
            else:
                self._zoom = 0

    def toggleDragMode(self):
        if self.dragMode() == QtWidgets.QGraphicsView.ScrollHandDrag:
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        elif not self._photo.pixmap().isNull():
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if self._photo.isUnderMouse() and self.has_photo():
            if event.key() == QtCore.Qt.Key_Right:
                self.right_arrow.emit()
            elif event.key() == QtCore.Qt.Key_Left:
                self.left_arrow.emit()
        return super().keyPressEvent(event)

    # def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
    #     if self._photo.isUnderMouse():
    #         self.photo_clicked.emit(self.mapToScene(event.pos()).toPoint())
    #     return super().mousePressEvent(event)
