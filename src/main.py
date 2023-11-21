import os

from preditor.preditor import Preditor


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    p = Preditor(intervalo_datas="2023-01-02,2022-01-03")
    p.fit()
    p.predict()
    p.mse()
    p.rmse()

    print(f"Erro médio quadrático: {p.mse}")
    print(f"Raiz do erro médio quadrático: {p.rmse}")


if __name__ == "__main__":
    main()
