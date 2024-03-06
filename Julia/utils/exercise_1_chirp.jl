include("question.jl")

#=
using QuantumPropagators: QuantumPropagators, hamiltonian, propagate
using OrdinaryDiffEq
using Plots

Plots.default(
    linewidth               = 2.0,
    foreground_color_legend = nothing,
    background_color_legend = RGBA(1, 1, 1, 0.8)
)
=#

problem_1 = Question(
    hint="""
      **Hint**: Combine the built-in functions `range` and `collect`.
      """,
    solution="""
      **Solution**:

      ```julia
      t = collect(range(-250, 250; length=5000));
      ```
      """,
)

problem_2 = Question(
    hint="""
      **Hint**:
      Matrices in Julia can be written by separating
      columns with spaces and rows with a semicolon or a newline (for a
      multiline format)
      """,
    solution=raw"""
      **Solution**:
      ```julia
      H₁ = -1/2 * [
          1  0
          0 -1
      ]
      H₂ = -1/2 * [
          0 1
          1 0
      ]
      ```

      or

      ```julia
      H₁ = -1/2 * [1 0; 0 -1]
      H₂ = -1/2 * [0 1; 1  0 ]
      ```
      """,
)

problem_3 = Question(
    hint=raw"""
      You can multiply to variables with the `*` operator,
      whereas `t^2` corresponds to "t to the power of two". The `*` can be
      omitted between numbers and variables, so `2τ` is equivalent to
      `2 * τ`.

      For unicode symbols, write latex-like code and convert it to unicode
      with the `<tab>` key.

      * `E\_0<tab>` becomes `E₀`
      * `\tau<tab>` becomes `τ`
      * `\alpha<tab>` becomes `\alpha`
      * `\phi<tab>` becomes `ϕ`

      You can always paste a particular unicode symbol into the help system
      to see how it can be written:

      ```
      ? ϕ
      ```
      """,
    solution="""
      **Solution**:

      ```julia
      E₀ = 1.0
      τ = 50.0
      α = 0.001

      Env(t) = E₀ * exp(-t^2 / 2τ^2)
      dϕ(t) = α * t
      ```
      """,
)

#=
H = hamiltonian((H₁, dϕ), (H₂, Env))

using QuantumPropagators.Controls: evaluate
=#

problem_4 = Question(
    hint=raw"""
        **Hint**:

        * An array with elements of type `Type` is create in Julia with
          `Type[…]`, e.g., `Float64[1.0, 1.1]`, where `Float64` is a
          double-precision (64 bit) float
        * When no type is given, Julia automatically derives the type from the
          values, e.g., `[1, 2]` is the same as `Int64[1, 2]`.
        * The type of a complex (double-precision) number is `ComplexF64`
        * Quantum state vectors have complex values
        """,
      solution="""
      **Solution**:

      ```
      Ψ₀ = ComplexF64[1, 0]
      Ψ₁ = ComplexF64[0, 1]
      ```
      """,
)

problem_5 = Question(
    hint=raw"""
        **Hint**:
        Julia uses `'` for complex conjugation of vectors and matrices, as a
        short-hand for `LinearAlgebra.Adjoint()`.
        """,
    solution="""
        **Solution**:

        ```julia
        P₀ = Ψ₀ * Ψ₀'
        P₁ = Ψ₁ * Ψ₁'
        ```
        """,
)

problem_6 = Question(
    hint=raw"""
        **Hint**

        You need to specify the following arguments to
        `QuantumPropagators.propagate`:

        As positional arguments:

        - initial state
        - Hamiltonian
        - time grid

        As keyword arguments

        - method: the propagation method (`OrdinaryDiffEq`)
        - observables: these are given in the form
        `observables=[op1, op2, ...]`.

        By default, `propagate` returns the final propagated states. Here, we
        want the expectation values of the projectores `P₀` and `P₁` for each
        point in time. We can obtain these by passing `storage=true`

        For details, query the help system about the `propagate` function
        (`? propagate`).
        """,
    solution=raw"""
        **Solution**:

        ```julia
        output = propagate( Ψ₀, H, t; method=OrdinaryDiffEq, observables=[P₀, P₁], storage=true )
        ```
        """,
)

problem_7 = Question(
    hint=raw"""
        **Hint**

        * When plotting the function `Env`, map it elementwise to the vector `t`
          using Julia's dot feature (`abs.(Env.(t))`). Also normalize to the peak
          value `maximum(abs.(Env.(t)))`
        * Use the `plot` function for the initial curve, giving an array of
          x-values and an array of y-values, and the options like color or
          label as keyword arguments (separated from the positional arguments
          by a semicolon)
        * Add more lines to the plot via the `plot!` function. In general, an
          exclamation mark at the end of a function in Julia is a convention
          to indicate that a function modifies an object. In this case, that
          object is the current plot (a hidden internal object)
        * You can use a call to `plot!` with only keyword arguments to set
          general properties like the axis labels. Don't forget the semicolon,
          or the `Plots` package might get confused about what parameters are
          data to be plotted and what parameters are options.
        """,
    solution=raw"""
        **Solution**:

        ```julia
        E_max = maximum(abs.(Env.(t)))
        plot(t, abs.(Env.(t)) / E_max; color="lightgray", label="|ℰ|")
        plot!(t, real.(output[1,:]); color="#1f77b4", label="|0⟩")
        plot!(t, real.(output[2,:]); color="#ff7f0e", linestyle=:dash, label="|1⟩")
        plot!(; xlabel="Time", ylabel="Population", legend=:right )
        ```
        """,
)

bonus = Question(
    hint=raw"""
        **Hint**:

        * Create a list of matrices, containing `H` evaluated for each point of
          the time grid
        * Map the function `eigvals` to that list of matrices to get a list of
          lists of eigenvalues at each point in time (two eigenvalues at `t`).
          Remember that any function can be mapped to an array by appending a
          dot (`func.(array)` is equivalent to `[func(val) for val in array]`)
        * Plot the the two eigenvalues over time. Also plot `±dϕ(t)` for
          comparison.
        """,
    solution="""
        **Solution**:

        ```julia
        H_over_t = [Array(evaluate(H, tval)) for tval in t]
        evals = eigvals.(H_over_t)

        plot(t, t -> -dϕ(t)/2; color="grey", linestyle=:dash, label="")
        plot!(t, t ->  dϕ(t)/2; color="grey", linestyle=:dash, label="")
        plot!(t, [e[1] for e in evals]; color="#1f77b4", label="E₀")
        plot!(t, [e[2] for e in evals]; color="#ff7f0e", label="E₁")
        plot!(; xlabel="t", ylabel="Eigenenergies" )
        ```
        """,
)


"""
# Super-Bonus: Track the eigenstates
#
# It's the eigenvalues that should vary continuously, and in theory, we need to
# make sure that the eigenvalues correspond to the "correct" eigenstate, i.e.,
# that the eigenstates didn't "flip" at the avoided crossing.

using LinearAlebra

eigensys = LinearAlgebra.eigen.(H_over_t)

# How much do the eigenvectors change compared to the previous point in time?
function evec_change(U1, U2)
    [1 - abs2(U1[:,i] ⋅ U2[:,i]) for i=1:2]
end

# Do the eigenvectors "flip"?
function evec_flipped(U1, U2)
    [1 - abs2(U1[:,1] ⋅ U2[:,2]),  1 - abs2(U1[:,2] ⋅ U2[:,1])]
end

change = hcat([evec_change(eigensys[i].vectors, eigensys[i-1].vectors) for i=2:length(eigensys)]...)

plot(t[2:end], change')

# If there's a discontinuity in that plot, we're in trouble (but there's not)

flipped = hcat([evec_flipped(eigensys[i].vectors, eigensys[i-1].vectors) for i=2:length(eigensys) ]...)

plot(t[2:end], flipped')
"""
