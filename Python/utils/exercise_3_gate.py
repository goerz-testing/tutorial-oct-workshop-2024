from textwrap import dedent
from .question import NoSolveQuestion

problem_1 = NoSolveQuestion(
    hint=dedent(
        r"""
        * When taking the derivative, you can treat $\ket{\Psi_k(T)}$ and
            $\bra{\Psi_k(T)}$ as independent variables. The proper mathematical
            footing for this (a) matrix calculus, which tells us that the
            derivative of a scalar function w.r.t. a row vector is a column vector
            of the component-wise derivatives, and (b) the definition of "Wirtinger
            derivatives", which justify treating a complex variable `z` and its
            complex conjugate `z*` as independent. So the derivative of a scalar
            function w.r.t. a bra-state (a row vector) is the ket (column vector)
            with the componentwise derivatives w.r.t. the complex conjugate
            elements of $\Psi_k$.
        * Make sure you get the sign right. The definition of $\ket{\chi_k}$
            includes a minus sign, but $J_T$ also is 1 minus the fidelity. These
            two minuses cancel.
        * Be careful about the definition of $\tau$ and where $\tau$
            respectively the complex conjugate $\tau^*$ appears.
        """
    ),
    solution_message=dedent(
        r"""
        ```python
        def chi_constructor(fw_states_T, objectives, **kwargs):
            τ = np.array([fw_states_T[k].overlap(objectives[k].target) for k in range(4)])
            α = τ.conjugate().sum() / 16
            chi_states = []
            for k in range(4):
                chi_states.append(
                    α * objectives[k].target
                )
            return chi_states
        ```
        """
    ),
)

problem_2 = NoSolveQuestion(
    hint=dedent(
        r"""
        What kind of functions can be calculate derivatives of?
        """
    ),
    solution_message=dedent(
        r"""
        The functional contains several non-analytic functions:

        * The `eigvals` in the `c1c2c3`
        * The branch selection and sorting
        * The `max` function in `concurrence`

        None of these are functions where we can write out a derivative by hand.
        """
    ),
)
