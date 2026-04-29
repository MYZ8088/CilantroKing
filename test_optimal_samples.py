import tempfile
import unittest
from pathlib import Path

from optimal_samples import Problem, save_result, solve_problem, verify_solution


class PdfExampleTests(unittest.TestCase):
    def assert_solver_example(self, n: int, k: int, j: int, s: int, expected_at_most: int) -> None:
        problem = Problem(45, n, k, j, s)
        result = solve_problem(problem, tuple(range(1, n + 1)), time_limit=10)
        self.assertTrue(verify_solution(problem, result.index_blocks))
        self.assertLessEqual(len(result.blocks), expected_at_most)

    def test_n15_and_n16_smoke_examples(self) -> None:
        examples = [
            (15, 7, 6, 3, 2),
            (16, 7, 7, 3, 2),
        ]
        for n, k, j, s, expected_at_most in examples:
            with self.subTest(n=n, k=k, j=j, s=s):
                self.assert_solver_example(n, k, j, s, expected_at_most)


class DatabaseFileTests(unittest.TestCase):
    def test_save_result_uses_pdf_filename_shape(self) -> None:
        problem = Problem(45, 15, 7, 6, 3)
        result = solve_problem(problem, tuple(range(1, 16)), time_limit=10)
        with tempfile.TemporaryDirectory() as directory:
            path = save_result(result, Path(directory), run_number=2)
            self.assertEqual(path.name, f"45-15-7-6-3-2-{len(result.blocks)}.txt")
            content = path.read_text(encoding="utf-8")
            self.assertIn("An Optimal Samples Selection System", content)
            self.assertIn("selected_n_samples=1,2,3,4,5,6,7,8,9,10,11,12,13,14,15", content)


if __name__ == "__main__":
    unittest.main()