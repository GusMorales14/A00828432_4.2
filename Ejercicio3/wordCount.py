# pylint: disable=invalid-name
"""Identify all distinct words and the frequency of them"""

import argparse
import time


def split_by_spaces_keep_blanks(text: str) -> list[str]:
    """
    Split text by spaces, keeping blank tokens.
    Equivalent to Excel-like behavior that produces (blank).
    """
    tokens = []
    current = []

    for ch in text:
        if ch == " ":
            tokens.append("".join(current))
            current = []
        else:
            current.append(ch)

    tokens.append("".join(current))
    return tokens


def count_words(file_path: str) -> dict[str, int]:
    """Count word frequencies from file, including blanks."""
    counts: dict[str, int] = {}

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            tokens = split_by_spaces_keep_blanks(line.rstrip("\n"))

            for token in tokens:
                word = token.strip().lower()

                if word == "":
                    key = "(blank)"
                else:
                    key = word

                counts[key] = counts.get(key, 0) + 1

    return counts

def ordenar_por_frecuencia_desc(items: list[tuple[str, int]]) -> list[tuple[str, int]]:
    """Ordena (word, freq) de mayor a menor frecuencia usando insertion sort."""
    sorted_items = items[:]

    for i in range(1, len(sorted_items)):
        key_word, key_freq = sorted_items[i]
        j = i - 1

        while j >= 0 and sorted_items[j][1] < key_freq:
            sorted_items[j + 1] = sorted_items[j]
            j -= 1

        sorted_items[j + 1] = (key_word, key_freq)

    return sorted_items

def build_output(counts: dict[str, int], elapsed: float) -> str:
    """Build output text ordered by frequency (desc)."""
    lines = []

    # convertir dict a lista de tuplas
    items = []
    total = 0
    for word, freq in counts.items():
        items.append((word, freq))
        total += freq

    # ordenar por frecuencia descendente
    ordered_items = ordenar_por_frecuencia_desc(items)

    # header
    lines.append("Row Labels\tCount")

    for word, freq in ordered_items:
        lines.append(f"{word}\t{freq}")

    lines.append(f"Grand Total\t{total}")
    lines.append("")
    lines.append(f"ElapsedTimeSeconds\t{elapsed}")

    return "\n".join(lines)


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser()
    parser.add_argument("parameter_file", help="Input file with words")
    args = parser.parse_args()

    start = time.perf_counter()
    counts = count_words(args.parameter_file)
    elapsed = time.perf_counter() - start

    output_text = build_output(counts, elapsed)

    print(output_text)

    with open(f"ConvertionResults_{args.parameter_file}.txt",
               "w",
               encoding="utf-8") as out_file:
        out_file.write(output_text)


if __name__ == "__main__":
    main()
