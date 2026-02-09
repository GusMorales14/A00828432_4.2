# pylint: disable=invalid-name
"""Compute descriptive statistics from an input file of numbers."""

import argparse
import time

def ordenar_lista(values: list[float]) -> list[float]:
    """Ordena una lista de números en orden ascendente usando insertion sort."""
    sorted_values = values[:]

    for i in range(1, len(sorted_values)):
        key = sorted_values[i]
        j = i - 1

        while j >= 0 and sorted_values[j] > key:
            sorted_values[j + 1] = sorted_values[j]
            j -= 1

        sorted_values[j + 1] = key

    return sorted_values

def calcular_mediana(values: list[float]) -> float:
    """Calcula la mediana de una lista de números."""
    sorted_values = ordenar_lista(values)
    n = len(sorted_values)
    mid = n // 2

    if n % 2 == 1:
        return sorted_values[mid]

    return (sorted_values[mid - 1] + sorted_values[mid]) / 2.0

def calcular_moda(values: list[float]) -> float:
    """Calcula la moda. En empate, regresa el mayor valor."""
    counts: dict[float, int] = {}

    for v in values:
        counts[v] = counts.get(v, 0) + 1

    moda_valor = values[0]
    moda_freq = counts[moda_valor]

    for v, c in counts.items():
        if c > moda_freq or (c == moda_freq and v > moda_valor):
            moda_valor = v
            moda_freq = c

    return moda_valor

def calcular_varianza_poblacional(values: list[float]) -> float:
    """Calcula la varianza poblacional (divide entre N)."""
    total = 0.0
    n = 0
    for v in values:
        total += v
        n += 1

    mean = total / n

    ss = 0.0
    for v in values:
        diff = v - mean
        ss += diff * diff

    if n < 2:
        return 0.0

    return ss / (n - 1)

def calcular_desv_estandar_poblacional(values: list[float]) -> float:
    """Calcula la desviación estándar poblacional."""
    return calcular_varianza_poblacional(values) ** 0.5

def leer_numeros(file_path: str) -> list[float]:
    """Lee números desde un archivo, uno por línea."""
    values: list[float] = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            text = line.strip()
            if not text:
                continue
            try:
                values.append(float(text))
            except ValueError:
                # Línea inválida
                print(f"Valor no valido {text}")
                continue

    return values

def build_output(stats: dict [str,float], elapsed: float) -> str:
    """Construye el texto de salida requerido."""
    return (
        f"{stats['count']} Count\n"
        f"{stats['promedio']} PROMEDIO\n"
        f"{stats['mediana']} MEDIANA\n"
        f"{stats['moda']} MODA\n"
        f"{stats['desv_std_pobl']} DESV ESTA POBLACIONAL\n"
        f"{stats['var_pobl']} VARIANZA POBLACIONAL\n"
        f"\nElapsedTimeSeconds\t{elapsed}"
    )

def calcular_promedio(values: list[float]) -> tuple [int,float]:
    """Hace el conteo total de elementos y calcula el promedio"""
    count = 0
    total_sum = 0.0
    for v in values:
        total_sum += v
        count += 1
    promedio = total_sum / count
    return count, promedio

def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "parameter_file",
        help="Path to the input file containing numbers."
    )
    args = parser.parse_args()
    start = time.perf_counter()
    values = leer_numeros(args.parameter_file)

    count , promedio = calcular_promedio(values)
    mediana = calcular_mediana(values)
    moda = calcular_moda(values)
    varianza_poblacional = calcular_varianza_poblacional(values)
    desv_estandar_poblacional = varianza_poblacional ** 0.5

    stats = {
    "count": count,
    "promedio": promedio,
    "mediana": mediana,
    "moda": moda,
    "desv_std_pobl": desv_estandar_poblacional,
    "var_pobl": varianza_poblacional,
    }
    elapsed = time.perf_counter() - start
    output_content = build_output(stats, elapsed)

    print(output_content)

    with open(f"ConvertionResults_{args.parameter_file}.txt",
               "w",
               encoding="utf-8") as out_file:
        out_file.write(output_content)

if __name__ == "__main__":
    main()
