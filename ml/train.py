import joblib
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)
from sklearn.model_selection import GroupKFold

from api.database import engine


def carregar_dataset():
    consulta = """
        SELECT
            temperatura_celsius,
            vibracao_mm_s,
            pressao_bar,
            estado_simulado,
            ciclo_id
        FROM sensores_telemetria
        WHERE
            estado_simulado IS NOT NULL
            AND ciclo_id IS NOT NULL;
    """

    dataframe = pd.read_sql(
        consulta,
        engine
    )

    return dataframe


def preparar_dados(dataframe):
    ciclos_treino = list(
        range(1, 17)
    )

    ciclos_teste = list(
        range(17, 21)
    )

    dados_treino = dataframe[
        dataframe["ciclo_id"].isin(
            ciclos_treino
        )
    ]

    dados_teste = dataframe[
        dataframe["ciclo_id"].isin(
            ciclos_teste
        )
    ]

    colunas_features = [
        "temperatura_celsius",
        "vibracao_mm_s",
        "pressao_bar"
    ]

    X_treino = dados_treino[
        colunas_features
    ]

    y_treino = dados_treino[
        "estado_simulado"
    ]

    X_teste = dados_teste[
        colunas_features
    ]

    y_teste = dados_teste[
        "estado_simulado"
    ]

    return (
        X_treino,
        X_teste,
        y_treino,
        y_teste
    )


def treinar_modelo(
    X_treino,
    y_treino
):
    modelo = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    modelo.fit(
        X_treino,
        y_treino
    )

    return modelo


def avaliar_modelo(
    modelo,
    X_teste,
    y_teste
):
    previsoes = modelo.predict(
        X_teste
    )

    acuracia = accuracy_score(
        y_teste,
        previsoes
    )

    print(
        "=== AVALIAÇÃO DO MODELO ==="
    )

    print(
        f"Acurácia: "
        f"{acuracia:.2%}"
    )

    print(
        "\nRelatório de classificação:"
    )

    print(
        classification_report(
            y_teste,
            previsoes
        )
    )

    matriz = confusion_matrix(
        y_teste,
        previsoes,
        labels=[
            "NORMAL",
            "DEGRADACAO",
            "FALHA"
        ]
    )

    print(
        "\nMatriz de confusão:"
    )

    print(
        "              PREVISTO"
    )

    print(
        "              NORMAL  "
        "DEGRADACAO  FALHA"
    )

    nomes_classes = [
        "NORMAL     ",
        "DEGRADACAO ",
        "FALHA      "
    ]

    for nome, linha in zip(
        nomes_classes,
        matriz
    ):
        print(
            f"{nome} {linha}"
        )


def validar_por_ciclos(dataframe):
    X = dataframe[
        [
            "temperatura_celsius",
            "vibracao_mm_s",
            "pressao_bar"
        ]
    ]

    y = dataframe[
        "estado_simulado"
    ]

    grupos = dataframe[
        "ciclo_id"
    ]

    group_kfold = GroupKFold(
        n_splits=5
    )

    acuracias = []

    print(
        "\n=== VALIDAÇÃO CRUZADA POR CICLOS ==="
    )

    for numero_fold, (
        indices_treino,
        indices_teste
    ) in enumerate(
        group_kfold.split(
            X,
            y,
            groups=grupos
        ),
        start=1
    ):
        X_treino = X.iloc[
            indices_treino
        ]

        X_teste = X.iloc[
            indices_teste
        ]

        y_treino = y.iloc[
            indices_treino
        ]

        y_teste = y.iloc[
            indices_teste
        ]

        modelo = RandomForestClassifier(
            n_estimators=100,
            random_state=42
        )

        modelo.fit(
            X_treino,
            y_treino
        )

        previsoes = modelo.predict(
            X_teste
        )

        acuracia = accuracy_score(
            y_teste,
            previsoes
        )

        acuracias.append(
            acuracia
        )

        print(
            f"Fold {numero_fold}: "
            f"{acuracia:.2%}"
        )

    media = sum(
        acuracias
    ) / len(
        acuracias
    )

    print(
        f"\nAcurácia média: "
        f"{media:.2%}"
    )


def treinar_modelo_final(dataframe):
    X = dataframe[
        [
            "temperatura_celsius",
            "vibracao_mm_s",
            "pressao_bar"
        ]
    ]

    y = dataframe[
        "estado_simulado"
    ]

    modelo_final = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    modelo_final.fit(
        X,
        y
    )

    print(
        f"\nModelo final treinado com "
        f"{len(X)} amostras."
    )

    return modelo_final


def salvar_modelo(modelo):
    pasta_modelo = Path(
        "ml/model"
    )

    pasta_modelo.mkdir(
        parents=True,
        exist_ok=True
    )

    caminho_modelo = (
        pasta_modelo
        / "random_forest.pkl"
    )

    joblib.dump(
        modelo,
        caminho_modelo
    )

    print(
        f"\nModelo salvo em: "
        f"{caminho_modelo}"
    )


if __name__ == "__main__":
    dataframe = carregar_dataset()

    (
        X_treino,
        X_teste,
        y_treino,
        y_teste
    ) = preparar_dados(
        dataframe
    )

    print(
        "=== DIVISÃO POR CICLOS ==="
    )

    print(
        f"Treinamento: "
        f"{len(X_treino)} amostras"
    )

    print(
        f"Teste: "
        f"{len(X_teste)} amostras"
    )

    modelo_avaliacao = treinar_modelo(
        X_treino,
        y_treino
    )

    avaliar_modelo(
        modelo_avaliacao,
        X_teste,
        y_teste
    )

    validar_por_ciclos(
        dataframe
    )

    modelo_final = treinar_modelo_final(
        dataframe
    )

    salvar_modelo(
        modelo_final
    )