# 6 The R API: entry points for C code

---

---

• [Memory allocation](#Memory-allocation)     
 • [Error signaling](#Error-signaling)     
 • [Random numbers](#Random-numbers)     
 • [Missing and IEEE values](#Missing-and-IEEE-values)     
 • [Printing](#Printing)     
 • [Calling C from Fortran and vice versa](#Calling-C-from-Fortran-and-vice-versa)     
 • [Numerical analysis subroutines](#Numerical-analysis-subroutines)     
 • [Optimization](#Optimization)     
 • [Integration](#Integration)     
 • [Utility functions](#Utility-functions)     
 • [Re-encoding](#Re_002dencoding)     
 • [Condition handling and cleanup code](#Condition-handling-and-cleanup-code)     
 • [Allowing interrupts](#Allowing-interrupts)     
 • [Platform and version information](#Platform-and-version-information)     
 • [Inlining C functions](#Inlining-C-functions)     
 • [Controlling visibility](#Controlling-visibility)     
 • [Standalone Mathlib](#Standalone-Mathlib)     
 • [Organization of header files](#Organization-of-header-files)

---

There are a large number of entry points in the R executable/DLL that
can be called from C code (and some that can be called from Fortran
code). Only those documented here are stable enough that they will only
be changed with considerable notice.

The recommended procedure to use these is to include the header file
`R.h` in your C code by

```r
#include <R.h>
```

This will include several other header files from the directory
`R_INCLUDE_DIR/R_ext`, and there are other header files there
that can be included too, but many of the features they contain should
be regarded as undocumented and unstable.

Most of these header files, including all those included by
`R.h`, can be used from C++ code.

> **Note:** Because R re-maps many of its external names to avoid
> clashes with user code, it is _essential_ to include the appropriate
> header files when using these entry points.

This remapping can cause problems[^146^](#FOOT146), and can be
eliminated by defining `R_NO_REMAP` and prepending '`Rf_`' to
_all_ the function names used from `Rinternals.h` and
`R_ext/Error.h`. These problems can usually be avoided by
including other headers (such as system headers and those for external
software used by the package) before `R.h`.

We can classify the entry points as

_API_

: Entry points which are documented in this manual and declared in an
installed header file. These can be used in distributed packages and
will only be changed after deprecation.

_public_

: Entry points declared in an installed header file that are exported
on all R platforms but are not documented and subject to change
without notice.

_private_

: Entry points that are used when building R and exported on all R
platforms but are not declared in the installed header files. Do not
use these in distributed code.

_hidden_

: Entry points that are where possible (Windows and some modern
Unix-alike compilers/loaders when using R as a shared library) not
exported.

---

### 6.1 Memory allocation

---

• [Transient storage allocation](#Transient-storage-allocation)     
 • [User-controlled memory](#User_002dcontrolled-memory)

---

There are two types of memory allocation available to the C programmer,
one in which R manages the clean-up and the other in which user has full
control (and responsibility).

---

#### 6.1.1 Transient storage allocation

Here R will reclaim the memory at the end of the call to `.C`, `.Call`
or `.External`. Use

```r
char *R_alloc(size_t n, int size)
```

which allocates `n` units of `size` bytes each. A
typical usage (from package **stats**) is

```r
x = (int *) R_alloc(nrows(merge)+2, sizeof(int));
```

(`size_t` is defined in `stddef.h` which the header defining
`R_alloc` includes.)

There is a similar call, `S_alloc` (for compatibility with older
versions of S) which zeroes the memory allocated,

```r
char *S_alloc(long n, int size)
```

and

```r
char *S_realloc(char *p, long new, long old, int size)
```

which changes the allocation size from `old` to
`new` units, and zeroes the additional units.

For compatibility with current versions of S, header `S.h`
(only) defines wrapper macros equivalent to

```r
type* Salloc(long n, int type)
type* Srealloc(char *p, long new, long old, int type)
```

This memory is taken from the heap, and released at the end of the `.C`,
`.Call` or `.External` call. Users can also manage it, by noting the
current position with a call to `vmaxget` and subsequently clearing
memory allocated by a call to `vmaxset`. An example might be

```r
void *vmax = vmaxget()
// a loop involving the use of R_alloc at each iteration
vmaxset(vmax)
```

This is only recommended for experts.

Note that this memory will be freed on error or user interrupt (if
allowed: see [Allowing interrupts](#Allowing-interrupts)).

The memory returned is only guaranteed to be aligned as required for
`double` pointers: take precautions if casting to a pointer which needs
more. There is also

```r
long double *R_allocLD(size_t n)
```

which is guaranteed to have the 16-byte alignment needed for
`long double` pointers on some platforms.

These functions should only be used in code called by `.C` etc, never
from front-ends. They are not thread-safe.

---

#### 6.1.2 User-controlled memory

The other form of memory allocation is an interface to `malloc`, the
interface providing R error signaling. This memory lasts until freed by
the user and is additional to the memory allocated for the R workspace.

The interface functions are

```r
type* Calloc(size_t n, type)
type* Realloc(any *p, size_t n, type)
void Free(any *p)
```

providing analogues of `calloc`, `realloc` and `free`. If there is an
error during allocation it is handled by R, so if these routines return
the memory has been successfully allocated or freed. `Free` will set the
pointer `p` to `NULL`. (Some but not all versions of S do
so.)

Users should arrange to `Free` this memory when no longer needed,
including on error or user interrupt. This can often be done most
conveniently from an `on.exit` action in the calling R function -- see
`pwilcox` for an example.

Do not assume that memory allocated by `Calloc`/`Realloc` comes from the
same pool as used by `malloc`: in particular do not use `free` or
`strdup` with it.

Memory obtained by these functions should be aligned in the same way as
`malloc`, that is 'suitably aligned for any kind of variable'.

These entry points need to be prefixed by `R_` if `STRICT_R_HEADERS` has
been defined.

---

### 6.2 Error signaling

The basic error signaling routines are the equivalents of `stop` and
`warning` in R code, and use the same interface.

```r
void error(const char * format, ...);
void warning(const char * format, ...);
```

These have the same call sequences as calls to `printf`, but in the
simplest case can be called with a single character string argument
giving the error message. (Don't do this if the string contains
'`%`' or might otherwise be interpreted as a format.)

If `STRICT_R_HEADERS` is not defined there is also an S-compatibility
interface which uses calls of the form

```r
PROBLEM ...... ERROR
MESSAGE ...... WARN
PROBLEM ...... RECOVER(NULL_ENTRY)
MESSAGE ...... WARNING(NULL_ENTRY)
```

the last two being the forms available in all S versions. Here
'`......`' is a set of arguments to `printf`, so can be a
string or a format string followed by arguments separated by commas.

---

• [Error signaling from Fortran](#Error-signaling-from-Fortran)

---

---

#### 6.2.1 Error signaling from Fortran

There are two interface function provided to call `error` and `warning`
from Fortran code, in each case with a simple character string argument.
They are defined as

```r
subroutine rexit(message)
subroutine rwarn(message)
```

Messages of more than 255 characters are truncated, with a warning.

---

### 6.3 Random number generation

The interface to R's internal random number generation routines is

```r
double unif_rand();
double norm_rand();
double exp_rand();
double R_unif_index(double);
```

giving one uniform, normal or exponential pseudo-random variate.
However, before these are used, the user must call

```r
GetRNGstate();
```

and after all the required variates have been generated, call

```r
PutRNGstate();
```

These essentially read in (or create) `.Random.seed` and write it out
after use.

File `S.h` defines `seed_in` and `seed_out` for S-compatibility
rather than `GetRNGstate` and `PutRNGstate`. These take a `long *`
argument which is ignored.

The random number generator is private to R; there is no way to select
the kind of RNG or set the seed except by evaluating calls to the R
functions.

The C code behind R's `rxxx` functions can be accessed by including the
header file `Rmath.h`; See [Distribution functions](#Distribution-functions). Those calls generate a single
variate and should also be enclosed in calls to `GetRNGstate` and
`PutRNGstate`.

---

### 6.4 Missing and IEEE special values

A set of functions is provided to test for `NA`, `Inf`, `-Inf` and
`NaN`. These functions are accessed _via_ macros:

```r
ISNA(x)        True for R’s NA only
ISNAN(x)       True for R’s NA and IEEE NaN
R_FINITE(x)    False for Inf, -Inf, NA, NaN
```

and _via_ function `R_IsNaN` which is true for `NaN` but not `NA`.

Do use `R_FINITE` rather than `isfinite` or `finite`; the latter is
often mendacious and `isfinite` is only available on a some platforms,
on which `R_FINITE` is a macro expanding to `isfinite`.

Currently in C code `ISNAN` is a macro calling `isnan`. (Since this
gives problems on some C++ systems, if the R headers is called from C++
code a function call is used.)

You can check for `Inf` or `-Inf` by testing equality to `R_PosInf` or
`R_NegInf`, and set (but not test) an `NA` as `NA_REAL`.

All of the above apply to _double_ variables only. For integer variables
there is a variable accessed by the macro `NA_INTEGER` which can used to
set or test for missingness.

---

### 6.5 Printing

The most useful function for printing from a C routine compiled into R
is `Rprintf`. This is used in exactly the same way as `printf`, but is
guaranteed to write to R's output (which might be a GUI console rather
than a file, and can be re-directed by `sink`). It is wise to write
complete lines (including the `"\n"`) before returning to R. It is
defined in `R_ext/Print.h`.

The function `REprintf` is similar but writes on the error stream
(`stderr`) which may or may not be different from the standard output
stream.

Functions `Rvprintf` and `REvprintf` are analogues using the `vprintf`
interface. Because that is a C99[^147^](#FOOT147) interface,
they are only defined by `R_ext/Print.h` in C++ code if the
macro `R_USE_C99_IN_CXX` is defined when it is included.

Another circumstance when it may be important to use these functions is
when using parallel computation on a cluster of computational nodes, as
their output will be re-directed/logged appropriately.

---

• [Printing from Fortran](#Printing-from-Fortran)

---

---

#### 6.5.1 Printing from Fortran

On many systems Fortran `write` and `print` statements can be used, but
the output may not interleave well with that of C, and will be invisible
on GUI interfaces. They are not portable and best avoided.

Three subroutines are provided to ease the output of information from
Fortran code.

```r
subroutine dblepr(label, nchar, data, ndata)
subroutine realpr(label, nchar, data, ndata)
subroutine intpr (label, nchar, data, ndata)
```

Here `label` is a character label of up to 255 characters,
`nchar` is its length (which can be `-1` if the whole label
is to be used), and `data` is an array of length at least
`ndata` of the appropriate type (`double precision`, `real`
and `integer` respectively). These routines print the label on one line
and then print `data` as if it were an R vector on subsequent
line(s). They work with zero `ndata`, and so can be used to
print a label alone. Note though that some compilers will give an error
or warning unless `data` is an array: others will accept a
scalar when `ndata` has value one or zero.

---

### 6.6 Calling C from Fortran and vice versa

Naming conventions for symbols generated by Fortran differ by platform:
it is not safe to assume that Fortran names appear to C with a trailing
underscore. To help cover up the platform-specific differences there is
a set of macros[^148^](#FOOT148) that should be used.

`F77_SUB(name)`

: to define a function in C to be called from Fortran

`F77_NAME(name)`

: to declare a Fortran routine in C before use

`F77_CALL(name)`

: to call a Fortran routine from C

`F77_COMDECL(name)`

: to declare a Fortran common block in C

`F77_COM(name)`

: to access a Fortran common block from C

On most current platforms these are all the same, but it is unwise to
rely on this. Note that names containing underscores were not legal in
Fortran 77, and are not portably handled by the above macros. (Also, all
Fortran names for use by R are lower case, but this is not enforced by
the macros.)

For example, suppose we want to call R's normal random numbers from
Fortran. We need a C wrapper along the lines of

```r
#include <R.h>

void F77_SUB(rndstart)(void) { GetRNGstate(); }
void F77_SUB(rndend)(void) { PutRNGstate(); }
double F77_SUB(normrnd)(void) { return norm_rand(); }
```

to be called from Fortran as in

```r
      subroutine testit()
      double precision normrnd, x
      call rndstart()
      x = normrnd()
      call dblepr("X was", 5, x, 1)
      call rndend()
      end
```

Note that this is not guaranteed to be portable, for the return
conventions might not be compatible between the C and Fortran compilers
used. (Passing values _via_ arguments is safer.)

The standard packages, for example **stats**, are a rich source of
further examples.

Where supported, _link time optimization_ provides a reliable way to
check the consistency of calls to C from Fortran or _vice versa_. See
[Link-Time Optimization](./R-admin.html#Link_002dTime-Optimization) in R
Installation and Administration. One place where this occurs is the
registration of `.Fortran` calls in C code (see [Registering native routines](#Registering-native-routines)). For example

```r
init.c:10:13: warning: type of ‘vsom_’ does not match original
 declaration [-Wlto-type-mismatch]
  extern void F77_NAME(vsom)(void *, void *, void *, void *,
    void *, void *, void *, void *, void *);
vsom.f90:20:33: note: type mismatch in parameter 9
   subroutine vsom(neurons,dt,dtrows,dtcols,xdim,ydim,alpha,train)
vsom.f90:20:33: note: ‘vsom’ was previously declared here
```

shows that a subroutine has been registered with 9 arguments (as that is
what the `.Fortran` call used) but only has 8.

---

• [Fortran character strings](#Fortran-character-strings)     
 • [Fortran LOGICAL](#Fortran-LOGICAL)

---

---

#### 6.6.1 Fortran character strings

Passing character strings from C to Fortran or _vice versa_ is not
portable, but can be done with care. The internal representations are
different: a character array in C (or C++) is nul-terminated so its
length can be computed by `strlen`. Fortran character arrays are
typically stored as an array of bytes and a length. This matters when
passing strings from C to Fortran or _vice versa_: in many cases one has
been able to get away with passing the string but not the length.
However, in 2019 this changed for `gfortran`, starting with version 9
but backported to versions 7 and 8. Several months later, `gfortran` 9.2
introduced an option

```r
-ftail-call-workaround
```

and made it the current default but said it might be withdrawn in
future.

Suppose we want a function to report a message from Fortran to R's
console (one could use `intpr` with dummy data, but it might be the
basis of a custom reporting function). Suppose the equivalent in Fortran
would be

```r
      subroutine rmsg(msg)
      character*(*) msg
      print *.msg
      end
```

in file `rmsg.f`. Using `gfortran` 9.2 and later we can extract
the C view by

```r
gfortran -c -fc-prototypes-external rmsg.f
```

which gives

```r
void rmsg_ (char *msg, size_t msg_len);
```

(where `size_t` applies to version 8 and later). We could re-write that
portably in C as

```r
#define USE_FC_LEN_T
#include <Rconfig.h> // included by R.h, so define USE_FC_LEN_T early

void F77_NAME(rmsg)(char *msg, FC_LEN_T msg_len)
{
    char cmsg[msg_len+1];
    strncpy(cmsg, msg, msg_len);
    cmsg[msg_len] = ‘\0’; // nul-terminate the string, to be sure
    // do something with ‘cmsg’
}
```

in code depending on `R(>= 3.6.2)`. For earlier versions of R we could
just assume that `msg` is nul-terminated (not guaranteed, but people
have been getting away with it for many years), so the complete C side
might be

```r
#define USE_FC_LEN_T
#include <Rconfig.h>

#ifdef FC_LEN_T
void F77_NAME(rmsg)(char *msg, FC_LEN_T msg_len)
{
    char cmsg[msg_len+1];
    strncpy(cmsg, msg, msg_len);
    cmsg[msg_len] = ‘\0’;
    // do something with ‘cmsg’
}
#else
void F77_NAME(rmsg)(char *msg)
{
    // do something with ‘msg’
}
#endif
```

An alternative is to use Fortran 2003
features[^149^](#FOOT149) to set up the Fortran routine to
pass a C-compatible character string. We could use something like

```r
      module cfuncs
        use iso_c_binding, only: c_char, c_null_char
        interface
          subroutine cmsg(msg) bind(C, name = ‘cmsg’)
            use iso_c_binding, only: c_char
            character(kind = c_char):: msg(*)
          end subroutine cmsg
        end interface
      end module

      subroutine rmsg(msg)
        use cfuncs
        character(*) msg
        call cmsg(msg//c_null_char) ! need to concatenate a nul terminator
      end subroutine rmsg
```

where the C side is simply

```r
void cmsg(const char *msg)
{
    // do something with nul-terminated string ‘msg’
}
```

Passing a variable-length string from C to Fortran is trickier, but all
the uses in BLAS and LAPACK are of a single character, and for these we
can write a wrapper in Fortran along the lines of

```r
      subroutine c_dgemm(transa, transb, m, n, k, alpha,
     +     a, lda, b, ldb, beta, c, ldc)
     +     bind(C, name = ‘Cdgemm’)
        use iso_c_binding, only : c_char, c_int, c_double
        character(c_char):: transa, transb
        integer(c_int):: m, n, k, lda, ldb, ldc
        real(c_double):: alpha, beta, a(lda,*), b(ldb,*), c(ldc,*)
        call dgemm(transa, transb, m, n, k, alpha,
     +             a, lda, b, ldb, beta, c, ldc)
      end subroutine c_dgemm
```

which is then called from C with declaration

```r
void
Cdgemm(const char *transa, const char *transb, const int *m,
       const int *n, const int *k, const double *alpha,
       const double *a, const int *lda, const double *b, const int *ldb,
       const double *beta, double *c, const int *ldc);
```

Alternatively, do as R does as from version 3.6.2 and pass the character
length(s) from C to Fortran. A portable way to do this is

```r
// before any R headers, or define in PKG_CPPFLAGS
#define USE_FC_LEN_T
#include <Rconfig.h>
#include <R_ext/BLAS.h>
#ifndef FCONE
# define FCONE
#endif
...
        F77_CALL(dgemm)("N", "T", &nrx, &ncy, &ncx, &one, x,
                        &nrx, y, &nry, &zero, z, &nrx FCONE FCONE);
```

(Note there is no comma before or between the `FCONE` invocations.) It
is strongly recommended that packages which call from C/C++ BLAS/LAPACK
routines with character arguments adopt this approach.

---

#### 6.6.2 Fortran LOGICAL

Passing Fortran LOGICAL variables to/from C/C++ is potentially
compiler-dependent. Fortran compilers have long used a 32-bit integer
type so it is pretty portable to use `int *` on the C/C++ side. However,
recent versions of `gfortran` _via_ the option
`-fc-prototypes-external` say the C equivalent is
`int_least32_t *`: 'Link-Time Optimization' will report `int *` as a
mismatch.

---

### 6.7 Numerical analysis subroutines

R contains a large number of mathematical functions for its own use, for
example numerical linear algebra computations and special functions.

The header files `R_ext/BLAS.h`, `R_ext/Lapack.h` and
`R_ext/Linpack.h` contains declarations of the BLAS, LAPACK and
LINPACK linear algebra functions included in R. These are expressed as
calls to Fortran subroutines, and they will also be usable from users'
Fortran code. Although not part of the official API, this set of
subroutines is unlikely to change (but might be supplemented).

The header file `Rmath.h` lists many other functions that are
available and documented in the following subsections. Many of these are
C interfaces to the code behind R functions, so the R function
documentation may give further details.

---

• [Distribution functions](#Distribution-functions)     
 • [Mathematical functions](#Mathematical-functions)     
 • [Numerical Utilities](#Numerical-Utilities)     
 • [Mathematical constants](#Mathematical-constants)

---

---

#### 6.7.1 Distribution functions

The routines used to calculate densities, cumulative distribution
functions and quantile functions for the standard statistical
distributions are available as entry points.

The arguments for the entry points follow the pattern of those for the
normal distribution:

```r
double dnorm(double x, double mu, double sigma, int give_log);
double pnorm(double x, double mu, double sigma, int lower_tail,
             int give_log);
double qnorm(double p, double mu, double sigma, int lower_tail,
             int log_p);
double rnorm(double mu, double sigma);
```

That is, the first argument gives the position for the density and CDF
and probability for the quantile function, followed by the
distribution's parameters. Argument `lower_tail` should be
`TRUE` (or `1`) for normal use, but can be `FALSE` (or `0`) if the
probability of the upper tail is desired or specified.

Finally, `give_log` should be non-zero if the result is
required on log scale, and `log_p` should be non-zero if
`p` has been specified on log scale.

Note that you directly get the cumulative (or "integrated") _hazard_
function, H(t) = - log(1 - F(t)), by using

```r
- pdist(t, ..., /*lower_tail = */ FALSE, /* give_log = */ TRUE)
```

or shorter (and more cryptic) `- pdist(t, ..., 0, 1)`.

The random-variate generation routine `rnorm` returns one normal
variate. See [Random numbers](#Random-numbers), for the protocol in
using the random-variate routines.

Note that these argument sequences are (apart from the names and that
`rnorm` has no `n`) mainly the same as the corresponding R
functions of the same name, so the documentation of the R functions can
be used. Note that the exponential and gamma distributions are
parametrized by `scale` rather than `rate`.

For reference, the following table gives the basic name (to be prefixed
by '`d`', '`p`', '`q`' or '`r`'
apart from the exceptions noted) and distribution-specific arguments for
the complete set of distributions.

> ---
>
> beta `beta` `a`, `b`
> non-central beta `nbeta` `a`, `b`, `ncp`
> binomial `binom` `n`, `p`
> Cauchy `cauchy` `location`, `scale`
> chi-squared `chisq` `df`
> non-central chi-squared `nchisq` `df`, `ncp`
> exponential `exp` `scale` (and **not** `rate`)
> F `f` `n1`, `n2`
> non-central F `nf` `n1`, `n2`, `ncp`
> gamma `gamma` `shape`, `scale`
> geometric `geom` `p`
> hypergeometric `hyper` `NR`, `NB`, `n`
> logistic `logis` `location`, `scale`
> lognormal `lnorm` `logmean`, `logsd`
> negative binomial `nbinom` `size`, `prob`
> normal `norm` `mu`, `sigma`
> Poisson `pois` `lambda`
> Student's t `t` `n`
> non-central t `nt` `df`, `delta`
> Studentized range `tukey` (\*) `rr`, `cc`, `df`
> uniform `unif` `a`, `b`
> Weibull `weibull` `shape`, `scale`
> Wilcoxon rank sum `wilcox` `m`, `n`
> Wilcoxon signed rank `signrank` `n`
>
> ---

Entries marked with an asterisk only have '`p`' and
'`q`' functions available, and none of the non-central
distributions have '`r`' functions. After a call to `dwilcox`,
`pwilcox` or `qwilcox` the function `wilcox_free()` should be called,
and similarly for the signed rank functions.

(If remapping is suppressed, the Normal distribution names are
`Rf_dnorm4`, `Rf_pnorm5` and `Rf_qnorm5`.)

For the negative binomial distribution ('`nbinom`'), in
addition to the `(size, prob)` parametrization, the alternative
`(size, mu)` parametrization is provided as well by functions
'`[dpqr]nbinom_mu()`', see [?NegBinomial] in R.

Functions `dpois_raw(x, *)` and `dbinom_raw(x, *)` are versions of the
Poisson and binomial probability mass functions which work continuously
in `x`, whereas `dbinom(x,*)` and `dpois(x,*)` only return non zero
values for integer `x`.

```r
double dbinom_raw(double x, double n, double p, double q, int give_log)
double dpois_raw (double x, double lambda, int give_log)
```

Note that `dbinom_raw()` gets both p and q = 1-p which may be
advantageous when one of them is close to 1.

---

#### 6.7.2 Mathematical functions

Function: _double_ **gammafn** _(double `x`)_\
Function: _double_ **lgammafn** _(double `x`)_\
Function: _double_ **digamma** _(double `x`)_\
Function: _double_ **trigamma** _(double `x`)_\
Function: _double_ **tetragamma** _(double `x`)_\
Function: _double_ **pentagamma** _(double `x`)_\
Function: _double_ **psigamma** _(double `x`, double `deriv`)_

: The Gamma function, the natural logarithm of its absolute value and
first four derivatives and the n-th derivative of Psi, the digamma
function, which is the derivative of `lgammafn`. In other words,
`digamma(x)` is the same as `psigamma(x,0)`,
`trigamma(x) == psigamma(x,1)`, etc.

Function: _double_ **beta** _(double `a`, double `b`)_\
Function: _double_ **lbeta** _(double `a`, double `b`)_

: The (complete) Beta function and its natural logarithm.

Function: _double_ **choose** _(double `n`, double `k`)_\
Function: _double_ **lchoose** _(double `n`, double `k`)_

: The number of combinations of `k` items chosen from from
`n` and the natural logarithm of its absolute value,
generalized to arbitrary real `n`. `k` is
rounded to the nearest integer (with a warning if needed).

Function: _double_ **bessel_i** _(double `x`, double `nu`, double `expo`)_\
Function: _double_ **bessel_j** _(double `x`, double `nu`)_\
Function: _double_ **bessel_k** _(double `x`, double `nu`, double `expo`)_\
Function: _double_ **bessel_y** _(double `x`, double `nu`)_

: Bessel functions of types I, J, K and Y with index `nu`.
For `bessel_i` and `bessel_k` there is the option to return
[exp(-]`x`) I(`x`; `nu`)
or exp(`x`) K(`x`; `nu`) if
`expo` is 2. (Use `expo == 1` for unscaled values.)

---

#### 6.7.3 Numerical Utilities

There are a few other numerical utility functions available as entry
points.

Function: _double_ **R_pow** _(double `x`, double `y`)_\
Function: _double_ **R_pow_di** _(double `x`, int `i`)_

: `R_pow(x, y)` and `R_pow_di(x, i)` compute `x^y` and `x^i`,
respectively using `R_FINITE` checks and returning the proper result
(the same as R) for the cases where `x`, `y`
or `i` are 0 or missing or infinite or `NaN`.

Function: _double_ **log1p** _(double `x`)_

: Computes `log(1 + x)` (_log 1 **p**lus x_), accurately even for
small `x`, i.e., \|x\| \<\< 1.

    This should be provided by your platform, in which case it is not
    included in `Rmath.h`, but is (probably) in
    `math.h` which `Rmath.h` includes (except under
    C++, so it may not be declared for C++98).

Function: _double_ **log1pmx** _(double `x`)_

: Computes `log(1 + x) - x` (\*log 1 **p**lus x **m**inus **x\***),
accurately even for small `x`, i.e., \|x\| \<\< 1.

Function: _double_ **log1pexp** _(double `x`)_

: Computes `log(1 + exp(x))` (\*log 1 **p**lus **exp\***), accurately,
notably for large `x`, e.g., x \> 720.

Function: _double_ **expm1** _(double `x`)_

: Computes `exp(x) - 1` (_exp x **m**inus 1_), accurately even for
small `x`, i.e., \|x\| \<\< 1.

    This should be provided by your platform, in which case it is not
    included in `Rmath.h`, but is (probably) in
    `math.h` which `Rmath.h` includes (except under
    C++, so it may not be declared for C++98).

Function: _double_ **lgamma1p** _(double `x`)_

: Computes `log(gamma(x + 1))` (_log(gamma(1 **p**lus x))_),
accurately even for small `x`, i.e., 0 \< x \< 0.5.

Function: _double_ **cospi** _(double `x`)_

: Computes `cos(pi * x)` (where `pi` is 3.14159\...), accurately,
notably for half integer `x`.

    This might be provided by your platform[^150^](#FOOT150),
    in which case it is not included in `Rmath.h`, but is in
    `math.h` which `Rmath.h` includes. (Ensure that
    neither `math.h` nor `cmath` is included before
    `Rmath.h` or define


    ``` r
    #define __STDC_WANT_IEC_60559_FUNCS_EXT__ 1
    ```

    before the first inclusion.)

Function: _double_ **sinpi** _(double `x`)_

: Computes `sin(pi * x)` accurately, notably for (half) integer
`x`.

    This might be provided by your platform, in which case it is not
    included in `Rmath.h`, but is in `math.h` which
    `Rmath.h` includes (but see the comments for `cospi`).

Function: _double_ **tanpi** _(double `x`)_

: Computes `tan(pi * x)` accurately, notably for (half) integer
`x`.

    This might be provided by your platform, in which case it is not
    included in `Rmath.h`, but is in `math.h` which
    `Rmath.h` includes (but see the comments for `cospi`).

Function: _double_ **logspace_add** _(double `logx`, double `logy`)_\
Function: _double_ **logspace_sub** _(double `logx`, double `logy`)_\
Function: _double_ **logspace_sum** _(const double\* `logx`, int `n`)_

: Compute the log of a sum or difference from logs of terms, i.e., "x + y" as `log (exp(logx) + exp(logy))` and "x - y" as
`log (exp(logx) - exp(logy))`, and "sum_i x\[i\]" as
`log (sum[i = 1:n exp(logx[i])] )` without causing unnecessary
overflows or throwing away too much accuracy.

Function: _int_ **imax2** _(int `x`, int `y`)_\
Function: _int_ **imin2** _(int `x`, int `y`)_\
Function: _double_ **fmax2** _(double `x`, double `y`)_\
Function: _double_ **fmin2** _(double `x`, double `y`)_

: Return the larger (`max`) or smaller (`min`) of two integer or
double numbers, respectively. Note that `fmax2` and `fmin2` differ
from C99/C++11's `fmax` and `fmin` when one of the arguments is a
`NaN`: these versions return `NaN`.

Function: _double_ **sign** _(double `x`)_

: Compute the _signum_ function, where sign(`x`) is 1, 0,
or _-1_, when `x` is positive, 0, or negative,
respectively, and `NaN` if `x` is a `NaN`.

Function: _double_ **fsign** _(double `x`, double `y`)_

: Performs "transfer of sign" and is defined as \|x\| \* sign(y).

Function: _double_ **fprec** _(double `x`, double `digits`)_

: Returns the value of `x` rounded to `digits`
decimal digits (after the decimal point).

    This is the function used by R's `signif()`.

Function: _double_ **fround** _(double `x`, double `digits`)_

: Returns the value of `x` rounded to `digits`
_significant_ decimal digits.

    This is the function used by R's `round()`. (Note that C99/C++11
    provide a `round` function but C++98 need not.)

Function: _double_ **ftrunc** _(double `x`)_

: Returns the value of `x` truncated (to an integer value)
towards zero.

---

#### 6.7.4 Mathematical constants

R has a set of commonly used mathematical constants encompassing
constants defined by POSIX and usually[^151^](#FOOT151) found
in `math.h` (but maybe not in the C++ header `cmath`)
and contains further ones that are used in statistical computations.
These are defined to (at least) 30 digits accuracy in
`Rmath.h`. The following definitions use `ln(x)` for the
natural logarithm (`log(x)` in R).

> Name Definition (`ln = log`) round(_value_, 7)
>
> ---
>
> `M_E` _e_ 2.7182818
> `M_LOG2E` log2(_e_) 1.4426950
> `M_LOG10E` log10(_e_) 0.4342945
> `M_LN2` ln(2) 0.6931472
> `M_LN10` ln(10) 2.3025851
> `M_PI` pi 3.1415927
> `M_PI_2` pi/2 1.5707963
> `M_PI_4` pi/4 0.7853982
> `M_1_PI` 1/pi 0.3183099
> `M_2_PI` 2/pi 0.6366198
> `M_2_SQRTPI` 2/sqrt(pi) 1.1283792
> `M_SQRT2` sqrt(2) 1.4142136
> `M_SQRT1_2` 1/sqrt(2) 0.7071068
> `M_SQRT_3` sqrt(3) 1.7320508
> `M_SQRT_32` sqrt(32) 5.6568542
> `M_LOG10_2` log10(2) 0.3010300
> `M_2PI` 2\*pi 6.2831853
> `M_SQRT_PI` sqrt(pi) 1.7724539
> `M_1_SQRT_2PI` 1/sqrt(2\*pi) 0.3989423
> `M_SQRT_2dPI` sqrt(2/pi) 0.7978846
> `M_LN_SQRT_PI` ln(sqrt(pi)) 0.5723649
> `M_LN_SQRT_2PI` ln(sqrt(2\*pi)) 0.9189385
> `M_LN_SQRT_PId2` ln(sqrt(pi/2)) 0.2257914

There are a set of constants (`PI`, `DOUBLE_EPS`) (and so on) defined
(unless `STRICT_R_HEADERS` is defined) in the included header
`R_ext/Constants.h`, mainly for compatibility with S.

Further, the included header `R_ext/Boolean.h` has enumeration
constants `TRUE` and `FALSE` of type `Rboolean` in order to provide a
way of using "logical" variables in C consistently. This can conflict
with other software: for example it conflicts with the headers in IJG's
`jpeg-9` (but not earlier versions).

---

### 6.8 Optimization

The C code underlying `optim` can be accessed directly. The user needs
to supply a function to compute the function to be minimized, of the
type

```r
typedef double optimfn(int n, double *par, void *ex);
```

where the first argument is the number of parameters in the second
argument. The third argument is a pointer passed down from the calling
routine, normally used to carry auxiliary information.

Some of the methods also require a gradient function

```r
typedef void optimgr(int n, double *par, double *gr, void *ex);
```

which passes back the gradient in the `gr` argument. No function is
provided for finite-differencing, nor for approximating the Hessian at
the result.

The interfaces (defined in header `R_ext/Applic.h`) are

- Nelder Mead:

  ```r
  void nmmin(int n, double *xin, double *x, double *Fmin, optimfn fn,
             int *fail, double abstol, double intol, void *ex,
             double alpha, double beta, double gamma, int trace,
             int *fncount, int maxit);
  ```

- BFGS:

  ```r
  void vmmin(int n, double *x, double *Fmin,
             optimfn fn, optimgr gr, int maxit, int trace,
             int *mask, double abstol, double reltol, int nREPORT,
             void *ex, int *fncount, int *grcount, int *fail);
  ```

- Conjugate gradients:

  ```r
  void cgmin(int n, double *xin, double *x, double *Fmin,
             optimfn fn, optimgr gr, int *fail, double abstol,
             double intol, void *ex, int type, int trace,
             int *fncount, int *grcount, int maxit);
  ```

- Limited-memory BFGS with bounds:

  ```r
  void lbfgsb(int n, int lmm, double *x, double *lower,
              double *upper, int *nbd, double *Fmin, optimfn fn,
              optimgr gr, int *fail, void *ex, double factr,
              double pgtol, int *fncount, int *grcount,
              int maxit, char *msg, int trace, int nREPORT);
  ```

- Simulated annealing:

  ```r
  void samin(int n, double *x, double *Fmin, optimfn fn, int maxit,
             int tmax, double temp, int trace, void *ex);
  ```

Many of the arguments are common to the various methods. `n` is the
number of parameters, `x` or `xin` is the starting parameters on entry
and `x` the final parameters on exit, with final value returned in
`Fmin`. Most of the other parameters can be found from the help page for
`optim`: see the source code `src/appl/lbfgsb.c` for the values
of `nbd`, which specifies which bounds are to be used.

---

### 6.9 Integration

The C code underlying `integrate` can be accessed directly. The user
needs to supply a _vectorizing_ C function to compute the function to be
integrated, of the type

```r
typedef void integr_fn(double *x, int n, void *ex);
```

where `x[]` is both input and output and has length `n`, i.e., a C
function, say `fn`, of type `integr_fn` must basically do
`for(i in 1:n) x[i] := f(x[i], ex)`. The vectorization requirement can
be used to speed up the integrand instead of calling it `n` times. Note
that in the current implementation built on QUADPACK, `n` will be either
15 or 21. The `ex` argument is a pointer passed down from the calling
routine, normally used to carry auxiliary information.

There are interfaces (defined in header `R_ext/Applic.h`) for
integrals over finite and infinite intervals (or "ranges" or
"integration boundaries").

- Finite:

  ```r
  void Rdqags(integr_fn f, void *ex, double *a, double *b,
              double *epsabs, double *epsrel,
              double *result, double *abserr, int *neval, int *ier,
              int *limit, int *lenw, int *last,
              int *iwork, double *work);
  ```

- Infinite:

  ```r
  void Rdqagi(integr_fn f, void *ex, double *bound, int *inf,
              double *epsabs, double *epsrel,
              double *result, double *abserr, int *neval, int *ier,
              int *limit, int *lenw, int *last,
              int *iwork, double *work);
  ```

Only the 3rd and 4th argument differ for the two integrators; for the
finite range integral using `Rdqags`, `a` and `b` are the integration
interval bounds, whereas for an infinite range integral using `Rdqagi`,
`bound` is the finite bound of the integration (if the integral is not
doubly-infinite) and `inf` is a code indicating the kind of integration
range,

`inf = 1`

: corresponds to (bound, +Inf),

`inf = -1`

: corresponds to (-Inf, bound),

`inf = 2`

: corresponds to (-Inf, +Inf),

`f` and `ex` define the integrand function, see above; `epsabs` and
`epsrel` specify the absolute and relative accuracy requested, `result`,
`abserr` and `last` are the output components `value`, `abs.err` and
`subdivisions` of the R function integrate, where `neval` gives the
number of integrand function evaluations, and the error code `ier` is
translated to R's `integrate() $ message`, look at that function
definition. `limit` corresponds to `integrate(..., subdivisions = *)`.
It seems you should always define the two work arrays and the length of
the second one as

```r
    lenw = 4 * limit;
    iwork =   (int *) R_alloc(limit, sizeof(int));
    work = (double *) R_alloc(lenw,  sizeof(double));
```

The comments in the source code in `src/appl/integrate.c` give
more details, particularly about reasons for failure (`ier >= 1`).

---

### 6.10 Utility functions

R has a fairly comprehensive set of sort routines which are made
available to users' C code. The following is declared in header file
`Rinternals.h`.

Function: _void_ **R_orderVector** _(int\* `indx`, int `n`, SEXP `arglist`, Rboolean `nalast`, Rboolean `decreasing`)_\
Function: _void_ **R_orderVector1** _(int\* `indx`, int `n`, SEXP `x`, Rboolean `nalast`, Rboolean `decreasing`)_

: `R_orderVector()` corresponds to R's
`order(..., na.last, decreasing)`. More specifically,
`indx <- order(x, y, na.last, decreasing)` corresponds to
`R_orderVector(indx, n, Rf_lang2(x, y), nalast, decreasing)` and for
three vectors, `Rf_lang3(x,y,z)` is used as `arglist`.

    Both `R_orderVector` and `R_orderVector1` assume the vector `indx`
    to be allocated to length \>= n. On return, `indx[]` contains a
    permutation of `0:(n-1)`, i.e., 0-based C indices (and not 1-based R
    indices, as R's `order()`).

    When ordering only one vector, `R_orderVector1` is faster and
    corresponds (but is 0-based) to R's
    `indx <- order(x, na.last, decreasing)`. It was added in R 3.3.0.

All other sort routines are declared in header file
`R_ext/Utils.h` (included by `R.h`) and include the
following.

Function: _void_ **R_isort** _(int\* `x`, int `n`)_\
Function: _void_ **R_rsort** _(double\* `x`, int `n`)_\
Function: _void_ **R_csort** _(Rcomplex\* `x`, int `n`)_\
Function: _void_ **rsort_with_index** _(double\* `x`, int\* `index`, int `n`)_

: The first three sort integer, real (double) and complex data
respectively. (Complex numbers are sorted by the real part first
then the imaginary part.) `NA`s are sorted last.

    `rsort_with_index` sorts on `x`, and applies the same
    permutation to `index`. `NA`s are sorted last.

Function: _void_ **revsort** _(double\* `x`, int\* `index`, int `n`)_

: Is similar to `rsort_with_index` but sorts into decreasing order,
and `NA`s are not handled.

Function: _void_ **iPsort** _(int\* `x`, int `n`, int `k`)_\
Function: _void_ **rPsort** _(double\* `x`, int `n`, int `k`)_\
Function: _void_ **cPsort** _(Rcomplex\* `x`, int `n`, int `k`)_

: These all provide (very) partial sorting: they permute
`x` so that `x[k]` is in the correct place with smaller
values to the left, larger ones to the right.

Function: _void_ **R_qsort** _(double \*`v`, size_t `i`, size_t `j`)_\
Function: _void_ **R_qsort_I** _(double \*`v`, int \*`I`, int `i`, int `j`)_\
Function: _void_ **R_qsort_int** _(int \*`iv`, size_t `i`, size_t `j`)_\
Function: _void_ **R_qsort_int_I** _(int \*`iv`, int \*`I`, int `i`, int `j`)_

: These routines sort `v[i:j]` or `iv[i:j]` (using 1-indexing, i.e.,
`v[1]` is the first element) calling the quicksort algorithm as used
by R's `sort(v, method = "quick")` and documented on the help page
for the R function `sort`. The `..._I()` versions also return the
`sort.index()` vector in `I`. Note that the ordering is _not_
stable, so tied values may be permuted.

    Note that `NA`s are not handled (explicitly) and you should use
    different sorting functions if `NA`s can be present.

Function: _subroutine_ **qsort4** _(double precision `v`, integer `indx`, integer `ii`, integer `jj`)_\
Function: _subroutine_ **qsort3** _(double precision `v`, integer `ii`, integer `jj`)_

: The Fortran interface routines for sorting double precision vectors
are `qsort3` and `qsort4`, equivalent to `R_qsort` and `R_qsort_I`,
respectively.

Function: _void_ **R_max_col** _(double\* `matrix`, int\* `nr`, int\* `nc`, int\* `maxes`, int\* `ties_meth`)_

: Given the `nr` by `nc` matrix `matrix` in
column-major ("Fortran") order, `R_max_col()` returns in
`maxes[i-1]` the column number of the maximal element in the
`i`-th row (the same as R's `max.col()` function). In the
case of ties (multiple maxima), `*ties_meth` is an integer code in
`1:3` determining the method: 1 = "random", 2 = "first" and 3 =
"last". See R's help page `?max.col`.

Function: _int_ **findInterval** _(double\* `xt`, int `n`, double `x`, Rboolean `rightmost_closed`, Rboolean `all_inside`, int `ilo`, int\* `mflag`)_\
Function: _int_ **findInterval2(double\*** _`xt`, int `n`, double `x`, Rboolean `rightmost_closed`, Rboolean `all_inside`, Rboolean `left_open`, int `ilo`, int\* `mflag`)_

: Given the ordered vector `xt` of length `n`,
return the interval or index of `x` in `xt[]`, typically
max(_i_; 1 \<= i \<= `n` & _`xt`\[i\]_ \<=
`x`) where we use 1-indexing as in R and Fortran (but not
C). If `rightmost_closed` is true, also returns
_`n`-1_ if `x` equals
_`xt`\[`n`\]_. If `all_inside` is
not 0, the result is coerced to lie in `1:(n-1)` even when
`x` is outside the `xt`\[\] range. On return,
`*mflag` equals _-1_ if `x` \< `xt`\[1\], _+1_
if `x` \>= `xt`\[`n`\], and 0
otherwise.

    The algorithm is particularly fast when `ilo` is set to
    the last result of `findInterval()` and `x` is a value of
    a sequence which is increasing or decreasing for subsequent calls.

    `findInterval2()` is a generalization of `findInterval()`, with an
    extra `Rboolean` argument `left_open`. Setting
    `left_open = TRUE` basically replaces all left-closed right-open
    intervals t) by left-open ones t\], see the help page of R function
    `findInterval` for details.

    There is also an `F77_CALL(interv)()` version of `findInterval()`
    with the same arguments, but all pointers.

A system-independent interface to produce the name of a temporary file
is provided as

Function: \*char \*_ **R_tmpnam** _(const char \*`prefix`, const char \*`tmpdir`)*\
Function: *char \*_ **R_tmpnam2** _(const char \*`prefix`, const char \*`tmpdir`, const char \*`fileext`)\*

: Return a pathname for a temporary file with name beginning with
`prefix` and ending with `fileext` in
directory `tmpdir`. A `NULL` prefix or extension is
replaced by `""`. Note that the return value is dynamically
allocated and should be freed using `R_free_tmpnam` when no longer
needed (unlike the system call `tmpnam`). Freeing the result using
`free` is no longer recommended.

There is also the internal function used to expand file names in several
R functions, and called directly by `path.expand`.

Function: \*const char \*_ **R_ExpandFileName** _(const char \*`fn`)\*

: Expand a path name `fn` by replacing a leading tilde by
the user's home directory (if defined). The precise meaning is
platform-specific; it will usually be taken from the environment
variable `HOME` if this is defined.

For historical reasons there are Fortran interfaces to functions
`D1MACH` and `I1MACH`. These can be called from C code as e.g.
`F77_CALL(d1mach)(4)`. Note that these are emulations of the original
functions by Fox, Hall and Schryer on NetLib at
<http://www.netlib.org/slatec/src/> for IEC 60559 arithmetic (required
by R).

---

### 6.11 Re-encoding

R has its own C-level interface to the encoding conversion capabilities
provided by `iconv` because there are incompatibilities between the
declarations in different implementations of `iconv`.

These are declared in header file `R_ext/Riconv.h`.

Function: \*void \*_ **Riconv_open** _(const char \*`to`,
const char \*`from`)\*

Set up a pointer to an encoding object to be used to convert between two
encodings: `""` indicates the current locale.

Function: _size_t_ **Riconv** _(void \*`cd`, const char
\*\*`inbuf`, size_t \*`inbytesleft`, char
\*\*`outbuf`, size_t \*`outbytesleft`)_

Convert as much as possible of `inbuf` to `outbuf`. Initially the `int`
variables indicate the number of bytes available in the buffers, and
they are updated (and the `char` pointers are updated to point to the

### 6.12 Condition handling and cleanup code

Two functions are available for establishing condition handlers from
within C code:

```r
#include <Rinternals.h>

SEXP R_tryCatchError(SEXP (*fun)(void *data), void *data,
             SEXP (*hndlr)(SEXP cond, void *hdata), void *hdata);

SEXP R_tryCatch(SEXP (*fun)(void *data), void *data,
        SEXP,
        SEXP (*hndlr)(SEXP cond, void *hdata), void *hdata,
        void (*clean)(void *cdata), void *cdata);
```

`R_tryCatchError` establishes an exiting handler for conditions
inheriting form class `error`.

`R_tryCatch` can be used to establish a handler for other conditions and
to register a cleanup action. The conditions to be handled are specified
as a character vector (`STRSXP`). A `NULL` pointer can be passed as
`fun` or `clean` if condition handling or cleanup are not needed.

These are currently implemented using the R-level `tryCatch` mechanism
so are subject to some overhead.

The function `R_UnwindProtect` can be used to ensure that a cleanup
action takes place on ordinary return as well as on a non-local transfer
of control, which R implements as a `longjmp`.

```r
SEXP R_UnwindProtect(SEXP (*fun)(void *data), void *data,
                     void (*clean)(void *data, Rboolean jump), void *cdata,
                     SEXP cont);
```

`R_UnwindProtect` can be used in two ways. The simper usage, suitable
for use in C code, passes `NULL` for the `cont` argument.
`R_UnwindProtect` will call `fun(data)`. If `fun` returns a value, then
`R_UnwindProtect` calls `clean(cleandata, FALSE)` before returning the
value returned by `fun`. If `fun` executes a non-local transfer of
control, then `clean(cleandata, TRUE)` is called, and the non-local
transfer of control is resumed.

The second use pattern, suitable to support C++ stack unwinding, uses
two additional functions:

```r
SEXP R_MakeUnwindCont();
void NORET R_ContinueUnwind(SEXP cont);
```

`R_MakeUnwindCont` allocates a _continuation token_ `cont` to pass to
`R_UnwindProtect`. This token should be protected with `PROTECT` before
calling `R_UnwindProtect`. When the `clean` function is called with
`jump == TRUE`, indicating that R is executing a non-local transfer of
control, it can throw a C++ exception to a C++ `catch` outside the C++
code to be unwound, and then use the continuation token in the a call
`R_ContinueUnwind(cont)` to resume the non-local transfer of control
within R.

---

### 6.13 Allowing interrupts

No part of R can be interrupted whilst running long computations in
compiled code, so programmers should make provision for the code to be
interrupted at suitable points by calling from C

```r
#include <R_ext/Utils.h>

void R_CheckUserInterrupt(void);
```

and from Fortran

```r
subroutine rchkusr()
```

These check if the user has requested an interrupt, and if so branch to
R's error signaling functions.

Note that it is possible that the code behind one of the entry points
defined here if called from your C or Fortran code could be
interruptible or generate an error and so not return to your code.

---

### 6.14 Platform and version information

The header files define `USING_R`, which can be used to test if the code
is indeed being used with R.

Header file `Rconfig.h` (included by `R.h`) is used to
define platform-specific macros that are mainly for use in other header
files. The macro `WORDS_BIGENDIAN` is defined on
big-endian[^152^](#FOOT152) systems (e.g. most OSes on Sparc
and PowerPC hardware) and not on little-endian systems (nowadays all the
commoner R platforms). It can be useful when manipulating binary files.
NB: these macros apply only to the C compiler used to build R, not
necessarily to another C or C++ compiler.

Header file `Rversion.h` (**not** included by `R.h`)
defines a macro `R_VERSION` giving the version number encoded as an
integer, plus a macro `R_Version` to do the encoding. This can be used
to test if the version of R is late enough, or to include
back-compatibility features. For protection against very old versions of
R which did not have this macro, use a construction such as

```r
#if defined(R_VERSION) && R_VERSION >= R_Version(3, 1, 0)
  ...
#endif
```

More detailed information is available in the macros `R_MAJOR`,
`R_MINOR`, `R_YEAR`, `R_MONTH` and `R_DAY`: see the header file
`Rversion.h` for their format. Note that the minor version
includes the patchlevel (as in '`2.2`').

Packages which use `alloca` need to ensure it is defined: as it is part
of neither C nor POSIX there is no standard way to do so. One can use

```r
#include <Rconfig.h> // for HAVE_ALLOCA_H
#ifdef __GNUC__
// this covers gcc, clang, icc
# undef alloca
# define alloca(x) __builtin_alloca((x))
#elif defined(HAVE_ALLOCA_H)
// needed for native compilers on Solaris and AIX
# include <alloca.h>
#endif
```

(and this should be included before standard C headers such as
`stdlib.h`, since on some platforms these include
`malloc.h` which may have a conflicting definition), which
suffices for known R platforms.

---

### 6.15 Inlining C functions

The C99 keyword `inline` should be recognized by all compilers nowadays
used to build R. Portable code which might be used with earlier versions
of R can be written using the macro `R_INLINE` (defined in file
`Rconfig.h` included by `R.h`), as for example from
package [**cluster**](https://CRAN.R-project.org/package=cluster)

```r
#include <R.h>

static R_INLINE int ind_2(int l, int j)
{
...
}
```

Be aware that using inlining with functions in more than one compilation
unit is almost impossible to do portably, see
<http://www.greenend.org.uk/rjk/2003/03/inline.html>, so this usage is
for `static` functions as in the example. All the R configure code has
checked is that `R_INLINE` can be used in a single C file with the
compiler used to build R. We recommend that packages making extensive
use of inlining include their own configure code.

---

### 6.16 Controlling visibility

Header `R_ext/Visibility.h` has some definitions for
controlling the visibility of entry points. These are only effective
when '`HAVE_VISIBILITY_ATTRIBUTE`' is defined -- this is
checked when R is configured and recorded in header `Rconfig.h`
(included by `R_ext/Visibility.h`). It is often defined on
modern Unix-alikes with a recent compiler[^153^](#FOOT153),
but not supported on macOS nor Windows. Minimizing the visibility of
symbols in a shared library will both speed up its loading (unlikely to
be significant) and reduce the possibility of linking to other entry
points of the same name.

C/C++ entry points prefixed by `attribute_hidden` will not be visible in
the shared object. There is no comparable mechanism for Fortran entry
points, but there is a more comprehensive scheme used by, for example
package **stats**. Most compilers which allow control of visibility will
allow control of visibility for all symbols _via_ a flag, and where
known the flag is encapsulated in the macros '`C_VISIBILITY`',
'`CXX_VISIBILITY`'[^154^](#FOOT154) and
'`F_VISIBILITY`' for C, C++ and Fortran
compilers.[^155^](#FOOT155) These are defined in
`etc/Makeconf` and so available for normal compilation of
package code. For example, `src/Makevars` could include some of

```r
PKG_CFLAGS=$(C_VISIBILITY)
PKG_CXXFLAGS=$(CXX_VISIBILITY)
PKG_FFLAGS=$(F_VISIBILITY)
```

This would end up with **no** visible entry points, which would be
pointless. However, the effect of the flags can be overridden by using
the `attribute_visible` prefix. A shared object which registers its
entry points needs only for have one visible entry point, its
initializer, so for example package **stats** has

```r
void attribute_visible R_init_stats(DllInfo *dll)
{
    R_registerRoutines(dll, CEntries, CallEntries, FortEntries, NULL);
    R_useDynamicSymbols(dll, FALSE);
...
}
```

Because the '`C_VISIBILITY`' mechanism is only useful in
conjunction with `attribute_visible`, it is not enabled unless
'`HAVE_VISIBILITY_ATTRIBUTE`' is defined. The usual visibility
flag is `-fvisibility=hidden`: some compilers also support
`-fvisibility-inlines-hidden` which can be used by overriding
'`C_VISIBILITY`' and '`CXX_VISIBILITY`' in
`config.site` when building R, or editing
`etc/Makeconf` in the R installation.

Note that `configure` only checks that visibility attributes and flags
are accepted, not that they actually hide symbols.

The visibility mechanism is not available on Windows, but there is an
equally effective way to control which entry points are visible, by
supplying a definitions file `pkgnme/src/pkgname-win.def`: only
entry points listed in that file will be visible. Again using **stats**
as an example, it has

```r
LIBRARY stats.dll
EXPORTS
 R_init_stats
```

---

### 6.17 Using these functions in your own C code

It is possible to build `Mathlib`, the R set of mathematical functions
documented in `Rmath.h`, as a standalone library
`libRmath` under both Unix-alikes and Windows. (This includes
the functions documented in [Numerical analysis subroutines](#Numerical-analysis-subroutines) as from that header file.)

The library is not built automatically when R is installed, but can be
built in the directory `src/nmath/standalone` in the R sources:
see the file `README` there. To use the code in your own C
program include

```r
#define MATHLIB_STANDALONE
#include <Rmath.h>
```

and link against '`-lRmath`' (and perhaps '`-lm`').
There is an example file `test.c`.

A little care is needed to use the random-number routines. You will need
to supply the uniform random number generator

```r
double unif_rand(void)
```

or use the one supplied (and with a dynamic library or DLL you will have
to use the one supplied, which is the Marsaglia-multicarry with an entry
points

```r
set_seed(unsigned int, unsigned int)
```

to set its seeds and

```r
get_seed(unsigned int *, unsigned int *)
```

to read the seeds).

---

### 6.18 Organization of header files

The header files which R installs are in directory
`R_INCLUDE_DIR` (default `R_HOME/include`). This
currently includes

> ---
>
> `R.h` includes many other files
> `S.h` different version for code ported from S
> `Rinternals.h` definitions for using R's internal structures
> `Rdefines.h` macros for an S-like interface to the above (no longer maintained)
> `Rmath.h` standalone math library
> `Rversion.h` R version information
> `Rinterface.h` for add-on front-ends (Unix-alikes only)
> `Rembedded.h` for add-on front-ends
> `R_ext/Applic.h` optimization and integration
> `R_ext/BLAS.h` C definitions for BLAS routines
> `R_ext/Callbacks.h` C (and R function) top-level task handlers
> `R_ext/GetX11Image.h` X11Image interface used by package **trkplot** > `R_ext/Lapack.h` C definitions for some LAPACK routines
> `R_ext/Linpack.h` C definitions for some LINPACK routines, not all of which are included in R
> `R_ext/Parse.h` a small part of R's parse interface: not part of the stable API.
> `R_ext/RStartup.h` for add-on front-ends
> `R_ext/Rdynload.h` needed to register compiled code in packages
> `R_ext/R-ftp-http.h` interface to internal method of `download.file` > `R_ext/Riconv.h` interface to `iconv` > `R_ext/Visibility.h` definitions controlling visibility
> `R_ext/eventloop.h` for add-on front-ends and for packages that need to share in the R event loops (not Windows)
>
> ---

The following headers are included by `R.h`:

> ---
>
> `Rconfig.h` configuration info that is made available
> `R_ext/Arith.h` handling for `NA`s, `NaN`s, `Inf`/`-Inf` > `R_ext/Boolean.h` `TRUE`/`FALSE` type
> `R_ext/Complex.h` C typedefs for R's `complex` > `R_ext/Constants.h` constants
> `R_ext/Error.h` error signaling
> `R_ext/Memory.h` memory allocation
> `R_ext/Print.h` `Rprintf` and variations.
> `R_ext/RS.h` definitions common to `R.h` and `S.h`, including `F77_CALL` etc.
> `R_ext/Random.h` random number generation
> `R_ext/Utils.h` sorting and other utilities
> `R_ext/libextern.h` definitions for exports from `R.dll` on Windows.
>
> ---

The graphics systems are exposed in headers
`R_ext/GraphicsEngine.h`, `R_ext/GraphicsDevice.h`
(which it includes) and `R_ext/QuartzDevice.h`. Facilities for
defining custom connection implementations are provided in
`R_ext/Connections.h`, but make sure you consult the file
before use.

Let us re-iterate the advice to include system headers before the R
header files, especially `Rinternals.h` (included by
`Rdefines.h`) and `Rmath.h`, which redefine names
which may be used in system headers (fewer if '`R_NO_REMAP`' is
defined, or '`R_NO_REMAP_RMATH`' for `Rmath.h`).

---
