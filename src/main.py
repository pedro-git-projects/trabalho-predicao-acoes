import os

from preditor.preditor import Preditor


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Regrassão linear
    preditor_linear = Preditor(intervalo_datas=None, modelo='linear')
    preditor_linear.fit()
    preditor_linear.predict()
    print(f'Raiz quadrada do erro médio: {preditor_linear.rmse()}')

    # Regressão vetorial de suporte epsilon
    preditor_svm = Preditor(intervalo_datas=None, modelo='svm')
    preditor_svm.fit()
    preditor_svm.predict()
    print(f'SVM RMSE: {preditor_svm.rmse()}')

if __name__ == "__main__":
    main()
