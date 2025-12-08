from PyQt6.QtWidgets import (QMainWindow, QFileDialog, QInputDialog, QMessageBox,
                             QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QScrollArea, QSplitter)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
from core.image_io import read_raw, write_raw, to_qimage, auto_detect_raw_shape
from ui.workspace import Workspace
from ui.block_types import BLOCK_TYPES

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PSE-Image - Editor Visual de Processamento")
        self.setGeometry(100, 100, 1200, 800)
        
        # Layout principal com splitter
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        
        # Splitter para dividir sidebar e workspace
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Sidebar com paleta de blocos
        self.sidebar = self._create_sidebar()
        splitter.addWidget(self.sidebar)
        
        # Workspace visual
        self.workspace = Workspace()
        splitter.addWidget(self.workspace)
        
        # Proporção inicial (20% sidebar, 80% workspace)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 4)
        
        main_layout.addWidget(splitter)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Guarda imagem numpy atual (estado global - para compatibilidade)
        self.current_image = None  
        self.image_history = []

        self._create_menu()

    # ---------------------------------------------------------------------
    # SIDEBAR COM PALETA DE BLOCOS
    # ---------------------------------------------------------------------
    def _create_sidebar(self):
        """Cria a barra lateral com paleta de blocos."""
        sidebar_widget = QWidget()
        sidebar_layout = QVBoxLayout()
        
        # Título
        title_label = QLabel("Paleta de Blocos")
        title_label.setStyleSheet("font-size: 14px; font-weight: bold; padding: 10px;")
        sidebar_layout.addWidget(title_label)
        
        # Scroll area para os botões de blocos
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setMinimumWidth(200)
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout()
        
        # Criar botão para cada tipo de bloco
        for block_name in BLOCK_TYPES.keys():
            btn = QPushButton(block_name)
            btn.clicked.connect(lambda checked, name=block_name: self.add_block_to_workspace(name))
            btn.setStyleSheet("padding: 8px; text-align: left;")
            scroll_layout.addWidget(btn)
        
        scroll_layout.addStretch()
        scroll_content.setLayout(scroll_layout)
        scroll.setWidget(scroll_content)
        
        sidebar_layout.addWidget(scroll)
        
        # Botões de ação
        action_label = QLabel("Ações")
        action_label.setStyleSheet("font-size: 12px; font-weight: bold; padding: 10px;")
        sidebar_layout.addWidget(action_label)
        
        clear_btn = QPushButton("Limpar Workspace")
        clear_btn.clicked.connect(self.clear_workspace)
        sidebar_layout.addWidget(clear_btn)
        
        save_workflow_btn = QPushButton("Salvar Fluxo")
        save_workflow_btn.clicked.connect(self.save_workflow)
        sidebar_layout.addWidget(save_workflow_btn)
        
        load_workflow_btn = QPushButton("Carregar Fluxo")
        load_workflow_btn.clicked.connect(self.load_workflow)
        sidebar_layout.addWidget(load_workflow_btn)
        
        sidebar_widget.setLayout(sidebar_layout)
        sidebar_widget.setMaximumWidth(250)
        
        return sidebar_widget
    
    # ---------------------------------------------------------------------
    # FUNÇÕES DE BLOCOS
    # ---------------------------------------------------------------------
    def add_block_to_workspace(self, block_name):
        """Adiciona um bloco ao workspace."""
        if block_name in BLOCK_TYPES:
            block_class = BLOCK_TYPES[block_name]
            # Posicionar no centro visível do viewport
            center = self.workspace.mapToScene(self.workspace.viewport().rect().center())
            block = block_class(center.x() - 90, center.y() - 100)
            self.workspace.add_block(block)
    
    def clear_workspace(self):
        """Limpa todos os blocos do workspace."""
        reply = QMessageBox.question(
            self, "Confirmar", 
            "Deseja realmente limpar todo o workspace?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.workspace.clear_workspace()
    
    def save_workflow(self):
        """Salva o fluxo de trabalho atual."""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Salvar Fluxo de Trabalho", "", "JSON Files (*.json)"
        )
        if file_path:
            try:
                self.workspace.save_workflow(file_path)
                QMessageBox.information(self, "Sucesso", f"Fluxo salvo em:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Falha ao salvar fluxo:\n{e}")
    
    def load_workflow(self):
        """Carrega um fluxo de trabalho salvo."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Carregar Fluxo de Trabalho", "", "JSON Files (*.json)"
        )
        if file_path:
            try:
                self.workspace.load_workflow(file_path)
                QMessageBox.information(self, "Sucesso", "Fluxo carregado com sucesso!")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Falha ao carregar fluxo:\n{e}")
    
    # ---------------------------------------------------------------------
    # MENU DE AÇÕES
    # ---------------------------------------------------------------------
    def _create_menu(self):
        menubar = self.menuBar()

        # ---------------- Arquivo ----------------
        file_menu = menubar.addMenu("Arquivo")
        
        save_workflow_action = QAction("Salvar Fluxo", self)
        save_workflow_action.triggered.connect(self.save_workflow)
        file_menu.addAction(save_workflow_action)
        
        load_workflow_action = QAction("Carregar Fluxo", self)
        load_workflow_action.triggered.connect(self.load_workflow)
        file_menu.addAction(load_workflow_action)
        
        file_menu.addSeparator()
        
        clear_action = QAction("Limpar Workspace", self)
        clear_action.triggered.connect(self.clear_workspace)
        file_menu.addAction(clear_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Sair", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # ---------------- Ajuda ----------------
        help_menu = menubar.addMenu("Ajuda")
        
        instructions_action = QAction("Como Usar", self)
        instructions_action.triggered.connect(self.show_instructions)
        help_menu.addAction(instructions_action)
    
    # ---------------------------------------------------------------------
    # AJUDA E INSTRUÇÕES
    # ---------------------------------------------------------------------
    def show_instructions(self):
        """Exibe instruções de uso do editor."""
        instructions = """
        <h2>Como Usar o Editor Visual de Processamento de Imagens</h2>
        
        <h3>1. Adicionar Blocos</h3>
        <p>Clique nos botões da barra lateral esquerda para adicionar blocos ao workspace.</p>
        
        <h3>2. Conectar Blocos</h3>
        <p>• Clique em uma porta de <b>saída</b> (laranja, à direita do bloco)</p>
        <p>• Arraste até uma porta de <b>entrada</b> (azul, à esquerda do bloco)</p>
        <p>• O processamento ocorre <b>automaticamente</b> ao conectar</p>
        
        <h3>3. Configurar Parâmetros</h3>
        <p>Dê <b>duplo clique</b> em um bloco para configurar seus parâmetros.</p>
        
        <h3>4. Visualizar Resultados</h3>
        <p>Cada bloco mostra uma miniatura da imagem processada.</p>
        <p>Use o bloco "Exibir/Salvar" para salvar o resultado final.</p>
        <p>Use o bloco "Histograma" e dê duplo clique para ver o histograma.</p>
        
        <h3>5. Fluxo de Trabalho</h3>
        <p>• <b>Salvar Fluxo:</b> Salva a estrutura de blocos e conexões</p>
        <p>• <b>Carregar Fluxo:</b> Restaura um fluxo salvo</p>
        <p>• <b>Limpar Workspace:</b> Remove todos os blocos</p>
        
        <h3>6. Atalhos</h3>
        <p>• <b>Delete:</b> Remove blocos selecionados</p>
        <p>• <b>Duplo clique:</b> Abre parâmetros do bloco</p>
        
        <h3>Exemplo de Fluxo Básico:</h3>
        <p>1. Carregar Imagem → 2. Ajustar Brilho → 3. Convolução → 4. Exibir/Salvar</p>
        """
        
        msg = QMessageBox(self)
        msg.setWindowTitle("Instruções de Uso")
        msg.setTextFormat(Qt.TextFormat.RichText)
        msg.setText(instructions)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()