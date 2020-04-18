# 9 R Bugs

---

---

• [What is a bug?](#What-is-a-bug_003f)     
 • [How to report a bug](#How-to-report-a-bug)

---

---

### 9.1 What is a bug?

If R executes an illegal instruction, or dies with an operating system
error message that indicates a problem in the program (as opposed to
something like "disk full"), then it is certainly a bug. If you call
`.C()`, `.Fortran()`, `.External()` or `.Call()` (or `.Internal()`)
yourself (or in a function you wrote), you can always crash R by using
wrong argument types (modes). This is not a bug.

Taking forever to complete a command can be a bug, but you must make
certain that it was really R's fault. Some commands simply take a long
time. If the input was such that you _know_ it should have been
processed quickly, report a bug. If you don't know whether the command
should take a long time, find out by looking in the manual or by asking
for assistance.

If a command you are familiar with causes an R error message in a case
where its usual definition ought to be reasonable, it is probably a bug.
If a command does the wrong thing, that is a bug. But be sure you know
for certain what it ought to have done. If you aren't familiar with the
command, or don't know for certain how the command is supposed to work,
then it might actually be working right. For example, people sometimes
think there is a bug in R's mathematics because they don't understand
how finite-precision arithmetic works. Rather than jumping to
conclusions, show the problem to someone who knows for certain.
Unexpected results of comparison of decimal numbers, for example
`0.28 * 100 != 28` or `0.1 + 0.2 != 0.3`, are not a bug. See [Why
doesn\'t R think these numbers are
equal?](#Why-doesn_0027t-R-think-these-numbers-are-equal_003f), for more
details.

Finally, a command's intended definition may not be best for statistical
analysis. This is a very important sort of problem, but it is also a
matter of judgment. Also, it is easy to come to such a conclusion out of
ignorance of some of the existing features. It is probably best not to
complain about such a problem until you have checked the documentation
in the usual ways, feel confident that you understand it, and know for
certain that what you want is not available. If you are not sure what
the command is supposed to do after a careful reading of the manual this
indicates a bug in the manual. The manual's job is to make everything
clear. It is just as important to report documentation bugs as program
bugs. However, we know that the introductory documentation is seriously
inadequate, so you don't need to report this.

If the online argument list of a function disagrees with the manual, one
of them must be wrong, so report the bug.

---

### 9.2 How to report a bug

When you decide that there is a bug, it is important to report it and to
report it in a way which is useful. What is most useful is an exact
description of what commands you type, starting with the shell command
to run R, until the problem happens. Always include the version of R,
machine, and operating system that you are using; type [version]
in R to print this.

The most important principle in reporting a bug is to report _facts_,
not hypotheses or categorizations. It is always easier to report the
facts, but people seem to prefer to strain to posit explanations and
report them instead. If the explanations are based on guesses about how
R is implemented, they will be useless; others will have to try to
figure out what the facts must have been to lead to such speculations.
Sometimes this is impossible. But in any case, it is unnecessary work
for the ones trying to fix the problem.

For example, suppose that on a data set which you know to be quite large
the command

```r
R> data.frame(x, y, z, monday, tuesday)
```

never returns. Do not report that `data.frame()` fails for large data
sets. Perhaps it fails when a variable name is a day of the week. If
this is so then when others got your report they would try out the
`data.frame()` command on a large data set, probably with no day of the
week variable name, and not see any problem. There is no way in the
world that others could guess that they should try a day of the week
variable name.

Or perhaps the command fails because the last command you used was a
method for `"["()` that had a bug causing R's internal data structures
to be corrupted and making the `data.frame()` command fail from then on.
This is why others need to know what other commands you have typed (or
read from your startup file).

It is very useful to try and find simple examples that produce
apparently the same bug, and somewhat useful to find simple examples
that might be expected to produce the bug but actually do not. If you
want to debug the problem and find exactly what caused it, that is
wonderful. You should still report the facts as well as any explanations
or solutions. Please include an example that reproduces (e.g.,
<https://en.wikipedia.org/wiki/Reproducibility>) the problem, preferably
the simplest one you have found.

Invoking R with the `--vanilla` option may help in isolating a
bug. This ensures that the site profile and saved data files are not
read.

Before you actually submit a bug report, you should check whether the
bug has already been reported and/or fixed. First, try the "Show open
bugs new-to-old" or the search facility on
<https://bugs.R-project.org/>. Second, consult
<https://svn.R-project.org/R/trunk/doc/NEWS.Rd>, which records changes
that will appear in the _next_ release of R, including bug fixes that do
not appear on the Bug Tracker. Third, if possible try the current
r-patched or r-devel version of R. If a bug has already been reported or
fixed, please do not submit further bug reports on it. Finally, check
carefully whether the bug is with R, or a contributed package. Bug
reports on contributed packages should be sent first to the package
maintainer, and only submitted to the R-bugs repository by package
maintainers, mentioning the package in the subject line.

A bug report can be generated using the function `bug.report()`. For
reports on R this will open the Web page at
<https://bugs.R-project.org/>: for a contributed package it will open
the package's bug tracker Web page or help you compose an email to the
maintainer.

There is a section of the bug repository for suggestions for
enhancements for R labelled '`wishlist`'. Suggestions can be
submitted in the same ways as bugs, but please ensure that the subject
line makes clear that this is for the wishlist and not a bug report, for
example by starting with '`Wishlist:`'.

Comments on and suggestions for the Windows port of R should be sent to
<R-windows@R-project.org>.

Corrections to and comments on message translations should be sent to
the last translator (listed at the top of the appropriate
'`.po`' file) or to the translation team as listed at
<https://developer.R-project.org/TranslationTeams.html>.

---
