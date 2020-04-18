6 R and Emacs

---

---

• [Is there Emacs support for R?](#Is-there-Emacs-support-for-R_003f)     
 • [Should I run R from within Emacs?](#Should-I-run-R-from-within-Emacs_003f)     
 • [Debugging R from within Emacs](#Debugging-R-from-within-Emacs)

---

---

### 6.1 Is there Emacs support for R?

There is an Emacs package called ESS ("Emacs Speaks Statistics") which
provides a standard interface between statistical programs and
statistical processes. It is intended to provide assistance for
interactive statistical programming and data analysis. Languages
supported include: S dialects (R, S 3/4, and [S-PLUS]{.small}
3.x/4.x/5.x/6.x/7.x), LispStat dialects (XLispStat, ViSta), SAS, Stata,
and BUGS.

ESS grew out of the need for bug fixes and extensions to S-mode 4.8
(which was a GNU Emacs interface to S/[S-PLUS]{.small} version 3 only).
The current set of developers desired support for XEmacs, R, S4, and MS
Windows. In addition, with new modes being developed for R, Stata, and
SAS, it was felt that a unifying interface and framework for the user
interface would benefit both the user and the developer, by helping both
groups conform to standard Emacs usage. The end result is an increase in
efficiency for statistical programming and data analysis, over the usual
tools.

R support contains code for editing R source code (syntactic indentation
and highlighting of source code, partial evaluations of code, loading
and error-checking of code, and source code revision maintenance) and
documentation (syntactic indentation and highlighting of source code,
sending examples to running ESS process, and previewing), interacting
with an inferior R process from within Emacs (command-line editing,
searchable command history, command-line completion of R object and file
names, quick access to object and search lists, transcript recording,
and an interface to the help system), and transcript manipulation
(recording and saving transcript files, manipulating and editing saved
transcripts, and re-evaluating commands from transcript files).

The latest stable version of ESS is available via CRAN or the [ESS web page](https://ESS.R-project.org/).

ESS comes with detailed installation instructions.

For help with ESS, send email to <ESS-help@r-project.org>.

Please send bug reports and suggestions on ESS to
<ESS-bugs@r-project.org>. The easiest way to do this from is within
Emacs by typing [M-x ess-submit-bug-report]{.kbd} or using the \[ESS\]
or \[iESS\] pulldown menus.

---

### 6.2 Should I run R from within Emacs?

Yes, _definitely_. Inferior R mode provides a readline/history
mechanism, object name completion, and syntax-based highlighting of the
interaction buffer using Font Lock mode, as well as a very convenient
interface to the R help system.

Of course, it also integrates nicely with the mechanisms for editing R
source using Emacs. One can write code in one Emacs buffer and send
whole or parts of it for execution to R; this is helpful for both data
analysis and programming. One can also seamlessly integrate with a
revision control system, in order to maintain a log of changes in your
programs and data, as well as to allow for the retrieval of past
versions of the code.

In addition, it allows you to keep a record of your session, which can
also be used for error recovery through the use of the transcript mode.

To specify command line arguments for the inferior R process, use [C-u
M-x R]{.kbd} for starting R.

---

### 6.3 Debugging R from within Emacs

To debug R "from within Emacs", there are several possibilities. To use
the Emacs GUD (Grand Unified Debugger) library with the recommended
debugger GDB, type [M-x gdb]{.kbd} and give the path to the R _binary_
as argument. At the `gdb` prompt, set `R_HOME` and other environment
variables as needed (using e.g. [set env R\_HOME /path/to/R/]{.kbd}, but
see also below), and start the binary with the desired arguments (e.g.,
[run \--quiet]{.kbd}).

If you have ESS, you can do [C-u M-x R [RET]{.key} - d [SPC]{.key} g d b
[RET]{.key}]{.kbd} to start an inferior R process with arguments
`-d gdb`.

A third option is to start an inferior R process via ESS ([M-x R]{.kbd})
and then start GUD ([M-x gdb]{.kbd}) giving the R binary (using its full
path name) as the program to debug. Use the program `ps` to find the
process number of the currently running R process then use the `attach`
command in gdb to attach it to that process. One advantage of this
method is that you have separate `*R*` and `*gud-gdb*` windows. Within
the `*R*` window you have all the ESS facilities, such as object-name
completion, that we know and love.

When using GUD mode for debugging from within Emacs, you may find it
most convenient to use the directory with your code in it as the current
working directory and then make a symbolic link from that directory to
the R binary. That way `.gdbinit` can stay in the directory
with the code and be used to set up the environment and the search paths
for the source, e.g. as follows:

```r
set env R_HOME /opt/R
set env R_PAPERSIZE letter
set env R_PRINTCMD lpr
dir /opt/R/src/appl
dir /opt/R/src/main
dir /opt/R/src/nmath
dir /opt/R/src/unix
```

---
