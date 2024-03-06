import textwrap
from .question import Question, NoSolveQuestion

__all__ = [
    "problem_1",
    "problem_2a",
    "problem_2b",
    "problem_3",
    "problem_3b",
    "problem_3c",
    "problem_3d",
    "problem_4a",
    "problem_4b",
]

problem_1 = NoSolveQuestion(
    hint=textwrap.dedent(
        """
        Have a look at the documentation of krotov's
        [Objective class](https://qucontrol.github.io/krotov/v1.2.1/API/krotov.objectives.html#krotov.objectives.Objective).

        You will not need to specify the `c_ops` argument!
        The first three arguments are enough.
        """
    ),
    solution_message=textwrap.dedent(
        """
        ```python
        objective = [krotov.Objective(initial_state=ket1, target=ket3, H=H)]
        ```
        """
    ),
)


problem_2a = NoSolveQuestion(
    solution_message=textwrap.dedent(
        """
        A good parameter for `t_rise` is on the order of 1.0

        ```python
        def update_shape(t):
            return krotov.shapes.flattop(t, 0.0, 5.0, t_rise=1.0, func='sinsq')
        ```
        """
    ),
    hint=textwrap.dedent(
        """
        """
    ),
)

problem_2b = NoSolveQuestion(
    hint=textwrap.dedent(
        """
        Remember: the update is proportional to $1/{\lambda_a}$
        """
    ),
    solution_message=textwrap.dedent(
        """
        A parameter that works reasonably well is

        ```python
        lambda_a = 1
        ```
        """
    ),
)


problem_3 = NoSolveQuestion(
    solution_message=textwrap.dedent(
        """
        ```python
        oct_result = krotov.optimize_pulses(
            objective,
            pulse_options=pulse_options,
            tlist=tlist,
            propagator=krotov.propagators.expm,
            #
            chi_constructor=krotov.functionals.chis_ss,
            #
            info_hook=krotov.info_hooks.print_table(
                J_T=krotov.functionals.J_T_ss,
                unicode=True,
            ),
            check_convergence=krotov.convergence.Or(
                krotov.convergence.value_below(1e-2,
                name="J_T"),
                krotov.convergence.delta_below(1e-16),
                krotov.convergence.check_monotonic_error,
            ),
            iter_stop=50,
        )
        ```
        """
    ),
    hint=textwrap.dedent(
        """
        """
    ),
)

problem_3b = NoSolveQuestion(
    hint=textwrap.dedent(
        """
        Does the phase of the final state matter?
        """
    ),
)

problem_3c = NoSolveQuestion(
    hint=textwrap.dedent(
        """
        A fidelity (1-$J_{\mathrm{T}}$) of 99.9% is quite good.
        The steps should also be adjusted, to not wait longer than
        2 min (for this first guess). Maybe give it a try and see how long
        a few steps take
        """
    ),
)

problem_3d = NoSolveQuestion(
    hint=textwrap.dedent(
        """
        We give the `pulse_options` to krotov, which take some arguments
        that can be changed and we also have `tlist`, which we can also
        vary. Also the parameters of the system can dramatically change the
        result of the initial guess and therefore also the optimization
        behavior. And now that you say it: The initial guess...
        """
    ),
)


problem_4a = NoSolveQuestion(
    solution_message=textwrap.dedent(
        """
        ```python
        opt_dynamics = oct_result.optimized_objectives[0].mesolve(tlist, e_ops=[proj1, proj2, proj3])
        ```
        """
    ),
    hint=textwrap.dedent(
        """
        Have a look at the optimized objectives
        (oct_result.optimized_objectives). And don't forget that you always
        have a list of objectives
        """
    ),
)

problem_4b = NoSolveQuestion(
    solution_message=textwrap.dedent(
        """
        Pump pulse:
        ```python
        print("Pump pulse amplitude and phase:")
        plot_pulse_amplitude_and_phase(
            oct_result.optimized_controls[0],
            oct_result.optimized_controls[1],
            tlist
        )
        ```

        Stokes pulse:
        ```python
        print("Stokes pulse amplitude and phase:")
        plot_pulse_amplitude_and_phase(
            oct_result.optimized_controls[2],
            oct_result.optimized_controls[3],
            tlist
        )
        ```
        """
    ),
    hint=textwrap.dedent(
        """
        You can access the i'th optimized control via

        ```python
        oct_result.optimized_controls[i]
        ```
        """
    ),
)
