from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QColor, QPen
from ui.connectors import Port, ConnectionLine
import json

class Workspace(QGraphicsView):
    """Área principal onde blocos visuais são criados e conectados."""
    
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 3000, 2000)
        self.setScene(self.scene)
        self.setRenderHints(self.renderHints())
        self.setMinimumSize(800, 600)
        
        # Configuração de viewport
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        
        # Background
        self.setBackgroundBrush(QColor(45, 45, 50))
        
        # Estado de conexão
        self.connecting = False
        self.temp_connection = None
        self.start_port = None
        
        # Lista de blocos
        self.blocks = []
    
    def add_block(self, block):
        """Adiciona um bloco ao workspace."""
        self.scene.addItem(block)
        self.blocks.append(block)
    
    def remove_block(self, block):
        """Remove um bloco e suas conexões."""
        # Remover todas as conexões
        all_ports = block.input_ports + block.output_ports
        for port in all_ports:
            for connection in list(port.connections):
                connection.remove()
        
        # Remover bloco da cena e lista
        self.scene.removeItem(block)
        if block in self.blocks:
            self.blocks.remove(block)
    
    def mousePressEvent(self, event):
        """Captura clique em portas para criar conexões."""
        item = self.itemAt(event.pos())
        
        # Verifica se clicou em uma porta
        if isinstance(item, Port):
            if not self.connecting:
                # Inicia conexão apenas de portas de saída
                if item.port_type == 'output':
                    self.connecting = True
                    self.start_port = item
                    self.temp_connection = ConnectionLine(self.start_port)
                    self.scene.addItem(self.temp_connection)
            else:
                # Finaliza conexão em porta de entrada
                if item.port_type == 'input' and item != self.start_port:
                    # Verifica se já existe conexão nesta porta de entrada
                    has_connection = False
                    for conn in item.connections:
                        if conn.end_port == item:
                            has_connection = True
                            break
                    
                    if not has_connection:
                        # Finalizar conexão
                        self.temp_connection.finalize(item)
                        
                        # Processar o bloco destino automaticamente
                        dest_block = item.parent_block
                        dest_block.process()
                    else:
                        # Remover conexão temporária
                        self.scene.removeItem(self.temp_connection)
                    
                    self.connecting = False
                    self.temp_connection = None
                    self.start_port = None
                else:
                    # Cancelar conexão
                    if self.temp_connection:
                        self.scene.removeItem(self.temp_connection)
                    self.connecting = False
                    self.temp_connection = None
                    self.start_port = None
        else:
            # Cancelar conexão se clicar em outro lugar
            if self.connecting:
                if self.temp_connection:
                    self.scene.removeItem(self.temp_connection)
                self.connecting = False
                self.temp_connection = None
                self.start_port = None
        
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        """Atualiza linha temporária de conexão."""
        if self.connecting and self.temp_connection:
            # Atualizar ponto final da linha temporária
            scene_pos = self.mapToScene(event.pos())
            self.temp_connection.set_end_point(scene_pos)
        
        super().mouseMoveEvent(event)
    
    def keyPressEvent(self, event):
        """Deleta blocos selecionados com a tecla Delete."""
        if event.key() == Qt.Key.Key_Delete:
            for item in self.scene.selectedItems():
                from ui.block_base import BlockItem
                if isinstance(item, BlockItem):
                    self.remove_block(item)
        
        super().keyPressEvent(event)
    
    def clear_workspace(self):
        """Limpa todos os blocos do workspace."""
        for block in list(self.blocks):
            self.remove_block(block)
    
    def save_workflow(self, filepath):
        """Salva o fluxo de trabalho em arquivo JSON."""
        workflow_data = {
            'blocks': [],
            'connections': []
        }
        
        # Mapear blocos para IDs
        block_to_id = {}
        for idx, block in enumerate(self.blocks):
            block_id = f"block_{idx}"
            block_to_id[block] = block_id
            
            workflow_data['blocks'].append({
                'id': block_id,
                'type': block.block_type,
                'x': block.x(),
                'y': block.y(),
                'parameters': block.parameters
            })
        
        # Salvar conexões
        saved_connections = set()
        for block in self.blocks:
            for output_port in block.output_ports:
                for connection in output_port.connections:
                    if connection.end_port:
                        conn_id = id(connection)
                        if conn_id not in saved_connections:
                            saved_connections.add(conn_id)
                            
                            start_block_id = block_to_id.get(connection.start_port.parent_block)
                            end_block_id = block_to_id.get(connection.end_port.parent_block)
                            
                            workflow_data['connections'].append({
                                'start_block': start_block_id,
                                'start_port': connection.start_port.index,
                                'end_block': end_block_id,
                                'end_port': connection.end_port.index
                            })
        
        # Salvar em arquivo
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(workflow_data, f, indent=2, ensure_ascii=False)
    
    def load_workflow(self, filepath):
        """Carrega fluxo de trabalho de arquivo JSON."""
        from ui.block_types import BLOCK_TYPES
        
        # Limpar workspace
        self.clear_workspace()
        
        # Carregar dados
        with open(filepath, 'r', encoding='utf-8') as f:
            workflow_data = json.load(f)
        
        # Mapear IDs para blocos
        id_to_block = {}
        
        # Criar blocos
        for block_data in workflow_data['blocks']:
            block_type = block_data['type']
            if block_type in BLOCK_TYPES:
                block_class = BLOCK_TYPES[block_type]
                block = block_class(block_data['x'], block_data['y'])
                block.parameters = block_data.get('parameters', {})
                
                self.add_block(block)
                id_to_block[block_data['id']] = block
        
        # Criar conexões
        for conn_data in workflow_data['connections']:
            start_block = id_to_block.get(conn_data['start_block'])
            end_block = id_to_block.get(conn_data['end_block'])
            
            if start_block and end_block:
                start_port = start_block.output_ports[conn_data['start_port']]
                end_port = end_block.input_ports[conn_data['end_port']]
                
                connection = ConnectionLine(start_port, end_port)
                self.scene.addItem(connection)
    
    def show_image(self, qimage):
        """Exibe uma imagem na cena (compatibilidade com código antigo)."""
        from PyQt6.QtWidgets import QGraphicsPixmapItem
        from PyQt6.QtGui import QPixmap

        pixmap = QPixmap.fromImage(qimage)
        item = QGraphicsPixmapItem(pixmap)
        self.scene.clear()
        self.blocks.clear()
        self.scene.addItem(item)
        self.fitInView(item, Qt.AspectRatioMode.KeepAspectRatio)
