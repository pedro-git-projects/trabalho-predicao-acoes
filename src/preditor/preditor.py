from pandas.core.dtypes.dtypes import datetime
from preprocessadores.ouro import Ouro
from preprocessadores.petroleo import Petroleo
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np


class Preditor:
    def __init__(self, intervalo_datas=None):
        self.model = LinearRegression()
        self.carregar_dados(intervalo_datas)

        self.dados = (
            self.brl,
            self.bvsp,
            self.petroleo,
            self.ouro,
            self.goll4[["Date", "Adj Close"]],
        )

        self.sufixos = ("_brl", "_bvsp", "_petroleo", "_ouro", "_goll4")
        self.__combinar_dataframes(self.dados, self.sufixos)

        self.dados_combinados.to_csv("../data/combinado.csv", index=False)

        self.__selecionar_features_e_label()
        self.__selecionar_treino_e_teste()

    def carregar_dados(self, intervalo_datas=None):
        self.brl = pd.read_csv("../data/brl.csv")
        self.bvsp = pd.read_csv("../data/bvsp.csv")
        self.goll4 = pd.read_csv("../data/goll4.csv")

        processador_petroleo = Petroleo(
            "../data/desafio_petroleo.csv", "../data/petroleo_tratado.csv"
        )
        processador_ouro = Ouro("../data/desafio_ouro.csv", "../data/ouro_tratado.csv")
        self.ouro = processador_ouro.preprocess()
        self.petroleo = processador_petroleo.preprocess()

        if intervalo_datas:
            try:
                inicio, fim = map(datetime.fromisoformat, intervalo_datas.split(","))
            except ValueError:
                print("Erro: Formato de data inválido. Utilize o formato ISO.")
                return

            # Check if the date range is valid
            if inicio >= fim:
                print("Erro: A data de início deve ser anterior à data de término.")
                print("Os valores padrão serão utilizados...")
                return

            inicio, fim = map(datetime.fromisoformat, intervalo_datas.split(","))

            # Convertendo a coluna Date para DateTime
            self.brl["Date"] = pd.to_datetime(self.brl["Date"])
            self.bvsp["Date"] = pd.to_datetime(self.bvsp["Date"])
            self.goll4["Date"] = pd.to_datetime(self.goll4["Date"])
            self.ouro["Date"] = pd.to_datetime(self.ouro["Date"])
            self.petroleo["Date"] = pd.to_datetime(self.petroleo["Date"])

            # Filtra os dados baseado no intervalo
            self.brl = self.brl[
                (self.brl["Date"] >= inicio) & (self.brl["Date"] <= fim)
            ]
            self.bvsp = self.bvsp[
                (self.bvsp["Date"] >= inicio) & (self.bvsp["Date"] <= fim)
            ]
            self.goll4 = self.goll4[
                (self.goll4["Date"] >= inicio) & (self.goll4["Date"] <= fim)
            ]
            self.ouro = self.ouro[
                (self.ouro["Date"] >= inicio) & (self.ouro["Date"] <= fim)
            ]
            self.petroleo = self.petroleo[
                (self.petroleo["Date"] >= inicio) & (self.petroleo["Date"] <= fim)
            ]

    def __combinar_dataframes(self, dataframes, sufixos=None):
        if sufixos is None:
            sufixos = [""] * len(dataframes)

        dados_combinados = dataframes[0].copy()
        for i in range(0, len(dataframes)):
            dados_combinados = pd.merge(
                dados_combinados,
                dataframes[i],
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
            self.features, self.label, test_size=0.25
        )

    def fit(self) -> LinearRegression:
        return self.model.fit(self.X_train, self.y_train)

    def predict(self):
        self.prediction = self.model.predict(self.X_test)

    def mse(self):
        self.mse = mean_squared_error(self.y_test, self.prediction)

    def rmse(self):
        self.rmse = np.sqrt(self.mse)  # type: ignore
