# Predição de Valores das Ações da GOL (GOLL4SA) usando Regressão Linear

Este projeto visa desenvolver um modelo de predição para os valores das ações da empresa GOL (GOLL4SA) com base em séries históricas de dados do tipo CSV. As características consideradas no modelo são os valores de fechamento das seguintes variáveis:

1. Dólar em Reais (BRL=X)
2. Índice da bolsa de valores do Brasil (^BVSP)
3. Valor do Barril de Petróleo (Petroleo Tratado)
4. Valor do Ouro (Ouro Tratado)

A estrutura de predição será implementada, preferencialmente, utilizando regressão linear. A avaliação do modelo será realizada pela média dos erros e pela raiz quadrada do quadrado dos erros para uma amostra de teste de 25% da massa de dados.

## Instruções Importantes

Antes de iniciar o treinamento do modelo, é necessário realizar algumas etapas fundamentais:

1. **Ordenação e Sincronização de Datas:**
   - Garantir que os dados de Ouro e Petróleo tenham a mesma ordenação de datas que os demais arquivos.
   - Verificar e ajustar a janela de dados para que seja a mesma em todos os conjuntos.

2. **Tratamento de Dados:**
   - Tratar os dados de forma a lidar com valores ausentes. Isso pode ser feito preenchendo os dados faltantes com a média, mediana ou moda.
   - Certificar-se de que a quantidade de linhas nas amostras de treinamento/teste (X) é idêntica às amostras de respostas de treinamento/teste (y).

3. **Teste e Apresentação:**
   - Testar o código para garantir que seja executado sem bugs antes da apresentação.
   - Durante a apresentação, será realizada uma avaliação com uma amostra fornecida pelo professor, contendo valores do Dólar, Petróleo, Ouro e Índice da Bolsa.

## Pontos Extras

O projeto oferece a possibilidade de ganhar pontos extras através dos seguintes desafios:

1. Utilizar os arquivos DESAFIO das séries de Ouro e Petróleo e tratar os ajustes em código.
2. Implementar um filtro de intervalo de datas para dar carga nas amostras, permitindo treinar a máquina com dados específicos.
3. Utilizar outro modelo estatístico de treinamento e comparar a eficácia com o modelo de regressão linear.
4. Entregar o trabalho com 30 ou menos linhas de código, com um ponto extra se for menos de 25 linhas.
5. Comentar o código utilizando docstrings e gerar uma página em HTML com a documentação.

## Como Executar

1. Clone o repositório para a sua máquina.

2. Instale os requisitos necessários utilizando o arquivo requirements.txt

```sh
pip install -r requirements.txt 
```

3. Execute o código manualmente ou através do Makefile incluso
