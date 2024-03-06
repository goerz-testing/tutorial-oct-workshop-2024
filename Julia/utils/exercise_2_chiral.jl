include("question.jl")

problem_0 = Question(
    hint="""
      **Hint**: Start varying parameters to get close to the target pulse. Find
      an order-of-magnitude value for each free parameter. Then iterate over
      the parameters and bisect the value for each parameter to refine the
      value.
      """,
    solution="""
      **Solution**:

      A reasonably good set of parameters obtain by hand might be this:

      ```julia
      plot_parameterised_pulse(tlist; E₀=23, a=7.5, t₁=0.325, t₂=(1-0.325))
      ```
      """,
)

bonus = Question(
    hint=raw"""
      **Hint:**

      Set up a function that takes parameters `x` and returns the `mismatch`.
      You probably want to set t₂=1-t₁:

      ```julia
      function optimize_pulse_shape(x, _)
          E₀, a, t₁ = x
          t₂ = 1-t₁
          pulse = t -> E(t; E₀, a, t₁, t₂)
          target_pulse = t -> 20 * exp(-20 * (t - 0.5)^2)
          mismatch = sum(abs.(pulse.(tlist) .- target_pulse.(tlist))) / length(tlist)
          return mismatch
      end
      ```
      """,
    solution=raw"""
      **Solution:**

      ```julia
      function optimize_pulse_shape(x, _)
          E₀, a, t₁ = x
          t₂ = 1-t₁
          pulse = t -> E(t; E₀, a, t₁, t₂)
          target_pulse = t -> 20 * exp(-20 * (t - 0.5)^2)
          mismatch = sum(abs.(pulse.(tlist) .- target_pulse.(tlist))) / length(tlist)
          return mismatch
      end

      prob = OptimizationProblem(
          optimize_pulse_shape,
          [20.0, 7.5, 0.3],
          nothing;
          stopval=0.1,
      );

      res = Optimization.solve( prob, NLopt.LN_NELDERMEAD(), maxiters=100 )
      ```
      """
)


problem_1 = Question(
    hint="""
      **Hint**: The upper bounds are given in the description! For the pulse
      durations, we're not taking into account that ideally, they should sum up
      to 1 (this is not a strict requirement), so take that into account and
      choose guesses that sum up to slightly less than 1 (giving each pulse
      duration room to expand a bit). For the other parameters, starting
      halfway between the minimum and maximum value might be a good idea.
      """,
    solution="""
      ```julia
      guess = ComponentVector(
          ΔT=[0.2, 0.4, 0.3],
          ϕ=[π, π, π],
          E₀=[5.0, 5.0, 5.0]
      );

      prob = OptimizationProblem(
          loss,
          guess,
          (a=1000.0, T=1, nt=100);   # this is a NamedTuple
          lb=zeros(9),
          ub=ComponentVector(
              ΔT=[1.0, 1.0, 1.0],
              ϕ=[2π, 2π, 2π],
              E₀=[10.0, 10.0, 10.0]
          ),
          stopval=(1-0.99),
      );
      ```
      """,
)

