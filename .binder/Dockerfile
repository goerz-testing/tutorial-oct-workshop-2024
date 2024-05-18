FROM ghcr.io/goerz-testing/tutorial-oct-workshop-2024:latest

# Set `JULIA_CPU_TARGET` to same value as default Julia builds, to ensure we
# don't specialise pkgimages to the current host CPU:
# https://github.com/JuliaCI/julia-buildkite/blob/f70c9abc11abbf8c373c0cb9f8a7f8e3b165cced/utilities/build_envs.sh#L24-L31
ENV JULIA_CPU_TARGET="generic;sandybridge,-xsaveopt,clone_all;haswell,-rdrnd,base(1)"

ARG NB_USER=jovyan
ARG NB_UID=1000
ENV USER ${NB_USER}
ENV NB_UID ${NB_UID}
ENV HOME /home/${NB_USER}
ENV JULIA_NUM_PRECOMPILE_TASKS 1
ENV JULIA_PKG_PRESERVE_TIERED_INSTALLED true
ENV JULIA_PKG_OFFLINE true

WORKDIR ${HOME}
USER ${USER}
