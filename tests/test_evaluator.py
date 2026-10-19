from __future__ import annotations

import unittest

from calc import CalcError, evaluate, format_number


class EvaluateTests(unittest.TestCase):
    def test_precedence(self) -> None:
        self.assertEqual(evaluate("2 + 3 * 4"), 14)
        self.assertEqual(evaluate("2 * 3 + 4"), 10)
        self.assertEqual(evaluate("10 - 4 - 3"), 3)
        self.assertEqual(evaluate("8 / 4 / 2"), 1)

    def test_parentheses_and_unary_minus(self) -> None:
        self.assertEqual(evaluate("(1 + 2) * 3"), 9)
        self.assertEqual(evaluate("-3 + 5"), 2)
        self.assertEqual(evaluate("-(2 + 3)"), -5)
        self.assertEqual(evaluate("--4"), 4)

    def test_decimals(self) -> None:
        self.assertAlmostEqual(evaluate("1.5 * 2"), 3.0)
        self.assertAlmostEqual(evaluate(".5 + .25"), 0.75)

    def test_power(self) -> None:
        self.assertEqual(evaluate("2^3"), 8)
        self.assertEqual(evaluate("2^3^2"), 512)
        self.assertEqual(evaluate("-2^2"), -4)
        self.assertEqual(evaluate("2*3^2"), 18)
        self.assertEqual(evaluate("(-2)^2"), 4)
        self.assertEqual(evaluate("2^-1"), 0.5)
        self.assertEqual(format_number(evaluate("4^0.5")), "2")

    def test_invalid_power(self) -> None:
        for source in ("2^", "^2", "0^-1", "(-8)^0.5"):
            with self.subTest(source=source), self.assertRaises(CalcError):
                evaluate(source)

    def test_invalid_expressions(self) -> None:
        for source in ("", "1 +", "(1 + 2", "1 2", "2 $ 3", ")"):
            with self.subTest(source=source), self.assertRaises(CalcError):
                evaluate(source)


class FormatTests(unittest.TestCase):
    def test_integral_values_have_no_fraction(self) -> None:
        self.assertEqual(format_number(14.0), "14")
        self.assertEqual(format_number(-5.0), "-5")

    def test_fractions_are_kept(self) -> None:
        self.assertEqual(format_number(0.75), "0.75")


if __name__ == "__main__":
    unittest.main()
