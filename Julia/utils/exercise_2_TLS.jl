include("question.jl")

problem_0 = Question(
    hint=raw"""
      **Hint**:

      Start varying parameters to get close to a population of 1 in state $\ket{1}$.
      Find an order-of-magnitude value for each free parameter. Then iterate over
      the parameters and bisect the value for each parameter to refine the value.
      """,
    solution=raw"""
      **Solution**:

      A reasonably good set of parameters obtained by hand might be this:

      ```julia
      evolve_and_plot_parameterized_pulse( E₀=0.93, ΔT=8.0 )
      ```
      """,
)

problem_1 = Question(
    hint=raw"""
      **Hint**:

      The upper bounds are given in the description! For the other parameters,
      you can use for example the parameters from the guess pulse.
      """,
    solution=raw"""
      **Solution**:

      ```julia
        guess = [0.5, 5.0]
        upper_bounds = [10.0, T]
      ```
      """,
)

