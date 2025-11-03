# ./ui/main_window.py

from PyQt6.QtWidgets import QMainWindow, QFileDialog, QInputDialog, QMessageBox
from PyQt6.QtGui import QAction
from core.image_io import read_raw, to_qimage
from ui.workspace import Workspace

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PSE-Image - Processamento e Análise de Imagens")
        self.setGeometry(100, 100, 800, 600)
        
        self.workspace = Workspace()
        self.setCentralWidget(self.workspace)

        self._create_menu()

    def _create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Arquivo")

        open_action = QAction("Abrir RAW", self)
        open_action.triggered.connect(self.open_raw_image)
        file_menu.addAction(open_action)

    def open_raw_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Selecionar imagem RAW", "", "RAW Files (*.raw)")
        if not file_path:
            return

        try:
            width, ok_w = QInputDialog.getInt(self, "Largura", "Digite a largura da imagem:", 256, 1, 4096)
            if not ok_w: return
            height, ok_h = QInputDialog.getInt(self, "Altura", "Digite a altura da imagem:", 256, 1, 4096)
            if not ok_h: return

            img = read_raw(file_path, width, height)
            qimg = to_qimage(img)
            self.workspace.show_image(qimg)

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao abrir imagem RAW:\n{e}")
