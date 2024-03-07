# Question class taken from the ELCH Tutorial notebooks at
# https://gitlabph.physik.fu-berlin.de/ag-koch/resources/elch_workshop_2020
# Originally designed by Matthias Krauss.

from IPython.display import display, Markdown, HTML
from textwrap import dedent, indent
import matplotlib


html_disp_style = '<p style="color:{c};font-size:20px;">{txt}</p>'


class QuestionDisplay(object):
    def __init__(self, header, txt, indent="", header_color="k"):
        self.header = header
        self.txt = txt
        self.indent = indent
        self.header_color = matplotlib.colors.to_hex(header_color)

    def __call__(self):
        display(
            HTML(html_disp_style.format(c=self.header_color, txt=self.header))
        )
        display(Markdown(indent(self.txt, self.indent)))


class Question(object):
    """Basic Question class for jupyter notebooks

    Provides the functionality to `check` the result, give `hint`s and the
    `solution` and prints the result nicely formatted in jupyter notebooks.

    Parameters
    ----------
    correct_answer : any type or callable
        The correct answer for this question.
        If the object is not callable, the answer is compared to the answer
        given to the `check` function.
        If a callable is given, the answer given to the `check` function will
        be passed onto the callable given here. It should return True to print
        `success_message` or False to print `fail_message`. Otherwise it won't
        print anything. This can for example be used to check if the answer is
        in the range (0,1), which could be solved by provide the function
        `lambda x: 0<x<1`.
    success_message : str or callable
        The message that should be displayed if the correct answer was given to
        `check`.
        If callable, it will be called if the check is True.
    fail_message : str or callable
        The message that should be displayed if the wrong answer was given to
        `check`.
        If callable, it will be called if the check is False.
    solution_message : str or callable, optional
        The message that should be displayed if the `solution` property is
        called.
        If callable, it will be called if the solution is requested.
    hint : str or list, optional
        The message that should be displayed if the `hint` property is called.
        If a list is given, the `hint` property can be called multiple times,
        each time revealing next hint from the list
    default : str, optional
        The default argument used to tell the student where to place the
        answer. This could be something like `"### answer here ###"` or
        anything else.
        If this message is provided to the `check` function, it will tell the
        student, that the dummy answer is still set.


    Examples
    --------
    >>> q = Question(
    ...     42, "yaaay!", "too bad...", "well... it's 42",
    ...     ["the answer to life...","the universe ...", "... and everything"]
    ... )

    which could then be used as

    >>> q.hint

    >>> q.hint

    >>> q.hint

    >>> q.check(1)

    >>> q.check(42)

    >>> q.solution

    """

    def __init__(
        self,
        correct_answer,
        success_message,
        fail_message,
        solution_message=None,
        hint=None,
        default=None,
    ):
        self.answer = correct_answer
        if solution_message is None:
            self.solution_msg = solution_message
        elif callable(solution_message):
            self.solution_msg = solution_message
        elif isinstance(solution_message, str):
            self.solution_msg = QuestionDisplay(
                "Solution:", solution_message, header_color="CornFlowerBlue"
            )
        else:
            raise TypeError(
                f"Type {type(solution_message)} for argument solution_message"
                "not supported"
            )

        if hint is None:
            self.hint_msg = hint
        elif isinstance(hint, list):
            self._hint_counter = 0
            self.hint_msg = [
                QuestionDisplay(
                    f"Hint {idx+1}:", hint, header_color="DarkGoldenRod"
                )
                for idx, hint in enumerate(hint)
            ]
        elif isinstance(hint, str):
            self.hint_msg = QuestionDisplay(
                "Hint:", hint, header_color="DarkGoldenRod"
            )
        else:
            raise TypeError(
                f"Type {type(hint)} for argument hint not supported"
            )

        if success_message is None:
            self.success = success_message
        elif callable(success_message):
            self.success = success_message
        elif isinstance(success_message, str):
            self.success = QuestionDisplay(
                "Success!", success_message, indent="> ", header_color="green"
            )
        else:
            raise TypeError(
                f"Type {type(success_message)} for argument success_message "
                "not supported"
            )

        if fail_message is None:
            self.failure = fail_message
        elif callable(fail_message):
            self.failure = fail_message
        elif isinstance(fail_message, str):
            self.failure = QuestionDisplay(
                "Not quite", fail_message, indent="> ", header_color="red"
            )
        else:
            raise TypeError(
                f"Type {type(fail_message)} for argument fail_message "
                "not supported"
            )

        self.default = default

    def check(self, val2check):
        """Routine to check the answer to this question.

        Prints to the jupyter notebook if the result is correct or not.

        Parameters
        ----------
        val2check : any type
            The answer to be checked.
        """
        if (self.default is not None) and (val2check == self.default):
            print("You still use the default value!")
            return

        if callable(self.answer):
            res = self.answer(val2check)
            if res is True:
                self.success()
            elif res is False:
                self.failure()
        else:
            if (val2check) == self.answer:
                self.success()
            else:
                self.failure()

    @property
    def solution(self):
        """Print solution of the question."""
        if self.solution_msg:
            self.solution_msg()
        else:
            print("No solution available!")

    @property
    def hint(self):
        """Print hint(s) of the question."""
        if isinstance(self.hint_msg, list):
            self._hint_counter += 1
            for idx, hint in enumerate(self.hint_msg[: self._hint_counter]):
                hint()
            if self._hint_counter < len(self.hint_msg):
                display(
                    HTML(
                        '<br><p style="color:Gray;font-size:12px;">'
                        ">There are still hints left. Evaluate the cell"
                        " again to show them.<</p>"
                    )
                )

        elif isinstance(self.hint_msg, QuestionDisplay):
            self.hint_msg()
        else:
            print("No hint available!")


class NoSolveQuestion(Question):
    """Subclass of `Question`, that only gives hints.

    Parameters
    ----------
    hint : str or list, optional
        The message that should be displayed if the `hint` property is called.
        If a list is given, the `hint` property can be called multiple times,
        each time revealing next hint from the list
    """

    def __init__(self, hint, solution_message=None):
        super().__init__(
            None, None, None, solution_message=solution_message, hint=hint
        )

    def check(self, val2check):
        raise AttributeError('"Check" is not implemented for this question')


###############################################################################


"""
import matplotlib.pyplot as plt  # for plotting
import numpy as np               # for numerics
import qutip                     # for quantum mechanics
from numpy import pi, sqrt, exp, sin, cos
"""

step1 = NoSolveQuestion(
    solution_message=dedent(
        r"""
        ```python
        t = np.linspace(-250, 250, 5000)
        ```
        """
    ),
    hint=dedent(
        r"""
        You can use NumPy's function `np.linspace()`, which needs the
        starting point, the end point and the number of gridpoints as
        arguments.
        """
    ),
)


step2 = NoSolveQuestion(
    solution_message=dedent(
        r"""
        ```python
        H1 = -1/2 * qutip.sigmaz()
        H2 = -1/2 * qutip.sigmax()
        ```
        """
    ),
    hint=dedent(
        r"""
        You can convert a NumPy array to a quantum object for example
        by writing `qutip.Qobj(np.array[1, 0])`.

        Alternatively you can write the Hamiltonian in terms of Pauli
        matrices, given by `qutip.sigmax()`, `qutip.sigmay()` and
        `qutip.sigmaz()`.
        """
    ),
)


step3 = NoSolveQuestion(
    solution_message=dedent(
        r"""
        ```python
        E0 = 1
        tau = 50
        alpha = 0.001

        Env = E0 * np.exp(-t**2/(2*tau**2))
        dphi = alpha * t
        ```
        """
    ),
    hint=dedent(
        r"""
        You can multiply to variables with the `*` operator,
        whereas `t**2` corresponds to "t to the power of two".

        The import statements above defined the short hand notation
        `cos`, `exp` etc. for the NumPy functions `np.cos`, `np.exp`.
        """
    ),
)


"""
H = [[H1, dphi], [H2, Env]]

def evaluate(H, time_index):
    (H1, dphi), (H2, Env) = H
    return dphi[time_index] * H1 + Env[time_index] * H2
"""

step4 = NoSolveQuestion(
    solution_message=dedent(
        r"""
        ```python
        psi0 = qutip.basis(2, 0)
        psi1 = qutip.basis(2, 1)
        ```
        """
    ),
    hint=dedent(
        r"""
        Again, you can use `qutip.Qobj` to convert NumPy arrays or
        lists to quantum objects.

        Alternatively, you can produce the states with
        `qutip.basis(dim, n)`, which created the `n`th basis state
        of dimension `dim`.
        """
    ),
)


step5 = NoSolveQuestion(
    solution_message=dedent(
        r"""
        ```python
        proj0 = psi0 * psi0.dag()
        proj1 = psi1 * psi1.dag()
        ```
        """
    ),
    hint=dedent(
        r"""
        You can turn a ket state `psi` defined as a `qutip.Qobj` into
        a bra by writing `psi.dat()`.

        Alternatively, write `psi.proj()` to directly create a
        projector from this state.
        """
    ),
)


step6 = NoSolveQuestion(
    solution_message=dedent(
        r"""
        ```python
        output = qutip.mesolve(H, psi0, t, e_ops=[proj0, proj1])
        ```
        """
    ),
    hint=dedent(
        r"""
        You need to specify the following arguments to `qutip.mesolve()`
        - Hamiltonian (as nested list)
        - initial state
        - time grid
        - observables: these are given in the form
        `e_ops=[op1, op2, ...]`.
        """
    ),
)

step7 = NoSolveQuestion(
    solution_message=dedent(
        r"""
        ```python
        fig, ax = plt.subplots()
        ax.plot(t, np.abs(Env)/np.abs(Env).max(), '-',
                color='lightgrey', label='|E|')
        ax.plot(t, output.expect[0], '-', label=r'$|0\rangle$')
        ax.plot(t, output.expect[1], '--', label=r'$|1\rangle$')
        ax.set_xlim(t.min(), t.max())
        ax.set_xlabel('Time')
        ax.set_ylabel('Population')
        ax.legend()
        plt.show()
        ```
        """
    ),
    hint=dedent(
        r"""
        The time-dependent population of the `i`th state is stored in
        `output.expect[i]`.

        You can create a quick and dirty plot of `f` over `x` with
        `plt.plot(x, f)`.
        Check the documentation of the Matplotlib package for in depth
        plotting tutorials.
        """
    ),
)


bonus = NoSolveQuestion(
    solution_message=dedent(
        r"""
        ```python
        H = (np.array(H1) * dphi[:,np.newaxis,np.newaxis]
             + np.array(H2) * Env[:,np.newaxis,np.newaxis])

        e, v = np.linalg.eig(H)

        # Optional: fix ordering of eigenvalues for t>0
        e[t>0] = e[t>0][:, ::-1]
        v[t>0] = np.swapaxes(v[t>0][:, ::-1], -1, -2)

        fig, ax = plt.subplots()
        ax.plot(t, -dphi/2, '-', color='grey')
        ax.plot(t, +dphi/2, '--', color='grey')
        ax.plot(t, e[:, 0].real, '-', label='state 0')
        ax.plot(t, e[:, 1].real, '--', label='state 1')
        ax.set_xlabel('t')
        ax.set_ylabel('Eigenenergie')
        ax.legend()
        plt.show()
        ```
        """
    ),
    hint=dedent(
        r"""
        Construct the total Hamiltonian on the time grid as
        3d NumPy array with dimension `(Nt, 3, 3)`, where `Nt` is the
        number of points in the time grid.
        You can convert the previously defined quantum objects `H1` and `H2`
        to NumPy arrays with `np.array()` and multiply them with `Env` and `dphi`
        by using NumPy's broadcasting rules and `np.newaxis`.

        Diagonalise the time-dependent Hamiltonian with NumPy's function
        `np.linalg.eig()`.
        """
    ),
)
