14 OS facilities

---

R has quite extensive facilities to access the OS under which it is
running: this allows it to be used as a scripting language and that
ability is much used by R itself, for example to install packages.

Because R's own scripts need to work across all platforms, considerable
effort has gone into make the scripting facilities as
platform-independent as is feasible.

---

• [Files and directories](#Files-and-directories)     
 • [Filepaths](#Filepaths)     
 • [System commands](#System-commands)     
 • [Compression and Archives](#Compression-and-Archives)

---

---

### 14.1 Files and directories

There are many functions to manipulate files and directories. Here are
pointers to some of the more commonly used ones.

To create an (empty) file or directory, use `file.create` or
`dir.create`. (These are the analogues of the POSIX utilities `touch`
and `mkdir`.) For temporary files and directories in the R session
directory see `tempfile`.

Files can be removed by either `file.remove` or `unlink`: the latter can
remove directory trees.

For directory listings use `list.files` (also available as `dir`) or
`list.dirs`. These can select files using a regular expression: to
select by wildcards use `Sys.glob`.

Many types of information on a filepath (including for example if it is
a file or directory) can be found by `file.info`.

There are several ways to find out if a file 'exists' (a file can exist
on the filesystem and not be visible to the current user). There are
functions `file.exists`, `file.access` and `file_test` with various
versions of this test: `file_test` is a version of the POSIX `test`
command for those familiar with shell scripting.

Function `file.copy` is the R analogue of the POSIX command `cp`.

Choosing files can be done interactively by `file.choose`: the Windows
port has the more versatile functions `choose.files` and `choose.dir`
and there are similar functions in the **tcltk** package:
`tk_choose.files` and `tk_choose.dir`.

Functions `file.show` and `file.edit` will display and edit one or more
files in a way appropriate to the R port, using the facilities of a
console (such as RGui on Windows or R.app on macOS) if one is in use.

There is some support for _links_ in the filesystem: see functions
`file.link` and `Sys.readlink`.

---

### 14.2 Filepaths

With a few exceptions, R relies on the underlying OS functions to
manipulate filepaths. Some aspects of this are allowed to depend on the
OS, and do, even down to the version of the OS. There are POSIX
standards for how OSes should interpret filepaths and many R users
assume POSIX compliance: but Windows does not claim to be compliant and
other OSes may be less than completely compliant.

The following are some issues which have been encountered with
filepaths.

- POSIX filesystems are case-sensitive, so `foo.png` and
  `Foo.PNG` are different files. However, the defaults on
  Windows and macOS are to be case-insensitive, and FAT filesystems
  (commonly used on removable storage) are not normally case-sensitive
  (and all filepaths may be mapped to lower case).
- Almost all the Windows' OS services support the use of slash or
  backslash as the filepath separator, and R converts the known
  exceptions to the form required by Windows.
- The behaviour of filepaths with a trailing slash is OS-dependent.
  Such paths are not valid on Windows and should not be expected to
  work. POSIX-2008 requires such paths to match only directories, but
  earlier versions allowed them to also match files. So they are best
  avoided.
- Multiple slashes in filepaths such as `/abc//def` are valid
  on POSIX filesystems and treated as if there was only one slash.
  They are _usually_ accepted by Windows' OS functions. However,
  leading double slashes may have a different meaning.
- Windows' UNC filepaths (such as `\\server\dir1\dir2\file`
  and `\\?\UNC\server\dir1\dir2\file`) are not supported, but
  they may work in some R functions. POSIX filesystems are allowed to
  treat a leading double slash specially.
- Windows allows filepaths containing drives and relative to the
  current directory on a drive, e.g. `d:foo/bar` refers to
  `d:/a/b/c/foo/bar` if the current directory _on drive
  `d:`_ is `/a/b/c`. It is intended that these work,
  but the use of absolute paths is safer.

Functions `basename` and `dirname` select parts of a file path: the
recommended way to assemble a file path from components is `file.path`.
Function `pathexpand` does 'tilde expansion', substituting values for
home directories (the current user's, and perhaps those of other users).

On filesystems with links, a single file can be referred to by many
filepaths. Function `normalizePath` will find a canonical filepath.

Windows has the concepts of short ('8.3') and long file names:
`normalizePath` will return an absolute path using long file names and
`shortPathName` will return a version using short names. The latter does
not contain spaces and uses backslash as the separator, so is sometimes
useful for exporting names from R.

File _permissions_ are a related topic. R has support for the POSIX
concepts of read/write/execute permission for owner/group/all but this
may be only partially supported on the filesystem, so for example on
Windows only read-only files (for the account running the R session) are
recognized. Access Control Lists (ACLs) are employed on several
filesystems, but do not have an agreed standard and R has no facilities
to control them. Use `Sys.chmod` to change permissions.

---

### 14.3 System commands

Functions `system` and `system2` are used to invoke a system command and
optionally collect its output. `system2` is a little more general but
its main advantage is that it is easier to write cross-platform code
using it.

`system` behaves differently on Windows from other OSes (because the API
C call of that name does). Elsewhere it invokes a shell to run the
command: the Windows port of R has a function `shell` to do that.

To find out if the OS includes a command, use `Sys.which`, which
attempts to do this in a cross-platform way (unfortunately it is not a
standard OS service).

Function `shQuote` will quote filepaths as needed for commands in the
current OS.

---

### 14.4 Compression and Archives

Recent versions of R have extensive facilities to read and write
compressed files, often transparently. Reading of files in R is to a vey
large extent done by _connections_, and the `file` function which is
used to open a connection to a file (or a URL) and is able to identify
the compression used from the 'magic' header of the file.

The type of compression which has been supported for longest is `gzip`
compression, and that remains a good general compromise. Files
compressed by the earlier Unix `compress` utility can also be read, but
these are becoming rare. Two other forms of compression, those of the
`bzip2` and `xz` utilities are also available. These generally achieve
higher rates of compression (depending on the file, much higher) at the
expense of slower decompression and much slower compression.

There is some confusion between `xz` and `lzma` compression (see
<https://en.wikipedia.org/wiki/Xz> and
<https://en.wikipedia.org/wiki/LZMA>): R can read files compressed by
most versions of either.

File archives are single files which contain a collection of files, the
most common ones being 'tarballs' and zip files as used to distribute R
packages. R can list and unpack both (see functions `untar` and `unzip`)
and create both (for `zip` with the help of an external program).

---

## Appendix A A sample session

The following session is intended to introduce to you some features of
the R environment by using them. Many features of the system will be
unfamiliar and puzzling at first, but this puzzlement will soon
disappear.

`Start R appropriately for your platform (see Invoking R).`

: The R program begins, with a banner.

    (Within R code, the prompt on the left hand side will not be shown
    to avoid confusion.)

`help.start()`

: Start the HTML interface to on-line help (using a web browser
available at your machine). You should briefly explore the features
of this facility with the mouse.

    Iconify the help window and move on to the next part.

`x <- rnorm(50)`\
`y <- rnorm(x)`

: Generate two pseudo-random normal vectors of _x_- and
_y_-coordinates.

`plot(x, y)`

: Plot the points in the plane. A graphics window will appear
automatically.

`ls()`

: See which R objects are now in the R workspace.

`rm(x, y)`

: Remove objects no longer needed. (Clean up).

`x <- 1:20`

: Make _x = (1, 2, ..., 20)_.

`w <- 1 + sqrt(x)/2`

: A 'weight' vector of standard deviations.

`dummy <- data.frame(x=x, y= x + rnorm(x)*w)`\
`dummy`

: Make a _data frame_ of two columns, _x_ and _y_, and look at it.

`fm <- lm(y ~ x, data=dummy)`\
`summary(fm)`

: Fit a simple linear regression and look at the analysis. With `y` to
the left of the tilde, we are modelling _y_ dependent on _x_.

`fm1 <- lm(y ~ x, data=dummy, weight=1/w^2)`\
`summary(fm1)`

: Since we know the standard deviations, we can do a weighted
regression.

`attach(dummy)`

: Make the columns in the data frame visible as variables.

`lrf <- lowess(x, y)`

: Make a nonparametric local regression function.

`plot(x, y)`

: Standard point plot.

`lines(x, lrf$y)`

: Add in the local regression.

`abline(0, 1, lty=3)`

: The true regression line: (intercept 0, slope 1).

`abline(coef(fm))`

: Unweighted regression line.

`abline(coef(fm1), col = "red")`

: Weighted regression line.

`detach()`

: Remove data frame from the search path.

`plot(fitted(fm), resid(fm),`\
`xlab="Fitted values",`\
`ylab="Residuals",`\
`main="Residuals vs Fitted")`

: A standard regression diagnostic plot to check for
heteroscedasticity. Can you see it?

`qqnorm(resid(fm), main="Residuals Rankit Plot")`

: A normal scores plot to check for skewness, kurtosis and outliers.
(Not very useful here.)

`rm(fm, fm1, lrf, x, dummy)`

: Clean up again.

The next section will look at data from the classical experiment of
Michelson to measure the speed of light. This dataset is available in
the `morley` object, but we will read it to illustrate the `read.table`
function.

`filepath <- system.file("data", "morley.tab" , package="datasets")`\
`filepath`

: Get the path to the data file.

`file.show(filepath)`

: Optional. Look at the file.

`mm <- read.table(filepath)`\
`mm`

: Read in the Michelson data as a data frame, and look at it. There
are five experiments (column `Expt`) and each has 20 runs (column
`Run`) and `sl` is the recorded speed of light, suitably coded.

`mm$Expt <- factor(mm$Expt)`\
`mm$Run <- factor(mm$Run)`

: Change `Expt` and `Run` into factors.

`attach(mm)`

: Make the data frame visible at position 3 (the default).

`plot(Expt, Speed, main="Speed of Light Data", xlab="Experiment No.")`

: Compare the five experiments with simple boxplots.

`fm <- aov(Speed ~ Run + Expt, data=mm)`\
`summary(fm)`

: Analyze as a randomized block, with 'runs' and 'experiments' as
factors.

`fm0 <- update(fm, . ~ . - Run)`\
`anova(fm0, fm)`

: Fit the sub-model omitting 'runs', and compare using a formal
analysis of variance.

`detach()`\
`rm(fm, fm0)`

: Clean up before moving on.

We now look at some more graphical features: contour and image plots.

`x <- seq(-pi, pi, len=50)`\
`y <- x`

: _x_ is a vector of 50 equally spaced values in the interval \[-pi\\,
pi\]. _y_ is the same.

`f <- outer(x, y, function(x, y) cos(y)/(1 + x^2))`

: _f_ is a square matrix, with rows and columns indexed by _x_ and _y_
respectively, of values of the function cos(y)/(1 + x\^2).

`oldpar <- par(no.readonly = TRUE)`\
`par(pty="s")`

: Save the plotting parameters and set the plotting region to
"square".

`contour(x, y, f)`\
`contour(x, y, f, nlevels=15, add=TRUE)`

: Make a contour map of _f_; add in more lines for more detail.

`fa <- (f-t(f))/2`

: `fa` is the "asymmetric part" of _f_. (`t()` is transpose).

`contour(x, y, fa, nlevels=15)`

: Make a contour plot, ...

`par(oldpar)`

: ... and restore the old graphics parameters.

`image(x, y, f)`\
`image(x, y, fa)`

: Make some high density image plots, (of which you can get hardcopies
if you wish), ...

`objects(); rm(x, y, f, fa)`

: ... and clean up before moving on.

R can do complex arithmetic, also.

`th <- seq(-pi, pi, len=100)`\
`z <- exp(1i*th)`

: `1i` is used for the complex number _i_.

`par(pty="s")`\
`plot(z, type="l")`

: Plotting complex arguments means plot imaginary versus real parts.
This should be a circle.

`w <- rnorm(100) + rnorm(100)*1i`

: Suppose we want to sample points within the unit circle. One method
would be to take complex numbers with standard normal real and
imaginary parts ...

`w <- ifelse(Mod(w) > 1, 1/w, w)`

: ... and to map any outside the circle onto their reciprocal.

`plot(w, xlim=c(-1,1), ylim=c(-1,1), pch="+",xlab="x", ylab="y")`\
`lines(z)`

: All points are inside the unit circle, but the distribution is not
uniform.

`w <- sqrt(runif(100))*exp(2*pi*runif(100)*1i)`\
`plot(w, xlim=c(-1,1), ylim=c(-1,1), pch="+", xlab="x", ylab="y")`\
`lines(z)`

: The second method uses the uniform distribution. The points should
now look more evenly spaced over the disc.

`rm(th, w, z)`

: Clean up again.

`q()`

: Quit the R program. You will be asked if you want to save the R
workspace, and for an exploratory session like this, you probably do
not want to save it.

---

## Appendix B Invoking R

Users of R on Windows or macOS should read the OS-specific section
first, but command-line use is also supported.

---

• [Invoking R from the command line](#Invoking-R-from-the-command-line)     
 • [Invoking R under Windows](#Invoking-R-under-Windows)     
 • [Invoking R under macOS](#Invoking-R-under-macOS)     
 • [Scripting with R](#Scripting-with-R)

---

---

### B.1 Invoking R from the command line

When working at a command line on UNIX or Windows, the command
'`R`' can be used both for starting the main R program in the
form

```{.display}
R [options] [<infile] [>outfile],
```

or, via the `R CMD` interface, as a wrapper to various R tools (e.g.,
for processing files in R documentation format or manipulating add-on
packages) which are not intended to be called "directly".

At the Windows command-line, `Rterm.exe` is preferred to `R`.

You need to ensure that either the environment variable `TMPDIR` is
unset or it points to a valid place to create temporary files and
directories.

Most options control what happens at the beginning and at the end of an
R session. The startup mechanism is as follows (see also the on-line
help for topic '`Startup`' for more information, and the
section below for some Windows-specific details).

- Unless `--no-environ` was given, R searches for user and
  site files to process for setting environment variables. The name of
  the site file is the one pointed to by the environment variable
  `R_ENVIRON`; if this is unset, `R_HOME/etc/Renviron.site`
  is used (if it exists). The user file is the one pointed to by the
  environment variable `R_ENVIRON_USER` if this is set; otherwise,
  files `.Renviron` in the current or in the user's home
  directory (in that order) are searched for. These files should
  contain lines of the form '`name=value`'. (See
  `help("Startup")` for a precise description.) Variables you might
  want to set include `R_PAPERSIZE` (the default paper size),
  `R_PRINTCMD` (the default print command) and `R_LIBS` (specifies the
  list of R library trees searched for add-on packages).
- Then R searches for the site-wide startup profile unless the command
  line option `--no-site-file` was given. The name of this
  file is taken from the value of the `R_PROFILE` environment
  variable. If that variable is unset, the default
  `R_HOME/etc/Rprofile.site` is used if this exists.
- Then, unless `--no-init-file` was given, R searches for a
  user profile and sources it. The name of this file is taken from the
  environment variable `R_PROFILE_USER`; if unset, a file called
  `.Rprofile` in the current directory or in the user's home
  directory (in that order) is searched for.
- It also loads a saved workspace from file `.RData` in the
  current directory if there is one (unless `--no-restore` or
  `--no-restore-data` was specified).
- Finally, if a function `.First()` exists, it is executed. This
  function (as well as `.Last()` which is executed at the end of the R
  session) can be defined in the appropriate startup profiles, or
  reside in `.RData`.

In addition, there are options for controlling the memory available to
the R process (see the on-line help for topic '`Memory`' for
more information). Users will not normally need to use these unless they
are trying to limit the amount of memory used by R.

R accepts the following command-line options.

`--help`\
`-h`

: Print short help message to standard output and exit successfully.

`--version`

: Print version information to standard output and exit successfully.

`--encoding=enc`

: Specify the encoding to be assumed for input from the console or
`stdin`. This needs to be an encoding known to `iconv`: see its help
page. (`--encoding enc` is also accepted.) The input is re-encoded
to the locale R is running in and needs to be representable in the
latter's encoding (so e.g. you cannot re-encode Greek text in a
French locale unless that locale uses the UTF-8 encoding).

`RHOME`

: Print the path to the R "home directory" to standard output and exit
successfully. Apart from the front-end shell script and the man
page, R installation puts everything (executables, packages, etc.)
into this directory.

`--save`\
`--no-save`

: Control whether data sets should be saved or not at the end of the R
session. If neither is given in an interactive session, the user is
asked for the desired behavior when ending the session with
[q()]{.kbd}; in non-interactive use one of these must be specified
or implied by some other option (see below).

`--no-environ`

: Do not read any user file to set environment variables.

`--no-site-file`

: Do not read the site-wide profile at startup.

`--no-init-file`

: Do not read the user's profile at startup.

`--restore`\
`--no-restore`\
`--no-restore-data`

: Control whether saved images (file `.RData` in the
directory where R was started) should be restored at startup or not.
The default is to restore. (`--no-restore` implies all the
specific `--no-restore-*` options.)

`--no-restore-history`

: Control whether the history file (normally file `.Rhistory`
in the directory where R was started, but can be set by the
environment variable `R_HISTFILE`) should be restored at startup or
not. The default is to restore.

`--no-Rconsole`

: (Windows only) Prevent loading the `Rconsole` file at
startup.

`--vanilla`

: Combine `--no-save`, `--no-environ`,
`--no-site-file`, `--no-init-file` and
`--no-restore`. Under Windows, this also includes
`--no-Rconsole`.

`-f file`\
`--file=file`

: (not `Rgui.exe`) Take input from `file`{.variable}: '`-`'
means `stdin`. Implies `--no-save` unless `--save`
has been set. On a Unix-alike, shell metacharacters should be
avoided in `file`{.variable} (but spaces are allowed).

`-e expression`

: (not `Rgui.exe`) Use `expression`{.variable} as an input line. One
or more `-e` options can be used, but not together with
`-f` or `--file`. Implies `--no-save`
unless `--save` has been set. (There is a limit of 10,000
bytes on the total length of expressions used in this way.
Expressions containing spaces or shell metacharacters will need to
be quoted.)

`--no-readline`

: (UNIX only) Turn off command-line editing via **readline**. This is
useful when running R from within Emacs using the ESS ("Emacs Speaks
Statistics") package. See [The command-line editor](#The-command_002dline-editor), for more information.
Command-line editing is enabled for default interactive use (see
`--interactive`). This option also affects tilde-expansion:
see the help for `path.expand`.

`--min-vsize=N`\
`--min-nsize=N`

: For expert use only: set the initial trigger sizes for garbage
collection of vector heap (in bytes) and _cons cells_ (number)
respectively. Suffix '`M`' specifies megabytes or millions
of cells respectively. The defaults are 6Mb and 350k respectively
and can also be set by environment variables `R_NSIZE` and
`R_VSIZE`.

`--max-ppsize=N`

: Specify the maximum size of the pointer protection stack as
`N`{.variable} locations. This defaults to 10000, but can be
increased to allow large and complicated calculations to be done.
Currently the maximum value accepted is 100000.

`--max-mem-size=N`

: (Windows only) Specify a limit for the amount of memory to be used
both for R objects and working areas. This is set by default to the
smaller of the amount of physical RAM in the machine and for 32-bit
R, 1.5Gb[^26^](#FOOT26), and must be between 32Mb and the
maximum allowed on that version of Windows.

`--quiet`\
`--silent`\
`-q`

: Do not print out the initial copyright and welcome messages.

`--slave`

: Make R run as quietly as possible. This option is intended to
support programs which use R to compute results for them. It implies
`--quiet` and `--no-save`.

`--interactive`

: (UNIX only) Assert that R really is being run interactively even if
input has been redirected: use if input is from a FIFO or pipe and
fed from an interactive program. (The default is to deduce that R is
being run interactively if and only if `stdin` is connected
to a terminal or `pty`.) Using `-e`, `-f` or
`--file` asserts non-interactive use even if
`--interactive` is given.

    Note that this does not turn on command-line editing.

`--ess`

: (Windows only) Set `Rterm` up for use by `R-inferior-mode` in ESS,
including asserting interactive use (without the command-line
editor) and no buffering of `stdout`.

`--verbose`

: Print more information about progress, and in particular set R's
option `verbose` to `TRUE`. R code uses this option to control the
printing of diagnostic messages.

`--debugger=name`\
`-d name`

: (UNIX only) Run R through debugger `name`{.variable}. For most
debuggers (the exceptions are `valgrind` and recent versions of
`gdb`), further command line options are disregarded, and should
instead be given when starting the R executable from inside the
debugger.

`--gui=type`\
`-g type`

: (UNIX only) Use `type`{.variable} as graphical user interface (note
that this also includes interactive graphics). Currently, possible
values for `type`{.variable} are '`X11`' (the default) and,
provided that '`Tcl/Tk`' support is available,
'`Tk`'. (For back-compatibility, '`x11`' and
'`tk`' are accepted.)

`--arch=name`

: (UNIX only) Run the specified sub-architecture.

`--args`

: This flag does nothing except cause the rest of the command line to
be skipped: this can be useful to retrieve values from it with
`commandArgs(TRUE)`.

Note that input and output can be redirected in the usual way (using
'`<`' and '`>`'), but the line length limit of 4095
bytes still applies. Warning and error messages are sent to the error
channel (`stderr`).

The command `R CMD` allows the invocation of various tools which are
useful in conjunction with R, but not intended to be called "directly".
The general form is

```r
R CMD command args
```

where `command`{.variable} is the name of the tool and `args`{.variable}
the arguments passed on to it.

Currently, the following tools are available.

`BATCH`

: Run R in batch mode. Runs `R --restore --save` with possibly further
options (see `?BATCH`).

`COMPILE`

: (UNIX only) Compile C, C++, Fortran ... files for use with R.

`SHLIB`

: Build shared library for dynamic loading.

`INSTALL`

: Install add-on packages.

`REMOVE`

: Remove add-on packages.

`build`

: Build (that is, package) add-on packages.

`check`

: Check add-on packages.

`LINK`

: (UNIX only) Front-end for creating executable programs.

`Rprof`

: Post-process R profiling files.

`Rdconv`\
`Rd2txt`

: Convert Rd format to various other formats, including HTML, LaTeX,
plain text, and extracting the examples. `Rd2txt` can be used as
shorthand for `Rd2conv -t txt`.

`Rd2pdf`

: Convert Rd format to PDF.

`Stangle`

: Extract S/R code from Sweave or other vignette documentation

`Sweave`

: Process Sweave or other vignette documentation

`Rdiff`

: Diff R output ignoring headers etc

`config`

: Obtain configuration information

`javareconf`

: (Unix only) Update the Java configuration variables

`rtags`

: (Unix only) Create Emacs-style tag files from C, R, and Rd files

`open`

: (Windows only) Open a file via Windows' file associations

`texify`

: (Windows only) Process (La)TeX files with R's style files

Use

```r
R CMD command --help
```

to obtain usage information for each of the tools accessible via the
`R CMD` interface.

In addition, you can use options `--arch=`,
`--no-environ`, `--no-init-file`,
`--no-site-file` and `--vanilla` between `R` and
`CMD`: these affect any R processes run by the tools. (Here
`--vanilla` is equivalent to
`--no-environ --no-site-file --no-init-file`.) However, note
that `R CMD` does not of itself use any R startup files (in particular,
neither user nor site `Renviron` files), and all of the R
processes run by these tools (except `BATCH`) use
`--no-restore`. Most use `--vanilla` and so invoke no
R startup files: the current exceptions are `INSTALL`, `REMOVE`,
`Sweave` and `SHLIB` (which uses
`--no-site-file --no-init-file`).

```r
R CMD cmd args
```

for any other executable `cmd` on the path or given by an absolute
filepath: this is useful to have the same environment as R or the
specific commands run under, for example to run `ldd` or `pdflatex`.
Under Windows `cmd`{.variable} can be an executable or a batch file, or
if it has extension `.sh` or `.pl` the appropriate interpreter (if
available) is called to run it.

---

### B.2 Invoking R under Windows

There are two ways to run R under Windows. Within a terminal window
(e.g. `cmd.exe` or a more capable shell), the methods described in the

will run LaTeX on `mydoc.tex`, with the path to R's
`share/texmf` macros appended to `TEXINPUTS`. (Unfortunately,
this does not help with the MiKTeX build of LaTeX, but
`R CMD texify mydoc` will work in that case.)

---

### B.3 Invoking R under macOS

There are two ways to run R under macOS. Within a `Terminal.app` window
by invoking `R`, the methods described in the first subsection apply.
There is also console-based GUI (`R.app`) that by default is installed
in the `Applications` folder on your system. It is a standard
double-clickable macOS application.

The startup procedure under macOS is very similar to that under UNIX,
but `R.app` does not make use of command-line arguments. The 'home
directory' is the one inside the R.framework, but the startup and
current working directory are set as the user's home directory unless a
different startup directory is given in the Preferences window
accessible from within the GUI.

---

### B.4 Scripting with R

If you just want to run a file `foo.R` of R commands, the
recommended way is to use `R CMD BATCH foo.R`. If you want to run this
in the background or as a batch job use OS-specific facilities to do so:
for example in most shells on Unix-alike OSes `R CMD BATCH foo.R &` runs
a background job.

You can pass parameters to scripts via additional arguments on the
command line: for example (where the exact quoting needed will depend on
the shell in use)

```r
R CMD BATCH "--args arg1 arg2" foo.R &
```

will pass arguments to a script which can be retrieved as a character
vector by

```r
args <- commandArgs(TRUE)
```

This is made simpler by the alternative front-end `Rscript`, which can
be invoked by

```r
Rscript foo.R arg1 arg2
```

and this can also be used to write executable script files like (at
least on Unix-alikes, and in some Windows shells)

```r
#! /path/to/Rscript
args <- commandArgs(TRUE)
...
q(status=<exit status code>)
```

If this is entered into a text file `runfoo` and this is made
executable (by `chmod 755 runfoo`), it can be invoked for different
arguments by

```r
runfoo arg1 arg2
```

For further options see `help("Rscript")`. This writes R output to
`stdout` and `stderr`, and this can be redirected in
the usual way for the shell running the command.

If you do not wish to hardcode the path to `Rscript` but have it in your
path (which is normally the case for an installed R except on Windows,
but e.g. macOS users may need to add `/usr/local/bin` to their
path), use

```r
#! /usr/bin/env Rscript
...
```

At least in Bourne and bash shells, the `#!` mechanism does **not**
allow extra arguments like `#! /usr/bin/env Rscript --vanilla`.

One thing to consider is what `stdin()` refers to. It is commonplace to
write R scripts with segments like

```r
chem <- scan(n=24)
2.90 3.10 3.40 3.40 3.70 3.70 2.80 2.50 2.40 2.40 2.70 2.20
5.28 3.37 3.03 3.03 28.95 3.77 3.40 2.20 3.50 3.60 3.70 3.70
```

and `stdin()` refers to the script file to allow such traditional usage.
If you want to refer to the process's `stdin`, use `"stdin"` as
a `file` connection, e.g. `scan("stdin", ...)`.

Another way to write executable script files (suggested by François
Pinard) is to use a _here document_ like

```r
#!/bin/sh
[environment variables can be set here]
R --slave [other options] <<EOF

   R program goes here...

EOF
```

but here `stdin()` refers to the program source and `"stdin"` will not
be usable.

Short scripts can be passed to `Rscript` on the command-line _via_ the
`-e` flag. (Empty scripts are not accepted.)

Note that on a Unix-alike the input filename (such as `foo.R`)
should not contain spaces nor shell metacharacters.

---

## Appendix C The command-line editor

### C.1 Preliminaries

When the GNU **readline** library is available at the time R is
configured for compilation under UNIX, an inbuilt command line editor
allowing recall, editing and re-submission of prior commands is used.
Note that other versions of **readline** exist and may be used by the
inbuilt command line editor: this used to happen on macOS.

It can be disabled (useful for usage with ESS [^27^](#FOOT27))
using the startup option `--no-readline`.

Windows versions of R have somewhat simpler command-line editing: see
'`Console`' under the '`Help`' menu of the GUI, and
the file `README.Rterm` for command-line editing under
`Rterm.exe`.

When using R with GNU[^28^](#FOOT28) **readline** capabilities,
the functions described below are available, as well as others
(probably) documented in `man readline` or `info readline` on your
system.

Many of these use either Control or Meta characters. Control characters,
such as [Control-m]{.kbd}, are obtained by holding the `CTRL`{.key} down
while you press the `m`{.key} key, and are written as [C-m]{.kbd} below.
Meta characters, such as [Meta-b]{.kbd}, are typed by holding down
`META`{.key}[^29^](#FOOT29) and pressing `b`{.key}, and written
as [M-b]{.kbd} in the following. If your terminal does not have a
`META`{.key} key enabled, you can still type Meta characters using
two-character sequences starting with [ESC]{.kbd}. Thus, to enter
[M-b]{.kbd}, you could type `ESC`{.key}`b`{.key}. The [ESC]{.kbd}
character sequences are also allowed on terminals with real Meta keys.
Note that case is significant for Meta characters.

Some but not all versions[^30^](#FOOT30) of **readline** will
recognize resizing of the terminal window so this is best avoided.

### C.2 Editing actions

The R program keeps a history of the command lines you type, including
the erroneous lines, and commands in your history may be recalled,
changed if necessary, and re-submitted as new commands. In Emacs-style
command-line editing any straight typing you do while in this editing
phase causes the characters to be inserted in the command you are
editing, displacing any characters to the right of the cursor. In _vi_
mode character insertion mode is started by [M-i]{.kbd} or [M-a]{.kbd},
characters are typed and insertion mode is finished by typing a further
`ESC`{.key}. (The default is Emacs-style, and only that is described
here: for _vi_ mode see the **readline** documentation.)

Pressing the `RET`{.key} command at any time causes the command to be
re-submitted.

Other editing actions are summarized in the following table.

### C.3 Command-line editor summary

#### Command recall and vertical motion

[C-p]{.kbd}

: Go to the previous command (backwards in the history).

[C-n]{.kbd}

: Go to the next command (forwards in the history).

[C-r `text`{.variable}]{.kbd}

: Find the last command with the `text`{.variable} string in it. This
can be cancelled by `C-g` (and on some versions of R by `C-c`).

On most terminals, you can also use the up and down arrow keys instead
of [C-p]{.kbd} and [C-n]{.kbd}, respectively.

#### Horizontal motion of the cursor

[C-a]{.kbd}

: Go to the beginning of the command.

[C-e]{.kbd}

: Go to the end of the line.

[M-b]{.kbd}

: Go back one word.

[M-f]{.kbd}

: Go forward one word.

[C-b]{.kbd}

: Go back one character.

[C-f]{.kbd}

: Go forward one character.

On most terminals, you can also use the left and right arrow keys
instead of [C-b]{.kbd} and [C-f]{.kbd}, respectively.

#### Editing and re-submission

[`text`{.variable}]{.kbd}

: Insert `text`{.variable} at the cursor.

[C-f `text`{.variable}]{.kbd}

: Append `text`{.variable} after the cursor.

[[DEL]{.key}]{.kbd}

: Delete the previous character (left of the cursor).

[C-d]{.kbd}

: Delete the character under the cursor.

[M-d]{.kbd}

: Delete the rest of the word under the cursor, and "save" it.

[C-k]{.kbd}

: Delete from cursor to end of command, and "save" it.

[C-y]{.kbd}

: Insert (yank) the last "saved" text here.

[C-t]{.kbd}

: Transpose the character under the cursor with the next.

[M-l]{.kbd}

: Change the rest of the word to lower case.

[M-c]{.kbd}

: Change the rest of the word to upper case.

[[RET]{.key}]{.kbd}

: Re-submit the command to R.

The final `RET`{.key} terminates the command line editing sequence.

The **readline** key bindings can be customized in the usual way _via_ a
`~/.inputrc` file. These customizations can be conditioned on
application `R`, that is by including a section like

```r
$if R
  "\C-xd": "q('no')\n"
$endif
```

---

## Appendix D Function and variable index

---

Jump to:   [**!**](#Function-and-variable-index_vr_symbol-1){.summary-letter}  
[**%**](#Function-and-variable-index_vr_symbol-2){.summary-letter}  
[**&**](#Function-and-variable-index_vr_symbol-3){.summary-letter}  
[**\***](#Function-and-variable-index_vr_symbol-4){.summary-letter}  
[**+**](#Function-and-variable-index_vr_symbol-5){.summary-letter}  
[**-**](#Function-and-variable-index_vr_symbol-6){.summary-letter}  
[**.**](#Function-and-variable-index_vr_symbol-7){.summary-letter}  
[**/**](#Function-and-variable-index_vr_symbol-8){.summary-letter}  
[**:**](#Function-and-variable-index_vr_symbol-9){.summary-letter}  
[**\<**](#Function-and-variable-index_vr_symbol-10){.summary-letter}  
[**=**](#Function-and-variable-index_vr_symbol-11){.summary-letter}  
[**\>**](#Function-and-variable-index_vr_symbol-12){.summary-letter}  
[**?**](#Function-and-variable-index_vr_symbol-13){.summary-letter}  
[**\^**](#Function-and-variable-index_vr_symbol-14){.summary-letter}  
[**\|**](#Function-and-variable-index_vr_symbol-15){.summary-letter}  
[**\~**](#Function-and-variable-index_vr_symbol-16){.summary-letter}
 \
 [**A**](#Function-and-variable-index_vr_letter-A){.summary-letter}  
[**B**](#Function-and-variable-index_vr_letter-B){.summary-letter}  
[**C**](#Function-and-variable-index_vr_letter-C){.summary-letter}  
[**D**](#Function-and-variable-index_vr_letter-D){.summary-letter}  
[**E**](#Function-and-variable-index_vr_letter-E){.summary-letter}  
[**F**](#Function-and-variable-index_vr_letter-F){.summary-letter}  
[**G**](#Function-and-variable-index_vr_letter-G){.summary-letter}  
[**H**](#Function-and-variable-index_vr_letter-H){.summary-letter}  
[**I**](#Function-and-variable-index_vr_letter-I){.summary-letter}  
[**J**](#Function-and-variable-index_vr_letter-J){.summary-letter}  
[**K**](#Function-and-variable-index_vr_letter-K){.summary-letter}  
[**L**](#Function-and-variable-index_vr_letter-L){.summary-letter}  
[**M**](#Function-and-variable-index_vr_letter-M){.summary-letter}  
[**N**](#Function-and-variable-index_vr_letter-N){.summary-letter}  
[**O**](#Function-and-variable-index_vr_letter-O){.summary-letter}  
[**P**](#Function-and-variable-index_vr_letter-P){.summary-letter}  
[**Q**](#Function-and-variable-index_vr_letter-Q){.summary-letter}  
[**R**](#Function-and-variable-index_vr_letter-R){.summary-letter}  
[**S**](#Function-and-variable-index_vr_letter-S){.summary-letter}  
[**T**](#Function-and-variable-index_vr_letter-T){.summary-letter}  
[**U**](#Function-and-variable-index_vr_letter-U){.summary-letter}  
[**V**](#Function-and-variable-index_vr_letter-V){.summary-letter}  
[**W**](#Function-and-variable-index_vr_letter-W){.summary-letter}  
[**X**](#Function-and-variable-index_vr_letter-X){.summary-letter}

---

Index Entry

Section

---

!

[`!`](#index-_0021):

[Logical vectors](#Logical-vectors)

[`!=`](#index-_0021_003d):

[Logical vectors](#Logical-vectors)

---

\%

[`%*%`](#index-_0025_002a_0025):

[Multiplication](#Multiplication)

[`%o%`](#index-_0025o_0025):

[The outer product of two arrays](#The-outer-product-of-two-arrays)

---

&

[`&`](#index-_0026):

[Logical vectors](#Logical-vectors)

[`&&`](#index-_0026_0026):

[Conditional execution](#Conditional-execution)

---

\*

[`*`](#index-_002a):

[Vector arithmetic](#Vector-arithmetic)

---

\+

[`+`](#index-_002b):

[Vector arithmetic](#Vector-arithmetic)

---

\-

[`-`](#index-_002d):

[Vector arithmetic](#Vector-arithmetic)

---

.

[`.`](#index-_002e):

[Updating fitted models](#Updating-fitted-models)

[`.First`](#index-_002eFirst):

[Customizing the environment](#Customizing-the-environment)

[`.Last`](#index-_002eLast):

[Customizing the environment](#Customizing-the-environment)

---

/

[`/`](#index-_002f):

[Vector arithmetic](#Vector-arithmetic)

---

:

[`:`](#index-_003a):

[Generating regular sequences](#Generating-regular-sequences)

[`::`](#index-_003a_003a):

[Namespaces](#Namespaces)

[`:::`](#index-_003a_003a_003a):

[Namespaces](#Namespaces)

---

\<

[`<`](#index-_003c):

[Logical vectors](#Logical-vectors)

[`<<-`](#index-_003c_003c_002d):

[Scope](#Scope)

[`<=`](#index-_003c_003d):

[Logical vectors](#Logical-vectors)

---

=

[`==`](#index-_003d_003d):

[Logical vectors](#Logical-vectors)

---

\>

[`>`](#index-_003e):

[Logical vectors](#Logical-vectors)

[`>=`](#index-_003e_003d):

[Logical vectors](#Logical-vectors)

---

?

[`?`](#index-_003f):

[Getting help](#Getting-help)

[`??`](#index-_003f_003f):

[Getting help](#Getting-help)

---

\^

[`^`](#index-_005e):

[Vector arithmetic](#Vector-arithmetic)

---

\|

[`|`](#index-_007c):

[Logical vectors](#Logical-vectors)

[`||`](#index-_007c_007c):

[Conditional execution](#Conditional-execution)

---

\~

[`~`](#index-_007e):

[Formulae for statistical models](#Formulae-for-statistical-models)

---

A

[`abline`](#index-abline):

[Low-level plotting commands](#Low_002dlevel-plotting-commands)

[`ace`](#index-ace):

[Some non-standard models](#Some-non_002dstandard-models)

[`add1`](#index-add1):

[Updating fitted models](#Updating-fitted-models)

[`anova`](#index-anova):

[Generic functions for extracting model information](#Generic-functions-for-extracting-model-information)

[`anova`](#index-anova-1):

[ANOVA tables](#ANOVA-tables)

[`aov`](#index-aov):

[Analysis of variance and model comparison](#Analysis-of-variance-and-model-comparison)

[`aperm`](#index-aperm):

[Generalized transpose of an array](#Generalized-transpose-of-an-array)

[`array`](#index-array):

[The array() function](#The-array_0028_0029-function)

[`as.data.frame`](#index-as_002edata_002eframe):

[Making data frames](#Making-data-frames)

[`as.vector`](#index-as_002evector):

[The concatenation function c() with arrays](#The-concatenation-function-c_0028_0029-with-arrays)

[`attach`](#index-attach):

[attach() and detach()](#attach_0028_0029-and-detach_0028_0029)

[`attr`](#index-attr):

[Getting and setting attributes](#Getting-and-setting-attributes)

[`attr`](#index-attr-1):

[Getting and setting attributes](#Getting-and-setting-attributes)

[`attributes`](#index-attributes):

[Getting and setting attributes](#Getting-and-setting-attributes)

[`attributes`](#index-attributes-1):

[Getting and setting attributes](#Getting-and-setting-attributes)

[`avas`](#index-avas):

[Some non-standard models](#Some-non_002dstandard-models)

[`axis`](#index-axis):

[Low-level plotting commands](#Low_002dlevel-plotting-commands)

---

B

[`boxplot`](#index-boxplot):

[One- and two-sample tests](#One_002d-and-two_002dsample-tests)

[`break`](#index-break):

[Repetitive execution](#Repetitive-execution)

[`bruto`](#index-bruto):

[Some non-standard models](#Some-non_002dstandard-models)

---

C

[`c`](#index-c):

[Vectors and assignment](#Vectors-and-assignment)

[`c`](#index-c-1):

[Character vectors](#Character-vectors)

[`c`](#index-c-2):

[The concatenation function c() with arrays](#The-concatenation-function-c_0028_0029-with-arrays)

[`c`](#index-c-3):

[Concatenating lists](#Concatenating-lists)

[`C`](#index-C):

[Contrasts](#Contrasts)

[`cbind`](#index-cbind):

[Forming partitioned matrices](#Forming-partitioned-matrices)

[`coef`](#index-coef):

[Generic functions for extracting model information](#Generic-functions-for-extracting-model-information)

[`coefficients`](#index-coefficients):

[Generic functions for extracting model information](#Generic-functions-for-extracting-model-information)

[`contour`](#index-contour):

[Display graphics](#Display-graphics)

[`contrasts`](#index-contrasts):

[Contrasts](#Contrasts)

[`coplot`](#index-coplot):

[Displaying multivariate data](#Displaying-multivariate-data)

[`cos`](#index-cos):

[Vector arithmetic](#Vector-arithmetic)

[`crossprod`](#index-crossprod):

[Index matrices](#Index-matrices)

[`crossprod`](#index-crossprod-1):

[Multiplication](#Multiplication)

[`cut`](#index-cut):

[Frequency tables from factors](#Frequency-tables-from-factors)

---

D

[`data`](#index-data):

[Accessing builtin datasets](#Accessing-builtin-datasets)

[`data.frame`](#index-data_002eframe):

[Making data frames](#Making-data-frames)

[`density`](#index-density):

[Examining the distribution of a set of data](#Examining-the-distribution-of-a-set-of-data)

[`det`](#index-det):

[Singular value decomposition and determinants](#Singular-value-decomposition-and-determinants)

[`detach`](#index-detach):

[attach() and detach()](#attach_0028_0029-and-detach_0028_0029)

[`determinant`](#index-determinant):

[Singular value decomposition and determinants](#Singular-value-decomposition-and-determinants)

[`dev.list`](#index-dev_002elist):

[Multiple graphics devices](#Multiple-graphics-devices)

[`dev.next`](#index-dev_002enext):

[Multiple graphics devices](#Multiple-graphics-devices)

[`dev.off`](#index-dev_002eoff):

[Multiple graphics devices](#Multiple-graphics-devices)

[`dev.prev`](#index-dev_002eprev):

[Multiple graphics devices](#Multiple-graphics-devices)

[`dev.set`](#index-dev_002eset):

[Multiple graphics devices](#Multiple-graphics-devices)

[`deviance`](#index-deviance):

[Generic functions for extracting model information](#Generic-functions-for-extracting-model-information)

[`diag`](#index-diag):

[Multiplication](#Multiplication)

[`dim`](#index-dim):

[Arrays](#Arrays)

[`dotchart`](#index-dotchart):

[Display graphics](#Display-graphics)

[`drop1`](#index-drop1):

[Updating fitted models](#Updating-fitted-models)

---

E

[`ecdf`](#index-ecdf):

[Examining the distribution of a set of data](#Examining-the-distribution-of-a-set-of-data)

[`edit`](#index-edit):

[Editing data](#Editing-data)

[`eigen`](#index-eigen):

[Eigenvalues and eigenvectors](#Eigenvalues-and-eigenvectors)

[`else`](#index-else):

[Conditional execution](#Conditional-execution)

[`Error`](#index-Error):

[Analysis of variance and model comparison](#Analysis-of-variance-and-model-comparison)

[`example`](#index-example):

[Getting help](#Getting-help)

[`exp`](#index-exp):

[Vector arithmetic](#Vector-arithmetic)

---

F

[`F`](#index-F):

[Logical vectors](#Logical-vectors)

[`factor`](#index-factor):

[Factors](#Factors)

[`FALSE`](#index-FALSE):

[Logical vectors](#Logical-vectors)

[`fivenum`](#index-fivenum):

[Examining the distribution of a set of data](#Examining-the-distribution-of-a-set-of-data)

[`for`](#index-for):

[Repetitive execution](#Repetitive-execution)

[`formula`](#index-formula):

[Generic functions for extracting model information](#Generic-functions-for-extracting-model-information)

[`function`](#index-function):

[Writing your own functions](#Writing-your-own-functions)

---

G

[`getAnywhere`](#index-getAnywhere):

[Object orientation](#Object-orientation)

[`getS3method`](#index-getS3method):

[Object orientation](#Object-orientation)

[`glm`](#index-glm):

[The glm() function](#The-glm_0028_0029-function)

---

H

[`help`](#index-help):

[Getting help](#Getting-help)

[`help`](#index-help-1):

[Getting help](#Getting-help)

[`help.search`](#index-help_002esearch):

[Getting help](#Getting-help)

[`help.start`](#index-help_002estart):

[Getting help](#Getting-help)

[`hist`](#index-hist):

[Examining the distribution of a set of data](#Examining-the-distribution-of-a-set-of-data)

[`hist`](#index-hist-1):

[Display graphics](#Display-graphics)

---

I

[`identify`](#index-identify):

[Interacting with graphics](#Interacting-with-graphics)

[`if`](#index-if):

[Conditional execution](#Conditional-execution)

[`if`](#index-if-1):

[Conditional execution](#Conditional-execution)

[`ifelse`](#index-ifelse):

[Conditional execution](#Conditional-execution)

[`image`](#index-image):

[Display graphics](#Display-graphics)

[`is.na`](#index-is_002ena):

[Missing values](#Missing-values)

[`is.nan`](#index-is_002enan):

[Missing values](#Missing-values)

---

J

[`jpeg`](#index-jpeg):

[Device drivers](#Device-drivers)

---

K

[`ks.test`](#index-ks_002etest):

[Examining the distribution of a set of data](#Examining-the-distribution-of-a-set-of-data)

---

L

[`legend`](#index-legend):

[Low-level plotting commands](#Low_002dlevel-plotting-commands)

[`length`](#index-length):

[Vector arithmetic](#Vector-arithmetic)

[`length`](#index-length-1):

[The intrinsic attributes mode and length](#The-intrinsic-attributes-mode-and-length)

[`levels`](#index-levels):

[Factors](#Factors)

[`lines`](#index-lines):

[Low-level plotting commands](#Low_002dlevel-plotting-commands)

[`list`](#index-list):

[Lists](#Lists)

[`lm`](#index-lm):

[Linear models](#Linear-models)

[`lme`](#index-lme):

[Some non-standard models](#Some-non_002dstandard-models)

[`locator`](#index-locator):

[Interacting with graphics](#Interacting-with-graphics)

[`loess`](#index-loess):

[Some non-standard models](#Some-non_002dstandard-models)

[`loess`](#index-loess-1):

[Some non-standard models](#Some-non_002dstandard-models)

[`log`](#index-log):

[Vector arithmetic](#Vector-arithmetic)

[`lqs`](#index-lqs):

[Some non-standard models](#Some-non_002dstandard-models)

[`lsfit`](#index-lsfit):

[Least squares fitting and the QR decomposition](#Least-squares-fitting-and-the-QR-decomposition)

---

M

[`mars`](#index-mars):

[Some non-standard models](#Some-non_002dstandard-models)

[`max`](#index-max):

[Vector arithmetic](#Vector-arithmetic)

[`mean`](#index-mean):

[Vector arithmetic](#Vector-arithmetic)

[`methods`](#index-methods):

[Object orientation](#Object-orientation)

[`min`](#index-min):

[Vector arithmetic](#Vector-arithmetic)

[`mode`](#index-mode):

[The intrinsic attributes mode and length](#The-intrinsic-attributes-mode-and-length)

---

N

[`NA`](#index-NA):

[Missing values](#Missing-values)

[`NaN`](#index-NaN):

[Missing values](#Missing-values)

[`ncol`](#index-ncol):

[Matrix facilities](#Matrix-facilities)

[`next`](#index-next):

[Repetitive execution](#Repetitive-execution)

[`nlm`](#index-nlm):

[Nonlinear least squares and maximum likelihood models](#Nonlinear-least-squares-and-maximum-likelihood-models)

[`nlm`](#index-nlm-1):

[Least squares](#Least-squares)

[`nlm`](#index-nlm-2):

[Maximum likelihood](#Maximum-likelihood)

[`nlme`](#index-nlme):

[Some non-standard models](#Some-non_002dstandard-models)

[`nlminb`](#index-nlminb):

[Nonlinear least squares and maximum likelihood models](#Nonlinear-least-squares-and-maximum-likelihood-models)

[`nrow`](#index-nrow):

[Matrix facilities](#Matrix-facilities)

---

O

[`optim`](#index-optim):

[Nonlinear least squares and maximum likelihood models](#Nonlinear-least-squares-and-maximum-likelihood-models)

[`order`](#index-order):

[Vector arithmetic](#Vector-arithmetic)

[`ordered`](#index-ordered):

[Ordered factors](#Ordered-factors)

[`ordered`](#index-ordered-1):

[Ordered factors](#Ordered-factors)

[`outer`](#index-outer):

[The outer product of two arrays](#The-outer-product-of-two-arrays)

---

P

[`pairs`](#index-pairs):

[Displaying multivariate data](#Displaying-multivariate-data)

[`par`](#index-par):

[The par() function](#The-par_0028_0029-function)

[`paste`](#index-paste):

[Character vectors](#Character-vectors)

[`pdf`](#index-pdf):

[Device drivers](#Device-drivers)

[`persp`](#index-persp):

[Display graphics](#Display-graphics)

[`plot`](#index-plot):

[Generic functions for extracting model information](#Generic-functions-for-extracting-model-information)

[`plot`](#index-plot-1):

[The plot() function](#The-plot_0028_0029-function)

[`pmax`](#index-pmax):

[Vector arithmetic](#Vector-arithmetic)

[`pmin`](#index-pmin):

[Vector arithmetic](#Vector-arithmetic)

[`png`](#index-png):

[Device drivers](#Device-drivers)

[`points`](#index-points):

[Low-level plotting commands](#Low_002dlevel-plotting-commands)

[`polygon`](#index-polygon):

[Low-level plotting commands](#Low_002dlevel-plotting-commands)

[`postscript`](#index-postscript):

[Device drivers](#Device-drivers)

[`predict`](#index-predict):

[Generic functions for extracting model information](#Generic-functions-for-extracting-model-information)

[`print`](#index-print):

[Generic functions for extracting model information](#Generic-functions-for-extracting-model-information)

[`prod`](#index-prod):

[Vector arithmetic](#Vector-arithmetic)

---

Q

[`qqline`](#index-qqline):

[Examining the distribution of a set of data](#Examining-the-distribution-of-a-set-of-data)

[`qqline`](#index-qqline-1):

[Display graphics](#Display-graphics)

[`qqnorm`](#index-qqnorm):

[Examining the distribution of a set of data](#Examining-the-distribution-of-a-set-of-data)

[`qqnorm`](#index-qqnorm-1):

[Display graphics](#Display-graphics)

[`qqplot`](#index-qqplot):

[Display graphics](#Display-graphics)

[`qr`](#index-qr):

[Least squares fitting and the QR decomposition](#Least-squares-fitting-and-the-QR-decomposition)

[`quartz`](#index-quartz):

[Device drivers](#Device-drivers)

---

R

[`range`](#index-range):

[Vector arithmetic](#Vector-arithmetic)

[`rbind`](#index-rbind):

[Forming partitioned matrices](#Forming-partitioned-matrices)

[`read.table`](#index-read_002etable):

[The read.table() function](#The-read_002etable_0028_0029-function)

[`rep`](#index-rep):

[Generating regular sequences](#Generating-regular-sequences)

[`repeat`](#index-repeat):

[Repetitive execution](#Repetitive-execution)

[`resid`](#index-resid):

[Generic functions for extracting model information](#Generic-functions-for-extracting-model-information)

[`residuals`](#index-residuals):

[Generic functions for extracting model information](#Generic-functions-for-extracting-model-information)

[`rlm`](#index-rlm):

[Some non-standard models](#Some-non_002dstandard-models)

[`rm`](#index-rm):

[Data permanency and removing objects](#Data-permanency-and-removing-objects)

---

S

[`scan`](#index-scan):

[The scan() function](#The-scan_0028_0029-function)

[`sd`](#index-sd):

[The function tapply() and ragged arrays](#The-function-tapply_0028_0029-and-ragged-arrays)

[`search`](#index-search):

[Managing the search path](#Managing-the-search-path)

[`seq`](#index-seq):

[Generating regular sequences](#Generating-regular-sequences)

[`shapiro.test`](#index-shapiro_002etest):

[Examining the distribution of a set of data](#Examining-the-distribution-of-a-set-of-data)

[`sin`](#index-sin):

[Vector arithmetic](#Vector-arithmetic)

[`sink`](#index-sink):

[Executing commands from or diverting output to a file](#Executing-commands-from-or-diverting-output-to-a-file)

[`solve`](#index-solve):

[Linear equations and inversion](#Linear-equations-and-inversion)

[`sort`](#index-sort):

[Vector arithmetic](#Vector-arithmetic)

[`source`](#index-source):

[Executing commands from or diverting output to a file](#Executing-commands-from-or-diverting-output-to-a-file)

[`split`](#index-split):

[Repetitive execution](#Repetitive-execution)

[`sqrt`](#index-sqrt):

[Vector arithmetic](#Vector-arithmetic)

[`stem`](#index-stem):

[Examining the distribution of a set of data](#Examining-the-distribution-of-a-set-of-data)

[`step`](#index-step):

[Generic functions for extracting model information](#Generic-functions-for-extracting-model-information)

[`step`](#index-step-1):

[Updating fitted models](#Updating-fitted-models)

[`sum`](#index-sum):

[Vector arithmetic](#Vector-arithmetic)

[`summary`](#index-summary):

[Examining the distribution of a set of data](#Examining-the-distribution-of-a-set-of-data)

[`summary`](#index-summary-1):

[Generic functions for extracting model information](#Generic-functions-for-extracting-model-information)

[`svd`](#index-svd):

[Singular value decomposition and determinants](#Singular-value-decomposition-and-determinants)

---

T

[`T`](#index-T):

[Logical vectors](#Logical-vectors)

[`t`](#index-t):

[Generalized transpose of an array](#Generalized-transpose-of-an-array)

[`t.test`](#index-t_002etest):

[One- and two-sample tests](#One_002d-and-two_002dsample-tests)

[`table`](#index-table):

[Index matrices](#Index-matrices)

[`table`](#index-table-1):

[Frequency tables from factors](#Frequency-tables-from-factors)

[`tan`](#index-tan):

[Vector arithmetic](#Vector-arithmetic)

[`tapply`](#index-tapply):

[The function tapply() and ragged arrays](#The-function-tapply_0028_0029-and-ragged-arrays)

[`text`](#index-text):

[Low-level plotting commands](#Low_002dlevel-plotting-commands)

[`title`](#index-title):

[Low-level plotting commands](#Low_002dlevel-plotting-commands)

[`tree`](#index-tree):

[Some non-standard models](#Some-non_002dstandard-models)

[`TRUE`](#index-TRUE):

[Logical vectors](#Logical-vectors)

---

U

[`unclass`](#index-unclass):

[The class of an object](#The-class-of-an-object)

[`update`](#index-update):

[Updating fitted models](#Updating-fitted-models)

---

V

[`var`](#index-var):

[Vector arithmetic](#Vector-arithmetic)

[`var`](#index-var-1):

[The function tapply() and ragged arrays](#The-function-tapply_0028_0029-and-ragged-arrays)

[`var.test`](#index-var_002etest):

[One- and two-sample tests](#One_002d-and-two_002dsample-tests)

[`vcov`](#index-vcov):

[Generic functions for extracting model information](#Generic-functions-for-extracting-model-information)

[`vector`](#index-vector):

[Vectors and assignment](#Vectors-and-assignment)

---

W

[`while`](#index-while):

[Repetitive execution](#Repetitive-execution)

[`wilcox.test`](#index-wilcox_002etest):

[One- and two-sample tests](#One_002d-and-two_002dsample-tests)

[`windows`](#index-windows):

[Device drivers](#Device-drivers)

---

X

[`X11`](#index-X11):

[Device drivers](#Device-drivers)

---

---

Jump to:   [**!**](#Function-and-variable-index_vr_symbol-1){.summary-letter}  
[**%**](#Function-and-variable-index_vr_symbol-2){.summary-letter}  
[**&**](#Function-and-variable-index_vr_symbol-3){.summary-letter}  
[**\***](#Function-and-variable-index_vr_symbol-4){.summary-letter}  
[**+**](#Function-and-variable-index_vr_symbol-5){.summary-letter}  
[**-**](#Function-and-variable-index_vr_symbol-6){.summary-letter}  
[**.**](#Function-and-variable-index_vr_symbol-7){.summary-letter}  
[**/**](#Function-and-variable-index_vr_symbol-8){.summary-letter}  
[**:**](#Function-and-variable-index_vr_symbol-9){.summary-letter}  
[**\<**](#Function-and-variable-index_vr_symbol-10){.summary-letter}  
[**=**](#Function-and-variable-index_vr_symbol-11){.summary-letter}  
[**\>**](#Function-and-variable-index_vr_symbol-12){.summary-letter}  
[**?**](#Function-and-variable-index_vr_symbol-13){.summary-letter}  
[**\^**](#Function-and-variable-index_vr_symbol-14){.summary-letter}  
[**\|**](#Function-and-variable-index_vr_symbol-15){.summary-letter}  
[**\~**](#Function-and-variable-index_vr_symbol-16){.summary-letter}
 \
 [**A**](#Function-and-variable-index_vr_letter-A){.summary-letter}  
[**B**](#Function-and-variable-index_vr_letter-B){.summary-letter}  
[**C**](#Function-and-variable-index_vr_letter-C){.summary-letter}  
[**D**](#Function-and-variable-index_vr_letter-D){.summary-letter}  
[**E**](#Function-and-variable-index_vr_letter-E){.summary-letter}  
[**F**](#Function-and-variable-index_vr_letter-F){.summary-letter}  
[**G**](#Function-and-variable-index_vr_letter-G){.summary-letter}  
[**H**](#Function-and-variable-index_vr_letter-H){.summary-letter}  
[**I**](#Function-and-variable-index_vr_letter-I){.summary-letter}  
[**J**](#Function-and-variable-index_vr_letter-J){.summary-letter}  
[**K**](#Function-and-variable-index_vr_letter-K){.summary-letter}  
[**L**](#Function-and-variable-index_vr_letter-L){.summary-letter}  
[**M**](#Function-and-variable-index_vr_letter-M){.summary-letter}  
[**N**](#Function-and-variable-index_vr_letter-N){.summary-letter}  
[**O**](#Function-and-variable-index_vr_letter-O){.summary-letter}  
[**P**](#Function-and-variable-index_vr_letter-P){.summary-letter}  
[**Q**](#Function-and-variable-index_vr_letter-Q){.summary-letter}  
[**R**](#Function-and-variable-index_vr_letter-R){.summary-letter}  
[**S**](#Function-and-variable-index_vr_letter-S){.summary-letter}  
[**T**](#Function-and-variable-index_vr_letter-T){.summary-letter}  
[**U**](#Function-and-variable-index_vr_letter-U){.summary-letter}  
[**V**](#Function-and-variable-index_vr_letter-V){.summary-letter}  
[**W**](#Function-and-variable-index_vr_letter-W){.summary-letter}  
[**X**](#Function-and-variable-index_vr_letter-X){.summary-letter}

---

---

## Appendix E Concept index

---

Jump to:   [**A**](#Concept-index_cp_letter-A){.summary-letter}   [**B**](#Concept-index_cp_letter-B){.summary-letter}   [**C**](#Concept-index_cp_letter-C){.summary-letter}   [**D**](#Concept-index_cp_letter-D){.summary-letter}   [**E**](#Concept-index_cp_letter-E){.summary-letter}   [**F**](#Concept-index_cp_letter-F){.summary-letter}   [**G**](#Concept-index_cp_letter-G){.summary-letter}   [**I**](#Concept-index_cp_letter-I){.summary-letter}   [**K**](#Concept-index_cp_letter-K){.summary-letter}   [**L**](#Concept-index_cp_letter-L){.summary-letter}   [**M**](#Concept-index_cp_letter-M){.summary-letter}   [**N**](#Concept-index_cp_letter-N){.summary-letter}   [**O**](#Concept-index_cp_letter-O){.summary-letter}   [**P**](#Concept-index_cp_letter-P){.summary-letter}   [**Q**](#Concept-index_cp_letter-Q){.summary-letter}   [**R**](#Concept-index_cp_letter-R){.summary-letter}   [**S**](#Concept-index_cp_letter-S){.summary-letter}   [**T**](#Concept-index_cp_letter-T){.summary-letter}   [**U**](#Concept-index_cp_letter-U){.summary-letter}   [**V**](#Concept-index_cp_letter-V){.summary-letter}   [**W**](#Concept-index_cp_letter-W){.summary-letter}

---

Index Entry

Section

---

A

[Accessing builtin datasets](#index-Accessing-builtin-datasets):

[Accessing builtin datasets](#Accessing-builtin-datasets)

[Additive models](#index-Additive-models):

[Some non-standard models](#Some-non_002dstandard-models)

[Analysis of variance](#index-Analysis-of-variance):

[Analysis of variance and model comparison](#Analysis-of-variance-and-model-comparison)

[Arithmetic functions and operators](#index-Arithmetic-functions-and-operators):

[Vector arithmetic](#Vector-arithmetic)

[Arrays](#index-Arrays):

[Arrays](#Arrays)

[Assignment](#index-Assignment):

[Vectors and assignment](#Vectors-and-assignment)

[Attributes](#index-Attributes):

[Objects](#Objects)

---

B

[Binary operators](#index-Binary-operators):

[Defining new binary operators](#Defining-new-binary-operators)

[Box plots](#index-Box-plots):

[One- and two-sample tests](#One_002d-and-two_002dsample-tests)

---

C

[Character vectors](#index-Character-vectors):

[Character vectors](#Character-vectors)

[Classes](#index-Classes):

[The class of an object](#The-class-of-an-object)

[Classes](#index-Classes-1):

[Object orientation](#Object-orientation)

[Concatenating lists](#index-Concatenating-lists):

[Concatenating lists](#Concatenating-lists)

[Contrasts](#index-Contrasts):

[Contrasts](#Contrasts)

[Control statements](#index-Control-statements):

[Control statements](#Control-statements)

[CRAN](#index-CRAN):

[Contributed packages and CRAN](#Contributed-packages-and-CRAN)

[Customizing the environment](#index-Customizing-the-environment):

[Customizing the environment](#Customizing-the-environment)

---

D

[Data frames](#index-Data-frames):

[Data frames](#Data-frames)

[Default values](#index-Default-values):

[Named arguments and defaults](#Named-arguments-and-defaults)

[Density estimation](#index-Density-estimation):

[Examining the distribution of a set of data](#Examining-the-distribution-of-a-set-of-data)

[Determinants](#index-Determinants):

[Singular value decomposition and determinants](#Singular-value-decomposition-and-determinants)

[Diverting input and output](#index-Diverting-input-and-output):

[Executing commands from or diverting output to a file](#Executing-commands-from-or-diverting-output-to-a-file)

[Dynamic graphics](#index-Dynamic-graphics):

[Dynamic graphics](#Dynamic-graphics)

---

E

[Eigenvalues and eigenvectors](#index-Eigenvalues-and-eigenvectors):

[Eigenvalues and eigenvectors](#Eigenvalues-and-eigenvectors)

[Empirical CDFs](#index-Empirical-CDFs):

[Examining the distribution of a set of data](#Examining-the-distribution-of-a-set-of-data)

---

F

[Factors](#index-Factors):

[Factors](#Factors)

[Factors](#index-Factors-1):

[Contrasts](#Contrasts)

[Families](#index-Families):

[Families](#Families)

[Formulae](#index-Formulae):

[Formulae for statistical models](#Formulae-for-statistical-models)

---

G

[Generalized linear models](#index-Generalized-linear-models):

[Generalized linear models](#Generalized-linear-models)

[Generalized transpose of an array](#index-Generalized-transpose-of-an-array):

[Generalized transpose of an array](#Generalized-transpose-of-an-array)

[Generic functions](#index-Generic-functions):

[Object orientation](#Object-orientation)

[Graphics device drivers](#index-Graphics-device-drivers):

[Device drivers](#Device-drivers)

[Graphics parameters](#index-Graphics-parameters):

[The par() function](#The-par_0028_0029-function)

[Grouped expressions](#index-Grouped-expressions):

[Grouped expressions](#Grouped-expressions)

---

I

[Indexing of and by arrays](#index-Indexing-of-and-by-arrays):

[Array indexing](#Array-indexing)

[Indexing vectors](#index-Indexing-vectors):

[Index vectors](#Index-vectors)

---

K

[Kolmogorov-Smirnov test](#index-Kolmogorov_002dSmirnov-test):

[Examining the distribution of a set of data](#Examining-the-distribution-of-a-set-of-data)

---

L

[Least squares fitting](#index-Least-squares-fitting):

[Least squares fitting and the QR decomposition](#Least-squares-fitting-and-the-QR-decomposition)

[Linear equations](#index-Linear-equations):

[Linear equations and inversion](#Linear-equations-and-inversion)

[Linear models](#index-Linear-models):

[Linear models](#Linear-models)

[Lists](#index-Lists):

[Lists](#Lists)

[Local approximating regressions](#index-Local-approximating-regressions):

[Some non-standard models](#Some-non_002dstandard-models)

[Loops and conditional execution](#index-Loops-and-conditional-execution):

[Loops and conditional execution](#Loops-and-conditional-execution)

---

M

[Matrices](#index-Matrices):

[Arrays](#Arrays)

[Matrix multiplication](#index-Matrix-multiplication):

[Multiplication](#Multiplication)

[Maximum likelihood](#index-Maximum-likelihood):

[Maximum likelihood](#Maximum-likelihood)

[Missing values](#index-Missing-values):

[Missing values](#Missing-values)

[Mixed models](#index-Mixed-models):

[Some non-standard models](#Some-non_002dstandard-models)

---

N

[Named arguments](#index-Named-arguments):

[Named arguments and defaults](#Named-arguments-and-defaults)

[Namespace](#index-Namespace):

[Namespaces](#Namespaces)

[Nonlinear least squares](#index-Nonlinear-least-squares):

[Nonlinear least squares and maximum likelihood models](#Nonlinear-least-squares-and-maximum-likelihood-models)

---

O

[Object orientation](#index-Object-orientation):

[Object orientation](#Object-orientation)

[Objects](#index-Objects):

[Objects](#Objects)

[One- and two-sample tests](#index-One_002d-and-two_002dsample-tests):

[One- and two-sample tests](#One_002d-and-two_002dsample-tests)

[Ordered factors](#index-Ordered-factors):

[Factors](#Factors)

[Ordered factors](#index-Ordered-factors-1):

[Contrasts](#Contrasts)

[Outer products of arrays](#index-Outer-products-of-arrays):

[The outer product of two arrays](#The-outer-product-of-two-arrays)

---

P

[Packages](#index-Packages):

[R and statistics](#R-and-statistics)

[Packages](#index-Packages-1):

[Packages](#Packages)

[Probability distributions](#index-Probability-distributions):

[Probability distributions](#Probability-distributions)

---

Q

[QR decomposition](#index-QR-decomposition):

[Least squares fitting and the QR decomposition](#Least-squares-fitting-and-the-QR-decomposition)

[Quantile-quantile plots](#index-Quantile_002dquantile-plots):

[Examining the distribution of a set of data](#Examining-the-distribution-of-a-set-of-data)

---

R

[Reading data from files](#index-Reading-data-from-files):

[Reading data from files](#Reading-data-from-files)

[Recycling rule](#index-Recycling-rule):

[Vector arithmetic](#Vector-arithmetic)

[Recycling rule](#index-Recycling-rule-1):

[The recycling rule](#The-recycling-rule)

[Regular sequences](#index-Regular-sequences):

[Generating regular sequences](#Generating-regular-sequences)

[Removing objects](#index-Removing-objects):

[Data permanency and removing objects](#Data-permanency-and-removing-objects)

[Robust regression](#index-Robust-regression):

[Some non-standard models](#Some-non_002dstandard-models)

---

S

[Scope](#index-Scope):

[Scope](#Scope)

[Search path](#index-Search-path):

[Managing the search path](#Managing-the-search-path)

[Shapiro-Wilk test](#index-Shapiro_002dWilk-test):

[Examining the distribution of a set of data](#Examining-the-distribution-of-a-set-of-data)

[Singular value decomposition](#index-Singular-value-decomposition):

[Singular value decomposition and determinants](#Singular-value-decomposition-and-determinants)

[Statistical models](#index-Statistical-models):

[Statistical models in R](#Statistical-models-in-R)

[Student's _t_ test](#index-Student_0027s-t-test):

[One- and two-sample tests](#One_002d-and-two_002dsample-tests)

---

T

[Tabulation](#index-Tabulation):

[Frequency tables from factors](#Frequency-tables-from-factors)

[Tree-based models](#index-Tree_002dbased-models):

[Some non-standard models](#Some-non_002dstandard-models)

---

U

[Updating fitted models](#index-Updating-fitted-models):

[Updating fitted models](#Updating-fitted-models)

---

V

[Vectors](#index-Vectors):

[Simple manipulations numbers and vectors](#Simple-manipulations-numbers-and-vectors)

---

W

[Wilcoxon test](#index-Wilcoxon-test):

[One- and two-sample tests](#One_002d-and-two_002dsample-tests)

[Workspace](#index-Workspace):

[Data permanency and removing objects](#Data-permanency-and-removing-objects)

[Writing functions](#index-Writing-functions):

[Writing your own functions](#Writing-your-own-functions)

---

---

Jump to:   [**A**](#Concept-index_cp_letter-A){.summary-letter}   [**B**](#Concept-index_cp_letter-B){.summary-letter}   [**C**](#Concept-index_cp_letter-C){.summary-letter}   [**D**](#Concept-index_cp_letter-D){.summary-letter}   [**E**](#Concept-index_cp_letter-E){.summary-letter}   [**F**](#Concept-index_cp_letter-F){.summary-letter}   [**G**](#Concept-index_cp_letter-G){.summary-letter}   [**I**](#Concept-index_cp_letter-I){.summary-letter}   [**K**](#Concept-index_cp_letter-K){.summary-letter}   [**L**](#Concept-index_cp_letter-L){.summary-letter}   [**M**](#Concept-index_cp_letter-M){.summary-letter}   [**N**](#Concept-index_cp_letter-N){.summary-letter}   [**O**](#Concept-index_cp_letter-O){.summary-letter}   [**P**](#Concept-index_cp_letter-P){.summary-letter}   [**Q**](#Concept-index_cp_letter-Q){.summary-letter}   [**R**](#Concept-index_cp_letter-R){.summary-letter}   [**S**](#Concept-index_cp_letter-S){.summary-letter}   [**T**](#Concept-index_cp_letter-T){.summary-letter}   [**U**](#Concept-index_cp_letter-U){.summary-letter}   [**V**](#Concept-index_cp_letter-V){.summary-letter}   [**W**](#Concept-index_cp_letter-W){.summary-letter}

---

---

## Appendix F References

D. M. Bates and D. G. Watts (1988), _Nonlinear Regression Analysis and
Its Applications._ John Wiley & Sons, New York.

Richard A. Becker, John M. Chambers and Allan R. Wilks (1988), _The New
S Language._ Chapman & Hall, New York. This book is often called the
"_Blue Book_".

John M. Chambers and Trevor J. Hastie eds. (1992), _Statistical Models
in S._ Chapman & Hall, New York. This is also called the "_White Book_".

John M. Chambers (1998) _Programming with Data_. Springer, New York.
This is also called the "_Green Book_".

A. C. Davison and D. V. Hinkley (1997), _Bootstrap Methods and Their
Applications_, Cambridge University Press.

Annette J. Dobson (1990), _An Introduction to Generalized Linear
Models_, Chapman and Hall, London.

Peter McCullagh and John A. Nelder (1989), _Generalized Linear Models._
Second edition, Chapman and Hall, London.

John A. Rice (1995), _Mathematical Statistics and Data Analysis._ Second
edition. Duxbury Press, Belmont, CA.

S. D. Silvey (1970), _Statistical Inference._ Penguin, London.

---

#### Footnotes

[(1)](#DOCF1)

ACM Software Systems award, 1998:
<https://awards.acm.org/award_winners/chambers_6640862.cfm>.

[(2)](#DOCF2)

For portable R code (including that to be used in R packages) only
A--Za--z0--9 should be used.

[(3)](#DOCF3)

**not** inside strings, nor within the argument list of a function
definition

[(4)](#DOCF4)

some of the consoles will not allow you to enter more, and amongst those
which do some will silently discard the excess and some will use it as
the start of the next line.

[(5)](#DOCF5)

of unlimited length.

[(6)](#DOCF6)

The leading "dot" in this file name makes it _invisible_ in normal file
listings in UNIX, and in default GUI file listings on macOS and Windows.

[(7)](#DOCF7)

With other than vector types of argument, such as `list` mode arguments,
the action of `c()` is rather different. See [Concatenating lists](#Concatenating-lists).

[(8)](#DOCF8)

Actually, it is still available as `.Last.value` before any other
statements are executed.

[(9)](#DOCF9)

`paste(..., collapse=ss)` joins the arguments into a single character
string putting `ss`{.variable} in between, e.g., `ss <- "|"`. There are
more tools for character manipulation, see the help for `sub` and
`substring`.

[(10)](#DOCF10)

_numeric_ mode is actually an amalgam of two distinct modes, namely
_integer_ and _double_ precision, as explained in the manual.

[(11)](#DOCF11)

Note however that `length(object)` does not always contain intrinsic
useful information, e.g., when `object` is a function.

[(12)](#DOCF12)

In general, coercion from numeric to character and back again will not
be exactly reversible, because of roundoff errors in the character
representation.

[(13)](#DOCF13)

A different style using 'formal' or 'S4' classes is provided in package
`methods`.

[(14)](#DOCF14)

Readers should note that there are eight states and territories in
Australia, namely the Australian Capital Territory, New South Wales, the
Northern Territory, Queensland, South Australia, Tasmania, Victoria and
Western Australia.

[(15)](#DOCF15)

Note that `tapply()` also works in this case when its second argument is
not a factor, e.g., '`tapply(incomes, state)`', and this is
true for quite a few other functions, since arguments are _coerced_ to
factors when necessary (using `as.factor()`).

[(16)](#DOCF16)

Note that `x %*% x` is ambiguous, as it could mean either x'x or x x',
where x is the column form. In such cases the smaller matrix seems
implicitly to be the interpretation adopted, so the scalar x'x is in
this case the result. The matrix x x' may be calculated either by
`cbind(x) %*% x` or `x %*% rbind(x)` since the result of `rbind()` or
`cbind()` is always a matrix. However, the best way to compute x'x or x
x' is `crossprod(x)` or `x %o% x` respectively.

[(17)](#DOCF17)

Even better would be to form a matrix square root B with A = BB' and
find the squared length of the solution of By = x , perhaps using the
Cholesky or eigen decomposition of A.

[(18)](#DOCF18)

Conversion of character columns to factors is overridden using the
`stringsAsFactors` argument to the `data.frame()` function.

[(19)](#DOCF19)

See the on-line help for `autoload` for the meaning of the second term.

[(20)](#DOCF20)

Under UNIX, the utilities `sed` or`awk` can be used.

[(21)](#DOCF21)

to be discussed later, or use `xyplot` from package
[**lattice**](https://CRAN.R-project.org/package=lattice).

[(22)](#DOCF22)

See also the methods described in [Statistical models in R](#Statistical-models-in-R)

[(23)](#DOCF23)

In some sense this mimics the behavior in [S-PLUS]{.small} since in
[S-PLUS]{.small} this operator always creates or assigns to a global
variable.

[(24)](#DOCF24)

So it is hidden under UNIX.

[(25)](#DOCF25)

Some graphics parameters such as the size of the current device are for
information only.

[(26)](#DOCF26)

2.5Gb on versions of Windows that support 3Gb per process and have the
support enabled: see the `rw-FAQ` Q2.9; 3.5Gb on most 64-bit
versions of Windows.

[(27)](#DOCF27)

The 'Emacs Speaks Statistics' package; see the URL
<https://ESS.R-project.org/>

[(28)](#DOCF28)

It is possible to build R using an emulation of GNU **readline**, such
as one based on NetBSD's **editline**, it which case only a subset of
the capabilities may be provided.

[(29)](#DOCF29)

On a PC keyboard this is usually the Alt key, occasionally the 'Windows'
key. On a Mac keyboard normally no meta key is available.

[(30)](#DOCF30)

In particular, not versions 6.3 or later: this is worked around as from
R 3.4.0.

---
