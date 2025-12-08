# TP1_Processamento-E-Analise-De-Imagens

## 1. Objetivo da aplicação 

Permitir que o usuário monte fluxos de processamento visualmente conectando blocos (p.ex. Brilho → Convolução → Histograma), parametrizando cada bloco via diálogos e visualizando resultados em tempo real.

## 2. Estrutura Geral do Projeto

* PSE-Image/
* │
* ├── main.py                   # Ponto de entrada
* ├── ui/                       # Interface gráfica (QMainWindow, blocos)
* │   ├── workspace.py          # Área de montagem dos blocos
* │   ├── block_base.py         # Classe base para blocos
* │   ├── block_types.py        # Implementações específicas dos blocos
* │   ├── connectors.py         # Linhas/conexões entre blocos
* │   ├── main_window.py        # Janela principal (menu, toolbar, integração)
* │   ├── dialog_brilho.py      # Diálogo de ajuste de brilho (QSlider)
* │   ├── dialog_diff.py        # Diálogo para diferença entre imagens
* │   └── dialog_convolution.py # Diálogo de convolução personalizada
* │
* ├── core/                     # Processamento de imagem
* │   ├── image_io.py           # Leitura e gravação de arquivos RAW
* │   ├── point_ops.py          # Operações pontuais (brilho, threshold, etc)
* │   ├── local_ops.py          # Operações locais (convolução, máscaras)
* │   ├── histogram.py          # Cálculo e exibição de histogramas
* │   └── diff.py               # Diferença entre duas imagens
* │ 
* ├── assets/                   # Imagens de teste
* └── manual/                   # Manual do usuário e vídeo

## 3. Implementação

Use QGraphicsScene + QGraphicsView:

* Cada bloco é um QGraphicsRectItem com:

    * Nome (ex.: “Brilho”, “Histograma”)

    * Entradas e saídas conectáveis (círculos laterais)

    * Botão de parametrização (abre um QDialog)

**Classes principais:**

* WorkspaceView(QGraphicsView): área onde o usuário manipula os blocos.

* BlockItem(QGraphicsItem): bloco visual.

* ConnectorLine(QGraphicsPathItem): conexão entre blocos.

## 4. Utilização

Conferir manual disponível em `manual/manual.md`.