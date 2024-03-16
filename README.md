# Tutorial for the Workshop "Quantum Optimal Control"

https://mathplus.de/topic-development-lab/tes-summer-2024/qoc-workshop/


## Prerequisites

### Jupyter

This tutorial is a collection of [Jupyter notebooks](https://jupyter.org). The view and run them, you must have the Jupyter application installed on your system. We recommend using [Miniforge](https://github.com/conda-forge/miniforge?tab=readme-ov-file#miniforge) to install install Jupyter (or some other `conda`-based distribution like [Miniconda](https://github.com/conda-forge/miniforge?tab=readme-ov-file#miniforge) or the original [Anaconda](), but we recommend installing all packages from the [conda-forge channel](https://conda-forge.org/docs/user/introduction/)).

Assuming you have a Miniconda installation (or you have [set up `conda-forge` as your default channel](https://conda-forge.org/docs/user/introduction/#how-can-i-install-packages-from-conda-forge)), running the following command line instruction should install Jupyter into your `base` environment:

```
conda install jupyterlab notebook python-localvenv-kernel ipympl=0.9.3
```

Note the [`python-localvenv-kernel` package](https://github.com/goerz/python-localvenv-kernel), which is available only in `conda-forge`. If you cannot use the `conda-forge` channel, the package can also be installed into an existing environment [via `pip`](https://github.com/goerz/python-localvenv-kernel?tab=readme-ov-file#installation).

The `ipympl` package is used in some of the notebooks for interactive plots (`%matplotlib widget`). For this to work properly, the `ipympl` package must be installed both the in environment providing the Jupyter application and in the project environment used by the notebook (defined in `environment.yml`), in the same version `0.9.3`. If there is a mismatch, you may see errors when generating plots. However, you will still be able to follow the tutorial with non-interactive plots by removing the `%matplotlib widget` line in any notebook.

To make sure that your Jupyter is set up correctly, run

```
jupyter kernelspec list
```

on the command line and check that the output contains an entry for `python-localvenv`. You should now be able to launch Jupyter by running

```
jupyter lab
```

on the command line, from the folder containing this tutorial.

We also recommend that you install the [JuliaMono font](https://juliamono.netlify.app) on your system. If possible, set it as the default monospace font in your terminal as well as your browser (e.g, via the URL `chrome://settings/fonts` in Chrome) and in Jupyter Lab ("Settings", "Settings Editor", "Theme", set "code-font-family" to "JuliaMono" for your "Selected Theme").


### Julia

If you would like to complete this tutorial in the [Julia language](https://julialang.org), you must install Julia onto your system. Use the [Juliaup installer](https://github.com/JuliaLang/juliaup?tab=readme-ov-file#juliaup---julia-version-manager) and follow the [installation instructions](https://github.com/JuliaLang/juliaup?tab=readme-ov-file#installation).

Once you have `julia` installed, you also need [IJulia](https://github.com/JuliaLang/IJulia.jl) to make Julia available in Jupyter. Run the following on the command line:

```
julia -e 'using Pkg; Pkg.add("IJulia")'
```


### Python project initialization

Even though you already have `python` installed by virtue of having the Jupyter applications, you must still initialize the *project environment* in which the Python notebooks are executed. If you intend to follow this tutorial only in Julia, you can skip this setup. Because we will used Python packages that wrap around compiled C++ code, initializing the environment requires the `conda` executable, see the installation instructions for Jupyter above.

On the command line, from the folder containing this tutorial, run

```
conda env create -p .venv -f environment.yml
```


### Julia project initialization

Similarly, to execute any of the Julia notebooks, you muse initialize a Julia project environment. If you intend to follow this tutorial only in Python, you can skip this setup. Assuming you have Julia installed on your system (see above), run the following on the command line, from the folder containing this tutorial:

```
julia --project=. -e 'using Pkg; Pkg.instantiate()'
```

If you are on a Unix system and have some basic development tools installed, you can also run

```
make init
```

to initialize both the Python and Julia project configuration.


## Notebooks

Assuming you have set up all the prerequisites as described above, start `jupyter lab` from the folder containing this tutorial. If you are on a Unix system and have `make` installed, you may also run `make jupyter-lab`.

### Part 1 – Light Matter Interaction

* Exercise 1 – Two Level System ([Python](Python/py_exercise_1.ipynb), [Julia](Julia/jl_exercise_1.ipynb))
* Exercise 2 – Two Level System Interacting with a Chirped Laser ([Python](Python/py_exercise_2.ipynb), [Julia](Julia/jl_exercise_2.ipynb))

### Part 2 – Control Parameters

* Exercise 3 – Parameter Optimization of Three-Wave Mixing in a Three-Level System ([Python](Python/py_exercise_3a.ipynb), [Julia](Julia/jl_exercise_3a.ipynb))


### Part 3 – Gradient Optimization with Krotov's method and GRAPE

* Exercise 4 – State-to-state transfer in a two-level system [Python](Python/py_exercise_4a.ipynb), [Julia](Julia/jl_exercise_4a.ipynb))
