import pandas as pd


class Ouro:
    def __init__(self, caminho_entrada: str, caminho_saida: str):
        self.entrada = caminho_entrada
        self.saida = caminho_saida

    def preprocess(self):
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

        # Convertendo a data para o mesmo formato que no brl.csv
        data["Date"] = data["Date"].dt.strftime("%Y-%m-%d")

        # Reordenando as colunas
        # e removendo var%
        data = data[["Date", "Open", "High", "Low", "Adj Close", "Volume"]]

        # Removendo o K e trocando vírgulas por pontos
        data["Volume"] = (
            data["Volume"]
            .str.replace("K", "e3")  # type: ignore
            .replace("", 0.0)
            .replace({",": "."}, regex=True)
            .astype(float)
        )

        # Preenchendo valores vazios com a média
        data["Volume"] = data["Volume"].fillna(data["Volume"].mean())  # type: ignore

        # Salvando a saída em um novo arquivo
        data.to_csv(self.saida, index=False)

        if isinstance(data, pd.Series):
            return data.to_frame()
        else:
            return data
