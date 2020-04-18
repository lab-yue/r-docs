8 Tools

---

The behavior of `R CMD check` can be controlled through a variety of
command line arguments and environment variables.

There is an internal `--install=value` command line argument
not shown by `R CMD check --help`, with possible values

`check:file`

: Assume that installation was already performed with stdout/stderr to
`file`{.variable}, the contents of which need to be checked (without
repeating the installation). This is useful for checks applied by
repository maintainers: it reduces the check time by the
installation time given that the package has already been installed.
In this case, one also needs to specify _where_ the package was
installed to using command line option `--library`.

`fake`

: Fake installation, and turn off the run-time tests.

`skip`

: Skip installation, e.g., when testing recommended packages bundled
with R.

`no`

: The same as `--no-install` : turns off installation and the
tests which require the package to be installed.

The following environment variables can be used to customize the
operation of `check`: a convenient place to set these is the check
environment file (default, `~/.R/check.Renviron`).

`_R_CHECK_ALL_NON_ISO_C_`

: If true, do not ignore compiler (typically GCC) warnings about non
ISO C code in _system_ headers. Note that this may also show
additional ISO C++ warnings. Default: false.

`_R_CHECK_FORCE_SUGGESTS_`

: If true, give an error if suggested packages are not available.
Default: true (but false for CRAN submission checks).

`_R_CHECK_RD_CONTENTS_`

: If true, check `Rd` files for auto-generated content which
needs editing, and missing argument documentation. Default: true.

`_R_CHECK_RD_LINE_WIDTHS_`

: If true, check `Rd` line widths in usage and examples
sections. Default: false (but true for CRAN submission checks).

`_R_CHECK_RD_STYLE_`

: If true, check whether `Rd` usage entries for S3 methods
use the full function name rather than the appropriate `\method`
markup. Default: true.

`_R_CHECK_RD_XREFS_`

: If true, check the cross-references in `.Rd` files.
Default: true.

`_R_CHECK_SUBDIRS_NOCASE_`

: If true, check the case of directories such as `R` and
`man`. Default: true.

`_R_CHECK_SUBDIRS_STRICT_`

: Initial setting for `--check-subdirs`. Default:
'`default`' (which checks only tarballs, and checks in the
`src` only if there is no `configure` file).

`_R_CHECK_USE_CODETOOLS_`

: If true, make use of the
[**codetools**](https://CRAN.R-project.org/package=codetools)
package, which provides a detailed analysis of visibility of objects
(but may give false positives). Default: true (if recommended
packages are installed).

`_R_CHECK_USE_INSTALL_LOG_`

: If true, record the output from installing a package as part of its
check to a log file (`00install.out` by default), even when
running interactively. Default: true.

`_R_CHECK_VIGNETTES_NLINES_`

: Maximum number of lines to show from the bottom of the output when
reporting errors in running or re-building vignettes. ( Value `0`
means all lines will be shown.) Default: 10 for running, 25 for
re-building.

`_R_CHECK_CODOC_S4_METHODS_`

: Control whether `codoc()` testing is also performed on S4 methods.
Default: true.

`_R_CHECK_DOT_INTERNAL_`

: Control whether the package code is scanned for `.Internal` calls,
which should only be used by base (and occasionally by recommended)
packages. Default: true.

`_R_CHECK_EXECUTABLES_`

: Control checking for executable (binary) files. Default: true.

`_R_CHECK_EXECUTABLES_EXCLUSIONS_`

: Control whether checking for executable (binary) files ignores files
listed in the package's `BinaryFiles` file. Default: true
(but false for CRAN submission checks). However, most likely this
package-level override mechanism will be removed eventually.

`_R_CHECK_PERMISSIONS_`

: Control whether permissions of files should be checked. Default:
true iff `.Platform$OS.type == "unix"`.

`_R_CHECK_FF_CALLS_`

: Allows turning off `checkFF()` testing. If set to
'`registration`', checks the registration information
(number of arguments, correct choice of
`.C/.Fortran/.Call/.External`) for such calls provided the package
is installed. Default: true.

`_R_CHECK_FF_DUP_`

: Controls `checkFF(check_DUP)` Default: true (and forced to be true
for CRAN submission checks).

`_R_CHECK_LICENSE_`

: Control whether/how license checks are performed. A possible value
is '`maybe`' (warn in case of problems, but not about
standardizable non-standard license specs). Default: true.

`_R_CHECK_RD_EXAMPLES_T_AND_F_`

: Control whether `check_T_and_F()` also looks for "bad" (global)
'`T`'/'`F`' uses in examples. Off by default
because this can result in false positives.

`_R_CHECK_RD_CHECKRD_MINLEVEL_`

: Controls the minimum level for reporting warnings from `checkRd`.
Default: -1.

`_R_CHECK_XREFS_REPOSITORIES_`

: If set to a non-empty value, a space-separated list of repositories
to use to determine known packages. Default: empty, when the CRAN
and Bioconductor repositories known to R is used.

`_R_CHECK_SRC_MINUS_W_IMPLICIT_`

: Control whether installation output is checked for compilation
warnings about implicit function declarations (as spotted by GCC
with command line option `-Wimplicit-function-declaration`,
which is implied by `-Wall`). Default: false.

`_R_CHECK_SRC_MINUS_W_UNUSED_`

: Control whether installation output is checked for compilation
warnings about unused code constituents (as spotted by GCC with
command line option `-Wunused`, which is implied by
`-Wall`). Default: true.

`_R_CHECK_WALL_FORTRAN_`

: Control whether gfortran 4.0 or later `-Wall` warnings are
used in the analysis of installation output. Default: false, even
though the warnings are justifiable.

`_R_CHECK_ASCII_CODE_`

: If true, check R code for non-ascii characters. Default: true.

`_R_CHECK_ASCII_DATA_`

: If true, check data for non-ascii characters. _En route_, checks
that all the datasets can be loaded and that their components can be
accessed. Default: true.

`_R_CHECK_COMPACT_DATA_`

: If true, check data for ascii and uncompressed saves, and also check
if using `bzip2` or `xz` compression would be significantly better.
Default: true.

`_R_CHECK_SKIP_ARCH_`

: Comma-separated list of architectures that will be omitted from
checking in a multi-arch setup. Default: none.

`_R_CHECK_SKIP_TESTS_ARCH_`

: Comma-separated list of architectures that will be omitted from
running tests in a multi-arch setup. Default: none.

`_R_CHECK_SKIP_EXAMPLES_ARCH_`

: Comma-separated list of architectures that will be omitted from
running examples in a multi-arch setup. Default: none.

`_R_CHECK_VC_DIRS_`

: Should the unpacked package directory be checked for version-control
directories (`CVS`, `.svn` ...)? Default: true for
tarballs.

`_R_CHECK_PKG_SIZES_`

: Should `du` be used to find the installed sizes of packages?
`R CMD check` does check for the availability of `du`. but this
option allows the check to be overruled if an unsuitable command is
found (including one that does not respect the `-k` flag to
report in units of 1Kb, or reports in a different format -- the GNU,
macOS and Solaris `du` commands have been tested). Default: true if
`du` is found.

`_R_CHECK_PKG_SIZES_THRESHOLD_`

: Threshold used for `_R_CHECK_PKG_SIZES_` (in Mb). Default: 5

`_R_CHECK_DOC_SIZES_`

: Should `qpdf` be used to check the installed sizes of PDFs? Default:
true if `qpdf` is found.

`_R_CHECK_DOC_SIZES2_`

: Should `gs` be used to check the installed sizes of PDFs? This is
slower than (and in addition to) the previous check, but does detect
figures with excessive detail (often hidden by over-plotting) or
bitmap figures with too high a resolution. Requires that `R_GSCMD`
is set to a valid program, or `gs` (or on Windows, `gswin32.exe` or
`gswin64c.exe`) is on the path. Default: false (but true for CRAN
submission checks).

`_R_CHECK_ALWAYS_LOG_VIGNETTE_OUTPUT_`

: By default the output from running the R code in the vignettes is
kept only if there is an error. This also applies to the
`build_vignettes.log` log from the re-building of
vignettes. Default: false.

`_R_CHECK_CLEAN_VIGN_TEST_`

: Should the `vign_test` directory be removed if the test is
successful? Default: true.

`_R_CHECK_REPLACING_IMPORTS_`

: Should warnings about replacing imports be reported? These sometimes
come from auto-generated `NAMESPACE` files in other
packages, but most often from importing the whole of a namespace
rather than using `importFrom`. Default: true.

`_R_CHECK_UNSAFE_CALLS_`

: Check for calls that appear to tamper with (or allow tampering with)
already loaded code not from the current package: such calls may
well contravene CRAN policies. Default: true.

`_R_CHECK_TIMINGS_`

: Optionally report timings for installation, examples, tests and
running/re-building vignettes as part of the check log. The format
is '`[as/bs]`' for the total CPU time (including child
processes) '`a`' and elapsed time '`b`', except on
Windows, when it is '`[bs]`'. In most cases timings are
only given for '`OK`' checks. Times with an elapsed
component over 10 mins are reported in minutes (with abbreviation
'`m`'). The value is the smallest numerical value in
elapsed seconds that should be reported: non-numerical values
indicate that no report is required, a value of '`0`' that
a report is always required. Default: `""`. (`10` for CRAN checks.)

`_R_CHECK_EXAMPLE_TIMING_THRESHOLD_`

: If timings are being recorded, set the threshold in seconds for
reporting long-running examples (either user+system CPU time or
elapsed time). Default: `"5"`.

`_R_CHECK_EXAMPLE_TIMING_CPU_TO_ELAPSED_THRESHOLD_`

: For checks with timings enabled, report examples where the ratio of
CPU time to elapsed time exceeds this threshold (and the CPU time is
at least one second). This can help detect the simultaneous use of
multiple CPU cores. Default: `NA`.

`_R_CHECK_TEST_TIMING_CPU_TO_ELAPSED_THRESHOLD_`

: Report for running an individual test if the ratio of CPU time to
elapsed time exceeds this threshold (and the CPU time is at least
one second). Not supported on Windows. Default: `NA`.

`_R_CHECK_VIGNETTE_TIMING_CPU_TO_ELAPSED_THRESHOLD_`

: Report if when running/re-building vignettes (individually or in
aggregate) the ratio of CPU time to elapsed time exceeds this
threshold (and the CPU time is at least one second). Not supported
on Windows. Default: `NA`.

`_R_CHECK_INSTALL_DEPENDS_`

: If set to a true value and a test installation is to be done, this
is done with `.libPaths()` containing just a temporary library
directory and `.Library`. The temporary library is populated by
symbolic links[^22^](#FOOT22) to the installed copies of
all the Depends/Imports/LinkingTo packages which are not in
`.Library`. Default: false (but true for CRAN submission checks).

    Note that this is actually implemented in `R CMD INSTALL`, so it is
    available to those who first install recording to a log, then call
    `R CMD check`.

`_R_CHECK_DEPENDS_ONLY_` \
`\_R_CHECK_SUGGESTS_ONLY_`

: If set to a true value, running examples, tests and vignettes is
done with `.libPaths()` containing just a temporary library
directory and `.Library`. The temporary library is populated by
symbolic links[^23^](#FOOT23) to the installed copies of
all the Depends/Imports and (for the second only) Suggests packages
which are not in `.Library`. (As exceptions, packages in a
'`VignetteBuilder`' field and test-suite managers in
'`Suggests`' are always made available.) Default: false
(but `_R_CHECK_SUGGESTS_ONLY_` is true for CRAN submission checks:
some of the regular checks use true and some use false).

`_R_CHECK_NO_RECOMMENDED_`

: If set to a true value, augment the previous checks to make
recommended packages unavailable unless declared. Default: false
(but true for CRAN submission checks).

    This may give false positives on code which uses
    `grDevices::densCols` and `stats:::asSparse` as these invoke
    [**KernSmooth**](https://CRAN.R-project.org/package=KernSmooth) and
    [**Matrix**](https://CRAN.R-project.org/package=Matrix)
    respectively.

`_R_CHECK_CODETOOLS_PROFILE_`

: A string with comma-separated `name=value` pairs (with
`value`{.variable} a logical constant) giving additional arguments
for the
[**codetools**](https://CRAN.R-project.org/package=codetools)
functions used for analyzing package code. E.g., use
`_R_CHECK_CODETOOLS_PROFILE_="suppressLocalUnused=FALSE"` to turn
off suppressing warnings about unused local variables. Default: no
additional arguments, corresponding to using `skipWith = TRUE`,
`suppressPartialMatchArgs = FALSE` and `suppressLocalUnused = TRUE`.

`_R_CHECK_CRAN_INCOMING_`

: Check whether package is suitable for publication on CRAN. Default:
false, except for CRAN submission checks.

`_R_CHECK_CRAN_INCOMING_REMOTE_`

: Include checks that require remote access among the above. Default:
same as `_R_CHECK_CRAN_INCOMING_`

`_R_CHECK_XREFS_USE_ALIASES_FROM_CRAN_`

: When checking anchored Rd xrefs, use Rd aliases from the CRAN
package web areas in addition to those in the packages installed
locally. Default: false.

`_R_SHLIB_BUILD_OBJECTS_SYMBOL_TABLES_`

: Make the checks of compiled code more accurate by recording the
symbol tables for objects (`.o` files) at installation in a
file `symbols.rds`. (Only currently supported on Linux,
Solaris, macOS, Windows and FreeBSD.) Default: true.

`_R_CHECK_CODE_ASSIGN_TO_GLOBALENV_`

: Should the package code be checked for assignments to the global
environment? Default: false (but true for CRAN submission checks).

`_R_CHECK_CODE_ATTACH_`

: Should the package code be checked for calls to `attach()`? Default:
false (but true for CRAN submission checks).

`_R_CHECK_CODE_DATA_INTO_GLOBALENV_`

: Should the package code be checked for calls to `data()` which load
into the global environment? Default: false (but true for CRAN
submission checks).

`_R_CHECK_DOT_FIRSTLIB_`

: Should the package code be checked for the presence of the obsolete
function `.First.lib()`? Default: false (but true for CRAN
submission checks).

`_R_CHECK_DEPRECATED_DEFUNCT_`

: Should the package code be checked for the presence of recently
deprecated or defunct functions (including completely removed
functions). Also for platform-specific graphics devices. Default:
false (but true for CRAN submission checks).

`_R_CHECK_SCREEN_DEVICE_`

: If set to '`warn`', give a warning if examples etc open a
screen device. If set to '`stop`', give an error. Default:
empty (but '`stop`' for CRAN submission checks).

`_R_CHECK_WINDOWS_DEVICE_`

: If set to '`stop`', give an error if a Windows-only device
is used in example etc. This is only useful on Windows: the devices
do not exist elsewhere. Default: empty (but '`stop`' for
CRAN submission checks on Windows).

`_R_CHECK_TOPLEVEL_FILES_`

: Report on top-level files in the package sources that are not
described in 'Writing R Extensions' nor are commonly understood
(like `ChangeLog`). Variations on standard names (e.g.
`COPYRIGHT`) are also reported. Default: false (but true
for CRAN submission checks).

`_R_CHECK_GCT_N_`

: Should the `--use-gct` use `gctorture2(n)` rather than
`gctorture(TRUE)`? Use a positive integer to enable this. Default:
`0`.

`_R_CHECK_LIMIT_CORES_`

: If set, check the usage of too many cores in package **parallel**.
If set to '`warn`' gives a warning, to '`false`'
or '`FALSE`' the check is skipped, and any other non-empty
value gives an error when more than 2 children are spawned. Default:
unset (but '`TRUE`' for CRAN submission checks).

`_R_CHECK_CODE_USAGE_VIA_NAMESPACES_`

: If set, check code usage (via
[**codetools**](https://CRAN.R-project.org/package=codetools))
directly on the package namespace without loading and attaching the
package and its suggests and enhances. Default: true (and true for
CRAN submission checks).

`_R_CHECK_CODE_USAGE_WITH_ONLY_BASE_ATTACHED_`

: If set, check code usage (via
[**codetools**](https://CRAN.R-project.org/package=codetools)) with
only the base package attached. Default: true.

`_R_CHECK_EXIT_ON_FIRST_ERROR_`

: If set to a true value, the check will exit on the first error.
Default: false.

`_R_CHECK_S3_METHODS_NOT_REGISTERED_`

: If set to a true value, report (apparent) S3 methods exported but
not registered. Default: true.

`_R_CHECK_OVERWRITE_REGISTERED_S3_METHODS_`

: If set to a true value, report already registered S3 methods in
base/recommended packages which are overwritten when this package's
namespace is loaded. Default: false (but true for CRAN submission
checks).

`_R_CHECK_TESTS_NLINES_`

: Number of trailing lines of test output to reproduce in the log. If
`0` all lines except the R preamble are reproduced. Default: 13.

`_R_CHECK_NATIVE_ROUTINE_REGISTRATION_`

: If set to a true value, report if the entry points to register
native routines and to suppress dynamic search are not found in a
package's DLL. (**NB:** this requires system command `nm` to be on
the `PATH`. On Windows, `objdump.exe` is first searched for in
compiler toolchain specified via `Makeconf` (can be customized by
environment variable `BINPREF`). If not found there, it must be on
the `PATH`. On Unix this would be normal when using a package with
compiled code (which are the only ones this checks), but Windows'
users should check.) Default: false (but true for CRAN submission
checks).

`_R_CHECK_NO_STOP_ON_TEST_ERROR_`

: If set to a true value, do not stop running tests after first error
(as if command line option `--no-stop-on-test-error` had
been given). Default: false (but true for CRAN submission checks).

`_R_CHECK_PRAGMAS_`

: Run additional checks on the pragmas in C/C++ source code and
headers. Default: false (but true for CRAN submission checks).

`_R_CHECK_COMPILATION_FLAGS_`

: If the package is installed and has C/C++/Fortran code, check the
install log for non-portable flags (for example those added to
`src/Makevars` during configuration). Currently
`-W` flags are reported, except `-Wall`,
`-Wextra` and `-Weverything`, and flags which
appear to be attempts to suppress warnings are highlighted. See
[Writing portable packages](./R-exts.html#Writing-portable-packages)
in Writing R Extensions for the rationale of this check (and why
even `-Werror` is unsafe). Environment variable
`_R_CHECK_COMPILATION_FLAGS_KNOWN_` can be set to a space-separated
set of flags which come from the R build used for testing (flags
such as `-Wall` and `-Wextra` are already known).
Default: false (but true for CRAN submission checks).

`_R_CHECK_R_DEPENDS_`

: Check that any dependence on R is not on a recent patch-level
version such as `R (>= 3.3.3)` since blocking installation of a
package will also block its reverse dependencies. Possible values
'`"note"`', '`"warn"`' and logical values (where
currently true values are equivalent to '`"note"`').
Default: false (but '`"warn"`' for `--as-cran`).

`_R_CHECK_SERIALIZATION_`

: Check that serialized R objects in the package sources were
serialized with version 2 and there is no dependence on
'`R >= 3.5.0`'. (Version 3 is in use as from R 3.5.0 but
should only be used when necessary.) Default: false (but true for
CRAN submission checks).

`_R_CHECK_R_ON_PATH_`

: This checks if the package attempts to use `R` or `Rscript` from the
path rather than that under test. It does so by putting scripts at
the head of the path which print a message and fail. Default: false
(but true for CRAN submission checks).

`_R_CHECK_PACKAGES_USED_IN_TESTS_USE_SUBDIRS_`

: If set to a true value, also check the R code in common unit test
subdirectories of `tests` for undeclared package
dependencies. Default: false (but true for CRAN submission checks).

`_R_CHECK_SHLIB_OPENMP_FLAGS_`

: Check correct and portable use of `SHLIB_OPENMP_*FLAGS` in
`src/Makevars` (and similar). Default: false (but true for
CRAN submission checks).

`_R_CHECK_CONNECTIONS_LEFT_OPEN_`

: When checking examples, check for each example if connections are
left open: if any are found, this is reported with a fatal error.
NB: 'connections' includes most use of files and any parallel
clusters which have not be stopped by `stopCluster()`. Default:
false (but true for CRAN submission checks).

`_R_CHECK_FUTURE_FILE_TIMESTAMPS_`

: Check if any of the input files has a timestamp in the future (and
to do so, checks that the system clock is correct to within 5
minutes). Default: false (but true for CRAN submission checks).

`_R_CHECK_LENGTH_1_CONDITION_`

: Optionally check if the condition in `if` and `while` statements has
length greater than one. For a true value ('`T`',
'`True`', '`TRUE`' or '`true`'), give an
error. For a false value ('`F`', '`False`',
'`FALSE`' or '`false`') or when unset, print a
warning. Any other non-true non-empty value needs to be a list of
commands separated by comma: '`abort`' causes R to
terminate unconditionally instead of signalling an error,
'`verbose`' prints very detailed diagnostic message,
'`package:pkg`' restricts the check to if/while statements
executing in the namespace of package '`pkg`',
'`package:_R_CHECK_PACKAGE_NAME_`' restricts the check to
if/while statements executing in the package that is currently being
checked by `R CMD check`, '`warn`' causes R to report a
warning instead of signalling an error. Default: unset (warning is
reported)

`_R_CHECK_LENGTH_1_LOGIC2_`

: Optionally check if either argument of the binary operators `&&` and
`||` has length greater than one. The format is the same as for
\_R*CHECK_LENGTH_1_CONDITION\_. Default: unset (nothing is
reported, but
'`package:\_R_CHECK_PACKAGE_NAME*,abort,verbose`' for the
CRAN submission checks).

`_R_CHECK_BUILD_VIGNETTES_SEPARATELY_`

: Prior to R 3.6.0, re-building the vignette outputs was done in a
single R session which allowed accidental reliance of one vignette
on another (for example, in the loading of packages). The current
default is to use a separate session for each vignette; this option
allows testing the older behaviour, Default: true

`_R_CHECK_SYSTEM_CLOCK_`

: As part of the 'checking for future file timestamps' enabled by
`--as-cran`, check the system clock against an external
clock to catch errors such as the wrong day or even year. Not
necessary on systems doing repeated checks. Default: true (but false
for CRAN checking)

`_R_CHECK_AUTOCONF_`

: For packages with a `configure` file generated by GNU
`autoconf` and either `configure.ac` or
`configure,.in`, check that `autoreconf` can, if available,
be run in a copy of the sources (this will detect missing source
files and report `autoconf` warnings). Default: false (but true for
CRAN submission checks).

`_R_CHECK_THINGS_IN_TEMP_DIR_`

: Check and report at the end of the check run if files would have
been left in the temporary directory (usually `/tmp` on a
Unix-alike). It does this by setting the environment variable
`TEMPDIR` to a subdirectory of the R session directory for the
`check` process: if any files or directories are left there they are
removed. Since some of these might be out of the user's control,
environment variable `_R_CHECK_THINGS_IN_TEMP_DIR_EXCLUDE_` can
specify an (extended regex) pattern of file names not to be reported
-- CRAN uses '`^ompi.`' for directories left behind by
OpenMPI. There are rare instances where `TEMPDIR` is not respected
and so files are left in `/tmp` (and not reported): one
example is `/tmp/boost_interprocess` on some OSes. Default:
false (but true for CRAN submission checks).

CRAN's submission checks use something like

```r
_R_CHECK_CRAN_INCOMING_=TRUE
_R_CHECK_CRAN_INCOMING_REMOTE_=TRUE
_R_CHECK_VC_DIRS_=TRUE
_R_CHECK_TIMINGS_=10
_R_CHECK_INSTALL_DEPENDS_=TRUE
_R_CHECK_SUGGESTS_ONLY_=TRUE
_R_CHECK_NO_RECOMMENDED_=TRUE
_R_CHECK_EXECUTABLES_EXCLUSIONS_=FALSE
_R_CHECK_DOC_SIZES2_=TRUE
_R_CHECK_CODE_ASSIGN_TO_GLOBALENV_=TRUE
_R_CHECK_CODE_ATTACH_=TRUE
_R_CHECK_CODE_DATA_INTO_GLOBALENV_=TRUE
_R_CHECK_CODE_USAGE_VIA_NAMESPACES_=TRUE
_R_CHECK_DOT_FIRSTLIB_=TRUE
_R_CHECK_DEPRECATED_DEFUNCT_=TRUE
_R_CHECK_REPLACING_IMPORTS_=TRUE
_R_CHECK_SCREEN_DEVICE_=stop
_R_CHECK_TOPLEVEL_FILES_=TRUE
_R_CHECK_S3_METHODS_NOT_REGISTERED_=TRUE
_R_CHECK_OVERWRITE_REGISTERED_S3_METHODS_=TRUE
_R_CHECK_PRAGMAS_=TRUE
_R_CHECK_COMPILATION_FLAGS_=TRUE
_R_CHECK_R_DEPENDS_=warn
_R_CHECK_SERIALIZATION_=TRUE
_R_CHECK_R_ON_PATH_=TRUE
_R_CHECK_PACKAGES_USED_IN_TESTS_USE_SUBDIRS_=TRUE
_R_CHECK_SHLIB_OPENMP_FLAGS_=TRUE
_R_CHECK_CONNECTIONS_LEFT_OPEN_=TRUE
_R_CHECK_FUTURE_FILE_TIMESTAMPS_=TRUE
_R_CHECK_LENGTH_1_LOGIC2_=package:_R_CHECK_PACKAGE_NAME_,abort,verbose
_R_CHECK_AUTOCONF_=true
_R_CHECK_THINGS_IN_TEMP_DIR_=true
```

These are turned on by `R CMD check --as-cran`: the incoming checks also
use

```r
_R_CHECK_FORCE_SUGGESTS_=FALSE
```

since some packages do suggest other packages not available on CRAN or
other commonly-used repositories.

Several environment variables can be used to set 'timeouts': limits for
the elapsed time taken by the sub-processes used for parts of the
checks. A value of `0` indicates no limit, and is the default. Character
strings ending in '`s`', '`m`' or '`h`'
indicate a number of seconds, minutes or hours respectively: other
values are interpreted as a whole number of seconds (with invalid inputs
being treated as no limit).

`_R_CHECK_ELAPSED_TIMEOUT_`

: The default timeout for sub-processes not otherwise mentioned, and
the default value for all except
`_R_CHECK_ONE_TEST_ELAPSED_TIMEOUT_`. (This is also used by
`tools::check_packages_in_dir`.)

`_R_CHECK_INSTALL_ELAPSED_TIMEOUT_`

: Limit for when `R CMD INSTALL` is run by `check`.

`_R_CHECK_EXAMPLES_ELAPSED_TIMEOUT_`

: Limit for running all the examples for one sub-architecture.

`_R_CHECK_ONE_TEST_ELAPSED_TIMEOUT_`

: Limit for running one test for one sub-architecture. Default
`_R_CHECK_TESTS_ELAPSED_TIMEOUT_`.

`_R_CHECK_TESTS_ELAPSED_TIMEOUT_`

: Limit for running all the tests for one sub-architecture (and the
default limit for running one test).

`_R_CHECK_ONE_VIGNETTE_ELAPSED_TIMEOUT_`

: Limit for running the R code in one vignette, including for
re-building each vignette separately.

`_R_CHECK_BUILD_VIGNETTES_ELAPSED_TIMEOUT_`

: Limit for re-building all vignettes.

`_R_CHECK_PKGMAN_ELAPSED_TIMEOUT_`

: Limit for each attempt at building the PDF package manual.

Another variable which enables stricter checks is to set
`R_CHECK_CONSTANTS` to `5`. This checks that
nothing[^24^](#FOOT24) changes the values of
'constants'[^25^](#FOOT25) in R code. This is best used in
conjunction with setting `R_JIT_STRATEGY` to `3`, which checks code on
first use (by default most code is only checked after byte-compilation
on second use). Unfortunately these checks slow down checking of
examples, tests and vignettes, typically two-fold but in the worst cases
at least a hundred-fold.

---
