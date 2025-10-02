import math
from typing import Literal

from scipy.stats import poisson


def calculate_prob(
    mean: float, threshold: float, mode: Literal["over", "under", "exactly"]
) -> float:
    match mode:
        case "over":
            prob = 0
            for i in range(math.ceil(threshold)):
                prob += poisson.pmf(i, mean)
            return 1 - prob
        case "under":
            prob = 0
            for i in range(math.ceil(threshold)):
                prob += poisson.pmf(i, mean)
            return prob
        case "exactly":
            if threshold != int(threshold):
                return 0.0  # prob de um evento float é 0
            return poisson.pmf(threshold, mean)


def calculate_odd(prob):
    return 1 / prob


def calculate_house_edge(fair_odd, house_odd):
    edge = (fair_odd - house_odd) / fair_odd
    return edge * 100


if __name__ == "__main__":
    mean = float(input("Digite a média do evento por partida: "))
    threshold = float(input("Digite o número de ocorrências para odd bater: "))

    while True:
        print(
            f"over - para mais de {threshold} \nunder - para menos de {threshold} \nexactly - para exatamente {threshold}"
        )
        modo = input("Digite a opção desejada: ")
        if modo in ["over", "under", "exactly"]:
            prob = calculate_prob(mean, threshold, modo)
            break
        else:
            print("Opção inválida. Tente novamente.")

    print(f"\nA probabilidade de ocorrer é {prob * 100:.2f}%")

    odd = calculate_odd(prob)

    print(f"A odd justa, sem margem de lucro, é de {odd:.2f}")

    odd_house = float(input("Digite a odd da casa: "))
    edge = calculate_house_edge(odd, odd_house)

    print(f"A margem de lucro da casa nessa aposta é de {edge:.2f}%")
