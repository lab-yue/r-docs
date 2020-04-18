# 10 Writing your own functions

---

As we have seen informally along the way, the R language allows the user
to create objects of mode _function_. These are true R functions that
are stored in a special internal form and may be used in further
expressions and so on. In the process, the language gains enormously in
power, convenience and elegance, and learning to write useful functions
is one of the main ways to make your use of R comfortable and
productive.

It should be emphasized that most of the functions supplied as part of
the R system, such as `mean()`, `var()`, `postscript()` and so on, are
themselves written in R and thus do not differ materially from user
written functions.

A function is defined by an assignment of the form

```r
> name <- function(arg_1, arg_2, …) expression
```

The `expression` is an R expression, (usually a grouped
expression), that uses the arguments, `arg_i`, to calculate a
value. The value of the expression is the value returned for the
function.

A call to the function then usually takes the form
`name(expr_1, expr_2, …)` and may occur anywhere a function call is
legitimate.

---

• [Simple examples](#Simple-examples)     
 • [Defining new binary operators](#Defining-new-binary-operators)     
 • [Named arguments and defaults](#Named-arguments-and-defaults)     
 • [The three dots argument](#The-three-dots-argument)     
 • [Assignment within functions](#Assignment-within-functions)     
 • [More advanced examples](#More-advanced-examples)     
 • [Scope](#Scope)     
 • [Customizing the environment](#Customizing-the-environment)     
 • [Object orientation](#Object-orientation)

---

---

### 10.1 Simple examples

As a first example, consider a function to calculate the two sample
_t_-statistic, showing "all the steps". This is an artificial example,
of course, since there are other, simpler ways of achieving the same
end.

The function is defined as follows:

```r
> twosam <- function(y1, y2) {
    n1  <- length(y1); n2  <- length(y2)
    yb1 <- mean(y1);   yb2 <- mean(y2)
    s1  <- var(y1);    s2  <- var(y2)
    s <- ((n1-1)*s1 + (n2-1)*s2)/(n1+n2-2)
    tst <- (yb1 - yb2)/sqrt(s*(1/n1 + 1/n2))
    tst
  }
```

With this function defined, you could perform two sample _t_-tests using
a call such as

```r
> tstat <- twosam(data$male, data$female); tstat
```

As a second example, consider a function to emulate directly the
[MATLAB] backslash command, which returns the coefficients of
the orthogonal projection of the vector _y_ onto the column space of the
matrix, _X_. (This is ordinarily called the least squares estimate of
the regression coefficients.) This would ordinarily be done with the
`qr()` function; however this is sometimes a bit tricky to use directly
and it pays to have a simple function such as the following to use it
safely.

Thus given a _n_ by _1_ vector _y_ and an _n_ by _p_ matrix _X_ then _X
\\ y_ is defined as (X'X)\^{-}X'y, where (X'X)\^{-} is a generalized
inverse of _X\'X_.

```r
> bslash <- function(X, y) {
  X <- qr(X)
  qr.coef(X, y)
}
```

After this object is created it may be used in statements such as

```r
> regcoeff <- bslash(Xmat, yvar)
```

and so on.

The classical R function `lsfit()` does this job quite well, and
more[^22^](#FOOT22). It in turn uses the functions `qr()` and
`qr.coef()` in the slightly counterintuitive way above to do this part
of the calculation. Hence there is probably some value in having just
this part isolated in a simple to use function if it is going to be in
frequent use. If so, we may wish to make it a matrix binary operator for
even more convenient use.

---

### 10.2 Defining new binary operators

Had we given the `bslash()` function a different name, namely one of the
form

```r
%anything%
```

it could have been used as a _binary operator_ in expressions rather
than in function form. Suppose, for example, we choose `!` for the
internal character. The function definition would then start as

```r
> "%!%" <- function(X, y) { … }
```

(Note the use of quote marks.) The function could then be used as
`X %!% y`. (The backslash symbol itself is not a convenient choice as it
presents special problems in this context.)

The matrix multiplication operator, `%*%`, and the outer product matrix
operator `%o%` are other examples of binary operators defined in this
way.

---

### 10.3 Named arguments and defaults

As first noted in [Generating regular sequences](#Generating-regular-sequences), if arguments to called
functions are given in the "`name=object`" form, they may be given in
any order. Furthermore the argument sequence may begin in the unnamed,
positional form, and specify named arguments after the positional
arguments.

Thus if there is a function `fun1` defined by

```r
> fun1 <- function(data, data.frame, graph, limit) {
    [function body omitted]
  }
```

then the function may be invoked in several ways, for example

```r
> ans <- fun1(d, df, TRUE, 20)
> ans <- fun1(d, df, graph=TRUE, limit=20)
> ans <- fun1(data=d, limit=20, graph=TRUE, data.frame=df)
```

are all equivalent.

In many cases arguments can be given commonly appropriate default
values, in which case they may be omitted altogether from the call when
the defaults are appropriate. For example, if `fun1` were defined as

```r
> fun1 <- function(data, data.frame, graph=TRUE, limit=20) { … }
```

it could be called as

```r
> ans <- fun1(d, df)
```

which is now equivalent to the three cases above, or as

```r
> ans <- fun1(d, df, limit=10)
```

which changes one of the defaults.

It is important to note that defaults may be arbitrary expressions, even
involving other arguments to the same function; they are not restricted
to be constants as in our simple example here.

---

### 10.4 The '`…`' argument

Another frequent requirement is to allow one function to pass on
argument settings to another. For example many graphics functions use
the function `par()` and functions like `plot()` allow the user to pass
on graphical parameters to `par()` to control the graphical output. (See
[The par() function](#The-par_0028_0029-function), for more details on
the `par()` function.) This can be done by including an extra argument,
literally '`…`', of the function, which may then be passed on.
An outline example is given below.

```r
fun1 <- function(data, data.frame, graph=TRUE, limit=20, ...) {
  [omitted statements]
  if (graph)
    par(pch="*", ...)
  [more omissions]
}
```

Less frequently, a function will need to refer to components of
'`…`'. The expression `list(...)` evaluates all such arguments
and returns them in a named list, while `..1`, `..2`, etc. evaluate them
one at a time, with '`..n`' returning the n'th unmatched
argument.

---

### 10.5 Assignments within functions

Note that _any ordinary assignments done within the function are local
and temporary and are lost after exit from the function_. Thus the
assignment `X <- qr(X)` does not affect the value of the argument in the
calling program.

To understand completely the rules governing the scope of R assignments
the reader needs to be familiar with the notion of an evaluation
_frame_. This is a somewhat advanced, though hardly difficult, topic and
is not covered further here.

If global and permanent assignments are intended within a function, then
either the "superassignment" operator, `<<-` or the function `assign()`
can be used. See the `help` document for details. [S-PLUS] users
should be aware that `<<-` has different semantics in R. These are
discussed further in [Scope](#Scope).

---

### 10.6 More advanced examples

---

• [Efficiency factors in block designs](#Efficiency-factors-in-block-designs)     
 • [Dropping all names in a printed array](#Dropping-all-names-in-a-printed-array)     
 • [Recursive numerical integration](#Recursive-numerical-integration)

---

---

#### 10.6.1 Efficiency factors in block designs

As a more complete, if a little pedestrian, example of a function,
consider finding the efficiency factors for a block design. (Some
aspects of this problem have already been discussed in [Index matrices](#Index-matrices).)

A block design is defined by two factors, say `blocks` (`b` levels) and
`varieties` (`v` levels). If _R_ and _K_ are the _v_ by _v_ and _b_ by
_b_ _replications_ and _block size_ matrices, respectively, and _N_ is
the _b_ by _v_ incidence matrix, then the efficiency factors are defined
as the eigenvalues of the matrix E = I_v - R\^{-1/2}N'K\^{-1}NR\^{-1/2}
= I_v - A'A, where A = K\^{-1/2}NR\^{-1/2}. One way to write the
function is given below.

```r
> bdeff <- function(blocks, varieties) {
    blocks <- as.factor(blocks)             # minor safety move
    b <- length(levels(blocks))
    varieties <- as.factor(varieties)       # minor safety move
    v <- length(levels(varieties))
    K <- as.vector(table(blocks))           # remove dim attr
    R <- as.vector(table(varieties))        # remove dim attr
    N <- table(blocks, varieties)
    A <- 1/sqrt(K) * N * rep(1/sqrt(R), rep(b, v))
    sv <- svd(A)
    list(eff=1 - sv$d^2, blockcv=sv$u, varietycv=sv$v)
}
```

It is numerically slightly better to work with the singular value
decomposition on this occasion rather than the eigenvalue routines.

The result of the function is a list giving not only the efficiency
factors as the first component, but also the block and variety canonical
contrasts, since sometimes these give additional useful qualitative
information.

---

#### 10.6.2 Dropping all names in a printed array

For printing purposes with large matrices or arrays, it is often useful
to print them in close block form without the array names or numbers.
Removing the `dimnames` attribute will not achieve this effect, but
rather the array must be given a `dimnames` attribute consisting of
empty strings. For example to print a matrix, `X`

```r
> temp <- X
> dimnames(temp) <- list(rep("", nrow(X)), rep("", ncol(X)))
> temp; rm(temp)
```

This can be much more conveniently done using a function,
`no.dimnames()`, shown below, as a "wrap around" to achieve the same
result. It also illustrates how some effective and useful user functions
can be quite short.

```r
no.dimnames <- function(a) {
  ## Remove all dimension names from an array for compact printing.
  d <- list()
  l <- 0
  for(i in dim(a)) {
    d[[l <- l + 1]] <- rep("", i)
  }
  dimnames(a) <- d
  a
}
```

With this function defined, an array may be printed in close format
using

```r
> no.dimnames(X)
```

This is particularly useful for large integer arrays, where patterns are
the real interest rather than the values.

---

#### 10.6.3 Recursive numerical integration

Functions may be recursive, and may themselves define functions within
themselves. Note, however, that such functions, or indeed variables, are
not inherited by called functions in higher evaluation frames as they
would be if they were on the search path.

The example below shows a naive way of performing one-dimensional
numerical integration. The integrand is evaluated at the end points of
the range and in the middle. If the one-panel trapezium rule answer is
close enough to the two panel, then the latter is returned as the value.
Otherwise the same process is recursively applied to each panel. The
result is an adaptive integration process that concentrates function
evaluations in regions where the integrand is farthest from linear.
There is, however, a heavy overhead, and the function is only
competitive with other algorithms when the integrand is both smooth and
very difficult to evaluate.

The example is also given partly as a little puzzle in R programming.

```r
area <- function(f, a, b, eps = 1.0e-06, lim = 10) {
  fun1 <- function(f, a, b, fa, fb, a0, eps, lim, fun) {
    ## function ‘fun1’ is only visible inside ‘area’
    d <- (a + b)/2
    h <- (b - a)/4
    fd <- f(d)
    a1 <- h * (fa + fd)
    a2 <- h * (fd + fb)
    if(abs(a0 - a1 - a2) < eps || lim == 0)
      return(a1 + a2)
    else {
      return(fun(f, a, d, fa, fd, a1, eps, lim - 1, fun) +
             fun(f, d, b, fd, fb, a2, eps, lim - 1, fun))
    }
  }
  fa <- f(a)
  fb <- f(b)
  a0 <- ((fa + fb) * (b - a))/2
  fun1(f, a, b, fa, fb, a0, eps, lim, fun1)
}
```

---

• [Scope](#Scope)     
 • [Object orientation](#Object-orientation)

---

---

### 10.7 Scope

The discussion in this section is somewhat more technical than in other
parts of this document. However, it details one of the major differences
between [S-PLUS] and R.

The symbols which occur in the body of a function can be divided into
three classes; formal parameters, local variables and free variables.
The formal parameters of a function are those occurring in the argument
list of the function. Their values are determined by the process of
_binding_ the actual function arguments to the formal parameters. Local
variables are those whose values are determined by the evaluation of
expressions in the body of the functions. Variables which are not formal
parameters or local variables are called free variables. Free variables
become local variables if they are assigned to. Consider the following
function definition.

```r
f <- function(x) {
  y <- 2*x
  print(x)
  print(y)
  print(z)
}
```

In this function, `x` is a formal parameter, `y` is a local variable and
`z` is a free variable.

In R the free variable bindings are resolved by first looking in the
environment in which the function was created. This is called _lexical
scope_. First we define a function called `cube`.

```r
cube <- function(n) {
  sq <- function() n*n
  n*sq()
}
```

The variable `n` in the function `sq` is not an argument to that
function. Therefore it is a free variable and the scoping rules must be
used to ascertain the value that is to be associated with it. Under
static scope ([S-PLUS]) the value is that associated with a
global variable named `n`. Under lexical scope (R) it is the parameter
to the function `cube` since that is the active binding for the variable
`n` at the time the function `sq` was defined. The difference between
evaluation in R and evaluation in [S-PLUS] is that
[S-PLUS] looks for a global variable called `n` while R first
looks for a variable called `n` in the environment created when `cube`
was invoked.

```r
## first evaluation in S
S> cube(2)
Error in sq(): Object "n" not found
Dumped
S> n <- 3
S> cube(2)
[1] 18
## then the same function evaluated in R
R> cube(2)
[1] 8
```

Lexical scope can also be used to give functions _mutable state_. In the
following example we show how R can be used to mimic a bank account. A
functioning bank account needs to have a balance or total, a function
for making withdrawals, a function for making deposits and a function
for stating the current balance. We achieve this by creating the three
functions within `account` and then returning a list containing them.
When `account` is invoked it takes a numerical argument `total` and
returns a list containing the three functions. Because these functions
are defined in an environment which contains `total`, they will have
access to its value.

The special assignment operator, `<<-`, is
used to change the value associated with `total`. This operator looks
back in enclosing environments for an environment that contains the
symbol `total` and when it finds such an environment it replaces the
value, in that environment, with the value of right hand side. If the
global or top-level environment is reached without finding the symbol
`total` then that variable is created and assigned to there. For most
users `<<-` creates a global variable and assigns the value of the right
hand side to it[^23^](#FOOT23). Only when `<<-` has been used
in a function that was returned as the value of another function will
the special behavior described here occur.

```r
open.account <- function(total) {
  list(
    deposit = function(amount) {
      if(amount <= 0)
        stop("Deposits must be positive!\n")
      total <<- total + amount
      cat(amount, "deposited.  Your balance is", total, "\n\n")
    },
    withdraw = function(amount) {
      if(amount > total)
        stop("You don't have that much money!\n")
      total <<- total - amount
      cat(amount, "withdrawn.  Your balance is", total, "\n\n")
    },
    balance = function() {
      cat("Your balance is", total, "\n\n")
    }
  )
}

ross <- open.account(100)
robert <- open.account(200)

ross$withdraw(30)
ross$balance()
robert$balance()

ross$deposit(50)
ross$balance()
ross$withdraw(500)
```

---

### 10.8 Customizing the environment

Users can customize their environment in several different ways. There
is a site initialization file and every directory can have its own
special initialization file. Finally, the special functions `.First` and
`.Last` can be used.

The location of the site initialization file is taken from the value of
the `R_PROFILE` environment variable. If that variable is unset, the
file `Rprofile.site` in the R home subdirectory `etc`
is used. This file should contain the commands that you want to execute
every time R is started under your system. A second, personal, profile
file named `.Rprofile`[^24^](#FOOT24) can be placed in
any directory. If R is invoked in that directory then that file will be
sourced. This file gives individual users control over their workspace
and allows for different startup procedures in different working
directories. If no `.Rprofile` file is found in the startup
directory, then R looks for a `.Rprofile` file in the user's
home directory and uses that (if it exists). If the environment variable
`R_PROFILE_USER` is set, the file it points to is used instead of the
`.Rprofile` files.

Any function named `.First()` in either of the two profile files or in
the `.RData` image has a special status. It is automatically
performed at the beginning of an R session and may be used to initialize
the environment. For example, the definition in the example below alters
the prompt to `$` and sets up various other useful things that can then
be taken for granted in the rest of the session.

Thus, the sequence in which files are executed is,
`Rprofile.site`, the user profile, `.RData` and then
`.First()`. A definition in later files will mask definitions in earlier
files.

```r
> .First <- function() {
  options(prompt="$ ", continue="+\t")  # $ is the prompt
  options(digits=5, length=999)         # custom numbers and printout
  x11()                                 # for graphics
  par(pch = "+")                        # plotting character
  source(file.path(Sys.getenv("HOME"), "R", "mystuff.R"))
                                        # my personal functions
  library(MASS)                         # attach a package
}
```

Similarly a function `.Last()`, if defined, is (normally) executed at
the very end of the session. An example is given below.

```r
> .Last <- function() {
  graphics.off()                        # a small safety measure.
  cat(paste(date(),"\nAdios\n"))        # Is it time for lunch?
}
```

---

### 10.9 Classes, generic functions and object orientation

The class of an object determines how it will be treated by what are
known as _generic_ functions. Put the other way round, a generic
function performs a task or action on its arguments _specific to the
class of the argument itself_. If the argument lacks any `class`
attribute, or has a class not catered for specifically by the generic
function in question, there is always a _default action_ provided.

An example makes things clearer. The class mechanism offers the user the
facility of designing and writing generic functions for special
purposes. Among the other generic functions are `plot()` for displaying
objects graphically, `summary()` for summarizing analyses of various
types, and `anova()` for comparing statistical models.

The number of generic functions that can treat a class in a specific way
can be quite large. For example, the functions that can accommodate in
some fashion objects of class `"data.frame"` include

```r
[     [[<-    any    as.matrix
[<-   mean    plot   summary
```

A currently complete list can be got by using the `methods()` function:

```r
> methods(class="data.frame")
```

Conversely the number of classes a generic function can handle can also
be quite large. For example the `plot()` function has a default method
and variants for objects of classes `"data.frame"`, `"density"`,
`"factor"`, and more. A complete list can be got again by using the
`methods()` function:

```r
> methods(plot)
```

For many generic functions the function body is quite short, for example

```r
> coef
function (object, ...)
UseMethod("coef")
```

The presence of `UseMethod` indicates this is a generic function. To see
what methods are available we can use `methods()`

```r
> methods(coef)
[1] coef.aov*         coef.Arima*       coef.default*     coef.listof*
[5] coef.nls*         coef.summary.nls*

   Non-visible functions are asterisked
```

In this example there are six methods, none of which can be seen by
typing its name. We can read these by either of

```r
> getAnywhere("coef.aov")
A single object matching ‘coef.aov’ was found
It was found in the following places
  registered S3 method for coef from namespace stats
  namespace:stats
with value

function (object, ...)
{
    z <- object$coef
    z[!is.na(z)]
}

> getS3method("coef", "aov")
function (object, ...)
{
    z <- object$coef
    z[!is.na(z)]
}
```

A function named `gen.cl` will be invoked by the generic `gen` for class
`cl`, so do not name functions in this style unless they are intended to
be methods.

The reader is referred to the _R Language Definition_ for a more
complete discussion of this mechanism.

---
