# TP1_Processamento-E-Analise-De-Imagens
## Alunos
* Pedro Rodrigues Alves
* Yasmin Cassemiro Viegas
* Bárbara Luiza Freitas Carmo
* Gabriel Luna dos Anjos
* Daniel Lucas Murta

## Professor Orientador

* Carolina Stephanie Jerônimo de Almeida

## Video Tutorial

https://youtu.be/igLr-NViXqc

## 1. Objetivo da aplicação 

Permitir que o usuário monte fluxos de processamento visualmente conectando blocos (p.ex. Brilho → Convolução → Histograma), parametrizando cada bloco via diálogos e visualizando resultados em tempo real.

## 2. Estrutura Geral do Projeto

```text
| PSE-Image/
├── main.py                     # Ponto de entrada
├── ui/                         # Interface gráfica (Qt)
│   ├── workspace.py            # Área de montagem dos blocos
│   ├── block_base.py           # Classe base para blocos
│   ├── block_types.py          # Blocos específicos
│   ├── connectors.py           # Conexões entre blocos
│   ├── main_window.py          # Janela principal
│   ├── dialog_brilho.py        # Ajuste de brilho
│   ├── dialog_diff.py          # Diferença entre imagens
│   └── dialog_convolution.py   # Convolução personalizada
│
├── core/                       # Processamento de imagem
│   ├── image_io.py             # Leitura/gravação RAW
│   ├── point_ops.py            # Operações pontuais
│   ├── local_ops.py            # Convoluções e máscaras
│   ├── histogram.py            # Histograma
│   └── diff.py                 # Diferença entre imagens
│
├── assets/                     # Imagens de teste
└── manual/                     # Manual e vídeos
```

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

### 3.1 Funções de cada arquivo Core

#### 3.1.1 image_io.py

**read_raw**: Lê bytes e converte em matriz grayscale
- Abre o arquivo RAW em modo binário
- Lê todos os bytes como um vetor NumPy uint8
- Redimensiona para uma matriz 2D

**write_raw**: Salva matriz como arquivo RAW puro
- Garante que está em formato uint8
- Usa .tofile() para gravar diretamente os bytes

**to_qimage**: Converte uma matriz NumPy para um objeto QImage do PyQt6

**auto_detect_raw_shape**: Tenta descobrir width/height baseado no tamanho do arquivo

#### 3.1.2 point_ops.py

Ajuste de brilho: Ajusta o brilho da imagem somando um valor constante a todos os pixels.

Pontos importantes:
- valores negativos viram 0
- valores acima de 255 viram 255
- mantém a imagem válida para 8 bits

Threshold: Transforma a imagem em preto e branco binário, baseado em um limiar thresh.

- Separa objetos do fundo
- Se o pixel for maior ou igual ao limiar → vira 255 (branco)
- Caso contrário → vira 0 (preto)

#### 3.1.3 local_ops.py

Onde são implementadas as funções de convolução. Para cada pixel:

1. Extrai a vizinhança do mesmo tamanho do kernel (ex.: 3×3)
2. Multiplica elemento a elemento → region * kernel
3. Soma tudo → np.sum()
4. Armazena no pixel correspondente da imagem filtrada

#### 3.1.4 histogram.py

Recebe uma imagem grayscale (img como array NumPy 2D) e plota o histograma de suas intensidades. A função responde:

Quantos pixels têm intensidade 0?
...
Quantos têm intensidade 255?

O resultado é um gráfico com picos e vales que revela:
- se a imagem está clara ou escura
- se tem bom contraste
- se há regiões homogêneas
- se está superexposta ou subexposta
- se existe informação suficiente para segmentações limiarizadas

#### 3.1.5 diff.py

Calcula a diferença absoluta pixel a pixel entre duas imagens em escala de cinza:
- Converte as imagens para int (evitar bugs)
- Subtrai pixel por pixel
- Tira valor absoluto
- Converte de volta para uint8

## 4. Utilização

Conferir manual disponível em `manual/manual.md`.
