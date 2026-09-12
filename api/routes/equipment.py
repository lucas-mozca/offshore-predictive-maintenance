from fastapi import APIRouter
from sqlalchemy import text

from api.database import engine


router = APIRouter()


@router.get("/equipamentos")
def listar_equipamentos():
    with engine.connect() as conexao:
        resultado = conexao.execute(
            text("""
                SELECT
                    id,
                    codigo,
                    nome,
                    localizacao,
                    modelo,
                    status,
                    data_instalacao
                FROM equipamentos
                ORDER BY id;
            """)
        )

        equipamentos = []

        for linha in resultado:
            equipamentos.append({
                "id": linha.id,
                "codigo": linha.codigo,
                "nome": linha.nome,
                "localizacao": linha.localizacao,
                "modelo": linha.modelo,
                "status": linha.status,
                "data_instalacao": linha.data_instalacao
            })

        return equipamentos