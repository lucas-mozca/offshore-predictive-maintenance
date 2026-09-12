from fastapi import APIRouter
from sqlalchemy import text

from api.database import engine
from ml.predict import carregar_modelo, prever_estado


router = APIRouter()

modelo = carregar_modelo()


@router.get("/previsao")
def obter_previsao():
    with engine.connect() as conexao:
        resultado = conexao.execute(
            text("""
                SELECT
                    temperatura_celsius,
                    vibracao_mm_s,
                    pressao_bar
                FROM sensores_telemetria
                ORDER BY timestamp DESC
                LIMIT 1;
            """)
        )

        leitura = resultado.fetchone()

    if leitura is None:
        return {
            "erro": "Nenhuma leitura disponível."
        }

    estado_previsto, probabilidades = prever_estado(
        modelo,
        temperatura=float(leitura.temperatura_celsius),
        vibracao=float(leitura.vibracao_mm_s),
        pressao=float(leitura.pressao_bar)
    )

    probabilidades_formatadas = {}

    for classe, probabilidade in zip(
        modelo.classes_,
        probabilidades
    ):
        probabilidades_formatadas[classe] = round(
            float(probabilidade),
            4
        )

    return {
        "leitura": {
            "temperatura": float(leitura.temperatura_celsius),
            "vibracao": float(leitura.vibracao_mm_s),
            "pressao": float(leitura.pressao_bar)
        },
        "estado_previsto": estado_previsto,
        "probabilidades": probabilidades_formatadas
    }