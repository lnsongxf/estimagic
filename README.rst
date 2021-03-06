=========
estimagic
=========

Introduction
============

Estimagic is a Python package that helps to build high-quality and user
friendly implementations of (structural) econometric models.

It is designed with large structural models in mind. However, it is also
useful for any other estimator that numerically minimizes or maximizes a
criterion function (Extremum Estimator). Examples are maximum likelihood
estimation, generalized method of moments, method of simulated moments and
indirect inference.

Estimagic is in a very early stage and should not be used yet!


Credits
=======


Estimagic is a collaborative project right from the start. While the original
design was my idea, it would not be possible to implement the package without
the help of others. In particular I would like to thank:

- Klara Röhrl (`roecla <https://github.com/roecla>`_) for writing most of the
  dashboard code.
- Tobias Raabe (`tobiasraabe <https://github.com/tobiasraabe>`_) for setting
  up the continuous integration and testing.

If you want to find your name here as well, please contact me or browse
through our Issues and submit a Pull Request.


Installation
============

The package can be installed via conda. To do so, type the following commands
in a terminal:

conda config --add channels conda-forge conda install -c janosg estimagic

The first line adds conda-forge to your conda channels. This is necessary for
conda to find all dependencies of estimagic. The second line installs
estimagic and its dependencies.

