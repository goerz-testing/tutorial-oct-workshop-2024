from textwrap import dedent
from .question import NoSolveQuestion

problem_0 = NoSolveQuestion(
    hint=dedent(
        r"""
        Start varying parameters to get close to a population of 1 in state $\ket{1}$.
        Find an order-of-magnitude value for each free parameter. Then iterate over
        the parameters and bisect the value for each parameter to refine the value.
        """
    ),
    solution_message=dedent(
        r"""
        A reasonably good set of parameters obtained by hand might be this:

        ```python
        evolve_and_plot_parameterized_pulse(E_0=0.92,ΔT=8.0)
        ```
        """
    ),
)


problem_1 = NoSolveQuestion(
    hint=dedent(
        r"""
        The upper bounds are given in the description! For the other parameters,
        you can use for example the parameters from the guess pulse.
        """
    ),
    solution_message=dedent(
        r"""
        ```python
        bounds_lower = [0,0]
        bounds_upper = [10.0, T]
        guess = [0.5, 5.0]
        ```
        """
    ),
)
