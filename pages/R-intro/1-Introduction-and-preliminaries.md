1 Introduction and preliminaries

---

---

• [The R environment](#The-R-environment)     
 • [Related software and documentation](#Related-software-and-documentation)     
 • [R and statistics](#R-and-statistics)     
 • [R and the window system](#R-and-the-window-system)     
 • [Using R interactively](#Using-R-interactively)     
 • [Getting help](#Getting-help)     
 • [R commands; case sensitivity etc](#R-commands_003b-case-sensitivity-etc)     
 • [Recall and correction of previous commands](#Recall-and-correction-of-previous-commands)     
 • [Executing commands from or diverting output to a file](#Executing-commands-from-or-diverting-output-to-a-file)     
 • [Data permanency and removing objects](#Data-permanency-and-removing-objects)

---

---

### 1.1 The R environment

R is an integrated suite of software facilities for data manipulation,
calculation and graphical display. Among other things it has

- an effective data handling and storage facility,
- a suite of operators for calculations on arrays, in particular
  matrices,
- a large, coherent, integrated collection of intermediate tools for
  data analysis,
- graphical facilities for data analysis and display either directly
  at the computer or on hardcopy, and
- a well developed, simple and effective programming language (called
  'S') which includes conditionals, loops, user defined recursive
  functions and input and output facilities. (Indeed most of the
  system supplied functions are themselves written in the S language.)

The term "environment" is intended to characterize it as a fully planned
and coherent system, rather than an incremental accretion of very
specific and inflexible tools, as is frequently the case with other data
analysis software.

R is very much a vehicle for newly developing methods of interactive
data analysis. It has developed rapidly, and has been extended by a
large collection of _packages_. However, most programs written in R are
essentially ephemeral, written for a single piece of data analysis.

---

### 1.2 Related software and documentation

R can be regarded as an implementation of the S language which was
developed at Bell Laboratories by Rick Becker, John Chambers and Allan
Wilks, and also forms the basis of the [S-PLUS]{.small} systems.

The evolution of the S language is characterized by four books by John
Chambers and coauthors. For R, the basic reference is _The New S
Language: A Programming Environment for Data Analysis and Graphics_ by
Richard A. Becker, John M. Chambers and Allan R. Wilks. The new features
of the 1991 release of S are covered in _Statistical Models in S_ edited
by John M. Chambers and Trevor J. Hastie. The formal methods and classes
of the **methods** package are based on those described in _Programming
with Data_ by John M. Chambers. See [References](#References), for
precise references.

There are now a number of books which describe how to use R for data
analysis and statistics, and documentation for S/[S-PLUS]{.small} can
typically be used with R, keeping the differences between the S
implementations in mind. See [What documentation exists for
R?](R-FAQ.html#What-documentation-exists-for-R_003f) in The R
statistical system FAQ.

---

### 1.3 R and statistics

Our introduction to the R environment did not mention _statistics_, yet
many people use R as a statistics system. We prefer to think of it of an
environment within which many classical and modern statistical
techniques have been implemented. A few of these are built into the base
R environment, but many are supplied as _packages_. There are about 25
packages supplied with R (called "standard" and "recommended" packages)
and many more are available through the CRAN family of Internet sites
(via <https://CRAN.R-project.org>) and elsewhere. More details on
packages are given later (see [Packages](#Packages)).

Most classical statistics and much of the latest methodology is
available for use with R, but users may need to be prepared to do a
little work to find it.

There is an important difference in philosophy between S (and hence R)
and the other main statistical systems. In S a statistical analysis is
normally done as a series of steps, with intermediate results being
stored in objects. Thus whereas SAS and SPSS will give copious output
from a regression or discriminant analysis, R will give minimal output
and store the results in a fit object for subsequent interrogation by
further R functions.

---

### 1.4 R and the window system

The most convenient way to use R is at a graphics workstation running a
windowing system. This guide is aimed at users who have this facility.
In particular we will occasionally refer to the use of R on an X window
system although the vast bulk of what is said applies generally to any
implementation of the R environment.

Most users will find it necessary to interact directly with the
operating system on their computer from time to time. In this guide, we
mainly discuss interaction with the operating system on UNIX machines.
If you are running R under Windows or macOS you will need to make some
small adjustments.

Setting up a workstation to take full advantage of the customizable
features of R is a straightforward if somewhat tedious procedure, and
will not be considered further here. Users in difficulty should seek
local expert help.

---

### 1.5 Using R interactively

When you use the R program it issues a prompt when it expects input
commands. The default prompt is '`>`', which on UNIX might be
the same as the shell prompt, and so it may appear that nothing is
happening. However, as we shall see, it is easy to change to a different
R prompt if you wish. We will assume that the UNIX shell prompt is
'`$`'.

In using R under UNIX the suggested procedure for the first occasion is
as follows:

1.  Create a separate sub-directory, say `work`, to hold data
    files on which you will use R for this problem. This will be the
    working directory whenever you use R for this particular problem.

    ```r
    $ mkdir work
    $ cd work
    ```

2.  Start the R program with the command

    ```r
    $ R
    ```

3.  At this point R commands may be issued (see later).

4.  To quit the R program the command is

    ```r
    > q()
    ```

    At this point you will be asked whether you want to save the data
    from your R session. On some systems this will bring up a dialog
    box, and on others you will receive a text prompt to which you can
    respond [yes]{.kbd}, [no]{.kbd} or [cancel]{.kbd} (a single letter
    abbreviation will do) to save the data before quitting, quit without
    saving, or return to the R session. Data which is saved will be
    available in future R sessions.

Further R sessions are simple.

1.  Make `work` the working directory and start the program as
    before:

    ```r
    $ cd work
    $ R
    ```

2.  Use the R program, terminating with the `q()` command at the end of
    the session.

To use R under Windows the procedure to follow is basically the same.
Create a folder as the working directory, and set that in the
`Start In` field in your R shortcut. Then launch R by double
clicking on the icon.

### 1.6 An introductory session

Readers wishing to get a feel for R at a computer before proceeding are
strongly advised to work through the introductory session given in [A
sample session](#A-sample-session).

---

### 1.7 Getting help with functions and features

R has an inbuilt help facility similar to the `man` facility of UNIX. To
get more information on any specific named function, for example
`solve`, the command is

```r
> help(solve)
```

An alternative is

```r
> ?solve
```

For a feature specified by special characters, the argument must be
enclosed in double or single quotes, making it a "character string":
This is also necessary for a few words with syntactic meaning including
`if`, `for` and `function`.

```r
> help("[[")
```

Either form of quote mark may be used to escape the other, as in the
string `"It's important"`. Our convention is to use double quote marks
for preference.

On most R installations help is available in HTML format by running

```r
> help.start()
```

which will launch a Web browser that allows the help pages to be browsed
with hyperlinks. On UNIX, subsequent help requests are sent to the
HTML-based help system. The 'Search Engine and Keywords' link in the
page loaded by `help.start()` is particularly useful as it is contains a
high-level concept list which searches though available functions. It
can be a great way to get your bearings quickly and to understand the
breadth of what R has to offer.

The `help.search` command (alternatively `??`) allows searching for help
in various ways. For example,

```r
> ??solve
```

Try `?help.search` for details and more examples.

The examples on a help topic can normally be run by

```r
> example(topic)
```

Windows versions of R have other optional help systems: use

```r
> ?help
```

for further details.

---

### 1.8 R commands, case sensitivity, etc.

Technically R is an _expression language_ with a very simple syntax. It
is _case sensitive_ as are most UNIX based packages, so `A` and `a` are
different symbols and would refer to different variables. The set of
symbols which can be used in R names depends on the operating system and
country within which R is being run (technically on the _locale_ in
use). Normally all alphanumeric symbols are allowed[^2^](#FOOT2)
(and in some countries this includes accented letters) plus
'`.`' and '`_`', with the restriction that a name must
start with '`.`' or a letter, and if it starts with
'`.`' the second character must not be a digit. Names are
effectively unlimited in length.

Elementary commands consist of either _expressions_ or _assignments_. If
an expression is given as a command, it is evaluated, printed (unless
specifically made invisible), and the value is lost. An assignment also
evaluates an expression and passes the value to a variable but the
result is not automatically printed.

Commands are separated either by a semi-colon ('`;`'), or by a
newline. Elementary commands can be grouped together into one compound
expression by braces ('`{`' and '`}`'). _Comments_ can
be put almost[^3^](#FOOT3) anywhere, starting with a hashmark
('`#`'), everything to the end of the line is a comment.

If a command is not complete at the end of a line, R will give a
different prompt, by default

```r
+
```

on second and subsequent lines and continue to read input until the
command is syntactically complete. This prompt may be changed by the
user. We will generally omit the continuation prompt and indicate
continuation by simple indenting.

Command lines entered at the console are limited[^4^](#FOOT4) to
about 4095 bytes (not characters).

---

### 1.9 Recall and correction of previous commands

Under many versions of UNIX and on Windows, R provides a mechanism for
recalling and re-executing previous commands. The vertical arrow keys on
the keyboard can be used to scroll forward and backward through a
_command history_. Once a command is located in this way, the cursor can
be moved within the command using the horizontal arrow keys, and
characters can be removed with the `DEL`{.key} key or added with the
other keys. More details are provided later: see [The command-line editor](#The-command_002dline-editor).

The recall and editing capabilities under UNIX are highly customizable.
You can find out how to do this by reading the manual entry for the
**readline** library.

Alternatively, the Emacs text editor provides more general support
mechanisms (via ESS, _Emacs Speaks Statistics_) for working
interactively with R. See [R and Emacs](R-FAQ.html#R-and-Emacs) in The R
statistical system FAQ.

---

### 1.10 Executing commands from or diverting output to a file

If commands[^5^](#FOOT5) are stored in an external file, say
`commands.R` in the working directory `work`, they may
be executed at any time in an R session with the command

```r
> source("commands.R")
```

For Windows **Source** is also available on the **File** menu. The
function `sink`,

```r
> sink("record.lis")
```

will divert all subsequent output from the console to an external file,
`record.lis`. The command

```r
> sink()
```

restores it to the console once again.

---

### 1.11 Data permanency and removing objects

The entities that R creates and manipulates are known as _objects_.
These may be variables, arrays of numbers, character strings, functions,
or more general structures built from such components.

During an R session, objects are created and stored by name (we discuss
this process in the next section). The R command

```r
> objects()
```

(alternatively, `ls()`) can be used to display the names of (most of)
the objects which are currently stored within R. The collection of
objects currently stored is called the _workspace_.

To remove objects the function `rm` is available:

```r
> rm(x, y, z, ink, junk, temp, foo, bar)
```

All objects created during an R session can be stored permanently in a
file for use in future R sessions. At the end of each R session you are
given the opportunity to save all the currently available objects. If
you indicate that you want to do this, the objects are written to a file
called `.RData`[^6^](#FOOT6) in the current directory,
and the command lines used in the session are saved to a file called
`.Rhistory`.

When R is started at later time from the same directory it reloads the
workspace from this file. At the same time the associated commands
history is reloaded.

It is recommended that you should use separate working directories for
analyses conducted with R. It is quite common for objects with names `x`
and `y` to be created during an analysis. Names like this are often
meaningful in the context of a single analysis, but it can be quite hard
to decide what they might be when the several analyses have been
conducted in the same directory.

---
