import pandas as pd


class Petroleo:
    def __init__(self, caminho_entrada: str, caminho_saida: str):
        self.entrada = caminho_entrada
        self.saida = caminho_saida

    def preprocess(self) -> pd.DataFrame:
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

        data.to_csv(self.saida, index=False)

        if isinstance(data, pd.Series):
            return data.to_frame()
        else:
            return data
