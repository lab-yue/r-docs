# 6 Computing on the language

---

R belongs to a class of programming languages in which subroutines have
the ability to modify or construct other subroutines and evaluate the
result as an integral part of the language itself. This is similar to
Lisp and Scheme and other languages of the "functional programming"
variety, but in contrast to FORTRAN and the ALGOL family. The Lisp
family takes this feature to the extreme by the "everything is a list"
paradigm in which there is no distinction between programs and data.

R presents a friendlier interface to programming than Lisp does, at
least to someone used to mathematical formulas and C-like control
structures, but the engine is really very Lisp-like. R allows direct
access to parsed expressions and functions and
allows you to alter and subsequently execute them, or create entirely
new functions from scratch.

There is a number of standard applications of this facility, such as
calculation of analytical derivatives of expressions, or the generation
of polynomial functions from a vector of coefficients. However, there
are also uses that are much more fundamental to the workings of the
interpreted part of R. Some of these are essential to the reuse of
functions as components in other functions, as the (admittedly not very
pretty) calls to `model.frame` that are constructed in several modeling
and plotting routines. Other uses simply allow elegant interfaces to
useful functionality. As an example, consider the `curve` function,
which allows you to draw the graph of a function given as an expression
like `sin(x)` or the facilities for plotting mathematical expressions.

In this chapter, we give an introduction to the set of facilities that
are available for computing on the language.

---

• [Direct manipulation of language objects](#Direct-manipulation-of-language-objects)     
 • [Substitutions](#Substitutions)     
 • [More on evaluation](#More-on-evaluation)     
 • [Evaluation of expression objects](#Evaluation-of-expression-objects)     
 • [Manipulation of function calls](#Manipulation-of-function-calls)     
 • [Manipulation of functions](#Manipulation-of-functions)

---

---

### 6.1 Direct manipulation of language objects

There are three kinds of language objects that are available for
modification, calls, expressions, and functions. At this point, we shall
concentrate on the call objects. These are sometimes referred to as
"unevaluated expressions", although this terminology is somewhat
confusing. The most direct method of obtaining a call object is to use
`quote` with an expression argument, e.g.,

```r
> e1 <- quote(2 + 2)
> e2 <- quote(plot(x, y))
```

The arguments are not evaluated, the result is simply the parsed
argument. The objects `e1` and `e2` may be evaluated later using `eval`,
or simply manipulated as data. It is perhaps most immediately obvious
why the `e2` object has mode `"call"`, since it involves a call to the
`plot` function with some arguments. However, `e1` actually has exactly
the same structure as a call to the binary operator `+` with two
arguments, a fact that gets clearly displayed by the following

```r
> quote("+"(2, 2))
2 + 2
```

The components of a call object are accessed using a list-like syntax,
and may in fact be converted to and from lists using `as.list` and
`as.call`

```r
> e2[[1]]
plot
> e2[[2]]
x
> e2[[3]]
y
```

When keyword argument matching is used, the keywords can be used as list
tags:

```r
> e3 <- quote(plot(x = age, y = weight))
> e3$x
age
> e3$y
weight
```

All the components of the call object have mode `"name"` in the
preceding examples. This is true for identifiers in calls, but the
components of a call can also be constants---which can be of any type,
although the first component had better be a function if the call is to
be evaluated successfully---or other call objects, corresponding to
subexpressions. Objects of mode name can be
constructed from character strings using `as.name`, so one might modify
the `e2` object as follows

```r
> e2[[1]] <- as.name("+")
> e2
x + y
```

To illustrate the fact that subexpressions are simply components that
are themselves calls, consider

```r
> e1[[2]] <- e2
> e1
x + y + 2
```

All grouping parentheses in input are preserved in parsed expressions.
They are represented as a function call with one argument, so that
`4 - (2 - 2)` becomes `"-"(4, "(" ("-"(2, 2)))` in prefix notation. In
evaluations, the '`(`' operator just returns its argument.

This is a bit unfortunate, but it is not easy to write a
parser/deparser combination that both preserves
user input, stores it in minimal form and ensures that parsing a
deparsed expression gives the same expression back.

As it happens, R's parser is not perfectly invertible, nor is its
deparser, as the following examples show

```r
> str(quote(c(1,2)))
 language c(1, 2)
> str(c(1,2))
 num [1:2] 1 2
> deparse(quote(c(1,2)))
[1] "c(1, 2)"
> deparse(c(1,2))
[1] "c(1, 2)"
> quote("-"(2, 2))
2 - 2
> quote(2 - 2)
2 - 2
```

Deparsed expressions should, however, evaluate to an equivalent value to
the original expression (up to rounding error).

\...internal storage of flow control constructs\...note Splus
incompatibility\...

---

### 6.2 Substitutions

It is in fact not often that one wants to modify the innards of an
expression like in the previous section. More frequently, one wants to
simply get at an expression in order to deparse it and use it for
labeling plots, for instance. An example of this is seen at the
beginning of `plot.default`:

```r
xlabel <- if (!missing(x))
    deparse(substitute(x))
```

This causes the variable or expression given as the `x` argument to
`plot` to be used for labeling the x-axis later on.

The function used to achieve this is `substitute` which takes the
expression `x` and substitutes the expression that was passed through
the formal argument `x`. Notice that for this to happen, `x` must carry
information about the expression that creates its value. This is related
to the lazy evaluation scheme of R
(see [Promise objects](#Promise-objects)). A formal argument is really a
_promise_, an object with three slots, one for the expression that
defines it, one for the environment in which to evaluate that
expression, and one for the value of that expression once evaluated.
`substitute` will recognize a promise variable and substitute the value
of its expression slot. If `substitute` is invoked inside a function,
the local variables of the function are also subject to substitution.

The argument to `substitute` does not have to be a simple identifier, it
can be an expression involving several variables and substitution will
occur for each of these. Also, `substitute` has an additional argument
which can be an environment or a list in which the variables are looked
up. For example:

```r
> substitute(a + b, list(a = 1, b = quote(x)))
1 + x
```

Notice that quoting was necessary to substitute the `x`. This kind of
construction comes in handy in connection with the facilities for
putting math expression in graphs, as the following case shows

```r
> plot(0)
> for (i in 1:4)
+   text(1, 0.2 * i,
+        substitute(x[ix] == y, list(ix = i, y = pnorm(i))))
```

It is important to realize that the substitutions are purely lexical;
there is no checking that the resulting call objects make sense if they
are evaluated. `substitute(x <- x + 1, list(x = 2))` will happily return
`2 <- 2 + 1`. However, some parts of R make up their own rules for what
makes sense and what does not and might actually have a use for such
ill-formed expressions. For example, using the "math in graphs" feature
often involves constructions that are syntactically correct, but which
would be meaningless to evaluate, like '`{}>=40*" years"`'.

Substitute will not evaluate its first argument. This leads to the
puzzle of how to do substitutions on an object that is contained in a
variable. The solution is to use `substitute` once more, like this

```r
> expr <- quote(x + y)
> substitute(substitute(e, list(x = 3)), list(e = expr))
substitute(x + y, list(x = 3))
> eval(substitute(substitute(e, list(x = 3)), list(e = expr)))
3 + y
```

The exact rules for substitutions are as follows: Each
parse tree for
the first is matched against the second argument, which can be a tagged
list or an environment frame. If it is a simple local object, its value
is inserted, _except_ if matching against the global environment. If it
is a promise (usually a function argument), the promise expression is
substituted. If the symbol is not matched, it is left untouched. The
special exception for substituting at the top level is admittedly
peculiar. It has been inherited from S and the rationale is most likely
that there is no control over which variables might be bound at that
level so that it would be better to just make substitute act as `quote`.

The rule of promise substitution is slightly different from that of S if
the local variable is modified before `substitute` is used. R will then
use the new value of the variable, whereas S will unconditionally use
the argument expression---unless it was a constant, which has the
curious consequence that `f((1))` may be very different from `f(1)` in
S. The R rule is considerably cleaner, although it does have
consequences in connection with lazy
evaluation that comes as a surprise to some. Consider

```r
logplot <- function(y, ylab = deparse(substitute(y))) {
    y <- log(y)
    plot(y, ylab = ylab)
}
```

This looks straightforward, but one will discover that the y label
becomes an ugly `c(...)` expression. It happens because the rules of
lazy evaluation cause the evaluation of the `ylab` expression to happen
_after_ `y` has been modified. The solution is to force `ylab` to be
evaluated first, i.e.,

```r
logplot <- function(y, ylab = deparse(substitute(y))) {
    ylab
    y <- log(y)
    plot(y, ylab = ylab)
}
```

Notice that one should not use `eval(ylab)` in this situation. If `ylab`
is a language or expression object, then that would cause the object to
be evaluated as well, which would not at all be desirable if a math
expression like `quote(log[e](y))` was being passed.

A variant on `substitute` is `bquote`, which is used to replace some
subexpressions with their values. The example from above

```r
> plot(0)
> for (i in 1:4)
+   text(1, 0.2 * i,
+        substitute(x[ix] == y, list(ix = i, y = pnorm(i))))
```

could be written more compactly as

```r
plot(0)
for(i in 1:4)
   text(1, 0.2*i, bquote( x[.(i)] == .(pnorm(i)) ))
```

The expression is quoted except for the contents of `.()`
subexpressions, which are replaced with their values. There is an
optional argument to compute the values in a different environment. The
syntax for `bquote` is borrowed from the LISP backquote macro.

---

### 6.3 More on evaluation

The `eval` function was introduced earlier in this chapter as a means of
evaluating call objects. However, this is not the full story. It is also
possible to specify the environment in which
the evaluation is to take place. By default this is the evaluation frame
from which `eval` is called, but quite frequently it needs to be set to
something else.

Very often, the relevant evaluation frame is that of the parent of the
current frame (cf. ???). In particular, when the object to evaluate is
the result of a `substitute` operation of the function arguments, it
will contain variables that make sense to the caller only (notice that
there is no reason to expect that the variables of the caller are in the
lexical scope of the callee). Since evaluation in the
parent frame occurs frequently, an `eval.parent` function exists as a
shorthand for `eval(expr, sys.frame(sys.parent()))`.

Another case that occurs frequently is evaluation in a list or a data
frame. For instance, this happens in connection with the `model.frame`
function when a `data` argument is given. Generally, the terms of the
model formula need to be evaluated in `data`, but they may occasionally
also contain references to items in the caller of `model.frame`. This is
sometimes useful in connection with simulation studies. So for this
purpose one needs not only to evaluate an expression in a list, but also
to specify an enclosure into which the search continues if the variable
is not in the list. Hence, the call has the form

```r
eval(expr, data, sys.frame(sys.parent()))
```

Notice that evaluation in a given environment may actually change that
environment, most obviously in cases involving the
assignment operator, such as

```r
eval(quote(total <- 0), environment(robert$balance)) # rob Rob
```

This is also true when evaluating in lists, but the original list does
not change because one is really working on a copy.

---

### 6.4 Evaluation of expression objects

Objects of mode `"expression"` are defined in [Expression objects](#Expression-objects). They are very similar to lists of call
objects.

```r
> ex <- expression(2 + 2, 3 + 4)
> ex[[1]]
2 + 2
> ex[[2]]
3 + 4
> eval(ex)
[1] 7
```

Notice that evaluating an expression object evaluates each call in turn,
but the final value is that of the last call. In this respect it behaves
almost identically to the compound language object
`quote({2 + 2; 3 + 4})`. However, there is a subtle difference: Call
objects are indistinguishable from subexpressions in a parse tree. This
means that they are automatically evaluated in the same way a
subexpression would be. Expression objects can be recognized during
evaluation and in a sense retain their quotedness. The evaluator will
not evaluate an expression object recursively, only when it is passed
directly to `eval` function as above. The difference can be seen like
this:

```r
> eval(substitute(mode(x), list(x = quote(2 + 2))))
[1] "numeric"
> eval(substitute(mode(x), list(x = expression(2 + 2))))
[1] "expression"
```

The deparser represents an expression object by the call that creates
it. This is similar to the way it handles numerical vectors and several
other objects that do not have a specific external representation.
However, it does lead to the following bit of confusion:

```r
> e <- quote(expression(2 + 2))
> e
expression(2 + 2)
> mode(e)
[1] "call"
> ee <- expression(2 + 2)
> ee
expression(2 + 2)
> mode(ee)
[1] "expression"
```

I.e., `e` and `ee` look identical when printed, but one is a call that
generates an expression object and the other is the object itself.

---

### 6.5 Manipulation of function calls

It is possible for a function to find out how it
has been called by looking at the result of `sys.call` as in the
following example of a function that simply returns its own call:

```r
> f <- function(x, y, ...) sys.call()
> f(y = 1, 2, z = 3, 4)
f(y = 1, 2, z = 3, 4)
```

However, this is not really useful except for debugging because it
requires the function to keep track of argument matching in order to
interpret the call. For instance, it must be able to see that the 2nd
actual argument gets matched to the first formal one (`x` in the above
example).

More often one requires the call with all actual arguments bound to the
corresponding formals. To this end, the function `match.call` is used.
Here's a variant of the preceding example, a function that returns its
own call with arguments matched

```r
> f <- function(x, y, ...) match.call()
> f(y = 1, 2, z = 3, 4)
f(x = 2, y = 1, z = 3, 4)
```

Notice that the second argument now gets matched to `x` and appears in
the corresponding position in the result.

The primary use of this technique is to call another function with the
same arguments, possibly deleting some and adding others. A typical
application is seen at the start of the `lm` function:

```r
    mf <- cl <- match.call()
    mf$singular.ok <- mf$model <- mf$method <- NULL
    mf$x <- mf$y <- mf$qr <- mf$contrasts <- NULL
    mf$drop.unused.levels <- TRUE
    mf[[1]] <- as.name("model.frame")
    mf <- eval(mf, sys.frame(sys.parent()))
```

Notice that the resulting call is evaluated in
the parent frame, in which one can be certain that the involved
expressions make sense. The call can be treated as a list object where
the first element is the name of the function and the remaining elements
are the actual argument expressions, with the corresponding formal
argument names as tags. Thus, the technique to eliminate undesired
arguments is to assign `NULL`, as seen in lines 2 and 3, and to add an
argument one uses tagged list assignment (here
to pass `drop.unused.levels = TRUE`) as in line 4. To change the name of
the function called, assign to the first element of the list and make
sure that the value is a name, either using the `as.name("model.frame")`
construction here or `quote(model.frame)`.

The `match.call` function has an `expand.dots` argument which is a
switch which if set to `FALSE` lets all '`...`' arguments be
collected as a single argument with the tag '`...`'.

```r
> f <- function(x, y, ...) match.call(expand.dots = FALSE)
> f(y = 1, 2, z = 3, 4)
f(x = 2, y = 1, ... = list(z = 3, 4))
```

The '`...`' argument is a list (a pairlist to be precise), not
a call to `list` like it is in S:

```r
> e1 <- f(y = 1, 2, z = 3, 4)$...
> e1
$z
[1] 3

[[2]]
[1] 4
```

One reason for using this form of `match.call` is simply to get rid of
any '`...`' arguments in order not to be passing unspecified
arguments on to functions that may not know them. Here's an example
paraphrased from `plot.formula`:

```r
m <- match.call(expand.dots = FALSE)
m$... <- NULL
m[[1]] <- "model.frame"
```

A more elaborate application is in `update.default` where a set of
optional extra arguments can add to, replace, or cancel those of the
original call:

```r
extras <- match.call(expand.dots = FALSE)$...
if (length(extras) > 0) {
    existing <- !is.na(match(names(extras), names(call)))
    for (a in names(extras)[existing]) call[[a]] <- extras[[a]]
    if (any(!existing)) {
        call <- c(as.list(call), extras[!existing])
        call <- as.call(call)
    }
}
```

Notice that care is taken to modify existing arguments individually in
case `extras[[a]] == NULL`. Concatenation does not work on call objects
without the coercion as shown; this is arguably a bug.

Two further functions exist for the construction of function calls,
namely `call` and `do.call`.

The function `call` allows creation of a call object from the function
name and the list of arguments

```r
> x <- 10.5
> call("round", x)
round(10.5)
```

As seen, the value of `x` rather than the symbol is
inserted in the call, so it is distinctly different from `round(x)`. The
form is used rather rarely, but is occasionally useful where the name of
a function is available as a character variable.

The function `do.call` is related, but evaluates the call immediately
and takes the arguments from an object of mode `"list"` containing all
the arguments. A natural use of this is when one wants to apply a
function like `cbind` to all elements of a list or data frame.

```r
is.na.data.frame <- function (x) {
    y <- do.call("cbind", lapply(x, "is.na"))
    rownames(y) <- row.names(x)
    y
}
```

Other uses include variations over constructions like
`do.call("f", list(...))`. However, one should be aware that this
involves evaluation of the arguments before the actual function call,
which may defeat aspects of lazy evaluation and argument substitution in
the function itself. A similar remark applies to the `call` function.

---

### 6.6 Manipulation of functions

It is often useful to be able to manipulate the components of a
function or closure. R provides a set of
interface functions for this purpose.

`body`

: Returns the expression that is the body of the function.

`formals`

: Returns a list of the formal arguments to the function. This is a
`pairlist`.

`environment`

:

    Returns the environment associated with the function.

`body<-`

: This sets the body of the function to the supplied expression.

`formals<-`

: Sets the formal arguments of the function to the supplied list.

`environment<-`

: Sets the environment of the function to the specified environment.

It is also possible to alter the bindings of different variables in the
environment of the function, using code along the lines of
`evalq(x <- 5, environment(f))`.

It is also possible to convert a function to a
list using `as.list`. The result is the concatenation of the list of
formal arguments with the function body. Conversely such a list can be
converted to a function using `as.function`. This functionality is
mainly included for S compatibility. Notice that environment information
is lost when `as.list` is used, whereas `as.function` has an argument
that allows the environment to be set.

---
