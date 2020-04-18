3 R and S

---

---

• [What is S?](#What-is-S_003f)     
 • [What is S-PLUS?](#What-is-S_002dPLUS_003f)     
 • [What are the differences between R and S?](#What-are-the-differences-between-R-and-S_003f)     
 • [Is there anything R can do that S-PLUS cannot?](#Is-there-anything-R-can-do-that-S_002dPLUS-cannot_003f)     
 • [What is R-plus?](#What-is-R_002dplus_003f)

---

---

### 3.1 What is S?

S is a very high level language and an environment for data analysis and
graphics. In 1998, the Association for Computing Machinery (ACM)
presented its Software System Award to John M. Chambers, the principal
designer of S, for

> the S system, which has forever altered the way people analyze,
> visualize, and manipulate data ...
>
> S is an elegant, widely accepted, and enduring software system, with
> conceptual integrity, thanks to the insight, taste, and effort of John
> Chambers.

The evolution of the S language is characterized by four books by John
Chambers and coauthors, which are also the primary references for S.

- Richard A. Becker and John M. Chambers (1984), "S. An Interactive
  Environment for Data Analysis and Graphics," Monterey: Wadsworth and
  Brooks/Cole.

  This is also referred to as the "_Brown Book_", and of historical
  interest only.

- Richard A. Becker, John M. Chambers and Allan R. Wilks (1988), "The
  New S Language," London: Chapman & Hall.

  This book is often called the "_Blue Book_", and introduced what is
  now known as S version 2.

- John M. Chambers and Trevor J. Hastie (1992), "Statistical Models in
  S," London: Chapman & Hall.

  This is also called the "_White Book_", and introduced S version 3,
  which added structures to facilitate statistical modeling in S.

- John M. Chambers (1998), "Programming with Data," New York:
  Springer, ISBN 0-387-98503-4
  (<http://statweb.stanford.edu/~jmc4/Sbook/>).

  This "_Green Book_" describes version 4 of S, a major revision of S
  designed by John Chambers to improve its usefulness at every stage
  of the programming process.

See <http://statweb.stanford.edu/~jmc4/papers/96.7.ps> for further
information on the "Evolution of the S Language".

---

### 3.2 What is [S-PLUS]{.small}?

[S-PLUS]{.small} is a value-added version of S currently sold by [TIBCO
Software Inc](http://www.tibco.com/) as 'TIBCO Spotfire S+'. See
<https://en.wikipedia.org/wiki/S-PLUS> for more information.

---

### 3.3 What are the differences between R and S?

We can regard S as a language with three current implementations or
"engines", the "old S engine" (S version 3; [S-PLUS]{.small} 3.x and
4.x), the "new S engine" (S version 4; [S-PLUS]{.small} 5.x and above),
and R. Given this understanding, asking for "the differences between R
and S" really amounts to asking for the specifics of the R
implementation of the S language, i.e., the difference between the R and
S _engines_.

For the remainder of this section, "S" refers to the S engines and not
the S language.

---

• [Lexical scoping](#Lexical-scoping)     
 • [Models](#Models)     
 • [Others](#Others)

---

---

#### 3.3.1 Lexical scoping

Contrary to other implementations of the S language, R has adopted an
evaluation model in which nested function definitions are lexically
scoped. This is analogous to the evaluation model in Scheme.

This difference becomes manifest when _free_ variables occur in a
function. Free variables are those which are neither formal parameters
(occurring in the argument list of the function) nor local variables
(created by assigning to them in the body of the function). In S, the
values of free variables are determined by a set of global variables
(similar to C, there is only local and global scope). In R, they are
determined by the environment in which the function was created.

Consider the following function:

```r
cube <- function(n) {
  sq <- function() n * n
  n * sq()
}
```

Under S, `sq()` does not "know" about the variable `n` unless it is
defined globally:

```r
S> cube(2)
Error in sq():  Object "n" not found
Dumped
S> n <- 3
S> cube(2)
[1] 18
```

In R, the "environment" created when `cube()` was invoked is also looked
in:

```r
R> cube(2)
[1] 8
```

As a more "interesting" real-world problem, suppose you want to write a
function which returns the density function of the _r_-th order
statistic from a sample of size _n_ from a (continuous) distribution.
For simplicity, we shall use both the cdf and pdf of the distribution as
explicit arguments. (Example compiled from various postings by Luke
Tierney.)

The [S-PLUS]{.small} documentation for `call()` basically suggests the
following:

```r
dorder <- function(n, r, pfun, dfun) {
  f <- function(x) NULL
  con <- round(exp(lgamma(n + 1) - lgamma(r) - lgamma(n - r + 1)))
  PF <- call(substitute(pfun), as.name("x"))
  DF <- call(substitute(dfun), as.name("x"))
  f[[length(f)]] <-
    call("*", con,
         call("*", call("^", PF, r - 1),
              call("*", call("^", call("-", 1, PF), n - r),
                   DF)))
  f
}
```

Rather tricky, isn't it? The code uses the fact that in S, functions are
just lists of special mode with the function body as the last argument,
and hence does not work in R (one could make the idea work, though).

A version which makes heavy use of `substitute()` and seems to work
under both S and R is

```r
dorder <- function(n, r, pfun, dfun) {
  con <- round(exp(lgamma(n + 1) - lgamma(r) - lgamma(n - r + 1)))
  eval(substitute(function(x) K * PF(x)^a * (1 - PF(x))^b * DF(x),
                  list(PF = substitute(pfun), DF = substitute(dfun),
                       a = r - 1, b = n - r, K = con)))
}
```

(the `eval()` is not needed in S).

However, in R there is a much easier solution:

```r
dorder <- function(n, r, pfun, dfun) {
  con <- round(exp(lgamma(n + 1) - lgamma(r) - lgamma(n - r + 1)))
  function(x) {
    con * pfun(x)^(r - 1) * (1 - pfun(x))^(n - r) * dfun(x)
  }
}
```

This seems to be the "natural" implementation, and it works because the
free variables in the returned function can be looked up in the defining
environment (this is lexical scope).

Note that what you really need is the function _closure_, i.e., the body
along with all variable bindings needed for evaluating it. Since in the
above version, the free variables in the value function are not
modified, you can actually use it in S as well if you abstract out the
closure operation into a function `MC()` (for "make closure"):

```r
dorder <- function(n, r, pfun, dfun) {
  con <- round(exp(lgamma(n + 1) - lgamma(r) - lgamma(n - r + 1)))
  MC(function(x) {
       con * pfun(x)^(r - 1) * (1 - pfun(x))^(n - r) * dfun(x)
     },
     list(con = con, pfun = pfun, dfun = dfun, r = r, n = n))
}
```

Given the appropriate definitions of the closure operator, this works in
both R and S, and is much "cleaner" than a substitute/eval solution (or
one which overrules the default scoping rules by using explicit access
to evaluation frames, as is of course possible in both R and S).

For R, `MC()` simply is

```r
MC <- function(f, env) f
```

(lexical scope!), a version for S is

```r
MC <- function(f, env = NULL) {
  env <- as.list(env)
  if (mode(f) != "function")
    stop(paste("not a function:", f))
  if (length(env) > 0 && any(names(env) == ""))
    stop(paste("not all arguments are named:", env))
  fargs <- if(length(f) > 1) f[1:(length(f) - 1)] else NULL
  fargs <- c(fargs, env)
  if (any(duplicated(names(fargs))))
    stop(paste("duplicated arguments:", paste(names(fargs)),
         collapse = ", "))
  fbody <- f[length(f)]
  cf <- c(fargs, fbody)
  mode(cf) <- "function"
  return(cf)
}
```

Similarly, most optimization (or zero-finding) routines need some
arguments to be optimized over and have other parameters that depend on
the data but are fixed with respect to optimization. With R scoping
rules, this is a trivial problem; simply make up the function with the
required definitions in the same environment and scoping takes care of
it. With S, one solution is to add an extra parameter to the function
and to the optimizer to pass in these extras, which however can only
work if the optimizer supports this.

Nested lexically scoped functions allow using function closures and
maintaining local state. A simple example (taken from Abelson and
Sussman) is obtained by typing [demo(\"scoping\")]{.kbd} at the R
prompt. Further information is provided in the standard R reference "R:
A Language for Data Analysis and Graphics" (see [What documentation
exists for R?](#What-documentation-exists-for-R_003f)) and in Robert
Gentleman and Ross Ihaka (2000), "Lexical Scope and Statistical
Computing", [_Journal of Computational and Graphical
Statistics_](http://www.amstat.org/publications/jcgs/), **9**, 491--508.

Nested lexically scoped functions also imply a further major difference.
Whereas S stores all objects as separate files in a directory somewhere
(usually `.Data` under the current directory), R does not. All
objects in R are stored internally. When R is started up it grabs a
piece of memory and uses it to store the objects. R performs its own
memory management of this piece of memory, growing and shrinking its
size as needed. Having everything in memory is necessary because it is
not really possible to externally maintain all relevant "environments"
of symbol/value pairs. This difference also seems to make R _faster_
than S.

The down side is that if R crashes you will lose all the work for the
current session. Saving and restoring the memory "images" (the functions
and data stored in R's internal memory at any time) can be a bit slow,
especially if they are big. In S this does not happen, because
everything is saved in disk files and if you crash nothing is likely to
happen to them. (In fact, one might conjecture that the S developers
felt that the price of changing their approach to persistent storage
just to accommodate lexical scope was far too expensive.) Hence, when
doing important work, you might consider saving often (see [How can I
save my workspace?](#How-can-I-save-my-workspace_003f)) to safeguard
against possible crashes. Other possibilities are logging your sessions,
or have your R commands stored in text files which can be read in using
`source()`.

> **Note:** If you run R from within Emacs (see [R and
> Emacs](#R-and-Emacs)), you can save the contents of the interaction
> buffer to a file and conveniently manipulate it using
> `ess-transcript-mode`, as well as save source copies of all functions
> and data used.

---

#### 3.3.2 Models

There are some differences in the modeling code, such as

- Whereas in S, you would use `lm(y ~ x^3)` to regress `y` on `x^3`,
  in R, you have to insulate powers of numeric vectors (using `I()`),
  i.e., you have to use `lm(y ~ I(x^3))`.
- The glm family objects are implemented differently in R and S. The
  same functionality is available but the components have different
  names.
- Option `na.action` is set to `"na.omit"` by default in R, but not
  set in S.
- Terms objects are stored differently. In S a terms object is an
  expression with attributes, in R it is a formula with attributes.
  The attributes have the same names but are mostly stored
  differently.
- Finally, in R `y ~ x + 0` is an alternative to `y ~ x - 1` for
  specifying a model with no intercept. Models with no parameters at
  all can be specified by `y ~ 0`.

---

#### 3.3.3 Others

Apart from lexical scoping and its implications, R follows the S
language definition in the Blue and White Books as much as possible, and
hence really is an "implementation" of S. There are some intentional
differences where the behavior of S is considered "not clean". In
general, the rationale is that R should help you detect programming
errors, while at the same time being as compatible as possible with S.

Some known differences are the following.

- In R, if `x` is a list, then `x[i] <- NULL` and `x[[i]] <- NULL`
  remove the specified elements from `x`. The first of these is
  incompatible with S, where it is a no-op. (Note that you can set
  elements to `NULL` using `x[i] <- list(NULL)`.)

- In S, the functions named `.First` and `.Last` in the
  `.Data` directory can be used for customizing, as they are
  executed at the very beginning and end of a session, respectively.

  In R, the startup mechanism is as follows. Unless
  `--no-environ` was given on the command line, R searches
  for site and user files to process for setting environment
  variables. Then, R searches for a site-wide startup profile unless
  the command line option `--no-site-file` was given. This
  code is loaded in package **base**. Then, unless
  `--no-init-file` was given, R searches for a user profile
  file, and sources it into the user workspace. It then loads a saved
  image of the user workspace from `.RData` in case there is
  one (unless `--no-restore-data` or `--no-restore`
  were specified). Next, a function `.First()` is run if found on the
  search path. Finally, function `.First.sys` in the **base** package
  is run. When terminating an R session, by default a function `.Last`
  is run if found on the search path, followed by `.Last.sys`. If
  needed, the functions `.First()` and `.Last()` should be defined in
  the appropriate startup profiles. See the help pages for `.First`
  and `.Last` for more details.

- In R, `T` and `F` are just variables being set to `TRUE` and
  `FALSE`, respectively, but are not reserved words as in S and hence
  can be overwritten by the user. (This helps e.g. when you have
  factors with levels `"T"` or `"F"`.) Hence, when writing code you
  should always use `TRUE` and `FALSE`.

- In R, `dyn.load()` can only load _shared objects_, as created for
  example by [R CMD SHLIB]{.kbd}.

- In R, `attach()` currently only works for lists and data frames, but
  not for directories. (In fact, `attach()` also works for R data
  files created with `save()`, which is analogous to attaching
  directories in S.) Also, you cannot attach at position 1.

- Categories do not exist in R, and never will as they are deprecated
  now in S. Use factors instead.

- In R, `For()` loops are not necessary and hence not supported.

- In R, `assign()` uses the argument `envir=` rather than
  `where=` as in S.

- The random number generators are different, and the seeds have
  different length.

- R passes integer objects to C as `int *` rather than `long *` as
  in S.

- R has no single precision storage mode. However, as of version
  0.65.1, there is a single precision interface to C/FORTRAN
  subroutines.

- By default, `ls()` returns the names of the objects in the current
  (under R) and global (under S) environment, respectively. For
  example, given

```r
x <- 1; fun <- function() {y <- 1; ls()}
```

then `fun()` returns `"y"` in R and `"x"` (together with the rest of
the global environment) in S.

- R allows for zero-extent matrices (and arrays, i.e., some elements
  of the `dim` attribute vector can be 0). This has been determined a
  useful feature as it helps reducing the need for special-case tests
  for empty subsets. For example, if `x` is a matrix, `x[, FALSE]` is
  not `NULL` but a "matrix" with 0 columns. Hence, such objects need
  to be tested for by checking whether their `length()` is zero (which
  works in both R and S), and not using `is.null()`.

- Named vectors are considered vectors in R but not in S (e.g.,
  `is.vector(c(a = 1:3))` returns `FALSE` in S and `TRUE` in R).

- Data frames are not considered as matrices in R (i.e., if `DF` is a
  data frame, then `is.matrix(DF)` returns `FALSE` in R and `TRUE` in
  S).

- R by default uses treatment contrasts in the unordered case, whereas
  S uses the Helmert ones. This is a deliberate difference reflecting
  the opinion that treatment contrasts are more natural.

- In R, the argument of a replacement function which corresponds to
  the right hand side must be named '`value`'. E.g.,
  `f(a) <- b` is evaluated as `a <- "f<-"(a, value = b)`. S always
  takes the last argument, irrespective of its name.

- In S, `substitute()` searches for names for substitution in the
  given expression in three places: the actual and the default
  arguments of the matching call, and the local frame (in that order).
  R looks in the local frame only, with the special rule to use a
  "promise" if a variable is not evaluated. Since the local frame is
  initialized with the actual arguments or the default expressions,
  this is usually equivalent to S, until assignment takes place.

- In S, the index variable in a `for()` loop is local to the inside of
  the loop. In R it is local to the environment where the `for()`
  statement is executed.

- In S, `tapply(simplify=TRUE)` returns a vector where R returns a
  one-dimensional array (which can have named dimnames).

- In S(-[PLUS]{.small}) the C locale is used, whereas in R the current
  operating system locale is used for determining which characters are
  alphanumeric and how they are sorted. This affects the set of valid
  names for R objects (for example accented chars may be allowed in R)
  and ordering in sorts and comparisons (such as whether `"aA" < "Bb"`
  is true or false). From version 1.2.0 the locale can be (re-)set in
  R by the `Sys.setlocale()` function.

- In S, `missing(arg)` remains `TRUE` if `arg`{.variable} is
  subsequently modified; in R it doesn't.

- From R version 1.3.0, `data.frame` strips `I()` when creating
  (column) names.

- In R, the string `"NA"` is not treated as a missing value in a
  character variable. Use `as.character(NA)` to create a missing
  character value.

- R disallows repeated formal arguments in function calls.

- In S, `dump()`, `dput()` and `deparse()` are essentially different
  interfaces to the same code. In R from version 2.0.0, this is only
  true if the same `control` argument is used, but by default it is
  not. By default `dump()` tries to write code that will evaluate to
  reproduce the object, whereas `dput()` and `deparse()` default to
  options for producing deparsed code that is readable.

- In R, indexing a vector, matrix, array or data frame with `[` using
  a character vector index looks only for exact matches (whereas `[[`
  and `$` allow partial matches). In S, `[` allows partial matches.

- S has a two-argument version of `atan` and no `atan2`. A call in S
  such as `atan(x1, x2)` is equivalent to R's `atan2(x1, x2)`.
  However, beware of named arguments since S's `atan(x = a, y = b)` is
  equivalent to R's `atan2(y = a, x = b)` with the meanings of `x` and
  `y` interchanged. (R used to have undocumented support for a
  two-argument `atan` with positional arguments, but this has been
  withdrawn to avoid further confusion.)

- Numeric constants with no fractional and exponent (i.e., only
  integer) part are taken as integer in [S-PLUS]{.small} 6.x or later,
  but as double in R.

There are also differences which are not intentional, and result from
missing or incorrect code in R. The developers would appreciate hearing
about any deficiencies you may find (in a written report fully
documenting the difference as you see it). Of course, it would be useful
if you were to implement the change yourself and make sure it works.

---

### 3.4 Is there anything R can do that [S-PLUS]{.small} cannot?

Since almost anything you can do in R has source code that you could
port to [S-PLUS]{.small} with little effort there will never be much you
can do in R that you couldn't do in [S-PLUS]{.small} if you wanted to.
(Note that using lexical scoping may simplify matters considerably,
though.)

R offers several graphics features that [S-PLUS]{.small} does not, such
as finer handling of line types, more convenient color handling (via
palettes), gamma correction for color, and, most importantly,
mathematical annotation in plot texts, via input expressions reminiscent
of TeX constructs. See the help page for `plotmath`, which features an
impressive on-line example. More details can be found in Paul Murrell
and Ross Ihaka (2000), "An Approach to Providing Mathematical Annotation
in Plots", [_Journal of Computational and Graphical
Statistics_](http://www.amstat.org/publications/jcgs/), **9**, 582--599.

---

### 3.5 What is R-plus?

For a very long time, there was no such thing.

[XLSolutions Corporation](http://www.xlsolutions-corp.com/) is currently
beta testing a commercially supported version of R named R+ (read R
plus).

[Revolution Analytics](http://www.revolution-computing.com/) has
released REvolution R, now available as Microsoft R (see
<http://blog.revolutionanalytics.com/2016/01/microsoft-r-open.html> for
more information).

See also
<https://en.wikipedia.org/wiki/R_programming_language#Commercialized_versions_of_R>
for pointers to commercialized versions of R.

---
