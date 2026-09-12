import joblib
import pandas as pd
from pathlib import Path


def carregar_modelo():
    caminho_modelo = Path("ml/model/random_forest.pkl")

    modelo = joblib.load(caminho_modelo)

    return modelo


def prever_estado(modelo, temperatura, vibracao, pressao):
    dados = pd.DataFrame(
        [
            {
                "temperatura_celsius": temperatura,
                "vibracao_mm_s": vibracao,
                "pressao_bar": pressao
            }
        ]
    )

    previsao = modelo.predict(dados)[0]
    probabilidades = modelo.predict_proba(dados)[0]

    return previsao, probabilidades


if __name__ == "__main__":
    modelo = carregar_modelo()

    estado_previsto, probabilidades = prever_estado(
        modelo,
        temperatura=78.5,
        vibracao=5.4,
        pressao=16.2
    )

    print("=== PREVISÃO DO MODELO ===")
    print(f"Estado previsto: {estado_previsto}")

    print("\nProbabilidades:")

    for classe, probabilidade in zip(
        modelo.classes_,
        probabilidades
    ):
        print(
            f"{classe}: "
            f"{probabilidade:.2%}"
        )