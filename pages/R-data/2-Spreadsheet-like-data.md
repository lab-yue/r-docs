# 2 Spreadsheet-like data

---

---

• [Variations on read.table](#Variations-on-read_002etable)     
 • [Fixed-width-format files](#Fixed_002dwidth_002dformat-files)     
 • [Data Interchange Format (DIF)](#Data-Interchange-Format-_0028DIF_0029)     
 • [Using scan directly](#Using-scan-directly)     
 • [Re-shaping data](#Re_002dshaping-data)     
 • [Flat contingency tables](#Flat-contingency-tables)

---

In [Export to text files](#Export-to-text-files) we saw a number of
variations on the format of a spreadsheet-like text file, in which the
data are presented in a rectangular grid, possibly with row and column
labels. In this section we consider importing such files into R.

---

### 2.1 Variations on `read.table`

The function `read.table` is the most convenient way to read in a
rectangular grid of data. Because of the many possibilities, there are
several other functions that call `read.table` but change a group of
default arguments.

Beware that `read.table` is an inefficient way to read in very large
numerical matrices: see `scan` below.

Some of the issues to consider are:

1.  **Encoding**

    If the file contains non-ASCII character fields, ensure that it is
    read in the correct encoding. This is mainly an issue for reading
    Latin-1 files in a UTF-8 locale, which can be done by something like

    ```r
    read.table("file.dat", fileEncoding="latin1")
    ```

    Note that this will work in any locale which can represent Latin-1
    strings, but not many Greek/Russian/Chinese/Japanese ... locales.

2.  **Header line**

    We recommend that you specify the `header` argument explicitly,
    Conventionally the header line has entries only for the columns and
    not for the row labels, so is one field shorter than the remaining
    lines. (If R sees this, it sets `header = TRUE`.) If presented with
    a file that has a (possibly empty) header field for the row labels,
    read it in by something like

    ```r
    read.table("file.dat", header = TRUE, row.names = 1)
    ```

    Column names can be given explicitly via the `col.names`; explicit
    names override the header line (if present).

3.  **Separator**

    Normally looking at the file will determine the field separator to
    be used, but with white-space separated files there may be a choice
    between the default `sep = ""` which uses any white space (spaces,
    tabs or newlines) as a separator, `sep = " "` and `sep = "\t"`. Note
    that the choice of separator affects the input of quoted strings.

    If you have a tab-delimited file containing empty fields be sure to
    use `sep = "\t"`.

4.  **Quoting**

    By default character strings can be quoted by either '`"`'
    or '`'`', and in each case all the characters up to a
    matching quote are taken as part of the character string. The set of
    valid quoting characters (which might be none) is controlled by the
    `quote` argument. For `sep = "\n"` the default is changed to
    `quote = ""`.

    If no separator character is specified, quotes can be escaped within
    quoted strings by immediately preceding them by '`\`',
    C-style.

    If a separator character is specified, quotes can be escaped within
    quoted strings by doubling them as is conventional in spreadsheets.
    For example

    ```r
    'One string isn''t two',"one more"
    ```

    can be read by

    ```r
    read.table("testfile", sep = ",")
    ```

    This does not work with the default separator.

5.  **Missing values**

    By default the file is assumed to contain the character string `NA`
    to represent missing values, but this can be changed by the argument
    `na.strings`, which is a vector of one or more character
    representations of missing values.

    Empty fields in numeric columns are also regarded as missing values.

    In numeric columns, the values `NaN`, `Inf` and `-Inf` are accepted.

6.  **Unfilled lines**

    It is quite common for a file exported from a spreadsheet to have
    all trailing empty fields (and their separators) omitted. To read
    such files set `fill = TRUE`.

7.  **White space in character fields**

    If a separator is specified, leading and trailing white space in
    character fields is regarded as part of the field. To strip the
    space, use argument `strip.white = TRUE`.

8.  **Blank lines**

    By default, `read.table` ignores empty lines. This can be changed by
    setting `blank.lines.skip = FALSE`, which will only be useful in
    conjunction with `fill = TRUE`, perhaps to use blank rows to
    indicate missing cases in a regular layout.

9.  **Classes for the variables**

    Unless you take any special action, `read.table` reads all the
    columns as character vectors and then tries to select a suitable
    class for each variable in the data frame. It tries in turn
    `logical`, `integer`, `numeric` and `complex`, moving on if any
    entry is not missing and cannot be converted.[^3^](#FOOT3)
    If all of these fail, the variable is converted to a factor.

    Arguments `colClasses` and `as.is` provide greater control.
    Specifying `as.is = TRUE` suppresses conversion of character vectors
    to factors (only). Using `colClasses` allows the desired class to be
    set for each column in the input: it will be faster and use less
    memory.

    Note that `colClasses` and `as.is` are specified _per_ column, not
    _per_ variable, and so include the column of row names (if any).

10. **Comments**

    By default, `read.table` uses '`#`' as a comment character,
    and if this is encountered (except in quoted strings) the rest of
    the line is ignored. Lines containing only white space and a comment
    are treated as blank lines.

    If it is known that there will be no comments in the data file, it
    is safer (and may be faster) to use `comment.char = ""`.

11. **Escapes**

    Many OSes have conventions for using backslash as an escape
    character in text files, but Windows does not (and uses backslash in
    path names). It is optional in R whether such conventions are
    applied to data files.

    Both `read.table` and `scan` have a logical argument `allowEscapes`.
    This is false by default, and backslashes are then only interpreted
    as (under circumstances described above) escaping quotes. If this
    set to be true, C-style escapes are interpreted, namely the control
    characters `\a, \b, \f, \n, \r, \t, \v` and octal and hexadecimal
    representations like `\040` and `\0x2A`. Any other escaped character
    is treated as itself, including backslash. Note that Unicode escapes
    such as `\uxxxx` are never interpreted.

12. **Encoding**

    This can be specified by the `fileEncoding` argument, for example

    ```r
    fileEncoding = "UCS-2LE"    # Windows ‘Unicode’ files
    fileEncoding = "UTF-8"
    ```

    If you know (correctly) the file's encoding this will almost always
    work. However, we know of one exception, UTF-8 files with a BOM.
    Some people claim that UTF-8 files should never have a BOM, but some
    software (apparently including Excel:mac) uses them, and many
    Unix-alike OSes do not accept them. So faced with a file which
    `file` reports as

    ```r
    intro.dat: UTF-8 Unicode (with BOM) text
    ```

    it can be read on Windows by

    ```r
    read.table("intro.dat", fileEncoding = "UTF-8")
    ```

    but on a Unix-alike might need

    ```r
    read.table("intro.dat", fileEncoding = "UTF-8-BOM")
    ```

    (This would most likely work without specifying an encoding in a
    UTF-8 locale.)

Convenience functions `read.csv` and `read.delim` provide arguments to
`read.table` appropriate for CSV and tab-delimited files exported from
spreadsheets in English-speaking locales. The variations `read.csv2` and
`read.delim2` are appropriate for use in those locales where the comma
is used for the decimal point and (for `read.csv2`) for spreadsheets
which use semicolons to separate fields.

If the options to `read.table` are specified incorrectly, the error
message will usually be of the form

```r
Error in scan(file = file, what = what, sep = sep, :
        line 1 did not have 5 elements
```

or

```r
Error in read.table("files.dat", header = TRUE) :
        more columns than column names
```

This may give enough information to find the problem, but the auxiliary
function `count.fields` can be useful to investigate further.

Efficiency can be important when reading large data grids. It will help
to specify `comment.char = ""`, `colClasses` as one of the atomic vector
types (logical, integer, numeric, complex, character or perhaps raw) for
each column, and to give `nrows`, the number of rows to be read (and a
mild over-estimate is better than not specifying this at all). See the
examples in later sections.

---

### 2.2 Fixed-width-format files

Sometimes data files have no field delimiters but have fields in
pre-specified columns. This was very common in the days of punched
cards, and is still sometimes used to save file space.

Function `read.fwf` provides a simple way to read such files, specifying
a vector of field widths. The function reads the file into memory as
whole lines, splits the resulting character strings, writes out a
temporary tab-separated file and then calls `read.table`. This is
adequate for small files, but for anything more complicated we recommend
using the facilities of a language like `perl` to pre-process the file.

Function `read.fortran` is a similar function for fixed-format files,
using Fortran-style column specifications.

---

### 2.3 Data Interchange Format (DIF)

An old format sometimes used for spreadsheet-like data is DIF, or Data
Interchange format.

Function `read.DIF` provides a simple way to read such files. It takes
arguments similar to `read.table` for assigning types to each of the
columns.

On Windows, spreadsheet programs often store spreadsheet data copied to
the clipboard in this format; `read.DIF("clipboard")` can read it from
there directly. It is slightly more robust than
`read.table("clipboard")` in handling spreadsheets with empty cells.

---

### 2.4 Using `scan` directly

Both `read.table` and `read.fwf` use `scan` to read the file, and then
process the results of `scan`. They are very convenient, but sometimes
it is better to use `scan` directly.

Function `scan` has many arguments, most of which we have already
covered under `read.table`. The most crucial argument is `what`, which
specifies a list of modes of variables to be read from the file. If the
list is named, the names are used for the components of the returned
list. Modes can be numeric, character or complex, and are usually
specified by an example, e.g. `0`, `""` or `0i`. For example

```r
cat("2 3 5 7", "11 13 17 19", file="ex.dat", sep="\n")
scan(file="ex.dat", what=list(x=0, y="", z=0), flush=TRUE)
```

returns a list with three components and discards the fourth column in
the file.

There is a function `readLines` which will be more convenient if all you
want is to read whole lines into R for further processing.

One common use of `scan` is to read in a large matrix. Suppose file
`matrix.dat` just contains the numbers for a 200 x 2000 matrix.
Then we can use

```r
A <- matrix(scan("matrix.dat", n = 200*2000), 200, 2000, byrow = TRUE)
```

On one test this took 1 second (under Linux, 3 seconds under Windows on
the same machine) whereas

```r
A <- as.matrix(read.table("matrix.dat"))
```

took 10 seconds (and more memory), and

```r
A <- as.matrix(read.table("matrix.dat", header = FALSE, nrows = 200,
                          comment.char = "", colClasses = "numeric"))
```

took 7 seconds. The difference is almost entirely due to the overhead of
reading 2000 separate short columns: were they of length 2000, `scan`
took 9 seconds whereas `read.table` took 18 if used efficiently (in
particular, specifying `colClasses`) and 125 if used naively.

Note that timings can depend on the type read and the data. Consider
reading a million distinct integers:

```r
writeLines(as.character((1+1e6):2e6), "ints.dat")
xi <- scan("ints.dat", what=integer(0), n=1e6)   # 0.77s
xn <- scan("ints.dat", what=numeric(0), n=1e6)   # 0.93s
xc <- scan("ints.dat", what=character(0), n=1e6) # 0.85s
xf <- as.factor(xc)                              # 2.2s
DF <- read.table("ints.dat")                     # 4.5s
```

and a million examples of a small set of codes:

```r
code <- c("LMH", "SJC", "CHCH", "SPC", "SOM")
writeLines(sample(code, 1e6, replace=TRUE), "code.dat")
y <- scan("code.dat", what=character(0), n=1e6)  # 0.44s
yf <- as.factor(y)                               # 0.21s
DF <- read.table("code.dat")                     # 4.9s
DF <- read.table("code.dat", nrows=1e6)          # 3.6s
```

Note that these timings depend heavily on the operating system (the
basic reads in Windows take at least as twice as long as these Linux
times) and on the precise state of the garbage collector.

---

### 2.5 Re-shaping data

Sometimes spreadsheet data is in a compact format that gives the
covariates for each subject followed by all the observations on that
subject. R's modelling functions need observations in a single column.
Consider the following sample of data from repeated MRI brain
measurements

```r
 Status   Age    V1     V2     V3    V4
      P 23646 45190  50333  55166 56271
     CC 26174 35535  38227  37911 41184
     CC 27723 25691  25712  26144 26398
     CC 27193 30949  29693  29754 30772
     CC 24370 50542  51966  54341 54273
     CC 28359 58591  58803  59435 61292
     CC 25136 45801  45389  47197 47126
```

There are two covariates and up to four measurements on each subject.
The data were exported from Excel as a file `mr.csv`.

We can use `stack` to help manipulate these data to give a single
response.

```r
zz <- read.csv("mr.csv", strip.white = TRUE)
zzz <- cbind(zz[gl(nrow(zz), 1, 4*nrow(zz)), 1:2], stack(zz[, 3:6]))
```

with result

```r
      Status   Age values ind
X1         P 23646  45190  V1
X2        CC 26174  35535  V1
X3        CC 27723  25691  V1
X4        CC 27193  30949  V1
X5        CC 24370  50542  V1
X6        CC 28359  58591  V1
X7        CC 25136  45801  V1
X11        P 23646  50333  V2
...
```

Function `unstack` goes in the opposite direction, and may be useful for
exporting data.

Another way to do this is to use the function `reshape`, by

```r
> reshape(zz, idvar="id",timevar="var",
  varying=list(c("V1","V2","V3","V4")),direction="long")
    Status   Age var    V1 id
1.1      P 23646   1 45190  1
2.1     CC 26174   1 35535  2
3.1     CC 27723   1 25691  3
4.1     CC 27193   1 30949  4
5.1     CC 24370   1 50542  5
6.1     CC 28359   1 58591  6
7.1     CC 25136   1 45801  7
1.2      P 23646   2 50333  1
2.2     CC 26174   2 38227  2
...
```

The `reshape` function has a more complicated syntax than `stack` but
can be used for data where the 'long' form has more than the one column
in this example. With `direction="wide"`, `reshape` can also perform the
opposite transformation.

Some people prefer the tools in packages
[**reshape**](https://CRAN.R-project.org/package=reshape),
[**reshape2**](https://CRAN.R-project.org/package=reshape2) and
[**plyr**](https://CRAN.R-project.org/package=plyr).

---

### 2.6 Flat contingency tables

Displaying higher-dimensional contingency tables in array form typically
is rather inconvenient. In categorical data analysis, such information
is often represented in the form of bordered two-dimensional arrays with
leading rows and columns specifying the combination of factor levels
corresponding to the cell counts. These rows and columns are typically
"ragged" in the sense that labels are only displayed when they change,
with the obvious convention that rows are read from top to bottom and
columns are read from left to right. In R, such "flat" contingency
tables can be created using `ftable`, which creates
objects of class `"ftable"` with an appropriate print method.

As a simple example, consider the R standard data set `UCBAdmissions`
which is a 3-dimensional contingency table resulting from classifying
applicants to graduate school at UC Berkeley for the six largest
departments in 1973 classified by admission and sex.

```r
> data(UCBAdmissions)
> ftable(UCBAdmissions)
                Dept   A   B   C   D   E   F
Admit    Gender
Admitted Male        512 353 120 138  53  22
         Female       89  17 202 131  94  24
Rejected Male        313 207 205 279 138 351
         Female       19   8 391 244 299 317
```

The printed representation is clearly more useful than displaying the
data as a 3-dimensional array.

There is also a function `read.ftable` for reading in flat-like
contingency tables from files. This has
additional arguments for dealing with variants on how exactly the
information on row and column variables names and levels is represented.
The help page for `read.ftable` has some useful examples. The flat
tables can be converted to standard contingency tables in array form
using `as.table`.

Note that flat tables are characterized by their "ragged" display of row
(and maybe also column) labels. If the full grid of levels of the row
variables is given, one should instead use `read.table` to read in the
data, and create the contingency table from this using `xtabs`.

---
