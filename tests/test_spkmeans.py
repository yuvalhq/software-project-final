from typing import List

import numpy as np
import pytest

import spkmeans_c

Matrix = List[List[float]]


@pytest.mark.parametrize(
    "matrix, expected_eigenvalues, expected_eigenvectors",
    [
        (
            [[1.0, 2.0, 3.0], [2.0, 3.0, 11.0], [3.0, 11.0, 5.0]],
            [0.186, -7.084, 15.898],
            [[0.97, -0.211, -0.122], [0.071, 0.725, -0.685], [0.233, 0.656, 0.718]],
        ),
        (
            [[3.0, 2.0, 4.0], [2.0, 0.0, 2.0], [4.0, 2.0, 3.0]],
            [-1.0, -1.0, 8.0],
            [
                [0.7071, 0.0000, -0.7071],
                [-0.2357, 0.9428, -0.2357],
                [0.6667, 0.3333, 0.6667],
            ],
        ),
    ],
)
def test_jacobi_algorithm(
    matrix: Matrix, expected_eigenvalues: List[float], expected_eigenvectors: Matrix
):
    actual_eigenvectors, actual_eigenvalues = spkmeans_c.jacobi(matrix)
    np.testing.assert_almost_equal(expected_eigenvalues, actual_eigenvalues, decimal=3)
    np.testing.assert_almost_equal(
        expected_eigenvectors, actual_eigenvectors, decimal=3
    )