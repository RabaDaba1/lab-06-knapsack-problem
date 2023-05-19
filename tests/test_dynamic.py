import os.path

import numpy as np
import pytest
from typing import List
from saport.knapsack.model import Problem, Item, Solution
from saport.knapsack.solvers.dynamic import DynamicSolver

TEST_DIR = "knapsack_problems"
TIMEOUT = 5000


def get_problem(name: str) -> Problem:
    return Problem.from_path(os.path.join(TEST_DIR, name))

def indented_string(s: str, ident: str = '    '):
    return '\n'.join([ident + l for l in s.splitlines()])

class TestDynamicKnapsackSolver:

    @pytest.mark.parametrize("problem_name, expected_table", [
        ('ks_lecture_dp_1', [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 3], [0, 0, 0, 3], [0, 5, 5, 5], [0, 5, 6, 6], [0, 5, 6, 8], [0, 5, 6, 9], [0, 5, 6, 9], [0, 5, 11, 11]]),
        ('ks_lecture_dp_2', [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 16, 16, 16, 16], [0, 16, 19, 19, 19], [0, 16, 19, 23, 23], [0, 16, 35, 35, 35], [0, 16, 35, 39, 39], [0, 16, 35, 42, 44]])
    ])
    def test_dynamic_solver_should_properly_create_and_fill_table_for_example_knapsack_problems(self, problem_name: str, expected_table: List[List[int]]):
        problem = get_problem(problem_name)
        expected = np.array(expected_table)
        solver = DynamicSolver(problem, timelimit=TIMEOUT)
        solver.start_timer()
        got = solver._create_table()

        assert np.array_equal(got, expected), \
            f"got incorrect table for problem `{problem_name}`:" +\
            f"\n- got:\n{indented_string(str(got))}" +\
            f"\n- expected:\n{indented_string(str(expected))}"

    @pytest.mark.parametrize("problem_name, table_as_list, expected_items", [
        ('ks_lecture_dp_1', [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 3], [0, 0, 0, 3], [0, 5, 5, 5], [0, 5, 6, 6], [0, 5, 6, 8], [0, 5, 6, 9], [0, 5, 6, 9], [0, 5, 11, 11]], [1, 0]),
        ('ks_lecture_dp_2', [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 16, 16, 16, 16], [0, 16, 19, 19, 19], [0, 16, 19, 23, 23], [0, 16, 35, 35, 35], [0, 16, 35, 39, 39], [0, 16, 35, 42, 44]], [3, 0])
    ])
    def test_dynamic_solver_should_extract_proper_solution_from_correct_table(self, 
            problem_name: str, table_as_list: List[List[int]], expected_items: List[int]):
        table = np.array(table_as_list)
        problem = get_problem(problem_name)
        expected = Solution.from_items([problem.items[i] for i in expected_items], True)

        solver = DynamicSolver(problem, timelimit=TIMEOUT)
        solver.start_timer()
        got = solver._extract_solution(table.copy())
        
        assert got.is_equivalent(expected), "extracted an incorrect solution:" +\
            f"\n- got:\n{indented_string(str(got))}" +\
            f"\n- expected:\n{indented_string(str(expected))}" +\
            f"\n- from table:\n{indented_string(str(table))}"
