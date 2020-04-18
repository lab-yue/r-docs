7 Reading data from files

---

Large data objects will usually be read as values from external files
rather than entered during an R session at the keyboard. R input
facilities are simple and their requirements are fairly strict and even
rather inflexible. There is a clear presumption by the designers of R
that you will be able to modify your input files using other tools, such
as file editors or Perl[^20^](#FOOT20) to fit in with the
requirements of R. Generally this is very simple.

If variables are to be held mainly in data frames, as we strongly
suggest they should be, an entire data frame can be read directly with
the `read.table()` function. There is also a more primitive input
function, `scan()`, that can be called directly.

For more details on importing data into R and also exporting data, see
the _R Data Import/Export_ manual.

---

• [The read.table() function](#The-read_002etable_0028_0029-function)     
 • [The scan() function](#The-scan_0028_0029-function)     
 • [Accessing builtin datasets](#Accessing-builtin-datasets)     
 • [Editing data](#Editing-data)

---

---

### 7.1 The `read.table()` function

To read an entire data frame directly, the external file will normally
have a special form.

- The first line of the file should have a _name_ for each variable in
  the data frame.
- Each additional line of the file has as its first item a _row label_
  and the values for each variable.

If the file has one fewer item in its first line than in its second,
this arrangement is presumed to be in force. So the first few lines of a
file to be read as a data frame might look as follows.

> +-----------------------------------------------------------------------+
> | |
> | `r | | Input file form with names and row labels: | | | | Price Floor Area Rooms Age Cent.heat | | 01 52.00 111.0 830 5 6.2 no | | 02 54.75 128.0 710 5 7.5 no | | 03 57.50 101.0 1000 5 4.2 no | | 04 57.50 131.0 690 6 8.8 no | | 05 59.75 93.0 900 5 1.9 yes | | ... | |` |
> | ::: |
> +-----------------------------------------------------------------------+

By default numeric items (except row labels) are read as numeric
variables and non-numeric variables, such as `Cent.heat` in the example,
as factors. This can be changed if necessary.

The function `read.table()` can then be used to read the data frame
directly

```r
> HousePrice <- read.table("houses.data")
```

Often you will want to omit including the row labels directly and use
the default labels. In this case the file may omit the row label column
as in the following.

> +-----------------------------------------------------------------------+
> | |
> | `r | | Input file form without row labels: | | | | Price Floor Area Rooms Age Cent.heat | | 52.00 111.0 830 5 6.2 no | | 54.75 128.0 710 5 7.5 no | | 57.50 101.0 1000 5 4.2 no | | 57.50 131.0 690 6 8.8 no | | 59.75 93.0 900 5 1.9 yes | | ... | |` |
> | ::: |
> +-----------------------------------------------------------------------+

The data frame may then be read as

```r
> HousePrice <- read.table("houses.data", header=TRUE)
```

where the `header=TRUE` option specifies that the first line is a line
of headings, and hence, by implication from the form of the file, that
no explicit row labels are given.

---

• [The scan() function](#The-scan_0028_0029-function)

---

---

### 7.2 The `scan()` function

Suppose the data vectors are of equal length and are to be read in
parallel. Further suppose that there are three vectors, the first of
mode character and the remaining two of mode numeric, and the file is
`input.dat`. The first step is to use `scan()` to read in the
three vectors as a list, as follows

```r
> inp <- scan("input.dat", list("",0,0))
```

The second argument is a dummy list structure that establishes the mode
of the three vectors to be read. The result, held in `inp`, is a list
whose components are the three vectors read in. To separate the data
items into three separate vectors, use assignments like

```r
> label <- inp[[1]]; x <- inp[[2]]; y <- inp[[3]]
```

More conveniently, the dummy list can have named components, in which
case the names can be used to access the vectors read in. For example

```r
> inp <- scan("input.dat", list(id="", x=0, y=0))
```

If you wish to access the variables separately they may either be
re-assigned to variables in the working frame:

```r
> label <- inp$id; x <- inp$x; y <- inp$y
```

or the list may be attached at position 2 of the search path (see
[Attaching arbitrary lists](#Attaching-arbitrary-lists)).

If the second argument is a single value and not a list, a single vector
is read in, all components of which must be of the same mode as the
dummy value.

```r
> X <- matrix(scan("light.dat", 0), ncol=5, byrow=TRUE)
```

There are more elaborate input facilities available and these are
detailed in the manuals.

---

### 7.3 Accessing builtin datasets

Around 100 datasets are supplied with R (in package **datasets**), and
others are available in packages (including the recommended packages
supplied with R). To see the list of datasets currently available use

```r
data()
```

All the datasets supplied with R are available directly by name.
However, many packages still use the obsolete convention in which `data`
was also used to load datasets into R, for example

```r
data(infert)
```

and this can still be used with the standard packages (as in this
example). In most cases this will load an R object of the same name.
However, in a few cases it loads several objects, so see the on-line
help for the object to see what to expect.

#### 7.3.1 Loading data from other R packages

To access data from a particular package, use the `package` argument,
for example

```r
data(package="rpart")
data(Puromycin, package="datasets")
```

If a package has been attached by `library`, its datasets are
automatically included in the search.

User-contributed packages can be a rich source of datasets.

---

### 7.4 Editing data

When invoked on a data frame or matrix, `edit` brings up a separate
spreadsheet-like environment for editing. This is useful for making
small changes once a data set has been read. The command

```r
> xnew <- edit(xold)
```

will allow you to edit your data set `xold`, and on completion the
changed object is assigned to `xnew`. If you want to alter the original
dataset `xold`, the simplest way is to use `fix(xold)`, which is
equivalent to `xold <- edit(xold)`.

Use

```r
> xnew <- edit(data.frame())
```

to enter new data via the spreadsheet interface.

---
