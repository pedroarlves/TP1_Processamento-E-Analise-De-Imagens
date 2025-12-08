# Manual

## Pré-requisitos

- Clonar o repositório
- Ter python instalado na máquina
- Instalar as dependências indicadas abaixo

## Instale dependências
- PyQt6
- numpy
- matplotlib

`pip install PyQt6 numpy matplotlib`

## Execute

`python main.py` ou `python3 main.py`

## Link de imagens .raw para testar
https://links.uwaterloo.ca/Repository/RAW/

## Fluxo de utilização

1. Abrir aplicação.
2. Carregar imagem:
   - Menu Arquivo → Abrir ou arrastar para a área de trabalho (dependendo da implementação).
3. Adicionar blocos:
   - Na barra lateral, clique no bloco desejado (ex.: Brilho, Convolução, Histograma). O bloco aparece no Workspace.
4. Posicionar blocos:
   - Arraste os blocos na Workspace para organizar o fluxo.
5. Conectar blocos:
   - Clique e arraste do conector de saída de um bloco para o conector de entrada de outro. Linhas de conexão aparecem.
6. Parametrizar blocos:
   - Duplo-clique no bloco ou clique no botão de configuração no bloco para abrir o diálogo correspondente:
     - Brilho: use o slider para aumentar/diminuir; clique em Aplicar/OK para confirmar.
     - Convolução: insira valores do kernel, marque opção de normalizar, pré-visualize.
     - Diferença: selecione segunda imagem e método (absoluta/relativa).
7. Executar / visualizar:
   - Ao aplicar parâmetros, o bloco processa a imagem e envia para os próximos blocos conectados. O resultado é mostrado em uma visualização no bloco ou painel de saída.
8. Histogramas e comparação:
   - Adicione bloco Histograma para ver distribuição.
   - Use o bloco Diferença para comparar duas imagens e visualizar mapa de diferença.
9. Salvar resultado:
   - Menu Arquivo → Salvar ou botão de exportação no bloco de saída.