5 System and foreign language interfaces

---

---

• [Operating system access](#Operating-system-access)     
 • [Interface functions .C and .Fortran](#Interface-functions-_002eC-and-_002eFortran)     
 • [dyn.load and dyn.unload](#dyn_002eload-and-dyn_002eunload)     
 • [Registering native routines](#Registering-native-routines)     
 • [Creating shared objects](#Creating-shared-objects)     
 • [Interfacing C++ code](#Interfacing-C_002b_002b-code)     
 • [Fortran I/O](#Fortran-I_002fO)     
 • [Linking to other packages](#Linking-to-other-packages)     
 • [Handling R objects in C](#Handling-R-objects-in-C)     
 • [Interface functions .Call and .External](#Interface-functions-_002eCall-and-_002eExternal)     
 • [Evaluating R expressions from C](#Evaluating-R-expressions-from-C)     
 • [Parsing R code from C](#Parsing-R-code-from-C)     
 • [External pointers and weak references](#External-pointers-and-weak-references)     
 • [Vector accessor functions](#Vector-accessor-functions)     
 • [Character encoding issues](#Character-encoding-issues)

---

---

### 5.1 Operating system access

Access to operating system functions is _via_ the R functions `system`
and `system2`. The details will
differ by platform (see the on-line help), and about all that can safely
be assumed is that the first argument will be a string `command` that
will be passed for execution (not necessarily by a shell) and the second
argument to `system` will be `internal` which if true will collect the
output of the command into an R character vector.

On POSIX-compliant OSes these commands pass a command-line to a shell:
Windows is not POSIX-compliant and there is a separate function `shell`
to do so.

The function `system.time` is available for
timing. Timing on child processes is only available on Unix-alikes, and
may not be reliable there.

---

### 5.2 Interface functions `.C` and `.Fortran`

These two functions provide an interface to compiled code that has been
linked into R, either at build time or _via_ `dyn.load` (see [dyn.load
and dyn.unload](#dyn_002eload-and-dyn_002eunload)). They are primarily
intended for compiled C and Fortran code respectively, but the `.C`
function can be used with other languages which can generate C
interfaces, for example C++ (see [Interfacing C++ code](#Interfacing-C_002b_002b-code)).

The first argument to each function is a character string specifying the
symbol name as known[^126^](#FOOT126) to C or Fortran, that is
the function or subroutine name. (That the symbol is loaded can be
tested by, for example, `is.loaded("cg")`. Use the name you pass to `.C`
or `.Fortran` rather than the translated symbol name.)

There can be up to 65 further arguments giving R objects to be passed to
compiled code. Normally these are copied before being passed in, and
copied again to an R list object when the compiled code returns. If the
arguments are given names, these are used as names for the components in
the returned list object (but not passed to the compiled code).

The following table gives the mapping between the modes of R atomic
vectors and the types of arguments to a C function or Fortran
subroutine.

> R storage mode C type Fortran type
>
> ---
>
> `logical` `int *` `INTEGER` > `integer` `int *` `INTEGER` > `double` `double *` `DOUBLE PRECISION` > `complex` `Rcomplex *` `DOUBLE COMPLEX` > `character` `char **` `CHARACTER(255)` > `raw` `unsigned char *` none

On all R platforms `int` and `INTEGER` are 32-bit. Code ported from
S-PLUS (which uses `long *` for `logical` and `integer`) will not work
on all 64-bit platforms (although it may appear to work on some,
including Windows). Note also that if your compiled code is a mixture of
C functions and Fortran subprograms the argument types must match as
given in the table above.

C type `Rcomplex` is a structure with `double` members `r` and `i`
defined in the header file `R_ext/Complex.h` included by
`R.h`. (On most platforms this is stored in a way compatible
with the C99 `double complex` type: however, it may not be possible to
pass `Rcomplex` to a C99 function expecting a `double complex` argument.
Nor need it be compatible with a C++ `complex` type. Moreover, the
compatibility can depend on the optimization level set for the
compiler.)

Only a single character string of fixed length can be passed to or from
Fortran (the length is not passed), and the success of this is
compiler-dependent: its use was formally deprecated in 2019. Other R
objects can be passed to `.C`, but it is much better to use one of the
other interfaces.

It is possible to pass numeric vectors of storage mode `double` to C as
`float *` or to Fortran as `REAL` by setting the attribute `Csingle`,
most conveniently by using the R functions `as.single`, `single` or
`mode`. This is intended only to be used to aid interfacing existing C
or Fortran code.

Logical values are sent as `0` (`FALSE`), `1` (`TRUE`) or
`INT_MIN = -2147483648` (`NA`, but only if `NAOK` is true), and the
compiled code should return one of these three values. (Non-zero values
other than `INT_MIN` are mapped to `TRUE`.)

Unless formal argument `NAOK` is true, all the other arguments are
checked for missing values `NA` and for the IEEE special values `NaN`,
`Inf` and `-Inf`, and the presence of any of these generates an error.
If it is true, these values are passed unchecked.

Argument `PACKAGE` confines the search for the symbol name to a specific
shared object (or use `"base"` for code compiled into R). Its use is
highly desirable, as there is no way to avoid two package writers using
the same symbol name, and such name clashes are normally sufficient to
cause R to crash. (If it is not present and the call is from the body of
a function defined in a package namespace, the shared object loaded by
the first (if any) `useDynLib` directive will be used.

Note that the compiled code should not return anything except through
its arguments: C functions should be of type `void` and Fortran
subprograms should be subroutines.

To fix ideas, let us consider a very simple example which convolves two
finite sequences. (This is hard to do fast in interpreted R code, but
easy in C code.) We could do this using `.C` by

```r
void convolve(double *a, int *na, double *b, int *nb, double *ab)
{
    int nab = *na + *nb - 1;

    for(int i = 0; i < nab; i++)
        ab[i] = 0.0;
    for(int i = 0; i < *na; i++)
        for(int j = 0; j < *nb; j++)
            ab[i + j] += a[i] * b[j];
}
```

called from R by

```r
conv <- function(a, b)
    .C("convolve",
       as.double(a),
       as.integer(length(a)),
       as.double(b),
       as.integer(length(b)),
       ab = double(length(a) + length(b) - 1))$ab
```

Note that we take care to coerce all the arguments to the correct R
storage mode before calling `.C`; mistakes in matching the types can
lead to wrong results or hard-to-catch errors.

Special care is needed in handling `character` vector arguments in C (or
C++). On entry the contents of the elements are duplicated and assigned
to the elements of a `char **` array, and on exit the elements of the C
array are copied to create new elements of a character vector. This
means that the contents of the character strings of the `char **` array
can be changed, including to `\0` to shorten the string, but the strings
cannot be lengthened. It is possible[^127^](#FOOT127) to
allocate a new string _via_ `R_alloc` and replace an entry in the
`char **` array by the new string. However, when character vectors are
used other than in a read-only way, the `.Call` interface is much to be
preferred.

Passing character strings to Fortran code needs even more care, is
deprecated and should be avoided where possible. Only the first element
of the character vector is passed in, as a fixed-length (255) character
array. Up to 255 characters are passed back to a length-one character
vector. How well this works (or even if it works at all) depends on the
C and Fortran compilers on each platform (including on their options).
Often what is being passed to Fortran is one of a small set of possible
values (a factor in R terms) which could alternatively be passed as an
integer code: similarly Fortran code that wants to generate diagnostic
messages could pass an integer code to a C or R wrapper which would
convert it to a character string.

It is possible to pass some R objects other than atomic vectors _via_
`.C`, but this is only supported for historical compatibility: use the
`.Call` or `.External` interfaces for such objects. Any C/C++ code that
includes `Rinternals.h` should be called _via_ `.Call` or
`.External`.

---

### 5.3 `dyn.load` and `dyn.unload`

Compiled code to be used with R is loaded as a shared object
(Unix-alikes including macOS, see [Creating shared objects](#Creating-shared-objects) for more information) or DLL
(Windows).

The shared object/DLL is loaded by `dyn.load` and unloaded by
`dyn.unload`. Unloading is not normally necessary and is not safe in
general, but it is needed to allow the DLL to be re-built on some
platforms, including Windows. Unloading a DLL and then re-loading a DLL
of the same name may not work: Solaris uses the first version loaded. A
DLL that registers C finalizers, but fails to unregister them when
unloaded, may cause R to crash after unloading.

The first argument to both functions is a character string giving the
path to the object. Programmers should not assume a specific file
extension for the object/DLL (such as `.so`) but use a
construction like

```r
file.path(path1, path2, paste0("mylib", .Platform$dynlib.ext))
```

for platform independence. On Unix-alike systems the path supplied to
`dyn.load` can be an absolute path, one relative to the current
directory or, if it starts with '`~`', relative to the user's
home directory.

Loading is most often done automatically based on the `useDynLib()`
declaration in the `NAMESPACE` file, but may be done explicitly
_via_ a call to `library.dynam`. This has
the form

```r
library.dynam("libname", package, lib.loc)
```

where `libname` is the object/DLL name _with the extension omitted_.
Note that the first argument, `chname`, should **not** be `package`
since this will not work if the package is installed under another name.

Under some Unix-alike systems there is a choice of how the symbols are
resolved when the object is loaded, governed by the arguments `local`
and `now`. Only use these if really necessary: in particular using
`now=FALSE` and then calling an unresolved symbol will terminate R
unceremoniously.

R provides a way of executing some code automatically when a object/DLL
is either loaded or unloaded. This can be used, for example, to register
native routines with R's dynamic symbol mechanism, initialize some data
in the native code, or initialize a third party library. On loading a
DLL, R will look for a routine within that DLL named `R_init_lib` where
`lib`{.variable} is the name of the DLL file with the extension removed.
For example, in the command

```r
library.dynam("mylib", package, lib.loc)
```

R looks for the symbol named `R_init_mylib`. Similarly, when unloading
the object, R looks for a routine named `R_unload_lib`, e.g.,
`R_unload_mylib`. In either case, if the routine is present, R will
invoke it and pass it a single argument describing the DLL. This is a
value of type `DllInfo` which is defined in the `Rdynload.h`
file in the `R_ext` directory.

Note that there are some implicit restrictions on this mechanism as the
basename of the DLL needs to be both a valid file name and valid as part
of a C entry point (e.g. it cannot contain '`.`'): for portable
code it is best to confine DLL names to be ASCII alphanumeric plus
underscore. If entry point `R_init_lib` is not found it is also looked
for with '`.`' replaced by '`_`'.

The following example shows templates for the initialization and unload
routines for the `mylib` DLL.

> +-----------------------------------------------------------------------+
> | |
> | `r | | #include <R_ext/Rdynload.h> | | | | void | | R_init_mylib(DllInfo *info) | | { | | /* Register routines, | | allocate resources. */ | | } | | | | void | | R_unload_mylib(DllInfo *info) | | { | | /* Release resources. */ | | } | |` |
> | ::: |
> +-----------------------------------------------------------------------+

If a shared object/DLL is loaded more than once the most recent version
is used.[^128^](#FOOT128) More generally, if the same symbol
name appears in several shared objects, the most recently loaded
occurrence is used. The `PACKAGE` argument and registration (see the

### 5.4 Registering native routines

---

• [Speed considerations](#Speed-considerations)     
 • [Converting a package to use registration](#Converting-a-package-to-use-registration)     
 • [Linking to native routines in other packages](#Linking-to-native-routines-in-other-packages)

---

By 'native' routine, we mean an entry point in compiled code.

In calls to `.C`, `.Call`, `.Fortran` and `.External`, R must locate the
specified native routine by looking in the appropriate shared
object/DLL. By default, R uses the operating-system-specific dynamic
loader to lookup the symbol in all[^129^](#FOOT129) loaded
DLLs and the R executable or libraries it is linked to. Alternatively,
the author of the DLL can explicitly register routines with R and use a
single, platform-independent mechanism for finding the routines in the
DLL. One can use this registration mechanism to provide additional
information about a routine, including the number and type of the
arguments, and also make it available to R programmers under a different
name.

Registering routines has two main advantages: it provides a
faster[^130^](#FOOT130) way to find the address of the entry
point _via_ tables stored in the DLL at compilation time, and it
provides a run-time check that the entry point is called with the right
number of arguments and, optionally, the right argument types.

To register routines with R, one calls the C routine
`R_registerRoutines`. This is typically done when the DLL is first
loaded within the initialization routine `R_init_dll name` described in
[dyn.load and dyn.unload](#dyn_002eload-and-dyn_002eunload).
`R_registerRoutines` takes 5 arguments. The first is the `DllInfo`
object passed by R to the initialization routine. This is where R stores
the information about the methods. The remaining 4 arguments are arrays
describing the routines for each of the 4 different interfaces: `.C`,
`.Call`, `.Fortran` and `.External`. Each argument is a
`NULL`-terminated array of the element types given in the following
table:

> ---
>
> `.C` `R_CMethodDef` > `.Call` `R_CallMethodDef` > `.Fortran` `R_FortranMethodDef` > `.External` `R_ExternalMethodDef`
>
> ---

Currently, the `R_ExternalMethodDef` type is the same as
`R_CallMethodDef` type and contains fields for the name of the routine
by which it can be accessed in R, a pointer to the actual native symbol
(i.e., the routine itself), and the number of arguments the routine
expects to be passed from R. For example, if we had a routine named
`myCall` defined as

```r
SEXP myCall(SEXP a, SEXP b, SEXP c);
```

we would describe this as

```r
static const R_CallMethodDef callMethods[]  = {
  {"myCall", (DL_FUNC) &myCall, 3},
  {NULL, NULL, 0}
};
```

along with any other routines for the `.Call` interface. For routines
with a variable number of arguments invoked _via_ the `.External`
interface, one specifies `-1` for the number of arguments which tells R
not to check the actual number passed.

Routines for use with the `.C` and `.Fortran` interfaces are described
with similar data structures, but which have two additional fields for
describing the type and "style" of each argument. Each of these can be
omitted. However, if specified, each should be an array with the same
number of elements as the number of parameters for the routine. The
types array should contain the `SEXP` types describing the expected type
of the argument. (Technically, the elements of the types array are of
type `R_NativePrimitiveArgType` which is just an unsigned integer.) The
R types and corresponding type identifiers are provided in the following
table:

> ---
>
> `numeric` `REALSXP` > `integer` `INTSXP` > `logical` `LGLSXP` > `single` `SINGLESXP` > `character` `STRSXP` > `list` `VECSXP`
>
> ---

Consider a C routine, `myC`, declared as

```r
void myC(double *x, int *n, char **names, int *status);
```

We would register it as

```r
static R_NativePrimitiveArgType myC_t[] = {
    REALSXP, INTSXP, STRSXP, LGLSXP
};

static const R_CMethodDef cMethods[] = {
   {"myC", (DL_FUNC) &myC, 4, myC_t},
   {NULL, NULL, 0, NULL}
};
```

Note that `.Fortran` entry points are mapped to lowercase, so
registration should use lowercase only.

Having created the arrays describing each routine, the last step is to
actually register them with R. We do this by calling
`R_registerRoutines`. For example, if we have the descriptions above for
the routines accessed by the `.C` and `.Call` we would use the following
code:

```r
void
R_init_myLib(DllInfo *info)
{
   R_registerRoutines(info, cMethods, callMethods, NULL, NULL);
}
```

This routine will be invoked when R loads the shared object/DLL named
`myLib`. The last two arguments in the call to `R_registerRoutines` are
for the routines accessed by `.Fortran` and `.External` interfaces. In
our example, these are given as `NULL` since we have no routines of
these types.

When R unloads a shared object/DLL, its registrations are removed. There
is no other facility for unregistering a symbol.

Examples of registering routines can be found in the different packages
in the R source tree (e.g., **stats** and **graphics**). Also, there is
a brief, high-level introduction in _R News_ (volume 1/3, September
2001, pages 20--23,
<https://www.r-project.org/doc/Rnews/Rnews_2001-3.pdf>).

Once routines are registered, they can be referred to as R objects if
this is arranged in the `useDynLib` call in the package's
`NAMESPACE` file (see [useDynLib](#useDynLib)). So for example
the **stats** package has

```r
# Refer to all C/Fortran routines by their name prefixed by C_
useDynLib(stats, .registration = TRUE, .fixes = "C_")
```

in its `NAMESPACE` file, and then `ansari.test`'s default
methods can contain

```r
        pansari <- function(q, m, n)
            .C(C_pansari, as.integer(length(q)), p = as.double(q),
                as.integer(m), as.integer(n))$p
```

This avoids the overhead of looking up an entry point each time it is
used, and ensures that the entry point in the package is the one used
(without a `PACKAGE = "pkg"` argument).

`R_init_` routines are often of the form

```r
void attribute_visible R_init_mypkg(DllInfo *dll)
{
    R_registerRoutines(dll, CEntries, CallEntries, FortEntries,
                       ExternalEntries);
    R_useDynamicSymbols(dll, FALSE);
    R_forceSymbols(dll, TRUE);
...
}
```

The
`R_useDynamicSymbols` call says the DLL is not to be searched for entry
points specified by character strings so `.C` etc calls will only find
registered symbols: the `R_forceSymbols` call only allows `.C` etc calls
which specify entry points by R objects such as `C_pansari` (and not by
character strings). Each provides some protection against accidentally
finding your entry points when people supply a character string without
a package, and avoids slowing down such searches. (For the visibility
attribute see [Controlling visibility](#Controlling-visibility).)

In more detail, if a package `mypkg` contains entry points `reg` and
`unreg` and the first is registered as a 0-argument `.Call` routine, we
could use (from code in the package)

```r
.Call("reg")
.Call("unreg")
```

Without or with registration, these will both work. If `R_init_mypkg`
calls `R_useDynamicSymbols(dll, FALSE)`, only the first will work. If in
addition to registration the `NAMESPACE` file contains

```r
useDynLib(mypkg, .registration = TRUE, .fixes = "C_")
```

then we can call `.Call(C_reg)`. Finally, if `R_init_mypkg` also calls
`R_forceSymbols(dll, TRUE)`, only `.Call(C_reg)` will work (and not
`.Call("reg")`). This is usually what we want: it ensures that all of
our own `.Call` calls go directly to the intended code in our package
and that no one else accidentally finds our entry points. (Should
someone need to call our code from outside the package, for example for
debugging, they can use `.Call(mypkg:::C_reg)`.)

---

#### 5.4.1 Speed considerations

Sometimes registering native routines or using a `PACKAGE` argument can
make a large difference. The results can depend quite markedly on the OS
(and even if it is 32- or 64-bit), on the version of R and what else is
loaded into R at the time.

To fix ideas, first consider `x86_64` OS 10.7 and R 2.15.2. A simple
`.Call` function might be

```r
foo <- function(x) .Call("foo", x)
```

with C code

```r
#include <Rinternals.h>

SEXP foo(SEXP x)
{
    return x;
}
```

If we compile with by `R CMD SHLIB foo.c`, load the code by
`dyn.load("foo.so")` and run `foo(pi)` it took around 22 microseconds
(us). Specifying the DLL by

```r
foo2 <- function(x) .Call("foo", x, PACKAGE = "foo")
```

reduced the time to 1.7 us.

Now consider making these functions part of a package whose
`NAMESPACE` file uses `useDynlib(foo)`. This immediately
reduces the running time as `"foo"` will be preferentially looked for
`foo.dll`. Without specifying `PACKAGE` it took about 5 us (it
needs to fathom out the appropriate DLL each time it is invoked but it
does not need to search all DLLs), and with the `PACKAGE` argument it is
again about 1.7 us.

then the address for the native routine is looked up just once when the
package is loaded, and `foo3(pi)` takes about 0.8 us.

Versions using `.C()` rather than `.Call()` took about 0.2 us longer.

These are all quite small differences, but C routines are not uncommonly
invoked millions of times for run times of a few microseconds each, and
those doing such things may wish to be aware of the differences.

On Linux and Solaris there is a smaller overhead in looking up symbols.

Symbol lookup on Windows used to be far slower, so R maintains a small
cache. If the cache is currently empty enough that the symbol can be
stored in the cache then the performance is similar to Linux and
Solaris: if not it may be slower. R's own code always uses registered
symbols and so these never contribute to the cache: however many other
packages do rely on symbol lookup.

In more recent versions of R all the standard packages register native
symbols and do not allow symbol search, so in a new session `foo()` can
only look in `foo.so` and may be as fast as `foo2()`. This will
no longer apply when many contributed packages are loaded, and generally
those last loaded are searched first. For example, consider R 3.3.2 on
x86_64 Linux. In an empty R session, both `foo()` and `foo2()` took
about 0.75 us; however after packages
[**igraph**](https://CRAN.R-project.org/package=igraph) and
[**spatstat**](https://CRAN.R-project.org/package=spatstat) had been
loaded (which loaded another 12 DLLs), `foo()` took 3.6 us but `foo2()`
still took about 0.80 us. Using registration in a package reduced this
to 0.55 us and `foo3()` took 0.40 us, times which were unchanged when
further packages were loaded.

---

#### 5.4.2 Example: converting a package to use registration

The **splines** package was converted to use symbol registration in
2001, but we can use it as an example[^131^](#FOOT131) of what
needs to be done for a small package.

- Find the relevant entry points. This is somewhat OS-specific, but
  something like the following should be possible at the OS
  command-line

```r
nm -g /path/to/splines.so | grep " T "
0000000000002670 T _spline_basis
0000000000001ec0 T _spline_value
```

This indicates that there are two relevant entry points. (They may
or may not have a leading underscore, as here. Fortran entry points
will have a trailing underscore.) Check in the R code that they are
called by the package and how: in this case they are used by
`.Call`.

Alternatively, examine the package's R code for all `.C`,
`.Fortran`, `.Call` and `.External` calls.

- Construct the registration table. First write skeleton registration
  code, conventionally in file `src/init.c` (or at the end of
  the only C source file in the package: if included in a C++ file the
  '`R_init`' function would need to be declared
  `extern "C"`):

```r
#include <stdlib.h> // for NULL
#include <R_ext/Rdynload.h>

#define CALLDEF(name, n)

static const R_CallMethodDef R_CallDef[] = {
   CALLDEF(spline_basis, ?),
   CALLDEF(spline_value, ?),
   {NULL, NULL, 0}
};

void R_init_splines(DllInfo *dll)
{
    R_registerRoutines(dll, NULL, R_CallDef, NULL, NULL);
}
```

and then replace the `?` in the skeleton with the actual numbers of
arguments. You will need to add declarations (also known as
'prototypes') of the functions unless appending to the only C source
file. Some packages will already have these in a header file, or you
could create one and include it in `init.c`, for example
`splines.h` containing

```r
#include <Rinternals.h> // for SEXP
extern SEXP spline_basis(SEXP knots, SEXP order, SEXP xvals, SEXP derivs);
extern SEXP spline_value(SEXP knots, SEXP coeff, SEXP order, SEXP x, SEXP deriv);
```

Tools are available to extract declarations, at least for C and C++
code: see the help file for
`package_native_routine_registration_skeleton` in package **tools**.
Here we could have used

```r
cproto -I/path/to/R/include -e splines.c
```

For examples of registering other types of calls, see packages
**graphics** and **stats**. In particular, when registering entry
points for `.Fortran` one needs declarations as if called from C,
such as

```r
#include <R_ext/RS.h>
void F77_NAME(supsmu)(int *n, double *x, double *y,
                      double *w, int *iper, double *span, double *alpha,
                      double *smo, double *sc, double *edf);
```

`gfortran` 9.2[^132^](#FOOT132) and later can help
generate such prototypes with its flag
`-fc-prototypes-external` (although one will need to
replace the hard-coded trailing underscore with the `F77_NAME`
macro).

One can get away with inaccurate argument lists in the declarations:
it is easy to specify the arguments for `.Call` (all `SEXP`) and
`.External` (one `SEXP`) and as the arguments for `.C` and
`.Fortran` are all pointers, specifying them as `void *` suffices.
(For most platforms one can omit all the arguments, although
link-time optimization will warn.)

- (Optional but highly recommended.) Restrict `.Call` etc to use the
  symbols you chose to register by editing `src/init.c` to
  contain

  ```r
  void R_init_splines(DllInfo *dll)
  {
      R_registerRoutines(dll, NULL, R_CallDef, NULL, NULL);
      R_useDynamicSymbols(dll, FALSE);
  }
  ```

A skeleton for the steps so far can be made using
`package_native_routine_registration_skeleton` in package **tools**.
This will optionally create declarations based on the usage in the R
code.

The remaining steps are optional but recommended.

- Edit the `NAMESPACE` file to create R objects for the
  registered symbols:

```r
useDynLib(splines, .registration = TRUE, .fixes = "C_")
```

- Find all the relevant calls in the R code and edit them to use the R
  objects. This entailed changing the lines

```r
temp <- .Call("spline_basis", knots, ord, x, derivs, PACKAGE = "splines")
y[accept] <- .Call("spline_value", knots, coeff, ord, x[accept], deriv, PACKAGE = "splines")
y = .Call("spline_value", knots, coef(object), ord, x, deriv, PACKAGE = "splines")
```

to

```r
temp <- .Call(C_spline_basis, knots, ord, x, derivs)
y[accept] <- .Call(C_spline_value, knots, coeff, ord, x[accept], deriv)
y = .Call(C_spline_value, knots, coef(object), ord, x, deriv)
```

Check that there is no `exportPattern` directive which
unintentionally exports the newly created R objects.

- Restrict `.Call` to use the R symbols by editing
  `src/init.c` to contain

```r
void R_init_splines(DllInfo *dll)
{
    R_registerRoutines(dll, NULL, R_CallDef, NULL, NULL);
    R_useDynamicSymbols(dll, FALSE);
    R_forceSymbols(dll, TRUE);
}
```

- Consider visibility. On some OSes we can hide entry points from the
  loader, which precludes any possible name clashes and calling them
  accidentally (usually with incorrect arguments and crashing the R
  process). If we repeat the first step we now see

```r
nm -g /path/to/splines.so | grep " T "
0000000000002e00 T _R_init_splines
00000000000025e0 T _spline_basis
0000000000001e20 T _spline_value
```

If there were any entry points not intended to be used by the
package we should try to avoid exporting them, for example by making
them `static`. Now that the two relevant entry points are only
accessed _via_ the registration table, we can hide them. There are
two ways to do so on some Unix-alikes. We can hide individual entry
points _via_

```r
#include <R_ext/Visibility.h>

SEXP attribute_hidden
spline_basis(SEXP knots, SEXP order, SEXP xvals, SEXP derivs)
…

SEXP attribute_hidden
spline_value(SEXP knots, SEXP coeff, SEXP order, SEXP x, SEXP deriv)
…
```

Alternatively, we can change the default visibility for all C
symbols by including

```r
PKG_CFLAGS = $(C_VISIBILITY)
```

in `src/Makevars`, and then we need to allow registration
by declaring `R_init_splines` to be visible:

```r
#include <R_ext/Visibility.h>

void attribute_visible
R_init_splines(DllInfo *dll)
…
```

See [Controlling visibility](#Controlling-visibility) for more
details, including using Fortran code and ways to restrict
visibility on Windows.

- We end up with a file `src/init.c` containing

  > +-----------------------------------------------------------------------+
  > | |
  > | `r | | #include <stdlib.h> | | #include <R_ext/Rdynload.h> | | #include <R_ext/Visibility.h> // optional | | | | #include "splines.h" | | | | #define CALLDEF(name, n) | | | | static const R_CallMethodDef R_CallDef[] = { | | CALLDEF(spline_basis, 4), | | CALLDEF(spline_value, 5), | | {NULL, NULL, 0} | | }; | | | | void | | attribute_visible // optional | | R_init_splines(DllInfo *dll) | | { | | R_registerRoutines(dll, NULL, R_CallDef, NULL, NULL); | | R_useDynamicSymbols(dll, FALSE); | | R_forceSymbols(dll, TRUE); | | } | |` |
  > | ::: |
  > +-----------------------------------------------------------------------+

---

#### 5.4.3 Linking to native routines in other packages

In addition to registering C routines to be called by R, it can at times
be useful for one package to make some of its C routines available to be
called by C code in another package. The interface consists of two
routines declared in header `R_ext/Rdynload.h` as

```r
void R_RegisterCCallable(const char *package, const char *name,
                         DL_FUNC fptr);
DL_FUNC R_GetCCallable(const char *package, const char *name);
```

A package **packA** that wants to make a C routine `myCfun` available to
C code in other packages would include the call

```r
R_RegisterCCallable("packA", "myCfun", myCfun);
```

in its initialization function `R_init_packA`. A package **packB** that
wants to use this routine would retrieve the function pointer with a
call of the form

```r
p_myCfun = R_GetCCallable("packA", "myCfun");
```

The author of **packB** is responsible for ensuring that `p_myCfun` has
an appropriate declaration. In the future R may provide some automated
tools to simplify exporting larger numbers of routines.

A package that wishes to make use of header files in other packages
needs to declare them as a comma-separated list in the field
'`LinkingTo`' in the `DESCRIPTION` file. This then
arranges for the `include` directories in the installed
linked-to packages to be added to the include paths for C and C++ code.

It must specify[^133^](#FOOT133) '`Imports`' or
'`Depends`' of those packages, for they have to be
loaded[^134^](#FOOT134) prior to this one (so the path to
their compiled code has been registered).

CRAN examples of the use of this mechanism include
[**coxme**](https://CRAN.R-project.org/package=coxme) linking to
[**bdsmatrix**](https://CRAN.R-project.org/package=bdsmatrix) and
[**xts**](https://CRAN.R-project.org/package=xts) linking to
[**zoo**](https://CRAN.R-project.org/package=zoo).

---

### 5.5 Creating shared objects

Shared objects for loading into R can be created using `R CMD SHLIB`.
This accepts as arguments a list of files which must be object files
(with extension `.o`) or sources for C, C++, Fortran, Objective
C or Objective C++ (with extensions `.c`, `.cc` or
`.cpp`, `.f` (fixed-form Fortran), `.f90` or
`.f95` (free-form), `.m`, and `.mm` or
`.M`, respectively), or commands to be passed to the linker.
See [R CMD SHLIB \--help]{.kbd} (or the R help for `SHLIB`) for usage
information. Note that files intended for the Fortran pre-processor with
extension `.F` are not accepted.

If compiling the source files does not work "out of the box", you can
specify additional flags by setting some of the variables
`PKG_CPPFLAGS` (for the C/C++ preprocessor,
mainly '`-I`', '`-D`' and '`-U`' flags),

`PKG_CFLAGS`, `PKG_CXXFLAGS`,
`PKG_FFLAGS`, `PKG_OBJCFLAGS`, and `PKG_OBJCXXFLAGS` (for the C, C++,
Fortran, Objective C, and Objective C++ compilers, respectively) in the
file `Makevars` in the compilation directory (or, of course,
create the object files directly from the command line).
Similarly, variable `PKG_LIBS` in
`Makevars` can be used for additional '`-l`' and
'`-L`' flags to be passed to the linker when building the
shared object. (Supplying linker commands as arguments to `R CMD SHLIB`
will take precedence over `PKG_LIBS` in `Makevars`.)

It is possible to arrange to include compiled code from other languages
by setting the macro '`OBJECTS`' in file `Makevars`,
together with suitable rules to make the objects.

Flags that are already set (for example in file
`etcR_ARCH/Makeconf`) can be overridden by the environment
variable `MAKEFLAGS` (at least for systems using a POSIX-compliant
`make`), as in (Bourne shell syntax)

```r
MAKEFLAGS="CFLAGS=-O3" R CMD SHLIB *.c
```

It is also possible to set such variables in personal
`Makevars` files, which are read after the local
`Makevars` and the system makefiles or in a site-wide
`Makevars.site` file. See [Customizing package compilation](./R-admin.html#Customizing-package-compilation) in R
Installation and Administration,

Note that as `R CMD SHLIB` uses Make, it will not remake a shared object
just because the flags have changed, and if `test.c` and
`test.f` both exist in the current directory

```r
R CMD SHLIB test.f
```

will compile `test.c`!

If the `src` subdirectory of an add-on package contains source
code with one of the extensions listed above or a file
`Makevars` but **not** a file `Makefile`,
`R CMD INSTALL` creates a shared object (for loading into R through
`useDynlib` in the `NAMESPACE`, or in the `.onLoad` function of
the package) using the `R CMD SHLIB` mechanism. If file
`Makevars` exists it is read first, then the system makefile
and then any personal `Makevars` files.

If the `src` subdirectory of package contains a file
`Makefile`, this is used by `R CMD INSTALL` in place of the
`R CMD SHLIB` mechanism. `make` is called with makefiles
`R_HOME/etcR_ARCH/Makeconf`, `src/Makefile` and any
personal `Makevars` files (in that order). The first target
found in `src/Makefile` is used.

It is better to make use of a `Makevars` file rather than a
`Makefile`: the latter should be needed only exceptionally.

Under Windows the same commands work, but `Makevars.win` will
be used in preference to `Makevars`, and only
`src/Makefile.win` will be used by `R CMD INSTALL` with
`src/Makefile` being ignored. For past experiences of building
DLLs with a variety of compilers, see file '`README.packages`'.
Under Windows you can supply an exports definitions file called
`dllname-win.def`: otherwise all entry points in objects (but
not libraries) supplied to `R CMD SHLIB` will be exported from the DLL.
An example is `stats-win.def` for the **stats** package: a CRAN
example in package
[**fastICA**](https://CRAN.R-project.org/package=fastICA).

If you feel tempted to read the source code and subvert these
mechanisms, please resist. Far too much developer time has been wasted
in chasing down errors caused by failures to follow this documentation,
and even more by package authors demanding explanations as to why their
packages no longer work. In particular, undocumented environment or
`make` variables are not for use by package writers and are subject to
change without notice.

---

### 5.6 Interfacing C++ code

Suppose we have the following hypothetical C++ library, consisting of
the two files `X.h` and `X.cpp`, and implementing the
two classes `X` and `Y` which we want to use in R.

> +-----------------------------------------------------------------------+
> | |
> | `r | | // X.h | | | | class X { | | public: X (); ~X (); | | }; | | | | class Y { | | public: Y (); ~Y (); | | }; | |` |
> | ::: |
> +-----------------------------------------------------------------------+

> +-----------------------------------------------------------------------+
> | |
> | `r | | // X.cpp | | | | #include <R.h> | | #include "X.h" | | | | static Y y; | | | | X::X() { REprintf("constructor X\n"); } | | X::~X() { REprintf("destructor X\n"); } | | Y::Y() { REprintf("constructor Y\n"); } | | Y::~Y() { REprintf("destructor Y\n"); } | |` |
> | ::: |
> +-----------------------------------------------------------------------+

To use with R, the only thing we have to do is writing a wrapper
function and ensuring that the function is enclosed in

```r
extern "C" {

}
```

For example,

> +-----------------------------------------------------------------------+
> | |
> | `r | | // X_main.cpp: | | | | #include "X.h" | | | | extern "C" { | | | | void X_main () { | | X x; | | } | | | | } // extern "C" | |` |
> | ::: |
> +-----------------------------------------------------------------------+

Compiling and linking should be done with the C++ compiler-linker
(rather than the C compiler-linker or the linker itself); otherwise, the
C++ initialization code (and hence the constructor of the static
variable `Y`) are not called. On a properly configured system, one can
simply use

```r
R CMD SHLIB X.cpp X_main.cpp
```

to create the shared object, typically `X.so` (the file name
extension may be different on your platform). Now starting R yields

```r
R version 2.14.1 Patched (2012-01-16 r58124)
Copyright (C) 2012 The R Foundation for Statistical Computing
...
Type    "q()" to quit R.
```

```r

```

```r
R> dyn.load(paste("X", .Platform$dynlib.ext, sep = ""))
constructor Y
R> .C("X_main")
constructor X
destructor X
list()
R> q()
Save workspace image? [y/n/c]: y
destructor Y
```

The R for Windows FAQ (`rw-FAQ`) contains details of how to
compile this example under Windows.

Earlier versions of this example used C++ iostreams: this is best
avoided. There is no guarantee that the output will appear in the R
console, and indeed it will not on the R for Windows console. Use R code
or the C entry points (see [Printing](#Printing)) for all I/O if at all
possible. Examples have been seen where merely loading a DLL that
contained calls to C++ I/O upset R's own C I/O (for example by resetting
buffers on open files).

Most R header files can be included within C++ programs but they should
**not** be included within an `extern "C"` block (as they include system
headers[^135^](#FOOT135)). The inclusion of system headers in
C++ changed in R 3.3.0, so if you care about earlier versions of R
please check your package there.

Legacy header `S.h` cannot be used with C++.

#### 5.6.1 External C++ code

Quite a lot of external C++ software is header-only (e.g. most of the
Boost 'libraries' including all those supplied by package
[**BH**](https://CRAN.R-project.org/package=BH), and most of Armadillo
as supplied by package
[**RcppArmadillo**](https://CRAN.R-project.org/package=RcppArmadillo))
and so is compiled when an R package which uses it is installed. This
causes few problems.

A small number of external libraries used in R packages have a C++
interface to a library of compiled code, e.g. packages
[**rgdal**](https://CRAN.R-project.org/package=rgdal) and
[**rjags**](https://CRAN.R-project.org/package=rjags). This raises many
more problems! The C++ interface uses name-mangling and the
ABI[^136^](#FOOT136) may depend on the compiler, version and
even C++ defines[^137^](#FOOT137), so requires the package C++
code to be compiled in exactly the same way as the library (and what
that was is often undocumented). Examples include use of `g++` _vs_
`clang++` or Solaris' `CC`, and the two ABIs available for C++11 in
`g++` with different defaults for GCC 4.9 and 5.x in some Linux
distributions.

Even fewer external libraries use C++ internally but present a C
interface, such as
[**rgeos**](https://CRAN.R-project.org/package=rgeos). These require the
C++ runtime library to be linked into the package's shared object/DLL,
and this is best done by including a dummy C++ file in the package
sources.

There is a recent trend to link to the C++ interfaces offered by C
software such as **hdf5**, **pcre** and **ImageMagick**. Their C
interfaces are much preferred for portability (and can be used from C++
code). Also, the C++ interfaces are often optional in the software build
or packaged separately and so users installing from package sources are
far less likely to already have them installed.

---

### 5.7 Fortran I/O

We have already warned against the use of C++ iostreams not least
because output is not guaranteed to appear on the R console, and this
warning applies equally to Fortran output to units `*` and `6`. See
[Printing from Fortran](#Printing-from-Fortran), which describes
workarounds.

In the past most Fortran compilers implemented I/O on top of the C I/O
system and so the two interworked successfully. This was true of `g77`,
but it is less true of `gfortran` as used in `gcc` 4 and later. In
particular, any package that makes use of Fortran I/O will when compiled
on Windows interfere with C I/O: when the Fortran I/O support code is
initialized (typically when the package is loaded) the C `stdout` and
`stderr` are switched to LF line endings. (Function `init` in file
`src/modules/lapack/init_win.c` shows how to mitigate this. In
a package this would look something like

```r
#ifdef _WIN32
# include <fcntl.h>
#endif

void R_init_mypkgname(DllInfo *dll)
{
    // Native symbol registration calls

#ifdef _WIN32
    // gfortran I/O initialization sets these to _O_BINARY
    setmode(1, _O_TEXT); /* stdout */
    setmode(2, _O_TEXT); /* stderr */
#endif
}
```

in the file used for native symbol registration.)

---

### 5.8 Linking to other packages

It is not in general possible to link a DLL in package **packA** to a
DLL provided by package **packB** (for the security reasons mentioned in
[dyn.load and dyn.unload](#dyn_002eload-and-dyn_002eunload), and also
because some platforms distinguish between shared objects and dynamic
libraries), but it is on Windows.

Note that there can be tricky versioning issues here, as package
**packB** could be re-installed after package **packA** --- it is
desirable that the API provided by package **packB** remains
backwards-compatible.

Shipping a static library in package **packB** for other packages to
link to avoids most of the difficulties.

---

• [Unix-alikes](#Unix_002dalikes)     
 • [Windows](#Windows)

---

---

#### 5.8.1 Unix-alikes

It is possible to link a shared object in package **packA** to a library
provided by package **packB** under limited circumstances on a
Unix-alike OS. There are severe portability issues, so this is not
recommended for a distributed package.

This is easiest if **packB** provides a static library
`packB/lib/libpackB.a`. (Note using directory `lib`
rather than `libs` is conventional, and architecture-specific
sub-directories may be needed and are assumed in the sample code below.
The code in the static library will need to be compiled with `PIC` flags
on platforms where it matters.) Then as the code from package **packB**
is incorporated when package **packA** is installed, we only need to
find the static library at install time for package **packA**. The only
issue is to find package **packB**, and for that we can ask R by
something like (long lines broken for display here)

```r
PKGB_PATH=‘echo ’library(packB);
  cat(system.file("lib",  package="packB", mustWork=TRUE))' \
 | "${R_HOME}/bin/R" --vanilla --slave`
PKG_LIBS="$(PKGB_PATH)$(R_ARCH)/libpackB.a"
```

For a dynamic library `packB/lib/libpackB.so`
(`packB/lib/libpackB.dylib` on macOS: note that you cannot link
to a shared object, `.so`, on that platform) we could use

```r
PKGB_PATH=‘echo ’library(packB);
  cat(system.file("lib", package="packB", mustWork=TRUE))' \
 | "${R_HOME}/bin/R" --vanilla --slave`
PKG_LIBS=-L"$(PKGB_PATH)$(R_ARCH)" -lpackB
```

This will work for installation, but very likely not when package
`packB` is loaded, as the path to package **packB**'s `lib`
directory is not in the `ld.so`[^138^](#FOOT138) search path.
You can arrange to put it there **before** R is launched by setting (on
some platforms) `LD_RUN_PATH` or `LD_LIBRARY_PATH` or adding to the
`ld.so` cache (see `man ldconfig`). On platforms that support it, the
path to the directory containing the dynamic library can be hardcoded at
install time (which assumes that the location of package **packB** will
not be changed nor the package updated to a changed API). On systems
with the `gcc` or `clang` and the GNU linker (e.g. Linux) and some
others this can be done by e.g.

```r
PKGB_PATH=‘echo ’library(packB);
  cat(system.file("lib", package="packB", mustWork=TRUE)))' \
 | "${R_HOME}/bin/R" --vanilla --slave`
PKG_LIBS=-L"$(PKGB_PATH)$(R_ARCH)" -Wl,-rpath,"$(PKGB_PATH)$(R_ARCH)" -lpackB
```

Some other systems (e.g. Solaris with its native linker) use
`-Rdir` rather than `-rpath,dir` (and this is accepted
by the compiler as well as the linker).

It may be possible to figure out what is required semi-automatically
from the result of `R CMD libtool --config` (look for
'`hardcode`').

Making headers provided by package **packB** available to the code to be
compiled in package **packA** can be done by the `LinkingTo` mechanism
(see [Registering native routines](#Registering-native-routines)).

---

#### 5.8.2 Windows

Suppose package **packA** wants to make use of compiled code provided by
**packB** in DLL `packB/libs/exB.dll`, possibly the package's
DLL `packB/libs/packB.dll`. (This can be extended to linking to
more than one package in a similar way.) There are three issues to be
addressed:

- Making headers provided by package **packB** available to the code
  to be compiled in package **packA**.

  This is done by the `LinkingTo` mechanism (see [Registering native
  routines](#Registering-native-routines)).

- preparing `packA.dll` to link to `packB/libs/exB.dll`.

  This needs an entry in `Makevars.win` of the form

```r
PKG_LIBS= -L<something> -lexB
```

and one possibility is that `<something>` is the path to the
installed `pkgB/libs` directory. To find that we need to
ask R where it is by something like

```r
PKGB_PATH=‘echo ’library(packB);
  cat(system.file("libs", package="packB", mustWork=TRUE))' \
 | rterm --vanilla --slave`
PKG_LIBS= -L"$(PKGB_PATH)$(R_ARCH)" -lexB
```

Another possibility is to use an import library, shipping with
package **packA** an exports file `exB.def`. Then
`Makevars.win` could contain

```r
PKG_LIBS= -L. -lexB

all: $(SHLIB) before

before: libexB.dll.a
libexB.dll.a: exB.def
```

and then installing package **packA** will make and use the import
library for `exB.dll`. (One way to prepare the exports file
is to use `pexports.exe`.)

- loading `packA.dll` which depends on `exB.dll`.

  If `exB.dll` was used by package **packB** (because it is in fact
  `packB.dll` or `packB.dll` depends on it) and
  **packB** has been loaded before **packA**, then nothing more needs
  to be done as `exB.dll` will already be loaded into the R
  executable. (This is the most common scenario.)

  More generally, we can use the `DLLpath` argument to `library.dynam`
  to ensure that `exB.dll` is found, for example by setting

```r
library.dynam("packA", pkg, lib,
              DLLpath = system.file("libs", package="packB"))
```

Note that `DLLpath` can only set one path, and so for linking to two
or more packages you would need to resort to setting environment
variable `PATH`.

---

### 5.9 Handling R objects in C

Using C code to speed up the execution of an R function is often very
fruitful. Traditionally this has been done _via_ the `.C` function in R.
However, if a user wants to write C code using internal R data
structures, then that can be done using the `.Call` and `.External`
functions. The syntax for the calling function in R in each case is
similar to that of `.C`, but the two functions have different C
interfaces. Generally the `.Call` interface is simpler to use, but
`.External` is a little more general.

A call to `.Call` is very similar to `.C`, for example

```r
.Call("convolve2", a, b)
```

The first argument should be a character string giving a C symbol name
of code that has already been loaded into R. Up to 65 R objects can
passed as arguments. The C side of the interface is

```r
#include <R.h>
#include <Rinternals.h>

SEXP convolve2(SEXP a, SEXP b)
 ...
```

A call to `.External` is almost identical

```r
.External("convolveE", a, b)
```

but the C side of the interface is different, having only one argument

```r
#include <R.h>
#include <Rinternals.h>

SEXP convolveE(SEXP args)
 ...
```

Here `args` is a `LISTSXP`, a Lisp-style pairlist from which the
arguments can be extracted.

In each case the R objects are available for manipulation _via_ a set of
functions and macros defined in the header file `Rinternals.h`
or some S-compatibility macros[^139^](#FOOT139) See [Interface
functions .Call and
.External](#Interface-functions-_002eCall-and-_002eExternal) for details
on `.Call` and `.External`.

Before you decide to use `.Call` or `.External`, you should look at
other alternatives. First, consider working in interpreted R code; if
this is fast enough, this is normally the best option. You should also
see if using `.C` is enough. If the task to be performed in C is simple
enough involving only atomic vectors and requiring no call to R, `.C`
suffices. A great deal of useful code was written using just `.C` before
`.Call` and `.External` were available. These interfaces allow much more
control, but they also impose much greater responsibilities so need to
be used with care. Neither `.Call` nor `.External` copy their arguments:
you should treat arguments you receive through these interfaces as
read-only.

To handle R objects from within C code we use the macros and functions
that have been used to implement the core parts of R. A
public[^140^](#FOOT140) subset of these is defined in the
header file `Rinternals.h` in the directory
`R_INCLUDE_DIR` (default `R_HOME/include`) that should
be available on any R installation.

A substantial amount of R, including the standard packages, is
implemented using the functions and macros described here, so the R
source code provides a rich source of examples and "how to do it": do
make use of the source code for inspirational examples.

It is necessary to know something about how R objects are handled in C
code. All the R objects you will deal with will be handled with the type
_SEXP_[^141^](#FOOT141), which is a pointer to a structure
with typedef `SEXPREC`. Think of this structure as a _variant type_ that
can handle all the usual types of R objects, that is vectors of various
modes, functions, environments, language objects and so on. The details
are given later in this section and in [R Internal Structures](./R-ints.html#R-Internal-Structures) in R Internals, but for
most purposes the programmer does not need to know them. Think rather of
a model such as that used by Visual Basic, in which R objects are handed
around in C code (as they are in interpreted R code) as the variant
type, and the appropriate part is extracted for, for example, numerical
calculations, only when it is needed. As in interpreted R code, much use
is made of coercion to force the variant object to the right type.

---

• [Garbage Collection](#Garbage-Collection)     
 • [Allocating storage](#Allocating-storage)     
 • [Details of R types](#Details-of-R-types)     
 • [Attributes](#Attributes)     
 • [Classes](#Classes)     
 • [Handling lists](#Handling-lists)     
 • [Handling character data](#Handling-character-data)     
 • [Finding and setting variables](#Finding-and-setting-variables)     
 • [Some convenience functions](#Some-convenience-functions)     
 • [Named objects and copying](#Named-objects-and-copying)

---

---

#### 5.9.1 Handling the effects of garbage collection

We need to know a little about the way R handles memory allocation. The
memory allocated for R objects is not freed by the user; instead, the
memory is from time to time _garbage collected_. That is, some or all of
the allocated memory not being used is freed or marked as re-usable.

The R object types are represented by a C structure defined by a typedef
`SEXPREC` in `Rinternals.h`. It contains several things among
which are pointers to data blocks and to other `SEXPREC`s. A `SEXP` is
simply a pointer to a `SEXPREC`.

If you create an R object in your C code, you must tell R that you are
using the object by using the `PROTECT` macro on a pointer to the
object. This tells R that the object is in use so it is not destroyed
during garbage collection. Notice that it is the object which is
protected, not the pointer variable. It is a common mistake to believe
that if you invoked `PROTECT(p)` at some point then `p`{.variable} is
protected from then on, but that is not true once a new object is
assigned to `p`{.variable}.

Protecting an R object automatically protects all the R objects pointed
to in the corresponding `SEXPREC`, for example all elements of a
protected list are automatically protected.

The programmer is solely responsible for housekeeping the calls to
`PROTECT`. There is a corresponding macro `UNPROTECT` that takes as
argument an `int` giving the number of objects to unprotect when they
are no longer needed. The protection mechanism is stack-based, so
`UNPROTECT(n)` unprotects the last `n`{.variable} objects which were
protected. The calls to `PROTECT` and `UNPROTECT` must balance when the
user's code returns. R will warn about `"stack imbalance in .Call"` (or
`.External`) if the housekeeping is wrong.

Here is a small example of creating an R numeric vector in C code:

```r
#include <R.h>
#include <Rinternals.h>

    SEXP ab;
      ....
    ab = PROTECT(allocVector(REALSXP, 2));
    REAL(ab)[0] = 123.45;
    REAL(ab)[1] = 67.89;
    UNPROTECT(1);
```

Now, the reader may ask how the R object could possibly get removed
during those manipulations, as it is just our C code that is running. As
it happens, we can do without the protection in this example, but in
general we do not know (nor want to know) what is hiding behind the R
macros and functions we use, and any of them might cause memory to be
allocated, hence garbage collection and hence our object `ab` to be
removed. It is usually wise to err on the side of caution and assume
that any of the R macros and functions might remove the object.

In some cases it is necessary to keep better track of whether protection
is really needed. Be particularly aware of situations where a large
number of objects are generated. The pointer protection stack has a
fixed size (default 10,000) and can become full. It is not a good idea
then to just `PROTECT` everything in sight and `UNPROTECT` several
thousand objects at the end. It will almost invariably be possible to
either assign the objects as part of another object (which automatically
protects them) or unprotect them immediately after use.

Protection is not needed for objects which R already knows are in use.
In particular, this applies to function arguments.

There is a less-used macro `UNPROTECT_PTR(s)` that unprotects the object
pointed to by the `SEXP` `s`{.variable}, even if it is not the top item
on the pointer protection stack. This macro was introduced for use in
the parser, where the code interfacing with the R heap is generated and
the generator cannot be configured to insert proper calls to `PROTECT`
and `UNPROTECT`. However, `UNPROTECT_PTR` is dangerous to use in
combination with `UNPROTECT` when the same object has been protected
multiple times. It has been superseded by multi-set based functions
`R_PreserveInMSet` and `R_ReleaseFromMSet`, which protect objects in a
multi-set created by `R_NewPreciousMSet` and typically itself protected
using `PROTECT`. These functions should not be needed outside parsers.

Sometimes an object is changed (for example duplicated, coerced or
grown) yet the current value needs to be protected. For these cases
`PROTECT_WITH_INDEX` saves an index of the protection location that can
be used to replace the protected value using `REPROTECT`.
For example
(from the internal code for `optim`)

```r
    PROTECT_INDEX ipx;

    ....
    PROTECT_WITH_INDEX(s = eval(OS->R_fcall, OS->R_env), &ipx);
    REPROTECT(s = coerceVector(s, REALSXP), ipx);
```

Note that it is dangerous to mix `UNPROTECT_PTR` also with
`PROTECT_WITH_INDEX`, as the former changes the protection locations of
objects that were protected after the one being unprotected.

There is another way to avoid the affects of garbage collection: a call
to `R_PreserveObject` adds an object to an internal list of objects not
to be collects, and a subsequent call to `R_ReleaseObject` removes it
from that list. This provides a way for objects which are not returned
as part of R objects to be protected across calls to compiled code: on
the other hand it becomes the user's responsibility to release them when
they are no longer needed (and this often requires the use of a
finalizer). It is less efficient that the normal protection mechanism,
and should be used sparingly.

---

#### 5.9.2 Allocating storage

For many purposes it is sufficient to allocate R objects and manipulate
those. There are quite a few `allocXxx` functions defined in
`Rinternals.h`---you may want to explore them.

One that is commonly used is `allocVector`, the C-level equivalent of
R-level `vector()` and its wrappers such as `integer()` and
`character()`. One distinction is that whereas the R functions always
initialize the elements of the vector, `allocVector` only does so for
lists, expressions and character vectors (the cases where the elements
are themselves R objects).

If storage is required for C objects during the calculations this is
best allocating by calling `R_alloc`; see [Memory allocation](#Memory-allocation). All of these memory allocation routines
do their own error-checking, so the programmer may assume that they will
raise an error and not return if the memory cannot be allocated.

---

#### 5.9.3 Details of R types

Users of the `Rinternals.h` macros will need to know how the R
types are known internally. The different R data types are represented
in C by _SEXPTYPE_. Some of these are familiar from R and some are
internal data types. The usual R object modes are given in the table.

> SEXPTYPE R equivalent
>
> ---
>
> `REALSXP` numeric with storage mode `double` > `INTSXP` integer
> `CPLXSXP` complex
> `LGLSXP` logical
> `STRSXP` character
> `VECSXP` list (generic vector)
> `LISTSXP` pairlist
> `DOTSXP` a '`…`' object
> `NILSXP` NULL
> `SYMSXP` name/symbol
> `CLOSXP` function or function closure
> `ENVSXP` environment

Among the important internal `SEXPTYPE`s are `LANGSXP`, `CHARSXP`,
`PROMSXP`, etc. (**N.B.**: although it is possible to return objects of
internal types, it is unsafe to do so as assumptions are made about how
they are handled which may be violated at user-level evaluation.) More
details are given in [R Internal Structures](./R-ints.html#R-Internal-Structures) in R Internals.

Unless you are very sure about the type of the arguments, the code
should check the data types. Sometimes it may also be necessary to check
data types of objects created by evaluating an R expression in the C
code. You can use functions like `isReal`, `isInteger` and `isString` to
do type checking. See the header file `Rinternals.h` for
definitions of other such functions. All of these take a `SEXP` as
argument and return 1 or 0 to indicate `TRUE`{.variable} or
`FALSE`{.variable}.

What happens if the `SEXP` is not of the correct type? Sometimes you
have no other option except to generate an error. You can use the
function `error` for this. It is usually better to coerce the object to
the correct type. For example, if you find that an `SEXP` is of the type
`INTEGER`, but you need a `REAL` object, you can change the type by
using

```r
newSexp = PROTECT(coerceVector(oldSexp, REALSXP));
```

Protection is needed as a new _object_ is created; the object formerly
pointed to by the `SEXP` is still protected but now
unused.[^142^](#FOOT142)

All the coercion functions do their own error-checking, and generate
`NA`s with a warning or stop with an error as appropriate.

Note that these coercion functions are _not_ the same as calling
`as.numeric` (and so on) in R code, as they do not dispatch on the class
of the object. Thus it is normally preferable to do the coercion in the
calling R code.

So far we have only seen how to create and coerce R objects from C code,
and how to extract the numeric data from numeric R vectors. These can
suffice to take us a long way in interfacing R objects to numerical
algorithms, but we may need to know a little more to create useful
return objects.

---

#### 5.9.4 Attributes

Many R objects have attributes: some of the most useful are classes and
the `dim` and `dimnames` that mark objects as matrices or arrays. It can
also be helpful to work with the `names` attribute of vectors.

To illustrate this, let us write code to take the outer product of two
vectors (which `outer` and `%o%` already do). As usual the R code is
simple

```r
out <- function(x, y)
{
    storage.mode(x) <- storage.mode(y) <- "double"
    .Call("out", x, y)
}
```

where we expect `x` and `y` to be numeric vectors (possibly integer),
possibly with names. This time we do the coercion in the calling R code.

C code to do the computations is

```r
#include <R.h>
#include <Rinternals.h>

SEXP out(SEXP x, SEXP y)
{
    int nx = length(x), ny = length(y);
    SEXP ans = PROTECT(allocMatrix(REALSXP, nx, ny));
    double *rx = REAL(x), *ry = REAL(y), *rans = REAL(ans);
    for(int i = 0; i < nx; i++) {
        double tmp = rx[i];
        for(int j = 0; j < ny; j++)
            rans[i + nx*j] = tmp * ry[j];
    }
    UNPROTECT(1);
    return ans;
}
```

Note the way `REAL` is used: as it is a function call it can be
considerably faster to store the result and index that.

However, we would like to set the `dimnames` of the result. We can use

```r
#include <R.h>
#include <Rinternals.h>
```

```r
SEXP out(SEXP x, SEXP y)
{
    int nx = length(x), ny = length(y);
    SEXP ans = PROTECT(allocMatrix(REALSXP, nx, ny));
    double *rx = REAL(x), *ry = REAL(y), *rans = REAL(ans);

    for(int i = 0; i < nx; i++) {
      double tmp = rx[i];
      for(int j = 0; j < ny; j++)
        rans[i + nx*j] = tmp * ry[j];
    }

    SEXP dimnames = PROTECT(allocVector(VECSXP, 2));
    SET_VECTOR_ELT(dimnames, 0, getAttrib(x, R_NamesSymbol));
    SET_VECTOR_ELT(dimnames, 1, getAttrib(y, R_NamesSymbol));
    setAttrib(ans, R_DimNamesSymbol, dimnames);
```

```r

```

```r
    UNPROTECT(2);
    return ans;
}
```

This example introduces several new features. The `getAttrib` and
`setAttrib` functions get and
set individual attributes. Their second argument is a `SEXP` defining
the name in the symbol table of the attribute we want; these and many
such symbols are defined in the header file `Rinternals.h`.

There are shortcuts here too: the functions `namesgets`, `dimgets` and
`dimnamesgets` are the internal versions of the default methods of
`names<-`, `dim<-` and `dimnames<-` (for vectors and arrays), and there
are functions such as `GetMatrixDimnames` and `GetArrayDimnames`.

What happens if we want to add an attribute that is not pre-defined? We
need to add a symbol for it _via_ a call to
`install`. Suppose for illustration we wanted to add an attribute
`"version"` with value `3.0`. We could use

```r
    SEXP version;
    version = PROTECT(allocVector(REALSXP, 1));
    REAL(version)[0] = 3.0;
    setAttrib(ans, install("version"), version);
    UNPROTECT(1);
```

Using `install` when it is not needed is harmless and provides a simple
way to retrieve the symbol from the symbol table if it is already
installed. However, the lookup takes a non-trivial amount of time, so
consider code such as

```r
static SEXP VerSymbol = NULL;
...
    if (VerSymbol == NULL) VerSymbol = install("version");
```

if it is to be done frequently.

This example can be simplified by another convenience function:

```r
    SEXP version = PROTECT(ScalarReal(3.0));
    setAttrib(ans, install("version"), version);
    UNPROTECT(1);
```

---

#### 5.9.5 Classes

In R the class is just the attribute named `"class"` so it can be
handled as such, but there is a shortcut `classgets`. Suppose we want to
give the return value in our example the class `"mat"`. We can use

```r
#include <R.h>
#include <Rinternals.h>
      ....
    SEXP ans, dim, dimnames, class;
      ....
    class = PROTECT(allocVector(STRSXP, 1));
    SET_STRING_ELT(class, 0, mkChar("mat"));
    classgets(ans, class);
    UNPROTECT(4);
    return ans;
}
```

As the value is a character vector, we have to know how to create that
from a C character array, which we do using the function `mkChar`.

---

#### 5.9.6 Handling lists

Some care is needed with lists, as R moved early on from using LISP-like
lists (now called "pairlists") to S-like generic vectors. As a result,
the appropriate test for an object of mode `list` is `isNewList`, and we
need `allocVector(VECSXP, n`) and _not_ `allocList(n)`.

List elements can be retrieved or set by direct access to the elements
of the generic vector. Suppose we have a list object

```r
a <- list(f = 1, g = 2, h = 3)
```

Then we can access `a$g` as `a[[2]]` by

```r
    double g;
      ....
    g = REAL(VECTOR_ELT(a, 1))[0];
```

This can rapidly become tedious, and the following function (based on
one in package **stats**) is very useful:

```r
/* get the list element named str, or return NULL */

SEXP getListElement(SEXP list, const char *str)
{
    SEXP elmt = R_NilValue, names = getAttrib(list, R_NamesSymbol);
```

```r

```

```r
    for (int i = 0; i < length(list); i++)
        if(strcmp(CHAR(STRING_ELT(names, i)), str) == 0) {
           elmt = VECTOR_ELT(list, i);
           break;
        }
    return elmt;
}
```

and enables us to say

```r
  double g;
  g = REAL(getListElement(a, "g"))[0];
```

---

#### 5.9.7 Handling character data

R character vectors are stored as `STRSXP`s, a vector type like `VECSXP`
where every element is of type `CHARSXP`. The `CHARSXP` elements of
`STRSXP`s are accessed using `STRING_ELT` and `SET_STRING_ELT`.

`CHARSXP`s are read-only objects and must never be modified. In
particular, the C-style string contained in a `CHARSXP` should be
treated as read-only and for this reason the `CHAR` function used to
access the character data of a `CHARSXP` returns `(const char *)` (this
also allows compilers to issue warnings about improper use). Since
`CHARSXP`s are immutable, the same `CHARSXP` can be shared by any
`STRSXP` needing an element representing the same string. R maintains a
global cache of `CHARSXP`s so that there is only ever one `CHARSXP`
representing a given string in memory.

You can obtain a `CHARSXP` by calling `mkChar` and providing a
nul-terminated C-style string. This function will return a pre-existing
`CHARSXP` if one with a matching string already exists, otherwise it
will create a new one and add it to the cache before returning it to
you. The variant `mkCharLen` can be used to create a `CHARSXP` from part
of a buffer and will ensure null-termination.

Note that R character strings are restricted to `2^31 - 1` bytes, and
hence so should the input to `mkChar` be (C allows longer strings on
64-bit platforms).

---

#### 5.9.8 Finding and setting variables

It will be usual that all the R objects needed in our C computations are
passed as arguments to `.Call` or `.External`, but it is possible to
find the values of R objects from within the C given their names. The
following code is the equivalent of `get(name, envir = rho)`.

```r
SEXP getvar(SEXP name, SEXP rho)
{
    SEXP ans;

    if(!isString(name) || length(name) != 1)
        error("name is not a single string");
    if(!isEnvironment(rho))
        error("rho should be an environment");
    ans = findVar(installChar(STRING_ELT(name, 0)), rho);
    Rprintf("first value is %f\n", REAL(ans)[0]);
    return R_NilValue;
}
```

The main work is done by `findVar`, but to use it we
need to install `name` as a name in the symbol table. As we wanted the
value for internal use, we return `NULL`.

Similar functions with syntax

```r
void defineVar(SEXP symbol, SEXP value, SEXP rho)
void setVar(SEXP symbol, SEXP value, SEXP rho)
```

can be used to assign values to R variables. `defineVar` creates a new
binding or changes the value of an existing binding in the specified
environment frame; it is the analogue of
`assign(symbol, value, envir = rho, inherits = FALSE)`, but unlike
`assign`, `defineVar` does not make a copy of the object
`value`.[^143^](#FOOT143) `setVar` searches for an existing
binding for `symbol` in `rho` or its enclosing environments. If a
binding is found, its value is changed to `value`. Otherwise, a new
binding with the specified value is created in the global environment.
This corresponds to
`assign(symbol, value, envir = rho, inherits = TRUE)`.

---

#### 5.9.9 Some convenience functions

Some operations are done so frequently that there are convenience
functions to handle them. (All these are provided _via_ the header file
`Rinternals.h`.)

Suppose we wanted to pass a single logical argument `ignore_quotes`: we
could use

```r
    int ign = asLogical(ignore_quotes);
    if(ign == NA_LOGICAL) error("'ignore_quotes' must be TRUE or FALSE");
```

which will do any coercion needed (at least from a vector argument), and
return `NA_LOGICAL` if the value passed was `NA` or coercion failed.
There are also `asInteger`, `asReal` and `asComplex`. The function
`asChar` returns a `CHARSXP`. All of these functions ignore any elements
of an input vector after the first.

To return a length-one real vector we can use

```r
    double x;

    ...
    return ScalarReal(x);
```

and there are versions of this for all the atomic vector types (those
for a length-one character vector being `ScalarString` with argument a
`CHARSXP` and `mkString` with argument `const char *`).

Some of the `isXXXX` functions differ from their apparent R-level
counterparts: for example `isVector` is true for any atomic vector type
(`isVectorAtomic`) and for lists and expressions (`isVectorList`) (with
no check on attributes). `isMatrix` is a test of a length-2 `"dim"`
attribute.

There are a series of small macros/functions to help construct pairlists
and language objects (whose internal structures just differ by
`SEXPTYPE`). Function `CONS(u, v)` is the basic building block: it
constructs a pairlist from `u` followed by `v` (which is a pairlist or
`R_NilValue`). `LCONS` is a variant that constructs a language object.
Functions `list1` to `list6` construct a pairlist from one to six items,
and `lang1` to `lang6` do the same for a language object (a function to
call plus zero to five arguments). Functions `elt` and `lastElt` find
the `i`{.variable}th element and the last element of a pairlist, and
`nthcdr` returns a pointer to the `n`{.variable}th position in the
pairlist (whose `CAR` is the `n`{.variable}th item).

Functions `str2type` and `type2str` map R length-one character strings
to and from `SEXPTYPE` numbers, and `type2char` maps numbers to C
character strings.

---

• [Semi-internal convenience functions](#Semi_002dinternal-convenience-functions)

---

---

#### 5.9.9.1 Semi-internal convenience functions

There is quite a collection of functions that may be used in your C code
_if_ you are willing to adapt to rare "API" changes. These typically
contain "workhorses" of their R counterparts.

Functions `any_duplicated` and `any_duplicated3` are fast versions of
R's `any(duplicated(.))`.

Function `R_compute_identical` corresponds to R's `identical` function.

---

#### 5.9.10 Named objects and copying

When assignments are done in R such as

```r
x <- 1:10
y <- x
```

the named object is not necessarily copied, so after those two
assignments `y` and `x` are bound to the same `SEXPREC` (the structure a
`SEXP` points to). This means that any code which alters one of them has
to make a copy before modifying the copy if the usual R semantics are to
apply. Note that whereas `.C` and `.Fortran` do copy their arguments
(unless the dangerous `dup = FALSE` is used), `.Call` and `.External` do
not. So `duplicate` is commonly called on arguments to `.Call` before
modifying them.

However, at least some of this copying is unneeded. In the first
assignment shown, `x <- 1:10`, R first creates an object with value
`1:10` and then assigns it to `x` but if `x` is modified no copy is
necessary as the temporary object with value `1:10` cannot be referred
to again. R distinguishes between named and unnamed objects _via_ a
field in a `SEXPREC` that can be accessed _via_ the macros `NAMED` and
`SET_NAMED`. This can take values

`0`

: The object is not bound to any symbol

`1`

: The object has been bound to exactly one symbol

`>= 2`

: The object has potentially been bound to two or more symbols, and
one should act as if another variable is currently bound to this
value. The maximal value is `NAMEDMAX`.

Note the past tenses: R does not do full reference counting and there
may currently be fewer bindings.

It is safe to modify the value of any `SEXP` for which `NAMED(foo)` is
zero, and if `NAMED(foo)` is two or more, the value should be duplicated
(_via_ a call to `duplicate`) before any modification. Note that it is
the responsibility of the author of the code making the modification to
do the duplication, even if it is `x` whose value is being modified
after `y <- x`.

The case `NAMED(foo) == 1` allows some optimization, but it can be
ignored (and duplication done whenever `NAMED(foo) > 0`). (This
optimization is not currently usable in user code.) It is intended for
use within replacement functions. Suppose we used

```r
x <- 1:10
foo(x) <- 3
```

which is computed as

```r
x <- 1:10
x <- "foo<-"(x, 3)
```

Then inside `"foo<-"` the object pointing to the current value of `x`
will have `NAMED(foo)` as one, and it would be safe to modify it as the
only symbol bound to it is `x` and that will be rebound immediately.
(Provided the remaining code in `"foo<-"` make no reference to `x`, and
no one is going to attempt a direct call such as `y <- "foo<-"(x)`.)

This mechanism is to be replaced in R 4.0.0. To support future changes,
package code should use the macros `MAYBE_REFERENCED`, `MAYBE_SHARED`,
and `MARK_NOT_MUTABLE`. These currently correspond to

`MAYBE_REFERENCED(x)`

: `NAMED(x) > 0`

`MAYBE_SHARED(x)`

: `NAMED(x) > 1`

`MARK_NOT_MUTABLE(x)`

: `SET_NAMED(x, NAMEDMAX)`

---

### 5.10 Interface functions `.Call` and `.External`

In this section we consider the details of the R/C interfaces.

These two interfaces have almost the same functionality. `.Call` is
based on the interface of the same name in S version 4, and `.External`
is based on R's `.Internal`. `.External` is more complex but allows a
variable number of arguments.

---

• [Calling .Call](#Calling-_002eCall)     
 • [Calling .External](#Calling-_002eExternal)     
 • [Missing and special values](#Missing-and-special-values)

---

---

#### 5.10.1 Calling `.Call`

Let us convert our finite convolution example to use `.Call`. The
calling function in R is

```r
conv <- function(a, b) .Call("convolve2", a, b)
```

which could hardly be simpler, but as we shall see all the type coercion
is transferred to the C code, which is

```r
#include <R.h>
#include <Rinternals.h>

SEXP convolve2(SEXP a, SEXP b)
{
    int na, nb, nab;
    double *xa, *xb, *xab;
    SEXP ab;

    a = PROTECT(coerceVector(a, REALSXP));
    b = PROTECT(coerceVector(b, REALSXP));
    na = length(a); nb = length(b); nab = na + nb - 1;
    ab = PROTECT(allocVector(REALSXP, nab));
    xa = REAL(a); xb = REAL(b); xab = REAL(ab);
    for(int i = 0; i < nab; i++) xab[i] = 0.0;
    for(int i = 0; i < na; i++)
        for(int j = 0; j < nb; j++) xab[i + j] += xa[i] * xb[j];
    UNPROTECT(3);
    return ab;
}
```

---

#### 5.10.2 Calling `.External`

We can use the same example to illustrate `.External`. The R code
changes only by replacing `.Call` by `.External`

```r
conv <- function(a, b) .External("convolveE", a, b)
```

but the main change is how the arguments are passed to the C code, this
time as a single SEXP. The only change to the C code is how we handle
the arguments.

```r
#include <R.h>
#include <Rinternals.h>

SEXP convolveE(SEXP args)
{
    int i, j, na, nb, nab;
    double *xa, *xb, *xab;
    SEXP a, b, ab;

    a = PROTECT(coerceVector(CADR(args), REALSXP));
    b = PROTECT(coerceVector(CADDR(args), REALSXP));
    ...
}
```

Once again we do not need to protect the arguments, as in the R side of
the interface they are objects that are already in use. The macros

```r
  first = CADR(args);
  second = CADDR(args);
  third = CADDDR(args);
  fourth = CAD4R(args);
```

provide convenient ways to access the first four arguments. More
generally we can use the `CDR` and `CAR`
macros as in

```r
  args = CDR(args); a = CAR(args);
  args = CDR(args); b = CAR(args);
```

which clearly allows us to extract an unlimited number of arguments
(whereas `.Call` has a limit, albeit at 65 not a small one).

More usefully, the `.External` interface provides an easy way to handle
calls with a variable number of arguments, as `length(args)` will give
the number of arguments supplied (of which the first is ignored). We may
need to know the names ('tags') given to the actual arguments, which we
can by using the `TAG` macro and using something like the following
example, that prints the names and the first value of its arguments if
they are vector types.

```r
SEXP showArgs(SEXP args)
{
    args = CDR(args); /* skip ‘name’ */
    for(int i = 0; args != R_NilValue; i++, args = CDR(args)) {
        const char *name =
            isNull(TAG(args)) ? "" : CHAR(PRINTNAME(TAG(args)));
        SEXP el = CAR(args);
        if (length(el) == 0) {
            Rprintf("[%d] ‘%s’ R type, length 0\n", i+1, name);
           continue;
        }
```

```r
        switch(TYPEOF(el)) {
        case REALSXP:
            Rprintf("[%d] ‘%s’ %f\n", i+1, name, REAL(el)[0]);
            break;
```

```r
        case LGLSXP:
        case INTSXP:
            Rprintf("[%d] ‘%s’ %d\n", i+1, name, INTEGER(el)[0]);
            break;
```

```r
        case CPLXSXP:
        {
            Rcomplex cpl = COMPLEX(el)[0];
            Rprintf("[%d] ‘%s’ %f + %fi\n", i+1, name, cpl.r, cpl.i);
        }
            break;
```

```r
        case STRSXP:
            Rprintf("[%d] ‘%s’ %s\n", i+1, name,
                   CHAR(STRING_ELT(el, 0)));
           break;
```

```r
        default:
            Rprintf("[%d] ‘%s’ R type\n", i+1, name);
       }
    }
    return R_NilValue;
}
```

This can be called by the wrapper function

```r
showArgs <- function(...) invisible(.External("showArgs", ...))
```

Note that this style of programming is convenient but not necessary, as
an alternative style is

```r
showArgs1 <- function(...) invisible(.Call("showArgs1", list(...)))
```

The (very similar) C code is in the scripts.

---

#### 5.10.3 Missing and special values

One piece of error-checking the `.C` call does (unless `NAOK` is true)
is to check for missing (`NA`) and IEEE special values (`Inf`, `-Inf`
and `NaN`) and give an error if any are found. With the `.Call`
interface these will be passed to our code. In this example the special
values are no problem, as IEC60559 arithmetic will handle them
correctly. In the current implementation this is also true of `NA` as it
is a type of `NaN`, but it is unwise to rely on such details. Thus we
will re-write the code to handle `NA`s using macros defined in
`R_ext/Arith.h` included by `R.h`.

The code changes are the same in any of the versions of `convolve2` or
`convolveE`:

```r
    ...
  for(int i = 0; i < na; i++)
    for(int j = 0; j < nb; j++)
        if(ISNA(xa[i]) || ISNA(xb[j]) || ISNA(xab[i + j]))
            xab[i + j] = NA_REAL;
        else
            xab[i + j] += xa[i] * xb[j];
    ...
```

Note that the `ISNA` macro, and the similar macros `ISNAN` (which checks
for `NaN` or `NA`) and `R_FINITE` (which is false for `NA` and all the
special values), only apply to numeric values of type `double`.
Missingness of integers, logicals and character strings can be tested by
equality to the constants `NA_INTEGER`, `NA_LOGICAL` and `NA_STRING`.
These and `NA_REAL` can be used to set elements of R vectors to `NA`.

The constants `R_NaN`, `R_PosInf` and `R_NegInf` can be used to set
`double`s to the special values.

---

### 5.11 Evaluating R expressions from C

The main function we will use is

```r
SEXP eval(SEXP expr, SEXP rho);
```

the equivalent of the interpreted R code `eval(expr, envir = rho)` (so
`rho` must be an environment), although we can also make use of
`findVar`, `defineVar` and `findFun` (which restricts the search to
functions).

To see how this might be applied, here is a simplified internal version
of `lapply` for expressions, used as

```r
a <- list(a = 1:5, b = rnorm(10), test = runif(100))
.Call("lapply", a, quote(sum(x)), new.env())
```

with C code

```r
SEXP lapply(SEXP list, SEXP expr, SEXP rho)
{
    int n = length(list);
    SEXP ans;

    if(!isNewList(list)) error("'list' must be a list");
    if(!isEnvironment(rho)) error("'rho' should be an environment");
    ans = PROTECT(allocVector(VECSXP, n));
    for(int i = 0; i < n; i++) {
        defineVar(install("x"), VECTOR_ELT(list, i), rho);
        SET_VECTOR_ELT(ans, i, eval(expr, rho));
    }
    setAttrib(ans, R_NamesSymbol, getAttrib(list, R_NamesSymbol));
    UNPROTECT(1);
    return ans;
}
```

It would be closer to `lapply` if we could pass in a function rather
than an expression. One way to do this is _via_ interpreted R code as in
the next example, but it is possible (if somewhat obscure) to do this in
C code. The following is based on the code in
`src/main/optimize.c`.

```r
SEXP lapply2(SEXP list, SEXP fn, SEXP rho)
{
    int n = length(list);
    SEXP R_fcall, ans;

    if(!isNewList(list)) error("'list' must be a list");
    if(!isFunction(fn)) error("'fn' must be a function");
    if(!isEnvironment(rho)) error("'rho' should be an environment");
    R_fcall = PROTECT(lang2(fn, R_NilValue));
    ans = PROTECT(allocVector(VECSXP, n));
    for(int i = 0; i < n; i++) {
        SETCADR(R_fcall, VECTOR_ELT(list, i));
        SET_VECTOR_ELT(ans, i, eval(R_fcall, rho));
    }
    setAttrib(ans, R_NamesSymbol, getAttrib(list, R_NamesSymbol));
    UNPROTECT(2);
    return ans;
}
```

used by

```r
.Call("lapply2", a, sum, new.env())
```

Function `lang2` creates an executable pairlist of two elements, but
this will only be clear to those with a knowledge of a LISP-like
language.

As a more comprehensive example of constructing an R call in C code and
evaluating, consider the following fragment of `printAttributes` in
`src/main/print.c`.

```r
    /* Need to construct a call to
       print(CAR(a), digits=digits)
       based on the R_print structure, then eval(call, env).
       See do_docall for the template for this sort of thing.
    */
    SEXP s, t;
    t = s = PROTECT(allocList(3));
    SET_TYPEOF(s, LANGSXP);
    SETCAR(t, install("print")); t = CDR(t);
    SETCAR(t,  CAR(a)); t = CDR(t);
    SETCAR(t, ScalarInteger(digits));
    SET_TAG(t, install("digits"));
    eval(s, env);
    UNPROTECT(1);
```

At this point `CAR(a)` is the R object to be printed, the current
attribute. There are three steps: the call is constructed as a pairlist
of length 3, the list is filled in, and the expression represented by
the pairlist is evaluated.

A pairlist is quite distinct from a generic vector list, the only
user-visible form of list in R. A pairlist is a linked list (with
`CDR(t)` computing the next entry), with items (accessed by `CAR(t)`)
and names or tags (set by `SET_TAG`). In this call there are to be three
items, a symbol (pointing to the function to be called) and two argument
values, the first unnamed and the second named. Setting the type to
`LANGSXP` makes this a call which can be evaluated.

Customarily, the evaluation environment is passed from the calling R
code (see `rho` above). In special cases it is possible that the C code
may need to obtain the current evaluation environment which can be done
via `R_GetCurrentEnv()` function.

---

• [Zero-finding](#Zero_002dfinding)     
 • [Calculating numerical derivatives](#Calculating-numerical-derivatives)

---

---

#### 5.11.1 Zero-finding

In this section we re-work the example of Becker, Chambers & Wilks
(1988, pp.\~205--10) on finding a zero of a univariate function. The R
code and an example are

```r
zero <- function(f, guesses, tol = 1e-7) {
    f.check <- function(x) {
        x <- f(x)
        if(!is.numeric(x)) stop("Need a numeric result")
        as.double(x)
    }
    .Call("zero", body(f.check), as.double(guesses), as.double(tol),
          new.env())
}

cube1 <- function(x) (x^2 + 1) * (x - 1.5)
zero(cube1, c(0, 5))
```

where this time we do the coercion and error-checking in the R code. The
C code is

```r
SEXP mkans(double x)
{
    // no need for PROTECT() here, as REAL(.) does not allocate:
    SEXP ans = allocVector(REALSXP, 1);
    REAL(ans)[0] = x;
    return ans;
}
```

```r

```

```r
double feval(double x, SEXP f, SEXP rho)
{
    // a version with (too) much PROTECT()ion .. "better safe than sorry"
    SEXP symbol, value;
    PROTECT(symbol = install("x"));
    PROTECT(value = mkans(x));
    defineVar(symbol, value, rho);
    UNPROTECT(2);
    return(REAL(eval(f, rho))[0]);
}
```

```r

```

```r
SEXP zero(SEXP f, SEXP guesses, SEXP stol, SEXP rho)
{
    double x0 = REAL(guesses)[0], x1 = REAL(guesses)[1],
           tol = REAL(stol)[0];
    double f0, f1, fc, xc;
```

```r

```

```r
    if(tol <= 0.0) error("non-positive tol value");
    f0 = feval(x0, f, rho); f1 = feval(x1, f, rho);
    if(f0 == 0.0) return mkans(x0);
    if(f1 == 0.0) return mkans(x1);
    if(f0*f1 > 0.0) error("x[0] and x[1] have the same sign");
```

```r

```

```r
    for(;;) {
        xc = 0.5*(x0+x1);
        if(fabs(x0-x1) < tol) return  mkans(xc);
        fc = feval(xc, f, rho);
        if(fc == 0) return  mkans(xc);
        if(f0*fc > 0.0) {
            x0 = xc; f0 = fc;
        } else {
            x1 = xc; f1 = fc;
        }
    }
}
```

---

#### 5.11.2 Calculating numerical derivatives

We will use a longer example (by Saikat DebRoy) to illustrate the use of
evaluation and `.External`. This calculates numerical derivatives,
something that could be done as effectively in interpreted R code but
may be needed as part of a larger C calculation.

An interpreted R version and an example are

```r
numeric.deriv <- function(expr, theta, rho=sys.frame(sys.parent()))
{
    eps <- sqrt(.Machine$double.eps)
    ans <- eval(substitute(expr), rho)
    grad <- matrix(, length(ans), length(theta),
                   dimnames=list(NULL, theta))
    for (i in seq_along(theta)) {
        old <- get(theta[i], envir=rho)
        delta <- eps * max(1, abs(old))
        assign(theta[i], old+delta, envir=rho)
        ans1 <- eval(substitute(expr), rho)
        assign(theta[i], old, envir=rho)
        grad[, i] <- (ans1 - ans)/delta
    }
    attr(ans, "gradient") <- grad
    ans
}
omega <- 1:5; x <- 1; y <- 2
numeric.deriv(sin(omega*x*y), c("x", "y"))
```

where `expr` is an expression, `theta` a character vector of variable
names and `rho` the environment to be used.

For the compiled version the call from R will be

```r
.External("numeric_deriv", expr, theta, rho)
```

with example usage

```r
.External("numeric_deriv", quote(sin(omega*x*y)),
          c("x", "y"), .GlobalEnv)
```

Note the need to quote the expression to stop it being evaluated in the
caller.

Here is the complete C code which we will explain section by section.

```r
#include <R.h> /* for DOUBLE_EPS */
#include <Rinternals.h>

SEXP numeric_deriv(SEXP args)
{
    SEXP theta, expr, rho, ans, ans1, gradient, par, dimnames;
    double tt, xx, delta, eps = sqrt(DOUBLE_EPS), *rgr, *rans;
    int i, start;
```

```r

```

```r
    expr = CADR(args);
    if(!isString(theta = CADDR(args)))
        error("theta should be of type character");
    if(!isEnvironment(rho = CADDDR(args)))
        error("rho should be an environment");
```

```r

```

```r
    ans = PROTECT(coerceVector(eval(expr, rho), REALSXP));
    gradient = PROTECT(allocMatrix(REALSXP, LENGTH(ans), LENGTH(theta)));
    rgr = REAL(gradient); rans = REAL(ans);
```

```r

```

```r
    for(i = 0, start = 0; i < LENGTH(theta); i++, start += LENGTH(ans)) {
        par = PROTECT(findVar(installChar(STRING_ELT(theta, i)), rho));
        tt = REAL(par)[0];
        xx = fabs(tt);
        delta = (xx < 1) ? eps : xx*eps;
        REAL(par)[0] += delta;
        ans1 = PROTECT(coerceVector(eval(expr, rho), REALSXP));
        for(int j = 0; j < LENGTH(ans); j++)
            rgr[j + start] = (REAL(ans1)[j] - rans[j])/delta;
        REAL(par)[0] = tt;
        UNPROTECT(2); /* par, ans1 */
    }
```

```r

```

```r
    dimnames = PROTECT(allocVector(VECSXP, 2));
    SET_VECTOR_ELT(dimnames, 1,  theta);
    dimnamesgets(gradient, dimnames);
    setAttrib(ans, install("gradient"), gradient);
    UNPROTECT(3); /* ans  gradient  dimnames */
    return ans;
}
```

The code to handle the arguments is

```r
    expr = CADR(args);
    if(!isString(theta = CADDR(args)))
        error("theta should be of type character");
    if(!isEnvironment(rho = CADDDR(args)))
        error("rho should be an environment");
```

Note that we check for correct types of `theta` and `rho` but do not
check the type of `expr`. That is because `eval` can handle many types
of R objects other than `EXPRSXP`. There is no useful coercion we can
do, so we stop with an error message if the arguments are not of the
correct mode.

The first step in the code is to evaluate the expression in the
environment `rho`, by

```r
    ans = PROTECT(coerceVector(eval(expr, rho), REALSXP));
```

We then allocate space for the calculated derivative by

```r
    gradient = PROTECT(allocMatrix(REALSXP, LENGTH(ans), LENGTH(theta)));
```

The first argument to `allocMatrix` gives the `SEXPTYPE` of the matrix:
here we want it to be `REALSXP`. The other two arguments are the numbers
of rows and columns. (Note that `LENGTH` is intended to be used for
vectors: `length` is more generally applicable.)

```r
    for(i = 0, start = 0; i < LENGTH(theta); i++, start += LENGTH(ans)) {
        par = PROTECT(findVar(installChar(STRING_ELT(theta, i)), rho));
```

Here, we are entering a for loop. We loop through each of the variables.
In the `for` loop, we first create a symbol corresponding to the `i`'th
element of the `STRSXP` `theta`. Here, `STRING_ELT(theta, i)` accesses
the `i`'th element of the `STRSXP` `theta`. Macro `CHAR()` extracts the
actual character representation[^144^](#FOOT144) of it: it
returns a pointer. We then install the name and use `findVar` to find
its value.

```r
        tt = REAL(par)[0];
        xx = fabs(tt);
        delta = (xx < 1) ? eps : xx*eps;
        REAL(par)[0] += delta;
        ans1 = PROTECT(coerceVector(eval(expr, rho), REALSXP));
```

We first extract the real value of the parameter, then calculate
`delta`, the increment to be used for approximating the numerical
derivative. Then we change the value stored in `par` (in environment
`rho`) by `delta` and evaluate `expr` in environment `rho` again.
Because we are directly dealing with original R memory locations here, R
does the evaluation for the changed parameter value.

```r
        for(int j = 0; j < LENGTH(ans); j++)
            rgr[j + start] = (REAL(ans1)[j] - rans[j])/delta;
        REAL(par)[0] = tt;
        UNPROTECT(2);
    }
```

Now, we compute the `i`'th column of the gradient matrix. Note how it is
accessed: R stores matrices by column (like Fortran).

```r
    dimnames = PROTECT(allocVector(VECSXP, 2));
    SET_VECTOR_ELT(dimnames, 1, theta);
    dimnamesgets(gradient, dimnames);
    setAttrib(ans, install("gradient"), gradient);
    UNPROTECT(3);
    return ans;
}
```

First we add column names to the gradient matrix. This is done by
allocating a list (a `VECSXP`) whose first element, the row names, is
`NULL` (the default) and the second element, the column names, is set as
`theta`. This list is then assigned as the attribute having the symbol
`R_DimNamesSymbol`. Finally we set the gradient matrix as the gradient
attribute of `ans`, unprotect the remaining protected locations and
return the answer `ans`.

---

### 5.12 Parsing R code from C

Suppose an R extension want to accept an R expression from the user and
evaluate it. The previous section covered evaluation, but the expression
will be entered as text and needs to be parsed first. A small part of
R's parse interface is declared in header file
`R_ext/Parse.h`[^145^](#FOOT145).

An example of the usage can be found in the (example) Windows package
**windlgs** included in the R source tree. The essential part is

```r
#include <R.h>
#include <Rinternals.h>
#include <R_ext/Parse.h>

SEXP menu_ttest3()
{
    char cmd[256];
    SEXP cmdSexp, cmdexpr, ans = R_NilValue;
    ParseStatus status;
   ...
    if(done == 1) {
        cmdSexp = PROTECT(allocVector(STRSXP, 1));
        SET_STRING_ELT(cmdSexp, 0, mkChar(cmd));
        cmdexpr = PROTECT(R_ParseVector(cmdSexp, -1, &status, R_NilValue));
        if (status != PARSE_OK) {
            UNPROTECT(2);
            error("invalid call %s", cmd);
        }
        /* Loop is needed here as EXPSEXP will be of length > 1 */
        for(int i = 0; i < length(cmdexpr); i++)
            ans = eval(VECTOR_ELT(cmdexpr, i), R_GlobalEnv);
        UNPROTECT(2);
    }
    return ans;
}
```

Note that a single line of text may give rise to more than one R
expression.

`R_ParseVector` is essentially the code used to implement `parse(text=)`
at R level. The first argument is a character vector (corresponding to
`text`) and the second the maximal number of expressions to parse
(corresponding to `n`). The third argument is a pointer to a variable of
an enumeration type, and it is normal (as `parse` does) to regard all
values other than `PARSE_OK` as an error. Other values which might be
returned are `PARSE_INCOMPLETE` (an incomplete expression was found) and
`PARSE_ERROR` (a syntax error), in both cases the value returned being
`R_NilValue`. The fourth argument is a length one character vector to be
used as a filename in error messages, a `srcfile` object or the R `NULL`
object (as in the example above). If a `srcfile` object was used, a
`srcref` attribute would be attached to the result, containing a list of
`srcref` objects of the same length as the expression, to allow it to be
echoed with its original formatting.

---

• [Accessing source references](#Accessing-source-references)

---

---

#### 5.12.1 Accessing source references

The source references added by the parser are recorded by R's evaluator
as it evaluates code. Two functions make these available to debuggers
running C code:

```r
SEXP R_GetCurrentSrcref(int skip);
```

This function checks `R_Srcref` and the current evaluation stack for
entries that contain source reference information. The `skip` argument
tells how many source references to skip before returning the `SEXP` of
the `srcref` object, counting from the top of the stack. If `skip < 0`,
`abs(skip)` locations are counted up from the bottom of the stack. If
too few or no source references are found, `NULL` is returned.

```r
SEXP R_GetSrcFilename(SEXP srcref);
```

This function extracts the filename from the source reference for
display, returning a length 1 character vector containing the filename.
If no name is found, `""` is returned.

---

### 5.13 External pointers and weak references

The `SEXPTYPE`s `EXTPTRSXP` and `WEAKREFSXP` can be encountered at R
level, but are created in C code.

External pointer `SEXP`s are intended to handle references to C
structures such as 'handles', and are used for this purpose in package
[**RODBC**](https://CRAN.R-project.org/package=RODBC) for example. They
are unusual in their copying semantics in that when an R object is
copied, the external pointer object is not duplicated. (For this reason
external pointers should only be used as part of an object with normal
semantics, for example an attribute or an element of a list.)

An external pointer is created by

```r
SEXP R_MakeExternalPtr(void *p, SEXP tag, SEXP prot);
```

where `p` is the pointer (and hence this cannot portably be a function
pointer), and `tag` and `prot` are references to ordinary R objects
which will remain in existence (be protected from garbage collection)
for the lifetime of the external pointer object. A useful convention is
to use the `tag` field for some form of type identification and the
`prot` field for protecting the memory that the external pointer
represents, if that memory is allocated from the R heap. Both `tag` and
`prot` can be `R_NilValue`, and often are.

An alternative way as from R 3.4.0 to create an external pointer from a
function pointer is

```r
typedef void * (*R_DL_FUNC)();
SEXP R_MakeExternalPtrFn(R_DL_FUNC p, SEXP tag, SEXP prot);
```

The elements of an external pointer can be accessed and set _via_

```r
void *R_ExternalPtrAddr(SEXP s);
DL_FUNC R_ExternalPtrAddrFn(SEXP s);
SEXP R_ExternalPtrTag(SEXP s);
SEXP R_ExternalPtrProtected(SEXP s);
void R_ClearExternalPtr(SEXP s);
void R_SetExternalPtrAddr(SEXP s, void *p);
void R_SetExternalPtrTag(SEXP s, SEXP tag);
void R_SetExternalPtrProtected(SEXP s, SEXP p);
```

Clearing a pointer sets its value to the C `NULL` pointer.

An external pointer object can have a _finalizer_, a piece of code to be
run when the object is garbage collected. This can be R code or C code,
and the various interfaces are, respectively.

```r
void R_RegisterFinalizerEx(SEXP s, SEXP fun, Rboolean onexit);

typedef void (*R_CFinalizer_t)(SEXP);
void R_RegisterCFinalizerEx(SEXP s, R_CFinalizer_t fun, Rboolean onexit);
```

The R function indicated by `fun` should be a function of a single
argument, the object to be finalized. R does not perform a garbage
collection when shutting down, and the `onexit` argument of the extended
forms can be used to ask that the finalizer be run during a normal
shutdown of the R session. It is suggested that it is good practice to
clear the pointer on finalization.

The only R level function for interacting with external pointers is
`reg.finalizer` which can be used to set a finalizer.

It is probably not a good idea to allow an external pointer to be
`save`d and then reloaded, but if this happens the pointer will be set
to the C `NULL` pointer.

Finalizers can be run at many places in the code base and much of it,
including the R interpreter, is not re-entrant. So great care is needed
in choosing the code to be run in a finalizer. Finalizers are marked to
be run at garbage collection but only run at a somewhat safe point
thereafter.

Weak references are used to allow the programmer to maintain information
on entities without preventing the garbage collection of the entities
once they become unreachable.

A weak reference contains a key and a value. The value is reachable is
if it either reachable directly or _via_ weak references with reachable
keys. Once a value is determined to be unreachable during garbage
collection, the key and value are set to `R_NilValue` and the finalizer
will be run later in the garbage collection.

Weak reference objects are created by one of

```r
SEXP R_MakeWeakRef(SEXP key, SEXP val, SEXP fin, Rboolean onexit);
SEXP R_MakeWeakRefC(SEXP key, SEXP val, R_CFinalizer_t fin,
                    Rboolean onexit);
```

where the R or C finalizer are specified in exactly the same way as for
an external pointer object (whose finalization interface is implemented
_via_ weak references).

The parts can be accessed _via_

```r
SEXP R_WeakRefKey(SEXP w);
SEXP R_WeakRefValue(SEXP w);
void R_RunWeakRefFinalizer(SEXP w);
```

A toy example of the use of weak references can be found at
<https://homepage.stat.uiowa.edu/~luke/R/references/weakfinex.html>, but
that is used to add finalizers to external pointers which can now be
done more directly. At the time of writing no CRAN or Bioconductor
package uses weak references.

---

• [An external pointer example](#An-external-pointer-example)

---

---

#### 5.13.1 An example

Package [**RODBC**](https://CRAN.R-project.org/package=RODBC) uses
external pointers to maintain its _channels_, connections to databases.
There can be several connections open at once, and the status
information for each is stored in a C structure (pointed to by
`thisHandle` in the code extract below) that is returned _via_ an
external pointer as part of the RODBC 'channel' (as the `"handle_ptr"`
attribute). The external pointer is created by

```r
    SEXP ans, ptr;
    ans = PROTECT(allocVector(INTSXP, 1));
    ptr = R_MakeExternalPtr(thisHandle, install("RODBC_channel"), R_NilValue);
    PROTECT(ptr);
    R_RegisterCFinalizerEx(ptr, chanFinalizer, TRUE);
            ...
    /* return the channel no */
    INTEGER(ans)[0] = nChannels;
    /* and the connection string as an attribute */
    setAttrib(ans, install("connection.string"), constr);
    setAttrib(ans, install("handle_ptr"), ptr);
    UNPROTECT(3);
    return ans;
```

Note the symbol given to identify the usage of the external pointer, and
the use of the finalizer. Since the final argument when registering the
finalizer is `TRUE`, the finalizer will be run at the end of the R
session (unless it crashes). This is used to close and clean up the
connection to the database. The finalizer code is simply

```r
static void chanFinalizer(SEXP ptr)
{
    if(!R_ExternalPtrAddr(ptr)) return;
    inRODBCClose(R_ExternalPtrAddr(ptr));
    R_ClearExternalPtr(ptr); /* not really needed */
}
```

Clearing the pointer and checking for a `NULL` pointer avoids any
possibility of attempting to close an already-closed channel.

R's connections provide another example of using external pointers, in
that case purely to be able to use a finalizer to close and destroy the
connection if it is no longer is use.

---

### 5.14 Vector accessor functions

The vector accessors like `REAL` and `INTEGER` and `VECTOR_ELT` are
_functions_ when used in R extensions. (For efficiency they may be
macros or inline functions when used in the R source code, apart from
`SET_STRING_ELT` and `SET_VECTOR_ELT` which are always functions.)

The accessor functions check that they are being used on an appropriate
type of `SEXP`.

If efficiency is essential, the internal versions of the accessors can
be obtained by defining '`USE_RINTERNALS`' before including
`Rinternals.h`. If you find it necessary to do so, please do
test that your code compiles without '`USE_RINTERNALS`'
defined, as this provides a stricter test that the accessors have been
used correctly. Also be prepared to adjust your code should R internals
change. Note too that the use of '`USE_RINTERNALS`' when the
header is included in C++ code is not supported: doing so may use C99
features which are not necessarily supported by the C++ compiler. Nor is
use with `Rdefines.h` supported.

The accessor functions, and other functions in the R API, are also
subject to change to support the '`ALTREP`' project
(<https://svn.r-project.org/R/branches/ALTREP/ALTREP.html>). Code that
does not define '`USE_RINTERNALS`' should not be affected by
these changes, but code that does define '`USE_RINTERNALS`' may
need to be adjusted.

---

### 5.15 Character encoding issues

`CHARSXP`s can be marked as coming from a known encoding (Latin-1 or
UTF-8). This is mainly intended for human-readable output, and most
packages can just treat such `CHARSXP`s as a whole. However, if they
need to be interpreted as characters or output at C level then it would
normally be correct to ensure that they are converted to the encoding of
the current locale: this can be done by accessing the data in the
`CHARSXP` by `translateChar` rather than by `CHAR`. If re-encoding is
needed this allocates memory with `R_alloc` which thus persists to the
end of the `.Call`/`.External` call unless `vmaxset` is used (see
[Transient storage allocation](#Transient-storage-allocation)).

There is a similar function `translateCharUTF8` which converts to UTF-8:
this has the advantage that a faithful translation is almost always
possible (whereas only a few languages can be represented in the
encoding of the current locale unless that is UTF-8).

Both `translateChar` and `translateCharUTF8` will translate any input,
using escapes such as '`<A9>`' and '`<U+0093>`' to
represent untranslatable parts of the input.

There is a public interface to the encoding marked on `CHARXSXPs` _via_

```r
typedef enum {CE_NATIVE, CE_UTF8, CE_LATIN1, CE_BYTES, CE_SYMBOL, CE_ANY} cetype_t;
cetype_t getCharCE(SEXP);
SEXP mkCharCE(const char *, cetype_t);
```

Only `CE_UTF8` and `CE_LATIN1` are marked on `CHARSXPs` (and so
`Rf_getCharCE` will only return one of the first three), and these
should only be used on non-ASCII strings. Value `CE_BYTES` is used to
make `CHARSXP`s which should be regarded as a set of bytes and not
translated. Value `CE_SYMBOL` is used internally to indicate Adobe
Symbol encoding. Value `CE_ANY` is used to indicate a character string
that will not need re-encoding -- this is used for character strings
known to be in ASCII, and can also be used as an input parameter where
the intention is that the string is treated as a series of bytes. (See
the comments under `mkChar` about the length of input allowed.)

Function

```r
const char *reEnc(const char *x, cetype_t ce_in, cetype_t ce_out,
                  int subst);
```

can be used to re-encode character strings: like `translateChar` it
returns a string allocated by `R_alloc`. This can translate from
`CE_SYMBOL` to `CE_UTF8`, but not conversely. Argument `subst` controls
what to do with untranslatable characters or invalid input: this is done
byte-by-byte with `1` indicates to output hex of the form `<a0>`, and
`2` to replace by `.`, with any other value causing the byte to produce
no output.

There is also

```r
SEXP mkCharLenCE(const char *, size_t, cetype_t);
```

to create marked character strings of a given length.

---
