import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import text

from api.database import engine


def analisar_leituras():
    with engine.connect() as conexao:
        resultado = conexao.execute(
            text("""
                SELECT
                    COUNT(*) AS total,

                    COUNT(*) FILTER (
                        WHERE status = 'NORMAL'
                    ) AS normais,

                    COUNT(*) FILTER (
                        WHERE status = 'ALERTA'
                    ) AS alertas,

                    AVG(temperatura_celsius) AS temperatura_media,
                    MIN(temperatura_celsius) AS temperatura_minima,
                    MAX(temperatura_celsius) AS temperatura_maxima,

                    AVG(vibracao_mm_s) AS vibracao_media,
                    MIN(vibracao_mm_s) AS vibracao_minima,
                    MAX(vibracao_mm_s) AS vibracao_maxima,

                    AVG(pressao_bar) AS pressao_media,
                    MIN(pressao_bar) AS pressao_minima,
                    MAX(pressao_bar) AS pressao_maxima

                FROM sensores_telemetria;
            """)
        )

        linha = resultado.fetchone()

        print("=== ANÁLISE HISTÓRICA DA TELEMETRIA ===")

        print(f"\nTotal de leituras: {linha.total}")
        print(f"Leituras normais: {linha.normais}")
        print(f"Leituras em alerta: {linha.alertas}")

        print("\n--- TEMPERATURA ---")
        print(f"Média: {linha.temperatura_media:.2f} °C")
        print(f"Mínima: {linha.temperatura_minima:.2f} °C")
        print(f"Máxima: {linha.temperatura_maxima:.2f} °C")

        print("\n--- VIBRAÇÃO ---")
        print(f"Média: {linha.vibracao_media:.2f} mm/s")
        print(f"Mínima: {linha.vibracao_minima:.2f} mm/s")
        print(f"Máxima: {linha.vibracao_maxima:.2f} mm/s")

        print("\n--- PRESSÃO ---")
        print(f"Média: {linha.pressao_media:.2f} bar")
        print(f"Mínima: {linha.pressao_minima:.2f} bar")
        print(f"Máxima: {linha.pressao_maxima:.2f} bar")


def gerar_grafico_historico():
    consulta = """
        SELECT
            timestamp,
            temperatura_celsius,
            vibracao_mm_s,
            pressao_bar
        FROM sensores_telemetria
        ORDER BY timestamp ASC;
    """

    dataframe = pd.read_sql(consulta, engine)

    # TEMPERATURA
    plt.figure(figsize=(12, 5))

    plt.plot(
        dataframe["timestamp"],
        dataframe["temperatura_celsius"],
        label="Temperatura"
    )

    plt.axhline(
        y=80,
        linestyle="--",
        label="Limite de alerta (80 °C)"
    )

    plt.title("Histórico de Temperatura")
    plt.xlabel("Tempo")
    plt.ylabel("Temperatura (°C)")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # VIBRAÇÃO
    plt.figure(figsize=(12, 5))

    plt.plot(
        dataframe["timestamp"],
        dataframe["vibracao_mm_s"],
        label="Vibração"
    )

    plt.axhline(
        y=6,
        linestyle="--",
        label="Limite de alerta (6 mm/s)"
    )

    plt.title("Histórico de Vibração")
    plt.xlabel("Tempo")
    plt.ylabel("Vibração (mm/s)")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # PRESSÃO
    plt.figure(figsize=(12, 5))

    plt.plot(
        dataframe["timestamp"],
        dataframe["pressao_bar"],
        label="Pressão"
    )

    plt.axhline(
        y=15,
        linestyle="--",
        label="Limite de alerta (15 bar)"
    )

    plt.title("Histórico de Pressão")
    plt.xlabel("Tempo")
    plt.ylabel("Pressão (bar)")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    analisar_leituras()
    gerar_grafico_historico()