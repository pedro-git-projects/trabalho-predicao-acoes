import matplotlib.pyplot as plt
from preditor.preditor import Preditor


class Comparador:
    def __init__(self):
        self.modelos = {}

    def adicionar_modelo(self, nome_modelo, preditor: Preditor):
        self.modelos[nome_modelo] = preditor

    def plotar_resultados(self):
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
