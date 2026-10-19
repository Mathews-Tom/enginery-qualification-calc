from __future__ import annotations

import subprocess
import sys
import unittest


def run(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "calc", *arguments], capture_output=True, text=True, check=False
    )


class CliTests(unittest.TestCase):
    def test_prints_the_result(self) -> None:
        completed = run("2+3*4")
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(completed.stdout, "14\n")
        self.assertEqual(completed.stderr, "")

    def test_invalid_expression_exits_2_with_message(self) -> None:
        completed = run("2 $ 3")
        self.assertEqual(completed.returncode, 2)
        self.assertEqual(completed.stdout, "")
        self.assertTrue(completed.stderr.startswith("error: "))

    def test_division_by_zero_exits_2_with_message(self) -> None:
        for source in ("1/0", "1/(2-2)", "0/0", "1/0.0"):
            with self.subTest(source=source):
                completed = run(source)
                self.assertEqual(completed.returncode, 2)
                self.assertEqual(completed.stdout, "")
                self.assertEqual(completed.stderr, "error: division by zero\n")

    def test_valid_division(self) -> None:
        completed = run("1/4")
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(completed.stdout, "0.25\n")

    def test_usage_without_expression(self) -> None:
        completed = run()
        self.assertEqual(completed.returncode, 2)
        self.assertIn("usage:", completed.stderr)


if __name__ == "__main__":
    unittest.main()
