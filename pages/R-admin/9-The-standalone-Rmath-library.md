9 The standalone Rmath library

---

The routines supporting the distribution and
special[^39^](#FOOT39) functions in R and a few others are
declared in C header file `Rmath.h`. These can be compiled into
a standalone library for linking to other applications. (Note that they
are not a separate library when R is built, and the standalone version
differs in several ways.)

The makefiles and other sources needed are in directory
`src/nmath/standalone`, so the following instructions assume
that is the current working directory (in the build directory tree on a
Unix-alike if that is separate from the sources).

`Rmath.h` contains '`R_VERSION_STRING`', which is a
character string containing the current R version, for example
`"3.6.0"`.

There is full access to R's handling of `NaN`, `Inf` and `-Inf` via
special versions of the macros and functions

```r
    ISNAN, R_FINITE, R_log, R_pow and R_pow_di
```

and (extern) constants `R_PosInf`, `R_NegInf` and `NA_REAL`.

There is no support for R's notion of missing values, in particular not
for `NA_INTEGER` nor the distinction between `NA` and `NaN` for doubles.

A little care is needed to use the random-number routines. You will need
to supply the uniform random number generator

```r
    double unif_rand(void)
```

or use the one supplied (and with a shared library or DLL you may have
to use the one supplied, which is the Marsaglia-multicarry with an entry
point

```r
    set_seed(unsigned int, unsigned int)
```

to set its seeds).

The facilities to change the normal random number generator are
available through the constant `N01_kind`. This takes values from the
enumeration type

```r
typedef enum {
    BUGGY_KINDERMAN_RAMAGE,
    AHRENS_DIETER,
    BOX_MULLER,
    USER_NORM,
    INVERSION,
    KINDERMAN_RAMAGE
} N01type;
```

(and '`USER_NORM`' is not available).

---

• [Unix-alike standalone](#Unix_002dalike-standalone)     
 • [Windows standalone](#Windows-standalone)

---

---

### 9.1 Unix-alikes

If R has not already been made in the directory tree, `configure` must
be run as described in the main build instructions.

Then (in `src/nmath/standalone`)

```r
make
```

will make standalone libraries `libRmath.a` and
`libRmath.so` (`libRmath.dylib` on macOS):
'`make static`' and '`make shared`' will create just
one of them.

To use the routines in your own C or C++ programs, include

```r
#define MATHLIB_STANDALONE
#include <Rmath.h>
```

and link against '`-lRmath`' (and '`-lm`' if needed on
your OS). The example file `test.c` does nothing useful, but is
provided to test the process (via `make test`). Note that you will
probably not be able to run it unless you add the directory containing
to the
`LD_LIBRARY_PATH` environment variable (`libRmath.dylib`,
`DYLD_FALLBACK_LIBRARY_PATH` on macOS).

The targets

```r
make install
make uninstall
```

will (un)install the header `Rmath.h` and shared and static
libraries (if built). Both `prefix=` and `DESTDIR`
are supported, together with more precise control as described for the
main build.

'`make install`' installs a file for `pkg-config` to use by
e.g.

```r
$(CC) `pkg-config --cflags libRmath` -c test.c
$(CC) `pkg-config --libs libRmath` test.o -o test
```

On some systems '`make install-strip`' will install a stripped
shared library.

---

### 9.2 Windows

You need to set up[^40^](#FOOT40) almost all the tools to make
R and then run (in a Unix-like shell)

```r
(cd ../../gnuwin32; make MkRules)
(cd ../../include; make -f Makefile.win config.h Rconfig.h Rmath.h)
make -f Makefile.win
```

Alternatively, in a `cmd.exe` shell use

```r
cd ../../include
make -f Makefile.win config.h Rconfig.h Rmath.h
cd ../nmath/standalone
make -f Makefile.win
```

This creates a static library `libRmath.a` and a DLL
`Rmath.dll`. If you want an import library
`libRmath.dll.a` (you don't need one), use

```r
make -f Makefile.win shared implib
```

To use the routines in your own C or C++ programs using MinGW-w64,
include

```r
#define MATHLIB_STANDALONE
#include <Rmath.h>
```

and link against '`-lRmath`'. This will use the first found of
`libRmath.dll.a`, `libRmath.a` and
`Rmath.dll` in that order, so the result depends on which files
are present. You should be able to force static or dynamic linking _via_

```r
-Wl,-Bstatic -lRmath -Wl,Bdynamic
-Wl,-Bdynamic -lRmath
```

or by linking to explicit files (as in the '`test`' target in
`Makefile.win`: this makes two executables, `test.exe`
which is dynamically linked, and `test-static.exe`, which is
statically linked).

It is possible to link to `Rmath.dll` using other compilers,
either directly or via an import library: if you make a MinGW-w64 import
library as above, you will create a file `Rmath.def` which can
be used (possibly after editing) to create an import library for other
systems such as Visual C++.

If you make use of dynamic linking you should use

```r
#define MATHLIB_STANDALONE
#define RMATH_DLL
#include <Rmath.h>
```

to ensure that the constants like `NA_REAL` are linked correctly.
(Auto-import will probably work with MinGW-w64, but it is better to be
sure. This is likely to also work with VC++, Borland and similar
compilers.)

---

## Appendix A Essential and useful other programs under a Unix-alike

This appendix gives details of programs you will need to build R on
Unix-like platforms, or which will be used by R if found by `configure`.

Remember that some package management systems (such as RPM and
Debian/Ubuntu's) make a distinction between the user version of a
package and the development version. The latter usually has the same
name but with the extension '`-devel`' or '`-dev`':
you need both versions installed.

---

• [Essential programs and libraries](#Essential-programs-and-libraries)     
 • [Useful libraries and programs](#Useful-libraries-and-programs)     
 • [Linear algebra](#Linear-algebra)

---

---

### A.1 Essential programs and libraries

You need a means of compiling C and Fortran 90 (see [Using Fortran](#Using-Fortran)). Your C compiler should be
ISO/IEC 60059[^41^](#FOOT41), POSIX 1003.1 and
C99-compliant.[^42^](#FOOT42) R tries to choose suitable
flags[^43^](#FOOT43) for the C compilers it knows about, but
you may have to set `CC` or `CFLAGS` suitably. For versions of `gcc`
prior to 5.1 with `glibc`-based Linux this means including
`-std=gnu99`[^44^](#FOOT44). (Note that options
essential to run the compiler even for linking, such as those to set the
architecture, should be specified as part of `CC` rather than in
`CFLAGS`.)

Unless you do not want to view graphs on-screen (or use macOS) you need
'`X11`' installed, including its headers and client libraries.
For recent Fedora/RedHat distributions it means (at least) RPMs
'`libX11`', '`libX11-devel`', '`libXt`' and
'`libXt-devel`'. On Debian/Ubuntu we recommend the meta-package
'`xorg-dev`'. If you really do not want these you will need to
explicitly configure R without X11, using `--with-x=no`.

The command-line editing (and command completion) depends on the GNU
`readline` library (including its headers): version 4.2 or later is
needed for all the features to be enabled. Otherwise you will need to
configure with `--with-readline=no` (or equivalent).

A suitably comprehensive `iconv` function is essential. The R usage
requires `iconv` to be able to translate between `"latin1"` and
`"UTF-8"`, to recognize `""` (as the current encoding) and `"ASCII"`,
and to translate to and from the Unicode wide-character formats
`"UCS-[24][BL]E"` --- this is true by default for
`glibc`[^45^](#FOOT45) but not of most commercial Unixes.
However, you can make use of GNU `libiconv` (as used on macOS: see
<https://www.gnu.org/software/libiconv/>).

The OS needs to have enough support[^46^](#FOOT46) for
wide-character types: this is checked at configuration. Some C99
functions[^47^](#FOOT47) are required and checked for at
configuration. A small number of POSIX functions[^48^](#FOOT48)
are essential, and others[^49^](#FOOT49) will be used if
available.

Installations of `zlib` (version 1.2.5 or later), `libbz2` (version
1.0.6 or later: called **bzip2-libs**/**bzip2-devel** or
**libbz2-1.0**/**libbz2-dev** by some Linux distributions) and
`liblzma`[^50^](#FOOT50) version 5.0.3 or later are required.

PCRE[^51^](#FOOT51) (version 8.32 or later, although versions
8.20--8.31 will be accepted with a deprecation warning) is required (or
just its library and headers if packaged separately). Only the '8-bit'
interface is used (and only that is built by default when installing
from sources). PCRE must be built with UTF-8 support (not the default,
and checked by `configure`) and support for Unicode properties is
assumed by some R packages. JIT support (optionally available) is
desirable for the best performance: support for this and Unicode
properties can be checked at run-time by calling `pcre_config()`. If
building PCRE for use with R a suitable `configure` command might be

```r
./configure --enable-utf --enable-unicode-properties --enable-jit --disable-cpp
```

The `--enable-jit` flag is supported for most common CPUs. (See
also the comments for Solaris.)

Library `libcurl` (version 7.22.0 or later[^52^](#FOOT52)) is
required, with at least 7.28.0 being desirable. Information on `libcurl`
is found from the `curl-config` script: if that is missing or needs to
be overridden[^53^](#FOOT53) there are macros to do so
described in file `config.site`.

A `tar` program is needed to unpack the sources and packages (including
the recommended packages). A version[^54^](#FOOT54) that can
automagically detect compressed archives is preferred for use with
`untar()`: the configure script looks for `gtar` and `gnutar` before
`tar` -- use environment variable `TAR` to override this.
(On NetBSD/OpenBSD systems set this to `bsdtar` if that is installed.)

There need to be suitable versions of the tools `grep` and `sed`: the
problems are usually with old AT&T and BSD variants. `configure` will
try to find suitable versions (including looking in
`/usr/xpg4/bin` which is used on some commercial Unixes).

You will not be able to build most of the manuals unless you have
`texi2any` version 5.1 or later installed, and if not most of the HTML
manuals will be linked to a version on CRAN. To make PDF versions of the
manuals you will also need file `texinfo.tex` installed (which
is part of the GNU **texinfo** distribution but is often made part of
the TeX package in re-distributions) as well as
`texi2dvi`.[^55^](#FOOT55) Further, the versions of `texi2dvi`
and `texinfo.tex` need to be compatible: we have seen problems
with older TeX distributions.

If you want to build from the R Subversion repository then `texi2any` is
highly recommended as it is used to create files which are in the
tarball but not stored in the Subversion repository.

The PDF documentation (including `doc/NEWS.pdf`) and building
vignettes needs `pdftex` and `pdflatex`. We require LaTeX version
`2005/12/01` or later (for UTF-8 support). Building PDF package manuals
(including the R reference manual) and vignettes is sensitive to the
version of the LaTeX package **hyperref** and we recommend that the TeX
distribution used is kept up-to-date. A number of standard LaTeX
packages are required (including **url** and some of the font packages
such as **times**, **helvetic**, **ec** and **cm-super**) and others
such as **hyperref** and **inconsolata** are desirable (and without them
you may need to change R's defaults: see [Making the manuals](#Making-the-manuals)). Note that package **hyperref**
(currently) requires packages **kvoptions**, **ltxcmds** and
**refcount**. For distributions based on TeX Live the simplest approach
may be to install collections **collection-latex**,
**collection-fontsrecommended**, **collection-latexrecommended**,
**collection-fontsextra** and **collection-latexextra** (assuming they
are not installed by default): Fedora uses names like
**texlive-collection-fontsextra** and Debian/Ubuntu like
**texlive-fonts-extra**.

The essential programs should be in your `PATH` at the time `configure`
is run: this will capture the full paths.

Those distributing binary versions of R may need to be aware of the
licences of the external libraries it is linked to (including 'useful'
libraries from the next section). The `liblzma` library is in the public
domain and X11, `libbzip2`, `libcurl` and `zlib` have MIT-style
licences. PCRE has a BSD-style licence which requires distribution of
the licence (included in R's `COPYRIGHTS` file) in binary
distributions. GNU `readline` is licensed under GPL (which version(s)
depending on the `readline` version).

---

### A.2 Useful libraries and programs

The ability to use translated messages makes use of `gettext` and most
likely needs GNU `gettext`: you do need this to work with new
translations, but otherwise the version contained in the R sources will
be used if no suitable external `gettext` is found.

The 'modern' version of the `X11()`, `jpeg()`, `png()` and `tiff()`
graphics devices uses the `cairo` and (optionally) `Pango` libraries.
Cairo version 1.2.0 or later is required. Pango needs to be at least
version 1.10, and 1.12 is the earliest version we have tested. (For
Fedora users we believe the `pango-devel` RPM and its dependencies
suffice.) R checks for `pkg-config`, and uses that to check first that
the '`pangocairo`' package is installed (and if not,
'`cairo`') and if additional flags are needed for the
'`cairo-xlib`' package, then if suitable code can be compiled.
These tests will fail if `pkg-config` is not
installed[^56^](#FOOT56), and are likely to fail if `cairo` was
built statically (unusual). Most systems with `Gtk+` 2.8 or later
installed will have suitable libraries.

For the best font experience with these devices you need suitable fonts
installed: Linux users will want the `urw-fonts` package. On platforms
which have it available, the `msttcorefonts`
package[^57^](#FOOT57) provides TrueType versions of Monotype
fonts such as Arial and Times New Roman. Another useful set of fonts is
the 'liberation' TrueType fonts available at
<https://fedorahosted.org/liberation-fonts/>,[^58^](#FOOT58)
which cover the Latin, Greek and Cyrillic alphabets plus a fair range of
signs. These share metrics with Arial, Times New Roman and Courier New,
and contain fonts rather similar to the first two
(<https://en.wikipedia.org/wiki/Liberation_fonts>). Then there is the
'Free UCS Outline Fonts' project
(<https://www.gnu.org/software/freefont/>) which are OpenType/TrueType
fonts based on the URW fonts but with extended Unicode coverage. See the
R help on `X11` on selecting such fonts.

The bitmapped graphics devices `jpeg()`, `png()` and `tiff()` need the
appropriate headers and libraries installed: `jpeg` (version 6b or
later, or `libjpeg-turbo`) or `libpng` (version 1.2.7 or later) and
`zlib` or `libtiff` (versions 4.0.\[5-10\] and 4.1.0 have been tested)
respectively. `pkg-config` is used if available and so needs the
appropriate `.pc` file (which requires `libtiff` version 4.x
and is not available on all platforms for `jpeg` before version 9c).
They also need support for either `X11` or `cairo` (see above). Should
support for these devices **not** be required or broken system libraries
need to be avoided there are `configure` options
`--without-libpng`, `--without-jpeglib` and
`--without-libtiff`. The TIFF library has many optional
features such as `jpeg`, `libz`, `lzma`, `jbig` and `jpeg12`, none of
which is required for the `tiff()` devices but may need to be present to
link the library (usually only an issue for static linking).

Option `--with-system-tre` is also available: it needs a recent
version of TRE. (The latest (2016) sources are in the `git` repository
at <https://github.com/laurikari/tre/>, but at the time of writing the
resulting build will not pass its checks.).

An implementation of XDR is required, and the R sources contain one
which is likely to suffice (although a system version may have higher
performance). XDR is part of RPC and historically has been part of
`libc` on a Unix-alike. (In principle `man xdr_string` should
tell you which library is needed, but it often does not: on Solaris and
others it is provided by `libnsl`.) However some
builds[^59^](#FOOT59) of `glibc` omit or hide it with the
intention that the TI-RPC library be used, in which case `libtirpc` (and
its development version) should be installed, and its
headers[^60^](#FOOT60) need to be on the C include path or
under `/usr/include/tirpc`.

Use of the X11 clipboard selection requires the `Xmu` headers and
libraries. These are normally part of an X11 installation (e.g. the
Debian meta-package '`xorg-dev`'), but some distributions have
split this into smaller parts, so for example recent versions of Fedora
require the '`libXmu`' and '`libXmu-devel`' RPMs.

Some systems (notably macOS and at least some FreeBSD systems) have
inadequate support for collation in multibyte locales. It is possible to
replace the OS's collation support by that from ICU (International
Components for Unicode, <http://site.icu-project.org/>), and this
provides much more precise control over collation on all systems. ICU is
available as sources and as binary distributions for (at least) most
Linux distributions, Solaris, FreeBSD and AIX, usually as `libicu` or
`icu4c`. It will be used by default where available: should a very old
or broken version of ICU be found this can be suppressed by
`--without-ICU`.

The `bitmap` and `dev2bitmap` devices and function `embedFonts()` use
ghostscript (<http://www.ghostscript.com/>). This should either be in
your path when the command is run, or its full path specified by the
environment variable `R_GSCMD` at that time.

At the time of writing a full installation on Fedora Linux used the
following packages and their development versions, and this may provide
a useful checklist for other systems:

```r
bzip2 cairo fontconfig freetype fribidi glib2 libX11 libXext libXt
libcurl libicu libjpeg libpng libtiff libtirpc libxcrypt ncurses pango
pcre readline tcl tk xz zlib
```

---

• [Tcl/Tk](#Tcl_002fTk)     
 • [Java support](#Java-support)     
 • [Other compiled languages](#Other-compiled-languages)

---

---

#### A.2.1 Tcl/Tk

The **tcltk** package needs Tcl/Tk ≥ 8.4 installed: the sources are
available at <https://www.tcl.tk/>. To specify the locations of the
Tcl/Tk files you may need the configuration options

`--with-tcltk`

: use Tcl/Tk, or specify its library directory

`--with-tcl-config=TCL_CONFIG`

: specify location of `tclConfig.sh`

`--with-tk-config=TK_CONFIG`

: specify location of `tkConfig.sh`

or use the configure variables `TCLTK_LIBS` and `TCLTK_CPPFLAGS` to
specify the flags needed for linking against the Tcl and Tk libraries
and for finding the `tcl.h` and `tk.h` headers,
respectively. If you have both 32- and 64-bit versions of Tcl/Tk
installed, specifying the paths to the correct config files may be
necessary to avoid confusion between them.

Versions of Tcl/Tk up to 8.5.19 and 8.6.9 have been tested (including
most versions of 8.4.x, but not recently).

Note that the `tk.h` header includes[^61^](#FOOT61)
X11 headers, so you will need X11 and its development files installed.

---

#### A.2.2 Java support

The build process looks for Java support on the host system, and if it
finds it sets some settings which are useful for Java-using packages
(such as [**rJava**](https://CRAN.R-project.org/package=rJava) and
[**JavaGD**](https://CRAN.R-project.org/package=JavaGD): these require a
full JDK). This check can be suppressed by configure option
`--disable-java`. Configure variable
`JAVA_HOME` can be set to point to a specific JRE/JDK, on the
`configure` command line or in the environment.

Principal amongst these settings are some paths to the Java libraries
and JVM, which are stored in environment variable

`R_JAVA_LD_LIBRARY_PATH` in file `R_HOME/etc/ldpaths` (or a
sub-architecture-specific version). A typical setting for
'`x86_64`' Linux is

```r
JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.fc30.x86_64/jre
R_JAVA_LD_LIBRARY_PATH=${JAVA_HOME}/lib/that/server
```

Unfortunately this depends on the exact version of the JRE/JDK
installed, and so may need updating if the Java installation is updated.
This can be done by running `R CMD javareconf` which updates settings in
both `R_HOME/etc/Makeconf` and `R_HOME/etc/ldpaths`.
See `R CMD javareconf --help` for details: note that this needs to be
done by the account owning the R installation.

Another way of overriding those settings is to set the environment
variable
`R_JAVA_LD_LIBRARY_PATH` (before R is started, hence not in
`~/.Renviron`), which suffices to run already-installed
Java-using packages. For example

```r
R_JAVA_LD_LIBRARY_PATH=/usr/lib/jvm/java-1.8.0/jre/lib/amd64/server
```

It may be possible to avoid this by specifying an invariant link as the
path when configuring. For example, on that system any of

```r
JAVA_HOME=/usr/lib/jvm/java
JAVA_HOME=/usr/lib/jvm/java-1.8.0
JAVA_HOME=/usr/lib/jvm/java-1.8.0/jre
```

worked.

'Non-server' distributions of Java as from version 11 are of a full JDK.
However, Linux distributions can be confusing: for example Fedora 30 had

```r
java-1.8.0-openjdk
java-1.8.0-openjdk-devel
java-openjdk
java-openjdk-devel
java-11-openjdk
java-11-openjdk-devel
java-latest-openjdk
java-latest-openjdk-devel
```

where the `-devel` RPMs are needed to complete the JDK. (At the time of
writing `java-openjdk` was Java 12.) Debian/Ubuntu use '`-jre`'
and '`-jdk`', e.g.

```r
sudo apt install default-jdk
```

---

#### A.2.3 Other compiled languages

Some add-on packages need a C++ compiler. This is specified by the
configure variables `CXX`, `CXXFLAGS` and similar. `configure` will
normally find a suitable compiler. However, in many cases this will be a
C++98 compiler, and it is possible to specify an alternative compiler
for use with C++11 by the configure variables `CXX11`, `CXX11STD`,
`CXX11FLAGS` and similar (see [C++ Support](#C_002b_002b-Support)).
Again, `configure` will normally find a suitable value for `CXX11STD` if
the compiler given by `CXX` is capable of compiling C++11 code, but it
is possible that a completely different compiler will be needed.

For source files with extension `.f90` or `.f95`
containing free-form Fortran, the compiler defined by the macro `FC` is
used by `R CMD INSTALL`. Note that it is detected by the name of the
command without a test that it can actually compile Fortran 90 code. Set
the configure variable `FC` to override this if necessary: variables
`FCFLAGS` and `FCLIBS_XTRA` might also need to be set.

See file `config.site` in the R source for more details about
these variables.

---

### A.3 Linear algebra

---

• [BLAS](#BLAS)     
 • [LAPACK](#LAPACK)     
 • [Caveats](#Caveats)

---

---

#### A.3.1 BLAS

The linear algebra routines in R can make use of enhanced BLAS (Basic
Linear Algebra Subprograms, <http://www.netlib.org/blas/faq.html>)
routines. However, these have to be explicitly requested at configure
time: R provides an internal BLAS which is well-tested and will be
adequate for most uses of R.

You can specify a particular BLAS library _via_ a value for the
configuration option `--with-blas` and not to use an external
BLAS library by `--without-blas` (the default). If
`--with-blas` is given with no `=`, its value is taken from the
environment variable `BLAS_LIBS`, set for
example in `config.site`. If neither the option nor the
environment variable supply a value, a search is made for a
suitable[^62^](#FOOT62) BLAS. If the value is not obviously a
linker command (starting with a dash or giving the path to a library),
it is prefixed by '`-l`', so

```r
--with-blas="foo"
```

is an instruction to link against '`-lfoo`' to find an external
BLAS (which needs to be found both at link time and run time).

The configure code checks that the external BLAS is complete (it must
include all double precision and double complex routines, as well as
`LSAME`), and appears to be usable. However, an external BLAS has to be
usable from a shared object (so must contain position-independent code),
and that is not checked.

Some enhanced BLASes are compiler-system-specific (`sunperf` on
Solaris[^63^](#FOOT63), `libessl` on IBM, `Accelerate` on
macOS). The correct incantation for these is often found _via_
`--with-blas` with no value on the appropriate platforms.

Some of the external BLASes are multi-threaded. One issue is that R
profiling (which uses the `SIGPROF` signal) may cause problems, and you
may want to disable profiling if you use a multi-threaded BLAS. Note
that using a multi-threaded BLAS can result in taking more CPU time and
even more elapsed time (occasionally dramatically so) than using a
similar single-threaded BLAS. On a machine running other tasks, there
can be contention for CPU caches that reduces the effectiveness of the
optimization of cache use by a BLAS implementation: some people warn
that this is especially problematic for hyperthreaded CPUs.

Note that under Unix (but not under Windows) if R is compiled against a
non-default BLAS and `--enable-BLAS-shlib` is **not** used (it
is the default on all platforms except AIX), then all BLAS-using
packages must also be. So if R is re-built to use an enhanced BLAS then
packages such as
[**quantreg**](https://CRAN.R-project.org/package=quantreg) will need to
be re-installed; they may be under other circumstances.

R relies on ISO/IEC 60559 compliance of an external BLAS. This can be
broken if for example the code assumes that terms with a zero factor are
always zero and do not need to be computed---whereas `x*0` can be `NaN`.
This is checked in the test suite.

External BLAS implementations often make less use of extended-precision
floating-point registers (where available) and will almost certainly
re-order computations. This can result in less accuracy than using a
reference BLAS, and may result in different solutions, e.g. different
signs in SVD and eigendecompositions.

Debian/Ubuntu systems provide a system-specific way to switch the BLAS
in use. Build R with `-with-blas` to select the OS version of
the reference BLAS, and then use `update-alternatives` to switch between
the available BLAS libraries. See
<https://wiki.debian.org/DebianScience/LinearAlgebraLibraries>.

The URIs for several of these BLAS have been subject to frequent
gratuitous changes, so you will need to search for their current
locations.

BLAS (and LAPACK) routines may be used inside threaded code, for example
in OpenMP sections in packages such as **mgcv**. The reference
implementations are thread-safe but external ones may not be (even
single-threaded ones): this can lead to hard-to-track-down incorrect
results or segfaults.

**NOTE:** BLAS libraries built with `gfortran` 9 (and future versions
8.4, 7.5 and later) require calls from C/C++ to handle 'hidden'
character lengths --- R itself does so but many packages do not and some
segfault. (This applies also to external LAPACK libraries.)

---

• [ATLAS](#ATLAS)     
 • [OpenBLAS](#OpenBLAS)     
 • [MKL](#MKL)     
 • [Shared BLAS](#Shared-BLAS)

---

---

#### A.3.1.1 ATLAS

ATLAS (<http://math-atlas.sourceforge.net/>) is a "tuned" BLAS that runs
on a wide range of Unix-alike platforms. Unfortunately it is built by
default as a static library that on some platforms may not be able to be
used with shared objects such as are used in R packages. Be careful when
using pre-built versions of ATLAS static libraries (they seem to work on
'`ix86`' platforms, but not always on '`x86_64`'
ones).

ATLAS contains replacements for a small number of LAPACK routines, but
can be built to merge these with LAPACK sources to include a full LAPACK
library.

Recent versions of ATLAS can be built as a single shared library, either
`libsatlas` or `libtatlas` (serial or threaded respectively): these may
even contain a full LAPACK. Such builds can be used by one of

```r
--with-blas=satlas
--with-blas=tatlas
```

or, as on '`x86_64`' Fedora where a path needs to be specified,

```r
--with-blas="-L/usr/lib64/atlas -lsatlas"
--with-blas="-L/usr/lib64/atlas -ltatlas"
```

Distributed ATLAS libraries cannot be tuned to your machine and so are a
compromise: for example Fedora tunes '`x86_64`' for CPUs with
SSE3 extensions, and separate '`atlas-sse2`' and
'`atlas-sse3`' '`i686`' RPMs are
available.[^64^](#FOOT64)

Note that building R on Linux against distributed shared libraries may
need '`-devel`' or '`-dev`' packages installed.

Linking against multiple static libraries requires one of

```r
--with-blas="-lf77blas -latlas"
--with-blas="-lptf77blas -lpthread -latlas"
--with-blas="-L/path/to/ATLAS/libs -lf77blas -latlas"
--with-blas="-L/path/to/ATLAS/libs -lptf77blas -lpthread -latlas"
```

Consult its installation guide[^65^](#FOOT65) for how to build
ATLAS as a shared library or as a static library with
position-independent code (on platforms where that matters).

According to the ATLAS FAQ[^66^](#FOOT66) the maximum number of
threads used by multi-threaded ATLAS is set at compile time. Also, the
author advises against using multi-threaded ATLAS on hyperthreaded CPUs
without restricting affinities at compile-time to one virtual core per
physical CPU. (For the Fedora libraries the compile-time flag specifies
4 threads.)

---

#### A.3.1.2 OpenBLAS

Dr Kazushige Goto wrote a tuned BLAS for several processors and OSes,
which was frozen in mid-2010. OpenBLAS (<http://www.openblas.net/>) is a
descendant project with support for some later CPUs.

This can be used by configuring R with something like

```r
--with-blas="-lopenblas"
```

See see [Shared BLAS](#Shared-BLAS) for an alternative (and in many ways
preferable) way to use them.

Some platforms provide multiple builds of OpenBLAS: for example Fedora
30 has RPMs[^67^](#FOOT67)

```r
openblas
openblas-threads
openblas-openmp
```

providing shared libraries

```r
libopenblas.so
libopenblasp.so
libopenblaso.so
```

respectively, each of which can be used as a shared BLAS. For the second
and third the number of threads is controlled by `OPENBLAS_NUM_THREADS`
and `OMP_NUM_THREADS` (as usual for OpenMP) respectively. There is also
a Fedora RPM '`openblas-Rblas`' to replace
`libRblas.so` in their distribution of R.

Note that building R on Linux against distributed libraries may need
'`-devel`' or '`-dev`' packages installed.

For '`ix86`' and '`x86_64`' most distributed libraries
contain several alternatives for different CPU microarchitectures with
the choice being made at run time.

---

#### A.3.1.3 Intel MKL

For Intel processors (and perhaps others) and some distributions of
Linux, there is Intel's Math Kernel Library. You are strongly encouraged
to read the MKL User's Guide, which is installed with the library,
before attempting to link to MKL. This includes a 'link line advisor'
which will suggest appropriate incantations: its use is recommended. Or
see
<https://software.intel.com/en-us/articles/intel-mkl-link-line-advisor>.

There are also versions of MKL for macOS[^68^](#FOOT68) and
Windows, but when these have been tried they did not work with the
default compilers used for R on those platforms.

The MKL interface has changed several times but has been stable in
recent years: the following examples have been used with versions 10.3
to 2019.4, for GCC compilers on '`x86_64`'.

To use a sequential version of MKL we used

```r
MKL_LIB_PATH=/path/to/intel_mkl/mkl/lib/intel64
export LD_LIBRARY_PATH=$MKL_LIB_PATH
MKL="-L${MKL_LIB_PATH} -lmkl_gf_lp64 -lmkl_core -lmkl_sequential"
./configure --with-blas="$MKL" --with-lapack
```

The option `--with-lapack` is used since MKL contains a tuned
copy of LAPACK (often older than the current version) as well as BLAS
(see [LAPACK](#LAPACK)), although this can be omitted.

Threaded MKL may be used by replacing the line defining the variable
`MKL` by

```r
MKL="-L${MKL_LIB_PATH} -lmkl_gf_lp64 -lmkl_core \
     -lmkl_gnu_thread -dl -fopenmp"
```

R can also be linked against a single shared library, `libmkl_rt.so`,
for both BLAS and LAPACK, but the correct OpenMP and MKL interface layer
then has to be selected via environment variables. With 64-bit builds
and the GCC compilers, we used

```r
export MKL_INTERFACE_LAYER=GNU,LP64
export MKL_THREADING_LAYER=GNU
```

On Debian/Ubuntu, MKL is provided by package `intel-mkl-full` and one
can set `libmkl_rt.so` as the system-wide implementation of both BLAS
and LAPACK during installation of the package, so that also R installed
from Debian/Ubuntu package `r-base` would use it. It is, however, still
essential to set `MKL_INTERFACE_LAYER` and `MKL_THREADING_LAYER` before
running R, otherwise MKL computations will produce incorrect results. R
does not have to be rebuilt to use MKL, but `configure` include tests
which may discover some errors such as a failure to set the correct
OpenMP and MKL interface layer.

The default number of threads will be chosen by the OpenMP software, but
can be controlled by setting `OMP_NUM_THREADS` or `MKL_NUM_THREADS`, and
in recent versions seems to default to a sensible value for sole use of
the machine. (Parallel MKL has not always passed `make check-all`, but
did with MKL 2019.4.)

MKL includes a partial implementation of FFTW3, which causes trouble for
applications that require some of the FFTW3 functionality unsupported in
MKL. Please see the MKL manuals for description of these limitations and
for instructions on how to create a custom version of MKL which excludes
the FFTW3 wrappers.

It was reported in 2015 that

```r
--with-blas='-mkl=parallel' --with-lapack
```

worked with the Intel 2015.3 compilers on Centos 6.

---

#### A.3.1.4 Shared BLAS

The BLAS library will be used for many of the add-on packages as well as
for R itself. This means that it is better to use a shared/dynamic BLAS
library, as most of a static library will be compiled into the R
executable and each BLAS-using package.

R offers the option of compiling the BLAS into a dynamic library
`libRblas` stored in `R_HOME/lib` and linking both R itself and
all the add-on packages against that library.

This is the default on all platforms except AIX unless an external BLAS
is specified and found: for the latter it can be used by specifying the
option `--enable-BLAS-shlib`, and it can always be disabled via
`--disable-BLAS-shlib`.

This has both advantages and disadvantages.

- It saves space by having only a single copy of the BLAS routines,
  which is helpful if there is an external static BLAS (as used to be
  standard for ATLAS).
- There may be performance disadvantages in using a shared BLAS.
  Probably the most likely is when R's internal BLAS is used and R is
  _not_ built as a shared library, when it is possible to build the
  BLAS into `R.bin` (and `libR.a`) without using
  position-independent code. However, experiments showed that in many
  cases using a shared BLAS was as fast, provided high levels of
  compiler optimization are used.
- It is easy to change the BLAS without needing to re-install R and
  all the add-on packages, since all references to the BLAS go through
  `libRblas`, and that can be replaced. Note though that any dynamic
  libraries the replacement links to will need to be found by the
  linker: this may need the library path to be changed in
  `R_HOME/etc/ldpaths`.

Another option to change the BLAS in use is to symlink a single dynamic
BLAS library to `R_HOME/lib/libRblas.so`. For example, just

```r
mv R_HOME/lib/libRblas.so R_HOME/lib/libRblas.so.keep
ln -s /usr/lib64/libopenblasp.so.0 R_HOME/lib/libRblas.so
```

on '`x86_64`' Fedora will change the BLAS used to multithreaded
OpenBLAS. A similar link works for most versions of the OpenBLAS
(provided the appropriate `lib` directory is in the run-time
library path or `ld.so` cache). It can also be used for a single-library
ATLAS, so on '`x86_64`' Fedora

```r
ln -s /usr/lib64/atlas/libsatlas.so.3 R_HOME/lib/libRblas.so
ln -s /usr/lib64/atlas/libtatlas.so.3 R_HOME/lib/libRblas.so
```

can be used with its distributed ATLAS libraries. (If you have the
'`-devel`' RPMS installed you can omit the `.0`/`.3`.)

Note that rebuilding or symlinking `libRblas.so` may not
suffice if the intention is to use a modified LAPACK contained in an
external BLAS: the latter could even cause conflicts. However, on Fedora
where the OpenBLAS distribution contains a copy of LAPACK, it is the
latter which is used.

---

#### A.3.2 LAPACK

Provision is made for using an external LAPACK library, principally to
cope with BLAS libraries which contain a copy of LAPACK (such as
`sunperf` on Solaris, `Accelerate` on macOS and ATLAS and MKL on
'`ix86`'/'`x86_64`' Linux). At least LAPACK version
3.2 is required. This can only be done if `--with-blas` has
been used.

However, the likely performance gains are thought to be small (and may
be negative). The default is not to search for a suitable LAPACK
library, and this is definitely **not** recommended. You can specify a
specific LAPACK library or a search for a generic library by the
configuration option `--with-lapack`. The default for
`--with-lapack` is to check the BLAS library and then look for
an external library '`-llapack`'. Sites searching for the
fastest possible linear algebra may want to build a LAPACK library using
the ATLAS-optimized subset of LAPACK: this is simplest with a dynamic
ATLAS library which contains a full LAPACK, when
`--with-lapack` suffices.

A value for `--with-lapack` can be set _via_ the environment
variable `LAPACK_LIBS`, but this will only be
used if `--with-lapack` is specified (as the default value is
`no`) and the BLAS library does not contain LAPACK.

If you do use `--with-lapack`, be aware of potential problems
with bugs in the LAPACK sources (or in the posted corrections to those
sources). In particular, bugs in `DGEEV` and `DGESDD` have resulted in
error messages such as

```r
DGEBRD gave error code -10
```

. Other potential problems are incomplete versions of the libraries,
seen several times in Linux distributions over the years.

Please **do** bear in mind that using `--with-lapack` is
'definitely **not** recommended': it is provided **only** because it is
necessary on some platforms and because some users want to experiment
with claimed performance improvements. Reporting problems where it is
used unnecessarily will simply irritate the R helpers.

Note too the comments about ISO/IEC 60559 compliance in the section of
external BLAS: these apply equally to an external LAPACK, and for
example the Intel MKL documentation has said

> LAPACK routines assume that input matrices do not contain IEEE 754
> special values such as INF or NaN values. Using these special values
> may cause LAPACK to return unexpected results or become unstable.

We rely on limited support in LAPACK for matrices with _2\^{31}_ or more
elements: it is possible that an external LAPACK will not have that
support.

---

#### A.3.3 Caveats

As with all libraries, you need to ensure that they and R were compiled
with compatible compilers and flags. For example, this has meant that on
Sun Sparc using the Oracle compilers the flag `-dalign` is
needed if `sunperf` is to be used.

On some systems it has been necessary that an external BLAS/LAPACK was
built with the same Fortran compiler used to build R.

LAPACK 3.9.0 has a bug in which the DCOMBSSQ subroutine has a bug that
may cause NA to be interpreted as zero. This is fixed in R 3.6.3, but if
you use an external LAPACK, you may need to fix it there.

The code (in `dlapack.f`) should read

```r
*     ..
*     .. Executable Statements ..
*
      IF( V1( 1 ).GE.V2( 1 ) ) THEN
         IF( V1( 1 ).NE.ZERO ) THEN
            V1( 2 ) = V1( 2 ) + ( V2( 1 ) / V1( 1 ) )**2 * V2( 2 )
         ELSE
            V1( 2 ) = V1( 2 ) + V2( 2 )
         END IF
      ELSE
         V1( 2 ) = V2( 2 ) + ( V1( 1 ) / V2( 1 ) )**2 * V1( 2 )
         V1( 1 ) = V2( 1 )
      END IF
      RETURN
```

(The inner ELSE clause was missing in LAPACK 3.9.0).

---

## Appendix B Configuration on a Unix-alike

---

• [Configuration options](#Configuration-options)     
 • [Internationalization support](#Internationalization-support)     
 • [Configuration variables](#Configuration-variables)     
 • [Setting the shell](#Setting-the-shell)     
 • [Using make](#Using-make)     
 • [Using Fortran](#Using-Fortran)     
 • [Compile and load flags](#Compile-and-load-flags)     
 • [Maintainer mode](#Maintainer-mode)

---

---

### B.1 Configuration options

`configure` has many options: running

```r
./configure --help
```

will give a list. Probably the most important ones not covered elsewhere
are (defaults in brackets)

`--with-x`

: use the X Window System \[yes\]

`--x-includes=DIR`

: X include files are in `DIR`{.variable}

`--x-libraries=DIR`

: X library files are in `DIR`{.variable}

`--with-readline`

: use readline library (if available) \[yes\]

`--enable-R-profiling`

: attempt to compile support for `Rprof()` \[yes\]

`--enable-memory-profiling`

: attempt to compile support for `Rprofmem()` and `tracemem()` \[no\]

`--enable-R-shlib`

: build R as a shared/dynamic library \[no\]

`--enable-BLAS-shlib`

: build the BLAS as a shared/dynamic library \[yes, except on AIX\]

You can use `--without-foo` or `--disable-foo` for the
negatives.

You will want to use `--disable-R-profiling` if you are
building a profiled executable of R (e.g. with '`-pg)`'.
Support for R profiling requires OS support for POSIX threads (_aka_
'`pthreads`'), which are available on all mainstream Unix-alike
platforms.

Flag `--enable-R-shlib` causes the make process to build R as a
dynamic (shared) library, typically called `libR.so`, and link
the main R executable `R.bin` against that library. This can
only be done if all the code (including system libraries) can be
compiled into a dynamic library, and there may be a
performance[^69^](#FOOT69) penalty. So you probably only want
this if you will be using an application which embeds R. Note that C
code in packages installed on an R system linked with
`--enable-R-shlib` is linked against the dynamic library and so
such packages cannot be used from an R system built in the default way.
Also, because packages are linked against R they are on some OSes also
linked against the dynamic libraries R itself is linked against, and
this can lead to symbol conflicts.

For maximally effective use of `valgrind`, R should be compiled with
valgrind instrumentation. The `configure` option is
`--with-valgrind-instrumentation=level`, where
`level`{.variable} is 0, 1 or 2. (Level 0 is the default and does not
add anything.) The system headers for `valgrind` can be requested by
option `--with-system-valgrind-headers`: they will be used if
present (on Linux they may be in a separate package such as
**valgrind-devel**). Note though that there is no guarantee that the
code in R will be compatible with very old[^70^](#FOOT70) or
future `valgrind` headers.

If you need to re-configure R with different options you may need to run
`make clean` or even `make distclean` before doing so.

The `configure` script has other generic options added by
`autoconf` and which are not supported for R: in particular building for
one architecture on a different host is not possible.

---

### B.2 Internationalization support

Translation of messages is supported via GNU `gettext` unless disabled
by the configure option `--disable-nls`. The `configure` report
will show `NLS` as one of the 'Additional capabilities' if support has
been compiled in, and running in an English locale (but not the `C`
locale) will include

```r
  Natural language support but running in an English locale
```

in the greeting on starting R.

---

### B.3 Configuration variables

If you need or want to set certain configure variables to something
other than their default, you can do that by either editing the file
`config.site` (which documents many of the variables you might
want to set: others can be seen in file `etc/Renviron.in`) or
on the command line as

```r
./configure VAR=value
```

If you are building in a directory different from the sources, there can
be copies of `config.site` in the source and the build
directories, and both will be read (in that order). In addition, if
there is a file `~/.R/config`, it is read between the
`config.site` files in the source and the build directories.

There is also a general `autoconf` mechanism for `config.site`
files, which are read before any of those mentioned in the previous
paragraph. This looks first at a file specified by the
environment variable `CONFIG_SITE`, and if
not is set at files such as `/usr/local/share/config.site` and
`/usr/local/etc/config.site` in the area (exemplified by
`/usr/local`) where R would be installed.

These variables are _precious_, implying that they do not have to be
exported to the environment, are kept in the cache even if not specified
on the command line, checked for consistency between two configure runs
(provided that caching is used), and are kept during automatic
reconfiguration as if having been passed as command line arguments, even
if no cache is used.

See the variable output section of `configure --help` for a list of all
these variables.

If you find you need to alter configure variables, it is worth noting
that some settings may be cached in the file `config.cache`,
and it is a good idea to remove that file (if it exists) before
re-configuring. Note that caching is turned _off_ by default: use the
command line option `--config-cache` (or `-C`) to
enable caching.

---

• [Setting paper size](#Setting-paper-size)     
 • [Setting the browsers](#Setting-the-browsers)     
 • [Compilation flags](#Compilation-flags)     
 • [Making manuals](#Making-manuals)

---

---

#### B.3.1 Setting paper size

One common variable to change is `R_PAPERSIZE`, which defaults to
'`a4`', not '`letter`'. (Valid values are
'`a4`', '`letter`', '`legal`' and
'`executive`'.)

This is used both when configuring R to set the default, and when
running R to override the default. It is also used to set the paper size
when making PDF manuals.

The configure default will most often be '`a4`' if
`R_PAPERSIZE` is unset. (If the (Debian Linux) program `paperconf` is
found or the environment variable `PAPERSIZE` is
set, these are used to produce the default.)

---

#### B.3.2 Setting the browsers

Another precious variable is `R_BROWSER`, the default HTML browser,
which should take a value of an executable in the user's path or specify
a full path.

Its counterpart for PDF files is `R_PDFVIEWER`.

---

#### B.3.3 Compilation flags

If you have libraries and header files, e.g., for GNU readline, in
non-system directories, use the variables `LDFLAGS` (for libraries,
using '`-L`' flags to be passed to the linker) and `CPPFLAGS`
(for header files, using '`-I`' flags to be passed to the C/C++
preprocessors), respectively, to specify these locations. These default
to '`-L/usr/local/lib`' (`LDFLAGS`,
'`-L/usr/local/lib64`' on most 64-bit Linux OSes) and
'`-I/usr/local/include`' (`CPPFLAGS`, but note that on most
systems `/usr/local/include` is regarded as a system include
directory and so instances in that macro will be skipped) to catch the
most common cases. If libraries are still not found, then maybe your
compiler/linker does not support re-ordering of `-L` and
`-l` flags. In this case, use a different compiler (or a
front-end shell script which does the re-ordering).

These flags can also be used to build a faster-running version of R. On
most platforms using `gcc`, having '`-O3`' in `CFLAGS` and
`FFLAGS` produces worthwhile performance gains with `gcc` and
`gfortran`, but may result in a less reliable build (both segfaults and
incorrect numeric computations have been seen). On systems using the GNU
linker (especially those using R as a shared library), it is likely that
including '`-Wl,-O1`' in `LDFLAGS` is worthwhile, and
'`'-Bdirect,--hash-style=both,-Wl,-O1'`' is recommended at
<https://lwn.net/Articles/192624/>. Tuning compilation to a specific CPU
family (e.g. '`-mtune=native`' for `gcc`) can give worthwhile
performance gains, especially on older architectures such as
'`ix86`'.

---

#### B.3.4 Making manuals

The default settings for making the manuals are controlled by `R_RD4PDF`
and `R_PAPERSIZE`.

---

### B.4 Setting the shell

By default the shell scripts such as `R` will be
'`#!/bin/sh`' scripts (or using the `SHELL` chosen by
`configure`). This is almost always satisfactory, but on a few
systems `/bin/sh` is not a Bourne shell or clone, and the shell
to be used can be changed by setting the configure variable `R_SHELL` to
a suitable value (a full path to a shell, e.g.
`/usr/local/bin/bash`).

---

### B.5 Using make

To compile R, you will most likely find it easiest to use GNU `make`,
although the Sun `make` works on Solaris.

To build in a separate directory you need a `make` that supports the
`VPATH` variable, for example GNU `make` and Sun `make`.

`dmake` has also been used. e.g, on Solaris 10.

If you want to use a `make` by another name, for example if your GNU
`make` is called '`gmake`', you need to set the variable `MAKE`
at configure time, for example

```r
./configure MAKE=gmake
```

---

### B.6 Using Fortran

To compile R, you need a Fortran 90 compiler. The current default is to
search for `gfortran`, `g95`, `xlf95` `f95`, `fort`, `ifort`, `ifc`,
`efc`, `pgfortran`, `pgf95` `lf95`, `ftn`, `nagfor`, `xlf90`, `f90`,
`pgf90`, `pghpf`, `epcf90`. (Note that these are searched for by name,
without checking the standard of Fortran they support.) The command and
flags used should support fixed-form Fortran with extension
`.f`: in the unusual case that a specific flag is needed for
free-form Fortran with extension `.f90` or `.f95`,
this can be specified as part of `FCFLAGS`.

The search mechanism can be changed using the configure variable `FC`
which specifies the command that runs the Fortran compiler. If your
Fortran compiler is in a non-standard location, you
should set the environment variable `PATH` accordingly before running
`configure`, or use the configure variable `FC` to specify its full
path.

If your Fortran libraries are in slightly peculiar places, you should
also look at `LD_LIBRARY_PATH` (or
your system's equivalent) to make sure that all libraries are on this
path.

Note that only Fortran compilers which convert identifiers to lower case
are supported.

You must set whatever compilation flags (if any) are needed to ensure
that Fortran `integer` is equivalent to a C `int` pointer and Fortran
`double precision` is equivalent to a C `double` pointer. This is
checked during the configuration process.

Some of the Fortran code makes use of `DOUBLE COMPLEX` and `COMPLEX*16`
variables. This is checked for at configure time, as well as its
equivalence to the `Rcomplex` C structure defined in
`R_ext/Complex.h`.

Pre-release versions of `gfortran` 10 enforce a previously allowed
(without even a warning) restriction on the widespread practice of
passing Fortran array elements where an array is expected. To continue
to allow this (with a warning), add
`-fallow-argument-mismatch`[^71^](#FOOT71) to
`FFLAGS`.

---

### B.7 Compile and load flags

A wide range of flags can be set in the file `config.site` or
as configure variables on the command line. We have already mentioned

`CPPFLAGS`

: header file search directory (`-I`) and any other
miscellaneous options for the C and C++ preprocessors and compilers

`LDFLAGS`

: path (`-L`), stripping (`-s`) and any other
miscellaneous options for the linker

and others include

`CFLAGS`

: debugging and optimization flags, C

`MAIN_CFLAGS`

: ditto, for compiling the main program (e.g. when profiling)

`SHLIB_CFLAGS`

: for shared objects (no known examples)

`FFLAGS`

: debugging and optimization flags, fixed-form Fortran

`FCFLAGS`

: debugging and optimization flags, free-form Fortran

`SAFE_FFLAGS`

: ditto for source files which need exact floating point behaviour

`MAIN_FFLAGS`

: ditto, for compiling the main program (e.g. when profiling)

`SHLIB_FFLAGS`

: for shared objects (no known examples)

`MAIN_LDFLAGS`

: additional flags for the main link

`SHLIB_LDFLAGS`

: additional flags for linking the shared objects

`LIBnn`

: the primary library directory, `lib` or `lib64`

`CPICFLAGS`

: special flags for compiling C code to be turned into a shared object

`FPICFLAGS`

: special flags for compiling Fortran code to be turned into a shared
object

`CXXPICFLAGS`

: special flags for compiling C++ code to be turned into a shared
object

`DEFS`

: defines to be used when compiling C code in R itself

Library paths specified as `-L/lib/path` in `LDFLAGS` are
collected together and prepended to
`LD_LIBRARY_PATH` (or your system's equivalent), so there should be no
need for `-R` or `-rpath` flags.

Variables such as `CPICFLAGS` are determined where possible by
`configure`. Some systems allows two types of PIC flags, for example
'`-fpic`' and '`-fPIC`', and if they differ the first
allows only a limited number of symbols in a shared object. Since R as a
shared library has about 6200 symbols, if in doubt use the larger
version.

Other variables often set by `configure` include
'`MAIN_LDFLAGS`', '`SAFE_FFLAGS`',
'`SHLIB_LDFLAGS`' and '`SHLIB_CXXLDFLAGS`': see file
`config.site` in the sources for more documentation on these
and others.

To compile a profiling version of R, one might for example want to use
'`MAIN_CFLAGS=-pg`', '`MAIN_FFLAGS=-pg`',
'`MAIN_LDFLAGS=-pg`' on platforms where '`-pg`' cannot
be used with position-independent code.

**Beware**: it may be necessary to set `CFLAGS` and `FFLAGS` in ways
compatible with the libraries to be used: one possible issue is the
alignment of doubles, another is the way structures are passed.

On some platforms `configure` will select additional flags for `CFLAGS`,
`CPPFLAGS` and `LIBS` in `R_XTRA_CFLAGS` (and so on). These are for
options which are always required, for example to force IEC 60559
compliance.

---

### B.8 Maintainer mode

There are several files that are part of the R sources but can be
re-generated from their own sources by configuring with option
`--enable-maintainer-mode` and then running `make` in the build
directory. This requires other tools to be installed, discussed in the
rest of this section.

File `configure` is created from `configure.ac` and
the files under `m4` by `autoconf` and `aclocal` (part of the
**automake** package). There is a formal version requirement on
`autoconf` of 2.69 or later, but it is unlikely that anything other than
the most recent versions[^72^](#FOOT72) have been thoroughly
tested.

File `src/include/config.h` is created by `autoheader` (part of
**autoconf**).

Grammar files `*.y` are converted to C sources by an
implementation of `yacc`, usually `bison -y`: these are found in
`src/main` and `src/library/tools/src`. It is known
that earlier versions of `bison` generate code which reads (and in some
cases writes) outside array bounds: `bison` 2.6.1 was found to be
satisfactory.

The ultimate sources for package **compiler** are in its
`noweb` directory. To re-create the sources from
`src/library/compiler/noweb/compiler.nw`, the command
`notangle` is required. Some Linux distributions include this command in
package **noweb**. It can also be installed from the sources at
<https://www.cs.tufts.edu/~nr/noweb/>[^73^](#FOOT73). The
package sources are only re-created even in maintainer mode if
`src/library/compiler/noweb/compiler.nw` has been updated.

---

## Appendix C Platform notes

This section provides some notes on building R on different Unix-alike
platforms. These notes are based on tests run on one or two systems in
each case with particular sets of compilers and support libraries.
Success in building R depends on the proper installation and functioning
of support software; your results may differ if you have other versions
of compilers and support libraries.

Older versions of this manual contain notes on platforms such as HP-UX,
IRIX, Alpha/OSF1 (for R \< 2.10.0, and support has since been removed
for all of these) and AIX (for R \< = 3.5.x) for which we have had no
recent reports.

C macros to select particular platforms can be tricky to track down
(there is a fair amount of misinformation on the Web). The Wiki
(currently) at <http://sourceforge.net/p/predef/wiki/Home/> can be
helpful. The R sources have used (often in included software under
`src/extra`)

```r
AIX: _AIX
Cygwin: __CYGWIN__
FreeBSD: __FreeBSD__
HP-UX: __hpux__, __hpux
IRIX: sgi, __sgi
Linux: __linux__
macOS: __APPLE__
NetBSD: __NetBSD__
OpenBSD: __OpenBSD__
Solaris: __sun, sun
Windows: _WIN32, _WIN64
```

---

• [X11 issues](#X11-issues)     
 • [Linux](#Linux)     
 • [macOS](#macOS)     
 • [Solaris](#Solaris)     
 • [FreeBSD](#FreeBSD)     
 • [OpenBSD](#OpenBSD)     
 • [Cygwin](#Cygwin)     
 • [New platforms](#New-platforms)

---

---

### C.1 X11 issues

The '`X11()`' graphics device is the one started automatically
on Unix-alikes (except most macOS builds) when plotting. As its name
implies, it displays on a (local or remote) X server, and relies on the
services provided by the X server.

The 'modern' version of the '`X11()`' device is based on
'`cairo`' graphics and (in most implementations) uses
'`fontconfig`' to pick and render fonts. This is done on the
server, and although there can be selection issues, they are more
amenable than the issues with '`X11()`' discussed in the rest
of this section.

When X11 was designed, most displays were around 75dpi, whereas today
they are of the order of 100dpi or more. If you find that X11() is
reporting[^74^](#FOOT74) missing font sizes, especially larger
ones, it is likely that you are not using scalable fonts and have not
installed the 100dpi versions of the X11 fonts. The names and details
differ by system, but will likely have something like Fedora's

```r
xorg-x11-fonts-75dpi
xorg-x11-fonts-100dpi
xorg-x11-fonts-ISO8859-2-75dpi
xorg-x11-fonts-Type1
xorg-x11-fonts-cyrillic
```

and you need to ensure that the '`-100dpi`' versions are
installed and on the X11 font path (check via `xset -q`). The
'`X11()`' device does try to set a pointsize and not a pixel
size: laptop users may find the default setting of 12 too large
(although very frequently laptop screens are set to a fictitious dpi to
appear like a scaled-down desktop screen).

More complicated problems can occur in non-Western-European locales, so
if you are using one, the first thing to check is that things work in
the `C` locale. The likely issues are a failure to find any fonts or
glyphs being rendered incorrectly (often as a pair of ASCII characters).
X11 works by being asked for a font specification and coming up with its
idea of a close match. For text (as distinct from the symbols used by
plotmath), the specification is the first element of the option
`"X11fonts"` which defaults to

```r
"-adobe-helvetica-%s-%s-*-*-%d-*-*-*-*-*-*-*"
```

If you are using a single-byte encoding, for example ISO 8859-2 in
Eastern Europe or KOI8-R in Russian, use `xlsfonts` to find an
appropriate family of fonts in your encoding (the last field in the
listing). If you find none, it is likely that you need to install
further font packages, such as
'`xorg-x11-fonts-ISO8859-2-75dpi`' and
'`xorg-x11-fonts-cyrillic`' shown in the listing above.

Multi-byte encodings (most commonly UTF-8) are even more complicated.
There are few fonts in '`iso10646-1`', the Unicode encoding,
and they only contain a subset of the available glyphs (and are often
fixed-width designed for use in terminals). In such locales _fontsets_
are used, made up of fonts encoded in other encodings. If the locale you
are using has an entry in the '`XLC_LOCALE`' directory
(typically `/usr/share/X11/locale`), it is likely that all you
need to do is to pick a suitable font specification that has fonts in
the encodings specified there. If not, you may have to get hold of a
suitable locale entry for X11. This may mean that, for example, Japanese
text can be displayed when running in '`ja_JP.UTF-8`' but not
when running in '`en_GB.UTF-8`' on the same machine (although
on some systems many UTF-8 X11 locales are aliased to
'`en_US.UTF-8`' which covers several character sets, e.g. ISO
8859-1 (Western European), JISX0208 (Kanji), KSC5601 (Korean), GB2312
(Chinese Han) and JISX0201 (Kana)).

On some systems scalable fonts are available covering a wide range of
glyphs. One source is TrueType/OpenType fonts, and these can provide
high coverage. Another is Type 1 fonts: the URW set of Type 1 fonts
provides standard typefaces such as Helvetica with a larger coverage of
Unicode glyphs than the standard X11 bitmaps, including Cyrillic. These
are generally not part of the default install, and the X server may need
to be configured to use them. They might be under the X11
`fonts` directory or elsewhere, for example,

```r
/usr/share/fonts/default/Type1
/usr/share/fonts/ja/TrueType
```

---

### C.2 Linux

Linux is the main development platform for R, so compilation from the
sources is normally straightforward with the most common compilers and
libraries.[^75^](#FOOT75)

Recall that some package management systems (such as RPM and deb) make a
distinction between the user version of a package and the developer
version. The latter usually has the same name but with the extension
'`-devel`' or '`-dev`': you need both versions
installed. So please check the `configure` output to see if the expected
features are detected: if for example '`readline`' is missing
add the developer package. (On most systems you will also need
'`ncurses`' and its developer package, although these should be
dependencies of the '`readline`' package(s).) You should expect
to see in the `configure` summary

```r
  Interfaces supported:      X11, tcltk
  External libraries:        readline, curl
  Additional capabilities:   PNG, JPEG, TIFF, NLS, cairo, ICU
```

When R has been installed from a binary distribution there are sometimes
problems with missing components such as the Fortran compiler. Searching
the '`R-help`' archives will normally reveal what is needed.

It seems that '`ix86`' Linux accepts non-PIC code in shared
libraries, but this is not necessarily so on other platforms, in
particular on 64-bit CPUs such as '`x86_64`'. So care can be
needed with BLAS libraries and when building R as a shared library to
ensure that position-independent code is used in any static libraries
(such as the Tcl/Tk libraries, `libpng`, `libjpeg` and `zlib`) which
might be linked against. Fortunately these are normally built as shared
libraries with the exception of the ATLAS BLAS libraries.

The default optimization settings chosen for `CFLAGS` etc are
conservative. It is likely that using `-mtune` will result in
significant performance improvements on recent CPUs: one possibility is
to add `-mtune=native` for the best possible performance on the
machine on which R is being installed. It is also possible to increase
the optimization levels to `-O3`: however for many versions of
the compilers this has caused problems in at least one CRAN package.

For platforms with both 64- and 32-bit support, it is likely that

```r
LDFLAGS="-L/usr/local/lib64 -L/usr/local/lib"
```

is appropriate since most (but not all) software installs its 64-bit
libraries in `/usr/local/lib64`. To build a 32-bit version of R
on '`x86_64`' with Fedora 28 we used

```r
CC="gcc -m32"
CXX="g++ -m32"
FC="gfortran -m32"
OBJC=${CC}
LDFLAGS="-L/usr/local/lib"
LIBnn=lib
```

Note the use of '`LIBnn`': '`x86_64`' Fedora installs
its 64-bit software in `/usr/lib64` and 32-bit software in
`/usr/lib`. Linking will skip over inappropriate binaries, but
for example the 32-bit Tcl/Tk configure scripts are in
`/usr/lib`. It may also be necessary to set the `pkg-config`
path, e.g. by

```r
export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig:/usr/lib/pkgconfig
```

The 32-bit system `libcurl` did not work with the system CA
certificates: this is worked around in R's test suite.

64-bit versions on Linux are built with support for files \> 2Gb, and
32-bit versions will be if possible unless
`--disable-largefile` is specified.

Note that 32-bit `glibc` currently[^76^](#FOOT76) uses a 32-bit
`time_t` type, so to pass all the date-time checks needs R built with
flag `--with-internal-tzcode`.

To build a 64-bit version of R on '`ppc64`' (also known as
'`powerpc64`') with `gcc` 4.1.1, Ei-ji Nakama used

```r
CC="gcc -m64"
CXX="gxx -m64"
FC="gfortran -m64"
CFLAGS="-mminimal-toc -fno-optimize-sibling-calls -g -O2"
FFLAGS="-mminimal-toc -fno-optimize-sibling-calls -g -O2"
```

the additional flags being needed to resolve problems linking against
`libnmath.a` and when linking R as a shared library.

The setting of the macro '`SAFE_FFLAGS`' may need some help. It
should not need additional flags on platforms other than
'`68000`' (not likely to be encountered) and '`ix86`'.
For the latter, if the Fortran compiler is GNU (`gfortran` or possibly
`g77`) the flags

```r
-msse2 -mfpmath=sse
```

are added: earlier versions of R added `-ffloat-store` and this
might still be needed if a '`ix86`' CPU is encountered without
SSE2 support. Note that it is a _replacement_ for '`FFLAGS`',
so should include all the flags in that macro (except perhaps the
optimization level).

Additional compilation flags can be specified for added safety/security
checks. For example Fedora 30 adds

```r
-Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -Wp,-D_GLIBCXX_ASSERTIONS
-Fexceptions -fstack-protector-strong -fasynchronous-unwind-tables
-fstack-clash-protection -fcf-protection
```

to all the C, C++ and Fortran compiler flags (even though
`_GLIBCXX_ASSERTIONS` is only for C++ in current GCC and `glibc` and
none of these are documented for `gfortran`). Use of
`_GLIBCXX_ASSERTIONS` will link `abort` and `printf` into almost all C++
code, and `R CMD check --as-cran` will warn.

---

• [Clang](#Clang)     
 • [Intel compilers](#Intel-compilers)

---

---

#### C.2.1 Clang

R has been built with Linux '`ix86`' and '`x86_64`' C
and C++ compilers (<http://clang.llvm.org>) based on the Clang
front-ends, invoked by `CC=clang CXX=clang++`, together with `gfortran`.
These take very similar options to the corresponding GCC compilers.

This has to be used in conjunction with a Fortran compiler: the
`configure` code will remove `-lgcc` from `FLIBS`, which is
needed for some versions of `gfortran`.

The current out-of-the-box default for `clang++` is to use the C++
runtime from the installed `g++`. Using the runtime from the `libc++`
project (<http://libcxx.llvm.org/>, Fedora RPM `libcxx-devel`) _via_
`-stdlib=libc++` has also been tested.

Recent versions have (optional when built) OpenMP
support.[^77^](#FOOT77)

There is a project called `flang`
(<https://github.com/flang-compiler/flang>)) to develop a Fortran
compiler similar to clang but based on the Portland Group's front end.
This needs something like

```r
FC=/usr/local/flang/bin/flang
LDFLAGS="-L/usr/local/flang/lib -L/usr/local/lib64"
```

Note that `flang` accepts all the flags which `clang` does (the driver
is a modified version of `clang`, and `flang` is a symbolic link to
`clang`), but does not implement all of them for Fortran compilation: it
also accepts most PGI-style flags such as `-mp` for OpenMP. It
currently produces few diagnostics even with `-Wall -pedantic`.

`flang`'s Fortran runtime is compiled against OpenMP and it seems this
conflicts with using OpenMP in R. So it may be necessary to disable the
latter by configuring R using `--disable-openmp`.

It is not clear what architectures `flang` intends to support: our
experiments were done on '`x86_64`'. At the time of writing
binary 'releases' were available for that platform (called by them
'`x86`') and '`ppc64le`'.

---

#### C.2.2 Intel compilers

Intel compilers have been used under '`ix86`' and
'`x86_64`' Linux. Brian Ripley used version 9.0 of the
compilers for '`x86_64`' on Fedora Core 5 with

```r
CC=icc
CFLAGS="-g -O3 -wd188 -ip -mp"
FC=ifort
FLAGS="-g -O3 -mp"
CXX=icpc
CXXFLAGS="-g -O3 -mp"
ICC_LIBS=/opt/compilers/intel/cce/9.1.039/lib
IFC_LIBS=/opt/compilers/intel/fce/9.1.033/lib
LDFLAGS="-L$ICC_LIBS -L$IFC_LIBS -L/usr/local/lib64"
SHLIB_CXXLD=icpc
```

It may be necessary to use `CC="icc -std=c99"` or `CC="icc -c99"` for
C99-compliance. The flag `-wd188` suppresses a large number of
warnings about the enumeration type '`Rboolean`'. Because the
Intel C compiler sets '`__GNUC__`' without complete emulation
of `gcc`, we suggest adding `CPPFLAGS=-no-gcc`.

To maintain correct IEC 60559 arithmetic you most likely need add flags
to `CFLAGS`, `FFLAGS` and `CXXFLAGS` such as `-mp` (shown
above) or `-fp-model precise -fp-model source`, depending on
the compiler version.

Others have reported success with versions 10.x and 11.x. Bjørn-Helge
Mevik reported success with version 2015.3 of the compilers, using (for
a SandyBridge CPU on Centos 6.x)

```r
fast="-fp-model precise -ip -O3 -opt-mem-layout-trans=3 -xHost -mavx"
CC=icc
CFLAGS="$fast -wd188"
FC=ifort
FFLAGS="$fast"
CXX=icpc
CXXFLAGS="$fast"
```

It is possible that 32-builds need to force the use of SSE2 instructions
in `SAFE_FFLAGS`, e.g. by

```r
SAFE_FFLAGS=-axsse2
```

---

### C.3 macOS

('macOS' was known as 'OS X' from 2012--2016.)

The instructions here are for 64-bit ('`x86_64`') builds on
10.11 (El Capitan) or later. R can in principle be built for 10.6 and
later, although this is little tested and it may be necessary to install
later versions of software such as `libcurl`.

---

• [Prerequisites](#Prerequisites)     
 • [Recommended C/C++ compilers](#Recommended-C_002fC_002b_002b-compilers)     
 • [Other libraries](#Other-libraries)     
 • [Tcl/Tk headers and libraries](#Tcl_002fTk-headers-and-libraries)     
 • [Java (macOS)](#Java-_0028macOS_0029)     
 • [Frameworks](#Frameworks)     
 • [Building R.app](#Building-R_002eapp)

---

---

#### C.3.1 Prerequisites

The following are essential to build R

- Apple's 'Command Line Tools': these can be (re-)installed by
  `xcode-select --install`. (If you have a fresh OS installation,
  running e.g. `make` in a terminal will offer the installation of the
  command-line tools. If you have installed Xcode, this provides the
  command-line tools. The tools may need to be reinstalled when macOS
  is upgraded, as upgrading partially removes them.)

  The Command Line Tools provide C and C++ compilers.

- A Fortran compiler. Installers[^78^](#FOOT78) are available
  at

  - El Capitan and later\
    <https://cran.r-project.org/bin/macosx/tools/gfortran-6.1.pkg>,\
    which is a re-packaged (signed) version of\
    <https://github.com/fxcoudert/gfortran-for-macOS/releases/download/6.1/gfortran-6.1-ElCapitan.dmg>
  - Sierra and High Sierra\
    <https://github.com/fxcoudert/gfortran-for-macOS/releases/download/6.3/gfortran-6.3-Sierra.dmg>
  - Mojave and later\
    <https://github.com/fxcoudert/gfortran-for-macOS/releases/download/8.2/gfortran-8.2-Mojave.dmg>.

  These all install into `/usr/local/gfortran`. Its
  `bin` directory does not need to be on the path as a full
  path can be used for `FC`: see below.

- Binary components `pcre` and `xz` (for `libzma`) from
  <https://mac.R-project.org/libs>, as recent macOS versions provide
  libraries but not headers for these (and the system `pcre` is too
  old at 8.02 for versions up to Sierra, although High Sierra had
  8.40). For example

  ```r
  curl -OL https://mac.r-project.org/libs/pcre-8.40-darwin.15-x86_64.tar.gz
  sudo tar -fvxz pcre-8.40-darwin.15-x86_64.tar.gz -C /
  curl -OL https://mac.r-project.org/libs/xz-5.2.3-darwin.15-x86_64.tar.gz
  sudo tar -fvxz xz-5.2.3-darwin.15-x86_64.tar.gz -C /
  ```

and desirable

- GNU `readline` from <https://mac.R-project.org/libs>, or configure
  with `--without-readline`.

- Components `jpeg`, `libpng`, `pkgconfig`, `pkgconfig-system-stubs`
  and `tiff` from <https://mac.R-project.org/libs>, for the full range
  of bitmapped graphics devices.

- An X sub-system unless configuring using `--without-x`: see
  <https://xquartz.macosforge.org/>. R's `configure` script can be
  told to look for `X11` in `XQuartz`'s main location of
  `/opt/X11`, e.g. by

```r
--x-includes=/opt/X11/include --x-libraries=/opt/X11/lib
```

although linked versions under `/usr/X11` will be found.

- An Objective-C compiler, as provided by `clang` in the Command Line
  Tools: this is needed for the `quartz()` graphics device.

  Use `--without-aqua` if you want a standard Unix-alike
  build: apart from disabling `quartz()` and the ability to use the
  build with [R.APP]{.small}, it also changes the default location of
  the personal library (see `?.libPaths`).

- Support for `cairo` (without `Pango`) can be enabled if `pkg-config`
  and XQuartz are available. Make sure the XQuartz's `pkg-config`
  files are found first on the configuration path: for example by
  setting

```r
export PKG_CONFIG_PATH=/opt/X11/lib/pkgconfig:/usr/local/lib/pkgconfig:/usr/lib/pkgconfig
```

or appending that variable to the `configure` command.

- A TeX installation. See [Other libraries](#Other-libraries).

- `texi2any` from a '`texinfo`' distribution, which requires
  `perl` (currently part of macOS but it has been announced that it
  will not be from macOS 10.16). (An old version of `texi2any` has
  been included in the binary distribution of R.)

- Compilers supporting OpenMP: see the next subsection.

To build R itself from the sources with the compilers in the Command
Line Tools (or Xcode) and one of the `gfortran` installers, use a file
`config.site` containing

```r
CC=clang
OBJC=$CC
FC=/usr/local/gfortran/bin/gfortran
CXX=clang++
```

and configure by something like

```r
./configure -C \
--enable-R-shlib --enable-memory-profiling \
--x-includes=/opt/X11/include --x-libraries=/opt/X11/lib \
PKG_CONFIG_PATH=/opt/X11/lib/pkgconfig:/usr/local/lib/pkgconfig:/usr/lib/pkgconfig
```

To install packages using compiled code one needs the Command Line Tools
and appropriate compilers, e.g. Fortran and the C/C++ compilers from
those tools. Some packages have further requirements such as
`pkg-config`.

---

• [Note for Catalina users](#Note-for-Catalina-users)

---

---

#### C.3.1.1 Note for Catalina users

The default security settings for Catalina can make it difficult to
install Apple packages built after 2019-06-01 which have not been
'notarized'[^79^](#FOOT79) by Apple. And not just packages, as
this has been seen for executables contained in tarballs/zipfiles (for
example, for `pandoc`).

There are workarounds, including in some cases not installing the latest
version. Usually one can use '`Open With`'
(Control/right/two-finger-click in Finder), then select
'`Installer`' and '`Open`' if you get a further
warning message.

This applies also to some R distributions, including R 3.6.2 and
'nightly builds' from <https://mac.r-project.org/>.

---

#### C.3.2 Recommended C/C++ compilers

CRAN binary distributions of R 3.6.x use the build of `clang` 7.0.0
contained in
<https://cran.r-project.org/bin/macosx/tools/clang-7.0.0.pkg>. Other
recent distributions (including 9.0.0 and 8.0.0) of `clang` are
available from <http://releases.llvm.org/> (which the above
re-packages). In particular, these include support for OpenMP which
Apple builds of `clang` do not.

Suppose one of these distributions is installed under
`/usr/local/clang7`. Use a file `config.site`
containing

```r
CC=/usr/local/clang7/bin/clang
OBJC=$CC
FC=/usr/local/gfortran/bin/gfortran
CXX=/usr/local/clang7/bin/clang++
LDFLAGS="-L/usr/local/clang7/lib -L/usr/local/lib"
R_LD_LIBRARY_PATH=/usr/local/clang7/lib:/usr/local/lib
```

The care to specify library paths is to ensure that the OpenMP runtime
library, here `/usr/local/clang7/lib/libomp.dylib`, is found
when needed. If this works, you should see the line

```r
checking whether OpenMP SIMD reduction is supported... yes
```

in the `configure` output. Also, '`R_LD_LIBRARY_PATH`' needs to
be set to find the latest version of the C++ run-time libraries rather
than the system ones.

For macOS 10.14 ('Mojave') and versions 10.x of the Command Line Tools,
an additional step is needed to install the headers to
`/usr/include`: from a Terminal run

```r
sudo installer -pkg \
/Library/Developer/CommandLineTools/Packages/macOS_SDK_headers_for_macOS_10.14.pkg \
-target /
```

(This will need to be re-run if the OS decides to update the Command
Line Tools.)

Alternatively, change the system paths _via_

```r
CC="/usr/local/clang7/bin/clang -isysroot /Library/Developer/CommandLineTools/SDKs/MacOSX.sdk"
CXX="/usr/local/clang7/bin/clang++ -isysroot /Library/Developer/CommandLineTools/SDKs/MacOSX.sdk"
```

(The location of the SDK can be found by running
`xcrun -show-sdk-path`.)

This alternative approach is needed for versions 11.x of the Command
Line Tools/Xcode.

---

#### C.3.3 Other libraries

Pre-compiled versions of many of the [Useful libraries and programs](#Useful-libraries-and-programs) are available from
<https://mac.R-project.org/libs/>.

The `Accelerate` library[^80^](#FOOT80) can be used _via_ the
configuration options

```r
--with-blas="-framework Accelerate"
```

to provide potentially higher-performance versions of the BLAS and
LAPACK routines.[^81^](#FOOT81) This also includes a full
LAPACK which can be used _via_ `--with-lapack`: however, the
version of LAPACK it contains is often seriously old.

In recent versions of macOS, threading in Accelerate is controlled by
'Grand Central Dispatch' and is said not to need user control.

Looking at the top of
`/Library/Frameworks/R.framework/Resources/etc/Makeconf` will
show the compilers and configuration options used for the CRAN binary
package for R: at the time of writing the non-default options

```r
--enable-memory-profiling --enable-R-framework --x-libraries=/opt/X11/lib
```

were used. (`--enable-R-framework` implies
`--enable-R-shlib`.)

Configure option `--with-internal-tzcode` is the default on
macOS, as the system implementation of time zones does not work
correctly for times before 1902 or after 2037 (despite using a 64-bit
`time_t`).

The TeX implementation used by the developers is MacTeX
(<https://www.tug.org/mactex/>): the full installation is about 5GB, but
a smaller version ('Basic TeX') is available at
<https://www.tug.org/mactex/morepackages.html> to which you will need to
add some packages, e.g. for the 2019 version we needed to
add[^82^](#FOOT82) **cm-super**, **helvetic**, **inconsolata**
and **texinfo** which brought this to about 310MB. (After updates in Dec
2019 it was also necessary to add **letltxmacro** to make
`NEWS.pdf`.) '`TeX Live Utility`' (available _via_ the
MacTeX front page) provides a graphical means to manage TeX packages.
This is documented to require Sierra or later: for earlier versions see
the instructions on the MacTeX front page.

Checking packages thoroughly requires `ghostscript` (part of the full
MacTeX distribution or separately from
<https://www.tug.org/mactex/morepackages.html>) and `qpdf` (an early
version of which is in the `bin` directory of a binary
installation of R, usually
`/Library/Frameworks/R.framework/Resources/bin/qpdf`).

One macOS quirk is that the default path has `/usr/local/bin`
after `/usr/bin`, contrary to common practice on Unix-alikes.
This means that if you install tools from the sources they will by
default be installed under `/usr/local` and not supersede the
system versions.

---

#### C.3.4 Tcl/Tk headers and libraries

If you plan to use the `tcltk` package for R, you need to install a
distribution of Tcl/Tk. There are two alternatives. If you use
[R.APP]{.small} you will want to use X11-based Tcl/Tk (as used on other
Unix-alikes), which is installed as part of the CRAN binary for R and
available as separate `tcl` and `tk` components from
<https://mac.R-project.org/libs/>. This may need `configure` options

```r
-with-tcltk=/usr/local/lib
```

or

```r
--with-tcl-config=/usr/local/lib/tclConfig.sh
--with-tk-config=/usr/local/lib/tkConfig.sh
```

Note that this requires a matching XQuartz installation.

There is also a native ('Aqua') version of Tcl/Tk which produces widgets
in the native macOS style: this will not work with [R.APP]{.small}
because of conflicts over the macOS menu, but for those only using
command-line R this provides a much more intuitive interface to Tk for
experienced Mac users. Most versions of macOS come with Aqua Tcl/Tk
libraries, but these are not at all recent versions of Tcl/Tk (8.5.9 in
Sierra, which is not even the latest patched version in that series). It
is better to install Tcl/Tk 8.6.x from the sources or a binary
distribution from <https://www.activestate.com/activetcl/downloads>.
Configure R with

```r
--with-tcl-config=/Library/Frameworks/Tcl.framework/tclConfig.sh
--with-tk-config=/Library/Frameworks/Tk.framework/tkConfig.sh
```

If you need to find out which distribution of Tk is in use at run time,
use

```r
library(tcltk)
tclvalue(.Tcl("tk windowingsystem"))  # "x11" or "aqua"
```

---

#### C.3.5 Java

The situation with Java support on macOS is
messy,[^83^](#FOOT83) and distribution of Java for all
platforms changed in 2018.

macOS no longer comes with an installed Java runtime (JRE), and a macOS
upgrade may remove one if already installed: it is intended to be
installed at first use. Check if a JRE is installed by running
`java -version` in a `Terminal` window: if Java is not
installed[^84^](#FOOT84) this should prompt you to install it.
You can also install directly a recent Java from Oracle (currently from
<http://www.oracle.com/technetwork/java/javase/downloads/index.html>).
Builds of OpenJDK may also be available, e.g. from
<http://jdk.java.net/>. We recommend you install a version with
long-term support, e.g. 8 or 11 (but not 9, 10, 12 or 13 which have/had
a 6-month lifetime).

Binary distributions of R are built against a specific version (e.g. 9)
of Java so `sudo R CMD javareconf` will likely be needed before using
Java-using packages.

To see what compatible versions of Java are currently installed, run
`/usr/libexec/java_home -V -a x86_64`. If needed, set the environment
variable `JAVA_HOME` to choose between these, both when R is built from
the sources and when `R CMD javareconf` is run.

Configuring and building R both looks for a JRE and for support for
compiling JNI programs (used by packages
[**rJava**](https://CRAN.R-project.org/package=rJava) and
[**JavaGD**](https://CRAN.R-project.org/package=JavaGD)); the latter
requires a JDK (Java SDK) and not just a JRE[^85^](#FOOT85).

The build process tries to fathom out what JRE/JDK to use, but it may
need some help, e.g. by setting `JAVA_HOME`. A JDK can be specified
explicitly by something like

```r
JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk-11.jdk/Contents/Home
JAVA_CPPFLAGS="-I/${JAVA_HOME}/include -I/${JAVA_HOME}/include/darwin"
JAVA_LD_LIBRARY_PATH="${JAVA_HOME}/lib/server"
JAVA_LIBS="-L/${JAVA_HOME}/lib/server -ljvm"
```

or

```r
JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk1.8.0_191.jdk/Contents/Home
JAVA_CPPFLAGS="-I/${JAVA_HOME}/include -I/${JAVA_HOME}/include/darwin"
JAVA_LD_LIBRARY_PATH="${JAVA_HOME}/jre/lib/server"
JAVA_LIBS="-L/${JAVA_HOME}/jre/lib/server -ljvm"
```

in `config.site`.

To use the builds of OpenJDK (tarballs) from <http://jdk.java.net/>, set
`JAVA_HOME`:

```r
JAVA_HOME=/path/to/JDK/jdk-11.jdk/Contents/Home
```

where `/path/to/JDK` is wherever the distribution tarball was
unpacked.

Note that it is necessary to set the environment variable `NOAWT` to `1`
to install many of the Java-using packages.

---

#### C.3.6 Frameworks

The CRAN build of R is installed as a framework, which is selected by
the option

```r
./configure --enable-R-framework
```

(This is intended to be used with an Apple toolchain: others may not
support frameworks correctly but those from `llvm.org` do.)

It is only needed if you want to build R for use with the
[R.APP]{.small} console, and implies `--enable-R-shlib` to
build R as a dynamic library. This option configures R to be built and
installed as a framework called `R.framework`. The default
installation path for `R.framework` is
`/Library/Frameworks` but this can be changed at configure time
by specifying the flag `--enable-R-framework[=DIR]` (or
`--prefix`) or at install time _via_

```r
make prefix=/where/you/want/R.framework/to/go install
```

Note that installation as a framework is non-standard (especially to a
non-standard location) and Unix utilities may not support it (e.g. the
`pkg-config` file `libR.pc` will be put somewhere unknown to
`pkg-config`).

---

#### C.3.7 Building R.app

Note that building the [R.APP]{.small} GUI console is a separate
project, using Xcode. Before compiling [R.APP]{.small} make sure the
current version of R is installed in
`/Library/Frameworks/R.framework` and working at the
command-line (this can be a binary install).

The current sources can be checked out by

```r
svn co https://svn.r-project.org/R-packages/trunk/Mac-GUI
```

and built by loading the `R.xcodeproj` project (select the `R` target
and a suitable configuration), or from the command-line by e.g.

```r
xcodebuild -target R -configuration Release
```

See also the `INSTALL` file in the checkout or directly at
<https://svn.r-project.org/R-packages/trunk/Mac-GUI/INSTALL>.

[R.APP]{.small} does not need to be installed in any specific way.
Building [R.APP]{.small} results in the [R.APP]{.small} bundle which
appears as one R icon. This application bundle can be run anywhere and
it is customary to place it in the `/Applications` folder.

---

### C.4 Solaris

---

• [64-bit builds](#g_t64_002dbit-builds)     
 • [Using gcc](#Using-gcc)

---

R has been built successfully on Solaris 10 using the (zero cost) Oracle
Developer Studio[^86^](#FOOT86) compilers: there has also been
success with `gcc`/`gfortran`. (Recent Sun machines are AMD Opterons or
Intel Xeons ('`amd64`') rather than '`x86`', but
32-bit '`x86`' executables are the default.) How these
compilers identify themselves is slightly confusing: commands `CC -V`
with Developer Studio 12.5 and 12.6 report as versions 5.14 and 5.15. We
will only consider Developer Studio versions 12.5 (May 2016) and 12.6
(July 2017): instructions for 12.3 can be found in versions of this
manual for R 3.3.x.

There have been few reports on Solaris 11, with no known extra issues.

Solaris was last tested on Sparc machines in June 2017.

The Solaris versions of several of the tools needed to build R (e.g.
`make`, `ar` and `ld`) are in `/usr/ccs/bin`, so if using those
tools ensure this is in your path. A version of the preferred GNU `tar`
is (if installed) in `/usr/sfw/bin`. It may be necessary to
avoid the tools in `/usr/ucb`: POSIX-compliant versions of some
tools can be found in `/usr/xpg4/bin` and
`/usr/xpg6/bin`.

A large selection of Open Source software can be installed from
<https://www.opencsw.org>, by default installed under
`/opt/csw`. Solaris 10 ships with `bzlib` version 1.0.6
(sufficient) but `zlib` version 1.2.3 (too old): OpenCSW has 1.2.8.
(Note from 2019: updating of OpenCSW has slowed or stopped.)

At least when compiling with Oracle compilers, Solaris uses far more
stack space than other platforms. This makes it desirable to build PCRE
with the option `--disable-stack-for-recursion`: the OpenCSW
distribution was at the time of writing.

The Oracle compilers are unusual in not including
`/usr/local/include` in the default include search path: R's
default `CPPFLAGS=-I/usr/local/include` remedies this. If you rely on
OpenCSW software you may need `CPPFLAGS=-I/opt/csw/include` (or both).

You will need GNU `libiconv` and `readline`: the Solaris version of
`iconv` is not sufficiently powerful.

The native `make` suffices to build R but a number of packages require
GNU `make` (some without declaring it as '`SystemRequirements`'
in the `DESCRIPTION` file).

The support for the C99 `long double` type on Sparc hardware uses
quad-precision arithmetic, and this is usually slow because it is done
by software emulation. On such systems the `configure` option
`--disable-long-double` can be used for faster but less
accurate computations.

The Solaris time-zone conversion services seem to be unreliable pre-1916
in Europe (when daylight-savings time was first introduced): most often
reporting in the non-existent DST variant. Using `configure` option
`--with-internal-tzcode` is recommended, and required if you
find time-zone abbreviations being given odd values (as has been seen on
64-bit builds without it).

When using the Oracle compilers do _not_ specify `-fast`, as
this disables IEEE arithmetic and `make check` will fail.

A little juggling of paths was needed to ensure GNU `libiconv` (in
`/usr/local`) was used rather than the Solaris `iconv`:

```r
CC="cc -xc99"
CFLAGS="-O -xlibmieee"
FC=f95
FFLAGS=-O
CXX=CC
CXXSTD="-std=c++11 -library=stdcpp,CrunG3"
CXX11STD="-std=c++11 -library=stdcpp,CrunG3"
CXX14STD="-std=c++14 -library=stdcpp,CrunG3"
CXXFLAGS=-O
R_LD_LIBRARY_PATH="/opt/developerstudio12.6/lib:/usr/local/lib:/opt/csw/lib"
```

The Oracle compilers do not by default conform to the C99 standard
(appendix F 8.9) on the return values of functions such as `log`: use
`-xlibmieee` to ensure this.

A peculiarity of some versions of the Fortran compiler has been that
when asked to link a shared object they did not link against all the
Fortran 9x runtime libraries, hence

```r
FCLIBS_XTRA="-lfsu /opt/developerstudio12.6/lib/libfui.so.2"
```

has been needed.

Using `-xlibmil` in `CFLAGS` or `-xlibmil` in `FFLAGS` allows more
system mathematical functions to be inlined.

On '`x86`' you will get marginally higher performance _via_

```r
CFLAGS="-xO5 -xlibmieee -xlibmil -nofstore -xtarget=native"
FFLAGS="-xO5 -libmil -nofstore -xtarget=native"
CXXFLAGS="-xO5 -xlibmil -nofstore -xtarget=native"
SAFE_FFLAGS="-O -libmil -fstore -xtarget=native"
```

but the use of `-nofstore` can be less numerically stable, and some
packages have in the past failed to compile at optimization level 5.

The Oracle compilers provide several implementations of the C++
standards which select both the set of headers and a C++ runtime
library. One of those is selected by the `-library` flag, which
as it is needed for both compiling and linking is best specified as part
of the compiler or standard. Current R expects a C++11 compiler, for
which the choice given above is the only possibility. Although version
12.5 accepted the flag `-std=c++14`, it did not pass
`configure`'s conformance tests: version 12.6 does.

The performance library `sunperf` is available for use with the Oracle
compilers. If selected as a BLAS, it must also be selected as LAPACK
_via_

```r
./configure --with-blas='-library=sunperf' --with-lapack
```

This has often given test failures in the past, in several different
places.[^87^](#FOOT87)

Parsing very complex R expressions needs a lot of stack space when the
Oracle compilers are used: several packages require the stack increased
to at least 20MB.

Some people have reported that the Solaris `libintl` needs to be
avoided, for example by using `--disable-nls` or
`--with-included-gettext` or using `libintl` from OpenCSW. (On
the other hand, there have been many successful installs which
automatically detected `libintl` from OpenCSW or selected the included
`gettext`.)

It has been reported that some Solaris installations need

```r
INTERNET_LIBS="-lsocket -lnsl"
```

on the `configure` command line or in file `config.site`;
however, there have been many successful installs without this.

---

#### C.4.1 64-bit builds

On both '`x86`' and '`Sparc`' platforms the compilers
default to 32-bit code.

For a 64-bit target add `-m64` to the compiler macros and use
something like `LDFLAGS=-L/usr/local/lib/amd64` or
`LDFLAGS=-L/usr/local/lib/sparcv9` as appropriate (and other 64-bit
library directories if used, e.g. `-L/opt/csw/lib/amd64`). It will also
be necessary to point `pkg-config` at the 64-bit directories, e.g. by
something like

```r
PKG_CONFIG_PATH= /usr/local/lib/amd64/pkgconfig:/opt/csw/lib/64/pkgconfig:/usr/lib/64/pkgconfig
```

and to specify a 64-bit Java VM by e.g.

```r
JAVA_CPPFLAGS="-I${JAVA_HOME}/../include -I${JAVA_HOME}/../include/solaris"
JAVA_LD_LIBRARY_PATH=${JAVA_HOME}/lib/amd64/server
JAVA_LIBS="-L${JAVA_HOME}/lib/amd64/server \
  -R${JAVA_HOME}/lib/amd64/server -ljvm"
```

---

#### C.4.2 Using gcc

If using `gcc`, ensure that the compiler was compiled for the version of
Solaris in use. (This can be ascertained from `gcc -v`.) `gcc` makes
modified versions of some header files, and several reports of problems
were due to using `gcc` compiled on one version of Solaris on a later
version. Note that this can even apply to OS patches: some 2016 patches
to Solaris 10 changed its C header files in way
incompatible[^88^](#FOOT88) with the modified versions included
with OpenCSW's binary distribution.

The notes here are for `gcc` set up to use the Solaris linker: it can
also be set up to use GNU `ld`, but that has not been tested. The tests
were for compilers from the OpenCSW repository: Solaris systems often
come with much older compilers installed under `/usr/sfw/bin`.
One of `-m32` or `-m64` will be the default and could
be omitted, but it is not easy to find out which. (For OpenCSW it is
`-m32`.)

Compilation for an '`x86`' target with `gcc` 5.2.0 needed

```r
CC="gcc -m32"
CPPFLAGS="-I/opt/csw/include -I/usr/local/include"
FC="gfortran -m32"
CXX="g++ -m32"
LDFLAGS="-L/opt/csw/lib -L/usr/local/lib"
```

For an '`amd64`' target we used

```r
CC="gcc -m64"
CPPFLAGS="-I/opt/csw/include -I/usr/local/include"
FC="gfortran -m64"
CXX="g++ -m64"
LDFLAGS="-L/opt/csw/lib/amd64 -L/usr/local/lib/amd64"
```

Note that paths such as `/opt/csw/lib`,
`/usr/local/lib/amd64` and `/opt/csw/lib/amd64` may
need to be in the `LD_LIBRARY_PATH`
during configuration.

---

### C.5 FreeBSD

There have been few recent reports on FreeBSD: there is a 'port' at
<https://www.freebsd.org/ports/math.html>. Recent versions of FreeBSD
use Clang and the `libc++` C++ headers and runtime, but the 'port' is
configured to use GCC.

Use of ICU for collation and the `configure` option
`--with-internal-tzcode` are desirable workarounds.

---

### C.6 OpenBSD

Ingo Feinerer installed R version 3.2.2 on OpenBSD 5.8 arch
'`amd64`' (their name for '`x86_64`'). Details of the
build (and patches applied) are at
<http://cvsweb.openbsd.org/cgi-bin/cvsweb/ports/math/R/>. (Downgrading
the `zlib` requirement to 1.2.3 is against the advice of the R
developers.)

---

### C.7 Cygwin

The 32-bit version never worked well enough to pass R's `make check`,
and residual support from earlier experiments was removed in R 3.3.0.

The 64-bit version was never supported.

---

### C.8 New platforms

There are a number of sources of problems when installing R on a new
hardware/OS platform. These include

**Floating Point Arithmetic**: R requires arithmetic compliant with
IEC 60559, also known as IEEE 754. This mandates the use of plus and
minus infinity and `NaN` (not a number) as well as specific details of
rounding. Although almost all current FPUs can support this, selecting
such support can be a pain. The problem is that there is no agreement on
how to set the signalling behaviour; Sun/Sparc, SGI/IRIX and
'`ix86`' Linux require no special action, FreeBSD requires a
call to (the macro) `fpsetmask(0)` and OSF1 required that computation be
done with a `-ieee_with_inexact` flag etc. On a new platform
you must find out the magic recipe and add some code to make it work.
This can often be done via the file `config.site` which resides
in the top level directory.

Beware of using high levels of optimization, at least initially. On many
compilers these reduce the degree of compliance to the IEEE model. For
example, using `-fast` on the Oracle compilers has caused R's
`NaN` to be set incorrectly, and `gcc`'s `-ffast-math` and
`clang`'s `-Ofast` have given incorrect results.

**Shared Objects**: There seems to be very little agreement across
platforms on what needs to be done to build shared objects. there are
many different combinations of flags for the compilers and loaders. GNU
libtool cannot be used (yet), as it currently does not fully support
Fortran: one would need a shell wrapper for this). The technique we use
is to first interrogate the X window system about what it does (using
`xmkmf`), and then override this in situations where we know better (for
tools from the GNU Compiler Collection and/or platforms we know about).
This typically works, but you may have to manually override the results.
Scanning the manual entries for `cc` and `ld` usually reveals the
correct incantation. Once you know the recipe you can modify the file
`config.site` (following the instructions therein) so that the
build will use these options.

It seems that `gcc` 3.4.x and later on '`ix86`' Linux defeat
attempts by the LAPACK code to avoid computations entirely in
extended-precision registers, so file
`src/modules/lapack/dlamc.f` may need to be compiled without
optimization or with additional flags. Set the configure variable
`SAFE_FFLAGS` to the flags to be used for this file.

If you do manage to get R running on a new platform please let us know
about it so we can modify the configuration procedures to include that
platform.

If you are having trouble getting R to work on your platform please feel
free to use the '`R-devel`' mailing list to ask questions. We
have had a fair amount of practice at porting R to new platforms
[\...]{.small}

---

## Appendix D The Windows toolset

If you want to build R or add-on packages from source in Windows, you
will need to collect, install and test an extensive set of tools. See
<https://CRAN.R-project.org/bin/windows/Rtools/> for the current
locations and other updates to these instructions. (Most Windows users
will not need to build add-on packages from source; see [Add-on packages](#Add_002don-packages) for details.)

We have found that the build process for R is quite sensitive to the
choice of tools: please follow our instructions **exactly**, even to the
choice of particular versions of the tools.[^89^](#FOOT89) The
build process for add-on packages is somewhat more forgiving, but we
recommend using the exact toolset at first, and only substituting other
tools once you are familiar with the process.

_This appendix contains a lot of prescriptive comments. They are here as
a result of bitter experience. Please do not report problems to the R
mailing lists unless you have followed all the prescriptions._

We have collected most of the necessary tools (unfortunately not all,
due to license or size limitations) into an executable installer named
`Rtools*.exe`, available from
<https://CRAN.R-project.org/bin/windows/Rtools/>. You should download
and run it, choosing the default "Package authoring installation" to
build add-on packages, or the "full installation" if you intend to build
R.

You will need the following items to build R and packages. See the
subsections below for detailed descriptions.

- The command line tools (in `Rtools*.exe`)
- The MinGW-w64 32/64-bit toolchain to compile C, Fortran and C++.

For installing simple source packages containing data or R source but no
compiled code, none of these are needed.

A complete build of R including PDF manuals, and producing the installer
will also need the following:

- LaTeX
- The Inno Setup installer
- (optional) `qpdf`

It is important to set your `PATH` properly. The installer
`Rtools*.exe` optionally sets the path to components that it
installs.

Your `PATH` may include `.` first, then the `bin`
directories of the tools and LaTeX. Do not use filepaths containing
spaces: you can always use the short forms (found by `dir /x` at the
Windows command line). Network shares (with paths starting `\\`) are not
supported.

For example for a 32-bit build, all on one line,

```r
PATH=c:\Rtools\bin;c:\MiKTeX\miktex\bin;
     c:\R\R-3.2\bin\i386;c:\windows;c:\windows\system32
```

It is essential that the directory containing the command line tools
comes first or second in the path: there are typically like-named
tools[^90^](#FOOT90) in other directories, and they will
**not** work. The ordering of the other directories is less important,
but if in doubt, use the order above.

Our toolset contains copies of Cygwin DLLs that may conflict with other
ones on your system if both are in the path at once. The normal
recommendation is to delete the older ones; however, at one time we
found our tools did not work with a newer version of the Cygwin DLLs, so
it may be safest not to have any other version of the Cygwin DLLs in
your path.

---

• [LaTeX](#LaTeX)     
 • [The Inno Setup installer](#The-Inno-Setup-installer)     
 • [The command line tools](#The-command-line-tools)     
 • [The MinGW-w64 toolchain](#The-MinGW_002dw64-toolchain)     
 • [Useful additional programs](#Useful-additional-programs)

---

---

### D.1 LaTeX

The '`MiKTeX`' (<http://www.miktex.org/>) distribution of LaTeX
includes a suitable port of `pdftex`. This can be set up to install
extra packages 'on the fly', which is the simplest way to use it (and
the default). The 'basic' version of '`MiKTeX`' almost
suffices: when last checked packages

```r
epsf inconsolata mptopdf url
```

needed to be added (on the fly or _via_ the '`MiKTeX`' Package
Manager) to install R. In any case ensure that the **inconsolata**
package is installed---you can check with the '`MiKTeX`'
Package Manager.

The `Rtools*.exe` installer does _not_ include any version of
LaTeX.

It is also possible to use the TeX Live distribution from
<https://www.tug.org/texlive/>.

Please read [Making the manuals](#Making-the-manuals) about how to make
`fullrefman.pdf` and set the environment variable `R_RD4PDF`
suitably; ensure you have the required fonts installed or that
'`MiKTeX`' is set up to install LaTeX packages on first use.

---

### D.2 The Inno Setup installer

To make the installer package (`R-3.6.3-win.exe`) we currently
require the Unicode version of Inno Setup 5.3.7 or later from
<http://jrsoftware.org/> (starting from 6.0, Inno Setup provides only
one version, which supports Unicode). This is _not_ included in
`Rtools*.exe`.

Copy file `src/gnuwin32/MkRules.dist` to
`src/gnuwin32/MkRules.local` and edit it to set `ISDIR` to the
location where Inno Setup was installed.

---

### D.3 The command line tools

This item is installed by the `Rtools*.exe` installer.

If you choose to install these yourself, you will need suitable versions
of at least `basename`, `cat`, `cmp`, `comm`, `cp`, `cut`, `date`,
`diff`, `du`, `echo`, `expr`, `gzip`, `ls`, `make`, `makeinfo`, `mkdir`,
`mv`, `rm`, `rsync`, `sed`, `sh`, `sort`, `tar`, `texindex`, `touch` and
`uniq`; we use those from the Cygwin distribution
(<https://www.cygwin.com/>) or compiled from the sources. You will also
need `zip` and `unzip` from the Info-ZIP project
(<http://www.info-zip.org/>). All of these tools are in
`Rtools*.exe`.

**Beware**: 'Native' ports of make are **not** suitable (including those
called 'MinGW make' at the MinGW SourceForge site and `mingw32-make` in
some MinGW-w64 distributions). There were also problems with other
versions of the Cygwin tools and DLLs. To avoid frustration, please use
our tool set, and make sure it is at the front of your path (including
before the Windows system directories). If you are using a Windows
shell, type `PATH` at the prompt to find out.

You may need to set the environment variable `CYGWIN` to a value
including '`nodosfilewarning`' to suppress messages about
Windows-style paths.

---

### D.4 The MinGW-w64 toolchain

Technically you need more than just a compiler so the set of tools is
referred to as a 'toolchain'.

The preferred toolchain is part of `Rtools*.exe`: this uses a version of
`gcc 4.9.3` and version rt_v3 of the MinGW-w64 project's runtime.

This toolchain does not use _multilib_: separate front-ends are used for
32-bit and 64-bit compilation. These compilers need to be specified in
`BINPREF` and `BINPREF64` make variables as described previously at the
end of [Windows packages](#Windows-packages).

To select a 32-bit or 64-bit build of R, set the options in
`MkRules.local` appropriately (following the comments in the
file).

Some external software libraries will need to be re-compiled under the
new toolchain: especially those providing a C++ interface. Many of those
used by CRAN packages are available from
<https://www.stats.ox.ac.uk/pub/Rtools/multilib/>. Users developing
packages with [**Rcpp**](https://CRAN.R-project.org/package=Rcpp) need
to ensure that they use a version built with exactly the same toolchain
as their package: the recommendation is to build
[**Rcpp**](https://CRAN.R-project.org/package=Rcpp) from its sources
yourself.

There is support for OpenMP and pthreads in this toolchain. As the
performance of OpenMP on Windows is poor for small tasks, it is not used
for R itself.

---

### D.5 Useful additional programs

The process of making the installer will make use of `qpdf` to compact
some of the package vignettes, if it is available. Windows binaries of
`qpdf` are available from <http://sourceforge.net/projects/qpdf/files/>.
Set the path to the `qpdf` installation in file
`MkRules.local`.

Developers of packages will find some of the 'goodies' at
<https://www.stats.ox.ac.uk/pub/Rtools/goodies> useful.

There is a version of the `file` command that identifies the type of
files, and is used by `Rcmd check` if available. The binary distribution
is included in `Rtools*.exe`.

The file `xzutils.zip` contains the program `xz` which can be
used to (de)compress files with that form of compression.

---

## Function and variable index

---

Jump to:   [**C**](#Function-and-variable-index_vr_letter-C){.summary-letter}   [**I**](#Function-and-variable-index_vr_letter-I){.summary-letter}   [**M**](#Function-and-variable-index_vr_letter-M){.summary-letter}   [**R**](#Function-and-variable-index_vr_letter-R){.summary-letter}   [**U**](#Function-and-variable-index_vr_letter-U){.summary-letter}

---

Index Entry

Section

---

C

[`configure`](#index-configure):

[Simple compilation](#Simple-compilation)

[`configure`](#index-configure-1):

[Simple compilation](#Simple-compilation)

[`configure`](#index-configure-2):

[Installation](#Installation)

[`configure`](#index-configure-3):

[Installation](#Installation)

[`configure`](#index-configure-4):

[Configuration variables](#Configuration-variables)

[`configure`](#index-configure-5):

[Using make](#Using-make)

---

I

[`install.packages`](#index-install_002epackages):

[Installing packages](#Installing-packages)

---

M

[`make`](#index-make):

[Using make](#Using-make)

---

R

[`remove.packages`](#index-remove_002epackages):

[Removing packages](#Removing-packages)

[`R_HOME`](#index-R_005fHOME):

[Simple compilation](#Simple-compilation)

---

U

[`update.packages`](#index-update_002epackages):

[Updating packages](#Updating-packages)

---

---

Jump to:   [**C**](#Function-and-variable-index_vr_letter-C){.summary-letter}   [**I**](#Function-and-variable-index_vr_letter-I){.summary-letter}   [**M**](#Function-and-variable-index_vr_letter-M){.summary-letter}   [**R**](#Function-and-variable-index_vr_letter-R){.summary-letter}   [**U**](#Function-and-variable-index_vr_letter-U){.summary-letter}

---

---

## Concept index

---

Jump to:   [**B**](#Concept-index_cp_letter-B){.summary-letter}   [**F**](#Concept-index_cp_letter-F){.summary-letter}   [**I**](#Concept-index_cp_letter-I){.summary-letter}   [**L**](#Concept-index_cp_letter-L){.summary-letter}   [**M**](#Concept-index_cp_letter-M){.summary-letter}   [**O**](#Concept-index_cp_letter-O){.summary-letter}   [**P**](#Concept-index_cp_letter-P){.summary-letter}   [**R**](#Concept-index_cp_letter-R){.summary-letter}   [**S**](#Concept-index_cp_letter-S){.summary-letter}   [**U**](#Concept-index_cp_letter-U){.summary-letter}   [**V**](#Concept-index_cp_letter-V){.summary-letter}   [**W**](#Concept-index_cp_letter-W){.summary-letter}

---

Index Entry

Section

---

B

[BLAS library](#index-BLAS-library):

[Linear algebra](#Linear-algebra)

[BLAS library](#index-BLAS-library-1):

[Other libraries](#Other-libraries)

[BLAS library](#index-BLAS-library-2):

[Solaris](#Solaris)

---

F

[Fortran](#index-Fortran):

[Using Fortran](#Using-Fortran)

[FreeBSD](#index-FreeBSD):

[FreeBSD](#FreeBSD)

---

I

[Installation](#index-Installation):

[Installation](#Installation)

[Installing under Unix-alikes](#index-Installing-under-Unix_002dalikes):

[Installing R under Unix-alikes](#Installing-R-under-Unix_002dalikes)

[Installing under Windows](#index-Installing-under-Windows):

[Installing R under Windows](#Installing-R-under-Windows)

[Internationalization](#index-Internationalization):

[Internationalization](#Internationalization)

---

L

[LAPACK library](#index-LAPACK-library):

[LAPACK](#LAPACK)

[LAPACK library](#index-LAPACK-library-1):

[Other libraries](#Other-libraries)

[LAPACK library](#index-LAPACK-library-2):

[Solaris](#Solaris)

[Libraries](#index-Libraries):

[Add-on packages](#Add_002don-packages)

[Libraries, managing](#index-Libraries_002c-managing):

[Managing libraries](#Managing-libraries)

[Libraries, site](#index-Libraries_002c-site):

[Managing libraries](#Managing-libraries)

[Libraries, user](#index-Libraries_002c-user):

[Managing libraries](#Managing-libraries)

[Linux](#index-Linux):

[Installing R under Unix-alikes](#Installing-R-under-Unix_002dalikes)

[Linux](#index-Linux-1):

[Linux](#Linux)

[Locale](#index-Locale):

[Internationalization](#Internationalization)

[Locale](#index-Locale-1):

[Locales](#Locales)

[Localization](#index-Localization):

[Internationalization](#Internationalization)

---

M

[macOS](#index-macOS):

[Installing R under Unix-alikes](#Installing-R-under-Unix_002dalikes)

[macOS](#index-macOS-1):

[Installing R under macOS](#Installing-R-under-macOS)

[macOS](#index-macOS-2):

[macOS](#macOS)

[Manuals](#index-Manuals):

[Making the manuals](#Making-the-manuals)

[Manuals, installing](#index-Manuals_002c-installing):

[Installation](#Installation)

---

O

[Obtaining R](#index-Obtaining-R):

[Obtaining R](#Obtaining-R)

[OpenBSD](#index-OpenBSD):

[OpenBSD](#OpenBSD)

---

P

[Packages](#index-Packages):

[Add-on packages](#Add_002don-packages)

[Packages, default](#index-Packages_002c-default):

[Default packages](#Default-packages)

[Packages, installing](#index-Packages_002c-installing):

[Installing packages](#Installing-packages)

[Packages, removing](#index-Packages_002c-removing):

[Removing packages](#Removing-packages)

[Packages, updating](#index-Packages_002c-updating):

[Updating packages](#Updating-packages)

---

R

[Repositories](#index-Repositories):

[Setting up a package repository](#Setting-up-a-package-repository)

---

S

[Site libraries](#index-Site-libraries):

[Managing libraries](#Managing-libraries)

[Solaris](#index-Solaris):

[Solaris](#Solaris)

[Sources for R](#index-Sources-for-R):

[Getting and unpacking the sources](#Getting-and-unpacking-the-sources)

[Subversion](#index-Subversion):

[Using Subversion and rsync](#Using-Subversion-and-rsync)

[Subversion](#index-Subversion-1):

[Essential programs and libraries](#Essential-programs-and-libraries)

---

U

[User libraries](#index-User-libraries):

[Managing libraries](#Managing-libraries)

---

V

[Vignettes](#index-Vignettes):

[Essential programs and libraries](#Essential-programs-and-libraries)

---

W

[winCairo.dll](#index-winCairo_002edll):

[Building the cairo devices files](#Building-the-cairo-devices-files)

---

---

Jump to:   [**B**](#Concept-index_cp_letter-B){.summary-letter}   [**F**](#Concept-index_cp_letter-F){.summary-letter}   [**I**](#Concept-index_cp_letter-I){.summary-letter}   [**L**](#Concept-index_cp_letter-L){.summary-letter}   [**M**](#Concept-index_cp_letter-M){.summary-letter}   [**O**](#Concept-index_cp_letter-O){.summary-letter}   [**P**](#Concept-index_cp_letter-P){.summary-letter}   [**R**](#Concept-index_cp_letter-R){.summary-letter}   [**S**](#Concept-index_cp_letter-S){.summary-letter}   [**U**](#Concept-index_cp_letter-U){.summary-letter}   [**V**](#Concept-index_cp_letter-V){.summary-letter}   [**W**](#Concept-index_cp_letter-W){.summary-letter}

---

---

## Environment variable index

---

Jump to:   [**B**](#Environment-variable-index_en_letter-B){.summary-letter}   [**C**](#Environment-variable-index_en_letter-C){.summary-letter}   [**D**](#Environment-variable-index_en_letter-D){.summary-letter}   [**J**](#Environment-variable-index_en_letter-J){.summary-letter}   [**L**](#Environment-variable-index_en_letter-L){.summary-letter}   [**P**](#Environment-variable-index_en_letter-P){.summary-letter}   [**R**](#Environment-variable-index_en_letter-R){.summary-letter}   [**T**](#Environment-variable-index_en_letter-T){.summary-letter}

---

Index Entry

Section

---

B

[`BINPREF`](#index-BINPREF):

[Windows packages](#Windows-packages)

[`BINPREF64`](#index-BINPREF64):

[Windows packages](#Windows-packages)

[`BLAS_LIBS`](#index-BLAS_005fLIBS):

[BLAS](#BLAS)

---

C

[`CONFIG_SITE`](#index-CONFIG_005fSITE):

[Configuration variables](#Configuration-variables)

[`CYGWIN`](#index-CYGWIN):

[The command line tools](#The-command-line-tools)

---

D

[`DESTDIR`](#index-DESTDIR):

[Installation](#Installation)

[`DESTDIR`](#index-DESTDIR-1):

[Unix-alike standalone](#Unix_002dalike-standalone)

---

J

[`JAVA_HOME`](#index-JAVA_005fHOME):

[Java support](#Java-support)

---

L

[`LANG`](#index-LANG):

[Localization of messages](#Localization-of-messages)

[`LANGUAGE`](#index-LANGUAGE):

[Localization of messages](#Localization-of-messages)

[`LANGUAGE`](#index-LANGUAGE-1):

[Localization of messages](#Localization-of-messages)

[`LAPACK_LIBS`](#index-LAPACK_005fLIBS):

[LAPACK](#LAPACK)

[`LC_ALL`](#index-LC_005fALL):

[Localization of messages](#Localization-of-messages)

[`LC_COLLATE`](#index-LC_005fCOLLATE):

[Testing a Unix-alike Installation](#Testing-a-Unix_002dalike-Installation)

[`LC_MESSAGES`](#index-LC_005fMESSAGES):

[Localization of messages](#Localization-of-messages)

[`LD_LIBRARY_PATH`](#index-LD_005fLIBRARY_005fPATH):

[Unix-alike standalone](#Unix_002dalike-standalone)

[`LD_LIBRARY_PATH`](#index-LD_005fLIBRARY_005fPATH-1):

[Using Fortran](#Using-Fortran)

[`LD_LIBRARY_PATH`](#index-LD_005fLIBRARY_005fPATH-2):

[Compile and load flags](#Compile-and-load-flags)

[`LD_LIBRARY_PATH`](#index-LD_005fLIBRARY_005fPATH-3):

[Using gcc](#Using-gcc)

[`LOCAL_SOFT`](#index-LOCAL_005fSOFT):

[Windows packages](#Windows-packages)

---

P

[`PAPERSIZE`](#index-PAPERSIZE):

[Setting paper size](#Setting-paper-size)

[`PATH`](#index-PATH):

[Essential programs and libraries](#Essential-programs-and-libraries)

[`PATH`](#index-PATH-1):

[Using Fortran](#Using-Fortran)

[`PATH`](#index-PATH-2):

[The Windows toolset](#The-Windows-toolset)

---

R

[`R_ARCH`](#index-R_005fARCH):

[Sub-architectures](#Sub_002darchitectures)

[`R_ARCH`](#index-R_005fARCH-1):

[Sub-architectures](#Sub_002darchitectures)

[`R_BROWSER`](#index-R_005fBROWSER):

[Setting the browsers](#Setting-the-browsers)

[`R_DEFAULT_PACKAGES`](#index-R_005fDEFAULT_005fPACKAGES):

[Default packages](#Default-packages)

[`R_DISABLE_HTTPD`](#index-R_005fDISABLE_005fHTTPD):

[Help options](#Help-options)

[`R_GSCMD`](#index-R_005fGSCMD):

[Useful libraries and programs](#Useful-libraries-and-programs)

[`R_INSTALL_TAR`](#index-R_005fINSTALL_005fTAR):

[Windows packages](#Windows-packages)

[`R_JAVA_LD_LIBRARY_PATH`](#index-R_005fJAVA_005fLD_005fLIBRARY_005fPATH):

[Java support](#Java-support)

[`R_JAVA_LD_LIBRARY_PATH`](#index-R_005fJAVA_005fLD_005fLIBRARY_005fPATH-1):

[Java support](#Java-support)

[`R_LIBS`](#index-R_005fLIBS):

[Add-on packages](#Add_002don-packages)

[`R_LIBS_SITE`](#index-R_005fLIBS_005fSITE):

[Managing libraries](#Managing-libraries)

[`R_LIBS_USER`](#index-R_005fLIBS_005fUSER):

[Managing libraries](#Managing-libraries)

[`R_PAPERSIZE`](#index-R_005fPAPERSIZE):

[Making the manuals](#Making-the-manuals)

[`R_PAPERSIZE`](#index-R_005fPAPERSIZE-1):

[Running R](#Running-R)

[`R_PAPERSIZE`](#index-R_005fPAPERSIZE-2):

[Setting paper size](#Setting-paper-size)

[`R_PAPERSIZE`](#index-R_005fPAPERSIZE-3):

[Making manuals](#Making-manuals)

[`R_PDFVIEWER`](#index-R_005fPDFVIEWER):

[Setting the browsers](#Setting-the-browsers)

[`R_RD4PDF`](#index-R_005fRD4PDF):

[Making the manuals](#Making-the-manuals)

[`R_RD4PDF`](#index-R_005fRD4PDF-1):

[Making manuals](#Making-manuals)

[`R_RD4PDF`](#index-R_005fRD4PDF-2):

[LaTeX](#LaTeX)

[`R_SCRIPT_DEFAULT_PACKAGES`](#index-R_005fSCRIPT_005fDEFAULT_005fPACKAGES):

[Default packages](#Default-packages)

[`R_USER`](#index-R_005fUSER):

[Running R](#Running-R)

---

T

[`TAR`](#index-TAR):

[Essential programs and libraries](#Essential-programs-and-libraries)

[`TAR_OPTIONS`](#index-TAR_005fOPTIONS):

[Getting and unpacking the sources](#Getting-and-unpacking-the-sources)

[`TAR_OPTIONS`](#index-TAR_005fOPTIONS-1):

[Getting the source files](#Getting-the-source-files)

[`TEMP`](#index-TEMP):

[Running R](#Running-R)

[`TMP`](#index-TMP):

[Running R](#Running-R)

[`TMPDIR`](#index-TMPDIR):

[Simple compilation](#Simple-compilation)

[`TMPDIR`](#index-TMPDIR-1):

[Building the core files](#Building-the-core-files)

[`TMPDIR`](#index-TMPDIR-2):

[Running R](#Running-R)

[`TMPDIR`](#index-TMPDIR-3):

[Running R](#Running-R)

[`TMPDIR`](#index-TMPDIR-4):

[Installing packages](#Installing-packages)

---

---

Jump to:   [**B**](#Environment-variable-index_en_letter-B){.summary-letter}   [**C**](#Environment-variable-index_en_letter-C){.summary-letter}   [**D**](#Environment-variable-index_en_letter-D){.summary-letter}   [**J**](#Environment-variable-index_en_letter-J){.summary-letter}   [**L**](#Environment-variable-index_en_letter-L){.summary-letter}   [**P**](#Environment-variable-index_en_letter-P){.summary-letter}   [**R**](#Environment-variable-index_en_letter-R){.summary-letter}   [**T**](#Environment-variable-index_en_letter-T){.summary-letter}

---

---

#### Footnotes

[(1)](#DOCF1)

e.g. GNU `tar` version 1.15 or later, or that from the
'`libarchive`' (as used on macOS versions 10.6 and later) or
'Heirloom Toolchest' distributions.

[(2)](#DOCF2)

for some Subversion clients '`http:`' may appear to work, but
requires continual redirection.

[(3)](#DOCF3)

Most aspects will work with paths containing spaces, but external
software used by R may not.

[(4)](#DOCF4)

which use `lib` rather than `lib64` for their primary
64-bit library directories.

[(5)](#DOCF5)

Instructions on how to install the latest version are at
<https://www.ctan.org/tex-archive/fonts/inconsolata/>.

[(6)](#DOCF6)

on a Unix-alike, '`inconsolata`' is omitted if not found by
`configure`.

[(7)](#DOCF7)

This will be needed if more than one sub-architecture is to be
installed.

[(8)](#DOCF8)

with possible values '`i386`', '`x64`',
'`32`' and '`64`'.

[(9)](#DOCF9)

mainly on RedHat and Fedora, whose layout is described here.

[(10)](#DOCF10)

How to prepare such a directory is described in file
`src/extra/tzone/Notes` in the R sources.

[(11)](#DOCF11)

for example, `-fopenmp`, `-xopenmp` or
`-qopenmp`. This includes for `clang` and the Intel and Oracle
compilers.

[(12)](#DOCF12)

This does not necessarily disable _use_ of OpenMP -- the `configure`
code allows for platforms where OpenMP is used without a flag. For the
`flang` compiler in late 2017, the Fortran runtime always used OpenMP.

[(13)](#DOCF13)

Currently this is a valid option for `g++` 5 and later and 2016 versions
of the Intel and Solaris compilers. For earlier versions of `g++` one
could try `-std=c++1y`.

[(14)](#DOCF14)

This is true for earlier versions of `g++` such as 4.2.1, and also for
earlier versions of the Solaris compiler `CC`.

[(15)](#DOCF15)

For when features were supported, see
<https://gcc.gnu.org/projects/cxx-status.html#cxx11>.

[(16)](#DOCF16)

Nowadays part of GNU `binutils` and used by LLVM to support LTO. It is
sometimes installed as `ld.gold`.

[(17)](#DOCF17)

probably also 8.4 and later when released.

[(18)](#DOCF18)

or 9.1-patched since 2019-05-09.

[(19)](#DOCF19)

Suitable distributions include Strawberry Perl,
<http://strawberryperl.com/> and ActivePerl,
<https://www.activestate.com/activeperl>.

[(20)](#DOCF20)

The installer puts links to `R` and `Rscript` in
`/usr/local/bin`. If these are missing, you can run directly
the copies in `/Library/Frameworks/R.framework/Resources/`.

[(21)](#DOCF21)

The framework for R 3.3.x was named `org.r-project.R.mavericks.fw.pkg`:
use `pkgutil --pkgs | grep org.r-project` to check for earlier versions
of R.

[(22)](#DOCF22)

More precisely, of the Apple package of the same name: this means that
installing a package for 3.3.x does not remove an installation for 3.4.x
or later.

[(23)](#DOCF23)

The Oracle compilers on Solaris (where the issue is parsing very complex
R expressions) and GCC 9 on Linux.

[(24)](#DOCF24)

unless they were excluded in the build.

[(25)](#DOCF25)

its binding is locked once the startup files have been read, so users
cannot easily change it.

[(26)](#DOCF26)

If a proxy needs to be set, see `?download.file`.

[(27)](#DOCF27)

for a small number of CRAN packages where this is known to be safe and
is needed by the autobuilder this is the default. Look at the source of
`tools:::.install_packages` for the list. It can also be
specified in the package's `DESCRIPTION` file.

[(28)](#DOCF28)

or by adding it in a file such as `etc/i386/Makevars.site`,
which does not exist by default.

[(29)](#DOCF29)

Note that capitalization and version may differ from the Open Source
project.

[(30)](#DOCF30)

using a path containing spaces is likely to cause problems

[(31)](#DOCF31)

They need to have been created using
`-headerpad_max_install_names`, which is the default for an R
package.

[(32)](#DOCF32)

'X/Open Portability Guide', which has had several versions.

[(33)](#DOCF33)

On some systems setting `LC_ALL` or `LC_MESSAGES` to '`C`'
disables `LANGUAGE`.

[(34)](#DOCF34)

If you try changing from French to Russian except in a UTF-8 locale, you
will most likely find messages change to English.

[(35)](#DOCF35)

the language written in England: some people living in the USA
appropriate this name for their language.

[(36)](#DOCF36)

with Americanisms.

[(37)](#DOCF37)

also known as IEEE 754

[(38)](#DOCF38)

at least when storing quantities: the on-FPU precision is allowed to
vary

[(39)](#DOCF39)

e.g. Bessel, beta and gamma functions

[(40)](#DOCF40)

including copying `MkRules.dist` to `MkRule.local` and
selecting the architecture.

[(41)](#DOCF41)

also known as IEEE 754

[(42)](#DOCF42)

Note that C11 compilers need not be C99-compliant: R requires support
for `double complex` and variable-length arrays which are optional in
C11 but are mandatory in C99. C18 (also known as C17) is a 'bugfix
release' of C11, clarifying the standard.

[(43)](#DOCF43)

Examples are `-std=gnu99`, `-std=c99` and
`-c99`.

[(44)](#DOCF44)

`-std=c99` excludes POSIX functionality, but
`config.h` will turn on all GNU extensions to include the POSIX
functionality for R itself: this does not apply to badly-written
packages. The default mode for GCC 5.1 and later is
`-std=gnu11`, which currently includes the optional features R
needs.

[(45)](#DOCF45)

However, it is possible to break the default behaviour of `glibc` by
re-specifying the `gconv` modules to be loaded.

[(46)](#DOCF46)

specifically, the C99 functionality of headers `wchar.h` and
`wctype.h`, types `wctans_t` and `mbstate_t` and functions
`mbrtowc`, `mbstowcs`, `wcrtomb`, `wcscoll`, `wcstombs`, `wctrans`,
`wctype`, and `iswctype`.

[(47)](#DOCF47)

including `expm1`, `hypot`, `log1p`, `nearbyint` and `va_copy`.

[(48)](#DOCF48)

including `opendir`, `readdir`, `closedir`, `popen`, `stat`, `glob`,
`access`, `getcwd` and `chdir` system calls, `select` on a Unix-alike,
and either `putenv` or `setenv`.

[(49)](#DOCF49)

such as `realpath`, `symlink`.

[(50)](#DOCF50)

most often distributed as part of `xz`: possible names in Linux
distributions include `xz-devel`/`xz-libs` and `liblzma-dev`.

[(51)](#DOCF51)

sometimes known as PCRE1, and not PCRE2 which started at version 10.0.

[(52)](#DOCF52)

but not a major version greater than 7 should there ever be one: the
major version has been 7 since 2000.

[(53)](#DOCF53)

for example to specify static linking with a build which has both shared
and static libraries.

[(54)](#DOCF54)

Such as GNU `tar` 1.15 or later, `bsdtar` (from
<https://github.com/libarchive/libarchive/>, as used as `tar` by FreeBSD
and macOS 10.6 and later) or `tar` from the Heirloom Toolchest
(<http://heirloom.sourceforge.net/tools.html>), although the latter does
not support `xz` compression.

[(55)](#DOCF55)

`texi2dvi` is normally a shell script. Some versions (including those
from **texinfo** 5.2 and 6.0-6.6) need to be run under `bash` rather
than a Bourne shell, especially on Solaris. Some of the issues which
have been observed with broken versions of `texi2dvi` can be
circumvented by setting the environment variable `R_TEXI2DVICMD` to the
value `emulation`.

[(56)](#DOCF56)

If necessary the path to `pkg-config` can be specified by setting
`PKG_CONFIG` in `config.site`, on the `configure` command line
or in the environment.

[(57)](#DOCF57)

also known as `ttf-mscorefonts-installer` in the Debian/Ubuntu world:
see also <https://en.wikipedia.org/wiki/Core_fonts_for_the_Web>.

[(58)](#DOCF58)

`ttf-liberation` in Debian/Ubuntu.

[(59)](#DOCF59)

This is the default as from `glibc` 2.26 and has been confirmed for
Fedora 28, which does not mention this on its `man` pages.

[(60)](#DOCF60)

R uses `rpc/xdr.h` but that includes `netconfig.h`
from the top `tirpc` directory.

[(61)](#DOCF61)

This is true even for the 'Aqua' version of Tk on macOS, but
distributions of that include a copy of the X11 files needed.

[(62)](#DOCF62)

The search includes OpenBLAS, ATLAS and a generic `libblas`,
plus some platform-specific choices (see below).

[(63)](#DOCF63)

Using the Oracle Developer Studio `cc` and `f95` compilers

[(64)](#DOCF64)

There were others for earlier versions of ATLAS, and are for non-Intel
architectures. The only way to see exactly which CPUs the distributed
libraries have been tuned for is to read the `atlas.spec` file:
at the time of writing '`HAMMER64SSE3`' and
'`Corei264AVX`' for '`x86_64`' Fedora.

[(65)](#DOCF65)

<http://math-atlas.sourceforge.net/atlas_install/>

[(66)](#DOCF66)

<http://math-atlas.sourceforge.net/faq.html#tnum>

[(67)](#DOCF67)

(and more, e.g. for 64-bit ints and static versions).

[(68)](#DOCF68)

The issue for macOS has been the use of double-complex routines.

[(69)](#DOCF69)

We have measured 15--20% on '`i686`' Linux and around 10% on
'`x86_64`' Linux.

[(70)](#DOCF70)

We believe that versions 3.4.0 to 3.13.0 are compatible.

[(71)](#DOCF71)

At the time of writing using this with `-pedantic` still gave
an error.

[(72)](#DOCF72)

at the time of revision of this para in late 2018, **autoconf-2.69**
from 2012 and **automake-1.16.1** from 2018.

[(73)](#DOCF73)

The links there have proved difficult to access, in which case either
point an FTP client at <ftp://www.eecs.harvard.edu/pub/nr/> or grab the
copy made available at <http://developer.r-project.org/noweb-2.11b.tgz>.

[(74)](#DOCF74)

for example, `X11 font at size 14 could not be loaded`.

[(75)](#DOCF75)

For example, `glibc`: other C libraries such as `musl` have been used
but are not routinely tested.

[(76)](#DOCF76)

This has been announced to change in version 2.29, having been postponed
from 2.28.

[(77)](#DOCF77)

This also needs the OpenMP runtime which has sometimes been distributed
separately.

[(78)](#DOCF78)

Some of these are unsigned packages: to install them you may need to
right-click and select `Open with -> Installer`.

[(79)](#DOCF79)

See
<https://developer.apple.com//documentation/xcode/notarizing_macos_software_before_distribution>.

[(80)](#DOCF80)

<https://developer.apple.com/documentation/accelerate>.

[(81)](#DOCF81)

It was reported that for some non-Apple toolchains `CPPFLAGS` needed to
contain `-D__ACCELERATE__`: not needed for `clang` from
[releases.llvm.org](releases.llvm.org) though.

[(82)](#DOCF82)

E.g. _via_ `tlmgr install cm-super helvetic inconsolata texinfo` .

[(83)](#DOCF83)

For more details see <http://www.macstrategy.com/article.php?3>.

[(84)](#DOCF84)

In the unlikely event that the version reported does not start with
`1.8.0`, `11` or higher you need to update your Java.

[(85)](#DOCF85)

As from Java 11, there is no separate client JRE distribution.

[(86)](#DOCF86)

Oracle Solaris Studio prior to 2016, and previously Sun Studio.

[(87)](#DOCF87)

When last checked it failed in `tests/reg-BLAS.R`, and on some
builds, including for '`amd64`', it failed in `example(eigen)`.

[(88)](#DOCF88)

In particular, header `cmath` in C++11 mode includes
`math.h` and `iso/math_c99.h` and `gcc` had 'fixed' an
earlier version of the latter.

[(89)](#DOCF89)

For example, the Cygwin version of `make 3.81` fails to work correctly.

[(90)](#DOCF90)

such as `sort`, `find` and perhaps `make`.

---
