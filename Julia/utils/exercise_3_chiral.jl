include("question.jl")

problem_1 = Question(
    hint=raw"""
      """,
    solution=raw"""
      **Solution**:

      By using a Blackman window for our control fields, we are able to
      precisely isolate a time-interval in which the field is non-zero and
      connect our optimized fields in a continuously differentiable way to
      the situation with vanishing fields outside this interval. This allows
      a clean assignment of an initial time $t=0$ (before the initial time
      the system is subject to no field and hence unperturbed) and final time
      $t=T$ (after the final time the system is again evolving freely without
      the influence of any external field).
      """,
)

problem_2 = Question(
    hint=raw"""
        **Hint**:

        Try to figure out which of the attributes holds the expectation
        values for the projectors defined earlier. Now try to extract all
        the expectation values from the full list and get the last element
        (remember the `[end]` syntax).
        """,
    solution=raw"""
        **Solution**:

        ```julia
        pop1_plus = res_pt_p[1,end]
        pop2_plus = res_pt_p[2,end]
        pop3_plus = res_pt_p[3,end]
        pop1_minus = res_pt_m[1,end]
        pop2_minus = res_pt_m[2,end]
        pop3_minus = res_pt_m[3,end] 
        ```
        """,
)

problem_3 = Question(
    hint=raw"""
      **Hint**:

      Have a look at the "Setting the pulse options" section
      """,
    solution=raw"""
      **Solution**:

      A good value for $\lambda_a$ is `λₐ = 3.0`.
      """,
)
