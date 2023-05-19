import math
import os.path

import numpy as np
import pytest
from pytest_mock import MockerFixture
from typing import List
from saport.knapsack.model import Problem, Item, Solution
from saport.knapsack.solvers.bnb_dfs import BnbDFSSolver

TEST_DIR = "knapsack_problems"
TIMEOUT = 5000


def get_problem(name: str) -> Problem:
    return Problem.from_path(os.path.join(TEST_DIR, name))

def indented_string(s: str, ident: str = '    '):
    return '\n'.join([ident + l for l in s.splitlines()])

class TestBranchAndBoundKnapsackSolver:


    @pytest.mark.parametrize("problem_name, left_items, solution_items, expected", [
        ('ks_lecture_dp_1', [0, 1, 2], [], 11.6),
        ('ks_lecture_dp_1', [1, 2], [0], 11.6),
        ('ks_lecture_dp_1', [2], [0, 1], 11.0),
        ('ks_lecture_dp_1', [2], [0], 8.0),
        ('ks_lecture_dp_1', [1, 2], [], 9.0),
        ('ks_lecture_dp_2', [0, 1, 2, 3], [], 46.5),
        ('ks_lecture_dp_2', [1, 2, 3], [0], 46.5),
        ('ks_lecture_dp_2', [2, 3], [0, 1], 46.5),
        ('ks_lecture_dp_2', [3], [0, 1], 46.2),
        ('ks_lecture_dp_2', [2, 3], [0], 44.6),
        ('ks_lecture_dp_2', [3], [0, 2], 44.6),
        ('ks_lecture_dp_2', [3], [0], 44.0),
        ('ks_lecture_dp_2', [1, 2, 3], [], 42.0)
    ])
    def test_bnb_solver_should_properly_evaluate_upper_bound_for_given_lists_of_items_and_solutions(
            self, problem_name, left_items: List[int], solution_items: List[int], expected: float):
        problem = get_problem(problem_name)
        solver = BnbDFSSolver(problem, timelimit=TIMEOUT)
        solution = Solution.from_items([problem.items[i] for i in solution_items])
        left = [problem.items[i] for i in left_items]
        got = solver._upper_bound(left, solution)

        assert math.isclose(got, expected), \
            f"upper bound is not calculated correctly for problem `{problem_name}`" +\
            f"\n- got: {got}" +\
            f"\n- expected: {expected}" +\
            f"\n- for left items with indices: {left_items}"

    @pytest.mark.parametrize('problem_name, expected_solution_items, pure_dfs_calls, expected_dfs_calls, expected_upper_bound_calls', [
        ('ks_lecture_dp_1', [0, 1], 14, 6, 5),
        ('ks_lecture_dp_2', [0, 3], 23, 12, 8),
        ('ks_30_0', [2, 4, 6, 8, 10, 12, 14, 16, 24], 57191, 57159, 44136)
    ])
    def test_bnb_solver_should_solve_example_knapsack_problems_having_correct_upper_bound_function(
            self, mocker: MockerFixture, problem_name: str, 
            pure_dfs_calls: int, expected_dfs_calls: int, expected_upper_bound_calls: int, expected_solution_items: List[int],):
        problem = get_problem(problem_name)
        solver = BnbDFSSolver(problem, timelimit=TIMEOUT)
        expected_solution = Solution.from_items([problem.items[i] for i in expected_solution_items], True)
        dfs_spy = mocker.spy(obj=solver, name="_dfs_bnb")
        bound_spy = mocker.spy(obj=solver, name="_upper_bound")

        got_solution = solver.solve()
        assert got_solution.is_equivalent(expected_solution), f"failed to correctly solve `{problem_name}`:" +\
                f"\n- got: \n{indented_string(str(got_solution))}" +\
                f"\n- expected: \n{indented_string(str(expected_solution))}"

        assert dfs_spy.call_count < pure_dfs_calls, f"branch and bound failed to prune the tree:" +\
            f"\n- `_dsf_bnb` has been run {dfs_spy.call_count} times" +\
            f"\n- pure `dsf` without bnb would be run {pure_dfs_calls} times"

        assert dfs_spy.call_count <= expected_dfs_calls, f"branch and bound has not prune tree enough:" +\
            f"\n- `_dsf_bnb` has been run {dfs_spy.call_count} times" +\
            f"\n- correct implementation would be called just {expected_dfs_calls} times"

        assert 0 < bound_spy.call_count <= expected_upper_bound_calls, f"upper bound method is not used correctly:" +\
            f"\n- `_upper_bound` has been run {bound_spy.call_count} times" +\
            f"\n- correct implementation would be called just {expected_upper_bound_calls} times"
