# NavBench
Python 3 code for analysing and benchmarking navigation performance for
different algorithms.

To get started, take a look at the [examples](examples) folder.

## Datasets
A selection of image databases is included in the [datasets](datasets) folder as
[git submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules). To
download them you will need [git lfs](https://git-lfs.github.com) (which is
included in the standard [Git for Windows](https://git-scm.com/download/win)
package).

To download a particular dataset, from the root of this repository run e.g.:
```sh
git submodule update --init datasets/rc_car
```
(This requires that you have cloned this repository with git!)

These image databases are in the same format used by [BoB robotics](https://github.com/BrainsOnBoard/bob_robotics).
