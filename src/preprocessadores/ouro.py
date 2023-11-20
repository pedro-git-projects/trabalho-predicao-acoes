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
                "Último": "Close",
                "Abertura": "Open",
                "Máxima": "High",
                "Mínima": "Low",
                "Vol.": "Volume",
                "Var%": "Var%",
            }
        )

        # convertendo a data para o mesmo formato que no brl.csv
        data["Date"] = data["Date"].dt.strftime("%Y-%m-%d")

        # salvando a saída em um novo arquivo
        data.to_csv(self.saida, index=False)

        return data
