import sys
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import List, Optional

import numpy as np
from kmeanspp import kmeanspp

import mykmeanssp

Matrix = List[List[float]]


class Goal(Enum):
    SPK = auto()
    WAM = auto()
    DDG = auto()
    GL = auto()
    JACOBI = auto()

    @classmethod
    def from_lowercase_string(cls, goal_str: str) -> "Goal":
        return cls[goal_str.upper()]


@dataclass
class CommandLineArguments:
    k: Optional[int]
    goal: str
    file_path: Path


def handle_args() -> CommandLineArguments:
    if len(sys.argv) == 3:
        return CommandLineArguments(
            k=None,
            goal=Goal.from_lowercase_string(sys.argv[1]),
            file_path=Path(sys.argv[2]),
        )
    elif len(sys.argv) == 4:
        return CommandLineArguments(
            k=int(sys.argv[1]),
            goal=Goal.from_lowercase_string(sys.argv[2]),
            file_path=Path(sys.argv[3]),
        )
    sys.exit("An Error Has Ocurred")


def eigengap_heuristic(eigenvalues: List[float]) -> int:
    eigenvalues_sorted = np.sort(eigenvalues)
    deltas = np.abs(np.diff(eigenvalues_sorted))
    return np.argmax(deltas)


def read_matrix_from_file(file_path: Path) -> Matrix:
    result = []
    with open(file_path, "r") as fd:
        for line in fd.readlines():
            row = [float(x) for x in line.split(",")]
            result.append(row)
    return result


def print_matrix(matrix: Matrix) -> None:
    for row in matrix:
        print(",".join(format(x, '.4f') for x in row))
    print()


def spk(matrix: Matrix, k: Optional[int]) -> Matrix:
    gl = mykmeanssp.gl(matrix)
    eigenvectors, eigenvalues = mykmeanssp.jacobi(gl)
    k = k or eigengap_heuristic(eigenvalues)
    transposed_eigenvectors_np = np.array(eigenvectors).T
    result = kmeanspp(transposed_eigenvectors_np, k)
    return result.tolist()


def main():
    goal_map = {
        Goal.WAM: mykmeanssp.wam,
        Goal.DDG: mykmeanssp.ddg,
        Goal.GL: mykmeanssp.gl,
        Goal.JACOBI: mykmeanssp.jacobi,
    }
    np.random.seed(0)

    cmd_args = handle_args()
    input_matrix = read_matrix_from_file(cmd_args.file_path)
    if cmd_args.goal == Goal.SPK:
        output = spk(input_matrix, cmd_args.k)
    else:
        output = goal_map[cmd_args.goal](input_matrix)
    print_matrix(output)


if __name__ == "__main__":
    main()