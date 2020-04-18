5 R Add-On Packages

---

---

• [Which add-on packages exist for R?](#Which-add_002don-packages-exist-for-R_003f)     
 • [How can add-on packages be installed?](#How-can-add_002don-packages-be-installed_003f)     
 • [How can add-on packages be used?](#How-can-add_002don-packages-be-used_003f)     
 • [How can add-on packages be removed?](#How-can-add_002don-packages-be-removed_003f)     
 • [How can I create an R package?](#How-can-I-create-an-R-package_003f)     
 • [How can I contribute to R?](#How-can-I-contribute-to-R_003f)

---

---

### 5.1 Which add-on packages exist for R?

---

• [Add-on packages in R](#Add_002don-packages-in-R)     
 • [Add-on packages from CRAN](#Add_002don-packages-from-CRAN)     
 • [Add-on packages from Omegahat](#Add_002don-packages-from-Omegahat)     
 • [Add-on packages from Bioconductor](#Add_002don-packages-from-Bioconductor)     
 • [Other add-on packages](#Other-add_002don-packages)

---

---

#### 5.1.1 Add-on packages in R

The R distribution comes with the following packages:

**base**

: Base R functions (and datasets before R 2.0.0).

**compiler**

: R byte code compiler (added in R 2.13.0).

**datasets**

: Base R datasets (added in R 2.0.0).

**grDevices**

: Graphics devices for base and grid graphics (added in R 2.0.0).

**graphics**

: R functions for base graphics.

**grid**

: A rewrite of the graphics layout capabilities, plus some support for
interaction.

**methods**

: Formally defined methods and classes for R objects, plus other
programming tools, as described in the Green Book.

**parallel**

: Support for parallel computation, including by forking and by
sockets, and random-number generation (added in R 2.14.0).

**splines**

: Regression spline functions and classes.

**stats**

: R statistical functions.

**stats4**

: Statistical functions using S4 classes.

**tcltk**

: Interface and language bindings to Tcl/Tk GUI elements.

**tools**

: Tools for package development and administration.

**utils**

: R utility functions.

These "base packages" were substantially reorganized in R 1.9.0. The
former **base** was split into the four packages **base**, **graphics**,
**stats**, and **utils**. Packages **ctest**, **eda**, **modreg**,
**mva**, **nls**, **stepfun** and **ts** were merged into **stats**,
package **lqs** returned to the recommended package
[**MASS**](https://CRAN.R-project.org/package=MASS), and package **mle**
moved to **stats4**.

---

#### 5.1.2 Add-on packages from CRAN

The CRAN `src/contrib` area contains a wealth of add-on
packages, including the following _recommended_ packages which are to be
included in all binary distributions of R.

**KernSmooth**

: Functions for kernel smoothing (and density estimation)
corresponding to the book "Kernel Smoothing" by M. P. Wand and M. C.
Jones, 1995.

**MASS**

: Functions and datasets from the main package of Venables and Ripley,
"Modern Applied Statistics with S". (Contained in the `VR`
bundle for R versions prior to 2.10.0.)

**Matrix**

: A Matrix package. (Recommended for R 2.9.0 or later.)

**boot**

: Functions and datasets for bootstrapping from the book "Bootstrap
Methods and Their Applications" by A. C. Davison and D. V. Hinkley,
1997, Cambridge University Press.

**class**

: Functions for classification (_k_-nearest neighbor and LVQ).
(Contained in the `VR` bundle for R versions prior to
2.10.0.)

**cluster**

: Functions for cluster analysis.

**codetools**

: Code analysis tools. (Recommended for R 2.5.0 or later.)

**foreign**

: Functions for reading and writing data stored by statistical
software like Minitab, S, SAS, SPSS, Stata, Systat, etc.

**lattice**

: Lattice graphics, an implementation of Trellis Graphics functions.

**mgcv**

: Routines for GAMs and other generalized ridge regression problems
with multiple smoothing parameter selection by GCV or UBRE.

**nlme**

: Fit and compare Gaussian linear and nonlinear mixed-effects models.

**nnet**

: Software for single hidden layer perceptrons ("feed-forward neural
networks"), and for multinomial log-linear models. (Contained in the
`VR` bundle for R versions prior to 2.10.0.)

**rpart**

: Recursive PARTitioning and regression trees.

**spatial**

: Functions for kriging and point pattern analysis from "Modern
Applied Statistics with S" by W. Venables and B. Ripley. (Contained
in the `VR` bundle for R versions prior to 2.10.0.)

**survival**

: Functions for survival analysis, including penalized likelihood.

See the [CRAN contributed packages page](https://CRAN.R-project.org/web/packages/) for more information.

Many of these packages are categorized into [CRAN Task Views](https://CRAN.R-project.org/web/views/), allowing to browse
packages by topic and providing tools to automatically install all
packages for special areas of interest.

Some CRAN packages that do not build out of the box on Windows, require
additional software, or are shipping third party libraries for Windows
cannot be made available on CRAN in form of a Windows binary packages.
Nevertheless, some of these packages are available at the "CRAN extras"
repository at <https://www.stats.ox.ac.uk/pub/RWin/> kindly provided by
Brian D. Ripley. Note that this repository is a default repository for
recent versions of R for Windows.

---

#### 5.1.3 Add-on packages from Omegahat

The [Omega Project for Statistical Computing](http://www.omegahat.net/)
provides a variety of open-source software for statistical applications,
with special emphasis on web-based software, Java, the Java virtual
machine, and distributed computing. A CRAN style R package repository is
available via <http://www.omegahat.net/R/>. See
<http://www.omegahat.net/> for information on most R packages available
from the Omega project.

---

#### 5.1.4 Add-on packages from Bioconductor

[Bioconductor](https://www.bioconductor.org/) is an open source and open
development software project for the analysis and comprehension of
genomic data. Most Bioconductor components are distributed as R add-on
packages. Initially most of the [Bioconductor software packages](https://bioconductor.org/packages/release/BiocViews.html#___Software)
focused primarily on DNA microarray data analysis. As the project has
matured, the functional scope of the software packages broadened to
include the analysis of all types of genomic data, such as SAGE,
sequence, or SNP data. In addition, there are metadata (annotation, CDF
and probe) and experiment data packages. See
<https://www.bioconductor.org/download/> for available packages and a
complete taxonomy via BioC Views.

---

#### 5.1.5 Other add-on packages

Many more packages are available from places other than the three
default repositories discussed above (CRAN, Bioconductor and Omegahat).
In particular, R-Forge provides a CRAN style repository at
<https://R-Forge.R-project.org/>.

More code has been posted to the R-help mailing list, and can be
obtained from the mailing list archive.

---

### 5.2 How can add-on packages be installed?

(Unix-like only.) The add-on packages on CRAN come as gzipped tar files
named `pkg_version.tar.gz`, which may in fact be "bundles" containing
more than one package. Let `path`{.variable} be the path to such a
package file. Provided that `tar` and `gzip` are available on your
system, type

```r
$ R CMD INSTALL path/pkg_version.tar.gz
```

at the shell prompt to install to the library tree rooted at the first
directory in your library search path (see the help page for
`.libPaths()` for details on how the search path is determined).

To install to another tree (e.g., your private one), use

```r
$ R CMD INSTALL -l lib path/pkg_version.tar.gz
```

where `lib`{.variable} gives the path to the library tree to install to.

Even more conveniently, you can install and automatically update
packages from within R if you have access to repositories such as CRAN.
See the help page for `available.packages()` for more information.

---

### 5.3 How can add-on packages be used?

To find out which additional packages are available on your system, type

```r
library()
```

at the R prompt.

This produces something like

> +-----------------------------------------------------------------------+
> | |
> | `r | | Packages in ‘/home/me/lib/R’: | | | | mystuff My own R functions, nicely packaged but not documented | | | | Packages in ‘/usr/local/lib/R/library’: | | | | KernSmooth Functions for kernel smoothing for Wand & Jones (1995) | | MASS Main Package of Venables and Ripley's MASS | | Matrix Sparse and Dense Matrix Classes and Methods | | base The R Base package | | boot Bootstrap R (S-Plus) Functions (Canty) | | class Functions for Classification | | cluster Functions for clustering (by Rousseeuw et al.) | | codetools Code Analysis Tools for R | | datasets The R Datasets Package | | fo | | reign Read Data Stored by Minitab, S, SAS, SPSS, Stata, Systat, | | dBase, ... | | g | | rDevices The R Graphics Devices and Support for Colours and Fonts | | graphics The R Graphics Package | | grid The Grid Graphics Package | | lattice Lattice Graphics | | methods Formal Methods and Classes | | mgcv GAMs with GCV/AIC/REML smoothness estimation and GAMMs | | by PQL | | nlme Linear and Nonlinear Mixed Effects Models | | nnet Feed-forward Neural Networks and Multinomial Log-Linear | | Models | | rpart Recursive Partitioning | | spatial Functions for Kriging and Point Pattern Analysis | | splines Regression Spline Functions and Classes | | stats The R Stats Package | | stats4 Statistical functions using S4 Classes | | survival Survival analysis, including penalised likelihood | | tcltk Tcl/Tk Interface | | tools Tools for Package Development | | utils The R Utils Package | |` |
> | ::: |
> +-----------------------------------------------------------------------+

You can "load" the installed package `pkg`{.variable} by

```r
library(pkg)
```

You can then find out which functions it provides by typing one of

```r
library(help = pkg)
help(package = pkg)
```

You can unload the loaded package `pkg`{.variable} by

```r
detach("package:pkg", unload = TRUE)
```

(where `unload = TRUE` is needed only for packages with a namespace, see
`?unload`).

---

### 5.4 How can add-on packages be removed?

Use

```r
$ R CMD REMOVE pkg_1 … pkg_n
```

to remove the packages `pkg_1`{.variable}, ..., `pkg_n`{.variable} from
the library tree rooted at the first directory given in `R_LIBS` if this
is set and non-null, and from the default library otherwise. (Versions
of R prior to 1.3.0 removed from the default library by default.)

To remove from library `lib`{.variable}, do

```r
$ R CMD REMOVE -l lib pkg_1 … pkg_n
```

---

### 5.5 How can I create an R package?

A package consists of a subdirectory containing a file
`DESCRIPTION` and the subdirectories `R`,
`data`, `demo`, `exec`, `inst`,
`man`, `po`, `src`, and `tests`
(some of which can be missing). The package subdirectory may also
contain files `INDEX`, `NAMESPACE`,
`configure`, `cleanup`, `LICENSE`,
`LICENCE`, `COPYING` and `NEWS`.

See [Creating R packages](./R-exts.html#Creating-R-packages) in Writing
R Extensions, for details.

R version 1.3.0 has added the function `package.skeleton()` which will
set up directories, save data and code, and create skeleton help files
for a set of R functions and datasets.

See [What is CRAN?](#What-is-CRAN_003f), for information on uploading a
package to CRAN.

---

### 5.6 How can I contribute to R?

R is in active development and there is always a risk of bugs creeping
in. Also, the developers do not have access to all possible machines
capable of running R. So, simply using it and communicating problems is
certainly of great value.

The [R Developer Page](https://developer.R-project.org/) acts as an
intermediate repository for more or less finalized ideas and plans for
the R statistical system. It contains (pointers to) TODO lists, RFCs,
various other writeups, ideas lists, and SVN miscellanea.

---
