import pandas as pd
import os

from preprocessadores.ouro import Ouro
from preprocessadores.petroleo import Petroleo


def print_head(df: pd.DataFrame) -> None:
    print(df.head)


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    processador_ouro = Ouro("../data/desafio_ouro.csv", "../data/ouro_tratado.csv")
    ouro = processador_ouro.preprocess()

    processador_petroleo = Petroleo(
        "../data/desafio_petroleo.csv", "../data/petroleo_tratado.csv"
    )
    petroleo = processador_petroleo.preprocess()


    brl = pd.read_csv("../data/brl.csv")
    bvsp = pd.read_csv("../data/bvsp.csv")
    goll4 = pd.read_csv("../data/goll4.csv")

    dfs = (brl, bvsp, ouro, goll4, ouro, petroleo)
    for df in dfs:
        print_head(df)


if __name__ == "__main__":
    main()
