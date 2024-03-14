# Question class taken from the ELCH Tutorial notebooks at
# https://gitlabph.physik.fu-berlin.de/ag-koch/resources/elch_workshop_2020
# Originally designed by Matthias Krauss.

from IPython.display import display, Markdown, HTML
import matplotlib
from textwrap import indent

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
