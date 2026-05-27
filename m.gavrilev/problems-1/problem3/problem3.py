#!/usr/bin/env python3

from collections.abc import Iterator


def collatz_chain(start_number: int) -> Iterator[int]:
    if start_number <= 0:
        raise ValueError(f"expected positive integer, got {start_number}")

    current_number: int = start_number
    yield current_number
    while current_number != 1:
        if current_number % 2 == 0:
            current_number //= 2
        else:
            current_number = 3 * current_number + 1

        yield current_number


def print_collatz_chain(number: int) -> None:
    chain: Iterator[int] = collatz_chain(number)

    print(next(chain), end="")
    for value in chain:
        print(f" -> {value}", end="")

    print()


def main() -> None:
    number: int = int(input())
    print_collatz_chain(number)


if __name__ == "__main__":
    import sys

    try:
        main()
    except EOFError as e:
        print(f"EOFError: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("KeyboardInterrupt: interrupted", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)
