# TP1_Processamento-E-Analise-De-Imagens

## 🧩 1. Estrutura Geral do Projeto


* PSE-Image/
* │
* ├── main.py                # Ponto de entrada
* ├── ui/                    # Interface gráfica (QMainWindow, blocos)
* │   ├── workspace.py       # Área de montagem dos blocos
* │   ├── block_base.py      # Classe base para blocos
* │   ├── block_types.py     # Implementações específicas dos blocos
* │   └── connectors.py      # Gerencia conexões visuais entre blocos
* │
* ├── core/                  # Processamento de imagem
* │   ├── image_io.py        # Leitura e gravação de arquivos RAW
* │   ├── point_ops.py       # Operações pontuais (brilho, threshold, etc)
* │   ├── local_ops.py       # Operações locais (convolução, máscaras)
* │   ├── histogram.py       # Cálculo e exibição de histogramas
* │   └── diff.py            # Diferença entre duas imagens
* │
* ├── assets/                # Imagens de teste
* └── manual/                # Manual do usuário e vídeo