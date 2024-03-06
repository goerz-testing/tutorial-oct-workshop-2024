from textwrap import dedent
from .question import NoSolveQuestion


"""
import matplotlib.pyplot as plt  # for plotting
import numpy as np               # for numerics
import qutip                     # for quantum mechanics
from numpy import pi, sqrt, exp, sin, cos
"""

problem_1 = NoSolveQuestion(
    solution_message=dedent(
        r"""
        A guess that will take you to 99 % fidelity is `guess=[30,-30, 50,50, 25,25]`
        """
    ),
    hint=dedent(
        r"""
        Try starting from something like `guess=[10,-10, 30,60, 50,50]`
        """
    ),
)
