# 3 Evaluation of expressions

---

When a user types a command at the prompt (or when an expression is read
from a file) the first thing that happens to it is that the command is
transformed by the parser into an internal
representation. The evaluator executes parsed R expressions and returns
the value of the expression. All expressions have a value. This is the
core of the language.

This chapter describes the basic mechanisms of the evaluator, but avoids
discussion of specific functions or groups of functions which are
described in separate chapters later on or where the help pages should
be sufficient documentation.

Users can construct expressions and invoke the evaluator on them.

---

• [Simple evaluation](#Simple-evaluation)     
 • [Control structures](#Control-structures)     
 • [Elementary arithmetic operations](#Elementary-arithmetic-operations)     
 • [Indexing](#Indexing)     
 • [Scope of variables](#Scope-of-variables)

---

---

### 3.1 Simple evaluation

---

• [Constants](#Constants)     
 • [Symbol lookup](#Symbol-lookup)     
 • [Function calls](#Function-calls)     
 • [Operators](#Operators)

---

---

#### 3.1.1 Constants

Any number typed directly at the prompt is a constant and is evaluated.

```r
> 1
[1] 1
```

Perhaps unexpectedly, the number returned from the expression `1` is a
numeric. In most cases, the difference between an integer and a numeric
value will be unimportant as R will do the right thing when using the
numbers. There are, however, times when we would like to explicitly
create an integer value for a constant. We can do this by calling the
function `as.integer` or using various other techniques. But perhaps the
simplest approach is to qualify our constant with the suffix character
'L'. For example, to create the integer value 1, we might use

```r
> 1L
[1]
```

We can use the 'L' suffix to qualify any number with the intent of
making it an explicit integer. So '0x10L' creates the integer value 16
from the hexadecimal representation. The constant `1e3L` gives 1000 as
an integer rather than a numeric value and is equivalent to `1000L`.
(Note that the 'L' is treated as qualifying the term `1e3` and not the
`3`.) If we qualify a value with 'L' that is not an integer value, e.g.
`1e-3L`, we get a warning and the numeric value is created. A warning is
also created if there is an unnecessary decimal point in the number,
e.g. `1.L`.

We get a syntax error when using 'L' with complex numbers, e.g. `12iL`
gives an error.

Constants are fairly boring and to do more we need symbols.

---

#### 3.1.2 Symbol lookup

When a new variable is created it must have a name so
it can be referenced and it usually has a value. The name itself is a
symbol. When a symbol is
value
is returned. Later we shall explain in detail how to determine the value
associated with a symbol.

In this small example `y` is a symbol and its value is 4. A symbol is an
R object too, but one rarely needs to deal with symbols directly, except
when doing "programming on the language" ([Computing on the language](#Computing-on-the-language)).

```r
> y <- 4
> y
[1] 4
```

---

#### 3.1.3 Function calls

Most of the computations carried out in R involve the evaluation of
functions. We will also refer to this as
function _invocation_. Functions are invoked by name with a list of
arguments separated by commas.

```r
> mean(1:10)
[1] 5.5
```

In this example the function `mean` was called with one argument, the
vector of integers from 1 to 10.

R contains a huge number of functions with different purposes. Most are
used for producing a result which is an R object, but others are used
for their side effects, e.g., printing and plotting functions.

Function calls can have _tagged_ (or _named_) arguments, as in
`plot(x, y, pch = 3)`. Arguments without tags are known as _positional_
since the function must distinguish their meaning from their sequential
positions among the arguments of the call, e.g., that `x` denotes the
abscissa variable and `y` the ordinate. The use of tags/names is an
obvious convenience for functions with a large number of optional
arguments.

A special type of function calls can appear on the left hand side of the
assignment operator as in

```r
> class(x) <- "foo"
```

What this construction really does is to call the function `class<-`
with the original object and the right hand side. This function performs
the modification of the object and returns the result which is then
stored back into the original variable. (At least conceptually, this is
what happens. Some additional effort is made to avoid unnecessary data
duplication.)

---

#### 3.1.4 Operators

R allows the use of arithmetic expressions using operators similar to
those of the C programming language, for instance

```r
> 1 + 2
[1] 3
```

Expressions can be grouped using parentheses, mixed with function calls,
and assigned to variables in a straightforward manner

```r
> y <- 2 * (a + log(x))
```

R contains a number of operators. They are listed in the table below.

> ---
>
> `-` Minus, can be unary or binary
> `+` Plus, can be unary or binary
> `!` Unary not
> `~` Tilde, used for model formulae, can be either unary or binary
> `?` Help
> `:` Sequence, binary (in model formulae: interaction)
> `*` Multiplication, binary
> `/` Division, binary
> `^` Exponentiation, binary
> `%x%` Special binary operators, `x` can be replaced by any valid name
> `%%` Modulus, binary
> `%/%` Integer divide, binary
> `%*%` Matrix product, binary
> `%o%` Outer product, binary
> `%x%` Kronecker product, binary
> `%in%` Matching operator, binary (in model formulae: nesting)
> `<` Less than, binary
> `>` Greater than, binary
> `==` Equal to, binary
> `>=` Greater than or equal to, binary
> `<=` Less than or equal to, binary
> `&` And, binary, vectorized
> `&&` And, binary, not vectorized
> `|` Or, binary, vectorized
> `||` Or, binary, not vectorized
> `<-` Left assignment, binary
> `->` Right assignment, binary
> `$` List subset, binary
>
> ---

Except for the syntax, there is no difference between applying an
operator and calling a function. In fact, `x + y` can equivalently be
written `` `+`(x, y) ``. Notice that since '`+`' is a
non-standard function name, it needs to be quoted.

R deals with entire vectors of data at a time, and most of the
elementary operators and basic mathematical functions like `log` are
vectorized (as indicated in the table above). This means that e.g.
adding two vectors of the same length will create a vector containing
the element-wise sums, implicitly looping over the vector index. This
applies also to other operators like `-`, `*`, and `/` as well as to
higher dimensional structures. Notice in particular that multiplying two
matrices does not produce the usual matrix product (the `%*%` operator
exists for that purpose). Some finer points relating to vectorized
operations will be discussed in [Elementary arithmetic operations](#Elementary-arithmetic-operations).

To access individual elements of an atomic vector, one generally uses
the `x[i]` construction.

```r
> x <- rnorm(5)
> x
[1] -0.12526937 -0.27961154 -1.03718717 -0.08156527  1.37167090
> x[2]
[1] -0.2796115
```

List components are more commonly accessed using `x$a` or `x[[i]]`.

```r
> x <- options()
> x$prompt
[1] "> "
```

Indexing constructs can also appear on the right hand side of an
assignment.

Like the other operators, indexing is really done by functions, and one
could have used `` `[`(x, 2) `` instead of `x[2]`.

R's indexing operations contain many advanced features which are further
described in [Indexing](#Indexing).

---

### 3.2 Control structures

Computation in R consists of sequentially evaluating _statements_.
Statements, such as `x<-1:10` or `mean(y)`, can be separated by either a
semi-colon or a new line. Whenever the
evaluator is presented with a
syntactically complete statement that statement is evaluated and the
_value_ returned. The result of evaluating a statement can be referred
to as the value of the statement[^2^](#FOOT2) The value can
always be assigned to a symbol.

Both semicolons and new lines can be used to separate statements. A
semicolon always indicates the end of a statement while a new line _may_
indicate the end of a statement. If the current statement is not
syntactically complete new lines are simply ignored by the evaluator. If
the session is interactive the prompt changes from '`>`' to
'`+`'.

```r
> x <- 0; x + 5
[1] 5
> y <- 1:10
> 1; 2
[1] 1
[1] 2
```

Statements can be grouped together using braces '`{`' and
'`}`'. A group of statements is sometimes called a _block_.
Single statements are evaluated when a new line is typed at the end of
the syntactically complete statement. Blocks are not evaluated until a
new line is entered after the closing brace. In the remainder of this
section, _statement_ refers to either a single statement or a block.

```r
> { x <- 0
+ x + 5
+ }
[1] 5
```

---

• [if](#if)     
 • [Looping](#Looping)     
 • [repeat](#repeat)     
 • [while](#while)     
 • [for](#for)     
 • [switch](#switch)

---

---

#### 3.2.1 if

The `if`/`else` statement conditionally evaluates two statements. There
is a _condition_ which is evaluated and if the _value_ is `TRUE` then
the first statement is evaluated; otherwise the second statement will be
evaluated. The `if`/`else` statement returns, as its value, the value of
the statement that was selected. The formal syntax is

```r
if ( statement1 )
    statement2
else
    statement3
```

First, `statement1` is evaluated to yield
`value1`. If `value1` is a logical vector with
first element `TRUE` then `statement2` is evaluated. If the
first element of `value1` is `FALSE` then
`statement3` is evaluated. If `value1` is a
numeric vector then `statement3` is evaluated when the first
element of `value1` is zero and otherwise
`statement2` is evaluated. Only the first element of
`value1` is used. All other elements are ignored. If
`value1` has any type other than a logical or a numeric
vector an error is signalled.

`if`/`else` statements can be used to avoid numeric problems such as
taking the logarithm of a negative number. Because `if`/`else`
statements are the same as other statements you can assign the value of
them. The two examples below are equivalent.

```r
> if( any(x <= 0) ) y <- log(1+x) else y <- log(x)
> y <- if( any(x <= 0) ) log(1+x) else log(x)
```

The `else` clause is optional. The statement
`if(any(x <= 0)) x <- x[x <= 0]` is valid. When the `if` statement is
not in a block the `else`, if present, must appear on the same line as
the end of `statement2`. Otherwise the new line at the end of
`statement2` completes the `if` and yields a syntactically
complete statement that is evaluated. A simple solution is to use a
compound statement wrapped in braces, putting the `else` on the same
line as the closing brace that marks the end of the statement.

`if`/`else` statements can be nested.

```r
if ( statement1 ) {
    statement2
} else if ( statement3 ) {
    statement4
} else if ( statement5 ) {
    statement6
} else
    statement8
```

One of the even numbered statements will be evaluated and the resulting
value returned. If the optional `else` clause is omitted and all the odd
numbered `statement`s evaluate to `FALSE` no statement will
be evaluated and `NULL` is returned.

The odd numbered `statement`s are evaluated, in order, until
one evaluates to `TRUE` and then the associated even numbered
`statement` is evaluated. In this example,
`statement6` will only be evaluated if
`statement1` is `FALSE` and `statement3` is
`FALSE` and `statement5` is `TRUE`. There is no limit to the
number of `else if` clauses that are permitted.

---

#### 3.2.2 Looping

R has three statements that provide explicit
looping.[^3^](#FOOT3) They are `for`, `while` and `repeat`. The
two built-in constructs, `next` and `break`, provide additional control
over the evaluation. R provides other functions for implicit looping
such as `tapply`, `apply`, and `lapply`. In addition many operations,
especially arithmetic ones, are vectorized so you may not need to use a
loop.

There are two statements that can be used to explicitly control looping.
They are `break` and `next`. The
`break` statement causes an exit from the innermost loop that is
currently being executed. The `next` statement immediately causes
control to return to the start of the loop. The next iteration of the
loop (if there is one) is then executed. No statement below `next` in
the current loop is evaluated.

The value returned by a loop statement is always `NULL` and is returned
invisibly.

---

#### 3.2.3 repeat

The `repeat` statement causes repeated evaluation of the body until a
break is specifically requested. This means that you need to be careful
when using `repeat` because of the danger of an infinite loop. The
syntax of the `repeat` loop is

```r
repeat statement
```

When using `repeat`, `statement` must be a block statement.
You need to both perform some computation and test whether or not to
break from the loop and usually this requires two statements.

---

#### 3.2.4 while

The `while` statement is very similar to the `repeat` statement. The
syntax of the `while` loop is

```r
while ( statement1 ) statement2
```

where `statement1` is evaluated and if its value is `TRUE`
then `statement2` is evaluated. This process continues until
`statement1` evaluates to `FALSE`.

---

#### 3.2.5 for

The syntax of the `for` loop is

```r
for ( name in vector )
   statement1
```

where `vector` can be either a vector or a list. For each
element in `vector` the variable `name` is set to
the value of that element and `statement1` is evaluated. A
side effect is that the variable `name` still exists after
the loop has concluded and it has the value of the last element of
`vector` that the loop was evaluated for.

---

#### 3.2.6 switch

Technically speaking, `switch` is just another function, but its
semantics are close to those of control structures of other programming
languages.

The syntax is

```r
switch (statement, list)
```

where the elements of `list` may be named. First,
`statement` is evaluated and the result, `value`,
obtained. If `value` is a number between 1 and the length of
`list` then the corresponding element of `list` is
evaluated and the result returned. If `value` is too large or
too small `NULL` is returned.

```r
> x <- 3
> switch(x, 2+2, mean(1:10), rnorm(5))
[1]  2.2903605  2.3271663 -0.7060073  1.3622045 -0.2892720
> switch(2, 2+2, mean(1:10), rnorm(5))
[1] 5.5
> switch(6, 2+2, mean(1:10), rnorm(5))
NULL
```

If `value` is a character vector then the element of
'`...`' with a name that exactly matches `value` is
evaluated. If there is no match a single unnamed argument will be used
as a default. If no default is specified, `NULL` is returned.

```r
> y <- "fruit"
> switch(y, fruit = "banana", vegetable = "broccoli", "Neither")
[1] "banana"
> y <- "meat"
> switch(y, fruit = "banana", vegetable = "broccoli", "Neither")
[1] "Neither"
```

A common use of `switch` is to branch according to the character value
of one of the arguments to a function.

```r
> centre <- function(x, type) {
+ switch(type,
+        mean = mean(x),
+        median = median(x),
+        trimmed = mean(x, trim = .1))
+ }
> x <- rcauchy(10)
> centre(x, "mean")
[1] 0.8760325
> centre(x, "median")
[1] 0.5360891
> centre(x, "trimmed")
[1] 0.6086504
```

`switch` returns either the value of the statement that was evaluated or
`NULL` if no statement was evaluated.

To choose from a list of alternatives that already exists `switch` may
not be the best way to select one for evaluation. It is often better to
use `eval` and the subset operator, `[[`, directly via
`eval(x[[condition]])`.

---

### 3.3 Elementary arithmetic operations

---

• [Recycling rules](#Recycling-rules)     
 • [Propagation of names](#Propagation-of-names)     
 • [Dimensional attributes](#Dimensional-attributes)     
 • [NA handling](#NA-handling)

---

In this section, we discuss the finer points of the rules that apply to
basic operation like addition or multiplication of two vectors or
matrices.

---

#### 3.3.1 Recycling rules

If one tries to add two structures with a different number of elements,
then the shortest is recycled to length of longest. That is, if for
instance you add `c(1, 2, 3)` to a six-element vector then you will
really add `c(1, 2, 3, 1, 2, 3)`. If the length of the longer vector is
not a multiple of the shorter one, a warning is given.

As from R 1.4.0, any arithmetic operation involving a zero-length vector
has a zero-length result.

---

#### 3.3.2 Propagation of names

propagation of names (first one wins, I think - also if it has no
names?? ---- first one \*with names\* wins, recycling causes shortest to
lose names)

---

#### 3.3.3 Dimensional attributes

(matrix+matrix, dimensions must match. vector+matrix: first recycle,
then check if dims fit, error if not)

---

#### 3.3.4 NA handling

Missing values in the statistical sense, that is, variables whose value
is not known, have the value `NA`. This should not be confused with the
`missing` property for a function argument that has not been supplied
(see [Arguments](#Arguments)).

As the elements of an atomic vector must be of the same type there are
multiple types of `NA` values. There is one case where this is
particularly important to the user. The default type of `NA` is
`logical`, unless coerced to some other type, so the appearance of a
missing value may trigger logical rather than numeric indexing (see
[Indexing](#Indexing) for details).

Numeric and logical calculations with `NA` generally return `NA`. In
cases where the result of the operation would be the same for all
possible values the `NA` could take, the operation may return this
value. In particular, '`FALSE & NA`' is `FALSE`,
'`TRUE | NA`' is `TRUE`. `NA` is not equal to any other value
or to itself; testing for `NA` is done using `is.na`.
However, an `NA` value will match another `NA`
value in `match`.

Numeric calculations whose result is undefined, such as
'`0/0`', produce the value `NaN`. This exists only in the
`double` type and for real or imaginary components of the complex type.
The function `is.nan` is provided to check specifically for
`NaN`, `is.na` also returns `TRUE` for `NaN`.
Coercing `NaN` to logical or integer type gives an
`NA` of the appropriate type, but coercion to character gives the string
`"NaN"`. `NaN` values are incomparable so tests of equality or collation
involving `NaN` will result in `NA`. They are regarded as matching any
`NaN` value (and no other value, not even `NA`) by `match`.

The `NA` of character type is as from R 1.5.0 distinct from the string
`"NA"`. Programmers who need to specify an explicit string `NA` should
use '`as.character(NA)`' rather than `"NA"`, or set elements to
`NA` using `is.na<-`.

There are constants `NA_integer_`, `NA_real_`, `NA_complex_` and
`NA_character_` which will generate (in the parser) an `NA` value of the
appropriate type, and will be used in deparsing when it is not otherwise
possible to identify the type of an `NA` (and the `control` options ask
for this to be done).

There is no `NA` value for raw vectors.

---

### 3.4 Indexing

R contains several constructs which allow access to individual elements
or subsets through indexing operations. In the case of the basic vector
types one can access the i-th element using `x[i]`, but there is also
indexing of lists, matrices, and multi-dimensional arrays. There are
several forms of indexing in addition to indexing with a single integer.
Indexing can be used both to extract part of an object and to replace
parts of an object (or to add parts).

R has three basic indexing operators, with syntax displayed by the
following examples

```r
x[i]
x[i, j]
x[[i]]
x[[i, j]]
x$a
x$"a"
```

For vectors and matrices the `[[` forms are rarely used, although they
have some slight semantic differences from the `[` form (e.g. it drops
any `names` or `dimnames` attribute, and that partial matching is used
for character indices). When indexing multi-dimensional structures with
a single index, `x[[i]]` or `x[i]` will return the `i`th sequential
element of `x`.

For lists, one generally uses `[[` to select any single element, whereas
`[` returns a list of the selected elements.

The `[[` form allows only a single element to be selected using integer
or character indices, whereas `[` allows indexing by vectors. Note
though that for a list or other recursive object, the index can be a
vector and each element of the vector is applied in turn to the list,
the selected component, the selected component of that component, and so
on. The result is still a single element.

The form using `$` applies to recursive objects such as lists and
pairlists. It allows only a literal character string or a symbol as the
index. That is, the index is not computable: for cases where you need to
evaluate an expression to find the index, use `x[[expr]]`. Applying `$`
to a non-recursive object is an error.

---

• [Indexing by vectors](#Indexing-by-vectors)     
 • [Indexing matrices and arrays](#Indexing-matrices-and-arrays)     
 • [Indexing other structures](#Indexing-other-structures)     
 • [Subset assignment](#Subset-assignment)

---

---

#### 3.4.1 Indexing by vectors

R allows some powerful constructions using vectors as indices. We shall
discuss indexing of simple vectors first. For simplicity, assume that
the expression is `x[i]`. Then the following possibilities exist
according to the type of `i`.

- **Integer**. All elements of `i` must have the
  same sign. If they are positive, the elements of `x` with those
  index numbers are selected. If `i` contains negative elements, all
  elements except those indicated are selected.

If `i` is positive and exceeds `length(x)` then the corresponding
selection is `NA`. Negative out of bounds values for `i` are
silently disregarded since R version 2.6.0, S compatibly, as they
mean to drop non-existing elements and that is an empty operation
("no-op").

A special case is the zero index, which has null effects: `x[0]` is
an empty vector and otherwise including zeros among positive or
negative indices has the same effect as if they were omitted.

- **Other numeric**. Non-integer values are converted to integer (by
  truncation towards zero) before use.

- **Logical**. The indexing `i` should generally have the same length
  as `x`. If it is shorter, then its elements will be recycled as
  discussed in [Elementary arithmetic
  operations](#Elementary-arithmetic-operations). If it is longer,
  then `x` is conceptually extended with `NA`s. The selected values of
  `x` are those for which `i` is `TRUE`.

- **Character**. The strings in `i` are
  matched against the names attribute of `x` and the resulting
  integers are used. For `[[` and `$` partial matching is used if
  exact matching fails, so `x$aa` will match `x$aabb` if `x` does not
  contain a component named `"aa"` and `"aabb"` is the only name which
  has prefix `"aa"`. For `[[`, partial matching can be controlled via
  the `exact` argument which defaults to `NA` indicating that partial
  matching is allowed, but should result in a warning when it occurs.
  Setting `exact` to `TRUE` prevents partial matching from occurring,
  a `FALSE` value allows it and does not issue any warnings. Note that
  `[` always requires an exact match. The string `""` is treated
  specially: it indicates 'no name' and matches no element (not even
  those without a name). Note that partial matching is only used when
  extracting and not when replacing.

- **Factor**. The result is identical to `x[as.integer(i)]`. The
  factor levels are never used. If so desired, use
  `x[as.character(i)]` or a similar construction.

- **Empty**. The expression `x[]` returns `x`, but drops "irrelevant"
  attributes from the result. Only `names` and in multi-dimensional
  arrays `dim` and `dimnames` attributes are retained.

- **NULL**. This is treated as if it were `integer(0)`.

Indexing with a missing (i.e. `NA`) value gives an `NA` result. This
rule applies also to the case of logical indexing, i.e. the elements of
`x` that have an `NA` selector in `i` get included in the result, but
their value will be `NA`.

Notice however, that there are different modes of `NA`---the literal
constant is of mode `"logical"`, but it is frequently automatically
coerced to other types. One effect of this is that `x[NA]` has the
length of `x`, but `x[c(1, NA)]` has length 2. That is because the rules
for logical indices apply in the former case, but those for integer
indices in the latter.

Indexing with `[` will also carry out the relevant subsetting of any
names attributes.

---

#### 3.4.2 Indexing matrices and arrays

Subsetting multi-dimensional structures generally follows the same rules
as single-dimensional indexing for each index variable, with the
relevant component of `dimnames` taking the place of `names`. A couple
of special rules apply, though:

Normally, a structure is accessed using the number of indices
corresponding to its dimension. It is however also possible to use a
single index in which case the `dim` and `dimnames` attributes are
disregarded and the result is effectively that of `c(m)[i]`. Notice that
`m[1]` is usually very different from `m[1, ]` or `m[, 1]`.

It is possible to use a matrix of integers as an index. In this case,
the number of columns of the matrix should match the number of
dimensions of the structure, and the result will be a vector with length
as the number of rows of the matrix. The following example shows how to
extract the elements `m[1, 1]` and `m[2, 2]` in one operation.

```r
> m <- matrix(1:4, 2)
> m
     [,1] [,2]
[1,]    1    3
[2,]    2    4
> i <- matrix(c(1, 1, 2, 2), 2, byrow = TRUE)
> i
     [,1] [,2]
[1,]    1    1
[2,]    2    2
> m[i]
[1] 1 4
```

Indexing matrices may not contain negative indices. `NA` and zero values
are allowed: rows in an index matrix containing a zero are ignored,
whereas rows containing an `NA` produce an `NA` in the result.

Both in the case of using a single index and in
matrix indexing, a `names` attribute is used if present, as had the
structure been one-dimensional.

If an indexing operation causes the result to have one of its extents of
length one, as in selecting a single slice of a three-dimensional matrix
with (say) `m[2, , ]`, the corresponding dimension is generally dropped
from the result. If a single-dimensional structure results, a vector is
obtained. This is occasionally undesirable and can be turned off by
adding the '`drop = FALSE`' to the indexing operation. Notice
that this is an additional argument to the `[` function and doesn't add
to the index count. Hence the correct way of selecting the first row of
a matrix as a _1_ by _n_ matrix is `m[1, , drop = FALSE]`. Forgetting to
disable the dropping feature is a common cause of failure in general
subroutines where an index occasionally, but not usually has length one.
This rule still applies to a one-dimensional array, where any subsetting
will give a vector result unless '`drop = FALSE`' is used.

Notice that vectors are distinct from one-dimensional arrays in that the
latter have `dim` and `dimnames` attributes (both of length one).
One-dimensional arrays are not easily obtained from subsetting
operations but they can be constructed explicitly and are returned by
`table`. This is sometimes useful because the elements of the `dimnames`
list may themselves be named, which is not the case for the `names`
attribute.

Some operations such as `m[FALSE, ]` result in structures in which a
dimension has zero extent. R generally tries to handle these structures
sensibly.

---

#### 3.4.3 Indexing other structures

The operator `[` is a generic function which allows class methods to be
added, and the `$` and `[[` operators likewise. Thus, it is possible to
have user-defined indexing operations for any structure. Such a
function, say `[.foo` is called with a set of arguments of which the
first is the structure being indexed and the rest are the indices. In
the case of `$`, the index argument is of mode `"symbol"` even when
using the `x$"abc"` form. It is important to be aware that class methods
do not necessarily behave in the same way as the basic methods, for
example with respect to partial matching.

The most important example of a class method for `[` is that used for
data frames. It is not described in detail here (see the help page for
`[.data.frame`), but in broad terms, if two indices are supplied (even
if one is empty) it creates matrix-like indexing for a structure that is
basically a list of vectors of the same length. If a single index is
supplied, it is interpreted as indexing the list of columns---in that
case the `drop` argument is ignored, with a warning.

The basic operators `$` and `[[` can be applied to environments. Only
character indices are allowed and no partial matching is done.

---

#### 3.4.4 Subset assignment

Assignment to subsets of a structure is a special case of a general
mechanism for complex assignment:

```r
x[3:5] <- 13:15
```

The result of this command is as if the following had been executed

```r
`*tmp*` <- x
x <- "[<-"(`*tmp*`, 3:5, value=13:15)
rm(`*tmp*`)
```

Note that the index is first converted to a numeric index and then the
elements are replaced sequentially along the numeric index, as if a
`for` loop had been used. Any existing variable called `` `*tmp*` ``
will be overwritten and deleted, and this variable name should not be
used in code.

The same mechanism can be applied to functions other than `[`. The
replacement function has the same name with `<-` pasted on. Its last
argument, which must be called `value`, is the new value to be assigned.
For example,

```r
names(x) <- c("a","b")
```

is equivalent to

```r
`*tmp*` <- x
x <- "names<-"(`*tmp*`, value=c("a","b"))
rm(`*tmp*`)
```

Nesting of complex assignments is evaluated recursively

```r
names(x)[3] <- "Three"
```

is equivalent to

```r
`*tmp*` <- x
x <- "names<-"(`*tmp*`, value="[<-"(names(`*tmp*`), 3, value="Three"))
rm(`*tmp*`)
```

Complex assignments in the enclosing environment (using `<<-`) are also
permitted:

```r
names(x)[3] <<- "Three"
```

is equivalent to

```r
`*tmp*` <<- get(x, envir=parent.env(), inherits=TRUE)
names(`*tmp*`)[3] <- "Three"
x <<- `*tmp*`
rm(`*tmp*`)
```

and also to

```r
`*tmp*` <- get(x,envir=parent.env(), inherits=TRUE)
x <<- "names<-"(`*tmp*`, value="[<-"(names(`*tmp*`), 3, value="Three"))
rm(`*tmp*`)
```

Only the target variable is evaluated in the enclosing environment, so

```r
e<-c(a=1,b=2)
i<-1
local({
   e <- c(A=10,B=11)
   i <-2
   e[i] <<- e[i]+1
})
```

uses the local value of `i` on both the LHS and RHS, and the local value
of `e` on the RHS of the superassignment statement. It sets `e` in the
outer environment to

```r
 a  b
 1 12
```

That is, the superassignment is equivalent to the four lines

```r
`*tmp*` <- get(e, envir=parent.env(), inherits=TRUE)
`*tmp*`[i] <- e[i]+1
e <<- `*tmp*`
rm(`*tmp*`)
```

Similarly

```r
x[is.na(x)] <<- 0
```

is equivalent to

```r
`*tmp*` <- get(x,envir=parent.env(), inherits=TRUE)
`*tmp*`[is.na(x)] <- 0
x <<- `*tmp*`
rm(`*tmp*`)
```

and not to

```r
`*tmp*` <- get(x,envir=parent.env(), inherits=TRUE)
`*tmp*`[is.na(`*tmp*`)] <- 0
x <<- `*tmp*`
rm(`*tmp*`)
```

These two candidate interpretations differ only if there is also a local
variable `x`. It is a good idea to avoid having a local variable with
the same name as the target variable of a superassignment. As this case
was handled incorrectly in versions 1.9.1 and earlier there must not be
a serious need for such code.

---

### 3.5 Scope of variables

Almost every programming language has a set of scoping rules, allowing
the same name to be used for different objects. This allows, e.g., a
local variable in a function to have the same name as a global object.

R uses a _lexical scoping_ model, similar to languages like Pascal.
However, R is a _functional programming language_ and allows dynamic
creation and manipulation of functions and language objects, and has
additional features reflecting this fact.

---

• [Global environment](#Global-environment)     
 • [Lexical environment](#Lexical-environment)     
 • [Stacks](#Stacks)     
 • [Search path](#Search-path)

---

---

#### 3.5.1 Global environment

The global environment is the root of the user
workspace. An assignment operation from the
command line will cause the relevant object to belong to the global
environment. Its enclosing environment is the next environment on the
search path, and so on back to the empty environment that is the
enclosure of the base environment.

---

#### 3.5.2 Lexical environment

Every call to a function creates a
_frame_ which contains the
local variables created in the function, and is evaluated in an
environment, which in combination creates a new environment.

Notice the terminology: A frame is a set of variables, an environment is
a nesting of frames (or equivalently: the innermost frame plus the
enclosing environment).

Environments may be assigned to variables or be contained in other
objects. However, notice that they are not standard objects---in
particular, they are not copied on assignment.

A closure (mode `"function"`) object will contain the environment in
which it is created as part of its definition (By default. The
environment can be manipulated using `environment<-`). When the function
is subsequently called, its
evaluation environment is created with the closure's environment as
enclosure. Notice that this is not necessarily the environment of the
caller!

Thus, when a variable is requested inside a
function, it is first sought in the
evaluation environment, then in
the enclosure, the enclosure of the enclosure, etc.; once the global
environment or the environment of a package is reached, the search
continues up the search path to the environment of the base package. If
the variable is not found there, the search will proceed next to the
empty environment, and will fail.

---

#### 3.5.3 The call stack

Every time a function is invoked a new evaluation
frame is created. At any point in time during the computation the
currently active environments are accessible through the _call stack_.
Each time a function is invoked a special construct called a context is
created internally and is placed on a list of contexts. When a function
has finished evaluating its context is removed from the call stack.

Making variables defined higher up the call stack available is called
dynamic scope. The binding for a variable is then
determined by the most recent (in time) definition of the variable. This
contradicts the default scoping rules in R, which use the bindings in
the environment in which the function was
defined (lexical scope). Some functions, particularly those that use and
manipulate model formulas, need to simulate dynamic scope by directly
accessing the call stack.

Access to the call stack is provided through a
family of functions which have names that start with '`sys.`'.
They are listed briefly below.

`sys.call`

: Get the call for the specified context.

`sys.frame`

: Get the evaluation frame for the specified context.

`sys.nframe`

: Get the environment frame for all active contexts.

`sys.function`

: Get the function being invoked in the specified context.

`sys.parent`

: Get the parent of the current function invocation.

`sys.calls`

: Get the calls for all the active contexts.

`sys.frames`

: Get the evaluation frames for all the active contexts.

`sys.parents`

: Get the numeric labels for all active contexts.

`sys.on.exit`

: Set a function to be executed when the specified context is exited.

`sys.status`

: Calls `sys.frames`, `sys.parents` and `sys.calls`.

`parent.frame`

: Get the evaluation frame for the specified parent context.

---

#### 3.5.4 Search path

In addition to the evaluation
environment structure, R has a search path of
environments which are searched for variables not found elsewhere. This
is used for two things: packages of functions and attached user data.

The first element of the search path is the global environment and the
last is the base package. An `Autoloads` environment is used for holding
proxy objects that may be loaded on demand. Other environments are
inserted in the path using `attach` or `library`.

Packages which have a _namespace_ have a different search path. When a
search for an R object is started from an object in such a package, the
package itself is searched first, then its imports, then the base
namespace and finally the global environment and the rest of the regular
search path. The effect is that references to other objects in the same
package will be resolved to the package, and objects cannot be masked by
objects of the same name in the global environment or in other packages.

---
