#!/usr/bin/env python3

import io
import random
import unittest
from collections.abc import Iterator
from contextlib import redirect_stdout

from problem3 import collatz_chain, print_collatz_chain


def assert_collatz_steps(test_case: unittest.TestCase, chain: list[int]) -> None:
    for current, next_value in zip(chain, chain[1:]):
        if current % 2 == 0:
            test_case.assertEqual(next_value, current // 2)
        else:
            test_case.assertEqual(next_value, 3 * current + 1)


class TestCollatzChainBasic(unittest.TestCase):
    def test_example_for_three(self) -> None:
        chain: list[int] = list(collatz_chain(3))

        self.assertEqual(chain, [3, 10, 5, 16, 8, 4, 2, 1])

    def test_one_is_single_value_chain(self) -> None:
        self.assertEqual(list(collatz_chain(1)), [1])

    def test_power_of_two_halves_until_one(self) -> None:
        self.assertEqual(list(collatz_chain(32)), [32, 16, 8, 4, 2, 1])

    def test_short_known_chains(self) -> None:
        self.assertEqual(list(collatz_chain(2)), [2, 1])
        self.assertEqual(list(collatz_chain(5)), [5, 16, 8, 4, 2, 1])
        self.assertEqual(list(collatz_chain(6)), [6, 3, 10, 5, 16, 8, 4, 2, 1])


class TestCollatzChainInvariants(unittest.TestCase):
    def test_chain_starts_with_input_and_ends_with_one(self) -> None:
        chain: list[int] = list(collatz_chain(27))

        self.assertGreater(len(chain), 0)
        self.assertEqual(chain[0], 27)
        self.assertEqual(chain[-1], 1)

    def test_every_step_follows_collatz_rule(self) -> None:
        chain: list[int] = list(collatz_chain(19))

        assert_collatz_steps(self, chain)

    def test_all_values_are_positive(self) -> None:
        chain: list[int] = list(collatz_chain(871))

        self.assertTrue(all(value > 0 for value in chain))

    def test_known_chain_for_twenty_seven(self) -> None:
        chain: list[int] = list(collatz_chain(27))

        self.assertEqual(chain[-1], 1)
        self.assertEqual(max(chain), 9232)
        self.assertEqual(len(chain) - 1, 111)

    def test_chain_is_lazy_iterator(self) -> None:
        chain: Iterator[int] = collatz_chain(3)

        self.assertIs(iter(chain), chain)
        self.assertEqual(next(chain), 3)
        self.assertEqual(next(chain), 10)
        self.assertEqual(next(chain), 5)


class TestPrintCollatzChain(unittest.TestCase):
    def test_prints_example_chain(self) -> None:
        output: io.StringIO = io.StringIO()

        with redirect_stdout(output):
            print_collatz_chain(3)

        self.assertEqual(output.getvalue(), "3 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1\n")

    def test_prints_one_without_separator(self) -> None:
        output: io.StringIO = io.StringIO()

        with redirect_stdout(output):
            print_collatz_chain(1)

        self.assertEqual(output.getvalue(), "1\n")


class TestCollatzChainRandom(unittest.TestCase):
    def test_large_random_numbers_follow_invariants(self) -> None:
        rng: random.Random = random.Random(146)

        for _ in range(300):
            number: int = rng.randint(1, 100_000)
            chain: list[int] = list(collatz_chain(number))

            self.assertGreater(len(chain), 0)
            self.assertEqual(chain[0], number)
            self.assertEqual(chain[-1], 1)
            self.assertTrue(all(value > 0 for value in chain))
            assert_collatz_steps(self, chain)


class TestCollatzChainErrors(unittest.TestCase):
    def test_zero_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            list(collatz_chain(0))

    def test_negative_number_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            list(collatz_chain(-5))


if __name__ == "__main__":
    unittest.main()
