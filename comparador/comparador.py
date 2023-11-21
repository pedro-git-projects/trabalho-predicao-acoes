import matplotlib.pyplot as plt
from preditor.preditor import Preditor


class Comparador:
    """
    Classe responsável por comparar os resultados de diferentes modelos de predição.

    Attributes:
    - modelos (dict): Um dicionário para armazenar modelos de predição associados aos seus nomes.

    Methods:
    - __init__(): Inicializa a instância da classe com um dicionário vazio para armazenar modelos.
    - adicionar_modelo(nome_modelo, preditor): Adiciona um modelo de predição ao dicionário de modelos.
    - plotar_resultados(): Gera gráficos de dispersão para comparar os resultados dos diferentes modelos.
    """  # noqa: E501

    def __init__(self):
        """
        Inicializa a instância da classe Comparador.

        O atributo 'modelos' é um dicionário que será usado para armazenar modelos de predição.
        """  # noqa: E501

        self.modelos = {}

    def adicionar_modelo(self, nome_modelo: str, preditor: Preditor):
        """
        Adiciona um modelo de predição ao dicionário de modelos.

        Args:
        - nome_modelo (str): O nome do modelo a ser adicionado.
        - preditor (Preditor): Uma instância da classe Preditor associada ao modelo.

        Esta função atualiza o dicionário 'modelos' com o novo modelo adicionado.
        """
        self.modelos[nome_modelo] = preditor

    def plotar_resultados(self):
        """
        Gera gráficos de dispersão para comparar os resultados dos diferentes modelos.

        Para cada modelo armazenado no dicionário 'modelos', um gráfico de dispersão é gerado
        comparando os valores reais (y_test) com as previsões feitas pelo modelo.

        Cada gráfico inclui uma linha de referência (linha pontilhada) representando os valores
        reais ideais. Os gráficos são exibidos individualmente.

        Este método utiliza a biblioteca matplotlib para a geração dos gráficos.
        """  # noqa: E501
        for nome_modelo, preditor in self.modelos.items():
            plt.scatter(
                preditor.y_test,
                preditor.prediction,
                label=f"Previsões do modelo {nome_modelo}",
            )

            plt.plot(
                [preditor.y_test.min(), preditor.y_test.max()],
                [preditor.y_test.min(), preditor.y_test.max()],
                "k--",
                lw=2,
                label="Valores Reais",
            )

            plt.xlabel("Valores Reais")
            plt.ylabel("Previsões")
            plt.title(f"Comparação de Resultados - {nome_modelo}")
            plt.legend()
            plt.show()
