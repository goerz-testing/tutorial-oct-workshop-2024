include("question.jl")

problem_1 = Question(
    hint=raw"""
      **Hint**:

      * When taking the derivative, you can treat ``\ket{\Psi_k(T)}`` and
        ``\bra{\Psi_k(T)}`` as independent variables. The proper mathematical
        footing for this is (a) matrix calculus, which tells us that the
        derivative of a scalar function w.r.t. a row vector is a column vector
        of the component-wise derivatives, and (b) the definition of "Wirtinger
        derivatives", which justify treating a complex variable `z` and its
        complex conjugate `z*` as independent. So the derivative of a scalar
        function w.r.t. a bra-state (a row vector) is the ket (column vector)
        with the componentwise derivatives w.r.t. the complex conjugate
        elements of ``\Psi_k``.
      * Make sure you get the sign right. The definition of ``\ket{\chi_k}``
        includes a minus sign, but ``J_T`` also is 1 minus the fidelity. These
        two minuses cancel.
      * Be careful about the definition of ``\tau`` and where ``\tau``
        respectively the complex conjugate ``\tau^*`` appears.
      """,
    solution=raw"""
      **Solution**:

      ```julia
      function chi!(χ, Ψ, trajectories; kwargs...)
          τ = [Ψ[k] ⋅ trajectories[k].target_state for k = 1:4]
          α = sum(τ') / 16
          for k = 1:4
              χ[k] .= α .* trajectories[k].target_state
          end
      end
      ```
      """,
)

problem_2 = Question(
    solution=raw"""
    **Solution**:

    ```math
    \frac{\partial}{\partial \bra{\Psi_k(T)}} \left(
        \frac{1}{4} \tr[\Op{U}^\dagger \Op{U}]
    \right)
    =
    \frac{1}{4} \sum_j \left(
    \braket{\phi_j | \Psi_k(T)}
    \right) \, \ket{\phi_j}
    ```
    """,
    solution_code=raw"""
    Or, in code,

    ```julia
    function chi_unitarity!(χ, Ψ, trajectories; kwargs...)
        for k = 1:4
            χ[k] .= 0.0
            for j = 1:4
                χ[k] .+= 0.25 * sum([basis[j] ⋅ Ψ[k]]) .* basis[j]
            end
        end
        return χ
    end
    ```
    """
)

problem_3 = Question(
    hint=raw"""
    **Hint**: What kind of functions can we calculate derivatives of?
    """,
    solution=raw"""
    **Solution**:

    The functional contains several non-analytic functions:

    * The `eigvals` in the `weyl_chamber_coordinates`
    * The branch selection and sorting
    * The `max` function in `gate_concurrence`

    None of these are functions where we can write out a derivative by hand.

    Even if someone gave us a "black box" with the derivatives for these
    functions, the chain rule for the entire functional would be quite long and
    tedious to write out.
    """
)
