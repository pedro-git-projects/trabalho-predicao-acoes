from pandas.core.dtypes.dtypes import datetime
from preprocessadores.ouro import Ouro
from preprocessadores.petroleo import Petroleo
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.svm import SVR
import pandas as pd
import numpy as np


class Preditor:
    """
    Classe responsável por prever valores usando modelos de regressão linear ou SVM.

    Attributes:
    - model: O modelo de regressão utilizado (LinearRegression ou SVR).
    - brl (pd.DataFrame): DataFrame contendo dados sobre o valor do Dólar em Reais.
    - bvsp (pd.DataFrame): DataFrame contendo dados relacionados ao índice Bovespa.
    - goll4 (pd.DataFrame): DataFrame contendo dados relacionados à ação GOLL4.
    - petroleo (pd.DataFrame): DataFrame contendo dados relacionados ao preço do petróleo.
    - ouro (pd.DataFrame): DataFrame contendo dados relacionados ao preço do ouro.
    - dados_combinados (pd.DataFrame): DataFrame combinado a partir dos dados individuais.
    - sufixos (tuple): Sufixos utilizados para identificar as colunas de cada DataFrame.
    - features (pd.DataFrame): DataFrame contendo as features utilizadas para previsão.
    - label (pd.Series): Série contendo a variável alvo para previsão.
    - X_train, X_test, y_train, y_test: Conjuntos de treino e teste para features e label.
    - prediction (numpy.ndarray): Array contendo as previsões do modelo.
    - mse (float): Erro quadrático médio calculado a partir das previsões.
    - rmse (float): Raiz quadrada do erro quadrático médio.

    Methods:
    - __init__(intervalo_datas=None, modelo="linear"): Inicializa a instância da classe.
    - __carregar_dados(intervalo_datas=None): Carrega os dados necessários para o treinamento e teste do modelo.
    - __combinar_dataframes(dataframes, sufixos=None): Combina os DataFrames de acordo com as colunas de datas.
    - __selecionar_features_e_label(): Seleciona as features e a label a partir do DataFrame combinado.
    - __selecionar_treino_e_teste(): Divide os dados em conjuntos de treino e teste.
    - fit(): Treina o modelo usando os dados de treino.
    - predict(): Realiza previsões usando o modelo treinado nos dados de teste.
    - mse(): Calcula o erro quadrático médio das previsões.
    - rmse(): Calcula a raiz quadrada do erro quadrático médio.

    Note:
    - O modelo SVM é inicializado com parâmetros padrão e pode ser personalizado conforme necessário.
    - Os DataFrames de ouro e petróleo são pré-processados usando classes específicas (Ouro e Petroleo).
    """  # noqa: E501

    def __init__(self, intervalo_datas=None, modelo="linear"):
        """
        Inicializa a instância da classe Preditor.

        Args:
        - intervalo_datas (str): Intervalo de datas no formato ISO (opcional).
        - modelo (str): Tipo de modelo a ser utilizado ("linear" ou "svm").

        Raises:
        - ValueError: Se o modelo fornecido não for "linear" ou "svm".
        """
        if modelo == "linear":
            self.model = LinearRegression()
        elif modelo == "svm":
            self.model = SVR()
        else:
            raise ValueError("Modelo não suportado. Escolha 'linear' ou 'svm'.")

        self.__carregar_dados(intervalo_datas)
        self.dados = (
            self.brl,
            self.bvsp,
            self.petroleo,
            self.ouro,
            self.goll4[["Date", "Adj Close"]],
        )

        self.sufixos = ("_brl", "_bvsp", "_petroleo", "_ouro", "_goll4")
        self.__combinar_dataframes(self.dados, self.sufixos)

        self.dados_combinados.to_csv("data/combinado.csv", index=False)

        self.__selecionar_features_e_label()
        self.__selecionar_treino_e_teste()

    def __carregar_dados(self, intervalo_datas=None):
        """
        Carrega dados de diferentes fontes para os DataFrames da classe.

        Args:
        - intervalo_datas (str): Intervalo de datas no formato ISO (opcional).
        """
        self.brl = pd.read_csv("data/brl.csv")
        self.bvsp = pd.read_csv("data/bvsp.csv")
        self.goll4 = pd.read_csv("data/goll4.csv")

        processador_petroleo = Petroleo(
            "data/desafio_petroleo.csv", "data/petroleo_tratado.csv"
        )
        processador_ouro = Ouro("data/desafio_ouro.csv", "data/ouro_tratado.csv")
        self.ouro = processador_ouro.preprocess()
        self.petroleo = processador_petroleo.preprocess()

        if intervalo_datas:
            try:
                inicio, fim = map(datetime.fromisoformat, intervalo_datas.split(","))
            except ValueError:
                print("Erro: Formato de data inválido. Utilize o formato ISO.")
                return

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
        """
        Combina os DataFrames usando a coluna "Date" como referência.

        Args:
        - dataframes (list): Lista de DataFrames a serem combinados.
        - sufixos (tuple): Sufixos utilizados para identificar as colunas de cada DataFrame (opcional).
        """  # noqa: E501
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
        """
        Seleciona as features e a label a partir do DataFrame combinado.
        """
        self.features = self.dados_combinados[
            ["Adj Close_brl", "Adj Close_petroleo", "Adj Close_ouro", "Adj Close_bvsp"]
        ]
        self.label = self.dados_combinados["Adj Close_goll4"]

    def __selecionar_treino_e_teste(self):
        """
        Divide os dados em conjuntos de treino e teste.
        """
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.features, self.label, test_size=0.25
        )

    def fit(self):
        """
        Treina o modelo usando os dados de treino.
        """
        return self.model.fit(self.X_train, self.y_train)

    def predict(self):
        """
        Realiza previsões usando o modelo treinado nos dados de teste.
        """
        self.prediction = self.model.predict(self.X_test)

    def mse(self):
        """
        Calcula o erro quadrático médio das previsões.

        Returns:
        - float: O erro quadrático médio.
        """
        self.mse = mean_squared_error(self.y_test, self.prediction)
        return self.mse

    def rmse(self):
        """
        Calcula a raiz quadrada do erro quadrático médio.

        Returns:
        - float: A raiz quadrada do erro quadrático médio.
        """
        self.mse()
        self.rmse = np.sqrt(self.mse)  # type: ignore
        return self.rmse
