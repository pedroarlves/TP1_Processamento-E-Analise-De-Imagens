from PyQt6.QtWidgets import QMainWindow, QFileDialog, QInputDialog, QMessageBox
from PyQt6.QtGui import QAction
from core.image_io import read_raw, write_raw, to_qimage, auto_detect_raw_shape
from ui.workspace import Workspace

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PSE-Image - Processamento e Análise de Imagens")
        self.setGeometry(100, 100, 800, 600)
        
        # Workspace visual
        self.workspace = Workspace()
        self.setCentralWidget(self.workspace)

        # Guarda imagem numpy atual (estado global)
        self.current_image = None  
        self.image_history = []     # Futuro: histórico de blocos/processamentos

        self._create_menu()

    # ---------------------------------------------------------------------
    # MENU SUPERIOR
    # ---------------------------------------------------------------------
    def _create_menu(self):
        menubar = self.menuBar()

        # ---------------- Arquivo ----------------
        file_menu = menubar.addMenu("Arquivo")
        open_action = QAction("Abrir RAW", self)
        open_action.triggered.connect(self.open_raw_image)
        file_menu.addAction(open_action)

        save_action = QAction("Salvar RAW", self)
        save_action.triggered.connect(self.save_raw_image)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        exit_action = QAction("Sair", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # ---------------- Processamento ----------------
        process_menu = menubar.addMenu("Processamento")

        brightness_action = QAction("Ajustar Brilho", self)
        brightness_action.triggered.connect(self.open_brightness_dialog)
        process_menu.addAction(brightness_action)

        # ADICIONE ESTAS LINHAS PARA OS NOVOS BLOCOS:
        process_menu.addSeparator()
        
        diff_action = QAction("Diferença entre Imagens", self)
        diff_action.triggered.connect(self.open_diff_dialog)
        process_menu.addAction(diff_action)
        
        conv_action = QAction("Convolução Personalizada", self)
        conv_action.triggered.connect(self.open_convolution_dialog)
        process_menu.addAction(conv_action)
        
    # ---------------------------------------------------------------------
    # Diálogo de brilho
    # ---------------------------------------------------------------------
    def open_brightness_dialog(self):
        """Abre janela de ajuste de brilho."""
        if self.current_image is None:
            QMessageBox.warning(self, "Aviso", "Nenhuma imagem carregada.")
            return

        from ui.dialog_brilho import BrightnessDialog
        dialog = BrightnessDialog(self)
        dialog.exec()

    # ---------------------------------------------------------------------
    # ABRIR IMAGEM RAW
    # ---------------------------------------------------------------------
    def open_raw_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Selecionar imagem RAW", "", "RAW Files (*.raw)")
        if not file_path:
            return

        w, h = auto_detect_raw_shape(file_path)

        if w is None:
            QMessageBox.warning(
                self,
                "Dimensões desconhecidas",
                "Não foi possível detectar automaticamente o tamanho da imagem.\n"
                "Digite manualmente as dimensões."
            )
            width, ok_w = QInputDialog.getInt(self, "Largura", "Digite a largura da imagem:", 256, 1, 4096)
            if not ok_w: return
            height, ok_h = QInputDialog.getInt(self, "Altura", "Digite a altura da imagem:", 256, 1, 4096)
            if not ok_h: return
        else:
            width, height = w, h

        try:
            img = read_raw(file_path, width, height)
            qimg = to_qimage(img)
            self.workspace.show_image(qimg)
            self.current_image = img
            self.image_history = [img.copy()]  # reseta histórico
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao abrir imagem RAW:\n{e}")

    # ---------------------------------------------------------------------
    # SALVAR IMAGEM RAW
    # ---------------------------------------------------------------------
    def save_raw_image(self):
        """Salva a imagem atualmente exibida (última do pipeline)."""
        if self.current_image is None:
            QMessageBox.warning(self, "Aviso", "Nenhuma imagem carregada ou processada para salvar.")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Salvar imagem RAW", "", "RAW Files (*.raw)")
        if not file_path:
            return

        try:
            write_raw(self.current_image, file_path)
            QMessageBox.information(self, "Sucesso", f"Imagem salva com sucesso em:\n{file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao salvar imagem RAW:\n{e}")

    # ---------------------------------------------------------------------
    # INTERFACE PARA PROCESSAMENTO FUTURO
    # ---------------------------------------------------------------------
    def update_current_image(self, new_image, replace=True):
        """
        Atualiza a imagem atual após processamento (brilho, limiarização etc.).
        Se replace=False, atualiza apenas a exibição (não altera o histórico).
        """
        from core.image_io import to_qimage
        qimg = to_qimage(new_image)
        self.workspace.show_image(qimg)

        if replace:
            self.current_image = new_image
            self.image_history.append(new_image.copy())

        # ---------------------------------------------------------------------
    # Diálogo de diferença entre imagens
    # ---------------------------------------------------------------------
    def open_diff_dialog(self):
        """Abre janela para calcular diferença entre duas imagens."""
        from ui.dialog_diff import DiffDialog
        dialog = DiffDialog(self)
        dialog.exec()

    # ---------------------------------------------------------------------
    # Diálogo de convolução personalizada
    # ---------------------------------------------------------------------
    def open_convolution_dialog(self):
        """Abre janela para convolução com máscara personalizada."""
        if self.current_image is None:
            QMessageBox.warning(self, "Aviso", "Nenhuma imagem carregada.")
            return
        
        from ui.dialog_convolution import ConvolutionDialog
        dialog = ConvolutionDialog(self)
        dialog.exec()