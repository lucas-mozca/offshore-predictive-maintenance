import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


load_dotenv()


DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")


DATABASE_URL = (
    f"postgresql+psycopg2://{DATABASE_USER}:"
    f"{DATABASE_PASSWORD}@{DATABASE_HOST}:"
    f"{DATABASE_PORT}/{DATABASE_NAME}"
)


engine = create_engine(DATABASE_URL)


def testar_conexao():
    with engine.connect() as conexao:
        resultado = conexao.execute(
            text("SELECT * FROM equipamentos;")
        )

        for linha in resultado:
            print(linha)


if __name__ == "__main__":
    testar_conexao()