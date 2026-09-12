from simulator.sensor_generator import simular_ciclo
from simulator.save_reading import salvar_leitura


def gerar_dataset(quantidade_ciclos=20):
    total_leituras = 0

    print("=== GERAÇÃO DO DATASET ===")

    for numero_ciclo in range(1, quantidade_ciclos + 1):
        leituras = simular_ciclo()

        print(f"\nCiclo {numero_ciclo}/{quantidade_ciclos}")

        for leitura in leituras:
            salvar_leitura(
                leitura,
                ciclo_id=numero_ciclo
            )

            total_leituras += 1

    print("\n=== DATASET GERADO ===")
    print(f"Ciclos: {quantidade_ciclos}")
    print(f"Novas leituras: {total_leituras}")


if __name__ == "__main__":
    gerar_dataset()