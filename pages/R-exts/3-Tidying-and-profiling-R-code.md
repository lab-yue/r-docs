3 Tidying and profiling R code

---

---

• [Tidying R code](#Tidying-R-code)     
 • [Profiling R code for speed](#Profiling-R-code-for-speed)     
 • [Profiling R code for memory use](#Profiling-R-code-for-memory-use)     
 • [Profiling compiled code](#Profiling-compiled-code)

---

R code which is worth preserving in a package and perhaps making
available for others to use is worth documenting, tidying up and perhaps
optimizing. The last two of these activities are the subject of this
chapter.

---

### 3.1 Tidying R code

R treats function code loaded from packages and code entered by users
differently. By default code entered by users has the source code stored
internally, and when the function is listed, the original source is
reproduced. Loading code from a package (by default) discards the source
code, and the function listing is re-created from the parse tree of the
function.

Normally keeping the source code is a good idea, and in particular it
avoids comments being removed from the source. However, we can make use
of the ability to re-create a function listing from its parse tree to
produce a tidy version of the function, for example with consistent
indentation and spaces around operators. If the original source does not
follow the standard format this tidied version can be much easier to
read.

We can subvert the keeping of source in two ways.

1.  The option `keep.source` can be set to `FALSE` before the code is
    loaded into R.
2.  The stored source code can be removed by calling the
    `removeSource()` function, for example by

    ```r
    myfun <- removeSource(myfun)
    ```

In each case if we then list the function we will get the standard
layout.

Suppose we have a file of functions `myfuns.R` that we want to
tidy up. Create a file `tidy.R` containing

```r
source("myfuns.R", keep.source = FALSE)
dump(ls(all = TRUE), file = "new.myfuns.R")
```

and run R with this as the source file, for example by [R \--vanilla \<
tidy.R]{.kbd} or by pasting into an R session. Then the file
`new.myfuns.R` will contain the functions in alphabetical order
in the standard layout. Warning: comments in your functions will be
lost.

The standard format provides a good starting point for further tidying.
Although the deparsing cannot do so, we recommend the consistent use of
the preferred assignment operator '`<-`' (rather than
'`=`') for assignment. Many package authors use a version of
Emacs (on a Unix-alike or Windows) to edit R code, using the ESS\[S\]
mode of the ESS Emacs package. See [R coding standards](./R-ints.html#R-coding-standards) in R Internals for style
options within the ESS\[S\] mode recommended for the source code of R
itself.

---

### 3.2 Profiling R code for speed

It is possible to profile R code on Windows and
most[^111^](#FOOT111) Unix-alike versions of R.

The command `Rprof` is used to control profiling, and its help page can
be consulted for full details. Profiling works by recording at fixed
intervals[^112^](#FOOT112) (by default every 20 msecs) which
line in which R function is being used, and recording the results in a
file (default `Rprof.out` in the working directory). Then the
function `summaryRprof` or the command-line utility
`R CMD Rprof Rprof.out` can be used to summarize the activity.

As an example, consider the following code (from Venables & Ripley,
2002, pp. 225--6).

```r
library(MASS); library(boot)
storm.fm <- nls(Time ~ b*Viscosity/(Wt - c), stormer,
                start = c(b=30.401, c=2.2183))
st <- cbind(stormer, fit=fitted(storm.fm))
storm.bf <- function(rs, i) {
    st$Time <-  st$fit + rs[i]
    tmp <- nls(Time ~ (b * Viscosity)/(Wt - c), st,
               start = coef(storm.fm))
    tmp$m$getAllPars()
}
rs <- scale(resid(storm.fm), scale = FALSE) # remove the mean
Rprof("boot.out")
storm.boot <- boot(rs, storm.bf, R = 4999) # slow enough to profile
Rprof(NULL)
```

Having run this we can summarize the results by

```r
R CMD Rprof boot.out

Each sample represents 0.02 seconds.
Total run time: 22.52 seconds.

Total seconds: time spent in function and callees.
Self seconds: time spent in function alone.
```

```r

```

```r
   %       total       %        self
 total    seconds     self    seconds    name
 100.0     25.22       0.2      0.04     "boot"
  99.8     25.18       0.6      0.16     "statistic"
  96.3     24.30       4.0      1.02     "nls"
  33.9      8.56       2.2      0.56     "<Anonymous>"
  32.4      8.18       1.4      0.36     "eval"
  31.8      8.02       1.4      0.34     ".Call"
  28.6      7.22       0.0      0.00     "eval.parent"
  28.5      7.18       0.3      0.08     "model.frame"
  28.1      7.10       3.5      0.88     "model.frame.default"
  17.4      4.38       0.7      0.18     "sapply"
  15.0      3.78       3.2      0.80     "nlsModel"
  12.5      3.16       1.8      0.46     "lapply"
  12.3      3.10       2.7      0.68     "assign"
 ...
```

```r

```

```r
   %        self        %      total
  self    seconds     total   seconds    name
   5.7      1.44       7.5      1.88     "inherits"
   4.0      1.02      96.3     24.30     "nls"
   3.6      0.92       3.6      0.92     "$"
   3.5      0.88      28.1      7.10     "model.frame.default"
   3.2      0.80      15.0      3.78     "nlsModel"
   2.8      0.70       9.8      2.46     "qr.coef"
   2.7      0.68      12.3      3.10     "assign"
   2.5      0.64       2.5      0.64     ".Fortran"
   2.5      0.62       7.1      1.80     "qr.default"
   2.2      0.56      33.9      8.56     "<Anonymous>"
   2.1      0.54       5.9      1.48     "unlist"
   2.1      0.52       7.9      2.00     "FUN"
  ...
```

This often produces surprising results and can be used to identify
bottlenecks or pieces of R code that could benefit from being replaced
by compiled code.

Two warnings: profiling does impose a small performance penalty, and the
output files can be very large if long runs are profiled at the default
sampling interval.

Profiling short runs can sometimes give misleading results. R from time
to time performs _garbage collection_ to reclaim unused memory, and this
takes an appreciable amount of time which profiling will charge to
whichever function happens to provoke it. It may be useful to compare
profiling code immediately after a call to `gc()` with a profiling run
without a preceding call to `gc`.

More detailed analysis of the output can be achieved by the tools in the
CRAN packages
[**proftools**](https://CRAN.R-project.org/package=proftools) and
[**profr**](https://CRAN.R-project.org/package=profr): in particular
these allow call graphs to be studied.

---

### 3.3 Profiling R code for memory use

Measuring memory use in R code is useful either when the code takes more
memory than is conveniently available or when memory allocation and
copying of objects is responsible for slow code. There are three ways to
profile memory use over time in R code. All three require R to have been
compiled with `--enable-memory-profiling`, which is not the
default, but is currently used for the macOS and Windows binary
distributions. All can be misleading, for different reasons.

In understanding the memory profiles it is useful to know a little more
about R's memory allocation. Looking at the results of `gc()` shows a
division of memory into `Vcells` used to store the contents of vectors
and `Ncells` used to store everything else, including all the
administrative overhead for vectors such as type and length information.
In fact the vector contents are divided into two pools. Memory for small
vectors (by default 128 bytes or less) is obtained in large chunks and
then parcelled out by R; memory for larger vectors is obtained directly
from the operating system.

Some memory allocation is obvious in interpreted code, for example,

```r
y <- x + 1
```

allocates memory for a new vector `y`. Other memory allocation is less
obvious and occurs because `R` is forced to make good on its promise of
'call-by-value' argument passing. When an argument is passed to a
function it is not immediately copied. Copying occurs (if necessary)
only when the argument is modified. This can lead to surprising memory
use. For example, in the 'survey' package we have

```r
print.svycoxph <- function (x, ...)
{
    print(x$survey.design, varnames = FALSE, design.summaries = FALSE, ...)
    x$call <- x$printcall
    NextMethod()
}
```

It may not be obvious that the assignment to `x$call` will cause the
entire object `x` to be copied. This copying to preserve the
call-by-value illusion is usually done by the internal C function
`duplicate`.

The main reason that memory-use profiling is difficult is garbage
collection. Memory is allocated at well-defined times in an R program,
but is freed whenever the garbage collector happens to run.

---

• [Memory statistics from Rprof](#Memory-statistics-from-Rprof)     
 • [Tracking memory allocations](#Tracking-memory-allocations)     
 • [Tracing copies of an object](#Tracing-copies-of-an-object)

---

---

#### 3.3.1 Memory statistics from `Rprof`

The sampling profiler `Rprof` described in the previous section can be
given the option `memory.profiling=TRUE`. It then writes out the total R
memory allocation in small vectors, large vectors, and cons cells or
nodes at each sampling interval. It also writes out the number of calls
to the internal function `duplicate`, which is called to copy R objects.
`summaryRprof` provides summaries of this information. The main reason
that this can be misleading is that the memory use is attributed to the
function running at the end of the sampling interval. A second reason is
that garbage collection can make the amount of memory in use decrease,
so a function appears to use little memory. Running under `gctorture`
helps with both problems: it slows down the code to effectively increase
the sampling frequency and it makes each garbage collection release a
smaller amount of memory. Changing the memory limits with `mem.limits()`
may also be useful, to see how the code would run under different memory
conditions.

---

#### 3.3.2 Tracking memory allocations

The second method of memory profiling uses a memory-allocation profiler,
`Rprofmem()`, which writes out a stack trace to an output file every
time a large vector is allocated (with a user-specified threshold for
'large') or a new page of memory is allocated for the R heap. Summary
functions for this output are still being designed.

Running the example from the previous section with

```r
> Rprofmem("boot.memprof",threshold=1000)
> storm.boot <- boot(rs, storm.bf, R = 4999)
> Rprofmem(NULL)
```

shows that apart from some initial and final work in `boot` there are no
vector allocations over 1000 bytes.

---

#### 3.3.3 Tracing copies of an object

The third method of memory profiling involves tracing copies made of a
specific (presumably large) R object. Calling `tracemem` on an object
marks it so that a message is printed to standard output when the object
is copied _via_ `duplicate` or coercion to another type, or when a new
object of the same size is created in arithmetic operations. The main
reason that this can be misleading is that copying of subsets or
components of an object is not tracked. It may be helpful to use
`tracemem` on these components.

In the example above we can run `tracemem` on the data frame `st`

```r
> tracemem(st)
[1] "<0x9abd5e0>"
> storm.boot <- boot(rs, storm.bf, R = 4)
memtrace[0x9abd5e0->0x92a6d08]: statistic boot
memtrace[0x92a6d08->0x92a6d80]: $<-.data.frame $<- statistic boot
memtrace[0x92a6d80->0x92a6df8]: $<-.data.frame $<- statistic boot
memtrace[0x9abd5e0->0x9271318]: statistic boot
memtrace[0x9271318->0x9271390]: $<-.data.frame $<- statistic boot
memtrace[0x9271390->0x9271408]: $<-.data.frame $<- statistic boot
memtrace[0x9abd5e0->0x914f558]: statistic boot
memtrace[0x914f558->0x914f5f8]: $<-.data.frame $<- statistic boot
memtrace[0x914f5f8->0x914f670]: $<-.data.frame $<- statistic boot
memtrace[0x9abd5e0->0x972cbf0]: statistic boot
memtrace[0x972cbf0->0x972cc68]: $<-.data.frame $<- statistic boot
memtrace[0x972cc68->0x972cd08]: $<-.data.frame $<- statistic boot
memtrace[0x9abd5e0->0x98ead98]: statistic boot
memtrace[0x98ead98->0x98eae10]: $<-.data.frame $<- statistic boot
memtrace[0x98eae10->0x98eae88]: $<-.data.frame $<- statistic boot
```

The object is duplicated fifteen times, three times for each of the
`R+1` calls to `storm.bf`. This is surprising, since none of the
duplications happen inside `nls`. Stepping through `storm.bf` in the
debugger shows that all three happen in the line

```r
st$Time <- st$fit + rs[i]
```

Data frames are slower than matrices and this is an example of why.
Using `tracemem(st$Viscosity)` does not reveal any additional copying.

---

### 3.4 Profiling compiled code

Profiling compiled code is highly system-specific, but this section
contains some hints gleaned from various R users. Some methods need to
be different for a compiled executable and for dynamic/shared
libraries/objects as used by R packages. We know of no good way to
profile DLLs on Windows.

---

• [Linux](#Linux)     
 • [Solaris](#Solaris)     
 • [macOS](#macOS)

---

---

#### 3.4.1 Linux

Options include using `sprof` for a shared object, and `oprofile` (see
<http://oprofile.sourceforge.net/>) and `perf` (see
<https://perf.wiki.kernel.org/index.php/Tutorial>) for any executable or
shared object.

#### 3.4.1.1 sprof

You can select shared objects to be profiled with `sprof` by setting the
environment variable `LD_PROFILE`. For example

```r
% setenv LD_PROFILE /path/to/R_HOME/library/stats/libs/stats.so
R
... run the boot example
% sprof /path/to/R_HOME/library/stats/libs/stats.so \
  /var/tmp/path/to/R_HOME/library/stats/libs/stats.so.profile

Flat profile:

Each sample counts as 0.01 seconds.
  %   cumulative   self              self     total
 time   seconds   seconds    calls  us/call  us/call  name
 76.19      0.32     0.32        0     0.00           numeric_deriv
 16.67      0.39     0.07        0     0.00           nls_iter
  7.14      0.42     0.03        0     0.00           getListElement

rm /var/tmp/path/to/R_HOME/library/stats/libs/stats.so.profile
... to clean up ...
```

It is possible that root access is needed to create the directories used
for the profile data.

#### 3.4.1.2 oprofile and operf

The `oprofile` project has two modes of operation. In what is now called
'legacy' mode, it is uses a daemon to collect information on a process
(see below). Since version 0.9.8 (August 2012), the preferred mode is to
use `operf`, so we discuss that first. The modes differ in how the
profiling data is collected: it is analysed by tools such as `opreport`
and `oppannote` in both.

Here is an example on `x86_64` Linux using R 3.0.2. File
`pvec.R` contains the part of the examples from `pvec` in
package **parallel**:

```r
library(parallel)
N <- 1e6
dates <- sprintf('%04d-%02d-%02d', as.integer(2000+rnorm(N)),
                 as.integer(runif(N, 1, 12)), as.integer(runif(N, 1, 28)))
system.time(a <- as.POSIXct(dates, format = "%Y-%m-%d"))
```

with timings from the final step

```r
   user  system elapsed
  0.371   0.237   0.612
```

R-level profiling by `Rprof` shows

```r
                     self.time self.pct total.time total.pct
"strptime"                1.70    41.06       1.70     41.06
"as.POSIXct.POSIXlt"      1.40    33.82       1.42     34.30
"sprintf"                 0.74    17.87       0.98     23.67
...
```

so the conversion from character to `POSIXlt` takes most of the time.

This can be run under `operf` and analysed by

```r
operf R -f pvec.R
opreport
opreport -l /path/to/R_HOME/bin/exec/R
opannotate --source /path/to/R_HOME/bin/exec/R
## And for the system time
opreport -l /lib64/libc.so.6
```

The first report shows where (which library etc) the time was spent:

```r
CPU_CLK_UNHALT...|
  samples|      %|
------------------
   166761 99.9161 Rdev
        CPU_CLK_UNHALT...|
          samples|      %|
        ------------------
            70586 42.3276 no-vmlinux
            56963 34.1585 libc-2.16.so
            36922 22.1407 R
             1584  0.9499 stats.so
              624  0.3742 libm-2.16.so
...
```

The rest of the output is voluminous, and only extracts are shown below.

Most of the time within R is spent in

```r
samples  %        image name symbol name
10397    28.5123  R           R_gc_internal
5683     15.5848  R           do_sprintf
3036      8.3258  R           do_asPOSIXct
2427      6.6557  R           do_strptime
2421      6.6392  R           Rf_mkCharLenCE
1480      4.0587  R           w_strptime_internal
1202      3.2963  R           Rf_qnorm5
1165      3.1948  R           unif_rand
675       1.8511  R           mktime0
617       1.6920  R           makelt
617       1.6920  R           validate_tm
584       1.6015  R           day_of_the_week
...
```

`opannotate` shows that 31% of the time in R is spent in
`memory.c`, 21% in `datetime.c` and 7% in
`Rstrptime.h`. The analysis for `libc` showed that
calls to `wcsftime` dominated, so those calls were cached for R 3.0.3:
the time spent in `no-vmlinux` (the kernel) was reduced dramatically.

On platforms which support it, call graphs can be produced by
`opcontrol --callgraph` if collected _via_ `operf --callgraph`.

The profiling data is by default stored in sub-directory
`oprofile_data` of the current directory, which can be removed
at the end of the session.

Another example, from [**sm**](https://CRAN.R-project.org/package=sm)
version 2.2-5.4. The example for `sm.variogram` took a long time:

```r
system.time(example(sm.variogram))
...
   user  system elapsed
  5.543   3.202   8.785
```

including a lot of system time. Profiling just the slow part, the second
plot, showed

```r
  samples|      %|
------------------
   381845 99.9885 R
        CPU_CLK_UNHALT...|
          samples|      %|
        ------------------
           187484 49.0995 sm.so
           169627 44.4230 no-vmlinux
            12636  3.3092 libgfortran.so.3.0.0
             6455  1.6905 R
```

so the system time was almost all in the Linux kernel. It is possible to
dig deeper if you have a matching uncompressed kernel with debug symbols
to specify _via_ `--vmlinux`: we did not.

In 'legacy' mode `oprofile` works by running a daemon which collects
information. The daemon must be started as root, e.g.

```r
% su
% opcontrol --no-vmlinux
% (optional, some platforms) opcontrol --callgraph=5
% opcontrol --start
% exit
```

Then as a user

```r
% R
... run the boot example
% opcontrol --dump
% opreport -l /path/to/R_HOME/library/stats/libs/stats.so
...
samples  %        symbol name
1623     75.5939  anonymous symbol from section .plt
349      16.2552  numeric_deriv
113       5.2632  nls_iter
62        2.8878  getListElement
% opreport -l /path/to/R_HOME/bin/exec/R
...
samples  %        symbol name
76052    11.9912  Rf_eval
54670     8.6198  Rf_findVarInFrame3
37814     5.9622  Rf_allocVector
31489     4.9649  Rf_duplicate
28221     4.4496  Rf_protect
26485     4.1759  Rf_cons
23650     3.7289  Rf_matchArgs
21088     3.3250  Rf_findFun
19995     3.1526  findVarLocInFrame
14871     2.3447  Rf_evalList
13794     2.1749  R_Newhashpjw
13522     2.1320  R_gc_internal
...
```

Shutting down the profiler and clearing the records needs to be done as
root.

---

#### 3.4.2 Solaris

On 64-bit (only) Solaris, the standard profiling tool `gprof` collects
information from shared objects compiled with `-pg`.

---

#### 3.4.3 macOS

Developers have recommended `sample` (or `Sampler.app`, which is a GUI
version), `Shark` (in version of `Xcode` up to those for Snow Leopard),
and `Instruments` (part of `Xcode`, see
<https://developer.apple.com/library/content/documentation/DeveloperTools/Conceptual/InstrumentsUserGuide/index.html>).

---
