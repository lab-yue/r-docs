5 Arrays and matrices

---

---

• [Arrays](#Arrays)     
 • [Array indexing](#Array-indexing)     
 • [Index matrices](#Index-matrices)     
 • [The array() function](#The-array_0028_0029-function)     
 • [The outer product of two arrays](#The-outer-product-of-two-arrays)     
 • [Generalized transpose of an array](#Generalized-transpose-of-an-array)     
 • [Matrix facilities](#Matrix-facilities)     
 • [Forming partitioned matrices](#Forming-partitioned-matrices)     
 • [The concatenation function c() with arrays](#The-concatenation-function-c_0028_0029-with-arrays)     
 • [Frequency tables from factors](#Frequency-tables-from-factors)

---

---

### 5.1 Arrays

An array can be considered as a multiply subscripted collection of data
entries, for example numeric. R allows simple facilities for creating
and handling arrays, and in particular the special case of matrices.

A dimension vector is a vector of non-negative integers. If its length
is _k_ then the array is _k_-dimensional, e.g. a matrix is a
_2_-dimensional array. The dimensions are indexed from one up to the
values given in the dimension vector.

A vector can be used by R as an array only if it has a dimension vector
as its _dim_ attribute. Suppose, for example, `z` is a vector of 1500
elements. The assignment

```r
> dim(z) <- c(3,5,100)
```

gives it the _dim_ attribute that allows it to be treated as a _3_ by
_5_ by _100_ array.

Other functions such as `matrix()` and `array()` are available for
simpler and more natural looking assignments, as we shall see in [The
array() function](#The-array_0028_0029-function).

The values in the data vector give the values in the array in the same
order as they would occur in FORTRAN, that is "column major order," with
the first subscript moving fastest and the last subscript slowest.

For example if the dimension vector for an array, say `a`, is `c(3,4,2)`
then there are 3 \* 4 \* 2 = 24 entries in `a` and the data vector holds
them in the order `a[1,1,1], a[2,1,1], …, a[2,4,2], a[3,4,2]`.

Arrays can be one-dimensional: such arrays are usually treated in the
same way as vectors (including when printing), but the exceptions can
cause confusion.

---

### 5.2 Array indexing. Subsections of an array

Individual elements of an array may be referenced by giving the name of
the array followed by the subscripts in square brackets, separated by
commas.

More generally, subsections of an array may be specified by giving a
sequence of _index vectors_ in place of subscripts; however _if any
index position is given an empty index vector, then the full range of
that subscript is taken_.

Continuing the previous example, `a[2,,]` is a 4 \* 2 array with
dimension vector `c(4,2)` and data vector containing the values

```r
c(a[2,1,1], a[2,2,1], a[2,3,1], a[2,4,1],
  a[2,1,2], a[2,2,2], a[2,3,2], a[2,4,2])
```

in that order. `a[,,]` stands for the entire array, which is the same as
omitting the subscripts entirely and using `a` alone.

For any array, say `Z`, the dimension vector may be referenced
explicitly as `dim(Z)` (on either side of an assignment).

Also, if an array name is given with just _one subscript or index
vector_, then the corresponding values of the data vector only are used;
in this case the dimension vector is ignored. This is not the case,
however, if the single index is not a vector but itself an array, as we

### 5.3 Index matrices

As well as an index vector in any subscript position, a matrix may be
used with a single _index matrix_ in order either to assign a vector of
quantities to an irregular collection of elements in the array, or to
extract an irregular collection as a vector.

A matrix example makes the process clear. In the case of a doubly
indexed array, an index matrix may be given consisting of two columns
and as many rows as desired. The entries in the index matrix are the row
and column indices for the doubly indexed array. Suppose for example we
have a _4_ by _5_ array `X` and we wish to do the following:

- Extract elements `X[1,3]`, `X[2,2]` and `X[3,1]` as a vector
  structure, and
- Replace these entries in the array `X` by zeroes.

In this case we need a _3_ by _2_ subscript array, as in the following
example.

```r
> x <- array(1:20, dim=c(4,5))   # Generate a 4 by 5 array.
> x
     [,1] [,2] [,3] [,4] [,5]
[1,]    1    5    9   13   17
[2,]    2    6   10   14   18
[3,]    3    7   11   15   19
[4,]    4    8   12   16   20
> i <- array(c(1:3,3:1), dim=c(3,2))
> i                             # i is a 3 by 2 index array.
     [,1] [,2]
[1,]    1    3
[2,]    2    2
[3,]    3    1
> x[i]                          # Extract those elements
[1] 9 6 3
> x[i] <- 0                     # Replace those elements by zeros.
> x
     [,1] [,2] [,3] [,4] [,5]
[1,]    1    5    0   13   17
[2,]    2    0   10   14   18
[3,]    0    7   11   15   19
[4,]    4    8   12   16   20
>
```

Negative indices are not allowed in index matrices. `NA` and zero values
are allowed: rows in the index matrix containing a zero are ignored, and
rows containing an `NA` produce an `NA` in the result.

As a less trivial example, suppose we wish to generate an (unreduced)
design matrix for a block design defined by factors `blocks` (`b`
levels) and `varieties` (`v` levels). Further suppose there are `n`
plots in the experiment. We could proceed as follows:

```r
> Xb <- matrix(0, n, b)
> Xv <- matrix(0, n, v)
> ib <- cbind(1:n, blocks)
> iv <- cbind(1:n, varieties)
> Xb[ib] <- 1
> Xv[iv] <- 1
> X <- cbind(Xb, Xv)
```

To construct the incidence matrix, `N` say, we could use

```r
> N <- crossprod(Xb, Xv)
```

However a simpler direct way of producing this matrix is to use
`table()`:

```r
> N <- table(blocks, varieties)
```

Index matrices must be numerical: any other form of matrix (e.g. a
logical or character matrix) supplied as a matrix is treated as an
indexing vector.

---

### 5.4 The `array()` function

As well as giving a vector structure a `dim` attribute, arrays can be
constructed from vectors by the `array` function, which has the form

```r
> Z <- array(data_vector, dim_vector)
```

For example, if the vector `h` contains 24 or fewer, numbers then the
command

```r
> Z <- array(h, dim=c(3,4,2))
```

would use `h` to set up _3_ by _4_ by _2_ array in `Z`. If the size of
`h` is exactly 24 the result is the same as

```r
> Z <- h ; dim(Z) <- c(3,4,2)
```

However if `h` is shorter than 24, its values are recycled from the
beginning again to make it up to size 24 (see [The recycling rule](#The-recycling-rule)) but `dim(h) <- c(3,4,2)` would signal an
error about mismatching length. As an extreme but common example

```r
> Z <- array(0, c(3,4,2))
```

makes `Z` an array of all zeros.

At this point `dim(Z)` stands for the dimension vector `c(3,4,2)`, and
`Z[1:24]` stands for the data vector as it was in `h`, and `Z[]` with an
empty subscript or `Z` with no subscript stands for the entire array as
an array.

Arrays may be used in arithmetic expressions and the result is an array
formed by element-by-element operations on the data vector. The `dim`
attributes of operands generally need to be the same, and this becomes
the dimension vector of the result. So if `A`, `B` and `C` are all
similar arrays, then

```r
> D <- 2*A*B + C + 1
```

makes `D` a similar array with its data vector being the result of the
given element-by-element operations. However the precise rule concerning
mixed array and vector calculations has to be considered a little more
carefully.

---

• [The recycling rule](#The-recycling-rule)

---

---

#### 5.4.1 Mixed vector and array arithmetic. The recycling rule

The precise rule affecting element by element mixed calculations with
vectors and arrays is somewhat quirky and hard to find in the
references. From experience we have found the following to be a reliable
guide.

- The expression is scanned from left to right.
- Any short vector operands are extended by recycling their values
  until they match the size of any other operands.
- As long as short vectors and arrays _only_ are encountered, the
  arrays must all have the same `dim` attribute or an error results.
- Any vector operand longer than a matrix or array operand generates
  an error.
- If array structures are present and no error or coercion to vector
  has been precipitated, the result is an array structure with the
  common `dim` attribute of its array operands.

---

### 5.5 The outer product of two arrays

An important operation on arrays is the _outer product_. If `a` and `b`
are two numeric arrays, their outer product is an array whose dimension
vector is obtained by concatenating their two dimension vectors (order
is important), and whose data vector is got by forming all possible
products of elements of the data vector of `a` with those of `b`. The
outer product is formed by the special operator `%o%`:

```r
> ab <- a %o% b
```

An alternative is

```r
> ab <- outer(a, b, "*")
```

The multiplication function can be replaced by an arbitrary function of
two variables. For example if we wished to evaluate the function f(x; y)
= cos(y)/(1 + x\^2) over a regular grid of values with _x_- and
_y_-coordinates defined by the R vectors `x` and `y` respectively, we
could proceed as follows:

```r
> f <- function(x, y) cos(y)/(1 + x^2)
> z <- outer(x, y, f)
```

In particular the outer product of two ordinary vectors is a doubly
subscripted array (that is a matrix, of rank at most 1). Notice that the
outer product operator is of course non-commutative. Defining your own R
functions will be considered further in [Writing your own functions](#Writing-your-own-functions).

#### An example: Determinants of 2 by 2 single-digit matrices

As an artificial but cute example, consider the determinants of _2_ by
_2_ matrices _\[a, b; c, d\]_ where each entry is a non-negative integer
in the range _0, 1, ..., 9_, that is a digit.

The problem is to find the determinants, _ad - bc_, of all possible
matrices of this form and represent the frequency with which each value
occurs as a _high density_ plot. This amounts to finding the probability
distribution of the determinant if each digit is chosen independently
and uniformly at random.

A neat way of doing this uses the `outer()` function twice:

```r
> d <- outer(0:9, 0:9)
> fr <- table(outer(d, d, "-"))
> plot(fr, xlab="Determinant", ylab="Frequency")
```

Notice that `plot()` here uses a histogram like plot method, because it
"sees" that `fr` is of class `"table"`. The "obvious" way of doing this
problem with `for` loops, to be discussed in [Loops and conditional execution](#Loops-and-conditional-execution), is so inefficient as to be
impractical.

It is also perhaps surprising that about 1 in 20 such matrices is
singular.

---

### 5.6 Generalized transpose of an array

The function `aperm(a, perm)` may be used to permute an
array, `a`. The argument `perm` must be a permutation of the integers
_{1, ..., k}_, where _k_ is the number of subscripts in `a`. The result
of the function is an array of the same size as `a` but with old
dimension given by `perm[j]` becoming the new `j`-th dimension. The
easiest way to think of this operation is as a generalization of
transposition for matrices. Indeed if `A` is a matrix, (that is, a
doubly subscripted array) then `B` given by

```r
> B <- aperm(A, c(2,1))
```

is just the transpose of `A`. For this special case a simpler function
`t()` is available, so we could have used `B <- t(A)`.

---

### 5.7 Matrix facilities

As noted above, a matrix is just an array with two subscripts. However
it is such an important special case it needs a separate discussion. R
contains many operators and functions that are available only for
matrices. For example `t(X)` is the matrix transpose function, as noted
above. The functions `nrow(A)` and `ncol(A)` give the number of rows and
columns in the matrix `A` respectively.

---

• [Multiplication](#Multiplication)     
 • [Linear equations and inversion](#Linear-equations-and-inversion)     
 • [Eigenvalues and eigenvectors](#Eigenvalues-and-eigenvectors)     
 • [Singular value decomposition and determinants](#Singular-value-decomposition-and-determinants)     
 • [Least squares fitting and the QR decomposition](#Least-squares-fitting-and-the-QR-decomposition)

---

---

#### 5.7.1 Matrix multiplication

The operator `%*%` is used for matrix multiplication.
An _n_ by _1_ or _1_ by _n_ matrix may of
course be used as an _n_-vector if in the context such is appropriate.
Conversely, vectors which occur in matrix multiplication expressions are
automatically promoted either to row or column vectors, whichever is
multiplicatively coherent, if possible, (although this is not always
unambiguously possible, as we see later).

If, for example, `A` and `B` are square matrices of the same size, then

```r
> A * B
```

is the matrix of element by element products and

```r
> A %*% B
```

is the matrix product. If `x` is a vector, then

```r
> x %*% A %*% x
```

is a quadratic form.[^16^](#FOOT16)

The function `crossprod()` forms "crossproducts", meaning that
`crossprod(X, y)` is the same as `t(X) %*% y` but the operation is more
efficient. If the second argument to `crossprod()` is omitted it is
taken to be the same as the first.

The meaning of `diag()` depends on its argument. `diag(v)`, where `v` is
a vector, gives a diagonal matrix with elements of the vector as the
diagonal entries. On the other hand `diag(M)`, where `M` is a matrix,
gives the vector of main diagonal entries of `M`. This is the same
convention as that used for `diag()` in [MATLAB]{.small}. Also, somewhat
confusingly, if `k` is a single numeric value then `diag(k)` is the `k`
by `k` identity matrix!

---

#### 5.7.2 Linear equations and inversion

Solving linear equations is the inverse of matrix multiplication. When
after

```r
> b <- A %*% x
```

only `A` and `b` are given, the vector `x` is the solution of that
linear equation system. In R,

```r
> solve(A,b)
```

solves the system, returning `x` (up to some accuracy loss). Note that
in linear algebra, formally `x = A^{-1} %*% b` where `A^{-1}` denotes
the _inverse_ of `A`, which can be computed by

```r
solve(A)
```

but rarely is needed. Numerically, it is both inefficient and
potentially unstable to compute `x <- solve(A) %*% b` instead of
`solve(A,b)`.

The quadratic form  `x %*% A^{-1} %*% x`   which is used in multivariate
computations, should be computed by something
like[^17^](#FOOT17) `x %*% solve(A,x)`, rather than computing
the inverse of `A`.

---

#### 5.7.3 Eigenvalues and eigenvectors

The function `eigen(Sm)` calculates the eigenvalues and eigenvectors of
a symmetric matrix `Sm`. The result of this function is a list of two
components named `values` and `vectors`. The assignment

```r
> ev <- eigen(Sm)
```

will assign this list to `ev`. Then `ev$val` is the vector of
eigenvalues of `Sm` and `ev$vec` is the matrix of corresponding
eigenvectors. Had we only needed the eigenvalues we could have used the
assignment:

```r
> evals <- eigen(Sm)$values
```

`evals` now holds the vector of eigenvalues and the second component is
discarded. If the expression

```r
> eigen(Sm)
```

is used by itself as a command the two components are printed, with
their names. For large matrices it is better to avoid computing the
eigenvectors if they are not needed by using the expression

```r
> evals <- eigen(Sm, only.values = TRUE)$values
```

---

#### 5.7.4 Singular value decomposition and determinants

The function `svd(M)` takes an arbitrary matrix argument, `M`, and
calculates the singular value decomposition of `M`. This consists of a
matrix of orthonormal columns `U` with the same column space as `M`, a
second matrix of orthonormal columns `V` whose column space is the row
space of `M` and a diagonal matrix of positive entries `D` such that
`M = U %*% D %*% t(V)`. `D` is actually returned as a vector of the
diagonal elements. The result of `svd(M)` is actually a list of three
components named `d`, `u` and `v`, with evident meanings.

If `M` is in fact square, then, it is not hard to see that

```r
> absdetM <- prod(svd(M)$d)
```

calculates the absolute value of the determinant of `M`. If this
calculation were needed often with a variety of matrices it could be
defined as an R function

```r
> absdet <- function(M) prod(svd(M)$d)
```

after which we could use `absdet()` as just another R function. As a
further trivial but potentially useful example, you might like to
consider writing a function, say `tr()`, to calculate the trace of a
square matrix. \[Hint: You will not need to use an explicit loop. Look
again at the `diag()` function.\]

R has a builtin function `det` to calculate a determinant, including the
sign, and another, `determinant`, to give the sign and modulus
(optionally on log scale),

---

#### 5.7.5 Least squares fitting and the QR decomposition

The function `lsfit()` returns a list giving results of a least squares
fitting procedure. An assignment such as

```r
> ans <- lsfit(X, y)
```

gives the results of a least squares fit where `y` is the vector of
observations and `X` is the design matrix. See the help facility for
more details, and also for the follow-up function `ls.diag()` for, among
other things, regression diagnostics. Note that a grand mean term is
automatically included and need not be included explicitly as a column
of `X`. Further note that you almost always will prefer using `lm(.)`
(see [Linear models](#Linear-models)) to `lsfit()` for regression
modelling.

Another closely related function is `qr()` and its allies. Consider the
following assignments

```r
> Xplus <- qr(X)
> b <- qr.coef(Xplus, y)
> fit <- qr.fitted(Xplus, y)
> res <- qr.resid(Xplus, y)
```

These compute the orthogonal projection of `y` onto the range of `X` in
`fit`, the projection onto the orthogonal complement in `res` and the
coefficient vector for the projection in `b`, that is, `b` is
essentially the result of the [MATLAB]{.small} 'backslash' operator.

It is not assumed that `X` has full column rank. Redundancies will be
discovered and removed as they are found.

This alternative is the older, low-level way to perform least squares
calculations. Although still useful in some contexts, it would now
generally be replaced by the statistical models features, as will be
discussed in [Statistical models in R](#Statistical-models-in-R).

---

### 5.8 Forming partitioned matrices, `cbind()` and `rbind()`

As we have already seen informally, matrices can be built up from other
vectors and matrices by the functions `cbind()` and `rbind()`. Roughly
`cbind()` forms matrices by binding together matrices horizontally, or
column-wise, and `rbind()` vertically, or row-wise.

In the assignment

```r
> X <- cbind(arg_1, arg_2, arg_3, …)
```

the arguments to `cbind()` must be either vectors of any length, or
matrices with the same column size, that is the same number of rows. The
result is a matrix with the concatenated arguments `arg_1`{.variable},
`arg_2`{.variable}, ... forming the columns.

If some of the arguments to `cbind()` are vectors they may be shorter
than the column size of any matrices present, in which case they are
cyclically extended to match the matrix column size (or the length of
the longest vector if no matrices are given).

The function `rbind()` does the corresponding operation for rows. In
this case any vector argument, possibly cyclically extended, are of
course taken as row vectors.

Suppose `X1` and `X2` have the same number of rows. To combine these by
columns into a matrix `X`, together with an initial column of `1`s we
can use

```r
> X <- cbind(1, X1, X2)
```

The result of `rbind()` or `cbind()` always has matrix status. Hence
`cbind(x)` and `rbind(x)` are possibly the simplest ways explicitly to
allow the vector `x` to be treated as a column or row matrix
respectively.

---

### 5.9 The concatenation function, `c()`, with arrays

It should be noted that whereas `cbind()` and `rbind()` are
concatenation functions that respect `dim` attributes, the basic `c()`
function does not, but rather clears numeric objects of all `dim` and
`dimnames` attributes. This is occasionally useful in its own right.

The official way to coerce an array back to a simple vector object is to
use `as.vector()`

```r
> vec <- as.vector(X)
```

However a similar result can be achieved by using `c()` with just one
argument, simply for this side-effect:

```r
> vec <- c(X)
```

There are slight differences between the two, but ultimately the choice
between them is largely a matter of style (with the former being
preferable).

---

### 5.10 Frequency tables from factors

Recall that a factor defines a partition into groups. Similarly a pair
of factors defines a two way cross classification, and so on.
The function `table()` allows frequency tables to be
calculated from equal length factors. If there are _k_ factor arguments,
the result is a _k_-way array of frequencies.

Suppose, for example, that `statef` is a factor giving the state code
for each entry in a data vector. The assignment

```r
> statefr <- table(statef)
```

gives in `statefr` a table of frequencies of each state in the sample.
The frequencies are ordered and labelled by the `levels` attribute of
the factor. This simple case is equivalent to, but more convenient than,

```r
> statefr <- tapply(statef, statef, length)
```

Further suppose that `incomef` is a factor giving a suitably defined
"income class" for each entry in the data vector, for example with the
`cut()` function:

```r
> factor(cut(incomes, breaks = 35+10*(0:7))) -> incomef
```

Then to calculate a two-way table of frequencies:

```r
> table(incomef,statef)
         statef
incomef   act nsw nt qld sa tas vic wa
  (35,45]   1   1  0   1  0   0   1  0
  (45,55]   1   1  1   1  2   0   1  3
  (55,65]   0   3  1   3  2   2   2  1
  (65,75]   0   1  0   0  0   0   1  0
```

Extension to higher-way frequency tables is immediate.

---
