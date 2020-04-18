2 Installing R under Unix-alikes

---

R will configure and build under most common Unix and Unix-alike
platforms including '`cpu-*-linux-gnu`' for the
'`alpha`', '`arm64`', '`hppa`',
'`ix86`', '`m68k`', '`mips`',
'`mipsel`', '`ppc64`', '`s390`',
'`sparc64`', and '`x86_64`' CPUs,
'`x86_64-apple-darwin`', '`i386-sun-solaris`' and
'`sparc-sun-solaris`' as well as perhaps (it is tested less
frequently on these platforms) '`i386-*-freebsd`',
'`x86_64-*-freebsd`', '`i386-*-netbsd`',
'`x86_64-*-openbsd`' and '`powerpc-ibm-aix6*`'

In addition, binary distributions are available for some common Linux
distributions and for macOS (formerly OS X and Mac OS). See the FAQ for
current details. These are installed in platform-specific ways, so for
the rest of this chapter we consider only building from the sources.

Cross-building is not possible: installing R builds a minimal version of
R and then runs many R scripts to complete the build.

---

• [Simple compilation](#Simple-compilation)     
 • [Help options](#Help-options)     
 • [Making the manuals](#Making-the-manuals)     
 • [Installation](#Installation)     
 • [Uninstallation](#Uninstallation)     
 • [Sub-architectures](#Sub_002darchitectures)     
 • [Other Options](#Other-Options)     
 • [Testing a Unix-alike Installation](#Testing-a-Unix_002dalike-Installation)

---

---

### 2.1 Simple compilation

First review the essential and useful tools and libraries in [Essential
and useful other programs under a
Unix-alike](#Essential-and-useful-other-programs-under-a-Unix_002dalike),
and install those you want or need. Ensure that either
the environment variable `TMPDIR` is either unset (and `/tmp`
exists and can be written in and scripts can be executed from) or points
to the absolute path to a valid temporary directory (one from which
execution of scripts is allowed) which does not contain
spaces.[^3^](#FOOT3)

Choose a directory to install the R tree (R is not just a binary, but
has additional data sets, help files, font metrics etc). Let us call
this place `R_HOME`{.variable}. Untar the source code. This should
create directories `src`, `doc`, and several more
under a top-level directory: change to that top-level directory (At this
point North American readers should consult [Setting paper size](#Setting-paper-size).) Issue the following commands:

```r
./configure
make
```

(See [Using make](#Using-make) if your make is not called
'`make`'.) Users of Debian-based 64-bit
systems[^4^](#FOOT4) may need

```r
./configure LIBnn=lib
make
```

Then check the built system works correctly by

```r
make check
```

Failures are not necessarily problems as they might be caused by missing
functionality, but you should look carefully at any reported
discrepancies. (Some non-fatal errors are expected in locales that do
not support Latin-1, in particular in true `C` locales and non-UTF-8
non-Western-European locales.) A failure in `tests/ok-errors.R`
may indicate inadequate resource limits (see [Running R](#Running-R)).

More comprehensive testing can be done by

```r
make check-devel
```

or

```r
make check-all
```

see file `tests/README` and [Testing a Unix-alike Installation](#Testing-a-Unix_002dalike-Installation) for the
possibilities of doing this in parallel. Note that these checks are only
run completely if the recommended packages are installed.

If the `configure` and `make` commands execute successfully, a
shell-script front-end called `R` will be created and copied to
`R_HOME/bin`. You can link or copy this script to a place where
users can invoke it, for example to `/usr/local/bin/R`. You
could also copy the man page `R.1` to a place where your `man`
reader finds it, such as `/usr/local/man/man1`. If you want to
install the complete R tree to, e.g., `/usr/local/lib/R`, see
[Installation](#Installation). Note: you do not _need_ to install R: you
can run it from where it was built.

You do not necessarily have to build R in the top-level source directory
(say, `TOP_SRCDIR`). To build in `BUILDDIR`, run

```r
cd BUILDDIR
TOP_SRCDIR/configure
make
```

and so on, as described further below. This has the advantage of always
keeping your source tree clean and is particularly recommended when you
work with a version of R from Subversion. (You may need GNU `make` to
allow this, and you will need no spaces in the path to the build
directory. It is unlikely to work if the source directory has previously
been used for a build.)

Now `rehash` if necessary, type [R]{.kbd}, and read the R manuals and
the R FAQ (files `FAQ` or `doc/manual/R-FAQ.html`, or
<https://CRAN.R-project.org/doc/FAQ/R-FAQ.html> which always has the
version for the latest release of R).

Note: if you already have R installed, check that where you installed R
replaces or comes earlier in your path than the previous installation.
Some systems are set up to have `/usr/bin` (the standard place
for a system installation) ahead of `/usr/local/bin` (the
default place for installation of R) in their default path, and some do
not have `/usr/local/bin` on the default path.

---

### 2.2 Help options

R by default provides help pages a plain text displayed in a pager, with
the options (see the help for `help` of displaying help as HTML or PDF.

By default HTML help pages are created when needed rather than being
built at install time.

If you need to disable the server and want HTML help, there is the
option to build HTML pages when packages are installed (including those
installed with R). This is enabled by the `configure` option
`--enable-prebuilt-html`. Whether `R CMD INSTALL` (and hence
`install.packages`) pre-builds HTML pages is determined by looking at
the R installation and is reported by `R CMD INSTALL --help`: it can be
overridden by specifying one of the `INSTALL` options `--html`
or `--no-html`.

The server is disabled by setting the environment variable
`R_DISABLE_HTTPD` to a non-empty
value, either before R is started or within the R session before HTML
help (including `help.start`) is used. It is also possible that system
security measures will prevent the server from being started, for
example if the loopback interface has been disabled. See
`?tools::startDynamicHelp` for more details.

---

### 2.3 Making the manuals

There is a set of manuals that can be built from the sources,

'`fullrefman`'

: Printed versions of all the help pages for base and recommended
packages (around 3600 pages).

'`refman`'

: Printed versions of the help pages for selected base packages
(around 2200 pages)

'`R-FAQ`'

: R FAQ

'`R-intro`'

: "An Introduction to R".

'`R-data`'

: "R Data Import/Export".

'`R-admin`'

: "R Installation and Administration", this manual.

'`R-exts`'

: "Writing R Extensions".

'`R-lang`'

: "The R Language Definition".

To make these (with '`fullrefman`' rather than
'`refman`'), use

```r
make pdf      to create PDF versions
make info     to create info files (not ‘refman’ nor ‘fullrefman’).
```

You will not be able to build any of these unless you have `texi2any`
version 5.1 or later installed, and for PDF you must have `texi2dvi` and
`texinfo.tex` installed (which are part of the GNU **texinfo**
distribution but are, especially `texinfo.tex`, often made part
of the TeX package in re-distributions). The path to `texi2any` can be
set by macro '`TEXI2ANY`' in `config.site`. NB:
`texi2any` require `perl`.

The PDF versions can be viewed using any recent PDF viewer: they have
hyperlinks that can be followed. The info files are suitable for reading
online with Emacs or the standalone GNU `info` program. The PDF versions
will be created using the paper size selected at configuration (default
ISO a4): this can be overridden by setting `R_PAPERSIZE`
on the `make` command line, or setting
`R_PAPERSIZE` in the environment and using `make -e`. (If re-making the
manuals for a different paper size, you should first delete the file
`doc/manual/version.texi`. The usual value for North America
would be '`letter`'.)

There are some issues with making the PDF reference manual,
`fullrefman.pdf` or `refman.pdf`. The help files
contain both ISO Latin1 characters (e.g. in `text.Rd`) and
upright quotes, neither of which are contained in the standard LaTeX
Computer Modern fonts. We have provided four alternatives:

`times`

: (The default.) Using standard PostScript fonts, Times Roman,
Helvetica and Courier. This works well both for on-screen viewing
and for printing. One disadvantage is that the Usage and Examples
sections may come out rather wide: this can be overcome by using _in
addition_ either of the options `inconsolata` (on a Unix-alike only
if found by `configure`) or `beramono`, which replace the Courier
monospaced font by Inconsolata or Bera Sans mono respectively. (You
will need a recent version of the appropriate LaTeX package
**inconsolata**[^5^](#FOOT5) or **bera** installed.)

    Note that in most LaTeX installations this will not actually use the
    standard fonts for PDF, but rather embed the URW clones NimbusRom,
    NimbusSans and (for Courier, if used) NimbusMon.

    This needs LaTeX packages **times**, **helvetic** and (if used)
    **courier** installed.

`lm`

: Using the _Latin Modern_ fonts. These are not often installed as
part of a TeX distribution, but can obtained from
<https://www.ctan.org/tex-archive/fonts/ps-type1/lm/> and mirrors.
This uses fonts rather similar to Computer Modern, but is not so
good on-screen as `times`.

`cm-super`

: Using type-1 versions of the Computer Modern fonts by Vladimir
Volovich. This is a large installation, obtainable from
<https://www.ctan.org/tex-archive/fonts/ps-type1/cm-super/> and its
mirrors. These type-1 fonts have poor hinting and so are nowhere
near as readable on-screen as the other three options.

`ae`

: A package to use composites of Computer Modern fonts. This works
well most of the time, and its PDF is more readable on-screen than
the previous two options. There are three fonts for which it will
need to use bitmapped fonts, `tctt0900.600pk`,
`tctt1000.600pk` and `tcrm1000.600pk`.
Unfortunately, if those files are not available, Acrobat Reader will
substitute completely incorrect glyphs so you need to examine the
logs carefully.

The default can be overridden by setting the environment variable
`R_RD4PDF`. (On Unix-alikes, this will be picked
up at install time and stored in `etc/Renviron`, but can still
be overridden when the manuals are built, using `make -e`.) The
usual[^6^](#FOOT6) default value for `R_RD4PDF` is
'`times,inconsolata,hyper`': omit '`hyper`' if you do
not want hyperlinks (e.g. for printing the manual) or do not have LaTeX
package **hyperref**, and omit '`inconsolata`' if you do not
have LaTeX package **inconsolata** installed.

Further options, e.g for **hyperref**, can be included in a file
`Rd.cfg` somewhere on your LaTeX search path. For example, if
you prefer to hyperlink the text and not the page number in the table of
contents use

```r
\ifthenelse{\boolean{Rd@use@hyper}}{\hypersetup{linktoc=section}}{}
```

or

```r
\ifthenelse{\boolean{Rd@use@hyper}}{\hypersetup{linktoc=all}}{}
```

to hyperlink both text and page number.

Ebook versions of most of the manuals in one or both of `.epub`
and `.mobi` formats can be made by running in
`doc/manual` one of

```r
make ebooks
make epub
make mobi
```

This requires `ebook-convert` from `Calibre`
(<http://calibre-ebook.com/download>), or from most Linux distributions.
If necessary the path to `ebook-convert` can be set as make macro
`EBOOK` to by editing `doc/manual/Makefile` (which contains a
commented value suitable for macOS) or using `make -e`.

---

### 2.4 Installation

To ensure that the installed tree is usable by the right group of users,
set `umask` appropriately (perhaps to '`022`') before unpacking
the sources and throughout the build process.

After

```r
./configure
make
make check
```

(or, when building outside the source, `TOP_SRCDIR/configure`, etc) have
been completed successfully, you can install the complete R tree to your
system by typing

```r
make install
```

A parallel make can be used (but run `make` before `make install`).
Those using GNU `make` 4.0 or later may want to use `make -j n -O` to
avoid interleaving of output.

This will install to the following directories:

`prefix/bin` or `bindir`

: the front-end shell script and other scripts and executables

`prefix/man/man1` or `mandir/man1`

: the man page

`prefix/LIBnn/R` or `libdir/R`

: all the rest (libraries, on-line help system, ...). Here
`LIBnn`{.variable} is usually '`lib`', but may be
'`lib64`' on some 64-bit Linux systems. This is known as
the R home directory.

where `prefix`{.variable} is determined during configuration (typically
`/usr/local`) and can be set by running `configure` with the
option `--prefix`, as in

```r
./configure --prefix=/where/you/want/R/to/go
```

where the value should be an absolute path. This causes `make install`
to install the R script to `/where/you/want/R/to/go/bin`, and
so on. The prefix of the installation directories can be seen in the
status message that is displayed at the end of `configure`. The
installation may need to be done by the owner of `prefix`,
often a root account.

There is the option of using `make install-strip` (see [Debugging Symbols](#Debugging-Symbols)).

You can install into another directory tree by using

```r
make prefix=/path/to/here install
```

at least with GNU `make` (but not some other Unix makes).

More precise control is available at configure time via options: see
`configure --help` for details. (However, most of the 'Fine tuning of
the installation directories' options are not used by R.)

Configure options `--bindir` and `--mandir` are
supported and govern where a copy of the `R` script and the `man` page
are installed.

The configure option `--libdir` controls where the main R files
are installed: the default is '`eprefix/LIBnn`', where
`eprefix`{.variable} is the prefix used for installing
architecture-dependent files, defaults to `prefix`{.variable}, and can
be set via the configure option `--exec-prefix`.

Each of `bindir`, `mandir` and `libdir` can also be specified on the
`make install` command line (at least for GNU `make`).

The `configure` or `make` variables `rdocdir` and `rsharedir` can be
used to install the system-independent `doc` and
`share` directories to somewhere other than `libdir`. The C
header files can be installed to the value of `rincludedir`: note that
as the headers are not installed into a subdirectory you probably want
something like `rincludedir=/usr/local/include/R-3.6.3`.

If you want the R home to be something other than `libdir/R`,
use `rhome`: for example

```r
make install rhome=/usr/local/lib64/R-3.6.3
```

will use a version-specific R home on a non-Debian Linux 64-bit system.

If you have made R as a shared/static library you can install it in your
system's library directory by

```r
make prefix=/path/to/here install-libR
```

where `prefix` is optional, and `libdir` will give more precise
control.[^7^](#FOOT7) However, you should not install to a
directory mentioned in `LDPATHS` (e.g. `/usr/local/lib64`) if
you intend to work with multiple versions of R, since that directory may
be given precedence over the `lib` directory of other R
installations.

```r
make install-strip
```

will install stripped executables, and on platforms where this is
supported, stripped libraries in directories `lib` and
`modules` and in the standard packages.

Note that installing R into a directory whose path contains spaces is
not supported, and some aspects (such as installing source packages)
will not work.

To install info and PDF versions of the manuals, use one or both of

```r
make install-info
make install-pdf
```

Once again, it is optional to specify `prefix`, `libdir` or `rhome` (the
PDF manuals are installed under the R home directory).

More precise control is possible. For info, the setting used is that of
`infodir` (default `prefix/info`, set by configure option
`--infodir`). The PDF files are installed into the R
`doc` tree, set by the `make` variable `rdocdir`.

A staged installation is possible, that it is installing R into a
temporary directory in order to move the installed tree to its final
destination. In this case `prefix` (and so on) should reflect the
final destination, and `DESTDIR` should be used: see
<https://www.gnu.org/prep/standards/html_node/DESTDIR.html>.

You can optionally install the run-time tests that are part of
`make check-all` by

```r
make install-tests
```

which populates a `tests` directory in the installation.

---

### 2.5 Uninstallation

You can uninstall R by

```r
make uninstall
```

optionally specifying `prefix` etc in the same way as specified for
installation.

This will also uninstall any installed manuals. There are specific
targets to uninstall info and PDF manuals in file
`doc/manual/Makefile`.

Target `uninstall-tests` will uninstall any installed tests, as well as
removing the directory `tests` containing the test results.

An installed shared/static `libR` can be uninstalled by

```r
make prefix=/path/to/here uninstall-libR
```

---

### 2.6 Sub-architectures

Some platforms can support closely related builds of R which can share
all but the executables and dynamic objects. Examples include builds
under Linux and Solaris for different CPUs or 32- and 64-bit builds.

R supports the idea of architecture-specific builds, specified by adding
'`r_arch=name`' to the `configure` line. Here `name`{.variable}
can be anything non-empty, and is used to name subdirectories of
`lib`, `etc`, `include` and the package
`libs` subdirectories. Example names from other software are
the use of `sparcv9` on Sparc Solaris and `32` by
`gcc` on '`x86_64`' Linux.

If you have two or more such builds you can install them over each other
(and for 32/64-bit builds on one architecture, one build can be done
without '`r_arch`'). The space savings can be considerable: on
'`x86_64`' Linux a basic install (without debugging symbols)
took 74Mb, and adding a 32-bit build added 6Mb. If you have installed
multiple builds you can select which build to run by

```r
R --arch=name
```

and just running '`R`' will run the last build that was
installed.

`R CMD INSTALL` will detect if more than one build is installed and try
to install packages with the appropriate library objects for each. This
will not be done if the package has an executable `configure` script or
a `src/Makefile` file. In such cases you can install for extra
builds by

```r
R --arch=name CMD INSTALL --libs-only pkg1 pkg2 …
```

If you want to mix sub-architectures compiled on different platforms
(for example '`x86_64`' Linux and '`i686`' Linux), it
is wise to use explicit names for each, and you may also need to set
`libdir` to ensure that they install into the same place.

When sub-architectures are used the version of `Rscript` in e.g.
`/usr/bin` will be the last installed, but
architecture-specific versions will be available in e.g.
`/usr/lib64/R/bin/exec${R_ARCH}`. Normally all installed
architectures will run on the platform so the architecture of `Rscript`
itself does not matter. The executable `Rscript` will run the `R`
script, and at that time the setting of the
`R_ARCH` environment variable determines the architecture which is run.

When running post-install tests with sub-architectures, use

```r
R --arch=name CMD make check[-devel|all]
```

to select a sub-architecture to check.

Sub-architectures are also used on Windows, but by selecting executables
within the appropriate `bin` directory,
`R_HOME/bin/i386` or `R_HOME/bin/x64`. For backwards
compatibility there are executables `R_HOME/bin/R.exe` and
`R_HOME/bin/Rscript.exe`: these will run an executable from one
of the subdirectories, which one being taken first from the
`R_ARCH` environment variable, then from the
`--arch` command-line option[^8^](#FOOT8) and finally
from the installation default (which is 32-bit for a combined 32/64 bit
R installation).

---

• [Multilib](#Multilib)

---

---

#### 2.6.1 Multilib

For some Linux distributions[^9^](#FOOT9), there is an
alternative mechanism for mixing 32-bit and 64-bit libraries known as
_multilib_. If the Linux distribution supports multilib, then parallel
builds of R may be installed in the sub-directories `lib`
(32-bit) and `lib64` (64-bit). The build to be run may then be
selected using the `setarch` command. For example, a 32-bit build may be
run by

```r
setarch i686 R
```

The `setarch` command is only operational if both 32-bit and 64-bit
builds are installed. If there is only one installation of R, then this
will always be run regardless of the architecture specified by the
`setarch` command.

There can be problems with installing packages on the non-native
architecture. It is a good idea to run e.g. `setarch i686 R` for
sessions in which packages are to be installed, even if that is the only
version of R installed (since this tells the package installation code
the architecture needed).

There is a potential problem with packages using Java, as the
post-install for a '`i686`' RPM on '`x86_64`' Linux
reconfigures Java and will find the '`x86_64`' Java. If you
know where a 32-bit Java is installed you may be able to run (as root)

```r
export JAVA_HOME=<path to jre directory of 32-bit Java>
setarch i686 R CMD javareconf
```

to get a suitable setting.

When this mechanism is used, the version of `Rscript` in e.g.
`/usr/bin` will be the last installed, but an
architecture-specific version will be available in e.g.
`/usr/lib64/R/bin`. Normally all installed architectures will
run on the platform so the architecture of `Rscript` does not matter.

---

### 2.7 Other Options

There are many other installation options, most of which are listed by
`configure --help`. Almost all of those not listed elsewhere in this
manual are either standard `autoconf` options not relevant to R or
intended for specialist uses by the R developers.

One that may be useful when working on R itself is the option
`--disable-byte-compiled-packages`, which ensures that the base
and recommended packages are not byte-compiled. (Alternatively the (make
or environment) variable `R_NO_BASE_COMPILE` can be set to a non-empty
value for the duration of the build.)

Option `--with-internal-tzcode` makes use of R's own code and
copy of the Olson database for managing timezones. This will be
preferred where there are issues with the system implementation, usually
involving times after 2037 or before 1916. An alternative time-zone
directory[^10^](#FOOT10) can be used, pointed to by environment
variable `TZDIR`: this should contain files such as
`Europe/London`. On all tested OSes the system timezone was
deduced correctly, but if necessary it can be set as the value of
environment variable `TZ`.

---

• [Debugging Symbols](#Debugging-Symbols)     
 • [OpenMP Support](#OpenMP-Support)     
 • [C++ Support](#C_002b_002b-Support)     
 • [Link-Time Optimization](#Link_002dTime-Optimization)

---

---

#### 2.7.1 Debugging Symbols

By default, `configure` adds a flag (usually `-g`) to the
compilation flags for C, Fortran and CXX sources. This will slow down
compilation and increase object sizes of both R and packages, so it may
be a good idea to change those flags (set '`CFLAGS`' etc in
`config.site` before configuring, or edit files
`Makeconf` and `etc/Makeconf` between running
`configure` and `make`).

Having debugging symbols available is useful both when running R under a
debugger (e.g., `R -d gdb`) and when using sanitizers and `valgrind`,
all things intended for experts.

Debugging symbols (and some others) can be 'stripped' on installation by
using

```r
make install-strip
```

How well this is supported depends on the platform: it works best on
those using GNU `binutils`. On '`x86_64`' Linux a typical
reduction in overall size was from 92MB to 66MB. On macOS debugging
symbols are not by default included in `.dylib` and
`.so` files, so there is negligible difference.

---

#### 2.7.2 OpenMP Support

By default `configure` searches for suitable
flags[^11^](#FOOT11) for OpenMP support for the C, C++ (default
standard) and Fortran compilers.

Only the C result is currently used for R itself, and only if
`MAIN_LD`/`DYLIB_LD` were not specified. This can be overridden by
specifying

```r
R_OPENMP_CFLAGS
```

Use for packages has similar restrictions (involving `SHLIB_LD` and
similar: note that as Fortran code is by default linked by the C (or
C++) compiler, both need to support OpenMP) and can be overridden by
specifying some of

```r
SHLIB_OPENMP_CFLAGS
SHLIB_OPENMP_CXXFLAGS
SHLIB_OPENMP_FFLAGS
```

Setting these to an empty value will disable OpenMP for that compiler
(and configuring with `--disable-openmp` will disable all
detection[^12^](#FOOT12) of OpenMP). The `configure` detection
test is to compile and link a standalone OpenMP program, which is not
the same as compiling a shared object and loading it into the C program
of R's executable. Note that overridden values are not tested.

---

#### 2.7.3 C++ Support

C++ is not used by R itself, but support is provided for installing
packages with C++ code via `make` macros defined in file
`etc/Makeconf` (and with explanations in file
`config.site`):

```r
CXX
CXXFLAGS
CXXPICFLAGS
CXXSTD

CXX11
CXX11STD
CXX11FLAGS
CXX11PICFLAGS

CXX14
CXX14STD
CXX14FLAGS
CXX14PICFLAGS

CXX17
CXX17STD
CXX17FLAGS
CXX17PICFLAGS
```

The macros `CXX` etc are those used by default for C++ code. `configure`
will attempt to set the rest suitably, choosing for `CXX11STD` a
suitable flag such as `-std=c++11` for C++11 support.
Similarly, configure will if possible choose for `CXX14STD` a
flag[^13^](#FOOT13) such as `-std=c++14` for C++14
support and `-std=c++17` or `-std=c++1z` for support
for the C++17 standard. The inferred values can be overridden in file
`config.site` or on the `configure` command line: user-supplied
values will be tested by compiling some C++11/14/17 code.

R versions 3.1.0 to 3.3.3 used `CXX1X` rather than `CXX11`: these forms
were deprecated in 3.4.4 and removed in 3.6.0.

It may be[^14^](#FOOT14) that there is no suitable flag for
C++11 support, in which case a different compiler could be selected for
`CXX11` and its corresponding flags. Likewise, a different compiler can
be specified for C++14 support with `CXX14` and for C++17 support with
`CXX17`.

The `-std` flag is supported by the GCC, `clang++`, Intel and
Solaris compilers (the latter from version 12.4). Currently accepted
values are (plus some synonyms)

```r
g++:     c++98 gnu++98 c++11 gnu+11 c++14 gnu++14 c++17 gnu++17
Intel:   gnu+98 c++11 c++14 (from 16.0) c++17 (from 17.0)
Solaris: c++03 c++11 c++14 (from 12.5)
```

(Those for `clang++` are not documented, but seem to be based on `g++`.)
Versions 4.3.x to 4.8.x of `g++` accepted flag `-std=c++0x`
with partial support[^15^](#FOOT15) for C++11: this is
currently still accepted as a deprecated synonym for
`-std=c++11`. (At least for versions 4.8.x it has sufficient
support to be picked by `configure`.) Option `-std=c++14` was
introduced in version 5.x.

'Standards' for `g++` starting with '`gnu`' enable 'GNU
extensions': what those are is hard to track down.

For the use of C++11 and later in R packages see the 'Writing R
Extensions' manual. Prior to R 3.6.0 the default C++ standard was that
of the compiler used: currently it is C++11 if supported by the
compiler: this can be overridden by setting '`CXXSTD`' when R
is configured, for example to '`-std=gnu++14`'.

---

#### 2.7.4 Link-Time Optimization

There is support for using link-time optimization (LTO) if the toolchain
supports it: configure with flag `--enable-lto`.

Whether toolchains support LTO is often unclear: all of the C compiler,
the Fortran compiler and linker have to support it, and support it by
the same mechanism (so mixing compiler families may not work and a
non-system linker such as `gold`[^16^](#FOOT16) may be needed).
It has been tested recently on Linux with `gcc`/`gfortran` 8.x and 9.x:
that needed setting

```r
AR=gcc-ar
RANLIB=gcc-ranlib
```

(e.g. in `config.site`). For non-system compilers or if those
wrappers have not been installed one may need something like

```r
AR="ar --plugin=/path/to/liblto_plugin.so"
RANLIB="ranlib --plugin=/path/to/liblto_plugin.so"
```

amd it may be needed to set `NM` similarly.

Unfortunately `--enable-lto` may be accepted but silently do
nothing if some of the toolchain does not support LTO: that has happened
on macOS.

When LTO is enabled it is used for compiled code in packages (including
the recommended packages) unless the flag `--enable-lto=R` is
used. With sufficient diagnostic flags (e.g. `-Wall` in GCC)
this can flag inconsistencies between source files in a package.

Under some circumstances and for a few packages, the PIC flags have
needed overriding on Linux with GCC 9: e.g in `config.site`:

```r
CPICFLAGS=-fPIC
CXXPICFLAGS=-fPIC
CXX11PICFLAGS=-fPIC
CXX14PICFLAGS=-fPIC
CXX17PICFLAGS=-fPIC
FPICFLAGS=-fPIC
```

LTO support was added in 2011 for `gcc` 4.5.x on Linux but was little
used before 2019.

With `gcc`/`gfortran` 9.x[^17^](#FOOT17) this will flag
inconsistencies in calls to Fortran subroutines/functions, both between
Fortran source files and between Fortran and C/C++. `gfortran`
9.2[^18^](#FOOT18) can help understanding these by extracting C
prototypes from Fortran source files with its
`-fc-prototypes-external` option, e.g. that (at the time of
writing) Fortran `LOGICAL` corresponds to `int_least32_t *`.

---

### 2.8 Testing an Installation

Full post-installation testing is possible only if the test files have
been installed with

```r
make install-tests
```

which populates a `tests` directory in the installation.

If this has been done, two testing routes are available. The first is to
move to the home directory of the R installation (as given by `R RHOME`
or from R as `R.home()`) and run

```r
cd tests
## followed by one of
../bin/R CMD make check
../bin/R CMD make check-devel
../bin/R CMD make check-all
```

and other useful targets are `test-BasePackages` and `test-Recommended`
to run tests of the standard and recommended packages (if installed)
respectively.

This re-runs all the tests relevant to the installed R (including for
example the code in the package vignettes), but not for example the ones
checking the example code in the manuals nor making the standalone Rmath
library. This can occasionally be useful when the operating environment
has been changed, for example by OS updates or by substituting the BLAS
(see [Shared BLAS](#Shared-BLAS)).

Parallel checking of packages may be possible: set the environment
variable `TEST_MC_CORES` to the maximum number of processes to be run in
parallel. This affects both checking the package examples (part of
`make check`) and package sources (part of `make check-devel` and
`make check-recommended`). It does require a `make` command which
supports the `make -j n` option: most do but on Solaris you need to
select GNU `make` or `dmake`.

Alternatively, the installed R can be run, preferably with
`--vanilla`. Then

```r
Sys.setenv(LC_COLLATE = "C", LC_TIME = "C", LANGUAGE = "en")
tools::testInstalledBasic("both")
tools::testInstalledPackages(scope = "base")
tools::testInstalledPackages(scope = "recommended")
```

runs the basic tests and then all the tests on the standard and
recommended packages. These tests can be run from anywhere: the basic
tests write their results in the `tests` folder of the R home
directory and run fewer tests than the first approach: in particular
they do not test things which need Internet access---that can be tested
by

```r
tools::testInstalledBasic("internet")
```

These tests work best if `diff` (in `Rtools*.exe` for Windows
users) is in the path.

It is possible to test the installed packages (but not their
package-specific tests) by `testInstalledPackages` even if
`make install-tests` was not run.

Note that the results may depend on the language set for times and
messages: for maximal similarity to reference results you may want to
try setting (before starting the R session)

```r
LANGUAGE=en
```

and use a UTF-8 or Latin-1 locale.

---
