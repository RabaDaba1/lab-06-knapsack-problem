import os.path

import numpy as np
import pytest
from typing import List
from saport.knapsack.model import Problem, Item, Solution
from saport.knapsack.solvers.greedy import DensityHeuristic, GreedySolver, Heuristic, ValueHeuristic, WeightHeuristic

TEST_DIR = "knapsack_problems"
TIMEOUT = 5000


def get_problem(name: str) -> Problem:
    return Problem.from_path(os.path.join(TEST_DIR, name))

def indented_string(s: str, ident: str = '    '):
    return '\n'.join([ident + l for l in s.splitlines()])

class TestGreedyKnapsackSolvers:

    @pytest.mark.parametrize("heuristic, cases", [
        (ValueHeuristic(), [(1, -3, -3), (3, 0, 0), (0, 8, 8)]), 
        (WeightHeuristic(), [(-5, 3, 5), (0, 3, 0), (9, 0, -9)]), 
        (DensityHeuristic(), [(2, -4, -4/2), (3, 0, 0/3), (-5, 2, 2/-5), (5, 9, 9/5)])
    ])
    def test_greedy_heuristic_should_be_properly_implemented(
            self, heuristic: Heuristic, cases):

        for test_weight, test_value, expected in cases:
            got = heuristic(Item(0, test_value, test_weight))
            assert got == expected,\
                f"heuristic {heuristic.__class__.__name__} provides an incorrect estimate:" +\
                f"\n- got: {got}" +\
                f"\n- expected: {expected}" +\
                f"\n- for item with value: {test_value} and weight: {test_weight}"


    @pytest.mark.parametrize("problem_name,expected_items", [
        ('ks_lecture_dp_1', [2, 1]),
        ('ks_lecture_dp_2', [3, 0]),
        ('ks_30_0', [28, 26, 24, 22, 20, 18, 16, 14]),
        ('ks_45_0', [44, 37, 31, 40, 36, 42, 14, 30, 24, 19, 29, 15, 18, 27, 34, 16, 17, 25, 35, 20]),
        ('ks_50_1', [39, 22, 47, 25, 46, 24, 34, 38, 30, 32, 29, 49, 20, 17, 28, 44, 27, 43, 48, 19])
    ])
    def test_greedy_solver_should_solve_example_knapsack_problems_with_different_heuristics(
            self, problem_name: str, expected_items: List[int]):
        
        class DummyHeuristic(Heuristic):
            def __call__(self, item: Item) -> float:
                return item.index / item.value

        problem = get_problem(problem_name)
        solver = GreedySolver(problem, TIMEOUT, [DummyHeuristic()])
        got = solver._solve_using_heuristic(DummyHeuristic())
        expected = Solution.from_items([problem.items[i] for i in expected_items])
        assert got.is_equivalent(expected), f"failed to correctly solve `{problem_name}`:" +\
            f"\n- got: \n{indented_string(str(got))}" +\
            f"\n- expected: \n{indented_string(str(expected))}"