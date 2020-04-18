1 Introduction

---

Reading data into a statistical system for analysis and exporting the
results to some other system for report writing can be frustrating tasks
that can take far more time than the statistical analysis itself, even
though most readers will find the latter far more appealing.

This manual describes the import and export facilities available either
in R itself or via packages which are available from CRAN or elsewhere.

Unless otherwise stated, everything described in this manual is (at
least in principle) available on all platforms running R.

In general, statistical systems like R are not particularly well suited
to manipulations of large-scale data. Some other systems are better than
R at this, and part of the thrust of this manual is to suggest that
rather than duplicating functionality in R we can make another system do
the work! (For example Therneau & Grambsch (2000) commented that they
preferred to do data manipulation in SAS and then use package
[**survival**](https://CRAN.R-project.org/package=survival) in S for the
analysis.) Database manipulation systems are often very suitable for
manipulating and extracting data: several packages to interact with
DBMSs are discussed here.

There are packages to allow functionality developed in languages such as
`Java`, `perl` and `python` to be directly integrated with R code,
making the use of facilities in these languages even more appropriate.
(See the [**rJava**](https://CRAN.R-project.org/package=rJava) package
from CRAN and the **SJava**, **RSPerl** and **RSPython** packages from
the Omegahat project, <http://www.omegahat.net>.)

It is also worth remembering that R like S comes from the Unix tradition
of small re-usable tools, and it can be rewarding to use tools such as
`awk` and `perl` to manipulate data before import or after export. The
case study in Becker, Chambers & Wilks (1988, Chapter 9) is an example
of this, where Unix tools were used to check and manipulate the data
before input to S. The traditional Unix tools are now much more widely
available, including for Windows.

This manual was first written in 2000, and the number of scope of R
packages has increased a hundredfold since. For specialist data formats
it is worth searching to see if a suitable package already exists.

---

• [Imports](#Imports)     
 • [Export to text files](#Export-to-text-files)     
 • [XML](#XML)

---

---

### 1.1 Imports

The easiest form of data to import into R is a simple text file, and
this will often be acceptable for problems of small or medium scale. The
primary function to import from a text file is `scan`, and this
underlies most of the more convenient functions discussed in
[Spreadsheet-like data](#Spreadsheet_002dlike-data).

However, all statistical consultants are familiar with being presented
by a client with a memory stick (formerly, a floppy disc or CD-R) of
data in some proprietary binary format, for example 'an Excel
spreadsheet' or 'an SPSS file'. Often the simplest thing to do is to use
the originating application to export the data as a text file (and
statistical consultants will have copies of the most common applications
on their computers for that purpose). However, this is not always
possible, and [Importing from other statistical systems](#Importing-from-other-statistical-systems) discusses what
facilities are available to access such files directly from R. For Excel
spreadsheets, the available methods are summarized in [Reading Excel spreadsheets](#Reading-Excel-spreadsheets).

In a few cases, data have been stored in a binary form for compactness
and speed of access. One application of this that we have seen several
times is imaging data, which is normally stored as a stream of bytes as
represented in memory, possibly preceded by a header. Such data formats
are discussed in [Binary files](#Binary-files) and [Binary connections](#Binary-connections).

For much larger databases it is common to handle the data using a
database management system (DBMS). There is once again the option of
using the DBMS to extract a plain file, but for many such DBMSs the
extraction operation can be done directly from an R package: See
[Relational databases](#Relational-databases). Importing data via
network connections is discussed in [Network interfaces](#Network-interfaces).

---

• [Encodings](#Encodings)

---

---

#### 1.1.1 Encodings

Unless the file to be imported from is entirely in ASCII, it is usually
necessary to know how it was encoded. For text files, a good way to find
out something about its structure is the `file` command-line tool (for
Windows, included in `Rtools`). This reports something like

```r
text.Rd: UTF-8 Unicode English text
text2.dat: ISO-8859 English text
text3.dat: Little-endian UTF-16 Unicode English character data,
   with CRLF line terminators
intro.dat: UTF-8 Unicode text
intro.dat: UTF-8 Unicode (with BOM) text
```

Modern Unix-alike systems, including macOS, are likely to produce UTF-8
files. Windows may produce what it calls 'Unicode' files (`UCS-2LE` or
just possibly `UTF-16LE`[^1^](#FOOT1)). Otherwise most files
will be in a 8-bit encoding unless from a Chinese/Japanese/Korean locale
(which have a wide range of encodings in common use). It is not possible
to automatically detect with certainty which 8-bit encoding (although
guesses may be possible and `file` may guess as it did in the example
above), so you may simply have to ask the originator for some clues
(e.g. 'Russian on Windows').

'BOMs' (Byte Order Marks,
<https://en.wikipedia.org/wiki/Byte_order_mark>) cause problems for
Unicode files. In the Unix world BOMs are rarely used, whereas in the
Windows world they almost always are for UCS-2/UTF-16 files, and often
are for UTF-8 files. The `file` utility will not even recognize UCS-2
files without a BOM, but many other utilities will refuse to read files
with a BOM and the IANA standards for `UTF-16LE` and `UTF-16BE` prohibit
it. We have too often been reduced to looking at the file with the
command-line utility `od` or a hex editor to work out its encoding.

Note that `utf8` is not a valid encoding name (`UTF-8` is), and
`macintosh` is the most portable name for what is sometimes called 'Mac
Roman' encoding.

---

### 1.2 Export to text files

Exporting results from R is usually a less contentious task, but there
are still a number of pitfalls. There will be a target application in
mind, and often a text file will be the most convenient interchange
vehicle. (If a binary file is required, see [Binary files](#Binary-files).)

Function `cat` underlies the functions for exporting data. It takes a
`file` argument, and the `append` argument allows a text file to be
written via successive calls to `cat`. Better, especially if this is to
be done many times, is to open a `file` connection for writing or
appending, and `cat` to that connection, then `close` it.

The most common task is to write a matrix or data frame to file as a
rectangular grid of numbers, possibly with row and column labels. This
can be done by the functions `write.table` and `write`. Function `write`
just writes out a matrix or vector in a specified number of columns (and
transposes a matrix). Function `write.table` is more convenient, and
writes out a data frame (or an object that can be coerced to a data
frame) with row and column labels.

There are a number of issues that need to be considered in writing out a
data frame to a text file.

1.  **Precision**


    Most of the conversions of real/complex numbers done by these
    functions is to full precision, but those by `write` are governed by
    the current setting of `options(digits)`. For more control, use
    `format` on a data frame, possibly column-by-column.

2.  **Header line**

    R prefers the header line to have no entry for the row names, so the
    file looks like

    ```r
                    dist    climb   time
    Greenmantle     2.5     650     16.083
       ...
    ```

    Some other systems require a (possibly empty) entry for the row
    names, which is what `write.table` will provide if argument
    `col.names = NA` is specified. Excel is one such system.

3.  **Separator**


    A common field separator to use in the file is a comma, as that is
    unlikely to appear in any of the fields in English-speaking
    countries. Such files are known as CSV (comma separated values)
    files, and wrapper function `write.csv` provides appropriate
    defaults. In some locales the comma is used as the decimal point
    (set this in `write.table` by `dec = ","`) and there CSV files use
    the semicolon as the field separator: use `write.csv2` for
    appropriate defaults. There is an IETF standard for CSV files (which
    mandates commas and CRLF line endings, for which use
    `eol = "\r\n"`), RFC4180 (see
    <https://tools.ietf.org/html/rfc4180>), but what is more important
    in practice is that the file is readable by the application it is
    targeted at.

    Using a semicolon or tab (`sep = "\t"`) are probably the safest
    options.

4.  **Missing values**

    By default missing values are output as `NA`, but this may be
    changed by argument `na`. Note that `NaN`s are treated as `NA` by
    `write.table`, but not by `cat` nor `write`.

5.  **Quoting strings**

    By default strings are quoted (including the row and column names).
    Argument `quote` controls if character and factor variables are
    quoted: some programs, for example **Mondrian**
    (<https://en.wikipedia.org/wiki/Mondrian_(software)>), do not accept
    quoted strings.

    Some care is needed if the strings contain embedded quotes. Three
    useful forms are

    ```r
    > df <- data.frame(a = I("a \" quote"))
    > write.table(df)
    "a"
    "1" "a \" quote"
    > write.table(df, qmethod = "double")
    "a"
    "1" "a "" quote"
    > write.table(df, quote = FALSE, sep = ",")
    a
    1,a " quote
    ```

    The second is the form of escape commonly used by spreadsheets.

6.  **Encodings**

    Text files do not contain metadata on their encodings, so for
    non-ASCII data the file needs to be targetted to the application
    intended to read it. All of these functions can write to a
    _connection_ which allows an encoding to be specified for the file,
    and `write.table` has a `fileEncoding` argument to make this easier.

    The hard part is to know what file encoding to use. For use on
    Windows, it is best to use what Windows calls
    'Unicode'[^2^](#FOOT2), that is `"UTF-16LE"`. Using UTF-8 is
    a good way to make portable files that will not easily be confused
    with any other encoding, but even macOS applications (where UTF-8 is
    the system encoding) may not recognize them, and Windows
    applications are most unlikely to. Apparently Excel:mac 2004/8
    expected `.csv` files in `"macroman"` encoding (the encoding used in
    much earlier versions of Mac OS).

Function `write.matrix` in package
[**MASS**](https://CRAN.R-project.org/package=MASS) provides a
specialized interface for writing matrices, with the option of writing
them in blocks and thereby reducing memory usage.

It is possible to use `sink` to divert the standard R output to a file,
and thereby capture the output of (possibly implicit) `print`
statements. This is not usually the most efficient route, and the
`options(width)` setting may need to be increased.

Function `write.foreign` in package
[**foreign**](https://CRAN.R-project.org/package=foreign) uses
`write.table` to produce a text file and also writes a code file that
will read this text file into another statistical package. There is
currently support for export to `SAS`, `SPSS` and `Stata`.

---

### 1.3 XML

When reading data from text files, it is the responsibility of the user
to know and to specify the conventions used to create that file, e.g.
the comment character, whether a header line is present, the value
separator, the representation for missing values (and so on) described
in [Export to text files](#Export-to-text-files). A markup language
which can be used to describe not only content but also the structure of
the content can make a file self-describing, so that one need not
provide these details to the software reading the data.

The eXtensible Markup Language -- more commonly known simply as XML --
can be used to provide such structure, not only for standard datasets
but also more complex data structures. XML is becoming extremely popular
and is emerging as a standard for general data markup and exchange. It
is being used by different communities to describe geographical data
such as maps, graphical displays, mathematics and so on.

XML provides a way to specify the file's encoding, e.g.

```r
<?xml version="1.0" encoding="UTF-8"?>
```

although it does not require it.

The [**XML**](https://CRAN.R-project.org/package=XML) package provides
general facilities for reading and writing XML documents within R.
Package [**StatDataML**](https://CRAN.R-project.org/package=StatDataML)
on CRAN is one example building on
[**XML**](https://CRAN.R-project.org/package=XML). Another interface to
the **libxml2** C library is provided by package
[**xml2**](https://CRAN.R-project.org/package=xml2).

yaml is another system for structuring text data, with emphasis on
human-readability: it is supported by package
[**yaml**](https://CRAN.R-project.org/package=yaml).

---
