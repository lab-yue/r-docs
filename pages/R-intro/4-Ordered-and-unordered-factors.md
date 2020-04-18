# 4 Ordered and unordered factors

---

A _factor_ is a vector object used to specify a discrete classification
(grouping) of the components of other vectors of the same length. R
provides both _ordered_ and _unordered_ factors. While the "real"
application of factors is with model formulae (see
[Contrasts](#Contrasts)), we here look at a specific example.

---

• [The function `tapply()` and ragged arrays](#The-function-tapply_0028_0029-and-ragged-arrays)     
 • [Ordered factors](#Ordered-factors)

---

### 4.1 A specific example

Suppose, for example, we have a sample of 30 tax accountants from all
the states and territories of Australia[^14^](#FOOT14) and
their individual state of origin is specified by a character vector of
state mnemonics as

```r
> state <- c("tas", "sa",  "qld", "nsw", "nsw", "nt",  "wa",  "wa",
             "qld", "vic", "nsw", "vic", "qld", "qld", "sa",  "tas",
             "sa",  "nt",  "wa",  "vic", "qld", "nsw", "nsw", "wa",
             "sa",  "act", "nsw", "vic", "vic", "act")
```

Notice that in the case of a character vector, "sorted" means sorted in
alphabetical order.

A _factor_ is similarly created using the `factor()` function:

```r
> statef <- factor(state)
```

The `print()` function handles factors slightly differently from other
objects:

```r
> statef
 [1] tas sa  qld nsw nsw nt  wa  wa  qld vic nsw vic qld qld sa
[16] tas sa  nt  wa  vic qld nsw nsw wa  sa  act nsw vic vic act
Levels:  act nsw nt qld sa tas vic wa
```

To find out the levels of a factor the function `levels()` can be used.

```r
> levels(statef)
[1] "act" "nsw" "nt"  "qld" "sa"  "tas" "vic" "wa"
```

---

• [The function tapply() and ragged arrays](#The-function-tapply_0028_0029-and-ragged-arrays)     
 • [Ordered factors](#Ordered-factors)

---

---

### 4.2 The function `tapply()` and ragged arrays

To continue the previous example, suppose we have the incomes of the
same tax accountants in another vector (in suitably large units of
money)

```r
> incomes <- c(60, 49, 40, 61, 64, 60, 59, 54, 62, 69, 70, 42, 56,
               61, 61, 61, 58, 51, 48, 65, 49, 49, 41, 48, 52, 46,
               59, 46, 58, 43)
```

To calculate the sample mean income for each state we can now use the
special function `tapply()`:

```r
> incmeans <- tapply(incomes, statef, mean)
```

giving a means vector with the components labelled by the levels

```r
   act    nsw     nt    qld     sa    tas    vic     wa
44.500 57.333 55.500 53.600 55.000 60.500 56.000 52.250
```

The function `tapply()` is used to apply a function, here `mean()`, to
each group of components of the first argument, here `incomes`, defined
by the levels of the second component, here
`statef`[^15^](#FOOT15), as if they were separate vector
structures. The result is a structure of the same length as the levels
attribute of the factor containing the results. The reader should
consult the help document for more details.

Suppose further we needed to calculate the standard errors of the state
income means. To do this we need to write an R function to calculate the
standard error for any given vector. Since there is an builtin function
`var()` to calculate the sample variance, such a function is a very
simple one liner, specified by the assignment:

```r
> stdError <- function(x) sqrt(var(x)/length(x))
```

(Writing functions will be considered later in [Writing your own functions](#Writing-your-own-functions). Note that R's a builtin
function `sd()` is something different.)
After this assignment, the standard errors are calculated by

```r
> incster <- tapply(incomes, statef, stdError)
```

and the values calculated are then

```r
> incster
act    nsw  nt    qld     sa tas   vic     wa
1.5 4.3102 4.5 4.1061 2.7386 0.5 5.244 2.6575
```

As an exercise you may care to find the usual 95% confidence limits for
the state mean incomes. To do this you could use `tapply()` once more
with the `length()` function to find the sample sizes, and the `qt()`
function to find the percentage points of the appropriate
_t_-distributions. (You could also investigate R's facilities for
_t_-tests.)

The function `tapply()` can also be used to handle more complicated
indexing of a vector by multiple categories. For example, we might wish
to split the tax accountants by both state and sex. However in this
simple instance (just one factor) what happens can be thought of as
follows. The values in the vector are collected into groups
corresponding to the distinct entries in the factor. The function is
then applied to each of these groups individually. The value is a vector
of function results, labelled by the `levels` attribute of the factor.

The combination of a vector and a labelling factor is an example of what
is sometimes called a _ragged array_, since the subclass sizes are
possibly irregular. When the subclass sizes are all the same the
indexing may be done implicitly and much more efficiently, as we see in
the next section.

---

### 4.3 Ordered factors

The levels of factors are stored in alphabetical order, or in the order
they were specified to `factor` if they were specified explicitly.

Sometimes the levels will have a natural ordering that we want to record
and want our statistical analysis to make use of. The `ordered()`
function creates such ordered factors but is
otherwise identical to `factor`. For most purposes the only difference
between ordered and unordered factors is that the former are printed
showing the ordering of the levels, but the contrasts generated for them
in fitting linear models are different.

---
