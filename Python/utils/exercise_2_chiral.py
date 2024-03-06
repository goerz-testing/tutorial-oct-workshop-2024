from textwrap import dedent
from .question import NoSolveQuestion

problem_0 = NoSolveQuestion(
    hint=dedent(
        r"""
        Start varying parameters to get close to the target pulse. Find an
        order-of-magnitude value for each free parameter. Then iterate over the
        parameters and bisect the value for each parameter to refine the value.
        """
    ),
    solution_message=dedent(
        r"""
        A reasonably good set of parameters obtain by hand might be this:

        ```python
        plot_parameterised_pulse(E0=23,a=7.5,t_start=0.325,t_stop=0.665)
        ```
        """
    ),
)


problem_1 = NoSolveQuestion(
    hint=dedent(
        r"""
        The upper bounds are given in the description! For the pulse durations,
        we're not taking into account that ideally, they should sum up to 1
        (this is not a strict requirement), so take that into account and choose
        guesses that sum up to slightly less than 1 (giving each pulse duration
        room to expand a bit). For the other parameters, starting halfway
        between the minimum and maximum value might be a good idea.
        """
    ),
    solution_message=dedent(
        r"""
        ```python
        bounds_lower = [0,0,0, 0,0,0, 0,0,0]
        bounds_upper = [1.0, 1.0,1.0, 2*pi,2*pi,2*pi, 10.0, 10.0, 10.0]
        guess = [0.2,0.4,0.3, pi, pi, pi, 5.0, 5.0, 5.0]
        ```
        """
    ),
)
