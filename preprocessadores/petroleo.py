import pandas as pd


class Petroleo:
    """
    Classe responsável pelo pré-processamento de dados relacionados ao preço do petróleo.

    Attributes:
    - entrada (str): Caminho do arquivo de entrada contendo os dados brutos do petróleo.
    - saida (str): Caminho do arquivo de saída onde os dados pré-processados serão salvos.

    Methods:
    - __init__(caminho_entrada, caminho_saida): Inicializa a instância da classe Petroleo.
    - preprocess() -> pd.DataFrame: Realiza o pré-processamento dos dados de petróleo e salva o resultado no arquivo de saída.

    Note:
    - Esta classe espera que o arquivo de entrada tenha colunas específicas, como "Data", "Último", "Abertura", etc.
    - Os dados são ajustados para terem uma estrutura similar ao arquivo "brl.csv".
    - O pré-processamento inclui renomeação de colunas, conversão de datas, tratamento de valores ausentes e salvamento do arquivo final.
    """  # noqa: E501

    def __init__(self, caminho_entrada: str, caminho_saida: str):
        """
        Inicializa a instância da classe Petroleo.

        Args:
        - caminho_entrada (str): Caminho do arquivo de entrada contendo os dados brutos do petróleo.
        - caminho_saida (str): Caminho do arquivo de saída onde os dados pré-processados serão salvos.
        """  # noqa: E501

        self.entrada = caminho_entrada
        self.saida = caminho_saida

    def preprocess(self) -> pd.DataFrame:
        """
        Realiza o pré-processamento dos dados de petróleo.

        Returns:
        - pd.DataFrame: DataFrame contendo os dados pré-processados do petróleo.
        """
        data = pd.read_csv(
            self.entrada,
            thousands=".",
            decimal=",",
            parse_dates=["Data"],
            dayfirst=True,
        )

        # Renomeando as colunas para terem a mesma estrutura
        # do arquivo brl.csv
        data = data.rename(
            columns={
                "Data": "Date",
                "Último": "Adj Close",
                "Abertura": "Open",
                "Máxima": "High",
                "Mínima": "Low",
                "Vol.": "Volume",
                "Var%": "Var%",
            }
        )

        # Formatando a data de acordo com o aqruivo brl.csv
        data["Date"] = data["Date"].dt.strftime("%Y-%m-%d")

        # Reordenando as colunas
        # e removendo var%
        data = data[["Date", "Open", "High", "Low", "Adj Close", "Volume"]]

        # Removendo o K e M, trocando vírgulas por pontos
        data["Volume"] = (
            data["Volume"]
            .str.replace("K", "e3")  # type: ignore
            .replace("", 0.0)
            .replace({",": ".", "K": "e3", "M": "e6"}, regex=True)
            .astype(float)
        )

        # Preenchendo valores vazios com a média
        data["Volume"] = data["Volume"].fillna(data["Volume"].mean())  # type: ignore

        data.to_csv(self.saida, index=False)

        if isinstance(data, pd.Series):
            return data.to_frame()
        else:
            return data
