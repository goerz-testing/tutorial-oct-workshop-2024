include("question.jl")

problem_1 = Question(
    hint="""
      **Hint**: Look at the ordering of the pulses!
      """,
    solution="""
      **Solution**: The Stokes and Pump pulse are in the wrong order! Try setting `t_p=50` and `t_s=-50`. Leave the other parameters at `σ_p = 50`, `σ_s = 50`, `Δ = 1`, `d_12 = 25`, `d_23 = 25`.
      """,
)