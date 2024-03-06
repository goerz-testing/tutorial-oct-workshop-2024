include("question.jl")

problem_1 = Question(
    hint=raw"""
      **Hint**:

      Have a look at the documentation of the
      [Trajectory](https://juliaquantumcontrol.github.io/QuantumControl.jl/stable/api/quantum_control_base/#QuantumControlBase.Trajectory).
      You will need the `initial_state`, the `generator`, and the
      `target_state` as a keyword argument.
      """,
    solution=raw"""
      **Solution**:

      ```julia
      trajectory = Trajectory( ket1, H; target_state=ket3 )
      ```
      """,
)

problem_2a = Question(
    solution=raw"""
      **Solution**:

      A good parameter for `t_rise` is on the order of 1.0

      ```julia
      S(t) = flattop( t; T=tlist[end], t_rise=1.0, func=:sinsq )
      ```
      """,
)

problem_2b = Question(
    hint=raw"""
      **Hint**:

      Remember: the update is proportional to $1/{\lambda_a}$
      """,
    solution=raw"""
      **Solution**:

      A parameter that works reasonably well is $\lambda_a = 1$.

      ```julia
      λₐ = 1.0
      pulse_options = IdDict(
          ϵ => Dict(:lambda_a => λₐ, :update_shape => S,)
          for ϵ in get_controls(H)
      )
      ```
      """,
)

problem_3 = Question(
    solution=raw"""
      **Solution**:

      ```julia
      using QuantumControl.Functionals: J_T_ss

      problem = ControlProblem(
          [trajectory],
          tlist;
          pulse_options,  # or, `lambda_a=λₐ, update_shape=S`
          J_T=J_T_ss,
          iter_stop=50,
          check_convergence=res -> begin
              ((res.J_T <= 1e-2) && (res.converged = true) && (res.message = "J_T < 10⁻²"))
          end,
          prop_method=Cheby,
      );
      ```
      """,
)

problem_3b = Question(
    hint=raw"""
      **Hint**:

      Does the phase of the final state matter?
      """,
)

problem_3c = Question(
    hint=raw"""
      **Hint**:

      The `check_convergence` argument should receive a function that gets a
      [`KrotovResult`](https://juliaquantumcontrol.github.io/Krotov.jl/stable/api/#Krotov.KrotovResult)

      A fidelity (1-$J_{\mathrm{T}}$) of 99.9% should be sufficient for this
      example.

      You can check the `J_T` attribute of the `res` object. If it matches the
      convergence criterion, set the `converged` attribute to `true` and set
      the `message` attribute to an appropriate message.
      """,
)

problem_3d = Question(
    hint=raw"""
      **Hint**:

      The parameters set in `pulse_options`, especially the value of λₐ,
      influence the convergence. If λₐ is too large, convergence will be slow.
      If it is too small, you may see numerical instability ("spiky" pulses
      with large amplitude, or otherwise unphysical features)

      Of course, there' is also the question of the initial guess…
      """,
)

problem_4a = Question(
    hint=raw"""
      **Hint**:

      * the `substitute` functions should be called as `substitute(H, replacements)`
      * `replacements` should generally be an `IdDict`, since mutable objects
        (the guess pulses) make poor dictionary keys for a regular `Dict`
      * you can use a dict-comprehension of the form
       `IdDict(k => values[i] for (i, k) in enumerate(keys))`
      """,
    solution=raw"""
      **Solution**:

      ```julia
      H_opt = substitute(
          H,
          IdDict(
              ϵ => oct_result.optimized_controls[i]
              for (i, ϵ) in enumerate(get_controls(H))
          )
      );
      ```
      """,
)

problem_4b = Question(
    hint=raw"""
      **Hint**:

      * We need the propagated states at each point in time, so pass `storage=true`
      * This is pretty much the same call as we used for simulating the
        dynamics under the guess controls.
      """,
    solution=raw"""
      **Solution**:

      ```julia
      opt_dynamics = propagate( ket1, H_opt, tlist; method=Cheby, storage=true )
      ```
      """,
)

bonus_a = Question(
    hint=raw"""
      **Hint**:

      You really just need to replace `Krotov` with `GRAPE` and repeat the code
      for analyzing the results.

      As to what might be wrong with the result: Why did we set up
      `pulse_options` in the optimization with Krotov's method? Do the GRAPE
      results still match the requirements that we encoded with `update_shape`?
      """,
    solution=raw"""
      **Solution**:

      ```julia
      oct_result_grape = optimize(problem; method=GRAPE)

      H_opt_grape = substitute(
          H,
          IdDict(
              ϵ => oct_result_grape.optimized_controls[i]
              for (i, ϵ) in enumerate(get_controls(H))
          )
      );

      plot_pulses_abs_phase(H_opt_grape, tlist)

      opt_dynamics_grape = propagate( ket1, H_opt_grape, tlist; method=Cheby, storage=true )

      plot(
          tlist, abs2.(opt_dynamics_grape)';
          label=["⟨1|Ψ|1⟩" "⟨2|Ψ|2⟩" "⟨3|Ψ|3⟩"],
          xlabel="time", ylabel="population",
      )
      ```

      You will see that the optimized pulses are not zero at the beginning and
      end. This is because GRAPE has no direct mechanism similar to the
      `update_shape` option in Krotov's method that enforces boundary
      conditions in the pulse update.
      """,
)

bonus_b = Question(
    hint=raw"""
      **Hint**:

      Instead, we can use a `ShapedAmplitude`,
      where the control amplitude is the product of a constant shape $S(t)$ and
      a arbitrary function $\epsilon(t)$ that is tuned by GRAPE.

      This actually works both for Krotov's method and GRAPE, so we could have
      used the approach for Krotov's method as well instead of using an
      `update_shape`.

      You may use the same $S(t)$ that we used for `update_shape` as the
      `shape` in the `ShapedAmplitude`.

      Depending on the details of the guess pulse, you may find that GRAPE
      "overshoots" with the amplitude of the optimized control. You can use the
      `upper_bound` parameter when instantiating the modified `ControlProblem`
      to limit the pulse amplitude to, e.g., 1.5.
      """,
    solution=raw"""
      **Solution**:

      ```julia
      H2 = hamiltonian(
          H0,
          (H1P_re, ShapedAmplitude(t -> blackman(t, 1.0, 5.0), tlist; shape=S)),
          (H1P_im, ShapedAmplitude(t -> 0.0, tlist; shape=S)),
          (H1S_re, ShapedAmplitude(t -> blackman(t, 0.0, 4.0), tlist; shape=S)),
          (H1S_im, ShapedAmplitude(t -> 0.0, tlist; shape=S))
      )

      trajectory2 = Trajectory( ket1, H2; target_state=ket3 )

      problem2 = ControlProblem(
          [trajectory2],
          tlist;
          J_T=J_T_ss,
          iter_stop=1000,
          check_convergence=res -> begin
              ((res.J_T <= 1e-2) && (res.converged = true) && (res.message = "J_T < 10⁻²"))
          end,
          upper_bound=1.5,
          prop_method=Cheby,
      );

      oct_result_grape2 = optimize(problem2; method=GRAPE)


      opt_amplitudes = [
          substitute(a, IdDict(
                  ϵ => discretize_on_midpoints(
                      oct_result_grape2.optimized_controls[i],
                      tlist
                  )
                  for (i, ϵ) in enumerate(get_controls(H2))
              )
          ) for a in H2.amplitudes
      ]


      H_opt_grape2 = substitute(
          H2,
          IdDict(
              a => discretize(Array(opt_amplitudes[i]), tlist)
              for (i, a) in enumerate(H2.amplitudes)
          )
      );

      plot_pulses_abs_phase(H_opt_grape2, tlist)

      opt_dynamics_grape2 = propagate(ket1, H_opt_grape2, tlist; method=Cheby, storage=true )

      plot(
          tlist, abs2.(opt_dynamics_grape2)';
          label=["⟨1|Ψ|1⟩" "⟨2|Ψ|2⟩" "⟨3|Ψ|3⟩"],
          xlabel="time", ylabel="population",
      )
      ```
      """,
)
