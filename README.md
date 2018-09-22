# halstead

`halstead` is a package to analyze the Halstead metrics of a Python git
repository. For now, it takes arbitrary git repositories, computes the Halstead
metrics on them, and plots the Halstead estimated length against the actual
length. For example, the command `halstead rg3/youtube-dl` produced the
following graphic:

![Example run with the youtube-dl package](./youtube-dl.svg)

The command `halstead -j rg3/youtube-dl mwouts/jupytext
KonstantinSchubert/zero` produced the following, more complicated graphic:

![Example of a joined plot](./youtube-dl_jupytext_zero.svg)
