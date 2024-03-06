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
        The Stokes and Pump pulse are in the wrong order! Try setting `t_p=50` and `t_s=-50`. Leave the other parameters at `σ_p = 50`, `σ_s = 50`, `Δ = 1`, `d_12 = 25`, `d_23 = 25`.
        """
    ),
    hint=dedent(
        r"""
        Look at the ordering of the pulses!
        """
    ),
)
