import random
from datetime import datetime, timedelta


def gerar_leitura(estado="NORMAL"):

    if estado == "NORMAL":
        temperatura = random.uniform(60, 75)
        vibracao = random.uniform(2, 4.5)
        pressao = random.uniform(17, 20)

    elif estado == "DEGRADACAO":
        temperatura = random.uniform(74, 82)
        vibracao = random.uniform(4, 6.5)
        pressao = random.uniform(15, 18)

    elif estado == "FALHA":
        temperatura = random.uniform(82, 95)
        vibracao = random.uniform(6.5, 9)
        pressao = random.uniform(12, 15.5)

    else:
        raise ValueError("Estado de operação inválido.")

    leitura = {
        "timestamp": datetime.now(),
        "temperatura": round(temperatura, 2),
        "vibracao": round(vibracao, 2),
        "pressao": round(pressao, 2)
    }

    return leitura

def simular_ciclo():
    leituras = []

    total_leituras = 30
    tempo_inicial = datetime.now()
    

    for i in range(total_leituras):
        progresso = i / (total_leituras - 1)

        temperatura_base = 65 + (25 * progresso)
        vibracao_base = 3 + (5 * progresso)
        pressao_base = 19 - (6 * progresso)

        temperatura = temperatura_base + random.uniform(-2, 2)
        vibracao = vibracao_base + random.uniform(-0.5, 0.5)
        pressao = pressao_base + random.uniform(-0.7, 0.7)

        if progresso < 0.4:
            estado = "NORMAL"
        elif progresso < 0.75:
            estado = "DEGRADACAO"
        else:
            estado = "FALHA"

        leitura = {
           "timestamp": tempo_inicial + timedelta(seconds=i),
            "temperatura": round(temperatura, 2),
            "vibracao": round(vibracao, 2),
            "pressao": round(pressao, 2),
            "estado_simulado": estado
        }

        leituras.append(leitura)

    return leituras

if __name__ == "__main__":
    leituras = simular_ciclo()

    for leitura in leituras:
        print(leitura)
