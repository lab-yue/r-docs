3 Importing from other statistical systems

---

In this chapter we consider the problem of reading a binary data file
written by another statistical system. This is often best avoided, but
may be unavoidable if the originating system is not available.

In all cases the facilities described were written for data files from
specific versions of the other system (often in the early 2000s), and
have not necessarily been updated for the most recent versions of the
other system.

---

• [EpiInfo Minitab SAS S-PLUS SPSS Stata Systat](#EpiInfo-Minitab-SAS-S_002dPLUS-SPSS-Stata-Systat)     
 • [Octave](#Octave)

---

---

### 3.1 EpiInfo, Minitab, S-PLUS, SAS, SPSS, Stata, Systat

The recommended package
[**foreign**](https://CRAN.R-project.org/package=foreign) provides
import facilities for files produced by these statistical systems, and
for export to Stata. In some cases these functions may require
substantially less memory than `read.table` would. `write.foreign` (See
[Export to text files](#Export-to-text-files)) provides an export
mechanism with support currently for `SAS`, `SPSS` and `Stata`.

EpiInfo versions 5 and 6 stored data in a self-describing fixed-width
text format. `read.epiinfo` will read these `.REC` files into
an R data frame. EpiData also produces data in this format.

Function `read.mtp` imports a 'Minitab Portable Worksheet'. This returns
the components of the worksheet as an R list.

Function `read.xport` reads a file in SAS Transport (XPORT) format and
return a list of data frames. If SAS is available on your system,
function `read.ssd` can be used to create and run a SAS script that
saves a SAS permanent dataset (`.ssd` or `.sas7bdat`)
in Transport format. It then calls `read.xport` to read the resulting
file. (Package [**Hmisc**](https://CRAN.R-project.org/package=Hmisc) has
a similar function `sas.get`, also running SAS.) For those without
access to SAS but running on Windows, the SAS System Viewer (a zero-cost
download) can be used to open SAS datasets and export them to e.g.
`.csv` format.

Function `read.S` which can read binary objects produced by S-PLUS 3.x,
4.x or 2000 on (32-bit) Unix or Windows (and can read them on a
different OS). This is able to read many but not all S objects: in
particular it can read vectors, matrices and data frames and lists
containing those.

Function `data.restore` reads S-PLUS data dumps (created by `data.dump`)
with the same restrictions (except that dumps from the Alpha platform
can also be read). It should be possible to read data dumps from S-PLUS
5.x and later written with `data.dump(oldStyle=T)`.

If you have access to S-PLUS, it is usually more reliable to `dump` the
object(s) in S-PLUS and `source` the dump file in R. For S-PLUS 5.x and
later you may need to use `dump(..., oldStyle=T)`, and to read in very
large objects it may be preferable to use the dump file as a batch
script rather than use the `source` function.

Function `read.spss` can read files created by the 'save' and 'export'
commands in SPSS. It returns a list with one component for each variable
in the saved data set. SPSS variables with value labels are optionally
converted to R factors.

SPSS Data Entry is an application for creating data entry forms. By
default it creates data files with extra formatting information that
`read.spss` cannot handle, but it is possible to export the data in an
ordinary SPSS format.

Some third-party applications claim to produce data 'in SPSS format' but
with differences in the formats: `read.spss` may or may not be able to
handle these.

Stata `.dta` files are a binary file format. Files from
versions 5 up to 12 of Stata can be read and written by functions
`read.dta` and `write.dta`. Stata variables with value labels are
optionally converted to (and from) R factors. For Stata versions 13 and
later see CRAN packages
[**readstata13**](https://CRAN.R-project.org/package=readstata13) and
[**haven**](https://CRAN.R-project.org/package=haven).

`read.systat` reads those Systat `SAVE` files that are rectangular data
files (`mtype = 1`) written on little-endian machines (such as from
Windows). These have extension `.sys` or (more recently)
`.syd`.

---

### 3.2 Octave

Octave is a numerical linear algebra system (<http://www.octave.org>),
and function `read.octave` in package
[**foreign**](https://CRAN.R-project.org/package=foreign) can read in
files in Octave text data format created using the Octave command
`save -ascii`, with support for most of the common types of variables,
including the standard atomic (real and complex scalars, matrices, and
_N_-d arrays, strings, ranges, and boolean scalars and matrices) and
recursive (structs, cells, and lists) ones.

---
