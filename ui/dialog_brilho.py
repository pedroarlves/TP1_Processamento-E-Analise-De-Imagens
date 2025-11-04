from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QSlider, QPushButton
from PyQt6.QtCore import Qt

class BrightnessDialog(QDialog):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.setWindowTitle("Ajuste de Brilho")
        self.setFixedSize(300, 150)

        self.main_window = main_window
        self.slider_value = 0
        self.original_image = None  # Guarda imagem antes do ajuste

        # Faz uma cópia da imagem atual (para não sobrescrever)
        if self.main_window.current_image is not None:
            import numpy as np
            self.original_image = np.copy(self.main_window.current_image)

        layout = QVBoxLayout()

        self.label = QLabel("Brilho: 0")
        layout.addWidget(self.label)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(-100)
        self.slider.setMaximum(100)
        self.slider.setValue(0)
        self.slider.valueChanged.connect(self.update_label)
        layout.addWidget(self.slider)

        self.btn_apply = QPushButton("Aplicar e Fechar")
        self.btn_apply.clicked.connect(self.apply_and_close)
        layout.addWidget(self.btn_apply)

        self.setLayout(layout)

    def update_label(self, value):
        """Atualiza texto e aplica brilho em tempo real."""
        self.label.setText(f"Brilho: " + str(value))
        self.slider_value = value

        if self.original_image is not None:
            from core.point_ops import adjust_brightness
            new_img = adjust_brightness(self.original_image, value)
            self.main_window.update_current_image(new_img, replace=False)

    def apply_and_close(self):
        """Aplica definitivamente o brilho e fecha o diálogo."""
        # Atualiza a imagem principal com o brilho aplicado
        if self.original_image is not None:
            from core.point_ops import adjust_brightness
            final_img = adjust_brightness(self.original_image, self.slider_value)
            self.main_window.update_current_image(final_img)
        self.close()
