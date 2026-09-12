def detectar_anomalias(leitura):
    anomalias = []

    if leitura["temperatura"] > 80:
        anomalias.append({
            "tipo": "TEMPERATURA_ELEVADA",
            "nivel": "ALTO",
            "mensagem": "Temperatura acima do limite operacional esperado."
        })

    if leitura["vibracao"] > 6:
        anomalias.append({
            "tipo": "VIBRACAO_ELEVADA",
            "nivel": "ALTO",
            "mensagem": "Vibração acima do limite operacional esperado."
        })

    if leitura["pressao"] < 15:
        anomalias.append({
            "tipo": "PRESSAO_BAIXA",
            "nivel": "MEDIO",
            "mensagem": "Pressão abaixo do limite operacional esperado."
        })

    return anomalias


if __name__ == "__main__":
    leitura_teste = {
        "temperatura": 89.87,
        "vibracao": 6.83,
        "pressao": 14.96
    }

    resultado = detectar_anomalias(leitura_teste)

    print(resultado)