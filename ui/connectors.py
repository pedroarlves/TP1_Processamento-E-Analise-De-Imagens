# ./ui/connectors.py
# Sistema de portas e conexões entre blocos

from PyQt6.QtWidgets import QGraphicsEllipseItem, QGraphicsPathItem
from PyQt6.QtCore import Qt, QPointF, pyqtSignal, QObject
from PyQt6.QtGui import QPen, QColor, QBrush, QPainterPath

class Port(QGraphicsEllipseItem):
    """Porta de conexão (entrada ou saída) de um bloco."""
    
    def __init__(self, parent_block, port_type, port_name, index=0):
        # Tamanho e posição da porta
        size = 12
        super().__init__(-size/2, -size/2, size, size)
        
        self.parent_block = parent_block
        self.port_type = port_type  # 'input' ou 'output'
        self.port_name = port_name
        self.index = index
        self.connections = []  # Lista de ConnectionLine conectadas
        
        # Estilo visual
        if port_type == 'input':
            self.setBrush(QBrush(QColor(100, 150, 255)))
        else:
            self.setBrush(QBrush(QColor(255, 150, 100)))
        
        self.setPen(QPen(QColor(255, 255, 255), 2))
        self.setFlag(QGraphicsEllipseItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.setParentItem(parent_block)
        self.setAcceptHoverEvents(True)
        
    def hoverEnterEvent(self, event):
        """Destaca a porta ao passar o mouse."""
        self.setBrush(QBrush(QColor(255, 255, 100)))
        super().hoverEnterEvent(event)
    
    def hoverLeaveEvent(self, event):
        """Restaura cor original."""
        if self.port_type == 'input':
            self.setBrush(QBrush(QColor(100, 150, 255)))
        else:
            self.setBrush(QBrush(QColor(255, 150, 100)))
        super().hoverLeaveEvent(event)
    
    def get_center(self):
        """Retorna a posição central da porta em coordenadas de cena."""
        return self.scenePos()
    
    def add_connection(self, connection):
        """Adiciona uma conexão a esta porta."""
        if connection not in self.connections:
            self.connections.append(connection)
    
    def remove_connection(self, connection):
        """Remove uma conexão desta porta."""
        if connection in self.connections:
            self.connections.remove(connection)

class ConnectionLine(QGraphicsPathItem):
    """Linha de conexão entre duas portas."""
    
    def __init__(self, start_port, end_port=None):
        super().__init__()
        
        self.start_port = start_port
        self.end_port = end_port
        self.end_point = None  # Para conexões temporárias
        
        # Estilo da linha
        pen = QPen(QColor(200, 200, 200), 3)
        pen.setStyle(Qt.PenStyle.SolidLine)
        self.setPen(pen)
        
        # Adiciona aos conectores das portas
        self.start_port.add_connection(self)
        if self.end_port:
            self.end_port.add_connection(self)
        
        self.update_path()
        self.setZValue(-1)  # Atrás dos blocos
    
    def update_path(self):
        """Atualiza o caminho da linha de conexão."""
        path = QPainterPath()
        
        start_pos = self.start_port.get_center()
        
        if self.end_port:
            end_pos = self.end_port.get_center()
        elif self.end_point:
            end_pos = self.end_point
        else:
            return
        
        # Criar curva bezier para conexão suave
        path.moveTo(start_pos)
        
        # Pontos de controle para curva
        dx = end_pos.x() - start_pos.x()
        ctrl1 = QPointF(start_pos.x() + dx * 0.5, start_pos.y())
        ctrl2 = QPointF(end_pos.x() - dx * 0.5, end_pos.y())
        
        path.cubicTo(ctrl1, ctrl2, end_pos)
        
        self.setPath(path)
    
    def set_end_point(self, point):
        """Define o ponto final temporário (durante criação da conexão)."""
        self.end_point = point
        self.update_path()
    
    def finalize(self, end_port):
        """Finaliza a conexão com uma porta de destino."""
        self.end_port = end_port
        self.end_point = None
        self.end_port.add_connection(self)
        self.update_path()
    
    def remove(self):
        """Remove a conexão de ambas as portas."""
        self.start_port.remove_connection(self)
        if self.end_port:
            self.end_port.remove_connection(self)
        
        # Remove da cena
        if self.scene():
            self.scene().removeItem(self)