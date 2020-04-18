2 Writing R documentation files

---

---

• [Rd format](#Rd-format)     
 • [Sectioning](#Sectioning)     
 • [Marking text](#Marking-text)     
 • [Lists and tables](#Lists-and-tables)     
 • [Cross-references](#Cross_002dreferences)     
 • [Mathematics](#Mathematics)     
 • [Figures](#Figures)     
 • [Insertions](#Insertions)     
 • [Indices](#Indices)     
 • [Platform-specific sections](#Platform_002dspecific-sections)     
 • [Conditional text](#Conditional-text)     
 • [Dynamic pages](#Dynamic-pages)     
 • [User-defined macros](#User_002ddefined-macros)     
 • [Encoding](#Encoding)     
 • [Processing documentation files](#Processing-documentation-files)     
 • [Editing Rd files](#Editing-Rd-files)

---

---

### 2.1 Rd format

R objects are documented in files written in "R documentation" (Rd)
format, a simple markup language much of which closely resembles
(La)TeX, which can be processed into a variety of formats, including
LaTeX, HTML and plain text. The translation is carried out by functions
in the **tools** package called by the script `Rdconv` in
`R_HOME/bin` and by the installation scripts for packages.

The R distribution contains more than 1300 such files which can be found
in the `src/library/pkg/man` directories of the R source tree,
where `pkg`{.variable} stands for one of the standard packages which are
included in the R distribution.

As an example, let us look at a simplified version of
`src/library/base/man/load.Rd` which documents the R function
`load`.

> +-----------------------------------------------------------------------+
> | |
> | `r | | % File src/library/base/man/load.Rd | | \name{load} | | \alias{load} | | \title{Reload Saved Datasets} | | \description{ | | Reload the datasets written to a file with the function | | \code{save}. | | } | | \usage{ | | load(file, envir = parent.frame()) | | } | | \arguments{ | | \item{file}{a connection or a character string giving the | | name of the file to load.} | | \item{envir}{the environment where the data should be | | loaded.} | | } | | \seealso{ | | \code{\link{save}}. | | } | | \examples{ | | ## save all data | | save(list = ls(), file= "all.RData") | | | | ## restore the saved values to the current environment | | load("all.RData") | | | | ## restore the saved values to the workspace | | load("all.RData", .GlobalEnv) | | } | | \keyword{file} | |` |
> | ::: |
> +-----------------------------------------------------------------------+

An `Rd` file consists of three parts. The header gives basic
information about the name of the file, the topics documented, a title,
a short textual description and R usage information for the objects
documented. The body gives further information (for example, on the
function's arguments and return value, as in the above example).
Finally, there is an optional footer with keyword information. The
header is mandatory.

Information is given within a series of _sections_ with standard names
(and user-defined sections are also allowed). Unless otherwise
specified[^101^](#FOOT101) these should occur only once in an
`Rd` file (in any order), and the processing software will
retain only the first occurrence of a standard section in the file, with
a warning.

See ["Guidelines for Rd
files"](https://developer.r-project.org/Rds.html) for guidelines for
writing documentation in `Rd` format which should be useful for
package writers. The R generic function `prompt` is
used to construct a bare-bones `Rd` file ready for manual
editing. Methods are defined for documenting functions (which fill in
the proper function and argument names) and data frames. There are also
functions `promptData`, `promptPackage`, `promptClass`, and
`promptMethods` for other types of `Rd` file.

The general syntax of `Rd` files is summarized below. For a
detailed technical discussion of current `Rd` syntax, see
["Parsing Rd files"](https://developer.r-project.org/parseRd.pdf).

`Rd` files consist of four types of text input. The most common
is LaTeX-like, with the backslash used as a prefix on markup (e.g.
`\alias`), and braces used to indicate arguments (e.g. `{load}`). The
least common type of text is 'verbatim' text, where no markup other than
the comment marker (`%`) is processed. There is also a rare variant of
'verbatim' text (used in `\eqn`, `\deqn`, `\figure`, and `\newcommand`)
where comment markers need not be escaped. The final type is R-like,
intended for R code, but allowing some embedded macros. Quoted strings
within R-like text are handled specially: regular character escapes such
as `\n` may be entered as-is. Only markup starting with `\l` (e.g.
`\link`) or `\v` (e.g. `\var`) will be recognized within quoted strings.
The rarely used vertical tab `\v` must be entered as `\\v`.

Each macro defines the input type for its argument. For example, the
file initially uses LaTeX-like syntax, and this is also used in the
`\description` section, but the `\usage` section uses R-like syntax, and
the `\alias` macro uses 'verbatim' syntax. Comments run from a percent
symbol `%` to the end of the line in all types of text except the rare
'verbatim' variant (as on the first line of the `load` example).

Because backslashes, braces and percent symbols have special meaning, to
enter them into text sometimes requires escapes using a backslash. In
general balanced braces do not need to be escaped, but percent symbols
always do, except in the 'verbatim' variant. For the complete list of
macros and rules for escapes, see ["Parsing Rd
files"](https://developer.r-project.org/parseRd.pdf).

---

• [Documenting functions](#Documenting-functions)     
 • [Documenting data sets](#Documenting-data-sets)     
 • [Documenting S4 classes and methods](#Documenting-S4-classes-and-methods)     
 • [Documenting packages](#Documenting-packages)

---

---

#### 2.1.1 Documenting functions

The basic markup commands used for documenting R objects (in particular,
functions) are given in this subsection.

`\name{name}`

:

    `name`{.variable} typically[^102^](#FOOT102) is the
    basename of the `Rd` file containing the documentation. It
    is the "name" of the `Rd` object represented by the file
    and has to be unique in a package. To avoid problems with indexing
    the package manual, it may not contain '`!`' '`|`'
    nor '`@`', and to avoid possible problems with the HTML
    help system it should not contain '`/`' nor a space. (LaTeX
    special characters are allowed, but may not be collated correctly in
    the index.) There can only be one `\name` entry in a file, and it
    must not contain any markup. Entries in the package manual will be
    in alphabetic[^103^](#FOOT103) order of the `\name`
    entries.

`\alias{topic}`

:

    The `\alias` sections specify all "topics" the file documents. This
    information is collected into index data bases for lookup by the
    on-line (plain text and HTML) help systems. The `topic`{.variable}
    can contain spaces, but (for historical reasons) leading and
    trailing spaces will be stripped. Percent and left brace need to be
    escaped by a backslash.

    There may be several `\alias` entries. Quite often it is convenient
    to document several R objects in one file. For example, file
    `Normal.Rd` documents the density, distribution function,
    quantile function and generation of random variates for the normal
    distribution, and hence starts with


    ``` r
    \name{Normal}
    \alias{Normal}
    \alias{dnorm}
    \alias{pnorm}
    \alias{qnorm}
    \alias{rnorm}
    ```

    Also, it is often convenient to have several different ways to refer
    to an R object, and an `\alias` does not need to be the name of an
    object.

    Note that the `\name` is not necessarily a topic documented, and if
    so desired it needs to have an explicit `\alias` entry (as in this
    example).

`\title{Title}`

:

    Title information for the `Rd` file. This should be
    capitalized and not end in a period; try to limit its length to at
    most 65 characters for widest compatibility.

    Markup is supported in the text, but use of characters other than
    English text and punctuation (e.g., '`<`') may limit
    portability.

    There must be one (and only one) `\title` section in a help file.

`\description{…}`

:

    A short description of what the function(s) do(es) (one paragraph, a
    few lines only). (If a description is too long and cannot easily be
    shortened, the file probably tries to document too much at once.)
    This is mandatory except for package-overview files.

`\usage{fun(arg1, arg2, …)}`

:

    One or more lines showing the synopsis of the function(s) and
    variables documented in the file. These are set in typewriter font.
    This is an R-like command.

    The usage information specified should match the function definition
    *exactly* (such that automatic checking for consistency between code
    and documentation is possible).

    To indicate that a function can be used in several different ways,
    depending on the named arguments specified, use section `\details`.
    E.g., `abline.Rd` contains


    ``` r
    \details{
      Typical usages are
    \preformatted{abline(a, b, untf = FALSE, \dots)
    ......
    }
    ```



    Use `\method{generic}{class}` to indicate the name of an S3 method
    for the generic function `generic`{.variable} for objects inheriting
    from class `"class"`. In the printed versions, this will come out as
    `generic`{.variable} (reflecting the understanding that methods
    should not be invoked directly but *via* method dispatch), but
    `codoc()` and other QC tools always have access to the full name.

    For example, `print.ts.Rd` contains


    ``` r
    \usage{
    \method{print}{ts}(x, calendar, \dots)
    }
    ```

    which will print as


    ``` r
    Usage:

         ## S3 method for class ‘ts’:
         print(x, calendar, ...)
    ```

    Usage for replacement functions should be given in the style of
    `dim(x) <- value` rather than explicitly indicating the name of the
    replacement function (`"dim<-"` in the above). Similarly, one can
    use `\method{generic}{class}(arglist) <- value` to indicate the
    usage of an S3 replacement method for the generic replacement
    function `"generic<-"` for objects inheriting from class `"class"`.

    Usage for S3 methods for extracting or replacing parts of an object,
    S3 methods for members of the Ops group, and S3 methods for
    user-defined (binary) infix operators ('`%xxx%`') follows
    the above rules, using the appropriate function names. E.g.,
    `Extract.factor.Rd` contains


    ``` r
    \usage{
    \method{[}{factor}(x, \dots, drop = FALSE)
    \method{[[}{factor}(x, \dots)
    \method{[}{factor}(x, \dots) <- value
    }
    ```

    which will print as


    ``` r
    Usage:

         ## S3 method for class ‘factor’:
         x[..., drop = FALSE]
         ## S3 method for class ‘factor’:
         x[[...]]
         ## S3 replacement method for class ‘factor’:
         x[...] <- value
    ```



    `\S3method` is accepted as an alternative to `\method`.

`\arguments{…}`

:

    Description of the function's arguments, using an entry of the form


    ``` r
    \item{arg_i}{Description of arg_i.}
    ```

    for each element of the argument list. (Note that there is no
    whitespace between the three parts of the entry.) There may be
    optional text outside the `\item` entries, for example to give
    general information about groups of parameters.

`\details{…}`

:

    A detailed if possible precise description of the functionality
    provided, extending the basic information in the `\description`
    slot.

`\value{…}`

:

    Description of the function's return value.

    If a list with multiple values is returned, you can use entries of
    the form


    ``` r
    \item{comp_i}{Description of comp_i.}
    ```

    for each component of the list returned. Optional text may
    precede[^104^](#FOOT104) this list (see for example the
    help for `rle`). Note that `\value` is implicitly a `\describe`
    environment, so that environment should not be used for listing
    components, just individual `\item{}{}` entries.

`\references{…}`

:

    A section with references to the literature. Use `\url{}` or
    `\href{}{}` for web pointers.

`\note{...}`

:

    Use this for a special note you want to have pointed out. Multiple
    `\note` sections are allowed, but might be confusing to the end
    users.

    For example, `pie.Rd` contains


    ``` r
    \note{
      Pie charts are a very bad way of displaying information.
      The eye is good at judging linear measures and bad at
      judging relative areas.
      ......
    }
    ```

`\author{…}`

:

    Information about the author(s) of the `Rd` file. Use
    `\email{}` without extra delimiters (such as '`( )`' or
    '`< >`') to specify email addresses, or `\url{}` or
    `\href{}{}` for web pointers.

`\seealso{…}`

:

    Pointers to related R objects, using `\code{\link{...}}` to refer to
    them (`\code` is the correct markup for R object names, and `\link`
    produces hyperlinks in output formats which support this. See
    [Marking text](#Marking-text), and
    [Cross-references](#Cross_002dreferences)).

`\examples{…}`

: Examples of how to use the function. Code in this section is set in
typewriter font without reformatting and is run by `example()`
unless marked otherwise (see below).

    Examples are not only useful for documentation purposes, but also
    provide test code used for diagnostic checking of R code. By
    default, text inside `\examples{}` will be displayed in the output
    of the help page and run by `example()` and by `R CMD check`. You
    can use `\dontrun{}`  for text that should
    only be shown, but not run, and `\dontshow{}`
     for extra commands for testing that should
    not be shown to users, but will be run by `example()`. (Previously
    this was called `\testonly`, and that is still accepted.)

    Text inside `\dontrun{}` is 'verbatim', but the other parts of the
    `\examples` section are R-like text.

    For example,


    ``` r
    x <- runif(10)       # Shown and run.
    \dontrun{plot(x)}    # Only shown.
    \dontshow{log(x)}    # Only run.
    ```

    Thus, example code not included in `\dontrun` must be executable! In
    addition, it should not use any system-specific features or require
    special facilities (such as Internet access or write permission to
    specific directories). Text included in `\dontrun` is indicated by
    comments in the processed help files: it need not be valid R code
    but the escapes must still be used for `%`, `\` and unpaired braces
    as in other 'verbatim' text.

    Example code must be capable of being run by `example`, which uses
    `source`. This means that it should not access `stdin`,
    e.g. to `scan()` data from the example file.

    Data needed for making the examples executable can be obtained by
    random number generation (for example, `x <- rnorm(100)`), or by
    using standard data sets listed by `data()` (see `?data` for more
    info).

    Finally, there is `\donttest`, used (at the beginning of a separate
    line) to mark code that should be run by `example()` but not by
    `R CMD check` (by default: the option `--run-donttest` can
    be used). This should be needed only occasionally but can be used
    for code which might fail in circumstances that are hard to test
    for, for example in some locales. (Use e.g. `capabilities()` or
    `nzchar(Sys.which("someprogram"))` to test for features needed in
    the examples wherever possible, and you can also use `try()` or
    `tryCatch()`. Use `interactive()` to condition examples which need
    someone to interact with.) Note that code included in `\donttest`
    must be correct R code, and any packages used should be declared in
    the `DESCRIPTION` file. It is good practice to include a
    comment in the `\donttest` section explaining why it is needed.

    Output from code between comments


    ``` r
    ## IGNORE_RDIFF_BEGIN
    ## IGNORE_RDIFF_END
    ```

    is ignored when comparing check output to reference output (a
    `-Ex.Rout.save` file). This markup can also be used for
    scripts under `tests`.

`\keyword{key}`

: There can be zero or more `\keyword` sections per file. Each
`\keyword` section should specify a single keyword, preferably one
of the standard keywords as listed in file `KEYWORDS` in
the R documentation directory (default `R_HOME/doc`). Use
e.g. `RShowDoc("KEYWORDS")` to inspect the standard keywords from
within R. There can be more than one `\keyword` entry if the R
object being documented falls into more than one category, or none.

    Do strongly consider using `\concept` (see [Indices](#Indices))
    instead of `\keyword` if you are about to use more than very few
    non-standard keywords.

    The special keyword '`internal`' marks a page of internal
    objects that are not part of the package's API. If the help page for
    object `foo` has keyword '`internal`', then `help(foo)`
    gives this help page, but `foo` is excluded from several object
    indices, including the alphabetical list of objects in the HTML help
    system.

    `help.search()` can search by keyword, including user-defined
    values: however the 'Search Engine & Keywords' HTML page accessed
    *via* `help.start()` provides single-click access only to a
    pre-defined list of keywords.

---

#### 2.1.2 Documenting data sets

The structure of `Rd` files which document R data sets is
slightly different. Sections such as `\arguments` and `\value` are not
needed but the format and source of the data should be explained.

As an example, let us look at
`src/library/datasets/man/rivers.Rd` which documents the
standard R data set `rivers`.

> +-----------------------------------------------------------------------+
> | |
> | `r | | \name{rivers} | | \docType{data} | | \alias{rivers} | | \title{Lengths of Major North American Rivers} | | \description{ | | This data set gives the lengths (in miles) of 141 \dQuote{major} | | rivers in North America, as compiled by the US Geological | | Survey. | | } | | \usage{rivers} | | \format{A vector containing 141 observations.} | | \source{World Almanac and Book of Facts, 1975, page 406.} | | \references{ | | McNeil, D. R. (1977) \emph{Interactive Data Analysis}. | | New York: Wiley. | | } | | \keyword{datasets} | |` |
> | ::: |
> +-----------------------------------------------------------------------+

This uses the following additional markup commands.

`\docType{…}`

: Indicates the "type" of the documentation object. Always
'`data`' for data sets, and '`package`' for
`pkg-package.Rd` overview files. Documentation for S4
methods and classes uses '`methods`' (from
`promptMethods()`) and '`class`' (from `promptClass()`).

`\format{…}`

:

    A description of the format of the data set (as a vector, matrix,
    data frame, time series, ...). For matrices and data frames this
    should give a description of each column, preferably as a list or
    table. See [Lists and tables](#Lists-and-tables), for more
    information.

`\source{…}`

:

    Details of the original source (a reference or URL, see [Specifying
    URLs](#Specifying-URLs)). In addition, section `\references` could
    give secondary sources and usages.

Note also that when documenting data set `bar`{.variable},

- The `\usage` entry is always `bar` or (for packages which do not use
  lazy-loading of data) `data(bar)`. (In particular, only document a
  _single_ data object per `Rd` file.)
- The `\keyword` entry should always be '`datasets`'.

If `bar` is a data frame, documenting it as a data set can be initiated
_via_ `prompt(bar)`. Otherwise, the `promptData` function may be used.

---

#### 2.1.3 Documenting S4 classes and methods

There are special ways to use the '`?`' operator, namely
'`class?topic`' and '`methods?topic`', to access
documentation for S4 classes and methods, respectively. This mechanism
depends on conventions for the topic names used in `\alias` entries. The
topic names for S4 classes and methods respectively are of the form

```r
class-class
generic,signature_list-method
```

where `signature_list`{.variable} contains the names of the classes in
the signature of the method (without quotes) separated by '`,`'
(without whitespace), with '`ANY`' used for arguments without
an explicit specification. E.g., '`genericFunction-class`' is
the topic name for documentation for the S4 class `"genericFunction"`,
and '`coerce,ANY,NULL-method`' is the topic name for
documentation for the S4 method for `coerce` for signature
`c("ANY", "NULL")`.

Skeletons of documentation for S4 classes and methods can be generated
by using the functions `promptClass()` and `promptMethods()` from
package **methods**. If it is necessary or desired to provide an
explicit function declaration (in a `\usage` section) for an S4 method
(e.g., if it has "surprising arguments" to be mentioned explicitly), one
can use the special markup

```r
\S4method{generic}{signature_list}(argument_list)
```

(e.g., '`\S4method{coerce}{ANY,NULL}(from, to)`').

To make full use of the potential of the on-line documentation system,
all user-visible S4 classes and methods in a package should at least
have a suitable `\alias` entry in one of the package's `Rd`
files. If a package has methods for a function defined originally
somewhere else, and does not change the underlying default method for
the function, the package is responsible for documenting the methods it
creates, but not for the function itself or the default method.

An S4 replacement method is documented in the same way as an S3 one: see
the description of `\method` in [Documenting functions](#Documenting-functions).

See `help("Documentation", package = "methods")` for more information on
using and creating on-line documentation for S4 classes and methods.

---

#### 2.1.4 Documenting packages

Packages may have an overview help page with an `\alias`
`pkgname-package`, e.g. '`utils-package`' for the **utils**
package, when `package?pkgname` will open that help page. If a topic
named `pkgname` does not exist in another `Rd` file, it is
helpful to use this as an additional `\alias`.

Skeletons of documentation for a package can be generated using the
function `promptPackage()`. If the `final = LIBS` argument is used, then
the `Rd` file will be generated in final form, containing the
information that would be produced up to `library(help = pkgname)`.
Otherwise (the default) comments will be inserted giving suggestions for
content.

Apart from the mandatory `\name` and `\title` and the `pkgname-package`
alias, the only requirement for the package overview page is that it
include a `\docType{package}` statement. All other content is optional.
We suggest that it should be a short overview, to give a reader
unfamiliar with the package enough information to get started. More
extensive documentation is better placed into a package vignette (see
[Writing package vignettes](#Writing-package-vignettes)) and referenced
from this page, or into individual man pages for the functions,
datasets, or classes.

---

### 2.2 Sectioning

To begin a new paragraph or leave a blank line in an example, just
insert an empty line (as in (La)TeX). To break a line, use `\cr`.

In addition to the predefined sections (such as `\description{}`,
`\value{}`, etc.), you can "define" arbitrary ones by
`\section{section_title}{…}`. For example

```r
\section{Warning}{
  You must not call this function unless …
}
```

For consistency with the pre-assigned sections, the section name (the
first argument to `\section`) should be capitalized (but not all upper
case). Whitespace between the first and second braced expressions is not
allowed. Markup (e.g. `\code`) within the section title may cause
problems with the latex conversion (depending on the version of macro
packages such as '`hyperref`') and so should be avoided.

The `\subsection` macro takes arguments in the same format as
`\section`, but is used within a section, so it may be used to nest
subsections within sections or other subsections. There is no predefined
limit on the nesting level, but formatting is not designed for more than
3 levels (i.e. subsections within subsections within sections).

Note that additional named sections are always inserted at a fixed
position in the output (before `\note`, `\seealso` and the examples), no
matter where they appear in the input (but in the same order amongst
themselves as in the input).

---

### 2.3 Marking text

The following logical markup commands are available for emphasizing or
quoting text.

`\emph{text}`
:

`\strong{text}`

:

    Emphasize `text`{.variable} using *italic* and **bold** font if
    possible; `\strong` is regarded as stronger (more emphatic).

`\bold{text}`

:

    Set `text`{.variable} in **bold** font where possible.

`\sQuote{text}`
:

`\dQuote{text}`

:

    Portably single or double quote `text`{.variable} (without
    hard-wiring the characters used for quotation marks).

Each of the above commands takes LaTeX-like input, so other macros may
be used within `text`{.variable}.

The following logical markup commands are available for indicating
specific kinds of text. Except as noted, these take 'verbatim' text
input, and so other macros may not be used within them. Some characters
will need to be escaped (see [Insertions](#Insertions)).

`\code{text}`

:

    Indicate text that is a literal example of a piece of an R program,
    e.g., a fragment of R code or the name of an R object. Text is
    entered in R-like syntax, and displayed using `typewriter` font
    where possible. Macros `\var` and `\link` are interpreted within
    `text`{.variable}.

`\preformatted{text}`

:

    Indicate text that is a literal example of a piece of a program.
    Text is displayed using `typewriter` font where possible.
    Formatting, e.g. line breaks, is preserved. (Note that this includes
    a line break after the initial {, so typically text should start on
    the same line as the command.)

    Due to limitations in LaTeX as of this writing, this macro may not
    be nested within other markup macros other than `\dQuote` and
    `\sQuote`, as errors or bad formatting may result.

`\kbd{keyboard-characters}`

:

    Indicate keyboard input, using [slanted typewriter]{.kbd} font if
    possible, so users can distinguish the characters they are supposed
    to type from computer output. Text is entered 'verbatim'.

`\samp{text}`

:

    Indicate text that is a literal example of a sequence of characters,
    entered 'verbatim'. No wrapping or reformatting will occur.
    Displayed using `typewriter` font where possible.

`\verb{text}`

:

    Indicate text that is a literal example of a sequence of characters,
    with no interpretation of e.g. `\var`, but which will be included
    within word-wrapped text. Displayed using `typewriter` font if
    possible.

`\pkg{package_name}`

:

    Indicate the name of an R package. LaTeX-like.

`\file{file_name}`

:

    Indicate the name of a file. Text is LaTeX-like, so backslash needs
    to be escaped. Displayed using a distinct font where possible.

`\email{email_address}`

:

    Indicate an electronic mail address. LaTeX-like, will be rendered as
    a hyperlink in HTML and PDF conversion. Displayed using `typewriter`
    font where possible.

`\url{uniform_resource_locator}`

:

    Indicate a uniform resource locator (URL) for the World Wide Web.
    The argument is handled as 'verbatim' text (with percent and braces
    escaped by backslash), and rendered as a hyperlink in HTML and PDF
    conversion. Linefeeds are removed, and leading and trailing
    whitespace[^105^](#FOOT105) is removed. See [Specifying
    URLs](#Specifying-URLs).

    Displayed using `typewriter` font where possible.

`\href{uniform_resource_locator}{text}`

:

    Indicate a hyperlink to the World Wide Web. The first argument is
    handled as 'verbatim' text (with percent and braces escaped by
    backslash) and is used as the URL in the hyperlink, with the second
    argument of LaTeX-like text displayed to the user. Linefeeds are
    removed from the first argument, and leading and trailing whitespace
    is removed.

    Note that RFC3986-encoded URLs (e.g. using
    '`\%28VS.85\%29`' in place of '`(VS.85)`') may not
    work correctly in versions of R before 3.1.3 and are best
    avoided---use `URLdecode()` to decode them.

`\var{metasyntactic_variable}`

:

    Indicate a metasyntactic variable. In some cases this will be
    rendered distinctly, e.g. in italic, but not in
    all[^106^](#FOOT106). LaTeX-like.

`\env{environment_variable}`

:

    Indicate an environment variable. 'Verbatim'. Displayed using
    `typewriter` font where possible

`\option{option}`

:

    Indicate a command-line option. 'Verbatim'. Displayed using
    `typewriter` font where possible.

`\command{command_name}`

:

    Indicate the name of a command. LaTeX-like, so `\var` is
    interpreted. Displayed using `typewriter` font where possible.

`\dfn{term}`

:

    Indicate the introductory or defining use of a term. LaTeX-like.

`\cite{reference}`

:

    Indicate a reference without a direct cross-reference *via* `\link`
    (see [Cross-references](#Cross_002dreferences)), such as the name of
    a book. LaTeX-like.

`\acronym{acronym}`

:

    Indicate an acronym (an abbreviation written in all capital
    letters), such as GNU. LaTeX-like.

---

### 2.4 Lists and tables

The `\itemize` and `\enumerate` commands take a single argument, within
which there may be one or more `\item` commands. The text following each
`\item` is formatted as one or more paragraphs, suitably indented and
with the first paragraph marked with a bullet point (`\itemize`) or a
number (`\enumerate`).

Note that unlike argument lists, `\item` in these formats is followed by
a space and the text (not enclosed in braces). For example

```r
  \enumerate{
    \item A database consists of one or more records, each with one or
    more named fields.
    \item Regular lines start with a non-whitespace character.
    \item Records are separated by one or more empty lines.
  }
```

`\itemize` and `\enumerate` commands may be nested.

The `\describe` command is similar to `\itemize` but allows initial
labels to be specified. Each `\item` takes two arguments, the label and
the body of the item, in exactly the same way as an argument or value
`\item`. `\describe` commands are mapped to `<DL>` lists in HTML and
`\description` lists in LaTeX.

The `\tabular` command takes two arguments. The first gives for each of
the columns the required alignment ('`l`' for
left-justification, '`r`' for right-justification or
'`c`' for centring.) The second argument consists of an
arbitrary number of lines separated by `\cr`, and with fields separated
by `\tab`. For example:

```r
  \tabular{rlll}{
    [,1] \tab Ozone   \tab numeric \tab Ozone (ppb)\cr
    [,2] \tab Solar.R \tab numeric \tab Solar R (lang)\cr
    [,3] \tab Wind    \tab numeric \tab Wind (mph)\cr
    [,4] \tab Temp    \tab numeric \tab Temperature (degrees F)\cr
    [,5] \tab Month   \tab numeric \tab Month (1--12)\cr
    [,6] \tab Day     \tab numeric \tab Day of month (1--31)
  }
```

There must be the same number of fields on each line as there are
alignments in the first argument, and they must be non-empty (but can
contain only spaces). (There is no whitespace between `\tabular` and the
first argument, nor between the two arguments.)

---

### 2.5 Cross-references

The markup `\link{foo}` (usually in the combination `\code{\link{foo}}`)
produces a hyperlink to the help for `foo`{.variable}. Here
`foo`{.variable} is a _topic_, that is the argument of `\alias` markup
in another `Rd` file (possibly in another package). Hyperlinks
are supported in some of the formats to which `Rd` files are
converted, for example HTML and PDF, but ignored in others, e.g. the
text format.

One main usage of `\link` is in the `\seealso` section of the help page,
see [Rd format](#Rd-format).

Note that whereas leading and trailing spaces are stripped when
extracting a topic from a `\alias`, they are not stripped when looking
up the topic of a `\link`.

You can specify a link to a different topic than its name by
`\link[=dest]{name}` which links to topic `dest`{.variable} with name
`name`{.variable}. This can be used to refer to the documentation for
S3/4 classes, for example `\code{"\link[=abc-class]{abc}"}` would be a
way to refer to the documentation of an S4 class `"abc"` defined in your
package, and `\code{"\link[=terms.object]{terms}"}` to the S3 `"terms"`
class (in package **stats**). To make these easy to read in the source
file, `\code{"\linkS4class{abc}"}` expands to the form given above.

There are two other forms of optional argument specified as
`\link[pkg]{foo}` and `\link[pkg:bar]{foo}` to link to the package
**`pkg`{.variable}**, to _files_ `foo.html` and
`bar.html` respectively. These are rarely needed, perhaps to
refer to not-yet-installed packages (but there the HTML help system will
resolve the link at run time) or in the normally undesirable event that
more than one package offers help on a topic[^107^](#FOOT107)
(in which case the present package has precedence so this is only needed
to refer to other packages). They are currently only used in HTML help
(and ignored for hyperlinks in LaTeX conversions of help pages), and
link to the file rather than the topic (since there is no way to know
which topics are in which files in an uninstalled package). The **only**
reason to use these forms for base and recommended packages is to force
a reference to a package that might be further down the search path.
Because they have been frequently misused, the HTML help system looks
for topic `foo` in package **`pkg`{.variable}** if it does not find file
`foo.html`.

---

### 2.6 Mathematics

Mathematical formulae should be set beautifully for printed
documentation yet we still want something useful for text and HTML
online help. To this end, the two commands `\eqn{latex}{ascii}` and
`\deqn{latex}{ascii}` are used. Whereas `\eqn` is used for "inline"
formulae (corresponding to TeX's `$…$`), `\deqn` gives "displayed
equations" (as in LaTeX's `displaymath` environment, or TeX's `$$…$$`).
Both arguments are treated as 'verbatim' text.

Both commands can also be used as `\eqn{latexascii}` (only _one_
argument) which then is used for both `latex`{.variable} and
`ascii`{.variable}. No whitespace is allowed between command and the
first argument, nor between the first and second arguments.

The following example is from `Poisson.Rd`:

```r
  \deqn{p(x) = \frac{\lambda^x e^{-\lambda}}{x!}}{%
        p(x) = \lambda^x exp(-\lambda)/x!}
  for \eqn{x = 0, 1, 2, \ldots}.
```

For text on-line help we get

> +-----------------------------------------------------------------------+
> | |
> | `r | | p(x) = lambda^x exp(-lambda)/x! | | | | for x = 0, 1, 2, .... | |` |
> | ::: |
> +-----------------------------------------------------------------------+

Greek letters (both cases) will be rendered in HTML if preceded by a
backslash, `\dots` and `\ldots` will be rendered as ellipses and
`\sqrt`, `\ge` and `\le` as mathematical symbols.

Note that only basic LaTeX can be used, there being no provision to
specify LaTeX style files such as the AMS extensions.

---

### 2.7 Figures

To include figures in help pages, use the `\figure` markup. There are
three forms.

The two commonly used simple forms are `\figure{filename}` and
`\figure{filename}{alternate text}`. This will include a copy of the
figure in either HTML or LaTeX output. In text output, the alternate
text will be displayed instead. (When the second argument is omitted,
the filename will be used.) Both the filename and the alternate text
will be parsed verbatim, and should not include special characters that
are significant in HTML or LaTeX.

The expert form is `\figure{filename}{options: string}`. (The word
'`options:`' must be typed exactly as shown and followed by at
least one space.) In this form, the `string`{.variable} is copied into
the HTML `img` tag as attributes following the `src` attribute, or into
the second argument of the `\Figure` macro in LaTeX, which by default is
used as options to an `\includegraphics` call. As it is unlikely that
any single string would suffice for both display modes, the expert form
would normally be wrapped in conditionals. It is up to the author to
make sure that legal HTML/LaTeX is used. For example, to include a logo
in both HTML (using the simple form) and LaTeX (using the expert form),
the following could be used:

```r
\if{html}{\figure{Rlogo.svg}{options: width=100 alt="R logo"}}
\if{latex}{\figure{Rlogo.pdf}{options: width=0.5in}}
```

The files containing the figures should be stored in the directory
`man/figures`. Files with extensions `.jpg`,
`.jpeg`, `.pdf`, `.png` and `.svg`
from that directory will be copied to the `help/figures`
directory at install time. (Figures in PDF format will not display in
most HTML browsers, but might be the best choice in reference manuals.)
Specify the filename relative to `man/figures` in the `\figure`
directive.

---

### 2.8 Insertions

Use `\R` for the R system itself. Use `\dots` for
the dots in function argument lists '`…`', and `\ldots`
for ellipsis dots in ordinary
text.[^108^](#FOOT108) These can be followed by `{}`, and
should be unless followed by whitespace.

After an unescaped '`%`', you can put your own comments
regarding the help text. The rest of the line (but not the newline at
the end) will be completely disregarded. Therefore, you can also use it
to make part of the "help" invisible.

You can produce a backslash ('`\`') by escaping it by another
backslash. (Note that `\cr` is used for generating line breaks.)

The "comment" character '`%`' and unpaired
braces[^109^](#FOOT109) _almost always_ need to be escaped by
'`\`', and '`\\`' can be used for backslash and needs
to be when there are two or more adjacent backslashes. In R-like code
quoted strings are handled slightly differently; see ["Parsing Rd
files"](https://developer.r-project.org/parseRd.pdf) for details -- in
particular braces should not be escaped in quoted strings.

All of '`% { } \`' should be escaped in LaTeX-like text.

Text which might need to be represented differently in different
encodings should be marked by `\enc`, e.g. `\enc{Jöreskog}{Joreskog}`
(with no whitespace between the braces) where the first argument will be
used where encodings are allowed and the second should be ASCII (and is
used for e.g. the text conversion in locales that cannot represent the
encoded form). (This is intended to be used for individual words, not
whole sentences or paragraphs.)

---

### 2.9 Indices

The `\alias` command (see [Documenting functions](#Documenting-functions)) is used to specify the "topics"
documented, which should include _all_ R objects in a package such as
functions and variables, data sets, and S4 classes and methods (see
[Documenting S4 classes and methods](#Documenting-S4-classes-and-methods)). The on-line help system
searches the index data base consisting of all alias topics.

In addition, it is possible to provide "concept index entries" using
`\concept`, which can be used for `help.search()` lookups. E.g., file
`cor.test.Rd` in the standard package **stats** contains

```r
\concept{Kendall correlation coefficient}
\concept{Pearson correlation coefficient}
\concept{Spearman correlation coefficient}
```

so that e.g. [??Spearman]{.kbd} will succeed in finding the help page
for the test for association between paired samples using Spearman's
rho.

(Note that `help.search()` only uses "sections" of documentation objects
with no additional markup.)

Each `\concept` entry should give a _single_ index term (word or
phrase), and not use any Rd markup.

If you want to cross reference such items from other help files _via_
`\link`, you need to use `\alias` and not `\concept`.

---

### 2.10 Platform-specific documentation

Sometimes the documentation needs to differ by platform. Currently two
OS-specific options are available, '`unix`' and
'`windows`', and lines in the help source file can be enclosed
in

```r
#ifdef OS
   ...
#endif
```

or

```r
#ifndef OS
   ...
#endif
```

for OS-specific inclusion or exclusion. Such blocks should not be
nested, and should be entirely within a block (that, is between the
opening and closing brace of a section or item), or at top-level contain
one or more complete sections.

If the differences between platforms are extensive or the R objects
documented are only relevant to one platform, platform-specific
`Rd` files can be put in a `unix` or
`windows` subdirectory.

---

### 2.11 Conditional text

Occasionally the best content for one output format is different from
the best content for another. For this situation, the
`\if{format}{text}` or `\ifelse{format}{text}{alternate}` markup is
used. Here `format`{.variable} is a comma separated list of formats in
which the `text`{.variable} should be rendered. The
`alternate`{.variable} will be rendered if the format does not match.
Both `text`{.variable} and `alternate`{.variable} may be any sequence of
text and markup.

Currently the following formats are recognized: `example`, `html`,
`latex` and `text`. These select output for the corresponding targets.
(Note that `example` refers to extracted example code rather than the
displayed example in some other format.) Also accepted are `TRUE`
(matching all formats) and `FALSE` (matching no formats). These could be
the output of the `\Sexpr` macro (see [Dynamic pages](#Dynamic-pages)).

The `\out{literal}` macro would usually be used within the
`text`{.variable} part of `\if{format}{text}`. It causes the renderer to
output the literal text exactly, with no attempt to escape special
characters. For example, use the following to output the markup
necessary to display the Greek letter in LaTeX or HTML, and the text
string `alpha` in other formats:

```r
\ifelse{latex}{\out{$\alpha$}}{\ifelse{html}{\out{&alpha;}}{alpha}}
```

---

### 2.12 Dynamic pages

Two macros supporting dynamically generated man pages are `\Sexpr` and
`\RdOpts`. These are modelled after Sweave, and are intended to contain
executable R expressions in the `Rd` file.

The main argument to `\Sexpr` must be valid R code that can be executed.
It may also take options in square brackets before the main argument.
Depending on the options, the code may be executed at package build
time, package install time, or man page rendering time.

The options follow the same format as in Sweave, but different options
are supported. Currently the allowed options and their defaults are:

- `eval=TRUE` Whether the R code should be evaluated.

- `echo=FALSE` Whether the R code should be echoed. If `TRUE`, a
  display will be given in a preformatted block. For example,
  `\Sexpr[echo=TRUE]{ x <- 1 }` will be displayed as

  ```r
  > x <- 1
  ```

- `keep.source=TRUE` Whether to keep the author's formatting when
  displaying the code, or throw it away and use a deparsed version.

- `results=text` How should the results be displayed? The
  possibilities are:

  - \- `results=text` Apply `as.character()` to the result of the
    code, and insert it as a text element.
  - \- `results=verbatim` Print the results of the code just as if
    it was executed at the console, and include the printed results
    verbatim. (Invisible results will not print.)
  - \- `results=rd` The result is assumed to be a character vector
    containing markup to be passed to `parse_Rd()`, with the result
    inserted in place. This could be used to insert computed
    aliases, for instance. `parse_Rd()` is called first with
    `fragment = FALSE` to allow a single Rd section macro to be
    inserted. If that fails, it is called again with
    `fragment = TRUE`, the older behavior.
  - \- `results=hide` Insert no output.

- `strip.white=TRUE` Remove leading and trailing white space from each
  line of output if `strip.white=TRUE`. With `strip.white=all`, also
  remove blank lines.

- `stage=install` Control when this macro is run. Possible values are

  - \- `stage=build` The macro is run when building a source
    tarball.
  - \- `stage=install` The macro is run when installing from source.
  - \- `stage=render` The macro is run when displaying the help
    page.

  Conditionals such as `#ifdef` (see [Platform-specific
  sections](#Platform_002dspecific-sections)) are applied after the
  `build` macros but before the `install` macros. In some situations
  (e.g. installing directly from a source directory without a tarball,
  or building a binary package) the above description is not literally
  accurate, but authors can rely on the sequence being `build`,
  `#ifdef`, `install`, `render`, with all stages executed.

  Code is only run once in each stage, so a `\Sexpr[results=rd]` macro
  can output an `\Sexpr` macro designed for a later stage, but not for
  the current one or any earlier stage.

- `width, height, fig` These options are currently allowed but
  ignored.

The `\RdOpts` macro is used to set new defaults for options to apply to
following uses of `\Sexpr`.

For more details, see the online document ["Parsing Rd
files"](https://developer.r-project.org/parseRd.pdf).

---

### 2.13 User-defined macros

The `\newcommand` and `\renewcommand` macros allow new macros to be
defined within an Rd file. These are similar but not identical to the
same-named LaTeX macros.

They each take two arguments which are parsed verbatim. The first is the
name of the new macro including the initial backslash, and the second is
the macro definition. As in LaTeX, `\newcommand` requires that the new
macro not have been previously defined, whereas `\renewcommand` allows
existing macros (including all built-in ones) to be replaced. (This test
is disabled by default, but may be enabled by setting the environment
variable `_WARN_DUPLICATE_RD_MACROS_` to a true value.)

Also as in LaTeX, the new macro may be defined to take arguments, and
numeric placeholders such as `#1` are used in the macro definition.
However, unlike LaTeX, the number of arguments is determined
automatically from the highest placeholder number seen in the macro
definition. For example, a macro definition containing `#1` and `#3`
(but no other placeholders) will define a three argument macro (whose
second argument will be ignored). As in LaTeX, at most 9 arguments may
be defined. If the `#` character is followed by a non-digit it will have
no special significance. All arguments to user-defined macros will be
parsed as verbatim text, and simple text-substitution will be used to
replace the place-holders, after which the replacement text will be
parsed.

A number of macros are defined in the file
`share/Rd/macros/system.Rd` of the R source or home directory,
and these will normally be available in all `.Rd` files. For
example, that file contains the definition

```r
\newcommand{\PR}{\Sexpr[results=rd]{tools:::Rd_expr_PR(#1)}}
```

which defines `\PR` to be a single argument macro; then code (typically
used in the `NEWS.Rd` file) like

```r
\PR{1234}
```

will expand to

```r
\Sexpr[results=rd]{tools:::Rd_expr_PR(1234)}
```

when parsed.

Some macros that might be of general use are:

`\CRANpkg{pkg}`

: A package on CRAN

`\sspace`

: A single space (used after a period that does not end a sentence).

`\doi{numbers}`

: A digital object identifier (DOI).

See the `system.Rd` file in `share/Rd/macros` for more
details and macro definitions, including macros `\packageTitle`,
`\packageDescription`, `\packageAuthor`, `\packageMaintainer`,
`\packageDESCRIPTION` and `\packageIndices`.

Packages may also define their own common macros; these would be stored
in an `.Rd` file in `man/macros` in the package source
and will be installed into `help/macros` when the package is
installed. A package may also use the macros from a different package by
listing the other package in the '`RdMacros`' field in the
`DESCRIPTION` file.

---

### 2.14 Encoding

Rd files are text files and so it is impossible to deduce the encoding
they are written in unless ASCII: files with 8-bit characters could be
UTF-8, Latin-1, Latin-9, KOI8-R, EUC-JP, _etc_. So an `\encoding{}`
section must be used to specify the encoding if it is not ASCII. (The
`\encoding{}` section must be on a line by itself, and in particular one
containing no non-ASCII characters. The encoding declared in the
`DESCRIPTION` file will be used if none is declared in the
file.) The `Rd` files are converted to UTF-8 before parsing and
so the preferred encoding for the files themselves is now UTF-8.

Wherever possible, avoid non-ASCII chars in `Rd` files, and
even symbols such as '`<`', '`>`', '`$`',
'`^`', '`&`', '`|`', '`@`',
'`~`', and '`*`' outside 'verbatim' environments
(since they may disappear in fonts designed to render text). (Function
`showNonASCIIfile` in package **tools** can help in finding non-ASCII
bytes in the files.)

For convenience, encoding names '`latin1`' and
'`latin2`' are always recognized: these and '`UTF-8`'
are likely to work fairly widely. However, this does not mean that all
characters in UTF-8 will be recognized, and the coverage of non-Latin
characters[^110^](#FOOT110) is fairly low. Using LaTeX
`inputenx` (see `?Rd2pdf` in R) will give greater coverage of UTF-8.

The `\enc` command (see [Insertions](#Insertions)) can be used to
provide transliterations which will be used in conversions that do not
support the declared encoding.

The LaTeX conversion converts the file to UTF-8 from the declared
encoding, and includes a

```r
\inputencoding{utf8}
```

command, and this needs to be matched by a suitable invocation of the
`\usepackage{inputenc}` command. The R utility `R CMD Rd2pdf` looks at
the converted code and includes the encodings used: it might for example
use

```r
\usepackage[utf8]{inputenc}
```

(Use of `utf8` as an encoding requires LaTeX dated 2003/12/01 or later.
Also, the use of Cyrillic characters in '`UTF-8`' appears to
also need '`\usepackage[T2A]{fontenc}`', and `R CMD Rd2pdf`
includes this conditionally on the file `t2aenc.def` being
present and environment variable `_R_CYRILLIC_TEX_` being set.)

Note that this mechanism works best with Latin letters: the coverage of
UTF-8 in LaTeX is quite low.

---

### 2.15 Processing documentation files

There are several commands to process Rd files from the system command
line.

Using `R CMD Rdconv` one can convert R documentation format to other
formats, or extract the executable examples for run-time testing. The
currently supported conversions are to plain text, HTML and LaTeX as
well as extraction of the examples.

`R CMD Rd2pdf` generates PDF output from documentation in `Rd`
files, which can be specified either explicitly or by the path to a
directory with the sources of a package. In the latter case, a reference
manual for all documented objects in the package is created, including
the information in the `DESCRIPTION` files.

`R CMD Sweave` and `R CMD Stangle` process vignette-like documentation
files (e.g. Sweave vignettes with extension '`.Snw`' or
'`.Rnw`', or other non-Sweave vignettes). `R CMD Stangle` is
used to extract the R code fragments.

The exact usage and a detailed list of available options for all of
these commands can be obtained by running `R CMD command --help`, e.g.,
[R CMD Rdconv \--help]{.kbd}. All available commands can be listed using
[R \--help]{.kbd} (or [Rcmd \--help]{.kbd} under Windows).

All of these work under Windows. You may need to have installed the the
tools to build packages from source as described in the "R Installation
and Administration" manual, although typically all that is needed is a
LaTeX installation.

---

### 2.16 Editing Rd files

It can be very helpful to prepare `.Rd` files using a editor
which knows about their syntax and will highlight commands, indent to
show the structure and detect mis-matched braces, and so on.

The system most commonly used for this is some version of `Emacs`
(including `XEmacs`) with the ESS package (<https://ESS.R-project.org/>:
it is often is installed with `Emacs` but may need to be loaded, or even
installed, separately).

Another is the Eclipse IDE with the Stat-ET plugin
(<http://www.walware.de/goto/statet>), and (on Windows only) Tinn-R
(<http://sourceforge.net/projects/tinn-r/>).

People have also used LaTeX mode in a editor, as `.Rd` files
are rather similar to LaTeX files.

Some R front-ends provide editing support for `.Rd` files, for
example RStudio (<https://www.rstudio.com/>).

---
