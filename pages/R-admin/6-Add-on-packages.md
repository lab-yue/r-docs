# 6 Add-on packages

---

---

• [Default packages](#Default-packages)     
 • [Managing libraries](#Managing-libraries)     
 • [Installing packages](#Installing-packages)     
 • [Updating packages](#Updating-packages)     
 • [Removing packages](#Removing-packages)     
 • [Setting up a package repository](#Setting-up-a-package-repository)     
 • [Checking installed source packages](#Checking-installed-source-packages)

---

It is helpful to use the correct terminology. A _package_ is loaded from
a _library_ by the function `library()`. Thus a library is a directory
containing installed packages; the main library is
`R_HOME/library`, but others can be used, for example by
setting the environment variable `R_LIBS` or using
the R function `.libPaths()`. To avoid any confusion you will often see
a library directory referred to as a 'library tree'.

---

### 6.1 Default packages

The set of packages loaded on startup is by default

```r
> getOption("defaultPackages")
[1] "datasets"  "utils"     "grDevices" "graphics"  "stats"     "methods"
```

(plus, of course, **base**) and this can be changed by setting the
option in startup code (e.g. in `~/.Rprofile`). It is initially
set to the value of the
environment variable `R_DEFAULT_PACKAGES` if set (as a comma-separated
list). Setting `R_DEFAULT_PACKAGES=NULL` ensures that only package
**base** is loaded.

Changing the set of default packages is normally used to reduce the set
for speed when scripting: in particular not using **methods** will
reduce the start-up time by a factor of up to two. But it can also be
used to customize R, e.g. for class use. `Rscript` also checks the
environment variable `R_SCRIPT_DEFAULT_PACKAGES`;
if set, this takes
precedence over `R_DEFAULT_PACKAGES`.

---

### 6.2 Managing libraries

R packages are installed into _libraries_, which are directories in the
file system containing a subdirectory for each package installed there.

R comes with a single library, `R_HOME/library` which is the
value of the R object '`.Library`' containing the standard and
recommended[^24^](#FOOT24) packages. Both sites and users can
create others and make use of them (or not) in an R session. At the
lowest level '`.libPaths()`' can be used to add paths to the
collection of libraries or to report the current collection.

R will automatically make use of a site-specific library
`R_HOME/site-library` if this exists (it does not in a vanilla
R installation). This location can be overridden by
setting[^25^](#FOOT25) '`.Library.site`' in
`R_HOME/etc/Rprofile.site`, or (not recommended) by setting the
environment variable `R_LIBS_SITE`. Like
'`.Library`', the site libraries are always included by
'`.libPaths()`'.

Users can have one or more libraries, normally specified by the
environment variable `R_LIBS_USER`. This has a default value (to see it,
use '`Sys.getenv("R_LIBS_USER")`' within an R session), but
that is only used if the corresponding directory actually exists (which
by default it will not).

Both `R_LIBS_USER` and `R_LIBS_SITE` can specify multiple library paths,
separated by colons (semicolons on Windows).

---

### 6.3 Installing packages

---

• [Windows packages](#Windows-packages)     
 • [macOS packages](#macOS-packages)     
 • [Customizing package compilation](#Customizing-package-compilation)     
 • [Multiple sub-architectures](#Multiple-sub_002darchitectures)     
 • [Byte-compilation](#Byte_002dcompilation)     
 • [External software](#External-software)

---

Packages may be distributed in source form or compiled binary form.
Installing source packages which contain C/C++/Fortran code requires
that compilers and related tools be installed. Binary packages are
platform-specific and generally need no special tools to install, but
see the documentation for your platform for details.

Note that you may need to specify implicitly or explicitly the library
to which the package is to be installed. This is only an issue if you
have more than one library, of course.

Ensure that the environment variable `TMPDIR` is either unset (and
`/tmp` exists and can be written in and executed from) or is
the absolute path to a valid temporary directory, not containing spaces.

For most users it suffices to call
'`install.packages(pkgname)`' or its GUI equivalent if the
intention is to install a CRAN package and internet access is
available.[^26^](#FOOT26) On most systems
'`install.packages()`' will allow packages to be selected from
a list box (typically with thousands of items).

To install packages from source on a Unix-alike use in a terminal

```r
R CMD INSTALL -l /path/to/library pkg1 pkg2 …
```

The part '`-l /path/to/library`' can be omitted, in which case
the first library of a normal R session is used (that shown by
`.libPaths()[1]`).

There are a number of options available: use `R CMD INSTALL --help` to
see the current list.

Alternatively, packages can be downloaded and installed from within R.
First choose your nearest CRAN mirror using `chooseCRANmirror()`. Then
download and install packages **pkg1** and **pkg2** by

```r
> install.packages(c("pkg1", "pkg2"))
```

The essential dependencies of the specified packages will also be
fetched. Unless the library is specified (argument `lib`) the first
library in the library search path is used: if this is not writable, R
will ask the user (in an interactive session) if the default personal
library should be created, and if allowed to will install the packages
there.

If you want to fetch a package and all those it depends on (in any way)
that are not already installed, use e.g.

```r
> install.packages("Rcmdr", dependencies = TRUE)
```

`install.packages` can install a source package from a local
`.tar.gz` file (or a URL to such a file) by setting argument
`repos` to `NULL`: this will be selected automatically if the name given
is a single `.tar.gz` file.

`install.packages` can look in several repositories, specified as a
character vector by the argument `repos`: these can include a CRAN
mirror, Bioconductor, R-forge, rforge.net, local archives, local files,
...). Function `setRepositories()` can select amongst those repositories
that the R installation is aware of.

Naive users sometimes forget that as well as installing a package, they
have to use `library` to make its functionality available.

---

#### 6.3.1 Windows

What `install.packages` does by default is different on Unix-alikes
(except macOS) and Windows. On Unix-alikes it consults the list of
available _source_ packages on CRAN (or other repository/ies), downloads
the latest version of the package sources, and installs them (via
`R CMD INSTALL`). On Windows it looks (by default) first at the list of
_binary_ versions of packages available for your version of R and
downloads the latest versions (if any). If no binary version is
available or the source version is newer, it will install the source
versions of packages without compiled C/C++/Fortran code, and offer to
do so for those with, if `make` is available (and this can be tuned by
option `"install.packages.compile.from.source"`).

On Windows `install.packages` can also install a binary package from a
local `zip` file (or the URL of such a file) by setting
argument `repos` to `NULL`. `Rgui.exe` has a menu `Packages` with a GUI
interface to `install.packages`, `update.packages` and `library`.

Windows binary packages for R are distributed as a single binary
containing either or both architectures (32- and 64-bit).

A few of the binary packages need other software to be installed on your
system: see for example
<https://CRAN.R-project.org/bin/windows/contrib/3.2/@ReadMe>. Packages
using Gtk+ ([**Cairo**](https://CRAN.R-project.org/package=Cairo),
[**RGtk2**](https://CRAN.R-project.org/package=RGtk2),
[**cairoDevice**](https://CRAN.R-project.org/package=cairoDevice) and
those that depend on them) need the `bin` directory of a
bundled distribution of Gtk2 from
<http://ftp.gnome.org/pub/gnome/binaries/win32/gtk+> or
<http://ftp.gnome.org/pub/gnome/binaries/win64/gtk+> in the path: it
should work to have both 32- and 64-bit Gtk+ `bin` directories
in the path on a 64-bit version of R.

`R CMD INSTALL` works in Windows to install source packages. No
additional tools are needed if the package does not contain compiled
code, and `install.packages(type="source")` will work for such packages
(and for those with compiled code if the tools (see [The Windows toolset](#The-Windows-toolset)) are on the path, and the variables
`BINPREF` and `BINPREF64` are set properly; see the discussion below).
We have seen occasional permission problems after unpacking source
packages on some systems: these have been circumvented by setting the
environment variable `R_INSTALL_TAR` to '`tar.exe`'.

If you have only a source package that is known to work with current R
and just want a binary Windows build of it, you could make use of the
building service offered at <https://win-builder.r-project.org/>.

For almost all packages `R CMD INSTALL` will attempt to install both 32-
and 64-bit builds of a package if run from a 32/64-bit install of R. It
will report success if the installation of the architecture of the
running `R` succeeded, whether or not the other architecture was
successfully installed. The exceptions are packages with a non-empty
`configure.win` script or which make use of
`src/Makefile.win`. If `configure.win` does something
appropriate to both architectures use[^27^](#FOOT27) option
`--force-biarch`: otherwise `R CMD INSTALL --merge-multiarch`
can be applied to a source tarball to merge separate 32- and 64-bit
installs. (This can only be applied to a tarball, and will only succeed
if both installs succeed.)

If you have a package without compiled code and no Windows-specific
help, you can zip up an installation on another OS and install from that
zip file on Windows. However, such a package can be installed from the
sources on Windows without any additional tools.

Packages with compiled code may need to have paths to the compilers set
explicitly, and there is provision to make use of a system-wide library
of installed external software. The compiler paths are set using the
`make` variables `BINPREF` and (usually) `BINPREF64`. The library
location is set using `make` variable `LOCAL_SOFT`, to give an
equivalent of `/usr/local` on a Unix-alike. All of these can be
set in `src/gnuwin32/MkRules.local` when R is built from
sources (see the comments in `src/gnuwin32/MkRules.dist`), or
in file[^28^](#FOOT28) `etc/i386/Makeconf` or
`etc/x64/Makeconf` for an installed version of R. In the latter
case only `BINPREF` is used, with the 64 bit path used in
`etc/x64/Makeconf`. The version used by CRAN can be installed
as described in [Building from source](#Building-from-source).

---

#### 6.3.2 macOS

On macOS (formerly OS X) `install.packages` works as it does on other
Unix-alike systems, but there are additional types starting with
`mac.binary` (available for the CRAN distribution but not when compiling
R from source: `mac.binary.el-capitan` for an 'El Capitan and later'
build with `"default"` a synonym for the appropriate variant) which can
be passed to `install.packages` in order to download and install binary
packages from a suitable repository. These binary package files for
macOS have the extension '`.tgz`'. The [R.APP] GUI
provides menus for installation of either binary or source packages,
from CRAN or local files.

On R builds using binary packages, the default is type `both`: this
looks first at the list of binary packages available for your version of
R and installs the latest versions (if any). If no binary version is
available or the source version is newer, it will install the source
versions of packages without compiled C/C++/Fortran code and offer to do
so for those with, if `make` is available.

Note that most binary packages which include compiled code are tied to a
particular series (e.g. R 3.6.x or 3.5.x) of R.

Installing source packages which do not contain compiled code should
work with no additional tools. For others you will need the 'Command
Line Tools' for `Xcode` and compilers which match those used to build R:
see [macOS](#macOS).

Package [**rJava**](https://CRAN.R-project.org/package=rJava) and those
which depend on it need a Java runtime installed and several packages
need X11 installed, including those using Tk. See [macOS](#macOS) and
[Java (macOS)](#Java-_0028macOS_0029).

Tcl/Tk extensions `BWidget` and `Tktable` are part of the Tcl/Tk
contained in the R installer. These are required by a number of CRAN and
Bioconductor packages.

A few of the binary packages need other software to be installed on your
system. In particular packages using Gtk+
([**RGtk2**](https://CRAN.R-project.org/package=RGtk2),
[**cairoDevice**](https://CRAN.R-project.org/package=cairoDevice) and
those that depend on them) need the GTK framework installed from
<https://mac.R-project.org/libs/>: the appropriate version at the time
of writing was <https://mac.R-project.org/libs/GTK_2.24.17-X11.pkg>

The default compilers specified are shown in file
`/Library/Frameworks/R.framework/Resources/etc/Makeconf`. At
the time of writing these setting assumed that the C, Fortran and C++
compilers were on the path, using `gfortran` 6.1.0 (see
[macOS](#macOS)). The settings can be changed, either by editing that
file or in a file such as `~/.R/Makevars` (see the next
section). Entries which may need to be changed include '`CC`',
'`CXX`', '`FC`', '`FLIBS`' and the
corresponding flags, and perhaps '`CXXCPP`',
'`DYLIB_LD`', '`MAIN_LD`', '`SHLIB_CXXLD`'
and '`SHLIB_LD`', as well as the '`CXX11`',
'`CXX14`' and '`CXX17`' variants

So for example you could select a specific build of `clang` for both C
and C++ with extensive checking by having in `~/.R/Makevars`

```r
CC = /usr/local/clang7/bin/clang
CXX = /usr/local/clang7/bin/clang++
CXX11 = $CXX
CXX14 = $CXX
CXX17 = $CXX
CFLAGS = -g -O2 -Wall -pedantic -Wconversion -Wno-sign-conversion
CXXFLAGS = -g -O2 -Wall -pedantic -Wconversion -Wno-sign-conversion
CXX11FLAGS = $CXXFLAGS
CXX14FLAGS = $CXXFLAGS
CXX17FLAGS = $CXXFLAGS
```

and `gfortran` by (El Capitan)

```r
FC = /usr/local/gfortran/bin/gfortran
FLIBS = -L/usr/local/gfortran/lib/gcc/x86_64-apple-darwin15/6.1.0
  -L/usr/local/gfortran/lib -lgfortran -lquadmath -lm
```

or (Sierra or High Sierra)

```r
FC = /usr/local/gfortran/bin/gfortran
FLIBS = -L/usr/local/gfortran/lib/gcc/x86_64-apple-darwin16/6.3.0
  -L/usr/local/gfortran/lib -lgfortran -lquadmath -lm
```

or (Mojave or later)

```r
FC = /usr/local/gfortran/bin/gfortran
FLIBS = -L/usr/local/gfortran/lib/gcc/x86_64-apple-darwin18/8.2.0
  -L/usr/local/gfortran/lib -lgfortran -lquadmath -lm
```

(with lines broken here for legibility).

If using the C/C++ compilers from the Command Line Tools (which do not
have OpenMP support) one will need to include

```r
SHLIB_OPENMP_CFLAGS =
SHLIB_OPENMP_CXXFLAGS =
```

to compile OpenMP-using packages.

Apple includes many Open Source libraries in macOS but increasingly
without the corresponding headers (not even in Xcode nor the Command
Line Tools): they are often rather old versions. If installing packages
from source using them it is usually easiest to install a
statically-linked up-to-date copy of the Open Source package from its
sources or from <https://mac.R-project.org/libs>. But sometimes it is
desirable/necessary to use Apple's dynamically linked library, in which
case appropriate headers could be extracted from the
sources[^29^](#FOOT29) available _via_
<https://opensource.apple.com>.

---

#### 6.3.3 Customizing package compilation

The R system and package-specific compilation flags can be overridden or
added to by setting the appropriate Make variables in the personal file
`HOME/.R/Makevars-R_PLATFORM` (but
`HOME/.R/Makevars.win` or `HOME/.R/Makevars.win64` on
Windows), or if that does not exist, `HOME/.R/Makevars`, where
'`R_PLATFORM`' is the platform for which R was built, as
available in the `platform` component of the R variable `R.version`. The
path to an alternative personal file[^30^](#FOOT30) can be
specified _via_ the environment variable `R_MAKEVARS_USER`.

Package developers are encouraged to use this mechanism to enable a
reasonable amount of diagnostic messaging ("warnings") when compiling,
such as e.g. `-Wall -pedantic` for tools from GCC, the GNU
Compiler Collection or for `clang`.

Note that this mechanism can also be used when it necessary to change
the optimization level whilst installing a particular package. For
example

```r
## for C code
CFLAGS = -g -O -mtune=native
## for C++ code
CXXFLAGS = -g -O -mtune=native
## for fixed-form Fortran code
FFLAGS = -g -O -mtune=native
```

Another use is to override the settings in a binary installation of R.
For example, to use a different Fortran compiler on macOS

```r
FC = /usr/local/gfortran/bin/gfortran
FLIBS = -L/usr/local/gfortran/lib/gcc/x86_64-apple-darwin16/6.3.0
  -L/usr/local/gfortran/lib -lgfortran -lquadmath -lm
```

(line split for legibility here).

There is also provision for a site-wide `Makevars.site` file
under `R_HOME/etc` (in a sub-architecture-specific directory if
appropriate). This is read immediately after `Makeconf`, and
the path to an alternative file can be specified by environment variable
`R_MAKEVARS_SITE`.

Note that these mechanisms do not work with packages which fail to pass
settings down to sub-makes, perhaps reading `etc/Makeconf` in
makefiles in subdirectories. Fortunately such packages are unusual.

---

#### 6.3.4 Multiple sub-architectures

When installing packages from their sources, there are some extra
considerations on installations which use sub-architectures. These are
commonly used on Windows but can in principle be used on other
platforms.

When a source package is installed by a build of R which supports
multiple sub-architectures, the normal installation process installs the
packages for all sub-architectures. The exceptions are

_Unix-alikes_

: where there is an `configure` script, or a file
`src/Makefile`.

_Windows_

: where there is a non-empty `configure.win` script, or a
file `src/Makefile.win` (with some exceptions where the
package is known to have an architecture-independent
`configure.win`, or if `--force-biarch` or field
'`Biarch`' in the `DESCRIPTION` file is used to
assert so).

In those cases only the current architecture is installed. Further
sub-architectures can be installed by

```r
R CMD INSTALL --libs-only pkg
```

using the path to `R` or `R --arch` to select the additional
sub-architecture. There is also `R CMD INSTALL --merge-multiarch` to
build and merge the two architectures, starting with a source tarball.

---

#### 6.3.5 Byte-compilation

As from R 3.6.0, all packages are by default byte-compiled.

Byte-compilation can be controlled on a per-package basis by the
'`ByteCompile`' field in the `DESCRIPTION` file.

---

#### 6.3.6 External software

Some R packages contain compiled code which links to external software
libraries. Unless the external library is statically linked (which is
done as much as possible for binary packages on Windows and macOS), the
libraries have to be found when the package is loaded and not just when
it is installed. How this should be done depends on the OS (and in some
cases the version).

For Unix-alikes except macOS the primary mechanism is the `ld.so` cache
controlled by `ldconfig`: external dynamic libraries recorded in that
cache will be found. Standard library locations will be covered by the
cache, and well-designed software will add its locations (as for example
**openmpi** does on Fedora). The secondary mechanism is to consult the
environment variable `LD_LIBRARY_PATH`. The R script controls that
variable, and sets it to the concatenation of `R_LD_LIBRARY_PATH`,
`R_JAVA_LD_LIBRARY_PATH` and the environment value of `LD_LIBRARY_PATH`.
The first two have defaults which are normally set when R is installed
(but can be overridden in the environment) so `LD_LIBRARY_PATH` is the
best choice for a user to set.

On macOS the primary mechanism is to embed the absolute path to
dependent dynamic libraries into an object when it is compiled. Few R
packages arrange to do so, but it can be edited[^31^](#FOOT31)
_via_ `install_name_tool` --- that only deals with direct dependencies
and those would also need to be compiled to include the absolute paths
of their dependencies. If the choice of absolute path is to be deferred
to load time, how they are resolved is described in `man dyld`: the role
of `LD_LIBRARY_PATH` is replaced on macOS by `DYLD_LIBRARY_PATH` and
`DYLD_FALLBACK_LIBRARY_PATH`. Running `R CMD otool -L` on the package
shared object will show where (if anywhere) its dependencies are
resolved. `DYLD_FALLBACK_LIBRARY_PATH` is preferred (and it is that
which is manipulated by the R script), but as from 10.11 ('El Capitan')
the default behaviour had been changed for security reasons to discard
these environment variables when invoking a shell script (and
`R` is a shell script). That makes the only portable option to
set `R_LD_LIBRARY_PATH` in the environment, something like

```r
export R_LD_LIBRARY_PATH="`R RHOME`/lib:/opt/local/lib"
```

The precise rules for where Windows looks for DLLs are complex and
depend on the version of Windows. But for present purposes the main
solution is to put the directories containing the DLLs the package links
to (and any those DLLs link to) on the `PATH`. 64-bit versions of
Windows will ignore 32-bit DLLs from 64-bit R and _vice versa_.

The danger with any of the methods which involve setting environment
variables is of inadvertently masking a system library. This is less for
`DYLD_FALLBACK_LIBRARY_PATH` and for _appending_ to `PATH` on Windows
(as it should already contain the system library paths).

---

### 6.4 Updating packages

The command `update.packages()` is the simplest way to ensure that all
the packages on your system are up to date. It downloads the list of
available packages and their current versions, compares it with those
installed and offers to fetch and install any that have later versions
on the repositories.

An alternative interface to keeping packages up-to-date is provided by
the command `packageStatus()`, which returns an object with information
on all installed packages and packages available at multiple
repositories. The `print` and `summary` methods give an overview of
installed and available packages, the `upgrade` method offers to fetch
and install the latest versions of outdated packages.

One sometimes-useful additional piece of information that
`packageStatus()` returns is the status of a package, as `"ok"`,
`"upgrade"` or `"unavailable"` (in the currently selected repositories).
For example

```r
> inst <- packageStatus()$inst
> inst[inst$Status != "ok", c("Package", "Version", "Status")]
                  Package Version      Status
Biobase           Biobase   2.8.0 unavailable
RCurl               RCurl   1.4-2     upgrade
Rgraphviz       Rgraphviz  1.26.0 unavailable
rgdal               rgdal  0.6-27     upgrade
```

---

### 6.5 Removing packages

Packages can be removed in a number of ways. From a command prompt they
can be removed by

```r
R CMD REMOVE -l /path/to/library pkg1 pkg2 …
```

From a running R process they can be removed by

```r
> remove.packages(c("pkg1", "pkg2"),
                  lib = file.path("path", "to", "library"))
```

Finally, one can just remove the package directory from the library.

---

### 6.6 Setting up a package repository

Utilities such as `install.packages` can be pointed at any CRAN-style
repository, and R users may want to set up their own. The 'base' of a
repository is a URL such as <http://www.stats.ox.ac.uk/pub/RWin>: this
must be an URL scheme that `download.packages` supports (which also
includes '`https://`', '`ftp://`' and
'`file://`'). Under that base URL there should be directory
trees for one or more of the following types of package distributions:

- `"source"`: located at `src/contrib` and containing
  `.tar.gz` files. Other forms of compression can be used,
  e.g. `.tar.bz2` or `.tar.xz` files. Complete
  repositories contain the sources corresponding to any binary
  packages, and in any case it is wise to have a
  `src/contrib` area with a possibly empty
  `PACKAGES` file.
- `"win.binary"`: located at `bin/windows/contrib/x.y` for R
  versions `x.y.z` and containing `.zip` files for
  Windows.
- `"mac.binary.el-capitan"`: located at
  `bin/macosx/el-capitan/contrib/3.y` for the CRAN builds for
  'El Capitan (and later) for R versions `3.y.z`,
  containing `.tgz` files.

Each terminal directory must also contain a `PACKAGES` file.
This can be a concatenation of the `DESCRIPTION` files of the
packages separated by blank lines, but only a few of the fields are
needed. The simplest way to set up such a file is to use function
`write_PACKAGES` in the **tools** package, and its help explains which
fields are needed. Optionally there can also be `PACKAGES.rds`
and `PACKAGES.gz` files, downloaded in preference to
`PACKAGES`. (These files will be smaller:
`PACKAGES.rds` is used only from R 3.4.0. If you have a
mis-configured server that does not report correctly non-existent files
you may need these files.)

To add your repository to the list offered by `setRepositories()`, see
the help file for that function.

Incomplete repositories are better specified _via_ a `contriburl`
argument than _via_ being set as a repository.

A repository can contain subdirectories, when the descriptions in the
`PACKAGES` file of packages in subdirectories must include a
line of the form

```r
Path: path/to/subdirectory
```

---once again `write_PACKAGES` is the simplest way to set this up.

---

### 6.7 Checking installed source packages

It can be convenient to run `R CMD check` on an installed package,
particularly on a platform which uses sub-architectures. The outline of
how to do this is, with the source package in directory `pkg`
(or a tarball filename):

```r
R CMD INSTALL -l libdir pkg > pkg.log 2>&1
R CMD check -l libdir --install=check:pkg.log pkg
```

Where sub-architectures are in use the `R CMD check` line can be
repeated with additional architectures by

```r
R --arch arch CMD check -l libdir --extra-arch --install=check:pkg.log pkg
```

where `--extra-arch` selects only those checks which depend on
the installed code and not those which analyse the sources. (If multiple
sub-architectures fail only because they need different settings, e.g.
environment variables, `--no-multiarch` may need to be added to
the `INSTALL` lines.) On Unix-alikes the architecture to run is selected
by `--arch`: this can also be used on Windows with
`R_HOME/bin/R.exe`, but it is more usual to select the path to
the `Rcmd.exe` of the desired architecture.

So on Windows to install, check and package for distribution a source
package from a tarball which has been tested on another platform one
might use

```r
.../bin/i386/Rcmd INSTALL -l libdir tarball --build > pkg.log 2>&1
.../bin/i386/Rcmd check -l libdir --extra-arch --install=check:pkg.log pkg
.../bin/x64/Rcmd check -l libdir --extra-arch --install=check:pkg.log pkg
```

where one might want to run the second and third lines in a different
shell with different settings for environment variables and the path (to
find external software, notably for Gtk+).

`R CMD INSTALL` can do a `i386` install and then add the `x64` DLL from
a single command by

```r
R CMD INSTALL --merge-multiarch -l libdir tarball
```

and `--build` can be added to zip up the installation.

---
