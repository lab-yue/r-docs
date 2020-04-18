# 5 Running R

---

How to start R and what command-line options are available is discussed
in [Invoking R](./R-intro.html#Invoking-R) in An Introduction to R.

You should ensure that the shell has set adequate resource limits: R
expects a stack size of at least 8MB and to be able to open at least 256
file descriptors. (Any modern OS should have default limits at least as
large as these, but apparently NetBSD may not. Use the shell command
`ulimit` (`sh`/`bash`) or `limit` (`csh`/`tcsh`) to check.) For some
compilers[^23^](#FOOT23) and packages a larger stack size has
been needed: 20-25MB has sufficed to date.

R makes use of a number of environment variables, the default values of
many of which are set in file `R_HOME/etc/Renviron` (there are
none set by default on Windows and hence no such file). These are set at
`configure` time, and you would not normally want to
change them -- a possible exception is
`R_PAPERSIZE` (see [Setting paper size](#Setting-paper-size)). The paper
size will be deduced from the '`LC_PAPER`' locale category if
it exists and `R_PAPERSIZE` is unset, and this will normally produce the
right choice from '`a4`' and '`letter`' on modern
Unix-alikes (but can always be overridden by setting `R_PAPERSIZE`).

Various environment variables can be set to determine where R creates
its per-session temporary directory. The environment variables
`TMPDIR`, `TMP` and
`TEMP` are searched in turn and the first one which is set and points to
a writable area is used. If none do, the final default is
`/tmp` on Unix-alikes and the value of
`R_USER` on Windows. The path should be an absolute path not containing
spaces (and it is best to avoid non-alphanumeric characters such as
`+`).

Some Unix-alike systems are set up to remove files and directories
periodically from `/tmp`, for example by a `cron` job
running `tmpwatch`. Set `TMPDIR` to another
directory before starting long-running jobs on such a system.

Note that `TMPDIR` will be used to execute `configure` scripts when
installing packages, so if `/tmp` has been mounted as
'`noexec`', `TMPDIR` needs to be set to a directory from which
execution is allowed.

---
