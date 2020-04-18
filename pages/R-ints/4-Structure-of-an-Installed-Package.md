# 4 Structure of an Installed Package

---

---

• [Metadata](#Metadata)     
 • [Help](#Help)

---

The structure of a _source_ packages is described in [Creating R packages](./R-exts.html#Creating-R-packages) in Writing R Extensions:
this chapter is concerned with the structure of _installed_ packages.

An installed package has a top-level file `DESCRIPTION`, a copy
of the file of that name in the package sources with a
'`Built`' field appended, and file `INDEX`, usually
describing the objects on which help is available, a file
`NAMESPACE` if the package has a name space, optional files
such as `CITATION`, `LICENCE` and `NEWS`, and
any other files copied in from `inst`. It will have directories
`Meta`, `help` and `html` (even if the
package has no help pages), almost always has a directory `R`
and often has a directory `libs` to contain compiled code.
Other directories with known meaning to R are `data`,
`demo`, `doc` and `po`.

Function `library` looks for a namespace and if one is found passes
control to `loadNamespace`. Then `library` or `loadNamespace` looks for
file `R/pkgname`, warns if it is not found and otherwise
sources the code (using `sys.source`) into the package's environment,
then lazy-loads a database `R/sysdata` if present. So how R
code gets loaded depends on the contents of `R/pkgname`: a
standard template to load lazy-load databases are provided in
`share/R/nspackloader.R`.

Compiled code is usually loaded when the package's namespace is loaded
by a `useDynlib` directive in a `NAMESPACE` file or by the
package's `.onLoad` function. Conventionally compiled code is loaded by
a call to `library.dynam` and this looks in directory `libs`
(and in an appropriate sub-directory if sub-architectures are in use)
for a shared object (Unix-alike) or DLL (Windows).

Subdirectory `data` serves two purposes. In a package using
lazy-loading of data, it contains a lazy-load database `Rdata`,
plus a file `Rdata.rds` which contain a named character vector
used by `data()` in the (unusual) event that it is used for such a
package. Otherwise it is a copy of the `data` directory in the
sources, with saved images re-compressed if
`R CMD INSTALL --resave-data` was used.

Subdirectory `demo` supports the `demo` function, and is copied
from the sources.

Subdirectory `po` contains (in subdirectories) compiled message
catalogs.

---

### 4.1 Metadata

Directory `Meta` contains several files in `.rds` format, that
is serialized R objects written by `saveRDS`. All packages have files
`Rd.rds`, `hsearch.rds`, `links.rds`,
`features.rds`, and `package.rds`. Packages with
namespaces have a file `nsInfo.rds`, and those with data, demos
or vignettes have `data.rds`, `demo.rds` or
`vignette.rds` files.

The structure of these files (and their existence and names) is private
to R, so the description here is for those trying to follow the R
sources: there should be no reference to these files in non-base
packages.

File `package.rds` is a dump of information extracted from the
`DESCRIPTION` file. It is a list of several components. The
first, '`DESCRIPTION`', is a character vector, the
`DESCRIPTION` file as read by `read.dcf`. Further elements
'`Depends`', '`Suggests`', '`Imports`',
'`Rdepends`' and '`Rdepends2`' record the
'`Depends`', '`Suggests`' and '`Imports`'
fields. These are all lists, and can be empty. The first three have an
entry for each package named, each entry being a list of length 1 or 3,
which element '`name`' (the package name) and optional elements
'`op`' (a character string) and '`version`' (an object
of class '`"package_version"`'). Element '`Rdepends`'
is used for the first version dependency on R, and
'`Rdepends2`' is a list of zero or more R version
dependencies---each is a three-element list of the form described for
packages. Element '`Rdepends`' is no longer used, but it is
still potentially needed so R \< 2.7.0 can detect that the package was
not installed for it.

File `nsInfo.rds` records a list, a parsed version of the
`NAMESPACE` file.

File `Rd.rds` records a data frame with one row for each help
file. The columns are '`File`' (the file name with extension),
'`Name`' (the '`\name`' section), '`Type`'
(from the optional '`\docType`' section), '`Title`',
'`Encoding`', '`Aliases`', '`Concepts`' and
'`Keywords`'. All columns are character vectors apart from
'`Aliases`', which is a list of character vectors.

File `hsearch.rds` records the information to be used by
'`help.search`'. This is a list of four unnamed elements which
are character matrices for help files, aliases, keywords and concepts.
All the matrices have columns '`ID`' and '`Package`'
which are used to tie the aliases, keywords and concepts (the remaining
column of the last three elements) to a particular help file. The first
element has further columns '`LibPath`' (stored as `""` and
filled in what the file is loaded), '`name`',
'`title`', '`topic`' (the first alias, used when
presenting the results as '`pkgname::topic`') and
'`Encoding`'.

File `links.rds` records a named character vector, the names
being aliases and the values character strings of the form

```r
"../../pkgname/html/filename.html"
```

File `data.rds` records a two-column character matrix with
columns of dataset names and titles from the corresponding help file.
File `demo.rds` has the same structure for package demos.

File `vignette.rds` records a data frame with one row for each
'vignette' (`.[RS]nw` file in `inst/doc`) and with
columns '`File`' (the full file path in the sources),
'`Title`', '`PDF`' (the pathless file name of the
installed PDF version, if present), '`Depends`',
'`Keywords`' and '`R`' (the pathless file name of the
installed R code, if present).

---

### 4.2 Help

All installed packages, whether they had any `.Rd` files or
not, have `help` and `html` directories. The latter
normally only contains the single file `00Index.html`, the
package index which has hyperlinks to the help topics (if any).

Directory `help` contains files `AnIndex`,
`paths.rds` and `pkgname.rd[bx]`. The latter two files
are a lazy-load database of parsed `.Rd` files, accessed by
`tools:::fetchRdDB`. File `paths.rds` is a saved character
vector of the original path names of the `.Rd` files, used when
updating the database.

File `AnIndex` is a two-column tab-delimited file: the first
column contains the aliases defined in the help files and the second the
basename (without the `.Rd` or `.rd` extension) of the
file containing that alias. It is read by `utils:::index.search` to
search for files matching a topic (alias), and read by `scan` in
`utils:::matchAvailableTopics`, part of the completion system.

File `aliases.rds` is the same information as
`AnIndex` as a named character vector (names the topics, values
the file basename), for faster access.

---
