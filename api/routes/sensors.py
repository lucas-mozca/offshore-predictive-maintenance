from fastapi import APIRouter
from sqlalchemy import text

from api.database import engine


router = APIRouter()


@router.get("/sensores")
def listar_sensores():
    with engine.connect() as conexao:
        resultado = conexao.execute(
            text("""
                SELECT
                    id,
                    id_equipamento,
                    timestamp,
                    temperatura_celsius,
                    vibracao_mm_s,
                    pressao_bar,
                    status
                FROM sensores_telemetria
                ORDER BY timestamp DESC;
            """)
        )

        sensores = []

        for linha in resultado:
            sensores.append({
                "id": linha.id,
                "id_equipamento": linha.id_equipamento,
                "timestamp": linha.timestamp,
                "temperatura": float(linha.temperatura_celsius),
                "vibracao": float(linha.vibracao_mm_s),
                "pressao": float(linha.pressao_bar),
                "status": linha.status
            })

        return sensores