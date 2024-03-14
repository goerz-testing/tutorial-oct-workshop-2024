from question import NoSolveQuestion
from textwrap import dedent


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
