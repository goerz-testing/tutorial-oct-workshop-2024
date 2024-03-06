from textwrap import dedent
import matplotlib.pylab as plt
import numpy as np
from .question import NoSolveQuestion, Question

__all__ = [
    "problem_1",
    "problem_2",
    "problem_3",
    "plot_pulse",
    "plot_population_3lvl",
]

problem_1 = NoSolveQuestion(
    solution_message=dedent(
        r"""
        By using a Blackman window for our control fields, we are able to
        precisely isolate a time-interval in which the field is non-zero and
        connect our optimized fields in a continuously differentiable way to
        the situation with vanishing fields outside this interval. This allows
        a clean assignment of an initial time $t=0$ (before the initial time
        the system is subject to no field and hence unperturbed) and final time
        $t=T$ (after the final time the system is again evolving freely without
        the influence of any external field).
        """
    ),
    hint=None,
)

problem_2 = Question(
    correct_answer=lambda x: bool(
        np.all(
            np.abs(
                np.array(
                    [[0.95337, 0.04623, 0.00040], [0.95337, 0.04406, 0.00257]]
                )
                - np.array(x)
            )
            < 1e-3
        )
    ),
    success_message=dedent(
        r"""
        Correct, you got the right results! But if you look closely, the
        population seem to be very similar between the two enantiomers.  If you
        remember we wanted a total transfer of population to state 2, which
        means this guess pulse is really not good at all..."""
    ),
    fail_message=dedent(
        r"""
        Try to use the exact results from the propagation. Make sure to look at
        the hint in case you need help.
        """
    ),
    solution_message=dedent(
        r"""
        To extract the *i*th expectation value (for the + enantiomer) you can
        use `guess_dynamics_p.expect[i]`, where *i* is either 0,1 or 2.
        This gives you a list of all the eigenvalue over time. To get the last
        value you can use `guess_dynamics_p.expect[i][-1]`.
        With this, you can get all the results with:

        ```python
        pop1_plus = guess_dynamics_p.expect[0][-1]
        pop2_plus = guess_dynamics_p.expect[1][-1]
        pop3_plus = guess_dynamics_p.expect[2][-1]
        pop1_minus = guess_dynamics_m.expect[0][-1]
        pop2_minus = guess_dynamics_m.expect[1][-1]
        pop3_minus = guess_dynamics_m.expect[2][-1]
        ```
        """
    ),
    hint=[
        dedent(
            r"""
            Make sure to look at qutip's mesolve [`Result`
            class](https://qutip.readthedocs.io/en/stable/apidoc/classes.html#qutip.solver.result.Result).
            """
        ),
        dedent(
            r"""
            Try to figure out, which of the attributes holds the expectation
            values for the projectors defined earlier.  Now try to extract all
            the expectation values from the full list and get the last element
            (remember python's `[-1]` syntax).
            """
        ),
    ],
    default=[[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
)

problem_3 = NoSolveQuestion(
    solution_message=dedent(
        r"""
        A good value for $\lambda_a$ is `opt_lambda = 3.0`.
        """
    ),
    hint=dedent(
        r"""
        Have a look at the "Setting the pulse options" section
        """
    ),
)


def plot_pulse(pulse, tlist, label, spectrum_width=0.35, guess=None, **kwargs):
    """Routine to represent pulses"""
    fig, axs = plt.subplots(1, 2, figsize=(15, 4))
    if callable(pulse):
        pulse = np.array(
            [pulse(t, args={"final_t": tlist[-1]}) for t in tlist]
        )
    axs[0].plot(tlist, pulse, label="Optimized pulse", **kwargs)
    if guess is not None:
        guess = np.array(
            [guess(t, args={"final_t": tlist[-1]}) for t in tlist]
        )
        axs[0].plot(tlist, guess, "--", label="Guess pulse", **kwargs)
        axs[0].legend()
    axs[0].set_xlabel("time", fontsize=15)
    axs[0].set_ylabel("$%s$ pulse amplitude" % label, fontsize=15)
    axs[0].grid()

    padded_pulse = np.pad(
        pulse, (0, 10 * len(tlist)), "constant", constant_values=(0, 0)
    )
    frq = np.fft.fftshift(
        np.fft.fftfreq(len(padded_pulse), d=tlist[1] - tlist[0])
    )
    fft = np.fft.fftshift(np.fft.fft(padded_pulse))
    axs[1].plot(frq, abs(fft) / 1000, label="Optimized pulse", **kwargs)
    if guess is not None:
        padded_guess = np.pad(
            guess, (0, 10 * len(tlist)), "constant", constant_values=(0, 0)
        )
        guess_fft = np.fft.fftshift(np.fft.fft(padded_guess))
        axs[1].plot(
            frq, abs(guess_fft) / 1000, "--", label="Guess pulse", **kwargs
        )
        axs[1].legend()
    axs[1].set_xlim([0, spectrum_width])
    axs[1].set_xlabel("frequency", fontsize=15)
    axs[1].set_ylabel("abs($%s$ fourier transform)" % label, fontsize=15)
    axs[1].grid()
    plt.show(fig)


def plot_population_3lvl(result, title=""):
    """Routine to represent population of different states"""
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.axhline(1.0, c="k", lw=0.5)
    ax.plot(result.times, result.expect[0], label="1")
    ax.plot(result.times, result.expect[1], label="2")
    ax.plot(result.times, result.expect[2], label="3")
    ax.legend(fontsize=8)
    ax.set_xlabel("time", fontsize=15)
    ax.set_ylabel("population", fontsize=15)
    ax.grid()
    ax.set_title(title, fontsize=15)
    plt.show(fig)
