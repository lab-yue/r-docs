4 Debugging

---

This chapter covers the debugging of R extensions, starting with the
ways to get useful error information and moving on to how to deal with
errors that crash R. For those who prefer other styles there are
contributed packages such as
[**debug**](https://CRAN.R-project.org/package=debug) on CRAN (described
in an article in [R-News
3/3](https://CRAN.R-project.org/doc/Rnews/Rnews_2003-3.pdf)). (There are
notes from 2002 provided by Roger Peng at
<http://www.biostat.jhsph.edu/~rpeng/docs/R-debug-tools.pdf> which
provide complementary examples to those given here.)

---

• [Browsing](#Browsing)     
 • [Debugging R code](#Debugging-R-code)     
 • [Checking memory access](#Checking-memory-access)     
 • [Debugging compiled code](#Debugging-compiled-code)     
 • [Using Link-time Optimization](#Using-Link_002dtime-Optimization)

---

---

### 4.1 Browsing

Most of the R-level debugging facilities are based around the built-in
browser. This can be used directly by inserting a call to `browser()`
into the code of a function (for example, using `fix(my_function)` ).
When code execution reaches that point in the function, control returns
to the R console with a special prompt. For example

```r
> fix(summary.data.frame) ## insert browser() call after for() loop
> summary(women)
Called from: summary.data.frame(women)
Browse[1]> ls()
 [1] "digits" "i"      "lbs"    "lw"     "maxsum" "nm"     "nr"     "nv"
 [9] "object" "sms"    "z"
Browse[1]> maxsum
[1] 7
Browse[1]>
     height         weight
 Min.   :58.0   Min.   :115.0
 1st Qu.:61.5   1st Qu.:124.5
 Median :65.0   Median :135.0
 Mean   :65.0   Mean   :136.7
 3rd Qu.:68.5   3rd Qu.:148.0
 Max.   :72.0   Max.   :164.0
> rm(summary.data.frame)
```

At the browser prompt one can enter any R expression, so for example
`ls()` lists the objects in the current frame, and entering the name of
an object will[^113^](#FOOT113) print it. The following
commands are also accepted

- `n`

  Enter 'step-through' mode. In this mode, hitting return executes the
  next line of code (more precisely one line and any continuation
  lines). Typing `c` will continue to the end of the current context,
  e.g. to the end of the current loop or function.

- `c`

  In normal mode, this quits the browser and continues execution, and
  just return works in the same way. `cont` is a synonym.

- `where`

  This prints the call stack. For example

```r
> summary(women)
Called from: summary.data.frame(women)
Browse[1]> where
where 1: summary.data.frame(women)
where 2: summary(women)

Browse[1]>
```

- `Q`

  Quit both the browser and the current expression, and return to the
  top-level prompt.

Errors in code executed at the browser prompt will normally return
control to the browser prompt. Objects can be altered by assignment, and
will keep their changed values when the browser is exited. If really
necessary, objects can be assigned to the workspace from the browser
prompt (by using `<<-` if the name is not already in scope).

---

### 4.2 Debugging R code

Suppose your R program gives an error message. The first thing to find
out is what R was doing at the time of the error, and the most useful
tool is `traceback()`. We suggest that this is run whenever the cause of
the error is not immediately obvious. Daily, errors are reported to the
R mailing lists as being in some package when `traceback()` would show
that the error was being reported by some other package or base R. Here
is an example from the regression suite.

```r
> success <- c(13,12,11,14,14,11,13,11,12)
> failure <- c(0,0,0,0,0,0,0,2,2)
> resp <- cbind(success, failure)
> predictor <- c(0, 5^(0:7))
> glm(resp ~ 0+predictor, family = binomial(link="log"))
Error: no valid set of coefficients has been found: please supply starting values
> traceback()
3: stop("no valid set of coefficients has been found: please supply
         starting values", call. = FALSE)
2: glm.fit(x = X, y = Y, weights = weights, start = start, etastart = etastart,
       mustart = mustart, offset = offset, family = family, control = control,
       intercept = attr(mt, "intercept") > 0)
1: glm(resp ~ 0 + predictor, family = binomial(link ="log"))
```

The calls to the active frames are given in reverse order (starting with
the innermost). So we see the error message comes from an explicit check
in `glm.fit`. (`traceback()` shows you all the lines of the function
calls, which can be limited by setting `option`
`"deparse.max.lines"`.)

Sometimes the traceback will indicate that the error was detected inside
compiled code, for example (from `?nls`)

```r
Error in nls(y ~ a + b * x, start = list(a = 0.12345, b = 0.54321), trace = TRUE) :
        step factor 0.000488281 reduced below ‘minFactor’ of 0.000976563
>  traceback()
2: .Call(R_nls_iter, m, ctrl, trace)
1: nls(y ~ a + b * x, start = list(a = 0.12345, b = 0.54321), trace = TRUE)
```

This will be the case if the innermost call is to `.C`, `.Fortran`,
`.Call`, `.External` or `.Internal`, but as it is also possible for such
code to evaluate R expressions, this need not be the innermost call, as
in

```r
> traceback()
9: gm(a, b, x)
8: .Call(R_numeric_deriv, expr, theta, rho, dir)
7: numericDeriv(form[[3]], names(ind), env)
6: getRHS()
5: assign("rhs", getRHS(), envir = thisEnv)
4: assign("resid", .swts * (lhs - assign("rhs", getRHS(), envir = thisEnv)),
       envir = thisEnv)
3: function (newPars)
   {
       setPars(newPars)
       assign("resid", .swts * (lhs - assign("rhs", getRHS(), envir = thisEnv)),
           envir = thisEnv)
       assign("dev", sum(resid^2), envir = thisEnv)
       assign("QR", qr(.swts * attr(rhs, "gradient")), envir = thisEnv)
       return(QR$rank < min(dim(QR$qr)))
   }(c(-0.00760232418963883, 1.00119632515036))
2: .Call(R_nls_iter, m, ctrl, trace)
1: nls(yeps ~ gm(a, b, x), start = list(a = 0.12345, b = 0.54321))
```

Occasionally `traceback()` does not help, and this can be the case if S4
method dispatch is involved. Consider the following example

```r
> xyd <- new("xyloc", x=runif(20), y=runif(20))
Error in as.environment(pkg) : no item called "package:S4nswv"
on the search list
Error in initialize(value, ...) : S language method selection got
an error when called from internal dispatch for function ‘initialize’
> traceback()
2: initialize(value, ...)
1: new("xyloc", x = runif(20), y = runif(20))
```

which does not help much, as there is no call to `as.environment` in
`initialize` (and the note "called from internal dispatch" tells us so).
In this case we searched the R sources for the quoted call, which
occurred in only one place, `methods:::.asEnvironmentPackage`. So now we
knew where the error was occurring. (This was an unusually opaque
example.)

The error message

```r
evaluation nested too deeply: infinite recursion / options(expressions=)?
```

can be hard to handle with the default value (5000). Unless you know
that there actually is deep recursion going on, it can help to set
something like

```r
options(expressions=500)
```

and re-run the example showing the error.

Sometimes there is warning that clearly is the precursor to some later
error, but it is not obvious where it is coming from. Setting
`options(warn = 2)` (which turns warnings into errors) can help here.

Once we have located the error, we have some choices. One way to proceed
is to find out more about what was happening at the time of the crash by
looking a _post-mortem_ dump. To do so, set
`options(error=dump.frames)` and run the code again. Then invoke
`debugger()` and explore the dump. Continuing our example:

```r
> options(error = dump.frames)
> glm(resp ~ 0 + predictor, family = binomial(link ="log"))
Error: no valid set of coefficients has been found: please supply starting values
```

which is the same as before, but an object called `last.dump` has
appeared in the workspace. (Such objects can be large, so remove it when
it is no longer needed.) We can examine this at a later time by calling
the function `debugger`.

```r
> debugger()
Message:  Error: no valid set of coefficients has been found: please supply starting values
Available environments had calls:
1: glm(resp ~ 0 + predictor, family = binomial(link = "log"))
2: glm.fit(x = X, y = Y, weights = weights, start = start, etastart = etastart, mus
3: stop("no valid set of coefficients has been found: please supply starting values
Enter an environment number, or 0 to exit  Selection:
```

which gives the same sequence of calls as `traceback`, but in
outer-first order and with only the first line of the call, truncated to
the current width. However, we can now examine in more detail what was
happening at the time of the error. Selecting an environment opens the
browser in that frame. So we select the function call which spawned the
error message, and explore some of the variables (and execute two
function calls).

```r
Enter an environment number, or 0 to exit  Selection: 2
Browsing in the environment with call:
   glm.fit(x = X, y = Y, weights = weights, start = start, etas
Called from: debugger.look(ind)
Browse[1]> ls()
 [1] "aic"        "boundary"   "coefold"    "control"    "conv"
 [6] "dev"        "dev.resids" "devold"     "EMPTY"      "eta"
[11] "etastart"   "family"     "fit"        "good"       "intercept"
[16] "iter"       "linkinv"    "mu"         "mu.eta"     "mu.eta.val"
[21] "mustart"    "n"          "ngoodobs"   "nobs"       "nvars"
[26] "offset"     "start"      "valideta"   "validmu"    "variance"
[31] "varmu"      "w"          "weights"    "x"          "xnames"
[36] "y"          "ynames"     "z"
Browse[1]> eta
            1             2             3             4             5
 0.000000e+00 -2.235357e-06 -1.117679e-05 -5.588393e-05 -2.794197e-04
            6             7             8             9
-1.397098e-03 -6.985492e-03 -3.492746e-02 -1.746373e-01
Browse[1]> valideta(eta)
[1] TRUE
Browse[1]> mu
        1         2         3         4         5         6         7         8
1.0000000 0.9999978 0.9999888 0.9999441 0.9997206 0.9986039 0.9930389 0.9656755
        9
0.8397616
Browse[1]> validmu(mu)
[1] FALSE
Browse[1]> c
Available environments had calls:
1: glm(resp ~ 0 + predictor, family = binomial(link = "log"))
2: glm.fit(x = X, y = Y, weights = weights, start = start, etastart = etastart
3: stop("no valid set of coefficients has been found: please supply starting v

Enter an environment number, or 0 to exit  Selection: 0
> rm(last.dump)
```

Because `last.dump` can be looked at later or even in another R session,
post-mortem debugging is possible even for batch usage of R. We do need
to arrange for the dump to be saved: this can be done either using the
command-line flag `--save` to save the workspace at the end of
the run, or _via_ a setting such as

```r
> options(error = quote({dump.frames(to.file=TRUE); q()}))
```

See the help on `dump.frames` for further options and a worked example.

An alternative error action is to use the function `recover()`:

```r
> options(error = recover)
> glm(resp ~ 0 + predictor, family = binomial(link = "log"))
Error: no valid set of coefficients has been found: please supply starting values

Enter a frame number, or 0 to exit

1: glm(resp ~ 0 + predictor, family = binomial(link = "log"))
2: glm.fit(x = X, y = Y, weights = weights, start = start, etastart = etastart

Selection:
```

which is very similar to `dump.frames`. However, we can examine the
state of the program directly, without dumping and re-loading the dump.
As its help page says, `recover` can be routinely used as the error
action in place of `dump.calls` and `dump.frames`, since it behaves like
`dump.frames` in non-interactive use.

Post-mortem debugging is good for finding out exactly what went wrong,
but not necessarily why. An alternative approach is to take a closer
look at what was happening just before the error, and a good way to do
that is to use `debug`. This inserts a call to the browser at the
beginning of the function, starting in step-through mode. So in our
example we could use

```r
> debug(glm.fit)
> glm(resp ~ 0 + predictor, family = binomial(link ="log"))
debugging in: glm.fit(x = X, y = Y, weights = weights, start = start, etastart = etastart,
    mustart = mustart, offset = offset, family = family, control = control,
    intercept = attr(mt, "intercept") > 0)
debug: {
## lists the whole function
Browse[1]>
debug: x <- as.matrix(x)
...
Browse[1]> start
[1] -2.235357e-06
debug: eta <- drop(x %*% start)
Browse[1]> eta
            1             2             3             4             5
 0.000000e+00 -2.235357e-06 -1.117679e-05 -5.588393e-05 -2.794197e-04
            6             7             8             9
-1.397098e-03 -6.985492e-03 -3.492746e-02 -1.746373e-01
Browse[1]>
debug: mu <- linkinv(eta <- eta + offset)
Browse[1]> mu
        1         2         3         4         5         6         7         8
1.0000000 0.9999978 0.9999888 0.9999441 0.9997206 0.9986039 0.9930389 0.9656755
        9
0.8397616
```

(The prompt `Browse[1]>` indicates that this is the first level of
browsing: it is possible to step into another function that is itself
being debugged or contains a call to `browser()`.)

`debug` can be used for hidden functions and S3 methods by e.g.
`debug(stats:::predict.Arima)`. (It cannot be used for S4 methods, but
an alternative is given on the help page for `debug`.) Sometimes you
want to debug a function defined inside another function, e.g. the
function `arimafn` defined inside `arima`. To do so, set `debug` on the
outer function (here `arima`) and step through it until the inner
function has been defined. Then call `debug` on the inner function (and
use `c` to get out of step-through mode in the outer function).

To remove debugging of a function, call `undebug` with the argument

For your own functions, it may be as easy to use `fix` to insert
temporary code, but `trace` can help with functions in a namespace (as
can `fixInNamespace`). Alternatively, use `trace(,edit=TRUE)` to insert
code visually.

---

### 4.3 Checking memory access

Errors in memory allocation and reading/writing outside arrays are very
common causes of crashes (e.g., segfaults) on some machines. Often the
crash appears long after the invalid memory access: in particular damage
to the structures which R itself has allocated may only become apparent
at the next garbage collection (or even at later garbage collections
after objects have been deleted).

Note that memory access errors may be seen with LAPACK, BLAS, OpenMP and
Java-using packages: some at least of these seem to be intentional, and
some are related to passing characters to Fortran.

Some of these tools can detect mismatched allocation and deallocation.
C++ programmers should note that memory allocated by `new []` must be
freed by `delete []`, other uses of `new` by `delete`, and memory
allocated by `malloc`, `calloc` and `realloc` by `free`. Some platforms
will tolerate mismatches (perhaps with memory leaks) but others will
segfault.

---

• [Using gctorture](#Using-gctorture)     
 • [Using valgrind](#Using-valgrind)     
 • [Using Address Sanitizer](#Using-Address-Sanitizer)     
 • [Using Undefined Behaviour Sanitizer](#Using-Undefined-Behaviour-Sanitizer)     
 • [Other analyses with 'clang'](#Other-analyses-with-_0060clang_0027)     
 • [Using 'Dr. Memory'](#Using-_0060Dr_002e-Memory_0027)     
 • [Fortran array bounds checking](#Fortran-array-bounds-checking)

---

---

#### 4.3.1 Using gctorture

We can help to detect memory problems in R objects earlier by running
garbage collection as often as possible. This is achieved by
`gctorture(TRUE)`, which as described on its help page

> Provokes garbage collection on (nearly) every memory allocation.
> Intended to ferret out memory protection bugs. Also makes R run _very_
> slowly, unfortunately.

The reference to 'memory protection' is to missing C-level calls to
`PROTECT`/`UNPROTECT` (see [Garbage Collection](#Garbage-Collection))
which if missing allow R objects to be garbage-collected when they are
still in use. But it can also help with other memory-related errors.

Normally running under `gctorture(TRUE)` will just produce a crash
earlier in the R program, hopefully close to the actual cause. See the

#### 4.3.2 Using valgrind

If you have access to Linux on a common CPU type or supported versions
of macOS or Solaris you can use `valgrind` (<http://www.valgrind.org/>,
pronounced to rhyme with 'tinned') to check for possible problems. To
run some examples under `valgrind` use something like

```r
R -d valgrind --vanilla < mypkg-Ex.R
R -d "valgrind --tool=memcheck --leak-check=full" --vanilla < mypkg-Ex.R
```

where `mypkg-Ex.R` is a set of examples, e.g. the file created
in `mypkg.Rcheck` by `R CMD check`. Occasionally this reports
memory reads of 'uninitialised values' that are the result of compiler
optimization, so can be worth checking under an unoptimized compile: for
maximal information use a build with debugging symbols. We know there
will be some small memory leaks from `readline` and R itself --- these
are memory areas that are in use right up to the end of the R session.
Expect this to run around 20x slower than without `valgrind`, and in
some cases much slower than that. Several versions of `valgrind` were
not happy with some optimized BLASes that use CPU-specific instructions
so you may need to build a version of R specifically to use with
`valgrind`.

On platforms where `valgrind` is installed you can build a version of R
with extra instrumentation to help `valgrind` detect errors in the use
of memory allocated from the R heap. The `configure` option is
`--with-valgrind-instrumentation=level`, where
`level`{.variable} is 0, 1 or 2. Level 0 is the default and does not add
anything. Level 1 will detect some uses[^114^](#FOOT114) of
uninitialised memory and has little impact on speed (compared to level
0). Level 2 will detect many other memory-use
bugs[^115^](#FOOT115) but make R much slower when running
under `valgrind`. Using this in conjunction with `gctorture` can be even
more effective (and even slower).

An example of `valgrind` output is

```r
==12539== Invalid read of size 4
==12539==    at 0x1CDF6CBE: csc_compTr (Mutils.c:273)
==12539==    by 0x1CE07E1E: tsc_transpose (dtCMatrix.c:25)
==12539==    by 0x80A67A7: do_dotcall (dotcode.c:858)
==12539==    by 0x80CACE2: Rf_eval (eval.c:400)
==12539==    by 0x80CB5AF: R_execClosure (eval.c:658)
==12539==    by 0x80CB98E: R_execMethod (eval.c:760)
==12539==    by 0x1B93DEFA: R_standardGeneric (methods_list_dispatch.c:624)
==12539==    by 0x810262E: do_standardGeneric (objects.c:1012)
==12539==    by 0x80CAD23: Rf_eval (eval.c:403)
==12539==    by 0x80CB2F0: Rf_applyClosure (eval.c:573)
==12539==    by 0x80CADCC: Rf_eval (eval.c:414)
==12539==    by 0x80CAA03: Rf_eval (eval.c:362)
==12539==  Address 0x1C0D2EA8 is 280 bytes inside a block of size 1996 alloc'd
==12539==    at 0x1B9008D1: malloc (vg_replace_malloc.c:149)
==12539==    by 0x80F1B34: GetNewPage (memory.c:610)
==12539==    by 0x80F7515: Rf_allocVector (memory.c:1915)
...
```

This example is from an instrumented version of R, while tracking down a
bug in the [**Matrix**](https://CRAN.R-project.org/package=Matrix)
package in 2006. The first line indicates that R has tried to read 4
bytes from a memory address that it does not have access to. This is
followed by a C stack trace showing where the error occurred. Next is a
description of the memory that was accessed. It is inside a block
allocated by `malloc`, called from `GetNewPage`, that is, in the
internal R heap. Since this memory all belongs to R, `valgrind` would
not (and did not) detect the problem in an uninstrumented build of R. In
this example the stack trace was enough to isolate and fix the bug,
which was in `tsc_transpose`, and in this example running under
`gctorture()` did not provide any additional information.

`valgrind` is good at spotting the use of uninitialized values: use
option `--track-origins=yes` to show where these originated
from. What it cannot detect is the misuse of arrays allocated on the
stack: this includes C automatic variables and
some[^116^](#FOOT116) Fortran arrays.

It is possible to run all the examples, tests and vignettes covered by
`R CMD check` under `valgrind` by using the option
`--use-valgrind`. If you do this you will need to select the
`valgrind` options some other way, for example by having a
`~/.valgrindrc` file containing

```r
--leak-check=full
--track-origins=yes
```

or setting the environment variable `VALGRIND_OPTS`.

On macOS you may need to ensure that debugging symbols are made
available (so `valgrind` reports line numbers in files). This can
usually be done with the `valgrind` option `--dsymutil=yes` to
ask for the symbols to be dumped when the `.so` file is loaded.
This will not work where packages are installed into a system area (such
as the `R.framework`) and can be slow. Installing packages with
`R CMD INSTALL --dsym` installs the dumped symbols. (This can also be
done by setting environment variable `PKG_MAKE_DSYM` to a non-empty
value before the `INSTALL`.)

This section has described the use of `memtest`, the default (and most
useful) of `valgrind`'s tools. There are others described in its
documentation: `helgrind` can be useful for threaded programs.

---

#### 4.3.3 Using the Address Sanitizer

`AddressSanitizer` ('ASan') is a tool with similar aims to the memory
checker in `valgrind`. It is available with suitable
builds[^117^](#FOOT117) of `gcc` and `clang` on common Linux
and macOS platforms. See
<https://clang.llvm.org/docs/UsersManual.html#controlling-code-generation>,
<https://clang.llvm.org/docs/AddressSanitizer.html> and
<https://code.google.com/p/address-sanitizer/>.

More thorough checks of C++ code are done if the C++ library has been
'annotated': at the time of writing this applied to `std::vector` in
`libc++` for use with `clang` and gives rise to
'`container-overflow`'[^118^](#FOOT118) reports.

It requires code to have been compiled _and linked_ with
`-fsanitize=address` and compiling with
`-fno-omit-frame-pointer` will give more legible reports. It has a
runtime penalty of 2--3x, extended compilation times and uses
substantially more memory, often 1--2GB, at run time. On 64-bit
platforms it reserves (but does not allocate) 16--20TB of virtual
memory: restrictive shell settings can cause problems.

By comparison with `valgrind`, ASan can detect misuse of stack and
global variables but not the use of uninitialized memory.

Recent versions return symbolic addresses for the location of the error
provided `llvm-symbolizer`[^119^](#FOOT119) is on the path: if
it is available but not on the path or has been
renamed[^120^](#FOOT120), one can use an environment variable,
e.g.

```r
ASAN_SYMBOLIZER_PATH=/path/to/llvm-symbolizer
```

An alternative is to pipe the output through
`asan_symbolize.py`[^121^](#FOOT121) and perhaps then (for
compiled C++ code) `c++filt`. (On macOS, you may need to run `dsymutil`
to get line-number reports.)

The simplest way to make use of this is to build a version of R with
something like

```r
CC="gcc -std=gnu99 -fsanitize=address"
CFLAGS="-fno-omit-frame-pointer -g -O2 -Wall -pedantic -mtune=native"
```

which will ensure that the `libasan` run-time library is compiled into
the R executable. However this check can be enabled on a per-package
basis by using a `~/.R/Makevars` file like

```r
CC = gcc -std=gnu99 -fsanitize=address -fno-omit-frame-pointer
CXX = g++ -fsanitize=address -fno-omit-frame-pointer
FC = gfortran -fsanitize=address
```

(Note that `-fsanitize=address` has to be part of the compiler
specification to ensure it is used for linking. These settings will not
be honoured by packages which ignore `~/.R/Makevars`.) It will
be necessary to build R with

```r
MAIN_LDFLAGS = -fsanitize=address
```

to link the runtime libraries into the R executable if it was not
specified as part of '`CC`' when R was built. (For some builds
without OpenMP, `-pthread` is also required.)

For options available _via_ the environment variable `ASAN_OPTIONS` see
<https://code.google.com/p/address-sanitizer/wiki/AddressSanitizerFLags>.
With `gcc` additional control is available _via_ the `--param`
flag: see its `man` page.

For more detailed information on an error, R can be run under a debugger
with a breakpoint set before the address sanitizer report is produced:
for `gdb` or `lldb` you could use

```r
break __asan_report_error
```

(See
<https://code.google.com/p/address-sanitizer/wiki/AddressSanitizer#gdb>.)

More recent versions[^122^](#FOOT122) added the flag
`-fsanitize-address-use-after-scope`: see
<https://github.com/google/sanitizers/wiki/AddressSanitizerUseAfterScope>.

One of the checks done by ASAN is that `malloc/free` and in C++
`new/delete` and `new[]/delete[]` are used consistently (rather than say
`free` being used to dealloc memory allocated by `new[]`). This matters
on some systems but not all: unfortunately on some of those where it
does not matter, system libraries[^123^](#FOOT123) are not
consistent. The check can be suppressed by including
'`alloc_dealloc_mismatch=0`' in `ASAN_OPTIONS`.

ASAN also checks system calls and sometimes reports can refer to
problems in the system software and not the package nor R. A couple of
reports have been of 'heap-use-after-free' errors in the X11 libraries
called from Tcl/Tk.

---

• [Using Leak Sanitizer](#Using-Leak-Sanitizer)

---

---

#### 4.3.3.1 Using the Leak Sanitizer

For `x86_64` Linux there is a leak sanitizer, 'LSan': see
<https://code.google.com/p/address-sanitizer/wiki/LeakSanitizer>. This
is available on recent versions of `gcc` and `clang`, and where
available is compiled in as part of ASan.

One way to invoke this from an ASan-enabled build is by the environment
variable

```r
ASAN_OPTIONS='detect_leaks=1'
```

However, this was made the default as from `clang` 3.5 and `gcc` 5.1.0.

When LSan is enabled, leaks give the process a failure error status (by
default `23`). For an R package this means the R process, and as the
parser retains some memory to the end of the process, if R itself was
built against ASan, all runs will have a failure error status (which may
include running R as part of building R itself).

To disable this, allocation-mismatch checking and some strict C++
checking use

```r
setenv ASAN_OPTIONS ‘alloc_dealloc_mismatch=0:detect_leaks=0:detect_odr_violation=0’
```

LSan also has a 'stand-alone' mode where it is compiled in using
`-fsanitize=leak` and avoids the run-time overhead of ASan.

---

#### 4.3.4 Using the Undefined Behaviour Sanitizer

'Undefined behaviour' is where the language standard does not require
particular behaviour from the compiler. Examples include division by
zero (where for doubles R requires the ISO/IEC 60559 behaviour but C/C++
do not), use of zero-length arrays, shifts too far for signed types
(e.g. `int x, y; y = x << 31;`), out-of-range coercion, invalid C++
casts and mis-alignment. Not uncommon examples of out-of-range coercion
in R packages are attempts to coerce a `NaN` or infinity to type `int`
or `NA_INTEGER` to an unsigned type such as `size_t`. Also common is
`y[x - 1]` forgetting that `x` might be `NA_INTEGER`.

'UBSanitizer' is a tool for C/C++ source code selected by
`-fsanitize=undefined` in suitable
builds[^124^](#FOOT124) of `clang` and GCC. Its (main) runtime
library is linked into each package's DLL, so it is less often needed to
be included in `MAIN_LDFLAGS`.

This sanitizer can be combined with the Address Sanitizer by
`-fsanitize=undefined,address` (where both are supported).

Finer control of what is checked can be achieved by other options.

For `clang` see
<https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html#ubsan-checks>.
The current set is (on a single line):

```r
-fsanitize=alignment,bool,bounds,builtin,enum,float-cast-overflow,
float-divide-by-zero,function,implicit-unsigned-integer-truncation,
implicit-signed-integer-truncation,implicit-integer-sign-change,
integer-divide-by-zero,nonnull-attribute,null,object-size,
pointer-overflow,return,returns-nonnull-attribute,shift,
signed-integer-overflow,unreachable,unsigned-integer-overflow,vla-bound,vptr
```

(plus the more specific versions `shift-base` and `shift-exponent`) a
subset of which could be combined with `address`, or use something like

```r
-fsanitize=undefined -fno-sanitize=float-divide-by-zero
```

Options `function`, `return` and `vptr` apply only to C++: to use `vptr`
its run-time library needs to be linked into the main R executable by
building the latter with something like

```r
MAIN_LD="clang++ -fsanitize=undefined"
```

Option `float-divide-by-zero` is undesirable for use with R which allow
such divisions as part of IEC 60559 arithmetic.

For GCC see
<https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html> (or
the manual for your version of GCC, installed or _via_
<https://gcc.gnu.org/onlinedocs/>: look for 'Program Instrumentation
Options') for the options supported by GCC: 6 and 7 supported

```r
-fsanitize=alignment,bool,bounds,enum,integer-divide-by-zero,
nonnull-attribute,null,object-size,return,returns-nonnull-attribute,
shift,signed-integer-overflow,unreachable,vla-bound,vptr
```

plus the more specific versions `shift-base` and `shift-exponent` and
non-default options

```r
bound-strict,float-cast-overflow,float-divide-by-zero
```

where `float-divide-by-zero` is not desirable for R uses and
`bounds-strict` is an extension of `bounds`. From GCC 8
`signed-integer-overflow` is no longer a default part of
`-fsanitize=undefined`, but can be specified separately. It
adds options `-fsanitize=pointer-overflow` and
`-fsanitize=builtin`.

Other useful flags include

```r
-no-fsanitize-recover
```

which causes the first report to be fatal (it always is for the
`unreachable` and `return` suboptions). For more detailed information on
where the runtime error occurs, using

```r
setenv UBSAN_OPTIONS ‘print_stacktrace=1’
```

will include a traceback in the report. Beyond that, R can be run under
a debugger with a breakpoint set before the sanitizer report is
produced: for `gdb` or `lldb` you could use

```r
break __ubsan_handle_float_cast_overflow
break __ubsan_handle_float_cast_overflow_abort
```

or similar (there are handlers for each type of undefined behaviour).

There are also the compiler flags `-fcatch-undefined-behavior`
and `-ftrapv`, said to be more reliable in `clang` than `gcc`.

For more details on the topic see <http://blog.regehr.org/archives/213>
and
<http://blog.llvm.org/2011/05/what-every-c-programmer-should-know.html>
(which has 3 parts).

It may or may not be possible to build R itself with
`-fsanitize=undefined`: when last tried it worked with `clang`
but there were problems with OpenMP-using code with `gcc`.

---

#### 4.3.5 Other analyses with 'clang'

Recent versions of `clang` on '`x86_64`' Linux have
'ThreadSanitizer' (<https://code.google.com/p/thread-sanitizer/>), a
'data race detector for C/C++ programs', and 'MemorySanitizer'
(<https://clang.llvm.org/docs/MemorySanitizer.html>,
<https://code.google.com/p/memory-sanitizer/wiki/MemorySanitizer>) for
the detection of uninitialized memory. Both are based on and provide
similar functionality to tools in `valgrind`.

`clang` has a 'Static Analyser' which can be run on the source files
during compilation: see <https://clang-analyzer.llvm.org/>.

---

#### 4.3.6 Using 'Dr. Memory'

'Dr. Memory' from <http://www.drmemory.org/> is a memory checker for
(currently) 32-bit Windows, Linux and macOS with similar aims to
`valgrind`. It works with unmodified
executables[^125^](#FOOT125) and detects memory access errors,
uninitialized reads and memory leaks.

---

#### 4.3.7 Fortran array bounds checking

Most of the Fortran compilers used with R allow code to be compiled with
checking of array bounds: for example `gfortran` has option
`-fbounds-check` and Oracle Developer Studio has `-C`.
This will give an error when the upper or lower bound is exceeded, e.g.

```r
At line 97 of file .../src/appl/dqrdc2.f
Fortran runtime error: Index ‘1’ of dimension 1 of array ‘x’ above upper bound of 0
```

One does need to be aware that lazy programmers often specify Fortran
dimensions as `1` rather than `*` or a real bound and these will be
reported (as may `*` dimensions)

It is easy to arrange to use this check on just the code in your
package: add to `~/.R/Makevars` something like (for `gfortran`)

```r
FFLAGS = -g -O2 -mtune=native -fbounds-check
```

when you run `R CMD check`.

This may report errors with the way that Fortran character variables are
passed, particularly when Fortran subroutines are called from C code and
character lengths are not passed (see [Fortran character strings](#Fortran-character-strings)).

---

### 4.4 Debugging compiled code

Sooner or later programmers will be faced with the need to debug
compiled code loaded into R. This section is geared to platforms using
`gdb` with code compiled by `gcc`, but similar things are possible with
other debuggers such as `lldb` (<http://lldb.llvm.org/>, used on macOS)
and Sun's `dbx`: some debuggers have graphical front-ends available.

Consider first 'crashes', that is when R terminated unexpectedly with an
illegal memory access (a 'segfault' or 'bus error'), illegal instruction
or similar. Unix-alike versions of R use a signal handler which aims to
give some basic information. For example

```r
 *** caught segfault ***
address 0x20000028, cause ‘memory not mapped’

Traceback:
 1: .identC(class1[[1]], class2)
 2: possibleExtends(class(sloti), classi, ClassDef2 = getClassDef(classi,
where = where))
 3: validObject(t(cu))
 4: stopifnot(validObject(cu <- as(tu, "dtCMatrix")), validObject(t(cu)),
validObject(t(tu)))

Possible actions:
1: abort (with core dump)
2: normal R exit
3: exit R without saving workspace
4: exit R saving workspace
Selection: 3
```

Since the R process may be damaged, the only really safe options are the
first or third. (Note that a core dump is only produced where enabled: a
common default in a shell is to limit its size to 0, thereby disabling
it.)

A fairly common cause of such crashes is a package which uses `.C` or
`.Fortran` and writes beyond (at either end) one of the arguments it is
passed. There is a good way to detect this: using
`options(CBoundsCheck = TRUE)` (which can be selected _via_ the
environment variable `R_C_BOUNDS_CHECK=yes)` changes the way `.C` and
`.Fortran` work to check if the compiled code writes in the 64 bytes at
either end of an argument.

Another cause of a 'crash' is to overrun the C stack. R tries to track
that in its own code, but it may happen in third-party compiled code.
For modern POSIX-compliant OSes R can safely catch that and return to
the top-level prompt, so one gets something like

```r
> .C("aaa")
Error: segfault from C stack overflow
>
```

However, C stack overflows are fatal under Windows and normally defeat
attempts at debugging on that platform. Further, the size of the stack
is set when R is compiled, whereas on POSIX OSes it can be set in the
shell from which R is launched.

If you have a crash which gives a core dump you can use something like

```r
gdb /path/to/R/bin/exec/R core.12345
```

to examine the core dump. If core dumps are disabled or to catch errors
that do not generate a dump one can run R directly under a debugger by
for example

```r
$ R -d gdb --vanilla
...
gdb> run
```

at which point R will run normally, and hopefully the debugger will
catch the error and return to its prompt. This can also be used to catch
infinite loops or interrupt very long-running code. For a simple example

```r
> for(i in 1:1e7) x <- rnorm(100)
[hit Ctrl-C]
Program received signal SIGINT, Interrupt.
0x00397682 in _int_free () from /lib/tls/libc.so.6
(gdb) where
#0  0x00397682 in _int_free () from /lib/tls/libc.so.6
#1  0x00397eba in free () from /lib/tls/libc.so.6
#2  0xb7cf2551 in R_gc_internal (size_needed=313)
    at /users/ripley/R/svn/R-devel/src/main/memory.c:743
#3  0xb7cf3617 in Rf_allocVector (type=13, length=626)
    at /users/ripley/R/svn/R-devel/src/main/memory.c:1906
#4  0xb7c3f6d3 in PutRNGstate ()
    at /users/ripley/R/svn/R-devel/src/main/RNG.c:351
#5  0xb7d6c0a5 in do_random2 (call=0x94bf7d4, op=0x92580e8, args=0x9698f98,
    rho=0x9698f28) at /users/ripley/R/svn/R-devel/src/main/random.c:183
...
```

In many cases it is possible to attach a debugger to a running process:
this is helpful if an alternative front-end is in use or to investigate
a task that seems to be taking far too long. This is done by something
like

```r
gdb -p pid
```

where `pid` is the id of the R executable or front-end. This stops the
process so its state can be examined: use `continue` to resume
execution.

Some "tricks" worth knowing follow:

---

• [Finding entry points](#Finding-entry-points)     
 • [Inspecting R objects](#Inspecting-R-objects)

---

---

#### 4.4.1 Finding entry points in dynamically loaded code

Under most compilation environments, compiled code dynamically loaded
into R cannot have breakpoints set within it until it is loaded. To use
a symbolic debugger on such dynamically loaded code under Unix-alikes
use

- Call the debugger on the R executable, for example by [R -d
  gdb]{.kbd}.
- Start R.
- At the R prompt, use `dyn.load` or `library` to load your shared
  object.
- Send an interrupt signal. This will put you back to the debugger
  prompt.
- Set the breakpoints in your code.
- Continue execution of R by typing [signal 0[RET]{.key}]{.kbd}.

Under Windows signals may not be able to be used, and if so the
procedure is more complicated. See the rw-FAQ.

---

#### 4.4.2 Inspecting R objects when debugging

The key to inspecting R objects from compiled code is the function
`PrintValue(SEXP s)` which uses the normal R printing mechanisms to
print the R object pointed to by `s`{.variable}, or the safer version
`R_PV(SEXP s)` which will only print 'objects'.

One way to make use of `PrintValue` is to insert suitable calls into the
code to be debugged.

Another way is to call `R_PV` from the symbolic debugger. (`PrintValue`
is hidden as `Rf_PrintValue`.) For example, from `gdb` we can use

```r
(gdb) p R_PV(ab)
```

using the object `ab` from the convolution example, if we have placed a
suitable breakpoint in the convolution C code.

To examine an arbitrary R object we need to work a little harder. For
example, let

```r
R> DF <- data.frame(a = 1:3, b = 4:6)
```

By setting a breakpoint at `do_get` and typing [get(\"DF\")]{.kbd} at
the R prompt, one can find out the address in memory of `DF`, for
example

```r
Value returned is $1 = (SEXPREC *) 0x40583e1c
(gdb) p *$1
$2 = {
  sxpinfo = {type = 19, obj = 1, named = 1, gp = 0,
    mark = 0, debug = 0, trace = 0, = 0},
  attrib = 0x40583e80,
  u = {
    vecsxp = {
      length = 2,
      type = {c = 0x40634700 "0>X@D>X@0>X@", i = 0x40634700,
        f = 0x40634700, z = 0x40634700, s = 0x40634700},
      truelength = 1075851272,
    },
    primsxp = {offset = 2},
    symsxp = {pname = 0x2, value = 0x40634700, internal = 0x40203008},
    listsxp = {carval = 0x2, cdrval = 0x40634700, tagval = 0x40203008},
    envsxp = {frame = 0x2, enclos = 0x40634700},
    closxp = {formals = 0x2, body = 0x40634700, env = 0x40203008},
    promsxp = {value = 0x2, expr = 0x40634700, env = 0x40203008}
  }
}
```

(Debugger output reformatted for better legibility).

Using `R_PV()` one can "inspect" the values of the various elements of
the SEXP, for example,

```r
(gdb) p R_PV($1->attrib)
$names
[1] "a" "b"

$row.names
[1] "1" "2" "3"

$class
[1] "data.frame"

$3 = void
```

To find out where exactly the corresponding information is stored, one
needs to go "deeper":

```r
(gdb) set $a = $1->attrib
(gdb) p $a->u.listsxp.tagval->u.symsxp.pname->u.vecsxp.type.c
$4 = 0x405d40e8 "names"
(gdb) p $a->u.listsxp.carval->u.vecsxp.type.s[1]->u.vecsxp.type.c
$5 = 0x40634378 "b"
(gdb) p $1->u.vecsxp.type.s[0]->u.vecsxp.type.i[0]
$6 = 1
(gdb) p $1->u.vecsxp.type.s[1]->u.vecsxp.type.i[1]
$7 = 5
```

Another alternative is the `R_inspect` function which shows the
low-level structure of the objects recursively (addresses differ from
the above as this example is created on another machine):

```r
(gdb) p R_inspect($1)
@100954d18 19 VECSXP g0c2 [OBJ,NAM(2),ATT] (len=2, tl=0)
  @100954d50 13 INTSXP g0c2 [NAM(2)] (len=3, tl=0) 1,2,3
  @100954d88 13 INTSXP g0c2 [NAM(2)] (len=3, tl=0) 4,5,6
ATTRIB:
  @102a70140 02 LISTSXP g0c0 []
    TAG: @10083c478 01 SYMSXP g0c0 [MARK,NAM(2),gp=0x4000] "names"
    @100954dc0 16 STRSXP g0c2 [NAM(2)] (len=2, tl=0)
      @10099df28 09 CHARSXP g0c1 [MARK,gp=0x21] "a"
      @10095e518 09 CHARSXP g0c1 [MARK,gp=0x21] "b"
    TAG: @100859e60 01 SYMSXP g0c0 [MARK,NAM(2),gp=0x4000] "row.names"
    @102a6f868 13 INTSXP g0c1 [NAM(2)] (len=2, tl=1) -2147483648,-3
    TAG: @10083c948 01 SYMSXP g0c0 [MARK,gp=0x4000] "class"
    @102a6f838 16 STRSXP g0c1 [NAM(2)] (len=1, tl=1)
      @1008c6d48 09 CHARSXP g0c2 [MARK,gp=0x21,ATT] "data.frame"
```

In general the representation of each object follows the format:

```r
@<address> <type-nr> <type-name> <gc-info> [<flags>] ...
```

For a more fine-grained control over the depth of the recursion and the
output of vectors `R_inspect3` takes additional two character()
parameters: maximum depth and the maximal number of elements that will
be printed for scalar vectors. The defaults in `R_inspect` are currently
-1 (no limit) and 5 respectively.

---

### 4.5 Using Link-time Optimization

Where supported, _link time optimization_ provides a comprehensive way
to check the consistency of calls between Fortran files or between C and
Fortran. See [Link-Time Optimization](./R-admin.html#Link_002dTime-Optimization) in R
Installation and Administration.

For example:

```r
boot.f:61: warning: type of ‘ddot’ does not match original declaration [-Wlto-type-mismatch]
        y(j,i)=ddot(p,x(j,1),n,b(1,j,i),1)
crq.f:1023: note: return value type mismatch
```

where the package author forgot to declare

```r
      double precision ddot
      external ddot
```

in `boot.f`.

Further examples:

```r
rkpk2.f:77:5: warning: type of ‘dstup’ does not match original declaration [-Wlto-type-mismatch]
      *info, wk)
rkpk1.f:2565:5: note: type mismatch in parameter 14
       subroutine dstup (s, lds, nobs, nnull, qraux, jpvt, y, q, ldqr,
rkpk1.f:2565:5: note: ‘dstup’ was previously declared here
```

where the fourteenth argument `dum` was missing in the call.

```r
reg.f:78:33: warning: type of ‘dqrdc’ does not match original declaration [-Wlto-type-mismatch]
       call dqrdc (sr, nobs, nobs, nnull, wk, dum, dum, 0)
dstup.f:20: note: ‘dqrdc’ was previously declared here
       call dqrdc (s, lds, nobs, nnull, qraux, jpvt, work, 1)
```

`dqrdc` is a LINPACK routine from R, `jpvt` is an integer array and
`work` is a double precision one so `dum` cannot match both. (If
`--enable-lto=check` had been used the comparison would have
been with the definition in R.)

For Fortran files all in the package, most inconsistencies can be
detected by concatenating the Fortran files and compiling the result,
sometimes with clearer diagnostics than provided by LTO. For our last
two examples this gives

```r
all.f:2966:72:

      *info, work1)
                                                                        1
Warning: Missing actual argument for argument ‘dum’ at (1)
```

and

```r
all.f:1663:72:

      *ipvtwk), wk(ikwk), wk(iwork1), wk(iwork2), info)
                                                                        1
Warning: Type mismatch in argument ‘jpvt’ at (1); passed REAL(8) to INTEGER(4)
```

---
