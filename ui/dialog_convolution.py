from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QSpinBox, QTableWidget, QTableWidgetItem,
                             QComboBox, QMessageBox, QGroupBox)
from PyQt6.QtCore import Qt
import numpy as np
from core.local_ops import convolve, MASKS

class ConvolutionDialog(QDialog):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.setWindowTitle("Convolução Personalizada")
        self.setFixedSize(500, 400)

        self.main_window = main_window
        self.kernel_size = 3
        self.kernel = np.zeros((3, 3))

        layout = QVBoxLayout()

        # Seleção de máscara pré-definida
        group_preset = QGroupBox("Máscaras Pré-definidas")
        preset_layout = QVBoxLayout()
        
        self.combo_masks = QComboBox()
        self.combo_masks.addItem("Personalizada")
        for mask_name in MASKS.keys():
            self.combo_masks.addItem(mask_name)
        self.combo_masks.currentTextChanged.connect(self.load_preset_mask)
        preset_layout.addWidget(self.combo_masks)
        
        group_preset.setLayout(preset_layout)
        layout.addWidget(group_preset)

        # Tamanho do kernel
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("Tamanho do Kernel:"))
        self.spin_size = QSpinBox()
        self.spin_size.setMinimum(3)
        self.spin_size.setMaximum(11)
        self.spin_size.setSingleStep(2)  # Apenas tamanhos ímpares
        self.spin_size.setValue(3)
        self.spin_size.valueChanged.connect(self.update_kernel_table)
        size_layout.addWidget(self.spin_size)
        layout.addLayout(size_layout)

        # Tabela do kernel
        layout.addWidget(QLabel("Valores do Kernel:"))
        self.table_kernel = QTableWidget()
        self.table_kernel.cellChanged.connect(self.update_kernel_from_table)
        layout.addWidget(self.table_kernel)

        # Botões
        btn_layout = QHBoxLayout()
        
        self.btn_preview = QPushButton("Visualizar")
        self.btn_preview.clicked.connect(self.preview_convolution)
        btn_layout.addWidget(self.btn_preview)
        
        self.btn_apply = QPushButton("Aplicar")
        self.btn_apply.clicked.connect(self.apply_convolution)
        btn_layout.addWidget(self.btn_apply)
        
        self.btn_cancel = QPushButton("Cancelar")
        self.btn_cancel.clicked.connect(self.close)
        btn_layout.addWidget(self.btn_cancel)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

        # Inicializar tabela
        self.update_kernel_table(3)

    def update_kernel_table(self, size):
        """Atualiza a tabela para o novo tamanho do kernel."""
        self.kernel_size = size
        self.table_kernel.blockSignals(True)
        
        self.table_kernel.setRowCount(size)
        self.table_kernel.setColumnCount(size)
        
        # Inicializar com zeros
        self.kernel = np.zeros((size, size))
        
        for i in range(size):
            for j in range(size):
                item = QTableWidgetItem("0.0")
                self.table_kernel.setItem(i, j, item)
                
                # Se for o centro, colocar 1.0
                if i == size // 2 and j == size // 2:
                    item.setText("1.0")
                    self.kernel[i, j] = 1.0
        
        self.table_kernel.blockSignals(False)

    def update_kernel_from_table(self, row, col):
        """Atualiza o kernel com os valores da tabela."""
        try:
            value = float(self.table_kernel.item(row, col).text())
            self.kernel[row, col] = value
        except:
            pass

    def load_preset_mask(self, mask_name):
        """Carrega uma máscara pré-definida."""
        if mask_name == "Personalizada":
            return
            
        if mask_name in MASKS:
            mask = MASKS[mask_name]
            size = mask.shape[0]
            
            # Atualizar tamanho
            self.spin_size.setValue(size)
            
            # Preencher tabela
            self.table_kernel.blockSignals(True)
            for i in range(size):
                for j in range(size):
                    item = QTableWidgetItem(str(mask[i, j]))
                    self.table_kernel.setItem(i, j, item)
                    self.kernel[i, j] = mask[i, j]
            self.table_kernel.blockSignals(False)

    def preview_convolution(self):
        """Visualiza o resultado da convolução sem aplicar definitivamente."""
        try:
            if self.main_window.current_image is None:
                QMessageBox.warning(self, "Aviso", "Nenhuma imagem carregada.")
                return
            
            # Obter kernel da tabela
            for i in range(self.kernel_size):
                for j in range(self.kernel_size):
                    try:
                        self.kernel[i, j] = float(self.table_kernel.item(i, j).text())
                    except:
                        self.kernel[i, j] = 0.0
            
            # Aplicar convolução
            result = convolve(self.main_window.current_image, self.kernel)
            
            # Visualizar sem salvar
            from core.image_io import to_qimage
            qimg = to_qimage(result)
            self.main_window.update_current_image(result, replace=False)
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha na convolução:\n{e}")

    def apply_convolution(self):
        """Aplica a convolução definitivamente."""
        try:
            if self.main_window.current_image is None:
                QMessageBox.warning(self, "Aviso", "Nenhuma imagem carregada.")
                return
            
            # Obter kernel da tabela
            for i in range(self.kernel_size):
                for j in range(self.kernel_size):
                    try:
                        self.kernel[i, j] = float(self.table_kernel.item(i, j).text())
                    except:
                        self.kernel[i, j] = 0.0
            
            # Aplicar convolução
            result = convolve(self.main_window.current_image, self.kernel)
            
            # Aplicar definitivamente
            self.main_window.update_current_image(result)
            QMessageBox.information(self, "Sucesso", "Convolução aplicada com sucesso!")
            self.close()
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha na convolução:\n{e}")