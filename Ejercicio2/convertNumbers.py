# pylint: disable=invalid-name
"""Converter numbers input from a file and converts them to binary and hex"""
import argparse
import time

BIN_NEG_BITS = 10
HEX_NEG_BITS = 40  # 10 hex digits


def to_base_unsigned(n: int, base: int) -> str:
    """Convert non-negative integer n to base (2..16) without using bin/hex/format."""
    digits = "0123456789ABCDEF"

    if n == 0:
        return "0"

    result = []
    while n > 0:
        result.append(digits[n % base])
        n //= base

    result.reverse()
    return "".join(result)


def left_pad(s: str, width: int, pad_char: str = "0") -> str:
    """Left pad s to width."""
    if len(s) >= width:
        return s
    return (pad_char * (width - len(s))) + s


def to_binary(value: int) -> str:
    """Binary conversion with 2's complement for negatives (10 bits)."""
    if value >= 0:
        return to_base_unsigned(value, 2)

    unsigned_val = value % (1 << BIN_NEG_BITS)
    raw = to_base_unsigned(unsigned_val, 2)
    return left_pad(raw, BIN_NEG_BITS, "0")


def to_hex(value: int) -> str:
    """Hex conversion with 2's complement for negatives (10 hex digits = 40 bits)."""
    if value >= 0:
        return to_base_unsigned(value, 16)

    unsigned_val = value % (1 << HEX_NEG_BITS)
    raw = to_base_unsigned(unsigned_val, 16)
    return left_pad(raw, HEX_NEG_BITS // 4, "0")


def main() -> None:
    """Program entry point."""
    parser = argparse.ArgumentParser()
    parser.add_argument("parameter_file", help="Input file with one item per line")
    args = parser.parse_args()
    print(args.parameter_file)
    start = time.perf_counter()

    output_lines = ["ITEM\tDEC\tBIN\tHEX"]
    invalid_count = 0
    item_no = 1

    with open(args.parameter_file, "r", encoding="utf-8") as file:
        for line in file:
            text = line.strip()
            if not text:
                continue

            try:
                number = int(text)
            except ValueError:
                invalid_count += 1
                print(f"ERROR: invalid data '{text}' (item {item_no})")
                output_lines.append(f"{item_no}\t{text}\t#VALUE!\t#VALUE!")
                item_no += 1
                continue

            bin_str = to_binary(number)
            hex_str = to_hex(number)
            output_lines.append(f"{item_no}\t{number}\t{bin_str}\t{hex_str}")
            item_no += 1

    elapsed = time.perf_counter() - start
    output_lines.append("")
    output_lines.append(f"ElapsedTimeSeconds\t{elapsed}")
    output_lines.append(f"InvalidItems\t{invalid_count}")

    out_text = "\n".join(output_lines)
    print(out_text)

    with open(f"ConvertionResults_{args.parameter_file}.txt",
               "w",
               encoding="utf-8") as out_file:
        out_file.write(out_text)


if __name__ == "__main__":
    main()
