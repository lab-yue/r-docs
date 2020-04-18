7 Generic functions and methods

---

R programmers will often want to add methods for existing generic
functions, and may want to add new generic functions or make existing
functions generic. In this chapter we give guidelines for doing so, with
examples of the problems caused by not adhering to them.

This chapter only covers the 'informal' class system copied from S3, and
not with the S4 (formal) methods of package **methods**.

First, a _caveat_: a function named `gen.cl` will be invoked by the
generic `gen` for class `cl`, so do not name functions in this style
unless they are intended to be methods.

The key function for methods is `NextMethod`, which dispatches the next
method. It is quite typical for a method function to make a few changes
to its arguments, dispatch to the next method, receive the results and
modify them a little. An example is

```r
t.data.frame <- function(x)
{
    x <- as.matrix(x)
    NextMethod("t")
}
```

Note that the example above works because there is a _next_ method, the
default method, not that a new method is selected when the class is
changed.

_Any_ method a programmer writes may be invoked from another method by
`NextMethod`, _with the arguments appropriate to the previous method_.
Further, the programmer cannot predict which method `NextMethod` will
pick (it might be one not yet dreamt of), and the end user calling the
generic needs to be able to pass arguments to the next method. For this
to work

> _A method must have all the arguments of the generic, including `…` if
> the generic does._

It is a grave misunderstanding to think that a method needs only to
accept the arguments it needs. The original S version of `predict.lm`
did not have a `…` argument, although `predict` did. It soon became
clear that `predict.glm` needed an argument `dispersion` to handle
over-dispersion. As `predict.lm` had neither a `dispersion` nor a `…`
argument, `NextMethod` could no longer be used. (The legacy, two direct
calls to `predict.lm`, lives on in `predict.glm` in R, which is based on
the workaround for S3 written by Venables & Ripley.)

Further, the user is entitled to use positional matching when calling
the generic, and the arguments to a method called by `UseMethod` are
those of the call to the generic. Thus

> _A method must have arguments in exactly the same order as the
> generic._

To see the scale of this problem, consider the generic function `scale`,
defined as

```r
scale <- function (x, center = TRUE, scale = TRUE)
    UseMethod("scale")
```

Suppose an unthinking package writer created methods such as

```r
scale.foo <- function(x, scale = FALSE, ...) { }
```

Then for `x` of class `"foo"` the calls

```r
scale(x, , TRUE)
scale(x, scale = TRUE)
```

would do most likely do different things, to the justifiable
consternation of the end user.

To add a further twist, which default is used when a user calls
`scale(x)` in our example? What if

```r
scale.bar <- function(x, center, scale = TRUE) NextMethod("scale")
```

and `x` has class `c("bar", "foo")`? It is the default specified in the
method that is used, but the default specified in the generic may be the
one the user sees. This leads to the recommendation:

> _If the generic specifies defaults, all methods should use the same
> defaults._

An easy way to follow these recommendations is to always keep generics
simple, e.g.

```r
scale <- function(x, ...) UseMethod("scale")
```

Only add parameters and defaults to the generic if they make sense in
all possible methods implementing it.

---

• [Adding new generics](#Adding-new-generics)

---

---

### 7.1 Adding new generics

When creating a new generic function, bear in mind that its argument
list will be the maximal set of arguments for methods, including those
written elsewhere years later. So choosing a good set of arguments may
well be an important design issue, and there need to be good arguments
_not_ to include a `…` argument.

If a `…` argument is supplied, some thought should be given to its
position in the argument sequence. Arguments which follow `…` must be
named in calls to the function, and they must be named in full (partial
matching is suppressed after `…`). Formal arguments before `…` can be
partially matched, and so may 'swallow' actual arguments intended for
`…`. Although it is commonplace to make the `…` argument the last one,
that is not always the right choice.

Sometimes package writers want to make generic a function in the base
package, and request a change in R. This may be justifiable, but making
a function generic with the old definition as the default method does
have a small performance cost. It is never necessary, as a package can
take over a function in the base package and make it generic by
something like

```r
foo <- function(object, ...) UseMethod("foo")
foo.default <- function(object, ...) base::foo(object)
```

Earlier versions of this manual suggested assigning
`foo.default <- base::foo`. This is **not** a good idea, as it captures
the base function at the time of installation and it might be changed as
R is patched or updated.

The same idea can be applied for functions in other packages with
namespaces.

---
