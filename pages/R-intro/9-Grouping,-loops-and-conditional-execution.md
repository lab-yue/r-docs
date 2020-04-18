9 Grouping, loops and conditional execution

---

---

• [Grouped expressions](#Grouped-expressions)     
 • [Control statements](#Control-statements)

---

---

### 9.1 Grouped expressions

R is an expression language in the sense that its only command type is a
function or expression which returns a result. Even an assignment is an
expression whose result is the value assigned, and it may be used
wherever any expression may be used; in particular multiple assignments
are possible.

Commands may be grouped together in braces, `{expr_1; …; expr_m}`, in
which case the value of the group is the result of the last expression
in the group evaluated. Since such a group is also an expression it may,
for example, be itself included in parentheses and used as part of an
even larger expression, and so on.

---

### 9.2 Control statements

---

• [Conditional execution](#Conditional-execution)     
 • [Repetitive execution](#Repetitive-execution)

---

---

#### 9.2.1 Conditional execution: `if` statements

The language has available a conditional construction of the form

```r
> if (expr_1) expr_2 else expr_3
```

where `expr_1`{.variable} must evaluate to a single logical value and
the result of the entire expression is then evident.

The "short-circuit" operators `&&` and `||` are often used as part of
the condition in an `if` statement. Whereas `&` and `|` apply
element-wise to vectors, `&&` and `||` apply to vectors of length one,
and only evaluate their second argument if necessary.

There is a vectorized version of the `if`/`else` construct, the `ifelse`
function. This has the form `ifelse(condition, a, b)` and returns a
vector of the same length as `condition`, with elements `a[i]` if
`condition[i]` is true, otherwise `b[i]` (where `a` and `b` are recycled
as necessary).

---

#### 9.2.2 Repetitive execution: `for` loops, `repeat` and `while`

There is also a `for` loop construction which has the form

```r
> for (name in expr_1) expr_2
```

where `name` is the loop variable. `expr_1`{.variable} is a vector
expression, (often a sequence like `1:20`), and `expr_2`{.variable} is
often a grouped expression with its sub-expressions written in terms of
the dummy _name_. `expr_2`{.variable} is repeatedly evaluated as
`name`{.variable} ranges through the values in the vector result of
`expr_1`{.variable}.

As an example, suppose `ind` is a vector of class indicators and we wish
to produce separate plots of `y` versus `x` within classes. One
possibility here is to use `coplot()`,[^21^](#FOOT21) which
will produce an array of plots corresponding to each level of the
factor. Another way to do this, now putting all plots on the one
display, is as follows:

```r
> xc <- split(x, ind)
> yc <- split(y, ind)
> for (i in 1:length(yc)) {
    plot(xc[[i]], yc[[i]])
    abline(lsfit(xc[[i]], yc[[i]]))
  }
```

(Note the function `split()` which produces a list of vectors obtained
by splitting a larger vector according to the classes specified by a
factor. This is a useful function, mostly used in connection with
boxplots. See the `help` facility for further details.)

> **Warning**: `for()` loops are used in R code much less often than in
> compiled languages. Code that takes a 'whole object' view is likely to
> be both clearer and faster in R.

Other looping facilities include the

```r
> repeat expr
```

statement and the

```r
> while (condition) expr
```

statement.

The `break` statement can be used to terminate any loop, possibly
abnormally. This is the only way to terminate `repeat` loops.

The `next` statement can be used to discontinue one particular cycle and
skip to the "next".

Control statements are most often used in connection with _functions_
which are discussed in [Writing your own functions](#Writing-your-own-functions), and where more examples will
emerge.

---
