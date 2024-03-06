include("question.jl")

problem_1 = Question(
    hint=raw"""
      **Hint**:

      Try starting from something like `guess=[10,-10, 30,60, 50,50]`
      """,
    solution=raw"""
      **Solution**:

      A guess that will take you to 99 % fidelity is `guess=[30,-30, 50,50, 25,25]`
      """,
)
