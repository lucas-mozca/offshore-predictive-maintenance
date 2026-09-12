from sqlalchemy import text

from simulator.sensor_generator import simular_ciclo
from analysis.anomaly_detection import detectar_anomalias
from api.database import engine


def salvar_leitura(leitura, ciclo_id=None):
    anomalias = detectar_anomalias(leitura)

    if anomalias:
        status = "ALERTA"
    else:
        status = "NORMAL"

    with engine.begin() as conexao:
        conexao.execute(
            text("""
                INSERT INTO sensores_telemetria (
                    id_equipamento,
                    timestamp,
                    temperatura_celsius,
                    vibracao_mm_s,
                    pressao_bar,
                    status,
                    estado_simulado,
                    ciclo_id
                )
                VALUES (
                    :id_equipamento,
                    :timestamp,
                    :temperatura,
                    :vibracao,
                    :pressao,
                    :status,
                    :estado_simulado,
                    :ciclo_id
                )
            """),
            {
                "id_equipamento": 1,
                "timestamp": leitura["timestamp"],
                "temperatura": leitura["temperatura"],
                "vibracao": leitura["vibracao"],
                "pressao": leitura["pressao"],
                "status": status,
                "estado_simulado": leitura["estado_simulado"],
                "ciclo_id": ciclo_id
            }
        )

        for anomalia in anomalias:
            conexao.execute(
                text("""
                    INSERT INTO alertas (
                        id_equipamento,
                        timestamp,
                        tipo,
                        nivel,
                        mensagem
                    )
                    VALUES (
                        :id_equipamento,
                        :timestamp,
                        :tipo,
                        :nivel,
                        :mensagem
                    )
                """),
                {
                    "id_equipamento": 1,
                    "timestamp": leitura["timestamp"],
                    "tipo": anomalia["tipo"],
                    "nivel": anomalia["nivel"],
                    "mensagem": anomalia["mensagem"]
                }
            )

    print(
        f"Ciclo: {ciclo_id} | "
        f"{leitura['estado_simulado']} | "
        f"Temp: {leitura['temperatura']} °C | "
        f"Vib: {leitura['vibracao']} mm/s | "
        f"Pressão: {leitura['pressao']} bar | "
        f"Status: {status}"
    )

    if anomalias:
        for anomalia in anomalias:
            print(
                f"  → {anomalia['tipo']} | "
                f"{anomalia['nivel']}"
            )


if __name__ == "__main__":
    leituras = simular_ciclo()

    for leitura in leituras:
        salvar_leitura(
            leitura,
            ciclo_id=1
        )