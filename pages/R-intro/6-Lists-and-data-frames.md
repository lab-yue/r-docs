6 Lists and data frames

---

---

• [Lists](#Lists)     
 • [Constructing and modifying lists](#Constructing-and-modifying-lists)     
 • [Data frames](#Data-frames)

---

---

### 6.1 Lists

An R _list_ is an object consisting of an ordered collection of objects
known as its _components_.

There is no particular need for the components to be of the same mode or
type, and, for example, a list could consist of a numeric vector, a
logical value, a matrix, a complex vector, a character array, a
function, and so on. Here is a simple example of how to make a list:

```r
> Lst <- list(name="Fred", wife="Mary", no.children=3,
              child.ages=c(4,7,9))
```

Components are always _numbered_ and may always be referred to as such.
Thus if `Lst` is the name of a list with four components, these may be
individually referred to as `Lst[[1]]`, `Lst[[2]]`, `Lst[[3]]` and
`Lst[[4]]`. If, further, `Lst[[4]]` is a vector subscripted array then
`Lst[[4]][1]` is its first entry.

If `Lst` is a list, then the function `length(Lst)` gives the number of
(top level) components it has.

Components of lists may also be _named_, and in this case the component
may be referred to either by giving the component name as a character
string in place of the number in double square brackets, or, more
conveniently, by giving an expression of the form

```r
> name$component_name
```

for the same thing.

This is a very useful convention as it makes it easier to get the right
component if you forget the number.

So in the simple example given above:

`Lst$name` is the same as `Lst[[1]]` and is the string `"Fred"`,

`Lst$wife` is the same as `Lst[[2]]` and is the string `"Mary"`,

`Lst$child.ages[1]` is the same as `Lst[[4]][1]` and is the number `4`.

Additionally, one can also use the names of the list components in
double square brackets, i.e., `Lst[["name"]]` is the same as `Lst$name`.
This is especially useful, when the name of the component to be
extracted is stored in another variable as in

```r
> x <- "name"; Lst[[x]]
```

It is very important to distinguish `Lst[[1]]` from `Lst[1]`.
'`[[…]]`' is the operator used to select a single element,
whereas '`[…]`' is a general subscripting operator. Thus the
former is the _first object in the list_ `Lst`, and if it is a named
list the name is _not_ included. The latter is a _sublist of the list
`Lst` consisting of the first entry only. If it is a named list, the
names are transferred to the sublist._

The names of components may be abbreviated down to the minimum number of
letters needed to identify them uniquely. Thus `Lst$coefficients` may be
minimally specified as `Lst$coe` and `Lst$covariance` as `Lst$cov`.

The vector of names is in fact simply an attribute of the list like any
other and may be handled as such. Other structures besides lists may, of
course, similarly be given a _names_ attribute also.

---

### 6.2 Constructing and modifying lists

New lists may be formed from existing objects by the function `list()`.
An assignment of the form

```r
> Lst <- list(name_1=object_1, …, name_m=object_m)
```

sets up a list `Lst` of _m_ components using `object_1`{.variable}, ...,
`object_m`{.variable} for the components and giving them names as
specified by the argument names, (which can be freely chosen). If these
names are omitted, the components are numbered only. The components used
to form the list are _copied_ when forming the new list and the
originals are not affected.

Lists, like any subscripted object, can be extended by specifying
additional components. For example

```r
> Lst[5] <- list(matrix=Mat)
```

---

• [Concatenating lists](#Concatenating-lists)

---

---

#### 6.2.1 Concatenating lists

When the concatenation function `c()` is given list arguments, the
result is an object of mode list also, whose components are those of the
argument lists joined together in sequence.

```r
> list.ABC <- c(list.A, list.B, list.C)
```

Recall that with vector objects as arguments the concatenation function
similarly joined together all arguments into a single vector structure.
In this case all other attributes, such as `dim` attributes, are
discarded.

---

### 6.3 Data frames

A _data frame_ is a list with class `"data.frame"`. There are
restrictions on lists that may be made into data frames, namely

- The components must be vectors (numeric, character, or logical),
  factors, numeric matrices, lists, or other data frames.
- Matrices, lists, and data frames provide as many variables to the
  new data frame as they have columns, elements, or variables,
  respectively.
- Numeric vectors, logicals and factors are included as is, and by
  default[^18^](#FOOT18) character vectors are coerced to be
  factors, whose levels are the unique values appearing in the vector.
- Vector structures appearing as variables of the data frame must all
  have the _same length_, and matrix structures must all have the same
  _row size_.

A data frame may for many purposes be regarded as a matrix with columns
possibly of differing modes and attributes. It may be displayed in
matrix form, and its rows and columns extracted using matrix indexing
conventions.

---

• [Making data frames](#Making-data-frames)     
 • [attach() and detach()](#attach_0028_0029-and-detach_0028_0029)     
 • [Working with data frames](#Working-with-data-frames)     
 • [Attaching arbitrary lists](#Attaching-arbitrary-lists)     
 • [Managing the search path](#Managing-the-search-path)

---

---

#### 6.3.1 Making data frames

Objects satisfying the restrictions placed on the columns (components)
of a data frame may be used to form one using the function `data.frame`:

```r
> accountants <- data.frame(home=statef, loot=incomes, shot=incomef)
```

A list whose components conform to the restrictions of a data frame may
be _coerced_ into a data frame using the function `as.data.frame()`

The simplest way to construct a data frame from scratch is to use the
`read.table()` function to read an entire data frame from an external
file. This is discussed further in [Reading data from files](#Reading-data-from-files).

---

#### 6.3.2 `attach()` and `detach()`

The `$` notation, such as `accountants$home`, for list components is not
always very convenient. A useful facility would be somehow to make the
components of a list or data frame temporarily visible as variables
under their component name, without the need to quote the list name
explicitly each time.

The `attach()` function takes a 'database' such as a list or data frame
as its argument. Thus suppose `lentils` is a data frame with three
variables `lentils$u`, `lentils$v`, `lentils$w`. The attach

```r
> attach(lentils)
```

places the data frame in the search path at position 2, and provided
there are no variables `u`, `v` or `w` in position 1, `u`, `v` and `w`
are available as variables from the data frame in their own right. At
this point an assignment such as

```r
> u <- v+w
```

does not replace the component `u` of the data frame, but rather masks
it with another variable `u` in the working directory at position 1 on
the search path. To make a permanent change to the data frame itself,
the simplest way is to resort once again to the `$` notation:

```r
> lentils$u <- v+w
```

However the new value of component `u` is not visible until the data
frame is detached and attached again.

To detach a data frame, use the function

```r
> detach()
```

More precisely, this statement detaches from the search path the entity
currently at position 2. Thus in the present context the variables `u`,
`v` and `w` would be no longer visible, except under the list notation
as `lentils$u` and so on. Entities at positions greater than 2 on the
search path can be detached by giving their number to `detach`, but it
is much safer to always use a name, for example by `detach(lentils)` or
`detach("lentils")`

> **Note:** In R lists and data frames can only be attached at position
> 2 or above, and what is attached is a _copy_ of the original object.
> You can alter the attached values _via_ `assign`, but the original
> list or data frame is unchanged.

---

#### 6.3.3 Working with data frames

A useful convention that allows you to work with many different problems
comfortably together in the same working directory is

- gather together all variables for any well defined and separate
  problem in a data frame under a suitably informative name;
- when working with a problem attach the appropriate data frame at
  position 2, and use the working directory at level 1 for operational
  quantities and temporary variables;
- before leaving a problem, add any variables you wish to keep for
  future reference to the data frame using the `$` form of assignment,
  and then `detach()`;
- finally remove all unwanted variables from the working directory and
  keep it as clean of left-over temporary variables as possible.

In this way it is quite simple to work with many problems in the same
directory, all of which have variables named `x`, `y` and `z`, for
example.

---

#### 6.3.4 Attaching arbitrary lists

`attach()` is a generic function that allows not only directories and
data frames to be attached to the search path, but other classes of
object as well. In particular any object of mode `"list"` may be
attached in the same way:

```r
> attach(any.old.list)
```

Anything that has been attached can be detached by `detach`, by position
number or, preferably, by name.

---

#### 6.3.5 Managing the search path

The function `search` shows the current search path and so is a very
useful way to keep track of which data frames and lists (and packages)
have been attached and detached. Initially it gives

```r
> search()
[1] ".GlobalEnv"   "Autoloads"    "package:base"
```

where `.GlobalEnv` is the workspace.[^19^](#FOOT19)

After `lentils` is attached we have

```r
> search()
[1] ".GlobalEnv"   "lentils"      "Autoloads"    "package:base"
> ls(2)
[1] "u" "v" "w"
```

and as we see `ls` (or `objects`) can be used to examine the contents of
any position on the search path.

Finally, we detach the data frame and confirm it has been removed from
the search path.

```r
> detach("lentils")
> search()
[1] ".GlobalEnv"   "Autoloads"    "package:base"
```

---
