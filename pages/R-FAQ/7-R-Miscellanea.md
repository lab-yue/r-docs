7 R Miscellanea

---

---

• [How can I set components of a list to NULL?](#How-can-I-set-components-of-a-list-to-NULL_003f)     
 • [How can I save my workspace?](#How-can-I-save-my-workspace_003f)     
 • [How can I clean up my workspace?](#How-can-I-clean-up-my-workspace_003f)     
 • [How can I get eval() and D() to work?](#How-can-I-get-eval_0028_0029-and-D_0028_0029-to-work_003f)     
 • [Why do my matrices lose dimensions?](#Why-do-my-matrices-lose-dimensions_003f)     
 • [How does autoloading work?](#How-does-autoloading-work_003f)     
 • [How should I set options?](#How-should-I-set-options_003f)     
 • [How do file names work in Windows?](#How-do-file-names-work-in-Windows_003f)     
 • [Why does plotting give a color allocation error?](#Why-does-plotting-give-a-color-allocation-error_003f)     
 • [How do I convert factors to numeric?](#How-do-I-convert-factors-to-numeric_003f)     
 • [Are Trellis displays implemented in R?](#Are-Trellis-displays-implemented-in-R_003f)     
 • [What are the enclosing and parent environments?](#What-are-the-enclosing-and-parent-environments_003f)     
 • [How can I substitute into a plot label?](#How-can-I-substitute-into-a-plot-label_003f)     
 • [What are valid names?](#What-are-valid-names_003f)     
 • [Are GAMs implemented in R?](#Are-GAMs-implemented-in-R_003f)     
 • [Why is the output not printed when I source() a file?](#Why-is-the-output-not-printed-when-I-source_0028_0029-a-file_003f)     
 • [Why does outer() behave strangely with my function?](#Why-does-outer_0028_0029-behave-strangely-with-my-function_003f)     
 • [Why does the output from anova() depend on the order of factors in the model?](#Why-does-the-output-from-anova_0028_0029-depend-on-the-order-of-factors-in-the-model_003f)     
 • [How do I produce PNG graphics in batch mode?](#How-do-I-produce-PNG-graphics-in-batch-mode_003f)     
 • [How can I get command line editing to work?](#How-can-I-get-command-line-editing-to-work_003f)     
 • [How can I turn a string into a variable?](#How-can-I-turn-a-string-into-a-variable_003f)     
 • [Why do lattice/trellis graphics not work?](#Why-do-lattice_002ftrellis-graphics-not-work_003f)     
 • [How can I sort the rows of a data frame?](#How-can-I-sort-the-rows-of-a-data-frame_003f)     
 • [Why does the help.start() search engine not work?](#Why-does-the-help_002estart_0028_0029-search-engine-not-work_003f)     
 • [Why did my .Rprofile stop working when I updated R?](#Why-did-my-_002eRprofile-stop-working-when-I-updated-R_003f)     
 • [Where have all the methods gone?](#Where-have-all-the-methods-gone_003f)     
 • [How can I create rotated axis labels?](#How-can-I-create-rotated-axis-labels_003f)     
 • [Why is read.table() so inefficient?](#Why-is-read_002etable_0028_0029-so-inefficient_003f)     
 • [What is the difference between package and library?](#What-is-the-difference-between-package-and-library_003f)     
 • [I installed a package but the functions are not there](#I-installed-a-package-but-the-functions-are-not-there)     
 • [Why doesn\'t R think these numbers are equal?](#Why-doesn_0027t-R-think-these-numbers-are-equal_003f)     
 • [How can I capture or ignore errors in a long simulation?](#How-can-I-capture-or-ignore-errors-in-a-long-simulation_003f)     
 • [Why are powers of negative numbers wrong?](#Why-are-powers-of-negative-numbers-wrong_003f)     
 • [How can I save the result of each iteration in a loop into a separate file?](#How-can-I-save-the-result-of-each-iteration-in-a-loop-into-a-separate-file_003f)     
 • [Why are p-values not displayed when using lmer()?](#Why-are-p_002dvalues-not-displayed-when-using-lmer_0028_0029_003f)     
 • [Why are there unwanted borders](#Why-are-there-unwanted-borders)     
 • [Why does backslash behave strangely inside strings?](#Why-does-backslash-behave-strangely-inside-strings_003f)     
 • [How can I put error bars or confidence bands on my plot?](#How-can-I-put-error-bars-or-confidence-bands-on-my-plot_003f)     
 • [How do I create a plot with two y-axes?](#How-do-I-create-a-plot-with-two-y_002daxes_003f)     
 • [How do I access the source code for a function?](#How-do-I-access-the-source-code-for-a-function_003f)     
 • [Why does summary() report strange results for the R\^2 estimate when I fit a linear model with no intercept?](#Why-does-summary_0028_0029-report-strange-results-for-the-R_005e2-estimate-when-I-fit-a-linear-model-with-no-intercept_003f)     
 • [Why is R apparently not releasing memory?](#Why-is-R-apparently-not-releasing-memory_003f)     
 • [How can I enable secure https downloads in R?](#How-can-I-enable-secure-https-downloads-in-R_003f)     
 • [How can I get CRAN package binaries for outdated versions of R?](#How-can-I-get-CRAN-package-binaries-for-outdated-versions-of-R_003f)

---

---

### 7.1 How can I set components of a list to NULL?

You can use

```r
x[i] <- list(NULL)
```

to set component `i` of the list `x` to `NULL`, similarly for named
components. Do not set `x[i]` or `x[[i]]` to `NULL`, because this will
remove the corresponding component from the list.

For dropping the row names of a matrix `x`, it may be easier to use
`rownames(x) <- NULL`, similarly for column names.

---

### 7.2 How can I save my workspace?

`save.image()` saves the objects in the user's `.GlobalEnv` to the file
`.RData` in the R startup directory. (This is also what happens
after [q(\"yes\")]{.kbd}.) Using `save.image(file)` one can save the
image under a different name.

---

### 7.3 How can I clean up my workspace?

To remove all objects in the currently active environment (typically
`.GlobalEnv`), you can do

```r
rm(list = ls(all = TRUE))
```

(Without `all = TRUE`, only the objects with names not starting
with a '`.`' are removed.)

---

### 7.4 How can I get eval() and D() to work?

Strange things will happen if you use `eval(print(x), envir = e)` or
`D(x^2, "x")`. The first one will either tell you that \"`x`\" is not
found, or print the value of the wrong `x`. The other one will likely
return zero if `x` exists, and an error otherwise.

This is because in both cases, the first argument is evaluated in the
calling environment first. The result (which should be an object of mode
`"expression"` or `"call"`) is then evaluated or differentiated. What
you (most likely) really want is obtained by "quoting" the first
argument upon surrounding it with `expression()`. For example,

```r
R> D(expression(x^2), "x")
2 * x
```

Although this behavior may initially seem to be rather strange, it is
perfectly logical. The "intuitive" behavior could easily be implemented,
but problems would arise whenever the expression is contained in a
variable, passed as a parameter, or is the result of a function call.
Consider for instance the semantics in cases like

```r
D2 <- function(e, n) D(D(e, n), n)
```

or

```r
g <- function(y) eval(substitute(y), sys.frame(sys.parent(n = 2)))
g(a * b)
```

See the help page for `deriv()` for more examples.

---

### 7.5 Why do my matrices lose dimensions?

When a matrix with a single row or column is created by a subscripting
operation, e.g., `row <- mat[2, ]`, it is by default turned into a
vector. In a similar way if an array with dimension, say, 2 x 3 x 1 x 4
is created by subscripting it will be coerced into a 2 x 3 x 4 array,
losing the unnecessary dimension. After much discussion this has been
determined to be a _feature_.

To prevent this happening, add the option `drop = FALSE` to the
subscripting. For example,

```r
rowmatrix <- mat[2, , drop = FALSE]  # creates a row matrix
colmatrix <- mat[, 2, drop = FALSE]  # creates a column matrix
a <- b[1, 1, 1, drop = FALSE]        # creates a 1 x 1 x 1 array
```

The `drop = FALSE` option should be used defensively when
programming. For example, the statement

```r
somerows <- mat[index, ]
```

will return a vector rather than a matrix if `index` happens to have
length 1, causing errors later in the code. It should probably be
rewritten as

```r
somerows <- mat[index, , drop = FALSE]
```

---

### 7.6 How does autoloading work?

R has a special environment called `.AutoloadEnv`. Using
[autoload(`name`{.variable}, `pkg`{.variable})]{.kbd}, where
`name`{.variable} and `pkg`{.variable} are strings giving the names of
an object and the package containing it, stores some information in this
environment. When R tries to evaluate `name`{.variable}, it loads the
corresponding package `pkg`{.variable} and reevaluates `name`{.variable}
in the new package's environment.

Using this mechanism makes R behave as if the package was loaded, but
does not occupy memory (yet).

See the help page for `autoload()` for a very nice example.

---

### 7.7 How should I set options?

The function `options()` allows setting and examining a variety of
global "options" which affect the way in which R computes and displays
its results. The variable `.Options` holds the current values of these
options, but should never directly be assigned to unless you want to
drive yourself crazy---simply pretend that it is a "read-only" variable.

For example, given

```r
test1 <- function(x = pi, dig = 3) {
  oo <- options(digits = dig); on.exit(options(oo));
  cat(.Options$digits, x, "\n")
}
test2 <- function(x = pi, dig = 3) {
  .Options$digits <- dig
  cat(.Options$digits, x, "\n")
}
```

we obtain:

```r
R> test1()
3 3.14
R> test2()
3 3.141593
```

What is really used is the _global_ value of `.Options`, and using
[options(OPT = VAL)]{.kbd} correctly updates it. Local copies of
`.Options`, either in `.GlobalEnv` or in a function environment (frame),
are just silently disregarded.

---

### 7.8 How do file names work in Windows?

As R uses C-style string handling, '`\`' is treated as an
escape character, so that for example one can enter a newline as
'`\n`'. When you really need a '`\`', you have to
escape it with another '`\`'.

Thus, in filenames use something like `"c:\\data\\money.dat"`. You can
also replace '`\`' by '`/`' (`"c:/data/money.dat"`).

---

### 7.9 Why does plotting give a color allocation error?

On an X11 device, plotting sometimes, e.g., when running
`demo("image")`, results in "Error: color allocation error". This is an
X problem, and only indirectly related to R. It occurs when applications
started prior to R have used all the available colors. (How many colors
are available depends on the X configuration; sometimes only 256 colors
can be used.)

One application which is notorious for "eating" colors is Netscape. If
the problem occurs when Netscape is running, try (re)starting it with
either the `-no-install` (to use the default colormap) or the
`-install` (to install a private colormap) option.

You could also set the `colortype` of `X11()` to `"pseudo.cube"` rather
than the default `"pseudo"`. See the help page for `X11()` for more
information.

---

### 7.10 How do I convert factors to numeric?

It may happen that when reading numeric data into R (usually, when
reading in a file), they come in as factors. If `f` is such a factor
object, you can use

```r
as.numeric(as.character(f))
```

to get the numbers back. More efficient, but harder to remember, is

```r
as.numeric(levels(f))[as.integer(f)]
```

In any case, do not call `as.numeric()` or their likes directly for the
task at hand (as `as.numeric()` or `unclass()` give the internal codes).

---

### 7.11 Are Trellis displays implemented in R?

The recommended package
[**lattice**](https://CRAN.R-project.org/package=lattice) (which is
based on base package **grid**) provides graphical functionality that is
compatible with most Trellis commands.

You could also look at `coplot()` and `dotchart()` which might do at
least some of what you want. Note also that the R version of `pairs()`
is fairly general and provides most of the functionality of `splom()`,
and that R's default plot method has an argument `asp` allowing to
specify (and fix against device resizing) the aspect ratio of the plot.

(Because the word "Trellis" has been claimed as a trademark we do not
use it in R. The name "lattice" has been chosen for the R equivalent.)

---

### 7.12 What are the enclosing and parent environments?

Inside a function you may want to access variables in two additional
environments: the one that the function was defined in ("enclosing"),
and the one it was invoked in ("parent").

If you create a function at the command line or load it in a package its
enclosing environment is the global workspace. If you define a function
`f()` inside another function `g()` its enclosing environment is the
environment inside `g()`. The enclosing environment for a function is
fixed when the function is created. You can find out the enclosing
environment for a function `f()` using `environment(f)`.

The "parent" environment, on the other hand, is defined when you invoke
a function. If you invoke `lm()` at the command line its parent
environment is the global workspace, if you invoke it inside a function
`f()` then its parent environment is the environment inside `f()`. You
can find out the parent environment for an invocation of a function by
using `parent.frame()` or `sys.frame(sys.parent())`.

So for most user-visible functions the enclosing environment will be the
global workspace, since that is where most functions are defined. The
parent environment will be wherever the function happens to be called
from. If a function `f()` is defined inside another function `g()` it
will probably be used inside `g()` as well, so its parent environment
and enclosing environment will probably be the same.

Parent environments are important because things like model formulas
need to be evaluated in the environment the function was called from,
since that's where all the variables will be available. This relies on
the parent environment being potentially different with each invocation.

Enclosing environments are important because a function can use
variables in the enclosing environment to share information with other
functions or with other invocations of itself (see the section on
lexical scoping). This relies on the enclosing environment being the
same each time the function is invoked. (In C this would be done with
static variables.)

Scoping _is_ hard. Looking at examples helps. It is particularly
instructive to look at examples that work differently in R and S and try
to see why they differ. One way to describe the scoping differences
between R and S is to say that in S the enclosing environment is
_always_ the global workspace, but in R the enclosing environment is
wherever the function was created.

---

### 7.13 How can I substitute into a plot label?

Often, it is desired to use the value of an R object in a plot label,
e.g., a title. This is easily accomplished using `paste()` if the label
is a simple character string, but not always obvious in case the label
is an expression (for refined mathematical annotation). In such a case,
either use `parse()` on your pasted character string or use
`substitute()` on an expression. For example, if `ahat` is an estimator
of your parameter _a_ of interest, use

```r
title(substitute(hat(a) == ahat, list(ahat = ahat)))
```

(note that it is '`==`' and not '`=`'). Sometimes
`bquote()` gives a more compact form, e.g.,

```r
title(bquote(hat(a) = .(ahat)))
```

where subexpressions enclosed in '`.()`' are replaced by their
values.

There are more examples in the mailing list archives.

---

### 7.14 What are valid names?

When creating data frames using `data.frame()` or `read.table()`, R by
default ensures that the variable names are syntactically valid. (The
argument `check.names` to these functions controls whether
variable names are checked and adjusted by `make.names()` if needed.)

To understand what names are "valid", one needs to take into account
that the term "name" is used in several different (but related) ways in
the language:

1.  A _syntactic name_ is a string the parser interprets as this type of
    expression. It consists of letters, numbers, and the dot and (for
    versions of R at least 1.9.0) underscore characters, and starts with
    either a letter or a dot not followed by a number. Reserved words
    are not syntactic names.
2.  An _object name_ is a string associated with an object that is
    assigned in an expression either by having the object name on the
    left of an assignment operation or as an argument to the `assign()`
    function. It is usually a syntactic name as well, but can be any
    non-empty string if it is quoted (and it is always quoted in the
    call to `assign()`).
3.  An _argument name_ is what appears to the left of the equals sign
    when supplying an argument in a function call (for example,
    `f(trim=.5)`). Argument names are also usually syntactic names, but
    again can be anything if they are quoted.
4.  An _element name_ is a string that identifies a piece of an object
    (a component of a list, for example.) When it is used on the right
    of the '`$`' operator, it must be a syntactic name, or
    quoted. Otherwise, element names can be any strings. (When an object
    is used as a database, as in a call to `eval()` or `attach()`, the
    element names become object names.)
5.  Finally, a _file name_ is a string identifying a file in the
    operating system for reading, writing, etc. It really has nothing
    much to do with names in the language, but it is traditional to call
    these strings file "names".

---

### 7.15 Are GAMs implemented in R?

Package [**gam**](https://CRAN.R-project.org/package=gam) from CRAN
implements all the Generalized Additive Models (GAM) functionality as
described in the GAM chapter of the White Book. In particular, it
implements backfitting with both local regression and smoothing splines,
and is extendable. There is a `gam()` function for GAMs in package
[**mgcv**](https://CRAN.R-project.org/package=mgcv), but it is not an
exact clone of what is described in the White Book (no `lo()` for
example). Package [**gss**](https://CRAN.R-project.org/package=gss) can
fit spline-based GAMs too. And if you can accept regression splines you
can use `glm()`. For Gaussian GAMs you can use `bruto()` from package
[**mda**](https://CRAN.R-project.org/package=mda).

---

### 7.16 Why is the output not printed when I source() a file?

Most R commands do not generate any output. The command

```r
1+1
```

computes the value 2 and returns it; the command

```r
summary(glm(y~x+z, family=binomial))
```

fits a logistic regression model, computes some summary information and
returns an object of class `"summary.glm"` (see [How should I write
summary methods?](#How-should-I-write-summary-methods_003f)).

If you type '`1+1`' or
'`summary(glm(y~x+z, family=binomial))`' at the command line
the returned value is automatically printed (unless it is
`invisible()`), but in other circumstances, such as in a `source()`d
file or inside a function it isn't printed unless you specifically print
it.

To print the value use

```r
print(1+1)
```

or

```r
print(summary(glm(y~x+z, family=binomial)))
```

instead, or use `source(file, echo=TRUE)`.

---

### 7.17 Why does outer() behave strangely with my function?

As the help for `outer()` indicates, it does not work on arbitrary
functions the way the `apply()` family does. It requires functions that
are vectorized to work elementwise on arrays. As you can see by looking
at the code, `outer(x, y, FUN)` creates two large vectors containing
every possible combination of elements of `x` and `y` and then passes
this to `FUN` all at once. Your function probably cannot handle two
large vectors as parameters.

If you have a function that cannot handle two vectors but can handle two
scalars, then you can still use `outer()` but you will need to wrap your
function up first, to simulate vectorized behavior. Suppose your
function is

```r
foo <- function(x, y, happy) {
  stopifnot(length(x) == 1, length(y) == 1) # scalars only!
  (x + y) * happy
}
```

If you define the general function

```r
wrapper <- function(x, y, my.fun, ...) {
  sapply(seq_along(x), FUN = function(i) my.fun(x[i], y[i], ...))
}
```

then you can use `outer()` by writing, e.g.,

```r
outer(1:4, 1:2, FUN = wrapper, my.fun = foo, happy = 10)
```

Scalar functions can also be vectorized using `Vectorize()`.

---

### 7.18 Why does the output from anova() depend on the order of factors in the model?

In a model such as `~A+B+A:B`, R will report the difference in sums of
squares between the models `~1`, `~A`, `~A+B` and `~A+B+A:B`. If the
model were `~B+A+A:B`, R would report differences between `~1`, `~B`,
`~A+B`, and `~A+B+A:B` . In the first case the sum of squares for `A` is
comparing `~1` and `~A`, in the second case it is comparing `~B` and
`~B+A`. In a non-orthogonal design (i.e., most unbalanced designs) these
comparisons are (conceptually and numerically) different.

Some packages report instead the sums of squares based on comparing the
full model to the models with each factor removed one at a time (the
famous 'Type III sums of squares' from SAS, for example). These do not
depend on the order of factors in the model. The question of which set
of sums of squares is the Right Thing provokes low-level holy wars on
R-help from time to time.

There is no need to be agitated about the particular sums of squares
that R reports. You can compute your favorite sums of squares quite
easily. Any two models can be compared with `anova(model1, model2)`, and
`drop1(model1)` will show the sums of squares resulting from dropping
single terms.

---

### 7.19 How do I produce PNG graphics in batch mode?

Under a Unix-like, if your installation supports the `type="cairo"`
option to the `png()` device there should be no problems, and the
default settings should just work. This option is not available for
versions of R prior to 2.7.0, or without support for cairo. From R 2.7.0
`png()` by default uses the Quartz device on macOS, and that too works
in batch mode.

Earlier versions of the `png()` device used the X11 driver, which is a
problem in batch mode or for remote operation. If you have Ghostscript
you can use `bitmap()`, which produces a PostScript or PDF file then
converts it to any bitmap format supported by Ghostscript. On some
installations this produces ugly output, on others it is perfectly
satisfactory. Many systems now come with Xvfb from
[X.Org](http://www.x.org/) (possibly as an optional install), which is
an X11 server that does not require a screen; and there is the
[**GDD**](https://CRAN.R-project.org/package=GDD) package from CRAN,
which produces PNG, JPEG and GIF bitmaps without X11.

---

### 7.20 How can I get command line editing to work?

The Unix-like command-line interface to R can only provide the inbuilt
command line editor which allows recall, editing and re-submission of
prior commands provided that the GNU readline library is available at
the time R is configured for compilation. Note that the 'development'
version of readline including the appropriate headers is needed: users
of Linux binary distributions will need to install packages such as
`libreadline-dev` (Debian) or `readline-devel` (Red Hat).

---

### 7.21 How can I turn a string into a variable?

If you have

```r
varname <- c("a", "b", "d")
```

you can do

```r
get(varname[1]) + 2
```

for

```r
a + 2
```

or

```r
assign(varname[1], 2 + 2)
```

for

```r
a <- 2 + 2
```

or

```r
eval(substitute(lm(y ~ x + variable),
                list(variable = as.name(varname[1]))))
```

for

```r
lm(y ~ x + a)
```

At least in the first two cases it is often easier to just use a list,
and then you can easily index it by name

```r
vars <- list(a = 1:10, b = rnorm(100), d = LETTERS)
vars[["a"]]
```

without any of this messing about.

---

### 7.22 Why do lattice/trellis graphics not work?

The most likely reason is that you forgot to tell R to display the
graph. Lattice functions such as `xyplot()` create a graph object, but
do not display it (the same is true of
[**ggplot2**](https://CRAN.R-project.org/package=ggplot2) graphics, and
Trellis graphics in [S-PLUS]{.small}). The `print()` method for the
graph object produces the actual display. When you use these functions
interactively at the command line, the result is automatically printed,
but in `source()` or inside your own functions you will need an explicit
`print()` statement.

---

### 7.23 How can I sort the rows of a data frame?

To sort the rows within a data frame, with respect to the values in one
or more of the columns, simply use `order()` (e.g.,
`DF[order(DF$a, DF[["b"]]), ]` to sort the data frame `DF` on columns
named `a` and `b`).

---

### 7.24 Why does the help.start() search engine not work?

The browser-based search engine in `help.start()` utilizes a Java
applet. In order for this to function properly, a compatible version of
Java must installed on your system and linked to your browser, and both
Java _and_ JavaScript need to be enabled in your browser.

There have been a number of compatibility issues with versions of Java
and of browsers. See [Enabling search in HTML help](./R-admin.html#Enabling-search-in-HTML-help) in R Installation and
Administration, for further details.

---

### 7.25 Why did my .Rprofile stop working when I updated R?

Did you read the `NEWS` file? For functions that are not in the
**base** package you need to specify the correct package namespace,
since the code will be run _before_ the packages are loaded. E.g.,

```r
ps.options(horizontal = FALSE)
help.start()
```

needs to be

```r
grDevices::ps.options(horizontal = FALSE)
utils::help.start()
```

(`graphics::ps.options(horizontal = FALSE)` in R 1.9.x).

---

### 7.26 Where have all the methods gone?

Many functions, particularly S3 methods, are now hidden in namespaces.
This has the advantage that they cannot be called inadvertently with
arguments of the wrong class, but it makes them harder to view.

To see the code for an S3 method (e.g., `[.terms`) use

```r
getS3method("[", "terms")
```

To see the code for an unexported function `foo()` in the namespace of
package `"bar"` use `bar:::foo`. Don't use these constructions to call
unexported functions in your own code---they are probably unexported for
a reason and may change without warning.

---

### 7.27 How can I create rotated axis labels?

To rotate axis labels (using base graphics), you need to use `text()`,
rather than `mtext()`, as the latter does not support `par("srt")`.

```r
## Increase bottom margin to make room for rotated labels
par(mar = c(7, 4, 4, 2) + 0.1)
## Create plot with no x axis and no x axis label
plot(1 : 8, xaxt = "n",  xlab = "")
## Set up x axis with tick marks alone
axis(1, labels = FALSE)
## Create some text labels
labels <- paste("Label", 1:8, sep = " ")
## Plot x axis labels at default tick marks
text(1:8, par("usr")[3] - 0.25, srt = 45, adj = 1,
     labels = labels, xpd = TRUE)
## Plot x axis label at line 6 (of 7)
mtext(1, text = "X Axis Label", line = 6)
```

When plotting the x axis labels, we use `srt = 45` for text rotation
angle, `adj = 1` to place the right end of text at the tick marks, and
`xpd = TRUE` to allow for text outside the plot region. You can adjust
the value of the `0.25` offset as required to move the axis labels up or
down relative to the x axis. See `?par` for more information.

Also see Figure 1 and associated code in Paul Murrell (2003),
"Integrating grid Graphics Output with Base Graphics Output", _R News_,
**3/2**, 7--12.

---

### 7.28 Why is read.table() so inefficient?

By default, `read.table()` needs to read in everything as character
data, and then try to figure out which variables to convert to numerics
or factors. For a large data set, this takes considerable amounts of
time and memory. Performance can substantially be improved by using the
`colClasses` argument to specify the classes to be assumed for the
columns of the table.

---

### 7.29 What is the difference between package and library?

A _package_ is a standardized collection of material extending R, e.g.
providing code, data, or documentation. A _library_ is a place
(directory) where R knows to find packages it can use (i.e., which were
_installed_). R is told to use a package (to "load" it and add it to the
search path) via calls to the function `library`. I.e., `library()` is
employed to load a package from libraries containing packages.

See [R Add-On Packages](#R-Add_002dOn-Packages), for more details. See
also Uwe Ligges (2003), "R Help Desk: Package Management", _R News_,
**3/3**, 37--39.

---

### 7.30 I installed a package but the functions are not there

To actually _use_ the package, it needs to be _loaded_ using
`library()`.

See [R Add-On Packages](#R-Add_002dOn-Packages) and [What is the
difference between package and
library?](#What-is-the-difference-between-package-and-library_003f) for
more information.

---

### 7.31 Why doesn't R think these numbers are equal?

The only numbers that can be represented exactly in R's numeric type are
integers and fractions whose denominator is a power of 2. All other
numbers are internally rounded to (typically) 53 binary digits accuracy.
As a result, two floating point numbers will not reliably be equal
unless they have been computed by the same algorithm, and not always
even then. For example

```r
R> a <- sqrt(2)
R> a * a == 2
[1] FALSE
R> a * a - 2
[1] 4.440892e-16
R> print(a * a, digits = 18)
[1] 2.00000000000000044
```

The function `all.equal()` compares two objects using a numeric
tolerance of `.Machine$double.eps ^ 0.5`. If you want much greater
accuracy than this you will need to consider error propagation
carefully.

A discussion with many easily followed examples is in Appendix G
"Computational Precision and Floating Point Arithmetic", pages 753--771
of _Statistical Analysis and Data Display: An Intermediate Course with
Examples in R_, Richard M. Heiberger and Burt Holland (Springer 2015,
second edition). This appendix is a free download from
<http://link.springer.com/content/pdf/bbm%3A978-1-4939-2122-5%2F1.pdf>.

For more information, see e.g. David Goldberg (1991), "What Every
Computer Scientist Should Know About Floating-Point Arithmetic", _ACM
Computing Surveys_, **23/1**, 5--48, also available via
<http://www.validlab.com/goldberg/paper.pdf>.

Here is another example, this time using addition:

```r
R> .3 + .6 == .9
[1] FALSE
R> .3 + .6 - .9
[1] -1.110223e-16
R> print(matrix(c(.3,  .6,  .9, .3 + .6)), digits = 18)
                     [,1]
[1,] 0.299999999999999989
[2,] 0.599999999999999978
[3,] 0.900000000000000022
[4,] 0.899999999999999911
```

---

### 7.32 How can I capture or ignore errors in a long simulation?

Use `try()`, which returns an object of class `"try-error"` instead of
an error, or preferably `tryCatch()`, where the return value can be
configured more flexibly. For example

```r
beta[i,] <- tryCatch(coef(lm(formula, data)),
                     error = function(e) rep(NaN, 4))
```

would return the coefficients if the `lm()` call succeeded and would
return `c(NaN, NaN, NaN, NaN)` if it failed (presumably there are
supposed to be 4 coefficients in this example).

---

### 7.33 Why are powers of negative numbers wrong?

You are probably seeing something like

```r
R> -2^2
[1] -4
```

and misunderstanding the precedence rules for expressions in R. Write

```r
R> (-2)^2
[1] 4
```

to get the square of _-2_.

The precedence rules are documented in `?Syntax`, and to see how R
interprets an expression you can look at the parse tree

```r
R> as.list(quote(-2^2))
[[1]]
`-`

[[2]]
2^2
```

---

### 7.34 How can I save the result of each iteration in a loop into a separate file?

One way is to use `paste()` (or `sprintf()`) to concatenate a stem
filename and the iteration number while `file.path()` constructs the
path. For example, to save results into files `result1.rda`,
..., `result100.rda` in the subdirectory `Results` of
the current working directory, one can use

```r
for(i in 1:100) {
  ## Calculations constructing "some_object" ...
  fp <- file.path("Results", paste("result", i, ".rda", sep = ""))
  save(list = "some_object", file = fp)
}
```

---

### 7.35 Why are _p_-values not displayed when using lmer()?

Doug Bates has kindly provided an extensive response in a post to the
r-help list, which can be reviewed at
<https://stat.ethz.ch/pipermail/r-help/2006-May/094765.html>.

---

### 7.36 Why are there unwanted borders, lines or grid-like artifacts when viewing a plot saved to a PS or PDF file?

This can occur when using functions such as `polygon()`,
`filled.contour()`, `image()` or other functions which may call these
internally. In the case of `polygon()`, you may observe unwanted borders
between the polygons even when setting the `border` argument to `NA` or
`"transparent"`.

The source of the problem is the PS/PDF viewer when the plot is
anti-aliased. The details for the solution will be different depending
upon the viewer used, the operating system and may change over time. For
some common viewers, consider the following:

Acrobat Reader (cross platform)

: There are options in Preferences to enable/disable text smoothing,
image smoothing and line art smoothing. Disable line art smoothing.

Preview (macOS)

: There is an option in Preferences to enable/disable anti-aliasing of
text and line art. Disable this option.

GSview (cross platform)

: There are settings for Text Alpha and Graphics Alpha. Change
Graphics Alpha from 4 bits to 1 bit to disable graphic
anti-aliasing.

gv (Unix-like X)

: There is an option to enable/disable anti-aliasing. Disable this
option.

Evince (Linux/GNOME)

: There is not an option to disable anti-aliasing in this viewer.

Okular (Linux/KDE)

: There is not an option in the GUI to enable/disable anti-aliasing.
From a console command line, use:

    ``` r
    $ kwriteconfig --file okularpartrc --group ‘Dlg Performance’ \
                   --key GraphicsAntialias Disabled
    ```

    Then restart Okular. Change the final word to '`Enabled`'
    to restore the original setting.

---

### 7.37 Why does backslash behave strangely inside strings?

This question most often comes up in relation to file names (see [How do
file names work in Windows?](#How-do-file-names-work-in-Windows_003f))
but it also happens that people complain that they cannot seem to put a
single '`\`' character into a text string unless it happens to
be followed by certain other characters.

To understand this, you have to distinguish between character strings
and _representations_ of character strings. Mostly, the representation
in R is just the string with a single or double quote at either end, but
there are strings that cannot be represented that way, e.g., strings
that themselves contain the quote character. So

```r
> str <- "This \"text\" is quoted"
> str
[1] "This \"text\" is quoted"
> cat(str, "\n")
This "text" is quoted
```

The _escape sequences_ '`\"`' and '`\n`' represent a
double quote and the newline character respectively. Printing text
strings, using `print()` or by typing the name at the prompt will use
the escape sequences too, but the `cat()` function will display the
string as-is. Notice that '`"\n"`' is a one-character string,
not two; the backslash is not actually in the string, it is just
generated in the printed representation.

```r
> nchar("\n")
[1] 1
> substring("\n", 1, 1)
[1] "\n"
```

So how do you put a backslash in a string? For this, you have to escape
the escape character. I.e., you have to double the backslash. as in

```r
> cat("\\n", "\n")
\n
```

Some functions, particularly those involving regular expression
matching, themselves use metacharacters, which may need to be escaped by
the backslash mechanism. In those cases you may need a _quadruple_
backslash to represent a single literal one.

In versions of R up to 2.4.1 an unknown escape sequence like
'`\p`' was quietly interpreted as just '`p`'. Current
versions of R emit a warning.

---

### 7.38 How can I put error bars or confidence bands on my plot?

Some functions will display a particular kind of plot with error bars,
such as the `bar.err()` function in the
[**agricolae**](https://CRAN.R-project.org/package=agricolae) package,
the `plotCI()` function in the
[**gplots**](https://CRAN.R-project.org/package=gplots) package, the
`plotCI()` and `brkdn.plot()` functions in the
[**plotrix**](https://CRAN.R-project.org/package=plotrix) package and
the `error.bars()`, `error.crosses()` and `error.bars.by()` functions in
the [**psych**](https://CRAN.R-project.org/package=psych) package.
Within these types of functions, some will accept the measures of
dispersion (e.g., `plotCI`), some will calculate the dispersion measures
from the raw values (`bar.err`, `brkdn.plot`), and some will do both
(`error.bars`). Still other functions will just display error bars, like
the dispersion function in the
[**plotrix**](https://CRAN.R-project.org/package=plotrix) package. Most
of the above functions use the `arrows()` function in the base
**graphics** package to draw the error bars.

The above functions all use the base graphics system. The grid and
lattice graphics systems also have specific functions for displaying
error bars, e.g., the `grid.arrow()` function in the **grid** package,
and the `geom_errorbar()`, `geom_errorbarh()`, `geom_pointrange()`,
`geom_linerange()`, `geom_crossbar()` and `geom_ribbon()` functions in
the [**ggplot2**](https://CRAN.R-project.org/package=ggplot2) package.
In the lattice system, error bars can be displayed with `Dotplot()` or
`xYplot()` in the [**Hmisc**](https://CRAN.R-project.org/package=Hmisc)
package and `segplot()` in the
[**latticeExtra**](https://CRAN.R-project.org/package=latticeExtra)
package.

---

### 7.39 How do I create a plot with two y-axes?

Creating a graph with two y-axes, i.e., with two sorts of data that are
scaled to the same vertical size and showing separate vertical axes on
the left and right sides of the plot that reflect the original scales of
the data, is possible in R but is not recommended. The basic approach
for constructing such graphs is to use `par(new=TRUE)` (see `?par`);
functions `twoord.plot()` (in the
[**plotrix**](https://CRAN.R-project.org/package=plotrix) package) and
`doubleYScale()` (in the
[**latticeExtra**](https://CRAN.R-project.org/package=latticeExtra)
package) automate the process somewhat.

---

### 7.40 How do I access the source code for a function?

In most cases, typing the name of the function will print its source
code. However, code is sometimes hidden in a namespace, or compiled. For
a complete overview on how to access source code, see Uwe Ligges (2006),
"Help Desk: Accessing the sources", _R News_, **6/4**, 43--45
(<https://CRAN.R-project.org/doc/Rnews/Rnews_2006-4.pdf>).

---

### 7.41 Why does summary() report strange results for the R\^2 estimate when I fit a linear model with no intercept?

As described in `?summary.lm`, when the intercept is zero (e.g., from
`y ~ x - 1` or `y ~ x + 0`), `summary.lm()` uses the formula R\^2 = 1 -
Sum(R\[i\]\^2) / Sum((y\[i\])\^2) which is different from the usual R\^2
= 1 - Sum(R\[i\]\^2) / Sum((y\[i\] - mean(y))\^2). There are several
reasons for this:

- Otherwise the _R\^2_ could be negative (because the model with zero
  intercept can fit _worse_ than the constant-mean model it is
  implicitly compared to).
- If you set the slope to zero in the model with a line through the
  origin you get fitted values y\*=0
- The model with constant, non-zero mean is not nested in the model
  with a line through the origin.

All these come down to saying that if you know _a priori_ that
_E\[Y\]=0_ when _x=0_ then the 'null' model that you should compare to
the fitted line, the model where _x_ doesn't explain any of the
variance, is the model where _E\[Y\]=0_ everywhere. (If you don't know a
priori that _E\[Y\]=0_ when _x=0_, then you probably shouldn't be
fitting a line through the origin.)

---

### 7.42 Why is R apparently not releasing memory?

This question is often asked in different flavors along the lines of "I
have removed objects in R and run `gc()` and yet `ps`/`top` still shows
the R process using a lot of memory", often on Linux machines.

This is an artifact of the way the operating system (OS) allocates
memory. In general it is common that the OS is not capable of releasing
all unused memory. In extreme cases it is possible that even if R frees
almost all its memory, the OS can not release any of it due to its
design and thus tools such as `ps` or `top` will report substantial
amount of resident RAM used by the R process even though R has released
all that memory. In general such tools do _not_ report the actual memory
usage of the process but rather what the OS is reserving for that
process.

The short answer is that this is a limitation of the memory allocator in
the operating system and there is nothing R can do about it. That space
is simply kept by the OS in the hope that R will ask for it later. The
following paragraph gives more in-depth answer with technical details on
how this happens.

Most systems use two separate ways to allocate memory. For allocation of
large chunks they will use `mmap` to map memory into the process address
space. Such chunks can be released immediately when they are completely
free, because they can reside anywhere in the virtual memory. However,
this is a relatively expensive operation and many OSes have a limit on
the number of such allocated chunks, so this is only used for allocating
large memory regions. For smaller allocations the system can expand the
data segment of the process (historically using the `brk` system call),
but this whole area is always contiguous. The OS can only move the end
of this space, it cannot create any "holes". Since this operation is
fairly cheap, it is used for allocations of small pieces of memory.
However, the side-effect is that even if there is just one byte that is
in use at the end of the data segment, the OS cannot release any memory
at all, because it cannot change the address of that byte. This is
actually more common than it may seem, because allocating a lot of
intermediate objects, then allocating a result object and removing all
intermediate objects is a very common practice. Since the result is
allocated at the end it will prevent the OS from releasing any memory
used by the intermediate objects. In practice, this is not necessarily a
problem, because modern operating systems can page out unused portions
of the virtual memory so it does not necessarily reduce the amount of
real memory available for other applications. Typically, small objects
such as strings or pairlists will be affected by this behavior, whereas
large objects such as long vectors will be allocated using `mmap` and
thus not affected. On Linux (and possibly other Unix-like systems) it is
possible to use the `mallinfo` system call (also see the
[mallinfo](https://rforge.net/mallinfo) package) to query the allocator
about the layout of the allocations, including the actually used memory
as well as unused memory that cannot be released.

---

### 7.43 How can I enable secure https downloads in R?

When R transfers files over HTTP (e.g., using the `install.packages()`
or `download.file()` function), a download method is chosen based on the
`download.file.method` option. There are several methods
available and the default behavior if no option is explicitly specified
is to use R's internal HTTP implementation. In most circumstances this
internal method will not support HTTPS URLs so you will need to override
the default: this is done automatically for such URLs as from R 3.2.2.

R versions 3.2.0 and greater include two download methods (`"libcurl"`
and `"wininet"`) that both support HTTPS connections: we recommend that
you use these methods. The requisite code to add to `.Rprofile`
or `Rprofile.site` is:

```r
options(download.file.method = "wininet", url.method = "wininet")
(Windows)
options(download.file.method = "libcurl", url.method = "libcurl")
(Linux and macOS)
```

(Method `"wininet"` is the default on Windows as from R 3.2.2.)

Note that the `"libcurl"` method may or may not have been compiled in.
In the case that it was not, i.e. `capabilities("libcurl") == FALSE`, we
recommend method `"wget"` on Linux and `"curl"` on macOS. It is possible
that system versions of `"libcurl"`, `wget` or `curl` may have been
compiled without HTTPS support, but this is unlikely. As from R 3.3.0
`"libcurl"` with HTTPS support is required except on Windows.

---

### 7.44 How can I get CRAN package binaries for outdated versions of R?

Since March 2016, Windows and macOS binaries of CRAN packages for old
versions of R (released more than 5 years ago) are made available from a
central CRAN archive server instead of the CRAN mirrors. To get these,
one should set the CRAN "mirror" element of the `repos` option
accordingly, by something like

```r
local({r <- getOption("repos")
       r["CRAN"] <- "http://CRAN-archive.R-project.org"
       options(repos = r)
      })
```

(see `?options` for more information).

---
