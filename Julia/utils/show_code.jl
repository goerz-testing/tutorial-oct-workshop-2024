using CodeTracking: @code_string
using Markdown

macro show_code(expr...)
    return quote
        Markdown.parse(
            "\n````julia\n" * (@code_string $(expr...)) * " \n````\n"
            # There's an extra space here -----------------^ to get around
            # https://github.com/jupyterlab/jupyterlab/issues/16112
        )
    end
end
