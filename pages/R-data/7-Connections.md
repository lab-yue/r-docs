# 7 Connections

---

_Connections_ are used in R in the sense of Chambers (1998) and Ripley
(2001), a set of functions to replace the use of file names by a
flexible interface to file-like objects.

---

• [Types of connections](#Types-of-connections)     
 • [Output to connections](#Output-to-connections)     
 • [Input from connections](#Input-from-connections)     
 • [Listing and manipulating connections](#Listing-and-manipulating-connections)     
 • [Binary connections](#Binary-connections)

---

---

### 7.1 Types of connections

The most familiar type of connection will be a file, and file
connections are created by function `file`. File connections can (if the
OS will allow it for the particular file) be opened for reading or
writing or appending, in text or binary mode. In fact, files can be
opened for both reading and writing, and R keeps a separate file
position for reading and writing.

Note that by default a connection is not opened when it is created. The
rule is that a function using a connection should open a connection
(needed) if the connection is not already open, and close a connection
after use if it opened it. In brief, leave the connection in the state
you found it in. There are generic functions `open` and `close` with
methods to explicitly open and close connections.

Files compressed via the algorithm used by `gzip` can be used as
connections created by the function `gzfile`, whereas files compressed
by `bzip2` can be used via `bzfile`.

Unix programmers are used to dealing with special files `stdin`,
`stdout` and `stderr`. These exist as _terminal connections_ in R. They
may be normal files, but they might also refer to input from and output
to a GUI console. (Even with the standard Unix R interface, `stdin`
refers to the lines submitted from `readline` rather than a file.)

The three terminal connections are always open, and cannot be opened or
closed. `stdout` and `stderr` are conventionally used for normal output
and error messages respectively. They may normally go to the same place,
but whereas normal output can be re-directed by a call to `sink`, error
output is sent to `stderr` unless re-directed by
`sink, type="message")`. Note carefully the language used here: the
connections cannot be re-directed, but output can be sent to other
connections.

_Text connections_ are another source of input. They allow R character
vectors to be read as if the lines were being read from a text file. A
text connection is created and opened by a call to `textConnection`,
which copies the current contents of the character vector to an internal
buffer at the time of creation.

Text connections can also be used to capture R output to a character
vector. `textConnection` can be asked to create a new character object
or append to an existing one, in both cases in the user's workspace. The
connection is opened by the call to `textConnection`, and at all times
the complete lines output to the connection are available in the R
object. Closing the connection writes any remaining output to a final
element of the character vector.

_Pipes_ are a special form of file that connects to another process, and
pipe connections are created by the function `pipe`. Opening a pipe
connection for writing (it makes no sense to append to a pipe) runs an
OS command, and connects its standard input to whatever R then writes to
that connection. Conversely, opening a pipe connection for input runs an
OS command and makes its standard output available for R input from that
connection.

URLs of types '`http://`', '`https://`',
'`ftp://`' and '`file://`' can be read from using the
function `url`. For convenience, `file` will also accept these as the
file specification and call `url`.

Sockets can also be used as connections via function `socketConnection`
on platforms which support Berkeley-like sockets (most Unix systems,
Linux and Windows). Sockets can be written to or read from, and both
client and server sockets can be used.

---

### 7.2 Output to connections

We have described functions `cat`, `write`, `write.table` and `sink` as
writing to a file, possibly appending to a file if argument
`append = TRUE`, and this is what they did prior to R version 1.2.0.

The current behaviour is equivalent, but what actually happens is that
when the `file` argument is a character string, a file connection is
opened (for writing or appending) and closed again at the end of the
function call. If we want to repeatedly write to the same file, it is
more efficient to explicitly declare and open the connection, and pass
the connection object to each call to an output function. This also
makes it possible to write to pipes, which was implemented earlier in a
limited way via the syntax `file = "|cmd"` (which can still be used).

There is a function `writeLines` to write complete text lines to a
connection.

Some simple examples are

```r
zz <- file("ex.data", "w")  # open an output file connection
cat("TITLE extra line", "2 3 5 7", "", "11 13 17",
    file = zz, sep = "\n")
cat("One more line\n", file = zz)
close(zz)

## convert decimal point to comma in output, using a pipe (Unix)
## both R strings and (probably) the shell need \ doubled
zz <- pipe(paste("sed s/\\\\./,/ >", "outfile"), "w")
cat(format(round(rnorm(100), 4)), sep = "\n", file = zz)
close(zz)
## now look at the output file:
file.show("outfile", delete.file = TRUE)

## capture R output: use examples from help(lm)
zz <- textConnection("ex.lm.out", "w")
sink(zz)
example(lm, prompt.echo = "> ")
sink()
close(zz)
## now ‘ex.lm.out’ contains the output for futher processing.
## Look at it by, e.g.,
cat(ex.lm.out, sep = "\n")
```

---

### 7.3 Input from connections

The basic functions to read from connections are `scan` and `readLines`.
These take a character string argument and open a file connection for
the duration of the function call, but explicitly opening a file
connection allows a file to be read sequentially in different formats.

Other functions that call `scan` can also make use of connections, in
particular `read.table`.

Some simple examples are

```r
## read in file created in last examples
readLines("ex.data")
unlink("ex.data")

## read listing of current directory (Unix)
readLines(pipe("ls -1"))

# remove trailing commas from an input file.
# Suppose we are given a file ‘data’ containing
450, 390, 467, 654,  30, 542, 334, 432, 421,
357, 497, 493, 550, 549, 467, 575, 578, 342,
446, 547, 534, 495, 979, 479
# Then read this by
scan(pipe("sed -e s/,$// data"), sep=",")
```

For convenience, if the `file` argument specifies a FTP, HTTP or HTTPS
URL, the URL is opened for reading via `url`. Specifying files via
'`file://foo.bar`' is also allowed.

---

• [Pushback](#Pushback)

---

---

#### 7.3.1 Pushback

C programmers may be familiar with the `ungetc` function to push back a
character onto a text input stream. R connections have the same idea in
a more powerful way, in that an (essentially) arbitrary number of lines
of text can be pushed back onto a connection via a call to `pushBack`.

Pushbacks operate as a stack, so a read request first uses each line
from the most recently pushbacked text, then those from earlier
pushbacks and finally reads from the connection itself. Once a
pushbacked line is read completely, it is cleared. The number of pending
lines pushed back can be found via a call to `pushBackLength`.

A simple example will show the idea.

```r
> zz <- textConnection(LETTERS)
> readLines(zz, 2)
[1] "A" "B"
> scan(zz, "", 4)
Read 4 items
[1] "C" "D" "E" "F"
> pushBack(c("aa", "bb"), zz)
> scan(zz, "", 4)
Read 4 items
[1] "aa" "bb" "G"  "H"
> close(zz)
```

Pushback is only available for connections opened for input in text
mode.

---

### 7.4 Listing and manipulating connections

A summary of all the connections currently opened by the user can be
found by `showConnections()`, and a summary of all connections,
including closed and terminal connections, by
`showConnections(all = TRUE)`

The generic function `seek` can be used to read and (on some
connections) reset the current position for reading or writing.
Unfortunately it depends on OS facilities which may be unreliable (e.g.
with text files under Windows). Function `isSeekable` reports if `seek`
can change the position on the connection given by its argument.

The function `truncate` can be used to truncate a file opened for
writing at its current position. It works only for `file` connections,
and is not implemented on all platforms.

---

### 7.5 Binary connections

Functions `readBin` and `writeBin` read to and write from binary
connections. A connection is opened in binary mode by appending `"b"` to
the mode specification, that is using mode `"rb"` for reading, and mode
`"wb"` or `"ab"` (where appropriate) for writing. The functions have
arguments

```r
readBin(con, what, n = 1, size = NA, endian = .Platform$endian)
writeBin(object, con, size = NA, endian = .Platform$endian)
```

In each case `con` is a connection which will be opened if necessary for
the duration of the call, and if a character string is given it is
assumed to specify a file name.

It is slightly simpler to describe writing, so we will do that first.
`object` should be an atomic vector object, that is a vector of mode
`numeric`, `integer`, `logical`, `character`, `complex` or `raw`,
without attributes. By default this is written to the file as a stream
of bytes exactly as it is represented in memory.

`readBin` reads a stream of bytes from the file and interprets them as a
vector of mode given by `what`. This can be either an object of the
appropriate mode (e.g. `what=integer()`) or a character string
describing the mode (one of the five given in the previous paragraph or
`"double"` or `"int"`). Argument `n` specifies the maximum number of
vector elements to read from the connection: if fewer are available a
shorter vector will be returned. Argument `signed` allows 1-byte and
2-byte integers to be read as signed (the default) or unsigned integers.

The remaining two arguments are used to write or read data for
interchange with another program or another platform. By default binary
data is transferred directly from memory to the connection or _vice
versa_. This will not suffice if the data are to be transferred to a
machine with a different architecture, but between almost all R
platforms the only change needed is that of byte-order. Common PCs
('`ix86`'-based and '`x86_64`'-based machines), Compaq
Alpha and Vaxen are _little-endian_, whereas Sun Sparc, mc680x0 series,
IBM R6000, SGI and most others are _big-endian_. (Network byte-order (as
used by XDR, eXternal Data Representation) is big-endian.) To transfer
to or from other programs we may need to do more, for example to read
16-bit integers or write single-precision real numbers. This can be done
using the `size` argument, which (usually) allows sizes 1, 2, 4, 8 for
integers and logicals, and sizes 4, 8 and perhaps 12 or 16 for reals.
Transferring at different sizes can lose precision, and should not be
attempted for vectors containing `NA`'s.

Character strings are read and written in C format, that is as a string
of bytes terminated by a zero byte. Functions `readChar` and `writeChar`
provide greater flexibility.

---

• [Special values](#Special-values)

---

---

#### 7.5.1 Special values

Functions `readBin` and `writeBin` will pass missing and special values,
although this should not be attempted if a size change is involved.

The missing value for R logical and integer types is `INT_MIN`, the
smallest representable `int` defined in the C header
`limits.h`, normally corresponding to the bit pattern
`0x80000000`.

The representation of the special values for R numeric and complex types
is machine-dependent, and possibly also compiler-dependent. The simplest
way to make use of them is to link an external application against the
standalone `Rmath` library which exports double constants `NA_REAL`,
`R_PosInf` and `R_NegInf`, and include the header `Rmath.h`
which defines the macros `ISNAN` and `R_FINITE`.

If that is not possible, on all current platforms IEC 60559 (aka IEEE

754. arithmetic is used, so standard C facilities can be used to test
     for or set `Inf`, `-Inf` and `NaN` values. On such platforms `NA` is
     represented by the `NaN` value with low-word `0x7a2` (1954 in decimal).

Character missing values are written as `NA`, and there are no provision
to recognize character values as missing (as this can be done by
re-assigning them once read).

---
