# 3 Objects, their modes and attributes

---

---

• [The intrinsic attributes mode and length](#The-intrinsic-attributes-mode-and-length)     
 • [Changing the length of an object](#Changing-the-length-of-an-object)     
 • [Getting and setting attributes](#Getting-and-setting-attributes)     
 • [The class of an object](#The-class-of-an-object)

---

---

### 3.1 Intrinsic attributes: mode and length

The entities R operates on are technically known as _objects_. Examples
are vectors of numeric (real) or complex values, vectors of logical
values and vectors of character strings. These are known as "atomic"
structures since their components are all of the same type, or _mode_,
namely _numeric_[^10^](#FOOT10), _complex_, _logical_,
_character_ and _raw_.

Vectors must have their values _all of the same mode_. Thus any given
vector must be unambiguously either _logical_, _numeric_, _complex_,
_character_ or _raw_. (The only apparent exception to this rule is the
special "value" listed as `NA` for quantities not available, but in fact
there are several types of `NA`). Note that a vector can be empty and
still have a mode. For example the empty character string vector is
listed as `character(0)` and the empty numeric vector as `numeric(0)`.

R also operates on objects called _lists_, which are of mode _list_.
These are ordered sequences of objects which individually can be of any
mode. _lists_ are known as "recursive" rather than atomic structures
since their components can themselves be lists in their own right.

The other recursive structures are those of mode _function_ and
_expression_. Functions are the objects that form part of the R system
along with similar user written functions, which we discuss in some
detail later. Expressions as objects form an advanced part of R which
will not be discussed in this guide, except indirectly when we discuss
_formulae_ used with modeling in R.

By the _mode_ of an object we mean the basic type of its fundamental
constituents. This is a special case of a "property" of an object.
Another property of every object is its _length_. The functions
`mode(object)` and `length(object)` can be used to find out the mode and
length of any defined structure [^11^](#FOOT11).

Further properties of an object are usually provided by
`attributes(object)`, see [Getting and setting attributes](#Getting-and-setting-attributes). Because of this, _mode_
and _length_ are also called "intrinsic attributes" of an object.

For example, if `z` is a complex vector of length 100, then in an
expression `mode(z)` is the character string `"complex"` and `length(z)`
is `100`.

R caters for changes of mode almost anywhere it could be considered
sensible to do so, (and a few where it might not be). For example with

```r
> z <- 0:9
```

we could put

```r
> digits <- as.character(z)
```

after which `digits` is the character vector `c("0", "1", "2", …, "9")`.
A further _coercion_, or change of mode, reconstructs the numerical
vector again:

```r
> d <- as.integer(digits)
```

Now `d` and `z` are the same.[^12^](#FOOT12) There is a large
collection of functions of the form `as.something()` for either coercion
from one mode to another, or for investing an object with some other
attribute it may not already possess. The reader should consult the
different help files to become familiar with them.

---

### 3.2 Changing the length of an object

An "empty" object may still have a mode. For example

```r
> e <- numeric()
```

makes `e` an empty vector structure of mode numeric. Similarly
`character()` is a empty character vector, and so on. Once an object of
any size has been created, new components may be added to it simply by
giving it an index value outside its previous range. Thus

```r
> e[3] <- 17
```

now makes `e` a vector of length 3, (the first two components of which
are at this point both `NA`). This applies to any structure at all,
provided the mode of the additional component(s) agrees with the mode of
the object in the first place.

This automatic adjustment of lengths of an object is used often, for
example in the `scan()` function for input. (see [The scan() function](#The-scan_0028_0029-function).)

Conversely to truncate the size of an object requires only an assignment
to do so. Hence if `alpha` is an object of length 10, then

```r
> alpha <- alpha[2 * 1:5]
```

makes it an object of length 5 consisting of just the former components
with even index. (The old indices are not retained, of course.) We can
then retain just the first three values by

```r
> length(alpha) <- 3
```

and vectors can be extended (by missing values) in the same way.

---

### 3.3 Getting and setting attributes

The function `attributes(object)` returns a list
of all the non-intrinsic attributes currently defined for that object.
The function `attr(object, name)` can be used to
select a specific attribute. These functions are rarely used, except in
rather special circumstances when some new attribute is being created
for some particular purpose, for example to associate a creation date or
an operator with an R object. The concept, however, is very important.

Some care should be exercised when assigning or deleting attributes
since they are an integral part of the object system used in R.

When it is used on the left hand side of an assignment it can be used
either to associate a new attribute with `object` or to change an
existing one. For example

```r
> attr(z, "dim") <- c(10,10)
```

allows R to treat `z` as if it were a 10-by-10 matrix.

---

### 3.4 The class of an object

All objects in R have a _class_, reported by the function `class`. For
simple vectors this is just the mode, for example `"numeric"`,
`"logical"`, `"character"` or `"list"`, but `"matrix"`, `"array"`,
`"factor"` and `"data.frame"` are other possible values.

A special attribute known as the _class_ of the object is used to allow
for an object-oriented style[^13^](#FOOT13) of programming in
R. For example if an object has class `"data.frame"`, it will be printed
in a certain way, the `plot()` function will display it graphically in a
certain way, and other so-called generic functions such as `summary()`
will react to it as an argument in a way sensitive to its class.

To remove temporarily the effects of class, use the function
`unclass()`. For example if `winter` has the class
`"data.frame"` then

```r
> winter
```

will print it in data frame form, which is rather like a matrix, whereas

```r
> unclass(winter)
```

will print it as an ordinary list. Only in rather special situations do
you need to use this facility, but one is when you are learning to come
to terms with the idea of class and generic functions.

Generic functions and classes will be discussed further in [Object orientation](#Object-orientation), but only briefly.

---
