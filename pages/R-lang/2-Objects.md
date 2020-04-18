# 2 Objects

---

In every computer language variables provide a means
of accessing the data stored in memory. R does not provide direct access
to the computer's memory but rather provides a number of specialized
data structures we will refer to as objects. These
objects are referred to through symbols or variables. In R, however, the
symbols are themselves objects and can be manipulated in the same way as
any other object. This is different from many other languages and has
wide ranging effects.

In this chapter we provide preliminary descriptions of the various data
structures provided in R. More detailed discussions of many of them will
be found in the subsequent chapters. The R specific function `typeof`
returns the _type_ of an R object.
Note that in the C code underlying R, all objects are pointers to a
structure with typedef `SEXPREC`; the different R data types are
represented in C by `SEXPTYPE`, which determines how the information in
the various parts of the structure is used.

The following table describes the possible values returned by `typeof`
and what they are.

> ---
>
> `"NULL"` NULL
> `"symbol"` a variable name
> `"pairlist"` a pairlist object (mainly internal)
> `"closure"` a function
> `"environment"` an environment
> `"promise"` an object used to implement lazy evaluation
> `"language"` an R language construct
> `"special"` an internal function that does not evaluate its arguments
> `"builtin"` an internal function that evaluates its arguments
> `"char"` a 'scalar' string object (internal only) \*\*\* > `"logical"` a vector containing logical values
> `"integer"` a vector containing integer values
> `"double"` a vector containing real values
> `"complex"` a vector containing complex values
> `"character"` a vector containing character values
> `"..."` the special variable length argument \*\*\* > `"any"` a special type that matches all types: there are no objects of this type
> `"expression"` an expression object
> `"list"` a list
> `"bytecode"` byte code (internal only) \*\*\* > `"externalptr"` an external pointer object
> `"weakref"` a weak reference object
> `"raw"` a vector containing bytes
> `"S4"` an S4 object which is not a simple object
>
> ---

Users cannot easily get hold of objects of types marked with a '\*\*\*'.

Function `mode` gives information about the _mode_ of an object in the
sense of Becker, Chambers & Wilks (1988), and is more compatible with
other implementations of the S language.
Finally, the function `storage.mode` returns the _storage mode_ of its
argument in the sense of Becker et al. (1988). It is generally used when
calling functions written in another language, such as C or FORTRAN, to
ensure that R objects have the data type expected by the routine being
called. (In the S language, vectors with integer or real values are both
of mode `"numeric"`, so their storage modes need to be distinguished.)

```r
> x <- 1:3
> typeof(x)
[1] "integer"
> mode(x)
[1] "numeric"
> storage.mode(x)
[1] "integer"
```

R objects are often coerced to different
types during computations. There are also many
functions available to perform explicit coercion.
When programming in the R language the type of an object generally
doesn't affect the computations, however, when dealing with foreign
languages or the operating system it is often necessary to ensure that
an object is of the correct type.

---

• [Basic types](#Basic-types)     
 • [Attributes](#Attributes)     
 • [Special compound objects](#Special-compound-objects)

---

---

### 2.1 Basic types

---

• [Vector objects](#Vector-objects)     
 • [List objects](#List-objects)     
 • [Language objects](#Language-objects)     
 • [Expression objects](#Expression-objects)     
 • [Function objects](#Function-objects)     
 • [NULL object](#NULL-object)     
 • [Builtin objects and special forms](#Builtin-objects-and-special-forms)     
 • [Promise objects](#Promise-objects)     
 • [Dot-dot-dot](#Dot_002ddot_002ddot)     
 • [Environment objects](#Environment-objects)     
 • [Pairlist objects](#Pairlist-objects)     
 • [Any-type](#Any_002dtype)

---

---

#### 2.1.1 Vectors

Vectors can be thought of as contiguous cells containing data. Cells are
accessed through indexing operations such as `x[5]`.
More details are given in [Indexing](#Indexing).

R has six basic ('atomic') vector types: logical, integer, real,
complex, string (or character) and raw. The modes and storage modes for
the different vector types are listed in the following table.

> typeof mode storage.mode
>
> ---
>
> `logical` `logical` `logical` > `integer` `numeric` `integer` > `double` `numeric` `double` > `complex` `complex` `complex` > `character` `character` `character` > `raw` `raw` `raw`

Single numbers, such as `4.2`, and strings, such as `"four point two"`
are still vectors, of length 1; there are no more basic types. Vectors
with length zero are possible (and useful).

String vectors have mode and storage mode `"character"`. A single
element of a character vector is often referred to as a _character
string_.

---

#### 2.1.2 Lists

Lists ("generic vectors") are another kind of data storage. Lists have
elements, each of which can contain any type of R object, i.e. the
elements of a list do not have to be of the same type. List elements are
accessed through three different indexing operations.
These are explained in detail in [Indexing](#Indexing).

Lists are vectors, and the basic vector types are referred to as _atomic
vectors_ where it is necessary to exclude lists.

---

#### 2.1.3 Language objects

There are three types of objects that constitute the R language. They
are _calls_, _expressions_, and _names_.
Since R has objects of type
`"expression"` we will try to avoid the use of the word expression in
other contexts. In particular syntactically correct expressions will be
referred to as _statements_.

These objects have modes `"call"`, `"expression"`, and `"name"`,
respectively.

They can be created directly from expressions using the `quote`
mechanism and converted to and from lists by the `as.list` and `as.call`
functions.
parse tree
can be extracted using the standard indexing operations.

---

• [Symbol objects](#Symbol-objects)

---

---

#### 2.1.3.1 Symbol objects

Symbols refer to R
name of any R object is usually a symbol. Symbols can be created through
the functions `as.name` and `quote`.

Symbols have mode `"name"`, storage mode `"symbol"`, and type
`"symbol"`. They can be coerced to and from
character strings using `as.character` and `as.name`.

They naturally appear as atoms of parsed expressions, try e.g.
`as.list(quote(x + y))`.

---

#### 2.1.4 Expression objects

In R one can have objects of type `"expression"`. An _expression_
contains one or more statements. A statement is a syntactically correct
collection of
Expression objects are special language objects which contain parsed but
unevaluated R statements. The main difference is that an expression
object can contain several such expressions. Another more subtle
difference is that objects of type `"expression"` are only
evaluated when explicitly passed
to `eval`, whereas other language objects may get evaluated in some
unexpected cases.

An expression object behaves much like a
list and its components should be accessed in the same way as the
components of a list.

---

#### 2.1.5 Function objects

In R functions are objects and can be manipulated in much the same way
as any other object. Functions (or more precisely, function closures)
have three basic components: a formal argument list, a body and an
environment. The argument list is a
comma-separated list of arguments. An argument can
be a symbol, or a '`symbol = default`' construct, or the
special argument '`...`'. The second form of argument is used
to specify a default value for an argument. This value will be used if
the function is called without any value specified for that argument.
The '`...`' argument is special and can contain any number of
arguments. It is generally used if the number of arguments is unknown or
in cases where the arguments will be passed on to another function.

The body is a parsed R statement. It is usually a collection of
statements in braces but it can be a single statement, a symbol or even
a constant.

A function's environment
is the environment that was active at the time that the function was
created. Any symbols bound in that environment are _captured_ and
available to the function. This combination of the code of the function
and the bindings in its environment is called a 'function closure', a
term from functional programming theory. In this document we generally
use the term 'function', but use 'closure' to emphasize the importance
of the attached environment.

It is possible to extract and manipulate the three parts of a closure
object using `formals`, `body`, and `environment` constructs (all three
can also be used on the left hand side of
assignments).
The last of these can be used to remove
unwanted environment capture.

When a function is called, a new environment (called the _evaluation
environment_) is created, whose enclosure (see [Environment objects](#Environment-objects)) is the environment from the function
closure. This new environment is initially populated with the
unevaluated arguments to the function; as evaluation proceeds, local
variables are created within it.

There is also a facility for converting functions to and from list
structures using `as.list` and `as.function`.
These have been included to provide compatibility with S and their use
is discouraged.

---

#### 2.1.6 NULL

There is a special object called `NULL`. It is used whenever there is a
need to indicate or specify that an object is absent. It should not be
confused with a vector or list of zero length.

The `NULL` object has no type and no modifiable properties. There is
only one `NULL` object in R, to which all instances refer. To test for
`NULL` use `is.null`. You cannot set attributes on `NULL`.

---

#### 2.1.7 Builtin objects and special forms

These two kinds of object contain the builtin
functions of R, i.e.,
those that are displayed as `.Primitive` in code listings (as well as
those accessed via the `.Internal` function and hence not user-visible
as objects). The difference between the two lies in the argument
handling. Builtin functions have all their arguments evaluated and
passed to the internal function, in accordance with _call-by-value_,
whereas special functions pass the unevaluated arguments to the internal
function.

From the R language, these objects are just another kind of function.
The `is.primitive` function can distinguish them from interpreted
functions.

---

#### 2.1.8 Promise objects

Promise objects are part of R's lazy evaluation mechanism. They contain
three slots: a value, an expression, and an
environment. When a
function is called the arguments are matched and then each of the formal
arguments is bound to a promise. The expression that was given for that
formal argument and a pointer to the environment the function was called
from are stored in the promise.

Until that argument is accessed there is no _value_ associated with the
promise. When the argument is accessed, the stored expression is
evaluated in the stored
environment, and the result is returned. The result is also saved by the
promise. The `substitute` function will extract the content of the
expression slot. This allows the programmer to access either the value
or the expression associated with the promise.

Within the R language, promise objects are almost only seen implicitly:
actual function arguments are of this type. There is also a
`delayedAssign` function that will make a promise out of an expression.
There is generally no way in R code to check whether an object is a
promise or not, nor is there a way to use R code to determine the
environment of a promise.

---

#### 2.1.9 Dot-dot-dot

The '`...`' object type is stored as a type of pairlist. The
components of '`...`' can be accessed in the usual pairlist
manner from C code, but is not easily accessed as an object in
interpreted code. The object can be captured as a list, so for example
in `table` one sees

```r
    args <- list(...)
## ....
    for (a in args) {
## ....
```

If a function has '`...`' as a formal argument then any actual
arguments that do not match a formal argument are matched with
'`...`'.

---

#### 2.1.10 Environments

Environments can be thought of as consisting of two things. A _frame_,
consisting of a set of symbol-value pairs, and an _enclosure_, a pointer
to an enclosing environment. When R looks up the value for a symbol the
frame is examined and if a matching symbol is found its value will be
returned. If not, the enclosing environment is then accessed and the
process repeated. Environments form a tree structure in which the
enclosures play the role of parents. The tree of environments is rooted
in an empty environment, available through
`emptyenv()`, which has no parent. It is the direct parent of the
environment of the base package (available through
the `baseenv()` function). Formerly `baseenv()` had the special value
`NULL`, but as from version 2.4.0, the use of `NULL` as an environment
is defunct.

Environments are created implicitly by function calls, as described in
[Function objects](#Function-objects) and [Lexical environment](#Lexical-environment). In this case the environment
contains the variables local to the function (including the arguments),
and its enclosure is the environment of the currently called function.
Environments may also be created directly by `new.env`.
The frame content of an environment can be
accessed and manipulated by use of `ls`, `get` and `assign` as well as
`eval` and `evalq`.

The `parent.env` function may be used to access the enclosure of an
environment.

Unlike most other R objects, environments are not copied when passed to
functions or used in assignments. Thus, if you assign the same
environment to several symbols and change one, the others will change
too. In particular, assigning attributes to an environment can lead to
surprises.

---

#### 2.1.11 Pairlist objects

Pairlist objects are similar to Lisp's dotted-pair lists. They are used
extensively in the internals of R, but are rarely visible in interpreted
code, although they are returned by `formals`, and can be created by
(e.g.) the `pairlist` function. A zero-length pairlist is `NULL`, as
would be expected in Lisp but in contrast to a zero-length list.
Each such object has three slots, a CAR value, a CDR
value and a TAG value. The TAG value is a text string and CAR and CDR
usually represent, respectively, a list item (head) and the remainder
(tail) of the list with a NULL object as terminator (the CAR/CDR
terminology is traditional Lisp and originally referred to the address
and decrement registers on an early 60's IBM computer).

Pairlists are handled in the R language in exactly the same way as
generic vectors ("lists"). In particular, elements are accessed using
the same `[[]]` syntax. The use of pairlists is deprecated since generic
vectors are usually more efficient to use. When an internal pairlist is
accessed from R it is generally (including when subsetted) converted to
a generic vector.

In a very few cases pairlists are user-visible: one is `.Options`.

---

#### 2.1.12 The "Any" type

It is not really possible for an object to be of "Any" type, but it is
nevertheless a valid type value. It gets used in certain (rather rare)
circumstances, e.g. `as.vector(x, "any")`, indicating that type
coercion should not be done.

---

### 2.2 Attributes

All objects except `NULL` can have one or more attributes attached to
them. Attributes are stored as a pairlist where all elements are named,
but should be thought of as a set of name=value pairs. A listing of the
attributes can be obtained using `attributes` and set by `attributes<-`,
individual
components are accessed using `attr` and `attr<-`.

Some attributes have special accessor
functions (e.g. `levels<-` for factors) and these should be used when
available. In addition to hiding details of implementation they may
perform additional operations. R attempts to intercept calls to `attr<-`
and to `attributes<-` that involve the special attributes and enforces
the consistency checks.

Matrices and arrays are simply vectors with the attribute `dim` and
optionally `dimnames` attached to the vector.

Attributes are used to implement the class structure used in R. If an
object has a `class` attribute then that attribute will be examined
during evaluation. The class structure
in R is described in detail in [Object-oriented programming](#Object_002doriented-programming).

---

• [Names](#Names)     
 • [Dimensions](#Dimensions)     
 • [Dimnames](#Dimnames)     
 • [Classes](#Classes)     
 • [Time series attributes](#Time-series-attributes)     
 • [Copying of attributes](#Copying-of-attributes)

---

---

#### 2.2.1 Names

A `names` attribute, when present, labels the individual elements of a
vector or list. When an object is printed the `names` attribute, when
present, is used to label the elements. The `names` attribute can also
be used for indexing purposes, for example, `quantile(x)["25%"]`.

One may get and set the names using `names` and `names<-` constructions.
The latter
will perform the necessary consistency checks to ensure that the names
attribute has the proper type and length.

Pairlists and one-dimensional arrays are treated specially. For pairlist
objects, a virtual `names` attribute is used; the `names` attribute is
really constructed from the tags of the list components. For
one-dimensional arrays the `names` attribute really accesses
`dimnames[[1]]`.

---

#### 2.2.2 Dimensions

The `dim` attribute is used to implement arrays. The content of the
array is stored in a vector in column-major order and the `dim`
attribute is a vector of integers specifying the respective extents of
the array. R ensures that the length of the vector is the product of the
lengths of the dimensions. The length of one or more dimensions may be
zero.

A vector is not the same as a one-dimensional array since the latter has
a `dim` attribute of length one, whereas the former has no `dim`
attribute.

---

#### 2.2.3 Dimnames

Arrays may name each dimension separately using the `dimnames` attribute
which is a list of character vectors. The `dimnames` list may itself
have names which are then used for extent headings when printing arrays.

---

#### 2.2.4 Classes

R has an elaborate class system[^1^](#FOOT1), principally
controlled via the `class` attribute. This attribute is a character
vector containing the list of classes that an object inherits from. This
forms the basis of the "generic methods" functionality in R.

This attribute can be accessed and manipulated virtually without
restriction by users. There is no checking that an object actually
contains the components that class methods expect. Thus, altering the
`class` attribute should be done with caution, and when they are
available specific creation and coercion functions
should be preferred.

---

#### 2.2.5 Time series attributes

The `tsp` attribute is used to hold parameters of time series, start,
end, and frequency. This construction is mainly used to handle series
with periodic substructure such as monthly or quarterly data.

---

#### 2.2.6 Copying of attributes

Whether attributes should be copied when an object is altered is a
complex area, but there are some general rules (Becker, Chambers &
Wilks, 1988, pp. 144--6).

Scalar functions (those which operate element-by-element on a vector and
whose output is similar to the input) should preserve attributes (except
perhaps class).

Binary operations normally copy most attributes from the longer argument
(and if they are of the same length from both, preferring the values on
the first). Here 'most' means all except the `names`, `dim` and
`dimnames` which are set appropriately by the code for the operator.

Subsetting (other than by an empty index) generally drops all attributes
except `names`, `dim` and `dimnames` which are reset as appropriate. On
the other hand, subassignment generally preserves attributes even if the
length is changed. Coercion drops all attributes.

The default method for sorting drops all attributes except names, which
are sorted along with the object.

---

### 2.3 Special compound objects

---

• [Factors](#Factors)     
 • [Data frame objects](#Data-frame-objects)

---

---

#### 2.3.1 Factors

Factors are used to describe items that can have a finite number of
values (gender, social class, etc.). A factor has a `levels` attribute
and class `"factor"`. Optionally, it may also contain a `contrasts`
attribute which controls the parametrisation used when the factor is
used in a
modeling functions.

A factor may be purely nominal or may have ordered categories. In the
latter case, it should be defined as such and have a `class` vector
`c("ordered"," factor")`.

Factors are currently implemented using an integer array to specify the
actual levels and a second array of names that are mapped to the
integers. Rather unfortunately users often make use of the
implementation in order to make some calculations easier. This, however,
is an implementation issue and is not guaranteed to hold in all
implementations of R.

---

#### 2.3.2 Data frame objects

Data frames are the R structures which most closely mimic the SAS or
SPSS data set, i.e. a "cases by variables" matrix of data.

A data frame is a list of vectors, factors, and/or matrices all having
the same length (number of rows in the case of matrices). In addition, a
data frame generally has a `names` attribute labeling the variables and
a `row.names` attribute for labeling the cases.

A data frame can contain a list that is the same length as the other
components. The list can contain elements of differing lengths thereby
providing a data structure for ragged arrays. However, as of this
writing such arrays are not generally handled correctly.

---
