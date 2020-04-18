13 Packages

---

All R functions and datasets are stored in _packages_. Only when a
package is loaded are its contents available. This is done both for
efficiency (the full list would take more memory and would take longer
to search than a subset), and to aid package developers, who are
protected from name clashes with other code. The process of developing
packages is described in [Creating R packages](./R-exts.html#Creating-R-packages) in Writing R Extensions.
Here, we will describe them from a user's point of view.

To see which packages are installed at your site, issue the command

```r
> library()
```

with no arguments. To load a particular package (e.g., the
[**boot**](https://CRAN.R-project.org/package=boot) package containing
functions from Davison & Hinkley (1997)), use a command like

```r
> library(boot)
```

Users connected to the Internet can use the `install.packages()` and
`update.packages()` functions (available through the `Packages` menu in
the Windows and macOS GUIs, see [Installing packages](./R-admin.html#Installing-packages) in R Installation and
Administration) to install and update packages.

To see which packages are currently loaded, use

```r
> search()
```

to display the search list. Some packages may be loaded but not
available on the search list (see [Namespaces](#Namespaces)): these will
be included in the list given by

```r
> loadedNamespaces()
```

To see a list of all available help topics in an installed package, use

```r
> help.start()
```

to start the HTML help system, and then navigate to the package listing
in the `Reference` section.

---

• [Standard packages](#Standard-packages)     
 • [Contributed packages and CRAN](#Contributed-packages-and-CRAN)     
 • [Namespaces](#Namespaces)

---

---

### 13.1 Standard packages

The standard (or _base_) packages are considered part of the R source
code. They contain the basic functions that allow R to work, and the
datasets and standard statistical and graphical functions that are
described in this manual. They should be automatically available in any
R installation. See [R packages](R-FAQ.html#Which-add_002don-packages-exist-for-R_003f) in R
FAQ, for a complete list.

---

### 13.2 Contributed packages and CRAN

There are thousands of contributed packages for R, written by many
different authors. Some of these packages implement specialized
statistical methods, others give access to data or hardware, and others
are designed to complement textbooks. Some (the _recommended_ packages)
are distributed with every binary distribution of R. Most are available
for download from CRAN (<https://CRAN.R-project.org/> and its mirrors)
and other repositories such as Bioconductor
(<https://www.bioconductor.org/>). and Omegahat
(<http://www.omegahat.net/>). The _R FAQ_ contains a list of CRAN
packages current at the time of release, but the collection of available
packages changes very frequently.

---

### 13.3 Namespaces

Packages have _namespaces_, which do three things: they allow the
package writer to hide functions and data that are meant only for
internal use, they prevent functions from breaking when a user (or other
package writer) picks a name that clashes with one in the package, and
they provide a way to refer to an object within a particular package.

For example, `t()` is the transpose function in R, but users might
define their own function named `t`. Namespaces prevent the user's
definition from taking precedence, and breaking every function that
tries to transpose a matrix.

There are two operators that work with namespaces. The double-colon
operator `::` selects definitions from a particular namespace. In the
example above, the transpose function will always be available as
`base::t`, because it is defined in the `base` package. Only functions
that are exported from the package can be retrieved in this way.

The triple-colon operator `:::` may be seen in a few places in R code:
it acts like the double-colon operator but also allows access to hidden
objects. Users are more likely to use the `getAnywhere()` function,
which searches multiple packages.

Packages are often inter-dependent, and loading one may cause others to
be automatically loaded. The colon operators described above will also
cause automatic loading of the associated package. When packages with
namespaces are loaded automatically they are not added to the search
list.

---
