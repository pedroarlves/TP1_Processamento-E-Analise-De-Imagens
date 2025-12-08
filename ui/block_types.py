# ./ui/block_types.py
# Implementações específicas de blocos de processamento

from PyQt6.QtWidgets import QFileDialog, QInputDialog, QMessageBox
from ui.block_base import BlockItem
from core.image_io import read_raw, write_raw, auto_detect_raw_shape
from core.point_ops import adjust_brightness, threshold_image
from core.local_ops import convolve, MASKS
from core.diff import image_difference
from core.histogram import plot_histogram
import numpy as np

class ImageInputBlock(BlockItem):
    """Bloco para carregar imagem RAW."""
    
    def __init__(self, x=0, y=0):
        super().__init__("Carregar Imagem", x, y)
        self.file_path = None
        self.parameters = {'file_path': None, 'width': 256, 'height': 256}
    
    def create_ports(self):
        """Apenas porta de saída."""
        self.add_output_port("Imagem")
    
    def open_parameters_dialog(self):
        """Abre diálogo para selecionar arquivo."""
        from PyQt6.QtWidgets import QApplication
        
        file_path, _ = QFileDialog.getOpenFileName(None, "Selecionar imagem RAW", "", "RAW Files (*.raw)")
        if not file_path:
            return
        
        # Detectar dimensões
        w, h = auto_detect_raw_shape(file_path)
        
        if w is None:
            width, ok_w = QInputDialog.getInt(None, "Largura", "Digite a largura da imagem:", 256, 1, 4096)
            if not ok_w:
                return
            height, ok_h = QInputDialog.getInt(None, "Altura", "Digite a altura da imagem:", 256, 1, 4096)
            if not ok_h:
                return
        else:
            width, height = w, h
        
        self.parameters['file_path'] = file_path
        self.parameters['width'] = width
        self.parameters['height'] = height
        
        # Processar
        self.process()
    
    def process(self):
        """Carrega a imagem."""
        if self.parameters.get('file_path'):
            try:
                self.image_data = read_raw(
                    self.parameters['file_path'],
                    self.parameters['width'],
                    self.parameters['height']
                )
                self.update_thumbnail()
                self.propagate_output()
            except Exception as e:
                print(f"Erro ao carregar imagem: {e}")

class BrightnessBlock(BlockItem):
    """Bloco para ajustar brilho."""
    
    def __init__(self, x=0, y=0):
        super().__init__("Ajustar Brilho", x, y)
        self.parameters = {'brightness': 0}
    
    def create_ports(self):
        self.add_input_port("Entrada")
        self.add_output_port("Saída")
    
    def open_parameters_dialog(self):
        """Abre diálogo para ajustar valor do brilho."""
        value, ok = QInputDialog.getInt(
            None, "Ajustar Brilho", 
            "Valor de brilho (-255 a +255):", 
            self.parameters.get('brightness', 0), 
            -255, 255
        )
        if ok:
            self.parameters['brightness'] = value
            self.process()
    
    def process(self):
        """Aplica ajuste de brilho."""
        input_img = self.get_input_data(0)
        if input_img is not None:
            brightness = self.parameters.get('brightness', 0)
            self.image_data = adjust_brightness(input_img, brightness)
            self.update_thumbnail()
            self.propagate_output()

class ConvolutionBlock(BlockItem):
    """Bloco para aplicar convolução."""
    
    def __init__(self, x=0, y=0):
        super().__init__("Convolução", x, y)
        self.parameters = {'mask_name': 'Média 3x3'}
    
    def create_ports(self):
        self.add_input_port("Entrada")
        self.add_output_port("Saída")
    
    def open_parameters_dialog(self):
        """Abre diálogo para selecionar máscara."""
        from PyQt6.QtWidgets import QInputDialog
        
        mask_names = list(MASKS.keys())
        mask_name, ok = QInputDialog.getItem(
            None, "Convolução", 
            "Selecione a máscara:", 
            mask_names, 
            mask_names.index(self.parameters.get('mask_name', 'Média 3x3')), 
            False
        )
        if ok:
            self.parameters['mask_name'] = mask_name
            self.process()
    
    def process(self):
        """Aplica convolução."""
        input_img = self.get_input_data(0)
        if input_img is not None:
            mask_name = self.parameters.get('mask_name', 'Média 3x3')
            kernel = MASKS[mask_name]
            self.image_data = convolve(input_img, kernel)
            self.update_thumbnail()
            self.propagate_output()

class ThresholdBlock(BlockItem):
    """Bloco para limiarização."""
    
    def __init__(self, x=0, y=0):
        super().__init__("Limiarização", x, y)
        self.parameters = {'threshold': 128}
    
    def create_ports(self):
        self.add_input_port("Entrada")
        self.add_output_port("Saída")
    
    def open_parameters_dialog(self):
        """Abre diálogo para ajustar limiar."""
        value, ok = QInputDialog.getInt(
            None, "Limiarização", 
            "Valor do limiar (0-255):", 
            self.parameters.get('threshold', 128), 
            0, 255
        )
        if ok:
            self.parameters['threshold'] = value
            self.process()
    
    def process(self):
        """Aplica limiarização."""
        input_img = self.get_input_data(0)
        if input_img is not None:
            threshold = self.parameters.get('threshold', 128)
            self.image_data = threshold_image(input_img, threshold)
            self.update_thumbnail()
            self.propagate_output()

class DiffBlock(BlockItem):
    """Bloco para diferença entre duas imagens."""
    
    def __init__(self, x=0, y=0):
        super().__init__("Diferença", x, y)
    
    def create_ports(self):
        self.add_input_port("Imagem A")
        self.add_input_port("Imagem B")
        self.add_output_port("Saída")
    
    def process(self):
        """Calcula diferença entre duas imagens."""
        img1 = self.get_input_data(0)
        img2 = self.get_input_data(1)
        
        if img1 is not None and img2 is not None:
            if img1.shape == img2.shape:
                self.image_data = image_difference(img1, img2)
                self.update_thumbnail()
                self.propagate_output()

class HistogramBlock(BlockItem):
    """Bloco para exibir histograma."""
    
    def __init__(self, x=0, y=0):
        super().__init__("Histograma", x, y)
    
    def create_ports(self):
        self.add_input_port("Entrada")
        self.add_output_port("Saída")  # Passa a imagem adiante
    
    def open_parameters_dialog(self):
        """Exibe o histograma."""
        if self.image_data is not None:
            plot_histogram(self.image_data)
    
    def process(self):
        """Passa a imagem adiante sem modificá-la."""
        input_img = self.get_input_data(0)
        if input_img is not None:
            self.image_data = input_img.copy()
            self.update_thumbnail()
            self.propagate_output()

class ImageOutputBlock(BlockItem):
    """Bloco para exibir/salvar imagem."""
    
    def __init__(self, x=0, y=0):
        super().__init__("Exibir/Salvar", x, y)
    
    def create_ports(self):
        self.add_input_port("Entrada")
    
    def open_parameters_dialog(self):
        """Oferece opção de salvar a imagem."""
        if self.image_data is None:
            QMessageBox.warning(None, "Aviso", "Nenhuma imagem para salvar.")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(None, "Salvar imagem RAW", "", "RAW Files (*.raw)")
        if file_path:
            try:
                write_raw(self.image_data, file_path)
                QMessageBox.information(None, "Sucesso", f"Imagem salva em:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(None, "Erro", f"Falha ao salvar:\n{e}")
    
    def process(self):
        """Recebe a imagem processada."""
        input_img = self.get_input_data(0)
        if input_img is not None:
            self.image_data = input_img.copy()
            self.update_thumbnail()
            # Não propaga (bloco final)

# Mapeamento de tipos de blocos
BLOCK_TYPES = {
    'Carregar Imagem': ImageInputBlock,
    'Ajustar Brilho': BrightnessBlock,
    'Convolução': ConvolutionBlock,
    'Limiarização': ThresholdBlock,
    'Diferença': DiffBlock,
    'Histograma': HistogramBlock,
    'Exibir/Salvar': ImageOutputBlock
}