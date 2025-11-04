from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView
from PyQt6.QtCore import Qt

class Workspace(QGraphicsView):
    """Área principal onde blocos e imagens serão exibidos."""
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setRenderHints(self.renderHints())
        self.setMinimumSize(600, 400)

    def show_image(self, qimage):
        """Exibe uma imagem na cena."""
        from PyQt6.QtWidgets import QGraphicsPixmapItem
        from PyQt6.QtGui import QPixmap

        pixmap = QPixmap.fromImage(qimage)
        item = QGraphicsPixmapItem(pixmap)
        self.scene.clear()
        self.scene.addItem(item)
        self.fitInView(item, Qt.AspectRatioMode.KeepAspectRatio)
