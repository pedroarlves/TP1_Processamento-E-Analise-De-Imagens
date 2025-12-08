from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFileDialog, QMessageBox, QComboBox)
from PyQt6.QtCore import Qt
from core.image_io import read_raw, to_qimage, auto_detect_raw_shape
from core.diff import image_difference

class DiffDialog(QDialog):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.setWindowTitle("Diferença entre Imagens")
        self.setFixedSize(400, 200)

        self.main_window = main_window
        self.image1 = None
        self.image2 = None

        layout = QVBoxLayout()

        # Imagem 1
        hbox1 = QHBoxLayout()
        hbox1.addWidget(QLabel("Imagem 1:"))
        self.btn_img1 = QPushButton("Selecionar...")
        self.btn_img1.clicked.connect(lambda: self.select_image(1))
        hbox1.addWidget(self.btn_img1)
        self.label_img1 = QLabel("Nenhuma imagem selecionada")
        hbox1.addWidget(self.label_img1)
        layout.addLayout(hbox1)

        # Imagem 2
        hbox2 = QHBoxLayout()
        hbox2.addWidget(QLabel("Imagem 2:"))
        self.btn_img2 = QPushButton("Selecionar...")
        self.btn_img2.clicked.connect(lambda: self.select_image(2))
        hbox2.addWidget(self.btn_img2)
        self.label_img2 = QLabel("Nenhuma imagem selecionada")
        hbox2.addWidget(self.label_img2)
        layout.addLayout(hbox2)

        # Botões
        btn_layout = QHBoxLayout()
        self.btn_calculate = QPushButton("Calcular Diferença")
        self.btn_calculate.clicked.connect(self.calculate_diff)
        self.btn_calculate.setEnabled(False)
        btn_layout.addWidget(self.btn_calculate)

        self.btn_cancel = QPushButton("Cancelar")
        self.btn_cancel.clicked.connect(self.close)
        btn_layout.addWidget(self.btn_cancel)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def select_image(self, img_num):
        """Seleciona uma imagem RAW."""
        file_path, _ = QFileDialog.getOpenFileName(self, f"Selecionar Imagem {img_num}", "", "RAW Files (*.raw)")
        if not file_path:
            return

        # Detectar dimensões
        w, h = auto_detect_raw_shape(file_path)
        if w is None:
            QMessageBox.warning(self, "Erro", "Não foi possível detectar dimensões da imagem.")
            return

        try:
            img = read_raw(file_path, w, h)
            
            if img_num == 1:
                self.image1 = img
                self.label_img1.setText(file_path.split("/")[-1])
            else:
                self.image2 = img
                self.label_img2.setText(file_path.split("/")[-1])

            # Ativa botão se ambas imagens estão carregadas
            if self.image1 is not None and self.image2 is not None:
                # Verifica se as imagens têm o mesmo tamanho
                if self.image1.shape == self.image2.shape:
                    self.btn_calculate.setEnabled(True)
                else:
                    self.btn_calculate.setEnabled(False)
                    QMessageBox.warning(self, "Erro", "As imagens devem ter o mesmo tamanho!")
                    
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao carregar imagem:\n{e}")

    def calculate_diff(self):
        """Calcula e exibe a diferença entre as duas imagens."""
        try:
            # Calcular diferença
            diff_img = image_difference(self.image1, self.image2)
            
            # Converter para QImage e exibir
            qimg = to_qimage(diff_img)
            self.main_window.workspace.show_image(qimg)
            self.main_window.current_image = diff_img
            self.main_window.image_history.append(diff_img.copy())
            
            QMessageBox.information(self, "Sucesso", "Diferença calculada e exibida!")
            self.close()
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao calcular diferença:\n{e}")