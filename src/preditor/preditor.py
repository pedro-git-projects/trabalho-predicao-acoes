import pandas as pd
from preprocessadores.ouro import Ouro
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

from preprocessadores.petroleo import Petroleo


class Preditor:
    def __init__(self) -> None:
        self.model = LinearRegression()
        self.__carregar_dados()
        self.dados = (
            self.brl,
            self.bvsp,
            self.petroleo,
            self.ouro,
            self.goll4[["Date", "Adj Close"]],
        )

        self.sufixos = ("_brl", "_bvsp", "_petroleo", "_ouro", "_goll4")
        print(self.sufixos)
        self.__combinar_dataframes(self.dados, self.sufixos)

        self.dados_combinados.to_csv("../data/combinado.csv", index=False)
        print(f"COLUMNS::{self.dados_combinados.columns}")
        self.__selecionar_features_e_label()
        self.__selecionar_treino_e_teste()

    def __carregar_dados(self):
        self.brl = pd.read_csv("../data/brl.csv")
        self.bvsp = pd.read_csv("../data/bvsp.csv")
        self.goll4 = pd.read_csv("../data/goll4.csv")

        processador_petroleo = Petroleo(
            "../data/desafio_petroleo.csv", "../data/petroleo_tratado.csv"
        )
        processador_ouro = Ouro("../data/desafio_ouro.csv", "../data/ouro_tratado.csv")

        self.ouro = processador_ouro.preprocess()
        self.petroleo = processador_petroleo.preprocess()

    def __combinar_dataframes(self, dataframes, sufixos=None):
        if sufixos is None:
            sufixos = [""] * len(dataframes)

        dados_combinados = dataframes[0].copy()
        print(dataframes[0])
        for i in range(0, len(dataframes)):
            dados_combinados = pd.merge(
                dados_combinados,
                dataframes[i],
                how="left",
                on="Date",
                suffixes=("", sufixos[i]),
            )

        self.dados_combinados = dados_combinados

    def __selecionar_features_e_label(self):
        self.features = self.dados_combinados[
            ["Adj Close_brl", "Adj Close_petroleo", "Adj Close_ouro", "Adj Close_bvsp"]
        ]
        self.label = self.dados_combinados["Adj Close_goll4"]

    def __selecionar_treino_e_teste(self):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.features, self.label, test_size=0.2
        )

    # TODO: tratar Volume para poder utilizar regressão linear
    def fit(self) -> LinearRegression:
        return self.model.fit(self.X_train, self.y_train)

    def predict(self):
        return self.model.predict(self.X_test)
