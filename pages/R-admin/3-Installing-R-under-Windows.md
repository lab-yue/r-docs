3 Installing R under Windows

---

The `bin/windows` directory of a CRAN site contains binaries
for a base distribution and a large number of add-on packages from CRAN
to run on 32- or 64-bit Windows (Windows 7 and later are tested; XP is
known to fail some tests) on '`ix86`' and '`x86_64`'
CPUs.

Your file system must allow long file names (as is likely except perhaps
for some network-mounted systems). If it doesn't also support conversion
to short name equivalents (a.k.a. DOS 8.3 names), then R _must_ be
installed in a path that does not contain spaces.

Installation is _via_ the installer `R-3.6.3-win.exe`. Just
double-click on the icon and follow the instructions. When installing on
a 64-bit version of Windows the options will include 32- or 64-bit
versions of R (and the default is to install both). You can uninstall R
from the Control Panel.

Note that you will be asked to choose a language for installation, and
that choice applies to both installation and un-installation but not to
running R itself.

See the [R Windows FAQ](https://CRAN.R-project.org/bin/windows/base/rw-FAQ.html) for more
details on the binary installer.

---

• [Building from source](#Building-from-source)     
 • [Testing a Windows Installation](#Testing-a-Windows-Installation)

---

---

### 3.1 Building from source

R can be built as either a 32-bit or 64-bit application on Windows: to
build the 64-bit application you need a 64-bit edition of Windows: such
an OS can also be used to build 32-bit R.

The standard installer combines 32-bit and 64-bit builds into a single
executable which can then be installed into the same location and share
all the files except the `.exe` and `.dll` files and
some configuration files in the `etc` directory.

Building is only tested in a 8-bit locale: using a multi-byte locale (as
used for CJK languages) is unsupported and may not work (the scripts do
try to select a '`C`' locale; Windows may not honour this).

**NB:** The build process is currently being changed to require external
binary distributions of third-party software. Their location is set
using macro `EXT_LIBS` with default setting `$(LOCAL_SOFT)`;
the \$(LOCAL_SOFT) macro defaults to `$(R_HOME)/extsoft`. This
directory can be populated using `make rsync-extsoft`. The location can
be overridden by setting `EXT_LIBS` to a different path in
`src/gnuwin32/MkRules.local`. A suitable collection of files
can also be obtained from
<https://CRAN.R-project.org/bin/windows/extsoft> or
<https://www.stats.ox.ac.uk/pub/Rtools/libs.html>.

---

• [Getting the tools](#Getting-the-tools)     
 • [Getting the source files](#Getting-the-source-files)     
 • [Building the core files](#Building-the-core-files)     
 • [Building the cairo devices files](#Building-the-cairo-devices-files)     
 • [Using ICU for collation](#Using-ICU-for-collation)     
 • [Support for libcurl](#Support-for-libcurl)     
 • [Checking the build](#Checking-the-build)     
 • [Building the manuals](#Building-the-manuals)     
 • [Building the Inno Setup installer](#Building-the-Inno-Setup-installer)     
 • [Building the MSI installer](#Building-the-MSI-installer)     
 • [64-bit Windows builds](#g_t64_002dbit-Windows-builds)

---

---

#### 3.1.1 Getting the tools

If you want to build R from the sources, you will first need to collect,
install and test an extensive set of tools. See [The Windows toolset](#The-Windows-toolset) (and perhaps updates in
<https://CRAN.R-project.org/bin/windows/Rtools/>) for details.

The `Rtools*.exe` executable installer described in [The
Windows toolset](#The-Windows-toolset) also includes some source files
in addition to the R source as noted below. You should run it first, to
obtain a working `tar` and other necessities. Choose a "Full
installation", and install the extra files into your intended R source
directory, e.g. `C:/R`. The directory name _should not contain
spaces_. We will call this directory `R_HOME` below.

---

#### 3.1.2 Getting the source files

You need to collect the following sets of files:

- Get the R source code tarball `R-3.6.3.tar.gz` from CRAN.
  Open a command window (or another shell) at directory
  `R_HOME`{.variable}, and run

```r
tar -xf R-3.6.3.tar.gz
```

to create the source tree in `R_HOME`{.variable}. **Beware**: do use
`tar` to extract the sources rather than tools such as WinZip. If
you are using an account with administrative privileges you may get
a lot of messages which can be suppressed by

```r
tar --no-same-owner -xf R-3.6.3.tar.gz
```

or perhaps better, set the environment
variable `TAR_OPTIONS` to the value
'`--no-same-owner --no-same-permissions`'.

It is also possible to obtain the source code using Subversion; see
[Obtaining R](#Obtaining-R) for details.

- If you are not using a tarball you need to obtain copies of the
  recommended packages from CRAN. Put the `.tar.gz` files in
  `R_HOME/src/library/Recommended` and run
  `make link-recommended`. If you have an Internet connection, you can
  do this automatically by running in `R_HOME/src/gnuwin32`

```r
make rsync-recommended
```

- The binary distributions of external software. Download

```r
https://www.stats.ox.ac.uk/pub/Rtools/goodies/multilib/local323.zip
```

(or a more recent version if appropriate), create an empty
directory, say `c:/R/extsoft`, and unpack it in that
directory by e.g.

```r
unzip local323.zip -d c:/R/extsoft
```

- Make a local copy of the configuration rules by

```r
cd R_HOME/src/gnuwin32
cp MkRules.dist MkRules.local
```

and edit `MkRules.local`, uncommenting `EXT_LIBS` and
setting it to the appropriate path (in our example
`c:/R/extsoft`).

Look through the file `MkRules.local` and make any other
changes needed: in particular, this is where a 64-bit build is
selected and the locations are set of external software for ICU
collation and the cairo-based devices.

The following additional item is normally installed by
`Rtools*.exe`. If instead you choose to do a completely manual
build you will also need

- The Tcl/Tk support files are contained in `Rtools*.exe`.
  Please make sure you install the right version: there is a 32-bit
  version and a 64-bit version. They should be installed to
  `R_HOME`, creating directory `Tcl` there.

---

#### 3.1.3 Building the core files

Set the environment variable `TMPDIR` to the absolute path to a writable
directory, with a path specified with forward slashes and no spaces.
(The default is `/tmp`, which may not be useful on Windows.)

You may need to compile under a case-honouring file system: we found
that a `samba`-mounted file system (which maps all file names to lower
case) did not work.

Open a command window at `R_HOME/src/gnuwin32`, then run

```r
make all recommended vignettes
```

and sit back and wait while the basic compile takes place.

Notes:

- We have had reports that earlier versions of anti-virus software
  locking up the machine, but not for several years. However,
  aggressive anti-virus checking such as the on-access scanning of
  Sophos can slow the build down several-fold.

- You can run a parallel make by e.g.

```r
make -j4 all
make -j4 recommended
make vignettes
```

but this is only likely to be worthwhile on a multi-core machine
with ample memory, and is not 100% reliable.

- It is possible (mainly for those working on R itself) to set the
  (make or environment) variable `R_NO_BASE_COMPILE` to a non-empty
  value, which inhibits the byte-compilation of the base and
  recommended packages.

---

#### 3.1.4 Building the cairo devices

The devices based on cairographics (`svg`, `cairo_pdf`, `cairo_ps` and
the `type = "cairo"` versions of `png`, `jpeg`, `tiff` and `bmp`) are
implemented in a separate DLL `winCairo.dll` which is loaded
when one of these devices is first used. It is not built by default, and
needs to be built (after `make all`) by `make cairodevices`.

To enable the building of these devices you need to install the static
cairographics libraries built by Simon Urbanek at
<https://www.rforge.net/Cairo/files/cairo-current-win.tar.gz>. Set the
macro '`CAIRO_HOME`' in `MkRules.local`. (Note that
this tarball unpacks with a top-level directory `src/`:
'`CAIRO_HOME`' needs to include that directory in its path.)

---

#### 3.1.5 Using ICU for collation

It is recommended to build R to support ICU (International Components
for Unicode, <http://site.icu-project.org/>) for collation, as is
commonly done on Unix-alikes.

Two settings are needed in `MkRules.local`,

```r
# set to use ICU
# USE_ICU = YES
# path to parent of ICU headers
ICU_PATH = /path/to/ICU
```

The first should be uncommented and the second set to the top-level
directory of a suitably packaged binary build of ICU, for example that
at <https://www.stats.ox.ac.uk/pub/Rtools/goodies/ICU_531.zip>.
Depending on the build, it may be necessary to edit the macro
`ICU_LIBS`.

Unlike on a Unix-alike, it is normally necessary to call `icuSetCollate`
to set a locale before ICU is actually used for collation, or set the
environment variable `R_ICU_LOCALE`.

---

#### 3.1.6 Support for libcurl

`libcurl` version 7.28.0 or later is used to support `curlGetHeaders`
and the `"libcurl"` methods of `download.file` and `url`.

A suitable distribution can be found _via_
<https://www.stats.ox.ac.uk/pub/Rtools/libs.html> and its unpacked
location should be specified in file `MkRules.local`.

For secure use of e.g. '`https://`' URLs Windows users may need
to specify the path to up-to-date _CA root certificates_: see
`?download.file`.

---

#### 3.1.7 Checking the build

You can test a build by running

```r
make check
```

The recommended packages can be checked by

```r
make check-recommended
```

Other levels of checking are

```r
make check-devel
```

for a more thorough check of the R functionality, and

```r
make check-all
```

for both `check-devel` and `check-recommended`.

If a test fails, there will almost always be a `.Rout.fail`
file in the directory being checked (often `tests/Examples` or
`tests`): examine the file to help pinpoint the problem.

Parallel checking of package sources (part of `make check-devel` and
`make check-recommended`) is possible: see the environment variable
`TEST_MC_CORES` to the maximum number of processes to be run in
parallel.

---

#### 3.1.8 Building the manuals

The PDF manuals require **texinfo** 5.1 or later, and can be made by

```r
make manuals
```

If you want to make the info versions (not including the Reference
Manual), use

```r
cd ../../doc/manual
make -f Makefile.win info
```

(all assuming you have `pdftex`/`pdflatex` installed and in your path).

See the [Making the manuals](#Making-the-manuals) section in the
Unix-alike section for setting options such as the paper size and the
fonts used.

By default it is assumed that **texinfo** is not installed, and the
manuals will not be built. The comments in file `MkRules.dist`
describe settings to build them. (Copy that file to
`MkRules.local` and edit it.) The **texinfo** 5.x package for
use on Windows is available at <https://www.stats.ox.ac.uk/pub/Rtools/>:
you will also need to install `Perl`[^19^](#FOOT19)

---

#### 3.1.9 Building the Inno Setup installer

You need to have the files for a complete R build, including bitmap and
Tcl/Tk support and the manuals (which requires **texinfo** installed),
as well as the recommended packages and Inno Setup (see [The Inno Setup installer](#The-Inno-Setup-installer)).

Once everything is set up

```r
make distribution
make check-all
```

will make all the pieces and the installer and put them in the
`gnuwin32/cran` subdirectory, then check the build. This works
by building all the parts in the sequence:

```r
rbuild (the executables, the FAQ docs etc.)
rpackages (the base packages)
htmldocs (the HTML documentation)
cairodevices (the cairo-based graphics devices)
recommended (the recommended packages)
vignettes (the vignettes in base packages:
       only needed if building from an svn checkout)
manuals (the PDF manuals)
rinstaller (the install program)
crandir (the CRAN distribution directory, only for 64-bit builds)
```

The parts can be made individually if a full build is not needed, but
earlier parts must be built before later ones. (The `Makefile`
doesn't enforce this dependency---some build targets force a lot of
computation even if all files are up to date.) The first four targets
are the default build if just `make` (or `make all`) is run.

Parallel make is not supported and likely to fail.

If you want to customize the installation by adding extra packages,
replace `make rinstaller` by something like

```r
make rinstaller EXTRA_PKGS='pkg1 pkg2 pkg3'
```

An alternative way to customize the installer starting with a binary
distribution is to first make an installation of R from the standard
installer, then add packages and make other customizations to that
installation. Then (after having customized file `MkRules`,
possibly _via_ `MkRules.local`, and having made R in the source
tree) in `src/gnuwin32/installer` run

```r
make myR IMAGEDIR=rootdir
```

where `rootdir` is the path to the root of the customized
installation (in double quotes if it contains spaces or backslashes).

Both methods create an executable with a standard name such as
`R-3.6.3-win.exe`, so please rename it to indicate that it is
customized. If you intend to _distribute_ a customized installer please
do check that license requirements are met -- note that the installer
will state that the contents are distributed under GPL and this has a
requirement for _you_ to supply the complete sources (including the R
sources even if you started with a binary distribution of R, and also
the sources of any extra packages (including their external software)
which are included).

The defaults for the startup parameters may also be customized. For
example

```r
make myR IMAGEDIR=rootdir MDISDI=1
```

will create an installer that defaults to installing R to run in SDI
mode. See `src/gnuwin32/installer/Makefile` for the names and
values that can be set.

The standard CRAN distribution of a 32/64-bit installer is made by first
building 32-bit R (just

```r
make 32-bit
```

is needed), and then (in a separate directory) building 64-bit R with
the macro `HOME32` set in file `MkRules.local` to the top-level
directory of the 32-bit build. Then the `make rinstaller` step copies
the files that differ between architectures from the 32-bit build as it
builds the installer image.

---

#### 3.1.10 Building the MSI installer

It is also possible to build an installer for use with Microsoft
Installer. This is intended for use by sysadmins doing automated
installs, and is not recommended for casual use.

It makes use of the Windows Installer XML (WiX) toolkit _version 3.5_
(or perhaps later, untested) available from <http://wixtoolset.org/>.
Once WiX is installed, set the path to its home directory in
`MkRules.local`.

You need to have the files for a complete R build, including bitmap and
Tcl/Tk support and the manuals, as well as the recommended packages.
There is no option in the installer to customize startup options, so
edit `etc/Rconsole` and `etc/Rprofile.site` to set
these as required. Then

```r
cd installer
make msi
```

which will result in a file with a name like
`R-3.6.3-win32.msi`. This can be double-clicked to be
installed, but those who need it will know what to do with it (usually
by running `msiexec /i` with additional options). Properties that users
might want to set from the `msiexec` command line include
'`ALLUSERS`', '`INSTALLDIR`' (something like
`c:\Program Files\R\R-3.6.3`) and '`RMENU`' (the path
to the '`R`' folder on the start menu) and
'`STARTDIR`' (the starting directory for R shortcuts,
defaulting to something like `c:\Users\name\Documents\R`).

The MSI installer can be built both from a 32-bit build of R
(`R-3.6.3-win32.msi`) and from a 64-bit build of R
(`R-3.6.3-win64.msi`, optionally including 32-bit files by
setting the macro `HOME32`, when the name is
`R-3.6.3-win.msi`). Unlike the main installer, a 64-bit MSI
installer can only be run on 64-bit Windows.

Thanks to David del Campo (Dept of Statistics, University of Oxford) for
suggesting WiX and building a prototype installer.

---

#### 3.1.11 64-bit Windows builds

To build a 64-bit version of R you need a 64-bit toolchain: the only one
discussed here is based on the work of the MinGW-w64 project
(<http://sourceforge.net/projects/mingw-w64/>, but commercial compilers
such as those from Intel and PGI could be used (and have been by R
redistributors).

Support for MinGW-w64 was developed in the R sources over the period
2008--10 and was first released as part of R 2.11.0. The assistance of
Yu Gong at a crucial step in porting R to MinGW-w64 is gratefully
acknowledged, as well as help from Kai Tietz, the lead developer of the
MinGW-w64 project.

Windows 64-bit is now completely integrated into the R and package build
systems: a 64-bit build is selected in file `MkRules.local`.

---

### 3.2 Testing an Installation

The Windows installer contains a set of test files used when building R.

The `Rtools` are not needed to run these tests, but more comprehensive
analysis of errors will be given if `diff` is in the path (and
`errorsAreFatal = FALSE` is then not needed below).

Launch either `Rgui` or `Rterm`, preferably with `--vanilla`.
Then run

```r
Sys.setenv(LC_COLLATE = "C", LANGUAGE = "en")
library("tools")
testInstalledBasic("both")
testInstalledPackages(scope = "base", errorsAreFatal = FALSE)
testInstalledPackages(scope = "recommended", errorsAreFatal = FALSE)
```

runs the basic tests and then all the tests on the standard and
recommended packages. These tests can be run from anywhere: they write
some of their results in the `tests` folder of the R home
directory (as given by `R.home()`), and hence may need to be run under
the account used to install R.

The results of `example(md5sums)` when testing **tools** will differ
from the reference output as some files are installed with Windows' CRLF
line endings.

---
