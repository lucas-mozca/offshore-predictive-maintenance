import sys
from pathlib import Path

import pandas as pd
import streamlit as st
from sqlalchemy import text


# Permite importar módulos a partir da raiz do projeto
raiz_projeto = Path(__file__).resolve().parent.parent
sys.path.append(str(raiz_projeto))


from api.database import engine
from ml.predict import carregar_modelo, prever_estado


st.set_page_config(
    page_title="Offshore Predictive Maintenance",
    page_icon="⚙️",
    layout="wide"
)


@st.cache_resource
def obter_modelo():
    return carregar_modelo()


def carregar_telemetria():
    consulta = text("""
        SELECT
            id,
            id_equipamento,
            timestamp,
            temperatura_celsius,
            vibracao_mm_s,
            pressao_bar,
            status,
            estado_simulado,
            ciclo_id
        FROM sensores_telemetria
        ORDER BY timestamp DESC
        LIMIT 100;
    """)

    dataframe = pd.read_sql(
        consulta,
        engine
    )

    dataframe = dataframe.sort_values(
        "timestamp"
    )

    return dataframe


def carregar_alertas():
    consulta = text("""
        SELECT
            timestamp,
            tipo,
            nivel,
            mensagem,
            resolvido
        FROM alertas
        ORDER BY timestamp DESC
        LIMIT 10;
    """)

    return pd.read_sql(
        consulta,
        engine
    )


def definir_status_visual(previsao):
    if previsao == "NORMAL":
        return "🟢 NORMAL"

    if previsao == "DEGRADACAO":
        return "🟡 DEGRADAÇÃO"

    if previsao == "FALHA":
        return "🔴 FALHA"

    return previsao


st.title(
    "⚙️ Offshore Predictive Maintenance"
)

st.caption(
    "Sistema educacional de manutenção preditiva "
    "para bombas centrífugas com dados simulados."
)


try:
    dataframe = carregar_telemetria()

except Exception as erro:
    st.error(
        "Erro ao carregar dados do PostgreSQL."
    )

    st.exception(
        erro
    )

    st.stop()


if dataframe.empty:
    st.warning(
        "Nenhuma leitura de telemetria encontrada."
    )

    st.stop()


ultima_leitura = dataframe.iloc[-1]


temperatura = float(
    ultima_leitura[
        "temperatura_celsius"
    ]
)

vibracao = float(
    ultima_leitura[
        "vibracao_mm_s"
    ]
)

pressao = float(
    ultima_leitura[
        "pressao_bar"
    ]
)

status_regras = ultima_leitura[
    "status"
]


modelo = obter_modelo()


previsao, probabilidades = prever_estado(
    modelo,
    temperatura,
    vibracao,
    pressao
)


probabilidades_por_classe = dict(
    zip(
        modelo.classes_,
        probabilidades
    )
)


st.subheader(
    "📡 Estado atual da bomba"
)


coluna1, coluna2, coluna3 = st.columns(
    3
)


with coluna1:
    st.metric(
        label="Temperatura",
        value=f"{temperatura:.2f} °C"
    )


with coluna2:
    st.metric(
        label="Vibração",
        value=f"{vibracao:.2f} mm/s"
    )


with coluna3:
    st.metric(
        label="Pressão",
        value=f"{pressao:.2f} bar"
    )


st.divider()


coluna_status, coluna_ml = st.columns(
    2
)


with coluna_status:
    st.subheader(
        "🚨 Detecção por regras"
    )

    if status_regras == "ALERTA":
        st.error(
            "ALERTA"
        )
    else:
        st.success(
            "NORMAL"
        )

    st.caption(
        "Resultado obtido através dos limites "
        "definidos no sistema de regras."
    )


with coluna_ml:
    st.subheader(
        "🤖 Previsão do Machine Learning"
    )

    status_ml = definir_status_visual(
        previsao
    )

    if previsao == "NORMAL":
        st.success(
            status_ml
        )

    elif previsao == "DEGRADACAO":
        st.warning(
            status_ml
        )

    elif previsao == "FALHA":
        st.error(
            status_ml
        )

    else:
        st.info(
            status_ml
        )

    st.caption(
        "Classificação realizada pelo modelo "
        "Random Forest."
    )


st.divider()


st.subheader(
    "📊 Probabilidade por estado"
)


prob_normal = (
    probabilidades_por_classe.get(
        "NORMAL",
        0
    )
)

prob_degradacao = (
    probabilidades_por_classe.get(
        "DEGRADACAO",
        0
    )
)

prob_falha = (
    probabilidades_por_classe.get(
        "FALHA",
        0
    )
)


coluna_normal, coluna_degradacao, coluna_falha = (
    st.columns(3)
)


with coluna_normal:
    st.metric(
        "NORMAL",
        f"{prob_normal:.2%}"
    )

    st.progress(
        float(prob_normal)
    )


with coluna_degradacao:
    st.metric(
        "DEGRADAÇÃO",
        f"{prob_degradacao:.2%}"
    )

    st.progress(
        float(prob_degradacao)
    )


with coluna_falha:
    st.metric(
        "FALHA",
        f"{prob_falha:.2%}"
    )

    st.progress(
        float(prob_falha)
    )


st.caption(
    "As probabilidades representam a confiança "
    "do modelo nos dados simulados e não uma "
    "probabilidade real de falha industrial."
)


st.divider()


st.subheader(
    "📈 Histórico dos sensores"
)


grafico_temperatura = (
    dataframe[
        [
            "timestamp",
            "temperatura_celsius"
        ]
    ]
    .set_index(
        "timestamp"
    )
)


st.write(
    "### Temperatura"
)

st.line_chart(
    grafico_temperatura
)


grafico_vibracao = (
    dataframe[
        [
            "timestamp",
            "vibracao_mm_s"
        ]
    ]
    .set_index(
        "timestamp"
    )
)


st.write(
    "### Vibração"
)

st.line_chart(
    grafico_vibracao
)


grafico_pressao = (
    dataframe[
        [
            "timestamp",
            "pressao_bar"
        ]
    ]
    .set_index(
        "timestamp"
    )
)


st.write(
    "### Pressão"
)

st.line_chart(
    grafico_pressao
)


st.divider()


st.subheader(
    "📋 Últimas leituras"
)


tabela_leituras = dataframe[
    [
        "timestamp",
        "temperatura_celsius",
        "vibracao_mm_s",
        "pressao_bar",
        "status"
    ]
].sort_values(
    "timestamp",
    ascending=False
).head(10)


st.dataframe(
    tabela_leituras,
    use_container_width=True,
    hide_index=True
)


st.divider()


st.subheader(
    "🚨 Alertas recentes"
)


try:
    alertas = carregar_alertas()

    if alertas.empty:
        st.success(
            "Nenhum alerta registrado."
        )

    else:
        st.dataframe(
            alertas,
            use_container_width=True,
            hide_index=True
        )

except Exception as erro:
    st.warning(
        "Não foi possível carregar os alertas."
    )


st.divider()


st.subheader(
    "🧠 Informações do modelo"
)


coluna_modelo1, coluna_modelo2, coluna_modelo3 = (
    st.columns(3)
)


with coluna_modelo1:
    st.metric(
        "Algoritmo",
        "Random Forest"
    )


with coluna_modelo2:
    st.metric(
        "Validação cruzada",
        "93,50%"
    )


with coluna_modelo3:
    st.metric(
        "Amostras finais",
        "600"
    )


st.caption(
    "A acurácia de 93,50% corresponde à média "
    "obtida com GroupKFold em 20 ciclos simulados. "
    "O modelo final foi posteriormente treinado "
    "com todas as 600 leituras."
)