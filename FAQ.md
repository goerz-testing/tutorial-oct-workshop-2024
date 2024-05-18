# FAQ

## Do I need to do anything if I have Jupyter installed through Anaconda?

You should still make sure that `ipympl` is installed in version 0.9.3:

```
conda install ipympl=0.9.3
```

You also have to install the [`python-localvenv-kernel` package](https://github.com/goerz/python-localvenv-kernel). Since the conda package for that kernel is only on the [conda-forge channel](https://conda-forge.org/docs/user/introduction/)), not Anaconda's default channel, you may find it easier to install it via `pip`:

```
pip install python-localvenv-kernel
```

Make sure the `pip` binary you are using is from the same environment as the `jupyter` binary. If in doubt, you can also open a new Jupyter notebook (with the default kernel), and run `%pip install python-localvenv-kernel` in a cell.


## How do I ensure the `python-localvenv-kernel` Jupyter kernel is set up correctly?

On the command line, run

```
jupyter kernelspec list
```

The resulting list should contain an entry for `python-localvenv`.


## What do I do if initializing the Python project fails with Miniforge?

If you freshly installed Jupyter through Miniforge, as recommended, but then you see errors like
"warning libmamba Problem type note implemented…" or "mamba […] would require
libmambapy […] which conflicts with any installable versions […]" when you try
to instantiate the project environment with


```
conda env create -p .venv -f environment.yml
```

You may have a old conda configuration from an earlier installation of Anaconda
lying around on your hard drive

Check that

```
conda config --show channels
```

contains "conda-forge" as the only channel.

You can use `conda config --remove channels <channelname>` to remove extraneous
channels. You can also delete any existing `.condarc` file. On macOS or Linux,
this should be `~/.condarc` in your home directory, on Windows it is in
`C:\Users\username\.condarc`.


## What do I do if the installation of `juliaup` fails?

You can also [install the latest official Julia binaries](https://julialang.org/downloads/#official_binaries_for_manual_download). On macOS, this will create a "Julia" application in `/Applications`, and on Windows, "Julia" should show up in the start menu. Opening the application gives you a Julia REPL, and you can complete the installation of the `IJulia` kernel there instead of on the command line.


## How do I set up the IJulia kernel for Jupyter?

Installing the `IJulia` package into the default Julia environment (`using Pkg; Pkg.add("IJulia")`) or simply `] add IJulia` if you are already in the REPL should automatically set up the kernel for use with any running instance of Jupyter. However, if an `IJulia` kernel description already exists, it will not overwrite that kernel. To force writing a kernel, open a Julia REPL in your default environment and run

```julia
using IJulia
installkernel("Julia", "--threads=auto", "--project=@.")
```

The `--project=@.` is essential. The `--threads=auto` is optional. You may prefer to set the `JULIA_NUM_THREADS` environment variable before starting Jupyter, for controlling the number of threads on a case-by-case basis, instead of every kernel using all available threads.


## How do I ensure the IJulia Jupyter kernel is set up correctly?

On the command line, run

```
jupyter kernelspec list
```

You should see an entry for `julia-1.10`. If not, install `IJulia` and, if necessary, [set up the IJulia kernel](#how-do-i-set-up-the-ijulia-kernel-for-jupyter).

If the entry is there, open the file `kernel.json` inside the directory shown by `jupyter kernelspec list` in a text editor. It should look something like

```json
{
  "display_name": "Julia 1.10.2",
  "argv": [
    "/Users/user/.julia/juliaup/julia-1.10.2+0.aarch64.apple.darwin14/bin/julia",
    "-i",
    "--color=yes",
    "--threads=auto",
    "--project=@.",
    "/Users/user/.julia/packages/IJulia/Vo51o/src/kernel.jl",
    "{connection_file}"
  ],
  "language": "julia",
  "env": {},
  "interrupt_mode": "signal"
}
```

Make sure that the `kernel.json` file contains `--project=@.`. This is absolutely essential: it means that every notebook will use the local Julia environment described in the `JuliaProject.toml` (or `Project.toml`) file in the parent folder(s) of any `.ipynb` notebook file.

If the line is missing, add it manually, or [re-install the kernel](#how-do-i-set-up-the-ijulia-kernel-for-jupyter).

## Can I run the tutorial on Binder?

If you cannot set up the tutorial on your own laptop, you can run in on Binder as a last resort:

https://mybinder.org/v2/gh/goerz-testing/tutorial-oct-workshop-2024/HEAD

Please note:

* Binder does not save notebooks. If you disconnect, you will lose progress
* You may run into resource limitations like the 2GB RAM limit and be disconnected at any time
* In the Python "Hello World" notebook, ignore any mention of the `python-localvenv-kernel`. Binder is set up to automatically use the default kernel ("Python 3 (ipykernel)"), which has all required dependencies installed
* Calling Python code from Julia will not work. This affects the visualization on the Bloch sphere in one of the Julia examples. Just ignore any related error messages.

Due to these limitation, you are strongly encouraged to run the tutorial on your local laptop, not on Binder.
