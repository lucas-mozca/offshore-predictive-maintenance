from fastapi import APIRouter
from sqlalchemy import text

from api.database import engine


router = APIRouter()


@router.get("/alertas")
def listar_alertas():
    with engine.connect() as conexao:
        resultado = conexao.execute(
            text("""
                SELECT
                    id,
                    id_equipamento,
                    timestamp,
                    tipo,
                    nivel,
                    mensagem,
                    resolvido
                FROM alertas
                ORDER BY timestamp DESC;
            """)
        )

        alertas = []

        for linha in resultado:
            alertas.append({
                "id": linha.id,
                "id_equipamento": linha.id_equipamento,
                "timestamp": linha.timestamp,
                "tipo": linha.tipo,
                "nivel": linha.nivel,
                "mensagem": linha.mensagem,
                "resolvido": linha.resolvido
            })

        return alertas