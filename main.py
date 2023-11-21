from comparador.comparador import Comparador
from preditor.preditor import Preditor
import os


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    comparador = Comparador()

    # Regrassão linear
    preditor_linear = Preditor(intervalo_datas=None, modelo="linear")
    preditor_linear.fit()
    preditor_linear.predict()
    comparador.adicionar_modelo("Linear Regression", preditor_linear)
    print(f"Raiz quadrada do erro médio: {preditor_linear.rmse()}")

    # Regressão vetorial de suporte epsilon
    preditor_svm = Preditor(intervalo_datas=None, modelo="svm")
    preditor_svm.fit()
    preditor_svm.predict()
    comparador.adicionar_modelo("SVM", preditor_svm)
    print(f"SVM RMSE: {preditor_svm.rmse()}")

    comparador.plotar_resultados()


if __name__ == "__main__":
    main()
