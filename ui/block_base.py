# ./ui/block_base.py
# Classe base para blocos de processamento visual

from PyQt6.QtWidgets import (QGraphicsRectItem, QGraphicsTextItem, 
                             QGraphicsPixmapItem, QGraphicsItem)
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QColor, QPen, QBrush, QPixmap, QPainter
from ui.connectors import Port
import numpy as np

class BlockItem(QGraphicsRectItem):
    """Bloco visual base para processamento de imagens."""
    
    def __init__(self, block_type, x=0, y=0):
        # Dimensões do bloco
        self.width = 180
        self.height = 200
        
        super().__init__(0, 0, self.width, self.height)
        
        self.block_type = block_type
        self.block_id = id(self)  # ID único
        self.image_data = None  # Imagem processada (numpy array)
        self.parameters = {}  # Parâmetros configuráveis
        
        # Posição inicial
        self.setPos(x, y)
        
        # Estilo visual
        self.setBrush(QBrush(QColor(60, 60, 70)))
        self.setPen(QPen(QColor(100, 100, 110), 2))
        
        # Flags
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        
        # Título do bloco
        self.title = QGraphicsTextItem(self)
        self.title.setPlainText(block_type)
        self.title.setDefaultTextColor(QColor(255, 255, 255))
        self.title.setPos(10, 5)
        
        # Área para miniatura da imagem
        self.thumbnail = QGraphicsPixmapItem(self)
        self.thumbnail.setPos(10, 30)
        self.update_thumbnail()
        
        # Portas de entrada e saída
        self.input_ports = []
        self.output_ports = []
        
        self.create_ports()
    
    def create_ports(self):
        """Cria as portas de entrada e saída. Sobrescrever em subclasses."""
        pass
    
    def add_input_port(self, name, index=None):
        """Adiciona uma porta de entrada."""
        if index is None:
            index = len(self.input_ports)
        
        port = Port(self, 'input', name, index)
        # Posiciona à esquerda
        y_pos = 80 + index * 40
        port.setPos(0, y_pos)
        self.input_ports.append(port)
        return port
    
    def add_output_port(self, name, index=None):
        """Adiciona uma porta de saída."""
        if index is None:
            index = len(self.output_ports)
        
        port = Port(self, 'output', name, index)
        # Posiciona à direita
        y_pos = 80 + index * 40
        port.setPos(self.width, y_pos)
        self.output_ports.append(port)
        return port
    
    def update_thumbnail(self):
        """Atualiza a miniatura da imagem processada."""
        if self.image_data is None:
            # Imagem placeholder
            pixmap = QPixmap(160, 120)
            pixmap.fill(QColor(40, 40, 50))
        else:
            # Converter numpy array para QPixmap
            pixmap = self.numpy_to_pixmap(self.image_data)
            # Redimensionar para miniatura
            pixmap = pixmap.scaled(160, 120, Qt.AspectRatioMode.KeepAspectRatio,
                                  Qt.TransformationMode.SmoothTransformation)
        
        self.thumbnail.setPixmap(pixmap)
    
    def numpy_to_pixmap(self, image):
        """Converte numpy array para QPixmap."""
        from core.image_io import to_qimage
        qimg = to_qimage(image)
        return QPixmap.fromImage(qimg)
    
    def process(self):
        """Processa os dados de entrada. Sobrescrever em subclasses."""
        pass
    
    def get_input_data(self, port_index=0):
        """Obtém dados da porta de entrada especificada."""
        if port_index >= len(self.input_ports):
            return None
        
        port = self.input_ports[port_index]
        
        # Procura conexão conectada a esta porta
        for connection in port.connections:
            if connection.end_port == port:
                # Obtém dados do bloco de origem
                source_block = connection.start_port.parent_block
                return source_block.image_data
        
        return None
    
    def propagate_output(self):
        """Propaga os dados processados para blocos conectados."""
        for output_port in self.output_ports:
            for connection in output_port.connections:
                if connection.start_port == output_port and connection.end_port:
                    # Bloco de destino
                    dest_block = connection.end_port.parent_block
                    # Processa o bloco de destino
                    dest_block.process()
    
    def itemChange(self, change, value):
        """Atualiza conexões quando o bloco é movido."""
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            # Atualiza todas as conexões
            for port in self.input_ports + self.output_ports:
                for connection in port.connections:
                    connection.update_path()
        
        return super().itemChange(change, value)
    
    def paint(self, painter, option, widget):
        """Desenha o bloco com destaque se selecionado."""
        if self.isSelected():
            self.setPen(QPen(QColor(255, 200, 100), 3))
        else:
            self.setPen(QPen(QColor(100, 100, 110), 2))
        
        super().paint(painter, option, widget)
    
    def mouseDoubleClickEvent(self, event):
        """Abre diálogo de parâmetros ao dar duplo clique."""
        self.open_parameters_dialog()
        super().mouseDoubleClickEvent(event)
    
    def open_parameters_dialog(self):
        """Abre diálogo de configuração. Sobrescrever em subclasses."""
        pass
    
    def to_dict(self):
        """Serializa o bloco para dicionário (para salvar)."""
        return {
            'block_type': self.block_type,
            'block_id': self.block_id,
            'x': self.x(),
            'y': self.y(),
            'parameters': self.parameters
        }
    
    def from_dict(self, data):
        """Carrega dados do dicionário."""
        self.setPos(data['x'], data['y'])
        self.parameters = data.get('parameters', {})