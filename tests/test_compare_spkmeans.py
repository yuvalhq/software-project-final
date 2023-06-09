from pathlib import Path
from typing import List

import numpy as np
import pytest
from testutils import read_matrix_from_file, read_vector_and_matrix_from_file

import mykmeanssp

Matrix = List[List[float]]
TESTS_COUNT = 10

compare_input_output_test = pytest.mark.parametrize(
    "inputs_folder, output_folder",
    [
        (
            str(Path(__file__).parent.joinpath("testfiles").resolve()),
            str(Path(__file__).parent.joinpath("testfiles/ofek_s").resolve()),
        ),
        (
            str(Path(__file__).parent.joinpath("testfiles").resolve()),
            str(Path(__file__).parent.joinpath("testfiles/sophie").resolve()),
        ),
    ],
)


@compare_input_output_test
def test_wam(inputs_folder: str, output_folder: str):
    for i in range(1, TESTS_COUNT + 1):
        our_mat = read_matrix_from_file(
            str(Path(inputs_folder).joinpath(f"test{i}.txt"))
        )

        our_wam = mykmeanssp.wam(our_mat)
        other_wam = read_matrix_from_file(
            str(Path(output_folder).joinpath(f"test{i}_wam.txt"))
        )
        np.testing.assert_almost_equal(our_wam, other_wam, decimal=4)


@compare_input_output_test
def test_ddg(inputs_folder: str, output_folder: str):
    for i in range(1, TESTS_COUNT + 1):
        our_mat = read_matrix_from_file(
            str(Path(inputs_folder).joinpath(f"test{i}.txt"))
        )

        our_ddg = mykmeanssp.ddg(our_mat)
        other_ddg = read_matrix_from_file(
            str(Path(output_folder).joinpath(f"test{i}_ddg.txt"))
        )
        np.testing.assert_almost_equal(our_ddg, other_ddg, decimal=4)


@compare_input_output_test
def test_gl(inputs_folder: str, output_folder: str):
    for i in range(1, TESTS_COUNT + 1):
        our_mat = read_matrix_from_file(
            str(Path(inputs_folder).joinpath(f"test{i}.txt"))
        )

        our_gl = mykmeanssp.gl(our_mat)
        other_gl = read_matrix_from_file(
            str(Path(output_folder).joinpath(f"test{i}_gl.txt"))
        )
        np.testing.assert_almost_equal(our_gl, other_gl, decimal=4)


@compare_input_output_test
def test_jacobi(inputs_folder: str, output_folder: str):
    for i in range(1, TESTS_COUNT + 1):
        our_mat = read_matrix_from_file(
            str(Path(inputs_folder).joinpath(f"test{i}_j.txt"))
        )

        our_eigenvectors, our_eigenvalues = mykmeanssp.jacobi(our_mat)
        other_eigenvalues, other_eigenvectors = read_vector_and_matrix_from_file(
            str(Path(output_folder).joinpath(f"test{i}_j_ans.txt"))
        )
        np.testing.assert_almost_equal(
            np.array(our_eigenvectors).T, other_eigenvectors, decimal=4
        )
        np.testing.assert_almost_equal(our_eigenvalues, other_eigenvalues, decimal=4)
