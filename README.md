# Tutorial for the Workshop "Quantum Optimal Control"

https://mathplus.de/topic-development-lab/tes-summer-2024/qoc-workshop/


## Prerequisites

Please make sure to follow the installation instructions below carefully. **You must set up these prerequisites on your own laptop before the start of the tutorial**. During the two hours of the tutorial session, there will not be time for solving technical issues.

There is also a [YouTube playlist](https://www.youtube.com/playlist?list=PLD3uZJ5Hp3yveIUsParmhEJ0_v2u1Busn) to walk you through this installation:

* [Installation on a Windows system](https://youtu.be/01SSHEt-_fA)
* [Installation on a macOS system](https://youtu.be/5jacvF2dcAM). These would be mostly applicable to other Unix/Linux systems as well.

On Windows, it is easiest if you have full administrative privileges. On macOS or Linux, everything will install into your home directory by default, so "root access" is not required.


### Jupyter

This tutorial is a collection of [Jupyter notebooks](https://jupyter.org). To view and run them, you must have the Jupyter application installed on your system. We recommend using [Miniforge](https://github.com/conda-forge/miniforge?tab=readme-ov-file#miniforge) to install Jupyter (or some other `conda`-based distribution like [Miniconda](https://github.com/conda-forge/miniforge?tab=readme-ov-file#miniforge) or the original [Anaconda](), but we recommend installing all packages from the [conda-forge channel](https://conda-forge.org/docs/user/introduction/)).

> ⚠️ ⚠️ ⚠️
> Even if you already have Jupyter installed, you are probably missing the `python-localvenv-kernel` package. Make sure to install its latest version into the same environment that contains `jupyter`. You may also need to install `ipympl` in the correct version. See the [FAQ](FAQ.md) for details.

Assuming you have a Miniforge installation (or you have [set up `conda-forge` as your default channel](https://conda-forge.org/docs/user/introduction/#how-can-i-install-packages-from-conda-forge)), running the following command line instruction should install Jupyter into your `base` environment:

```
conda install jupyterlab python-localvenv-kernel=0.1.7 ipympl=0.9.3
```

Note the [`python-localvenv-kernel` package](https://github.com/goerz/python-localvenv-kernel), which is available only in `conda-forge`. If you cannot use the `conda-forge` channel, the package can also be installed into an existing environment [via `pip`](https://github.com/goerz/python-localvenv-kernel?tab=readme-ov-file#installation). When installing on Windows, it is important that the `python-localvenv-kernel` package is in the latest version (`pip install python-localvenv-kernel==0.1.7`.)


The `ipympl` package is used in some of the notebooks for interactive plots (`%matplotlib widget`). For this to work properly, `ipympl` must be installed both in the environment providing the Jupyter application and in the project environment used by the notebook (defined in `environment.yml`), in the same version `0.9.3`. If there is a mismatch, you may see errors when generating plots. However, you will still be able to follow the tutorial with non-interactive plots by removing the `%matplotlib widget` line in any notebook.

To make sure that your Jupyter is set up correctly, run

```
jupyter kernelspec list
```

on the command line and check that the output contains an entry for `python-localvenv`. In case `python-localvenv` does not appear in the kernel list try to reinstall the package with `pip`, see also the [package FAQ](https://github.com/goerz/python-localvenv-kernel/blob/master/FAQ.md#the-python-local-venv-kernel-does-not-show-up-in-jupyter), or with `%pip` inside a notebook cell inside a running `jupyter` instance, see the [tutorial FAQ](FAQ.md).

You should now be able to launch Jupyter by running

```
jupyter lab
```

on the command line, from the folder containing this tutorial.

We also recommend that you install the [JuliaMono font](https://juliamono.netlify.app) on your system. If possible, set it as the default monospace font in your terminal as well as your browser (e.g, via the URL `chrome://settings/fonts` in Chrome) and in Jupyter Lab ("Settings", "Settings Editor", "Theme", set "code-font-family" to "JuliaMono" for your "Selected Theme").


### Julia

If you would like to complete this tutorial in the [Julia language](https://julialang.org), you must install Julia onto your system. Use the [Juliaup installer](https://github.com/JuliaLang/juliaup?tab=readme-ov-file#juliaup---julia-version-manager) and follow the [installation instructions](https://github.com/JuliaLang/juliaup?tab=readme-ov-file#installation).

If you have problems with `juliaup`, you can also [manually install the official binaries](https://julialang.org/downloads/#official_binaries_for_manual_download).

Check that you get a Julia REPL ("Read-Evaluate-Print-Loop", the thing where you can type in code, press enter, and see the result) if you start `julia` on the command line, or if you click the appropriate Julia application icon in your start menu (Windows) or the Applications folder (macOS).

Once you have `julia` installed, you also need [IJulia](https://github.com/JuliaLang/IJulia.jl) to make Julia available in Jupyter. Run the following on the command line:

```
julia -e 'using Pkg; Pkg.add("IJulia")'
```

Or, if you are already in a Julia REPL,

```
] add IJulia
```

would be the equivalent command (`]` activates `Pkg` mode, press backspace to get back to the standard REPL mode).

Although this should happen automatically, in some situations you may have to to manually (re-)install the IJulia kernel. In a Julia REPL in the default environment, run

```julia
using IJulia
installkernel("Julia", "--threads=auto", "--project=@.")
```

See the [FAQ](FAQ.md) for details.


### Python project initialization

Even though you already have `python` installed by virtue of having the Jupyter applications, you must still initialize the *project environment* in which the Python notebooks are executed. If you intend to follow this tutorial only in Julia, you can skip this setup. Because we will use Python packages that wrap around compiled C++ code, initializing the environment requires the `conda` executable, see the installation instructions for Jupyter above.

On the command line, from the folder containing this tutorial, run

```
conda env create -p .venv -f environment.yml
```


### Julia project initialization

Similarly, to execute any of the Julia notebooks, you must initialize a Julia project environment. If you intend to follow this tutorial only in Python, you can skip this setup. Assuming you have Julia installed on your system (see above), run the following on the command line, from the folder containing this tutorial:

```
julia --project=. -e "using Pkg; Pkg.instantiate()"
```

Or, from inside a Julia REPL with the tutorial folder as the current working directory

```
using Pkg
Pkg.activate(".")  # equivalent to starting Julia with `--project=."
Pkg.instantiate()
```

The first time you do this, it will precompile a lot of packages. This can take a while (10-15 minutes, maybe more on a older Windows computer). Grab a coffee.

If you are on a Unix system and have some basic development tools installed, you can also run

```
make init
```

to initialize both the Python and Julia project configuration. Note that this will fail unless *both* Python and Julia are installed on your system.

This concludes the setup instructions for the tutorial. To verify the installation, run `jupyter lab` and find the "Hello World" notebooks in the Python and Julia subfolders. Run these to completely to make sure that everything is working, and please ask for help if it is not.


## Tutorial Notebooks

Assuming you have set up all the prerequisites as described above, start `jupyter lab` from the folder containing this tutorial. If you are on a Unix system and have `make` installed, you may also run `make jupyter-lab`.

> ⚠️ ⚠️ ⚠️
> You are not expected to work though all of the notebooks below.

### Part I – Light Matter Interaction

1. Population Inversion in a Two-Level-System ([Python](Python/py_exercise_1_1_TLS.ipynb), [Julia](Julia/jl_exercise_1_1_TLS.ipynb))
2. Population Transfer in a Three-Level-System with STIRAP ([Python](Python/py_exercise_1_2_lambda.ipynb), [Julia](Julia/jl_exercise_1_2_lambda.ipynb))
3. Interaction of a Two-Level-System with a Chirped Laser Pulse ([Python](Python/py_exercise_1_3_chirp.ipynb), [Julia](Julia/jl_exercise_1_3_chirp.ipynb))

### Part II – Control Parameters

1. Population Inversion in a Two-Level-System using Parameter Optimization ([Python](Python/py_exercise_2_1_TLS.ipynb), [Julia](Julia/jl_exercise_2_1_TLS.ipynb))
2. Parameter Optimization for STIRAP ([Python](Python/py_exercise_2_2_lambda.ipynb), [Julia](Julia/jl_exercise_2_2_lambda.ipynb))
3. Parameter Optimization of Three-Wave Mixing in a Three-Level System ([Python](Python/py_exercise_2_3_chiral.ipynb), [Julia](Julia/jl_exercise_2_3_chiral.ipynb))


### Part III – "Full" Optimization with gradient-based methods (Krotov's method and GRAPE)

Note that optimization with GRAPE is available only in the Julia version of these exercises.

1. Population Inversion in a Two-Level-System using Krotov's Method and GRAPE ([Python](Python/py_exercise_3_1_TLS.ipynb), [Julia](Julia/jl_exercise_3_1_TLS.ipynb))
2. Optimal Control for STIRAP ([Python](Python/py_exercise_3_2_lambda.ipynb), [Julia](Julia/jl_exercise_3_2_lambda.ipynb))
3. Chiral Three-Wave Mixing ([Python](Python/py_exercise_3_3_chiral.ipynb), [Julia](Julia/jl_exercise_3_3_chiral.ipynb))
4. Entangling Quantum Gates for Coupled Transmon Qubits ([Python](Python/py_exercise_3_4_gate.ipynb), [Julia](Julia/jl_exercise_3_4_gate.ipynb)). The Julia version of this notebook demonstrates logical subspaces embedded in a larger physical Hilbert space, and show the use of semi-automatic differentiation to optimize arbitrary, even non-analytical functionals like the gate concurrence with both GRAPE and Krotov's method.

---

The notebooks span a wide variety of examples and target different levels of expertise. You are encouraged to choose your own path through the tutorial. During the two hours of the tutorial session, you will probably only be able to go through two or so notebooks superficially, and one notebook in full detail. Follow your interests; there are many possible paths through the tutorial.

* If you want to stick to a simple two-level system, look at Exercises [I.1](Python/py_exercise_1_1_TLS.ipynb), [II.1](Python/py_exercise_2_1_TLS.ipynb), [II.3](Python/py_exercise_2_3_chiral.ipynb) (Python, or Julia [I.1](Julia/jl_exercise_1_1_TLS.ipynb), [II.1](Julia/jl_exercise_2_1_TLS.ipynb), [II.3](Julia/jl_exercise_2_3_chiral.ipynb))
* If you you want to develop a basic understanding of light-matter-interaction from a numerical perspective without much optimal control, look at Part 1 ([Python](Python/py_exercise_1_1_TLS.ipynb)/[Julia](Julia/jl_exercise_1_1_TLS.ipynb)), and maybe Exercise II.1 as a follow-up ([Python](Python/py_exercise_2_1_TLS.ipynb), [Julia](Python/py_exercise_2_1_TLS.ipynb))
* If you want to follow along the control of a three-level system ("STIRAP") consider Exercises [I.2](Python/py_exercise_1_2_lambda.ipynb), [II.2](Python/py_exercise_2_2_lambda.ipynb), [II.3](Python/py_exercise_2_3_chiral.ipynb), maybe with [I.1](Python/py_exercise_1_1_TLS.ipynb) as a quick "warm-up" (Python, or Julia, [I.1](Julia/jl_exercise_1_1_TLS.ipynb), [I.2](Julia/jl_exercise_1_2_lambda.ipynb), [II.2](Julia/jl_exercise_2_2_lambda.ipynb), [II.3](Julia/jl_exercise_2_3_chiral.ipynb))
* If you are interested in chiral molecules and some more advanced examples of parameter optimization, follow Exercises [I.1](Python/py_exercise_1_1_TLS.ipynb) (as warm-up), [II.3](Python/py_exercise_2_3_chiral.ipynb), [III.3](Python/py_exercise_3_3_chiral.ipynb) (Python, or Julia [I.1](Julia/jl_exercise_1_1_TLS.ipynb), [II.3](Julia/jl_exercise_2_3_chiral.ipynb), [III.3](Julia/jl_exercise_3_3_chiral.ipynb))
* If you want to learn specifically about parameter optimization, go through the Exercises in Part II ([Python](Python/py_exercise_2_1_TLS.ipynb), or [Julia](Julia/jl_exercise_2_1_TLS.ipynb)), with maybe III.2 ([Python](Python/py_exercise_3_2_lambda.ipynb), [Julia](Julia/jl_exercise_3_2_lambda.ipynb)) as an outlook
* If you want to learn about Krotov's method, go through Exercises [I.1](Python/py_exercise_1_1_TLS.ipynb) (prep), [III.2](Python/py_exercise_3_2_lambda.ipynb), [III.4](Python/py_exercise_3_4_gate.ipynb) (Python, or Julia [I.1](Julia/jl_exercise_1_1_TLS.ipynb), [III.2](Julia/jl_exercise_3_2_lambda.ipynb), [III.4](Julia/jl_exercise_3_4_gate.ipynb)). Note that later Julia Exercises dive into some more advanced topics compared to their Python counterparts. Specifically, the Julia versions support optimization both with Krotov's method and GRAPE.
* If you are interested in quantum information, briefly go through Exercises [II.1](Python/py_exercise_2_1_TLS.ipynb) and [III.1](Python/py_exercise_3_1_TLS.ipynb) and then mainly [III.4](Python/py_exercise_3_4_gate.ipynb) (Python, or Julia [II.1](Julia/jl_exercise_2_1_TLS.ipynb), [III.1](Julia/jl_exercise_3_1_TLS.ipynb), [III.4](Julia/jl_exercise_3_4_gate.ipynb))


You can go through earlier notebooks quickly until you reach on that is is challenging or of particular interest to you. Also, the notebooks will remain available after the end of the workshop so you can always come back, or explore other topics.


## Further Material

You may find further example beyond the scope of this tutorial in the [documentation of
the Python `krotov` package](https://qucontrol.github.io/krotov/v1.2.1/09_examples.html) and the [documentation of the Julia `QuantumControl` framework](https://juliaquantumcontrol.github.io/QuantumControlExamples.jl/stable/). These both include examples for the optimization of open quantum systems; it is worth noting that the techniques illustrated in this tutorial apply quite directly to both closed and open quantum systems.
