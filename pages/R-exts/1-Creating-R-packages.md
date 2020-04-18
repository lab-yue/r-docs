# 1 Creating R packages

---

Packages provide a mechanism for loading optional code, data and
documentation as needed. The R distribution itself includes about 30
packages.

In the following, we assume that you know the `library()` command,
including its `lib.loc` argument, and we also assume basic knowledge of
the `R CMD INSTALL` utility. Otherwise, please look at R's help pages on

```r
?library
?INSTALL
```

before reading on.

For packages which contain code to be compiled, a computing environment
including a number of tools is assumed; the "R Installation and
Administration" manual describes what is needed for each OS.

Once a source package is created, it must be installed by the command
`R CMD INSTALL`. See
[Add-on-packages](./R-admin.html#Add_002don-packages) in R Installation
and Administration.

Other types of extensions are supported (but rare): See [Package types](#Package-types).

Some notes on terminology complete this introduction. These will help
with the reading of this manual, and also in describing concepts
accurately when asking for help.

A _package_ is a directory of files which extend R, a _source package_
(the master files of a package), or a tarball containing the files of a
source package, or an _installed_ package, the result of running
`R CMD INSTALL` on a source package. On some platforms (notably macOS
and Windows) there are also _binary packages_, a zip file or tarball
containing the files of an installed package which can be unpacked
rather than installing from sources.

A package is **not**[^1^](#FOOT1) a _library_. The latter is
used in two senses in R documentation.

- A directory into which packages are installed, e.g.
  `/usr/lib/R/library`: in that sense it is sometimes
  referred to as a _library directory_ or _library tree_ (since the
  library is a directory which contains packages as directories, which
  themselves contain directories).
- That used by the operating system, as a shared, dynamic or static
  library or (especially on Windows) a DLL, where the second L stands
  for 'library'. Installed packages may contain compiled code in what
  is known on Unix-alikes as a _shared object_ and on Windows as a
  DLL. The concept of a _shared library_ (_dynamic library_ on macOS)
  as a collection of compiled code to which a package might link is
  also used, especially for R itself on some platforms. On most
  platforms these concepts are interchangeable (shared objects and
  DLLs can both be loaded into the R process and be linked against),
  but macOS distinguishes between shared objects (extension
  `.so`) and dynamic libraries (extension `.dylib`).

There are a number of well-defined operations on source packages.

- The most common is _installation_ which takes a source package and
  installs it in a library using `R CMD INSTALL` or
  `install.packages`.
- Source packages can be _built_. This involves taking a source
  directory and creating a tarball ready for distribution, including
  cleaning it up and creating PDF documentation from any _vignettes_
  it may contain. Source packages (and most often tarballs) can be
  _checked_, when a test installation is done and tested (including
  running its examples); also, the contents of the package are tested
  in various ways for consistency and portability.
- _Compilation_ is not a correct term for a package. Installing a
  source package which contains C, C++ or Fortran code will involve
  compiling that code. There is also the possibility of 'byte'
  compiling the R code in a package (using the facilities of package
  **compiler**): nowadays this is enabled by default for all packages.
  So _compiling_ a package may come to mean byte-compiling its R code.
- It used to be unambiguous to talk about _loading_ an installed
  package using `library()`, but since the advent of package
  namespaces this has been less clear: people now often talk about
  _loading_ the package's namespace and then _attaching_ the package
  so it becomes visible on the search path. Function `library`
  performs both steps, but a package's namespace can be loaded without
  the package being attached (for example by calls like
  `splines::ns`).

The concept of _lazy loading_ of code or data is mentioned at several
points. This is part of the installation, always selected for R code but
optional for data. When used the R objects of the package are created at
installation time and stored in a database in the `R` directory
of the installed package, being loaded into the session at first use.
This makes the R session start up faster and use less (virtual) memory.
(For technical details, see [Lazy loading](./R-ints.html#Lazy-loading)
in R Internals.)

CRAN is a network of WWW sites holding the R distributions and
contributed code, especially R packages. Users of R are encouraged to
join in the collaborative project and to submit their own packages to
CRAN: current instructions are linked from
<https://CRAN.R-project.org/banner.shtml#submitting>.

---

• [Package structure](#Package-structure)     
 • [Configure and cleanup](#Configure-and-cleanup)     
 • [Checking and building packages](#Checking-and-building-packages)     
 • [Writing package vignettes](#Writing-package-vignettes)     
 • [Package namespaces](#Package-namespaces)     
 • [Writing portable packages](#Writing-portable-packages)     
 • [Diagnostic messages](#Diagnostic-messages)     
 • [Internationalization](#Internationalization)     
 • [CITATION files](#CITATION-files)     
 • [Package types](#Package-types)     
 • [Services](#Services)

---

---

### 1.1 Package structure

The sources of an R package consists of a subdirectory containing a
files `DESCRIPTION` and `NAMESPACE`, and the
subdirectories `R`, `data`, `demo`,
`exec`, `inst`, `man`, `po`,
`src`, `tests`, `tools` and
`vignettes` (some of which can be missing, but which should not
be empty). The package subdirectory may also contain files
`INDEX`, `configure`, `cleanup`,
`LICENSE`, `LICENCE` and `NEWS`. Other files
such as `INSTALL` (for non-standard installation instructions),
`README`/`README.md`[^2^](#FOOT2), or
`ChangeLog` will be ignored by R, but may be useful to end
users. The utility `R CMD build` may add files in a `build`
directory (but this should not be used for other purposes).

Except where specifically mentioned,[^3^](#FOOT3) packages
should not contain Unix-style 'hidden' files/directories (that is, those
whose name starts with a dot).

The `DESCRIPTION` and `INDEX` files are described in
the subsections below. The `NAMESPACE` file is described in the
section on [Package namespaces](#Package-namespaces).

The optional files `configure` and `cleanup` are
(Bourne) shell scripts which are, respectively, executed before and (if
option `--clean` was given) after installation on Unix-alikes,
see [Configure and cleanup](#Configure-and-cleanup). The analogues on
Windows are `configure.win` and `cleanup.win`.

For the conventions for files `NEWS` and `ChangeLog`
in the GNU project see
<https://www.gnu.org/prep/standards/standards.html#Documentation>.

The package subdirectory should be given the same name as the package.
Because some file systems (e.g., those on Windows and by default on OS
X) are not case-sensitive, to maintain portability it is strongly
recommended that case distinctions not be used to distinguish different
packages. For example, if you have a package named `foo`, do
not also create a package named `Foo`.

To ensure that file names are valid across file systems and supported
operating systems, the ASCII control characters as well as the
characters '`"`', '`*`', '`:`',
'`/`', '`<`', '`>`', '`?`',
'`\`', and '`|`' are not allowed in file names. In
addition, files with names '`con`', '`prn`',
'`aux`', '`clock$`', '`nul`',
'`com1`' to '`com9`', and '`lpt1`' to
'`lpt9`' after conversion to lower case and stripping possible
"extensions" (e.g., '`lpt5.foo.bar`'), are disallowed. Also,
file names in the same directory must not differ only by case (see the

#### 1.1.1 The `DESCRIPTION` file

The `DESCRIPTION` file contains basic information about the
package in the following format:

> +-----------------------------------------------------------------------+
> | |
> | `r | | Package: pkgname | | Version: 0.5-1 | | Date: 2015-01-01 | | Title: My First Collection of Functions | | Authors@R: c(person("Joe", "Developer", role = c("aut", "cre"), | | email = "Joe.Developer@some.domain.net"), | | person("Pat", "Developer", role = "aut"), | | person("A.", "User", role = "ctb", | | email = "A.User@whereever.net")) | | Author: Joe Developer [aut, cre], | | Pat Developer [aut], | | A. User [ctb] | | Maintainer: Joe Developer <Joe.Developer@some.domain.net> | | Depends: R (>= 3.1.0), nlme | | Suggests: MASS | | Description: A (one paragraph) description of what | | the package does and why it may be useful. | | License: GPL (>= 2) | | URL: https://www.r-project.org, http://www.another.url | | BugReports: https://pkgname.bugtracker.url | |` |
> | ::: |
> +-----------------------------------------------------------------------+

The format is that of a version of a 'Debian Control File' (see the help
for '`read.dcf`' and
<https://www.debian.org/doc/debian-policy/ch-controlfields.html>: R does
not require encoding in UTF-8 and does not support comments starting
with '`#`'). Fields start with an ASCII name immediately
followed by a colon: the value starts after the colon and a space.
Continuation lines (for example, for descriptions longer than one line)
start with a space or tab. Field names are case-sensitive: all those
used by R are capitalized.

For maximal portability, the `DESCRIPTION` file should be
written entirely in ASCII --- if this is not possible it must contain an
'`Encoding`' field (see below).

Several optional fields take _logical values_: these can be specified as
'`yes`', '`true`', '`no`' or
'`false`': capitalized values are also accepted.

The '`Package`', '`Version`', '`License`',
'`Description`', '`Title`', '`Author`', and
'`Maintainer`' fields are mandatory, all other fields are
optional. Fields '`Author`' and '`Maintainer`' can be
auto-generated from '`Authors@R`', and may be omitted if the
latter is provided: however if they are not ASCII we recommend that they
are provided.

The mandatory '`Package`' field gives the name of the package.
This should contain only (ASCII) letters, numbers and dot, have at least
two characters and start with a letter and not end in a dot. If it needs
explaining, this should be done in the '`Description`' field
(and not the '`Title`' field).

The mandatory '`Version`' field gives the version of the
package. This is a sequence of at least _two_ (and usually three)
non-negative integers separated by single '`.`' or
'`-`' characters. The canonical form is as shown in the
example, and a version such as '`0.01`' or '`0.01.0`'
will be handled as if it were '`0.1-0`'. It is **not** a
decimal number, so for example `0.9 < 0.75` since `9 < 75`.

The mandatory '`License`' field is discussed in the next
subsection.

The mandatory '`Title`' field should give a _short_ description
of the package. Some package listings may truncate the title to 65
characters. It should use _title case_ (that is, use capitals for the
principal words: `tools::toTitleCase` can help you with this), not use
any markup, not have any continuation lines, and not end in a period
(unless part of ...). Do not repeat the package name: it is often used
prefixed by the name. Refer to other packages and external software in
single quotes, and to book titles (and similar) in double quotes.

The mandatory '`Description`' field should give a
_comprehensive_ description of what the package does. One can use
several (complete) sentences, but only one paragraph. It should be
intelligible to all the intended readership (e.g. for a CRAN package to
all CRAN users). It is good practice not to start with the package name,
'This package' or similar. As with the '`Title`' field, double
quotes should be used for quotations (including titles of books and
articles), and single quotes for non-English usage, including names of
other packages and external software. This field should also be used for
explaining the package name if necessary. URLs should be enclosed in
angle brackets, e.g. '`<https://www.r-project.org>`': see also
[Specifying URLs](#Specifying-URLs).

The mandatory '`Author`' field describes who wrote _the
package_. It is a plain text field intended for human readers, but not
for automatic processing (such as extracting the email addresses of all
listed contributors: for that use '`Authors@R`'). Note that all
significant contributors must be included: if you wrote an R wrapper for
the work of others included in the `src` directory, you are not
the sole (and maybe not even the main) author.

The mandatory '`Maintainer`' field should give a _single_ name
followed by a _valid_ (RFC 2822) email address in angle brackets. It
should not end in a period or comma. This field is what is reported by
the `maintainer` function and used by `bug.report`. For a CRAN package
it should be a _person_, not a mailing list and not a corporate entity:
do ensure that it is valid and will remain valid for the lifetime of the
package.

Note that the _display name_ (the part before the address in angle
brackets) should be enclosed in double quotes if it contains
non-alphanumeric characters such as comma or period. (The current
standard, RFC 5322, allows periods but RFC 2822 did not.)

Both '`Author`' and '`Maintainer`' fields can be
omitted if a suitable '`Authors@R`' field is given. This field
can be used to provide a refined and machine-readable description of the
package "authors" (in particular specifying their precise _roles_),
_via_ suitable R code. It should create an object of class `"person"`,
by either a call to `person` or a series of calls (one per "author")
concatenated by `c()`: see the example `DESCRIPTION` file
above. The roles can include '`"aut"`' (author) for full
authors, '`"cre"`' (creator) for the package maintainer, and
'`"ctb"`' (contributor) for other contributors,
'`"cph"`' (copyright holder), among others. See `?person` for
more information. Note that no role is assumed by default.
Auto-generated package citation information takes advantage of this
specification. The '`Author`' and '`Maintainer`'
fields are auto-generated from it if needed when
building[^5^](#FOOT5) or installing.

An optional '`Copyright`' field can be used where the copyright
holder(s) are not the authors. If necessary, this can refer to an
installed file: the convention is to use file
`inst/COPYRIGHTS`.

The optional '`Date`' field gives the _release date_ of the
current version of the package. It is strongly
recommended[^6^](#FOOT6) to use the '`yyyy-mm-dd`'
format conforming to the ISO 8601 standard.

The '`Depends`', '`Imports`', '`Suggests`',
'`Enhances`', '`LinkingTo`' and
'`Additional_repositories`' fields are discussed in a later
subsection.

Dependencies external to the R system should be listed in the
'`SystemRequirements`' field, possibly amplified in a separate
`README` file.

The '`URL`' field may give a list of URLs separated by commas
or whitespace, for example the homepage of the author or a page where
additional material describing the software can be found. These URLs are
converted to active hyperlinks in CRAN package listings. See [Specifying URLs](#Specifying-URLs).

The '`BugReports`' field may contain a single URL to which bug
reports about the package should be submitted. This URL will be used by
`bug.report` instead of sending an email to the maintainer. A browser is
opened for a '`http://`' or '`https://`' URL. To
specify another email address for bug reports, use '`Contact`'
instead: however `bug.report` will try to extract an email address
(preferably from a '`mailto:`' URL or enclosed in angle
brackets) from '`BugReports`'.

Base and recommended packages (i.e., packages contained in the R source
distribution or available from CRAN and recommended to be included in
every binary distribution of R) have a '`Priority`' field with
value '`base`' or '`recommended`', respectively. These
priorities must not be used by other packages.

A '`Collate`' field can be used for controlling the collation
order for the R code files in a package when these are processed for
package installation. The default is to collate according to the
'`C`' locale. If present, the collate specification must list
_all_ R code files in the package (taking possible OS-specific
subdirectories into account, see [Package subdirectories](#Package-subdirectories)) as a whitespace separated list
of file paths relative to the `R` subdirectory. Paths
containing white space or quotes need to be quoted. An OS-specific
collation field ('`Collate.unix`' or
'`Collate.windows`') will be used in preference to
'`Collate`'.

The '`LazyData`' logical field controls whether the R datasets
use lazy-loading. A '`LazyLoad`' field was used in versions
prior to 2.14.0, but now is ignored.

The '`KeepSource`' logical field controls if the package code
is sourced using `keep.source = TRUE` or `FALSE`: it might be needed
exceptionally for a package designed to always be used with
`keep.source = TRUE`.

The '`ByteCompile`' logical field controls if the package code
is to be byte-compiled on installation: the default is to byte-compile.
This can be overridden by installing with flag
`--no-byte-compile`.

The '`StagedInstall`' logical field controls if package
installation is 'staged', that is done to a temporary location and moved
to the final location when successfully completed. This field was
introduced in R 3.6.0 and it true by default: it is considered to be a
temporary measure which may be withdrawn in future.

The '`ZipData`' logical field has been ignored since R 2.13.0.

The '`Biarch`' logical field is used on Windows to select the
`INSTALL` option `--force-biarch` for this package.

The '`BuildVignettes`' logical field can be set to a false
value to stop `R CMD build` from attempting to build the vignettes, as
well as preventing[^7^](#FOOT7) `R CMD check` from testing this.
This should only be used exceptionally, for example if the PDFs include
large figures which are not part of the package sources (and hence only
in packages which do not have an Open Source license).

The '`VignetteBuilder`' field names (in a comma-separated list)
packages that provide an engine for building vignettes. These may
include the current package, or ones listed in '`Depends`',
'`Suggests`' or '`Imports`'. The **utils** package is
always implicitly appended. See [Non-Sweave vignettes](#Non_002dSweave-vignettes) for details. Note that if, for
example, a vignette has engine '`knitr::rmarkdown`', then
[**knitr**](https://CRAN.R-project.org/package=knitr) provides the
engine but both **knitr** and
[**rmarkdown**](https://CRAN.R-project.org/package=rmarkdown) are needed
for using it, so _both_ these packages need to be in the
'`VignetteBuilder`' field and at least suggested (as
**rmarkdown** is only suggested by **knitr**, and hence not available
automatically along with it). Many packages using
[**knitr**](https://CRAN.R-project.org/package=knitr) also need the
package [**formatR**](https://CRAN.R-project.org/package=formatR) which
it suggests and so the user package needs to do so too and include this
in '`VignetteBuilder`'.

If the `DESCRIPTION` file is not entirely in ASCII it should
contain an '`Encoding`' field specifying an encoding. This is
used as the encoding of the `DESCRIPTION` file itself and of
the `R` and `NAMESPACE` files, and as the default
encoding of `.Rd` files. The examples are assumed to be in this
encoding when running `R CMD check`, and it is used for the encoding of
the `CITATION` file. Only encoding names `latin1`, `latin2` and `UTF-8`
are known to be portable. (Do not specify an encoding unless one is
actually needed: doing so makes the package _less_ portable. If a
package has a specified encoding, you should run `R CMD build` etc in a
locale using that encoding.)

The '`NeedsCompilation`' field should be set to `"yes"` if the
package contains code which to be compiled, otherwise `"no"` (when the
package could be installed from source on any platform without
additional tools). This is used by `install.packages(type = "both")` in
R \>= 2.15.2 on platforms where binary packages are the norm: it is
normally set by `R CMD build` or the repository assuming compilation is
required if and only if the package has a `src` directory.

The '`OS_type`' field specifies the OS(es) for which the
package is intended. If present, it should be one of `unix` or
`windows`, and indicates that the package can only be installed on a
platform with '`.Platform$OS.type`' having that value.

The '`Type`' field specifies the type of the package: see
[Package types](#Package-types).

One can add subject classifications for the content of the package using
the fields '`Classification/ACM`' or
'`Classification/ACM-2012`' (using the Computing Classification
System of the Association for Computing Machinery,
<http://www.acm.org/about/class/>; the former refers to the 1998
version), '`Classification/JEL`' (the Journal of Economic
Literature Classification System,
<https://www.aeaweb.org/econlit/jelCodes.php>, or
'`Classification/MSC`' or '`Classification/MSC-2010`'
(the Mathematics Subject Classification of the American Mathematical
Society, <http://www.ams.org/msc/>; the former refers to the 2000
version). The subject classifications should be comma-separated lists of
the respective classification codes, e.g.,
'`Classification/ACM: G.4, H.2.8, I.5.1`'.

A '`Language`' field can be used to indicate if the package
documentation is not in English: this should be a comma-separated list
of standard (not private use or grandfathered) IETF language tags as
currently defined by RFC 5646 (<https://tools.ietf.org/html/rfc5646>,
see also <https://en.wikipedia.org/wiki/IETF_language_tag>), i.e., use
language subtags which in essence are 2-letter ISO 639-1
(<https://en.wikipedia.org/wiki/ISO_639-1>) or 3-letter ISO 639-3
(<https://en.wikipedia.org/wiki/ISO_639-3>) language codes.

An '`RdMacros`' field can be used to hold a comma-separated
list of packages from which the current package will import
`Rd` macro definitions. These package should also be listed in
'`Imports`', '`Suggests`' or '`Depends`'. The
macros in these packages will be imported after the system macros, in
the order listed in the '`RdMacros`' field, before any macro
definitions in the current package are loaded. Macro definitions in
individual `.Rd` files in the `man` directory are
loaded last, and are local to later parts of that file. In case of
duplicates, the last loaded definition will be used[^8^](#FOOT8)
Both `R CMD Rd2pdf` and `R CMD Rdconv` have an optional flag
`--RdMacros=pkglist`. The option is also a comma-separated list
of package names, and has priority over the value given in
`DESCRIPTION`. Packages using `Rd` macros should
depend on R 3.2.0 or later.

> **Note:** There should be no '`Built`' or
> '`Packaged`' fields, as these are added by the package
> management tools.

There is no restriction on the use of other fields not mentioned here
(but using other capitalizations of these field names would cause
confusion). Fields `Note`, `Contact` (for contacting the
authors/developers[^9^](#FOOT9)) and `MailingList` are in common
use. Some repositories (including CRAN and R-forge) add their own
fields.

---

#### 1.1.2 Licensing

Licensing for a package which might be distributed is an important but
potentially complex subject.

It is very important that you include license information! Otherwise, it
may not even be legally correct for others to distribute copies of the
package, let alone use it.

The package management tools use the concept of 'free or open source
software' (FOSS, e.g., <https://en.wikipedia.org/wiki/FOSS>) licenses:
the idea being that some users of R and its packages want to restrict
themselves to such software. Others need to ensure that there are no
restrictions stopping them using a package, e.g. forbidding commercial
or military use. It is a central tenet of FOSS software that there are
no restrictions on users nor usage.

Do not use the '`License`' field for information on copyright
holders: if needed, use a '`Copyright`' field.

The mandatory '`License`' field in the `DESCRIPTION`
file should specify the license of the package in a standardized form.
Alternatives are indicated _via_ vertical bars. Individual
specifications must be one of

- One of the "standard" short specifications

```r
GPL-2 GPL-3 LGPL-2 LGPL-2.1 LGPL-3 AGPL-3 Artistic-2.0
BSD_2_clause BSD_3_clause MIT
```

as made available _via_ <https://www.R-project.org/Licenses/> and
contained in subdirectory `share/licenses` of the R source
or home directory.

- The names or abbreviations of other licenses contained in the
  license data base in file `share/licenses/license.db` in
  the R source or home directory, possibly (for versioned licenses)
  followed by a version restriction of the form '`(op v)`'
  with '`op`' one of the comparison operators '`<`',
  '`<=`', '`>`', '`>=`', '`==`',
  or '`!=`' and '`v`' a numeric version
  specification (strings of non-negative integers separated by
  '`.`'), possibly combined _via_ '`,`' (see below
  for an example). For versioned licenses, one can also specify the
  name followed by the version, or combine an existing abbreviation
  and the version with a '`-`'.

  Abbreviations `GPL` and `LGPL` are ambiguous and
  usually[^10^](#FOOT10) taken to mean any version of the
  license: but it is better not to use them.

- One of the strings '`file LICENSE`' or
  '`file LICENCE`' referring to a file named
  `LICENSE` or `LICENCE` in the package (source and
  installation) top-level directory.

- The string '`Unlimited`', meaning that there are no
  restrictions on distribution or use other than those imposed by
  relevant laws (including copyright laws).

If a package license _restricts_ a base license (where permitted, e.g.,
using GPL-3 or AGPL-3 with an attribution clause), the additional terms
should be placed in file `LICENSE` (or `LICENCE`), and
the string '`+ file LICENSE`' (or '`+ file LICENCE`',
respectively) should be appended to the corresponding individual license
specification. Note that several commonly used licenses do not permit
restrictions: this includes GPL-2 and hence any specification which
includes it.

Examples of standardized specifications include

```r
License: GPL-2
License: LGPL (>= 2.0, < 3) | Mozilla Public License
License: GPL-2 | file LICENCE
License: GPL (>= 2) | BSD_3_clause + file LICENSE
License: Artistic-2.0 | AGPL-3 + file LICENSE
```

Please note in particular that "Public domain" is not a valid license,
since it is not recognized in some jurisdictions.

Please ensure that the license you choose also covers any dependencies
(including system dependencies) of your package: it is particularly
important that any restrictions on the use of such dependencies are
evident to people reading your `DESCRIPTION` file.

Fields '`License_is_FOSS`' and
'`License_restricts_use`' may be added by repositories where
information cannot be computed from the name of the license.
'`License_is_FOSS: yes`' is used for licenses which are known
to be FOSS, and '`License_restricts_use`' can have values
'`yes`' or '`no`' if the `LICENSE` file is
known to restrict users or usage, or known not to. These are used by,
e.g., the `available.packages` filters.

The optional file `LICENSE`/`LICENCE` contains a copy
of the license of the package. To avoid any confusion only include such
a file if it is referred to in the '`License`' field of the
`DESCRIPTION` file.

Whereas you should feel free to include a license file in your _source_
distribution, please do not arrange to _install_ yet another copy of the
GNU `COPYING` or `COPYING.LIB` files but refer to the
copies on <https://www.R-project.org/Licenses/> and included in the R
distribution (in directory `share/licenses`). Since files named
`LICENSE` or `LICENCE` _will_ be installed, do not use
these names for standard license files. To include comments about the
licensing rather than the body of a license, use a file named something
like `LICENSE.note`.

A few "standard" licenses are rather license templates which need
additional information to be completed _via_
'`+ file LICENSE`'.

---

#### 1.1.3 Package Dependencies

The '`Depends`' field gives a comma-separated list of package
names which this package depends on. Those packages will be attached
before the current package when `library` or `require` is called. Each
package name may be optionally followed by a comment in parentheses
specifying a version requirement. The comment should contain a
comparison operator, whitespace and a valid version number, e.g.
'`MASS (>= 3.1-20)`'.

The '`Depends`' field can also specify a dependence on a
certain version of R --- e.g., if the package works only with R version
3.6.0 or later, include '`R (>= 3.6)`' in the
'`Depends`' field. (As here, trailing zeroes can be dropped and
it is recommended that they are.) You can also require a certain SVN
revision for R-devel or R-patched, e.g.
'`R (>= 2.14.0), R (>= r56550)`' requires a version later than
R-devel of late July 2011 (including released versions of 2.14.0).

It makes no sense to declare a dependence on `R` without a version
specification, nor on the package **base**: this is an R package and
package **base** is always available.

A package or '`R`' can appear more than once in the
'`Depends`' field, for example to give upper and lower bounds
on acceptable versions.

It is inadvisable to use a dependence on R with patchlevel (the third
digit) other than zero. Doing so with packages which others depend on
will cause the other packages to become unusable under earlier versions
in the series, and e.g. versions 3.x.1 are widely used throughout the
Northern Hemisphere academic year.

Both `library` and the R package checking facilities use this field:
hence it is an error to use improper syntax or misuse the
'`Depends`' field for comments on other software that might be
needed. The R `INSTALL` facilities check if the version of R used is
recent enough for the package being installed, and the list of packages
which is specified will be attached (after checking version
requirements) before the current package.

The '`Imports`' field lists packages whose namespaces are
imported from (as specified in the `NAMESPACE` file) but which
do not need to be attached. Namespaces accessed by the '`::`'
and '`:::`' operators must be listed here, or in
'`Suggests`' or '`Enhances`' (see below). Ideally this
field will include all the standard packages that are used, and it is
important to include S4-using packages (as their class definitions can
change and the `DESCRIPTION` file is used to decide which
packages to re-install when this happens). Packages declared in the
'`Depends`' field should not also be in the
'`Imports`' field. Version requirements can be specified and
are checked when the namespace is loaded.

The '`Suggests`' field uses the same syntax as
'`Depends`' and lists packages that are not necessarily needed.
This includes packages used only in examples, tests or vignettes (see
[Writing package vignettes](#Writing-package-vignettes)), and packages
loaded in the body of functions. E.g., suppose an
example[^11^](#FOOT11) from package **foo** uses a dataset from
package **bar**. Then it is not necessary to have **bar** use **foo**
unless one wants to execute all the examples/tests/vignettes: it is
useful to have **bar**, but not necessary. Version requirements can be
specified but should be checked by the code which uses the package.

Finally, the '`Enhances`' field lists packages "enhanced" by
the package at hand, e.g., by providing methods for classes from these
packages, or ways to handle objects from these packages (so several
packages have '`Enhances: chron`' because they can handle
datetime objects from
[**chron**](https://CRAN.R-project.org/package=chron) even though they
prefer R's native datetime functions). Version requirements can be
specified, but are currently not used. Such packages cannot be required
to check the package: any tests which use them must be conditional on
the presence of the package. (If your tests use e.g. a dataset from
another package it should be in '`Suggests`' and not
'`Enhances`'.)

The general rules are

- A package should be listed in only one of these fields.
- Packages whose namespace only is needed to load the package using
  `library(pkgname)` should be listed in the '`Imports`'
  field and not in the '`Depends`' field. Packages listed in
  `import` or `importFrom` directives in the `NAMESPACE` file
  should almost always be in '`Imports`' and not
  '`Depends`'.
- Packages that need to be attached to successfully load the package
  using `library(pkgname)` must be listed in the '`Depends`'
  field.
- All packages that are needed[^12^](#FOOT12) to successfully
  run `R CMD check` on the package must be listed in one of
  '`Depends`' or '`Suggests`' or
  '`Imports`'. Packages used to run examples or tests
  conditionally (e.g. _via_ `if(require(pkgname))`) should be listed
  in '`Suggests`' or '`Enhances`'. (This allows
  checkers to ensure that all the packages needed for a complete check
  are installed.)
- Packages needed to use datasets from the package should be in
  '`Imports`': this includes those needed to define S4
  classes used.

In particular, packages providing "only" data for examples or vignettes
should be listed in '`Suggests`' rather than
'`Depends`' in order to make lean installations possible.

Version dependencies in the '`Depends`' and
'`Imports`' fields are used by `library` when it loads the
package, and `install.packages` checks versions for the
'`Depends`', '`Imports`' and (for
`dependencies = TRUE`) '`Suggests`' fields.

It is important that the information in these fields is complete and
accurate: it is for example used to compute which packages depend on an
updated package and which packages can safely be installed in parallel.

This scheme was developed before all packages had namespaces (R 2.14.0
in October 2011), and good practice changed once that was in place.

Field '`Depends`' should nowadays be used rarely, only for
packages which are intended to be put on the search path to make their
facilities available to the end user (and not to the package itself):
for example it makes sense that a user of package
[**latticeExtra**](https://CRAN.R-project.org/package=latticeExtra)
would want the functions of package
[**lattice**](https://CRAN.R-project.org/package=lattice) made
available.

Almost always packages mentioned in '`Depends`' should also be
imported from in the `NAMESPACE` file: this ensures that any
needed parts of those packages are available when some other package
imports the current package.

The '`Imports`' field should not contain packages which are not
imported from (_via_ the `NAMESPACE` file or `::` or `:::`
operators), as all the packages listed in that field need to be
installed for the current package to be installed. (This is checked by
`R CMD check`.)

R code in the package should call `library` or `require` only
exceptionally. Such calls are never needed for packages listed in
'`Depends`' as they will already be on the search path. It used
to be common practice to use `require` calls for packages listed in
'`Suggests`' in functions which used their functionality, but
nowadays it is better to access such functionality _via_ `::` calls.

A package that wishes to make use of header files in other packages
needs to declare them as a comma-separated list in the field
'`LinkingTo`' in the `DESCRIPTION` file. For example

```r
LinkingTo: link1, link2
```

The '`LinkingTo`' field can have a version requirement which is
checked at installation.

Specifying a package in '`LinkingTo`' suffices if these are C++
headers containing source code or static linking is done at
installation: the packages do not need to be (and usually should not be)
listed in the '`Depends`' or '`Imports`' fields. This
includes CRAN package [**BH**](https://CRAN.R-project.org/package=BH)
and almost all users of
[**RcppArmadillo**](https://CRAN.R-project.org/package=RcppArmadillo)
and [**RcppEigen**](https://CRAN.R-project.org/package=RcppEigen).

For another use of '`LinkingTo`' see [Linking to native
routines in other
packages](#Linking-to-native-routines-in-other-packages).

The '`Additional_repositories`' field is a comma-separated list
of repository URLs where the packages named in the other fields may be
found. It is currently used by `R CMD check` to check that the packages
can be found, at least as source packages (which can be installed on any
platform).

---

• [Suggested packages](#Suggested-packages)

---

---

#### 1.1.3.1 Suggested packages

Note that someone wanting to run the examples/tests/vignettes may not
have a suggested package available (and it may not even be possible to
install it for that platform). The recommendation used to be to make
their use conditional _via_ `if(require("pkgname"))`: this is OK if that
conditioning is done in examples/tests/vignettes, although using
`if(requireNamespace("pkgname"))` is preferred, if possible.

However, using `require` for conditioning _in package code_ is not good
practice as it alters the search path for the rest of the session and
relies on functions in that package not being masked by other `require`
or `library` calls. It is better practice to use code like

```r
   if (requireNamespace("rgl", quietly = TRUE)) {
      rgl::plot3d(...)
   } else {
      ## do something else not involving rgl.
   }
```

Note the use of `rgl::` as that object would not necessarily be visible
(and if it is, it need not be the one from that namespace: `plot3d`
occurs in several other packages). If the intention is to give an error
if the suggested package is not available, simply use e.g.
`rgl::plot3d`.

If the conditional code produces `print` output, function
`withAutoprint` can be useful.

Note that the recommendation to use suggested packages conditionally in
tests does also apply to packages used to manage test suites: a
notorious example was
[**testthat**](https://CRAN.R-project.org/package=testthat) which in
version 1.0.0 contained illegal C++ code and hence could not be
installed on standards-compliant platforms.

Some people have assumed that a 'recommended' package in
'`Suggests`' can safely be used unconditionally, but this is
not so. (R can be installed without recommended packages, and which
packages are 'recommended' may change.)

As noted above, packages in '`Enhances`' _must_ be used
conditionally and hence objects within them should always be accessed
_via_ `::`.

On most systems, `R CMD check` can be run with only those packages
declared in '`Depends`' and '`Imports`' by setting
environment variable `_R_CHECK_DEPENDS_ONLY_=true`, whereas setting
`_R_CHECK_SUGGESTS_ONLY_=true` also allows suggested packages, but not
those in '`Enhances`' nor those not mentioned in the
`DESCRIPTION` file. It is recommended that a package is checked
with each of these set, as well as with neither.

---

#### 1.1.4 The `INDEX` file

The optional file `INDEX` contains a line for each sufficiently
interesting object in the package, giving its name and a description
(functions such as print methods not usually called explicitly might not
be included). Normally this file is missing and the corresponding
information is automatically generated from the documentation sources
(using `tools::Rdindex()`) when installing from source.

The file is part of the information given by `library(help = pkgname)`.

Rather than editing this file, it is preferable to put customized
information about the package into an overview help page (see
[Documenting packages](#Documenting-packages)) and/or a vignette (see
[Writing package vignettes](#Writing-package-vignettes)).

---

#### 1.1.5 Package subdirectories

The `R` subdirectory contains R code files, only. The code
files to be installed must start with an ASCII (lower or upper case)
letter or digit and have one of the extensions[^13^](#FOOT13)
`.R`, `.S`, `.q`, `.r`, or
`.s`. We recommend using `.R`, as this extension seems
to be not used by any other software. It should be possible to read in
the files using `source()`, so R objects must be created by assignments.
Note that there need be no connection between the name of the file and
the R objects created by it. Ideally, the R code files should only
directly assign R objects and definitely should not call functions with
side effects such as `require` and `options`. If computations are
required to create objects these can use code 'earlier' in the package
(see the '`Collate`' field) plus functions in the
'`Depends`' packages provided that the objects created do not
depend on those packages except _via_ namespace imports.

Two exceptions are allowed: if the `R` subdirectory contains a
file `sysdata.rda` (a saved image of one or more R objects:
please use suitable compression as suggested by `tools::resaveRdaFiles`,
and see also the '`SysDataCompression`' `DESCRIPTION`
field.) this will be lazy-loaded into the namespace environment -- this
is intended for system datasets that are not intended to be
user-accessible _via_ `data`. Also, files ending in '`.in`'
will be allowed in the `R` directory to allow a
`configure` script to generate suitable files.

Only ASCII characters (and the control characters tab, formfeed, LF and
CR) should be used in code files. Other characters are accepted in
comments[^14^](#FOOT14), but then the comments may not be
readable in e.g. a UTF-8 locale. Non-ASCII characters in object names
will normally[^15^](#FOOT15) fail when the package is
installed. Any byte will be allowed in a quoted character string but
'`\uxxxx`' escapes should be used for non-ASCII characters.
However, non-ASCII character strings may not be usable in some locales
and may display incorrectly in others.

Various R functions in a package can be used to initialize and clean up.
See [Load hooks](#Load-hooks).

The `man` subdirectory should contain (only) documentation
files for the objects in the package in _R documentation_ (Rd) format.
The documentation filenames must start with an ASCII (lower or upper
case) letter or digit and have the extension `.Rd` (the
default) or `.rd`. Further, the names must be valid in
'`file://`' URLs, which means[^16^](#FOOT16) they must
be entirely ASCII and not contain '`%`'. See [Writing R
documentation files](#Writing-R-documentation-files), for more
information. Note that all user-level objects in a package should be
documented; if a package `pkg` contains user-level objects
which are for "internal" use only, it should provide a file
`pkg-internal.Rd` which documents all such objects, and clearly
states that these are not meant to be called by the user. See e.g. the
sources for package **grid** in the R distribution. Note that packages
which use internal objects extensively should not export those objects
from their namespace, when they do not need to be documented (see
[Package namespaces](#Package-namespaces)).

Having a `man` directory containing no documentation files may
give an installation error.

The `man` subdirectory may contain a subdirectory named
`macros`; this will contain source for user-defined Rd macros.
(See [User-defined macros](#User_002ddefined-macros).) These use the Rd
format, but may not contain anything but macro definitions, comments and
whitespace.

The `R` and `man` subdirectories may contain
OS-specific subdirectories named `unix` or `windows`.

The sources and headers for the compiled code are in `src`,
plus optionally a file `Makevars` or `Makefile`. When
a package is installed using `R CMD INSTALL`, `make` is used to control
compilation and linking into a shared object for loading into R. There
are default `make` variables and rules for this (determined when R is
configured and recorded in `R_HOME/etcR_ARCH/Makeconf`),
providing support for C, C++, fixed- or free-form Fortran, Objective C
and Objective C++[^17^](#FOOT17) with associated extensions
`.c`, `.cc` or `.cpp`, `.f`,
`.f90` or `.f95`, `.m`, and `.mm`,
respectively. We recommend using `.h` for headers, also for
C++[^18^](#FOOT18) or Fortran 9x include files. (Use of
extension `.C` for C++ is no longer supported.) Files in the
`src` directory should not be hidden (start with a dot), and
hidden files will under some versions of R be ignored.

It is not portable (and may not be possible at all) to mix all these
languages in a single package. Because R itself uses it, we know that C
and fixed-form Fortran can be used together, and mixing C, C++ and
Fortran usually work for the platform's native compilers.

If your code needs to depend on the platform there are certain defines
which can used in C or C++. On all Windows builds (even 64-bit ones)
'`_WIN32`' will be defined: on 64-bit Windows builds also
'`_WIN64`', and on macOS '`__APPLE__`' is
defined.[^19^](#FOOT19)

The default rules can be tweaked by setting
macros[^20^](#FOOT20) in a file `src/Makevars` (see
[Using Makevars](#Using-Makevars)). Note that this mechanism should be
general enough to eliminate the need for a package-specific
`src/Makefile`. If such a file is to be distributed,
considerable care is needed to make it general enough to work on all R
platforms. If it has any targets at all, it should have an appropriate
first target named '`all`' and a (possibly empty) target
'`clean`' which removes all files generated by running `make`
(to be used by '`R CMD INSTALL --clean`' and
'`R CMD INSTALL --preclean`'). There are platform-specific file
names on Windows: `src/Makevars.win` takes precedence over
`src/Makevars` and `src/Makefile.win` must be used.
Some `make` programs require makefiles to have a complete final line,
including a newline.

A few packages use the `src` directory for purposes other than
making a shared object (e.g. to create executables). Such packages
should have files `src/Makefile` and
`src/Makefile.win` (unless intended for only Unix-alikes or
only Windows).

In very special cases packages may create binary files other than the
shared objects/DLLs in the `src` directory. Such files will not
be installed in a multi-architecture setting since
`R CMD INSTALL --libs-only` is used to merge multiple sub-architectures
and it only copies shared objects/DLLs. If a package wants to install
other binaries (for example executable programs), it should provide an R
script `src/install.libs.R` which will be run as part of the
installation in the `src` build directory _instead of_ copying the
shared objects/DLLs. The script is run in a separate R environment
containing the following variables: `R_PACKAGE_NAME` (the name of the
package), `R_PACKAGE_SOURCE` (the path to the source directory of the
package), `R_PACKAGE_DIR` (the path of the target installation directory
of the package), `R_ARCH` (the arch-dependent part of the path, often
empty), `SHLIB_EXT` (the extension of shared objects) and `WINDOWS`
(`TRUE` on Windows, `FALSE` elsewhere). Something close to the default
behavior could be replicated with the following
`src/install.libs.R` file:

```r
files <- Sys.glob(paste0("*", SHLIB_EXT))
dest <- file.path(R_PACKAGE_DIR, paste0('libs', R_ARCH))
dir.create(dest, recursive = TRUE, showWarnings = FALSE)
file.copy(files, dest, overwrite = TRUE)
if(file.exists("symbols.rds"))
    file.copy("symbols.rds", dest, overwrite = TRUE)
```

On the other hand, executable programs could be installed along the
lines of

```r
execs <- c("one", "two", "three")
if(WINDOWS) execs <- paste0(execs, ".exe")
if ( any(file.exists(execs)) ) {
  dest <- file.path(R_PACKAGE_DIR,  paste0('bin', R_ARCH))
  dir.create(dest, recursive = TRUE, showWarnings = FALSE)
  file.copy(execs, dest, overwrite = TRUE)
}
```

Note the use of architecture-specific subdirectories of `bin`
where needed.

The `data` subdirectory is for data files: See [Data in packages](#Data-in-packages).

The `demo` subdirectory is for R scripts (for running _via_
`demo()`) that demonstrate some of the functionality of the package.
Demos may be interactive and are not checked automatically, so if
testing is desired use code in the `tests` directory to achieve
this. The script files must start with a (lower or upper case) letter
and have one of the extensions `.R` or `.r`. If
present, the `demo` subdirectory should also have a
`00Index` file with one line for each demo, giving its name and
a description separated by a tab or at least three spaces. (This index
file is not generated automatically.) Note that a demo does not have a
specified encoding and so should be an ASCII file (see [Encoding issues](#Encoding-issues)). Function `demo()` will use the package
encoding if there is one, but this is mainly useful for non-ASCII
comments.

The contents of the `inst` subdirectory will be copied
recursively to the installation directory. Subdirectories of
`inst` should not interfere with those used by R (currently,
`R`, `data`, `demo`, `exec`,
`libs`, `man`, `help`, `html` and
`Meta`, and earlier versions used `latex`,
`R-ex`). The copying of the `inst` happens after
`src` is built so its `Makefile` can create files to
be installed. To exclude files from being installed, one can specify a
list of exclude patterns in file `.Rinstignore` in the
top-level source directory. These patterns should be Perl-like regular
expressions (see the help for `regexp` in R for the precise details),
one per line, to be matched case-insensitively against the file and
directory paths, e.g. `doc/.*[.]png$` will exclude all PNG
files in `inst/doc` based on the extension.

Note that with the exceptions of `INDEX`,
`LICENSE`/`LICENCE` and `NEWS`, information
files at the top level of the package will _not_ be installed and so not
be known to users of Windows and macOS compiled packages (and not seen
by those who use `R CMD INSTALL` or `install.packages` on the tarball).
So any information files you wish an end user to see should be included
in `inst`. Note that if the named exceptions also occur in
`inst`, the version in `inst` will be that seen in the
installed package.

Things you might like to add to `inst` are a
`CITATION` file for use by the `citation` function, and a
`NEWS.Rd` file for use by the `news` function. See its help
page for the specific format restrictions of the `NEWS.Rd`
file.

Another file sometimes needed in `inst` is `AUTHORS`
or `COPYRIGHTS` to specify the authors or copyright holders
when this is too complex to put in the `DESCRIPTION` file.

Subdirectory `tests` is for additional package-specific test
code, similar to the specific tests that come with the R distribution.
Test code can either be provided directly in a `.R` (or
`.r` as from R 3.4.0) file, or _via_ a `.Rin` file
containing code which in turn creates the corresponding `.R`
file (e.g., by collecting all function objects in the package and then
calling them with the strangest arguments). The results of running a
`.R` file are written to a `.Rout` file. If there is a
corresponding[^21^](#FOOT21) `.Rout.save` file, these
two are compared, with differences being reported but not causing an
error. The directory `tests` is copied to the check area, and
the tests are run with the copy as the working directory and with
`R_LIBS` set to ensure that the copy of the package installed during
testing will be found by `library(pkg_name)`. Note that the
package-specific tests are run in a vanilla R session without setting
the random-number seed, so tests which use random numbers will need to
set the seed to obtain reproducible results (and it can be helpful to do
so in all cases, to avoid occasional failures when tests are run).

If directory `tests` has a subdirectory `Examples`
containing a file `pkg-Ex.Rout.save`, this is compared to the output
file for running the examples when the latter are checked. Reference
output should be produced without having the `--timings` option
set (and note that `--as-cran` sets it).

If reference output is included for examples, tests or vignettes do make
sure that it is fully reproducible, as it will be compared verbatim to
that produced in a check run, unless the '`IGNORE_RDIFF`'
markup is used. Things which trip maintainers up include displayed
version numbers from loading other packages, printing numerical results
to an unreproducibly high precision and printing timings. Another trap
is small values which are in fact rounding error from zero: consider
using `zapsmall`.

Subdirectory `exec` could contain additional executable scripts
the package needs, typically scripts for interpreters such as the shell,
Perl, or Tcl. NB: only files (and not directories) under `exec`
are installed (and those with names starting with a dot are ignored),
and they are all marked as executable (mode `755`, moderated by
'`umask`') on POSIX platforms. Note too that this is not
suitable for executable _programs_ since some platforms (including
Windows) support multiple architectures using the same installed package
directory.

Subdirectory `po` is used for files related to _localization_:
see [Internationalization](#Internationalization).

Subdirectory `tools` is the preferred place for auxiliary files
needed during configuration, and also for sources need to re-create
scripts (e.g. M4 files for `autoconf`).

---

#### 1.1.6 Data in packages

The `data` subdirectory is for data files, either to be made
available _via_ lazy-loading or for loading using `data()`. (The choice
is made by the '`LazyData`' field in the `DESCRIPTION`
file: the default is not to do so.) It should not be used for other data
files needed by the package, and the convention has grown up to use
directory `inst/extdata` for such files.

Data files can have one of three types as indicated by their extension:
plain R code (`.R` or `.r`), tables (`.tab`,
`.txt`, or `.csv`, see `?data` for the file formats,
and note that `.csv` is **not** the
standard[^22^](#FOOT22) CSV format), or `save()` images
(`.RData` or `.rda`). The files should not be hidden
(have names starting with a dot). Note that R code should be if possible
"self-sufficient" and not make use of extra functionality provided by
the package, so that the data file can also be used without having to
load the package or its namespace: it should run as silently as possible
and not change the `search()` path by attaching packages or other
environments.

Images (extensions `.RData`[^23^](#FOOT23) or
`.rda`) can contain references to the namespaces of packages
that were used to create them. Preferably there should be no such
references in data files, and in any case they should only be to
packages listed in the `Depends` and `Imports` fields, as otherwise it
may be impossible to install the package. To check for such references,
load all the images into a vanilla R session, run `str()` on all the
datasets, and look at the output of `loadedNamespaces()`.

Particular care is needed where a dataset or one of its components is of
an S4 class, especially if the class is defined in a different package.
First, the package containing the class definition has to be available
to do useful things with the dataset, so that package must be listed in
`Imports` or `Depends` (even if this gives a check warning about unused
imports). Second, the definition of an S4 class can change, and often is
unnoticed when in a package with a different author. So it may be wiser
to use the `.R` form and use that to create the dataset object
when needed (loading package namespaces but not attaching them by using
`requireNamespace(pkg, quietly = TRUE)` and using `pkg::` to refer to
objects in the namespace).

If you are not using '`LazyData`' and either your data files
are large or e.g., you use `data/foo.R` scripts to produce your
data, loading your namespace, you can speed up installation by providing
a file `datalist` in the `data` subdirectory. This
should have one line per topic that `data()` will find, in the format
'`foo`' if `data(foo)` provides '`foo`', or
'`foo: bar bah`' if `data(foo)` provides '`bar`' and
'`bah`'. `R CMD build` will automatically add a
`datalist` file to `data` directories of over 1Mb,
using the function `tools::add_datalist`.

Tables (`.tab`, `.txt`, or `.csv` files) can
be compressed by `gzip`, `bzip2` or `xz`, optionally with additional
extension `.gz`, `.bz2` or `.xz`.

If your package is to be distributed, do consider the resource
implications of large datasets for your users: they can make packages
very slow to download and use up unwelcome amounts of storage space, as
well as taking many seconds to load. It is normally best to distribute
large datasets as `.rda` images prepared by
`save(, compress = TRUE)` (the default). Using `bzip2` or `xz`
compression will usually reduce the size of both the package tarball and
the installed package, in some cases by a factor of two or more.

Package **tools** has a couple of functions to help with data images:
`checkRdaFiles` reports on the way the image was saved, and
`resaveRdaFiles` will re-save with a different type of compression,
including choosing the best type for that particular image.

Some packages using '`LazyData`' will benefit from using a form
of compression other than `gzip` in the installed lazy-loading database.
This can be selected by the `--data-compress` option to
`R CMD INSTALL` or by using the '`LazyDataCompression`' field
in the `DESCRIPTION` file. Useful values are `bzip2`, `xz` and
the default, `gzip`. The only way to discover which is best is to try
them all and look at the size of the `pkgname/data/Rdata.rdb`
file.

The analogue for `sysdata.rda` is field
'`SysDataCompression`': the default is `xz` for files bigger
than 1MB otherwise `gzip`.

Lazy-loading is not supported for very large datasets (those which when
serialized exceed 2GB, the limit for the format on 32-bit platforms).

---

#### 1.1.7 Non-R scripts in packages

Code which needs to be compiled (C, C++, Fortran ...) is included in the
`src` subdirectory and discussed elsewhere in this document.

Subdirectory `exec` could be used for scripts for interpreters
such as the shell, BUGS, JavaScript, Matlab, Perl, php
([**amap**](https://CRAN.R-project.org/package=amap)), Python or Tcl
([**Simile**](https://CRAN.R-project.org/package=Simile)), or even R.
However, it seems more common to use the `inst` directory, for
example `WriteXLS/inst/Perl`, `NMF/inst/m-files`,
`RnavGraph/inst/tcl`, `RProtoBuf/inst/python` and
`emdbook/inst/BUGS` and `gridSVG/inst/js`.

Java code is a special case: except for very small programs,
`.java` files should be byte-compiled (to a `.class`
file) and distributed as part of a `.jar` file: the
conventional location for the `.jar` file(s) is
`inst/java`. It is desirable (and required under an Open Source
license) to make the Java source files available: this is best done in a
top-level `java` directory in the package---the source files
should not be installed.

If your package requires one of these interpreters or an extension then
this should be declared in the '`SystemRequirements`' field of
its `DESCRIPTION` file. (Users of Java most often do so _via_
[**rJava**](https://CRAN.R-project.org/package=rJava), when depending
on/importing that suffices.)

Windows and Mac users should be aware that the Tcl extensions
'`BWidget`' and '`Tktable`' which are currently
included with the R for Windows and in the macOS installers _are_
extensions and do need to be declared for users of other platforms (and
that '`Tktable`' is less widely available than it used to be,
including not in the main repositories for major Linux distributions).

'`BWidget`' needs to be installed by the user on other OSes.
This is fairly easy to do: first find the Tcl/Tk search path:

```r
library(tcltk)
strsplit(tclvalue('auto_path'), " ")[[1]]
```

then download the sources from
<https://sourceforge.net/projects/tcllib/files/BWidget/> and at the
command line run something like

```r
tar xf bwidget-1.9.8.tar.gz
sudo mv bwidget-1.9.8 /usr/local/lib
```

substituting a location on the Tcl/Tk search path for
`/usr/local/lib` if needed.

---

#### 1.1.8 Specifying URLs

URLs in many places in the package documentation will be converted to
clickable hyperlinks in at least some of their renderings. So care is
needed that their forms are correct and portable.

The full URL should be given, including the scheme (often
'`http://`' or '`https://`') and a final
'`/`' for references to directories.

Spaces in URLs are not portable and how they are handled does vary by
HTTP server and by client. There should be no space in the host part of
an '`http://`' URL, and spaces in the remainder should be
encoded, with each space replaced by '`%20`'.

Other characters may benefit from being encoded: see the help on
`URLencode()`.

The canonical URL for a CRAN package is

```r
https://cran.r-project.org/package=pkgname
```

and not a version starting
'`https://cran.r-project.org/web/packages/pkgname`'.

---

### 1.2 Configure and cleanup

Note that most of this section is specific to Unix-alikes: see the
comments later on about the Windows port of R.

If your package needs some system-dependent configuration before
installation you can include an executable
(Bourne[^24^](#FOOT24)) shell script `configure` in
your package which (if present) is executed by `R CMD INSTALL` before
any other action is performed. This can be a script created by the
Autoconf mechanism, but may also be a script written by yourself. Use
this to detect if any nonstandard libraries are present such that
corresponding code in the package can be disabled at install time rather
than giving error messages when the package is compiled or used. To
summarize, the full power of Autoconf is available for your extension
package (including variable substitution, searching for libraries,
etc.).

Under a Unix-alike only, an executable (Bourne shell) script
`cleanup` is executed as the last thing by `R CMD INSTALL` if
option `--clean` was given, and by `R CMD build` when preparing
the package for building from its source.

As an example consider we want to use functionality provided by a (C or
Fortran) library `foo`. Using Autoconf, we can create a configure script
which checks for the library, sets variable `HAVE_FOO` to `TRUE` if it
was found and to `FALSE` otherwise, and then substitutes this value into
output files (by replacing instances of '`@HAVE_FOO@`' in input
files with the value of `HAVE_FOO`). For example, if a function named
`bar` is to be made available by linking against library `foo` (i.e.,
using `-lfoo`), one could use

```r
AC_CHECK_LIB(foo, fun, [HAVE_FOO=TRUE], [HAVE_FOO=FALSE])
AC_SUBST(HAVE_FOO)
......
AC_CONFIG_FILES([foo.R])
AC_OUTPUT
```

in `configure.ac` (assuming Autoconf 2.50 or later).

The definition of the respective R function in `foo.R.in` could
be

```r
foo <- function(x) {
    if(!@HAVE_FOO@)
      stop("Sorry, library ‘foo’ is not available")
    ...
```

From this file `configure` creates the actual R source file
`foo.R` looking like

```r
foo <- function(x) {
    if(!FALSE)
      stop("Sorry, library ‘foo’ is not available")
    ...
```

if library `foo` was not found (with the desired functionality). In this
case, the above R code effectively disables the function.

One could also use different file fragments for available and missing
functionality, respectively.

You will very likely need to ensure that the same C compiler and
compiler flags are used in the `configure` tests as when
compiling R or your package. Under a Unix-alike, you can achieve this by
including the following fragment early in `configure.ac`
(_before_ calling `AC_PROG_CC`)

```r
: ${R_HOME=`R RHOME`}
if test -z "${R_HOME}"; then
  echo "could not determine R_HOME"
  exit 1
fi
CC=`"${R_HOME}/bin/R" CMD config CC`
CFLAGS=`"${R_HOME}/bin/R" CMD config CFLAGS`
CPPFLAGS=`"${R_HOME}/bin/R" CMD config CPPFLAGS`
```

(Using '`${R_HOME}/bin/R`' rather than just '`R`' is
necessary in order to use the correct version of R when running the
script as part of `R CMD INSTALL`, and the quotes since
'`${R_HOME}`' might contain spaces.)

If your code does load checks then you may also need

```r
LDFLAGS=`"${R_HOME}/bin/R" CMD config LDFLAGS`
```

and packages written with C++ need to pick up the details for the C++
compiler and switch the current language to C++ by something like

```r
CXX=`"${R_HOME}/bin/R" CMD config CXX`
if test -z "$CXX"; then
  AC_MSG_ERROR([No C++ compiler is available])
fi
CXXFLAGS=`"${R_HOME}/bin/R" CMD config CXXFLAGS`
AC_LANG(C++)
```

The latter is important, as for example C headers may not be available
to C++ programs or may not be written to avoid C++ name-mangling. Note
that an R installation is not required to have a C++ compiler so
'`CXX`' may be empty.

You can use `R CMD config` to get the value of the basic configuration
variables, and also the header and library flags necessary for linking a
front-end executable program against R, see [R CMD config \--help]
for details. If you do, it is essential that you use both the command
and the appropriate flags, so that for example '`CC`' must
always be used with '`CFLAGS`' and (for code to be linked into
a shared library) '`CPICFLAGS`'. For Fortran, be careful to use
'`FC FFLAGS FPICFLAGS`' for fixed-form Fortran and
'`FC FCFLAGS FPICFLAGS`' for free-form Fortran. (Packages
intended to be used with R versions before 3.6.0 should use the legacy
forms '`F77 FFLAGS FPICFLAGS`' and
'`FC FCFLAGS FCPICFLAGS`', which are still accepted.)

To check for an external BLAS library using the `AX_BLAS` macro from the
official Autoconf Macro Archive, one can simply do

```r
FC=`"${R_HOME}/bin/R" CMD config FC`
FCLAGS=`"${R_HOME}/bin/R" CMD config FFLAGS`
AC_PROG_FC
FLIBS=`"${R_HOME}/bin/R" CMD config FLIBS`
AX_BLAS([], AC_MSG_ERROR([could not find your BLAS library], 1))
```

Note that `FLIBS` as determined by R must be used to ensure that Fortran
code works on all R platforms.

**N.B.**: If the `configure` script creates files, e.g.
`src/Makevars`, you do need a `cleanup` script to remove them.
Otherwise `R CMD build` may ship the files that are created. For
example, package [**RODBC**](https://CRAN.R-project.org/package=RODBC)
has

```r
#!/bin/sh

rm -f config.* src/Makevars src/config.h
```

As this example shows, `configure` often creates working files such as
`config.log`.

If your configure script needs auxiliary files, it is recommended that
you ship them in a `tools` directory (as R itself does).

You should bear in mind that the configure script will not be used on
Windows systems. If your package is to be made publicly available,
please give enough information for a user on a non-Unix-alike platform
to configure it manually, or provide a `configure.win` script
to be used on that platform. (Optionally, there can be a
`cleanup.win` script. Both should be shell scripts to be
executed by `ash`, which is a minimal version of Bourne-style `sh`.)
When `configure.win` is run the environment variables `R_HOME`
(which uses '`/`' as the file separator), `R_ARCH` and Use
`R_ARCH_BIN` will be set. Use `R_ARCH` to decide if this is a 64-bit
build (its value there is '`/x64`') and to install DLLs to the
correct place (`${R_HOME}/libs${R_ARCH}`). Use `R_ARCH_BIN` to
find the correct place under the `bin` directory, e.g.
`${R_HOME}/bin${R_ARCH_BIN}/Rscript.exe`.

In some rare circumstances, the configuration and cleanup scripts need
to know the location into which the package is being installed. An
example of this is a package that uses C code and creates two shared
object/DLLs. Usually, the object that is dynamically loaded by R is
linked against the second, dependent, object. On some systems, we can
add the location of this dependent object to the object that is
dynamically loaded by R. This means that each user does not have to set
the value of the `LD_LIBRARY_PATH` (or equivalent) environment variable,
but that the secondary object is automatically resolved. Another example
is when a package installs support files that are required at run time,
and their location is substituted into an R data structure at
installation time.
The
names of the top-level library directory (i.e., specifiable \_via\* the
'`-l`' argument) and the directory of the package itself are
made available to the installation scripts _via_ the two
shell/environment variables `R_LIBRARY_DIR` and `R_PACKAGE_DIR`.
Additionally, the name of the package (e.g. '`survival`' or
'`MASS`') being installed is available from the environment
variable `R_PACKAGE_NAME`. (Currently the value of `R_PACKAGE_DIR` is
always `${R_LIBRARY_DIR}/${R_PACKAGE_NAME}`, but this used not to be the
case when versioned installs were allowed. Its main use is in
`configure.win` scripts for the installation path of external
software's DLLs.) Note that the value of `R_PACKAGE_DIR` may contain
spaces and other shell-unfriendly characters, and so should be quoted in
makefiles and configure scripts.

One of the more tricky tasks can be to find the headers and libraries of
external software. One tool which is increasingly available on
Unix-alikes (but not by default[^25^](#FOOT25) on macOS) to do
this is `pkg-config`. The `configure` script will need to test
for the presence of the command itself (see for example package
[**Cairo**](https://CRAN.R-project.org/package=Cairo)), and if present
it can be asked if the software is installed, of a suitable version and
for compilation/linking flags by e.g.

```r
$ pkg-config --exists ‘QtCore >= 4.0.0’  # check the status
$ pkg-config --modversion QtCore
4.8.7
$ pkg-config --cflags QtCore
-DQT_SHARED -I/usr/include/QtCore
$ pkg-config --libs QtCore
-lQtCore
$ pkg-config --static --libs QtCore
-lQtCore -lpthread -lz -lm -ldl -lgthread-2.0 -pthread -lglib-2.0 -lrt
```

Note that `pkg-config --libs` gives the information required to link
against the default version[^26^](#FOOT26) of that library
(usually the dynamic one), and `pkg-config --static --libs` may be
needed if the static library is to be used.

Sometimes the name by which the software is known to `pkg-config` is not
what one might expect (e.g. '`gtk+-2.0`' even for 2.22). To get
a complete list use

```r
pkg-config --list-all | sort
```

If using Autoconf it is good practice to include all the Autoconf
sources in the the package (and required for an Open Source package).
This will include the file
`configure.ac`[^27^](#FOOT27) in the top-level
directory of the package. If extensions written in `m4` are needed,
these should be included under the directory `tools` and
included in `configure.ac` _via_ e.g.,

```r
m4_include([tools/ax_pthread.m4])
```

One source of such extensions is the 'Autoconf Archive'
(<https://www.gnu.org/software/autoconf-archive>. It is not safe to
assume this is installed on users' machines, so the extension should be
shipped with the package (taking care to comply with its licence).

---

• [Using Makevars](#Using-Makevars)     
 • [Configure example](#Configure-example)     
 • [Using F9x code](#Using-F9x-code)     
 • [Using C++11 code](#Using-C_002b_002b11-code)     
 • [Using C++14 code](#Using-C_002b_002b14-code)     
 • [Using C++17 code](#Using-C_002b_002b17-code)

---

---

#### 1.2.1 Using `Makevars`

---

• [OpenMP support](#OpenMP-support)     
 • [Using pthreads](#Using-pthreads)     
 • [Compiling in sub-directories](#Compiling-in-sub_002ddirectories)

---

Sometimes writing your own `configure` script can be avoided by
supplying a file `Makevars`: also one of the most common uses
of a `configure` script is to make `Makevars` from
`Makevars.in`.

A `Makevars` file is a makefile and is used as one of several
makefiles by `R CMD SHLIB` (which is called by `R CMD INSTALL` to
compile code in the `src` directory). It should be written if
at all possible in a portable style, in particular (except for
`Makevars.win`) without the use of GNU extensions.

The most common use of a `Makevars` file is to set additional
preprocessor options (for example include paths and definitions) for
C/C++ files _via_ `PKG_CPPFLAGS`, and additional compiler flags by
setting `PKG_CFLAGS`, `PKG_CXXFLAGS` or `PKG_FFLAGS`, for C, C++ or
Fortran respectively (see [Creating shared objects](#Creating-shared-objects)).

**N.B.**: Include paths are preprocessor options, not compiler options,
and **must** be set in `PKG_CPPFLAGS` as otherwise platform-specific
paths (e.g. '`-I/usr/local/include`') will take precedence.
`PKG_CPPFLAGS` should contain '`-I`', '`-D`',
'`-U`' and (where supported) '`-include`' and
'`-pthread`' options: everything else should be a compiler
flag.

`Makevars` can also be used to set flags for the linker, for
example '`-L`' and '`-l`' options, _via_ `PKG_LIBS`.

When writing a `Makevars` file for a package you intend to
distribute, take care to ensure that it is not specific to your
compiler: flags such as `-O2 -Wall -pedantic` (and all other
`-W` flags: for the Oracle compilers these are used to pass
arguments to compiler phases) are all specific to GCC.

Also, do not set variables such as `CPPFLAGS`, `CFLAGS` etc.: these
should be settable by users (sites) through appropriate personal
(site-wide) `Makevars` files. See [Customizing package compilation](./R-admin.html#Customizing-package-compilation) in R
Installation and Administration,

There are some macros[^28^](#FOOT28) which are set whilst
configuring the building of R itself and are stored in
`R_HOME/etcR_ARCH/Makeconf`. That makefile is included as a
`Makefile` _after_ `Makevars[.win]`, and the macros it
defines can be used in macro assignments and make command lines in the
latter. These include

`FLIBS`

:

    A macro containing the set of libraries need to link Fortran code.
    This may need to be included in `PKG_LIBS`: it will normally be
    included automatically if the package contains Fortran source files
    in the `src` directory.

`BLAS_LIBS`

:

    A macro containing the BLAS libraries used when building R. This may
    need to be included in `PKG_LIBS`. Beware that if it is empty then
    the R executable will contain all the double-precision and
    double-complex BLAS routines, but no single-precision nor complex
    routines. If `BLAS_LIBS` is included, then `FLIBS` also needs to
    be[^29^](#FOOT29) included following it, as most BLAS
    libraries are written at least partially in Fortran.

`LAPACK_LIBS`

:

    A macro containing the LAPACK libraries (and paths where
    appropriate) used when building R. This may need to be included in
    `PKG_LIBS`. It may point to a dynamic library `libRlapack` which
    contains the main double-precision LAPACK routines as well as those
    double-complex LAPACK routines needed to build R, or it may point to
    an external LAPACK library, or may be empty if an external BLAS
    library also contains LAPACK.

    \[`libRlapack` includes all the double-precision LAPACK routines
    which were current in 2003: a list of which routines are included is
    in file `src/modules/lapack/README`. Note that an external
    LAPACK/BLAS library need not do so, as some were 'deprecated' (and
    not compiled by default) in LAPACK 3.6.0 in late 2015.\]

    For portability, the macros `BLAS_LIBS` and `FLIBS` should always be
    included *after* `LAPACK_LIBS` (and in that order).

`SAFE_FFLAGS`

:

    A macro containing flags which are needed to circumvent
    over-optimization of FORTRAN code: it is might be
    '`-g -O2 -ffloat-store`' or
    '`-g -O2 -msse2 -mfpmath=sse`' on '`ix86`'
    platforms using `gfortran`. Note that this is **not** an additional
    flag to be used as part of `PKG_FFLAGS`, but a replacement for
    `FFLAGS`. See the example later in this section.

Setting certain macros in `Makevars` will prevent `R CMD SHLIB`
setting them: in particular if `Makevars` sets
'`OBJECTS`' it will not be set on the `make` command line. This
can be useful in conjunction with implicit rules to allow other types of
source code to be compiled and included in the shared object. It can
also be used to control the set of files which are compiled, either by
excluding some files in `src` or including some files in
subdirectories. For example

```r
OBJECTS = 4dfp/endianio.o 4dfp/Getifh.o R4dfp-object.o
```

Note that `Makevars` should not normally contain targets, as it
is included before the default makefile and `make` will call the first
target, intended to be `all` in the default makefile. If you really need
to circumvent that, use a suitable (phony) target `all` before any
actual targets in `Makevars.[win]`: for example package
[**fastICA**](https://CRAN.R-project.org/package=fastICA) used to have

```r
PKG_LIBS = @BLAS_LIBS@

SLAMC_FFLAGS=$(R_XTRA_FFLAGS) $(FPICFLAGS) $(SHLIB_FFLAGS) $(SAFE_FFLAGS)

all: $(SHLIB)

slamc.o: slamc.f
        $(FC) $(SLAMC_FFLAGS) -c -o slamc.o slamc.f
```

needed to ensure that the LAPACK routines find some constants without
infinite looping. The Windows equivalent was

```r
all: $(SHLIB)

slamc.o: slamc.f
        $(FC) $(SAFE_FFLAGS) -c -o slamc.o slamc.f
```

(since the other macros are all empty on that platform, and R's internal
BLAS was not used). Note that the first target in `Makevars`
will be called, but for back-compatibility it is best named `all`.

If you want to create and then link to a library, say using code in a
subdirectory, use something like

```r
.PHONY: all mylibs

all: $(SHLIB)
$(SHLIB): mylibs

mylibs:
        (cd subdir; $(MAKE))
```

Be careful to create all the necessary dependencies, as there is no
guarantee that the dependencies of `all` will be run in a particular
order (and some of the CRAN build machines use multiple CPUs and
parallel makes). In particular,

```r
all: mylibs
```

does **not** suffice. GNU make does allow the construct

```r
.NOTPARALLEL: all
all: mylibs $(SHLIB)
```

but that is not portable. `dmake` and `pmake` allow the similar
`.NO_PARALLEL`, also not portable: some variants of `pmake` accept
`.NOTPARALLEL` as an alias for `.NO_PARALLEL`.

Note that on Windows it is required that `Makevars[.win]` does
create a DLL: this is needed as it is the only reliable way to ensure
that building a DLL succeeded. If you want to use the `src`
directory for some purpose other than building a DLL, use a
`Makefile.win` file.

It is sometimes useful to have a target '`clean`' in
`Makevars` or `Makevars.win`: this will be used by
`R CMD build` to clean up (a copy of) the package sources. When it is
run by `build` it will have fewer macros set, in particular not
`$(SHLIB)`, nor `$(OBJECTS)` unless set in the file itself. It would
also be possible to add tasks to the target '`shlib-clean`'
which is run by `R CMD INSTALL` and `R CMD SHLIB` with options
`--clean` and `--preclean`.

If you want to run R code in `Makevars`, e.g. to find
configuration information, please do ensure that you use the correct
copy of `R` or `Rscript`: there might not be one in the path at all, or
it might be the wrong version or architecture. The correct way to do
this is _via_

```r
"$(R_HOME)/bin$(R_ARCH_BIN)/Rscript" filename
"$(R_HOME)/bin$(R_ARCH_BIN)/Rscript" -e ‘R expression’
```

where `$(R_ARCH_BIN)` is only needed currently on Windows.

Environment or make variables can be used to select different macros for
32- and 64-bit code, for example (GNU `make` syntax, allowed on Windows)

```r
ifeq "$(WIN)" "64"
PKG_LIBS = value for 64-bit Windows
else
PKG_LIBS = value for 32-bit Windows
endif
```

On Windows there is normally a choice between linking to an import
library or directly to a DLL. Where possible, the latter is much more
reliable: import libraries are tied to a specific toolchain, and in
particular on 64-bit Windows two different conventions have been
commonly used. So for example instead of

```r
PKG_LIBS = -L$(XML_DIR)/lib -lxml2
```

one can use

```r
PKG_LIBS = -L$(XML_DIR)/bin -lxml2
```

since on Windows `-lxxx` will look in turn for

```r
libxxx.dll.a
xxx.dll.a
libxxx.a
xxx.lib
libxxx.dll
xxx.dll
```

where the first and second are conventionally import libraries, the
third and fourth often static libraries (with `.lib` intended for Visual
C++), but might be import libraries. See for example
<https://sourceware.org/binutils/docs-2.20/ld/WIN32.html#WIN32>.

The fly in the ointment is that the DLL might not be named
`libxxx.dll`, and in fact on 32-bit Windows there is a
`libxml2.dll` whereas on one build for 64-bit Windows the DLL
is called `libxml2-2.dll`. Using import libraries can cover
over these differences but can cause equal difficulties.

If static libraries are available they can save a lot of problems with
run-time finding of DLLs, especially when binary packages are to be
distributed and even more when these support both architectures. Where
using DLLs is unavoidable we normally arrange (_via_
`configure.win`) to ship them in the same directory as the
package DLL.

---

#### 1.2.1.1 OpenMP support

There is some support for packages which wish to use
OpenMP[^30^](#FOOT30). The `make` macros

```r
SHLIB_OPENMP_CFLAGS
SHLIB_OPENMP_CXXFLAGS
SHLIB_OPENMP_FFLAGS
```

are available for use in `src/Makevars` or
`src/Makevars.win`. Include the appropriate macro in
`PKG_CFLAGS`, `PKG_CXXFLAGS` and so on, and also in `PKG_LIBS` (but see
below for Fortran). C/C++ code that needs to be conditioned on the use
of OpenMP can be used inside `#ifdef _OPENMP`: note that some toolchains
used for R (including Apple's for macOS and some others using
`clang`[^31^](#FOOT31)) have no OpenMP support at all, not even
`omp.h`.

For example, a package with C code written for OpenMP should have in
`src/Makevars` the lines

```r
PKG_CFLAGS = $(SHLIB_OPENMP_CFLAGS)
PKG_LIBS = $(SHLIB_OPENMP_CFLAGS)
```

Note that the macro `SHLIB_OPENMP_CXXFLAGS` applies to the default C++11
compiler and not necessarily to the C++98/14/17 compiler: users of the
latter should do their own `configure` checks. If you do use your own
checks, make sure that OpenMP support is complete by compiling and
linking an OpenMP-using program: on some platforms the runtime library
is optional and on others that library depends on other optional
libraries.

Some care is needed when compilers are from different families which may
use different OpenMP runtimes (e.g. `clang` _vs_ GCC including
`gfortran`, although it is often possible to use the `clang` runtime
with GCC but not _vice versa_: however `gfortran` 9.x may generate calls
not in the `clang` runtime). For a package with Fortran code using
OpenMP the appropriate lines are

```r
PKG_FFLAGS = $(SHLIB_OPENMP_FFLAGS)
PKG_LIBS = $(SHLIB_OPENMP_CFLAGS)
```

as the C compiler will be used to link the package code. There are
platforms on which this does not work _for some OpenMP-using code_ and
installation will fail, so portable packages wanting to use Fortran code
with OpenMP need to test their usage for themselves. An alternative for
a package with only Fortran sources using OpenMP is to use a file
`src/Makefile` (and `src/Makefile.win`) something like

```r
PKG_FFLAGS = $(SHLIB_OPENMP_FFLAGS)
PKG_LIBS = $(SHLIB_OPENMP_FFLAGS) $(LAPACK_LIBS) $(BLAS_LIBS) $(FLIBS)
SHLIB_LD = $(SHLIB_FCLD)
SHLIB_LDFLAGS = $(SHLIB_FCLDFLAGS)
SHLIB = pkgname$(SHLIB_EXT)

all: $(SHLIB)

$(SHLIB): $(OBJECTS)
        $(SHLIB_LINK) -o $ $(OBJECTS) $(ALL_LIBS)
```

Since R \>= 3.6.2 a further alternative is to use

```r
USE_FC_TO_LINK =
PKG_FFLAGS = $(SHLIB_OPENMP_FFLAGS)
PKG_LIBS = $(SHLIB_OPENMP_FFLAGS)
```

in `src/Makevars` or `src/Makevsars.win`.

It is not portable to use OpenMP with more than one of C, C++ and
Fortran in a single package since it is not uncommon that the compilers
are of different families.

For portability, any C/C++ code using the `omp_*` functions should
include the `omp.h` header: some compilers (but not all)
include it when OpenMP mode is switched on (e.g. _via_ flag
`-fopenmp`).

There is nothing[^32^](#FOOT32) to say what version of OpenMP
is supported: version 3.1 (and much of 4.0) is supported by recent
versions of the Linux, Windows and Solaris platforms, but portable
packages cannot assume that end users have recent versions. Apple builds
of `clang` on macOS currently have no OpenMP support, but CRAN binary
packages are built with a `clang`-based toolchain which supports OpenMP.
<http://www.openmp.org/resources/openmp-compilers-tools> gives some idea
of what compilers support what versions.

The performance of OpenMP varies substantially between platforms. The
Windows implementation has substantial
overheads[^33^](#FOOT33), so is only beneficial if quite
substantial tasks are run in parallel. Also, on Windows new threads are
started with the default[^34^](#FOOT34) FPU control word, so
computations done on OpenMP threads will not make use of
extended-precision arithmetic which is the default for the main process.

Do not include these macros unless your code does make use of OpenMP
(possibly for C++ via included external headers): this can result in the
OpenMP runtime being linked in, threads being started, ....

Calling any of the R API from threaded code is 'for experts only' and
strongly discouraged. Many functions in the R API modify internal R data
structures and might corrupt these data structures if called
simultaneously from multiple threads. Most R API functions can signal
errors, which must only happen on the R main thread. Also, external
libraries (e.g. LAPACK) may not be thread-safe.

Packages are not standard-alone programs, and an R process could contain
more than one OpenMP-enabled package as well as other components (for
example, an optimized BLAS) making use of OpenMP. So careful
consideration needs to be given to resource usage. OpenMP works with
parallel regions, and for most implementations the default is to use as
many threads as 'CPUs' for such regions. Parallel regions can be nested,
although it is common to use only a single thread below the first level.
The correctness of the detected number of 'CPUs' and the assumption that
the R process is entitled to use them all are both dubious assumptions.
One way to limit resources is to limit the overall number of threads
available to OpenMP in the R process: this can be done _via_ environment
variable `OMP_THREAD_LIMIT`, where implemented.[^35^](#FOOT35)
Alternatively, the number of threads per region can be limited by the
environment variable `OMP_NUM_THREADS` or API call
`omp_set_num_threads`, or, better, for the regions in your code as part
of their specification. E.g. R uses[^36^](#FOOT36)

```r
#pragma omp parallel for num_threads(nthreads) …
```

That way you only control your own code and not that of other OpenMP
users.

Note that setting environment variables to control OpenMP is
implementation-dependent and may need to be done outside the R process
or before any use of OpenMP (which might be by another process or R
itself). Also, implementation-specific variables such as
`KMP_THREAD_LIMIT` might take precedence.

---

#### 1.2.1.2 Using pthreads

There is no direct support for the POSIX threads (more commonly known as
`pthreads`): by the time we considered adding it several packages were
using it unconditionally so it seems that nowadays it is universally
available on POSIX operating systems (hence not Windows).

For reasonably recent versions of `gcc` and `clang` the correct
specification is

```r
PKG_CPPFLAGS = -pthread
PKG_LIBS = -pthread
```

(and the plural version is also accepted on some systems/versions). For
other platforms the specification is

```r
PKG_CPPFLAGS = -D_REENTRANT
PKG_LIBS = -lpthread
```

(and note that the library name is singular). This is what
`-pthread` does on all known current platforms (although
earlier versions of OpenBSD used a different library name).

For a tutorial see <https://computing.llnl.gov/tutorials/pthreads/>.

POSIX threads are not normally used on Windows, which has its own native
concepts of threads. However, there are two projects implementing
`pthreads` on top of Windows, `pthreads-w32` and `winpthreads` (part of
the MinGW-w64 project).

Whether Windows toolchains implement `pthreads` is up to the toolchain
provider. A `make` variable `SHLIB_PTHREAD_FLAGS` is available for use
in `src/Makevars.win`: this should be included in both
`PKG_CPPFLAGS` (or the Fortran compiler flags) and `PKG_LIBS`.

The presence of a working `pthreads` implementation cannot be
unambiguously determined without testing for yourself: however, that
'`_REENTRANT`' is defined[^37^](#FOOT37) in C/C++ code
is a good indication.

Note that not all `pthreads` implementations are equivalent as parts are
optional (see
<http://pubs.opengroup.org/onlinepubs/009695399/basedefs/pthread.h.html>):
for example, macOS lacks the 'Barriers' option.

See also the comments on thread-safety and performance under OpenMP: on
all known R platforms OpenMP is implemented _via_ `pthreads` and the
known performance issues are in the latter.

---

#### 1.2.1.3 Compiling in sub-directories

Package authors fairly often want to organize code in sub-directories of
`src`, for example if they are including a separate piece of
external software to which this is an R interface.

One simple way is simply to set `OBJECTS` to be all the objects that
need to be compiled, including in sub-directories. For example, CRAN
package [**RSiena**](https://CRAN.R-project.org/package=RSiena) has

```r
SOURCES = $(wildcard data/*.cpp network/*.cpp utils/*.cpp model/*.cpp model/*/*.cpp model/*/*/*.cpp)

OBJECTS = siena07utilities.o siena07internals.o siena07setup.o siena07models.o $(SOURCES:.cpp=.o)
```

One problem with that approach is that unless GNU make extensions are
used, the source files need to be listed and kept up-to-date. As in the
following from CRAN package
[**lossDev**](https://CRAN.R-project.org/package=lossDev):

```r
OBJECTS.samplers = samplers/ExpandableArray.o samplers/Knots.o \
  samplers/RJumpSpline.o samplers/RJumpSplineFactory.o \
  samplers/RealSlicerOV.o samplers/SliceFactoryOV.o samplers/MNorm.o
OBJECTS.distributions = distributions/DSpline.o \
  distributions/DChisqrOV.o distributions/DTOV.o \
  distributions/DNormOV.o distributions/DUnifOV.o distributions/RScalarDist.o
OBJECTS.root = RJump.o

OBJECTS = $(OBJECTS.samplers) $(OBJECTS.distributions) $(OBJECTS.root)
```

Where the subdirectory is self-contained code with a suitable makefile,
the best approach is something like

```r
PKG_LIBS = -LCsdp/lib -lsdp $(LAPACK_LIBS) $(BLAS_LIBS) $(FLIBS)

$(SHLIB): Csdp/lib/libsdp.a

Csdp/lib/libsdp.a:
        @(cd Csdp/lib && $(MAKE) libsdp.a \
          CC="$(CC)" CFLAGS="$(CFLAGS) $(CPICFLAGS)" AR="$(AR)" RANLIB="$(RANLIB)")
```

Note the quotes: the macros can contain spaces, e.g.
`CC = "gcc -m64 -std=gnu99"`. Several authors have forgotten about
parallel makes: the static library in the subdirectory must be made
before the shared object (`$(SHLIB)`) and so the latter must depend on
the former. Others forget the need[^38^](#FOOT38) for
position-independent code.

We really do not recommend using `src/Makefile` instead of
`src/Makevars`, and as the example above shows, it is not
necessary.

---

#### 1.2.2 Configure example

It may be helpful to give an extended example of using a
`configure` script to create a `src/Makevars` file:
this is based on that in the
[**RODBC**](https://CRAN.R-project.org/package=RODBC) package.

The `configure.ac` file follows: `configure` is
created from this by running `autoconf` in the top-level package
directory (containing `configure.ac`).

> ```r
> AC_INIT([RODBC], 1.1.8) dnl package name, version
>
> dnl A user-specifiable option
> odbc_mgr=""
> AC_ARG_WITH([odbc-manager],
>             AC_HELP_STRING([--with-odbc-manager=MGR],
>                            [specify the ODBC manager, e.g. odbc or iodbc]),
>             [odbc_mgr=$withval])
>
> if test "$odbc_mgr" = "odbc" ; then
>   AC_PATH_PROGS(ODBC_CONFIG, odbc_config)
> fi
>
> dnl Select an optional include path, from a configure option
> dnl or from an environment variable.
> AC_ARG_WITH([odbc-include],
>             AC_HELP_STRING([--with-odbc-include=INCLUDE_PATH],
>                            [the location of ODBC header files]),
>             [odbc_include_path=$withval])
> RODBC_CPPFLAGS="-I."
> if test [ -n "$odbc_include_path" ] ; then
>    RODBC_CPPFLAGS="-I. -I${odbc_include_path}"
> else
>   if test [ -n "${ODBC_INCLUDE}" ] ; then
>      RODBC_CPPFLAGS="-I. -I${ODBC_INCLUDE}"
>   fi
> fi
>
> dnl ditto for a library path
> AC_ARG_WITH([odbc-lib],
>             AC_HELP_STRING([--with-odbc-lib=LIB_PATH],
>                            [the location of ODBC libraries]),
>             [odbc_lib_path=$withval])
> if test [ -n "$odbc_lib_path" ] ; then
>    LIBS="-L$odbc_lib_path ${LIBS}"
> else
>   if test [ -n "${ODBC_LIBS}" ] ; then
>      LIBS="-L${ODBC_LIBS} ${LIBS}"
>   else
>     if test -n "${ODBC_CONFIG}"; then
>       odbc_lib_path=`odbc_config --libs | sed s/-lodbc//`
>       LIBS="${odbc_lib_path} ${LIBS}"
>     fi
>   fi
> fi
>
> dnl Now find the compiler and compiler flags to use
> : ${R_HOME=`R RHOME`}
> if test -z "${R_HOME}"; then
>   echo "could not determine R_HOME"
>   exit 1
> fi
> CC=`"${R_HOME}/bin/R" CMD config CC`
> CFLAGS=`"${R_HOME}/bin/R" CMD config CFLAGS`
> CPPFLAGS=`"${R_HOME}/bin/R" CMD config CPPFLAGS`
>
> if test -n "${ODBC_CONFIG}"; then
>   RODBC_CPPFLAGS=`odbc_config --cflags`
> fi
> CPPFLAGS="${CPPFLAGS} ${RODBC_CPPFLAGS}"
>
> dnl Check the headers can be found
> AC_CHECK_HEADERS(sql.h sqlext.h)
> if test "${ac_cv_header_sql_h}" = no ||
>    test "${ac_cv_header_sqlext_h}" = no; then
>    AC_MSG_ERROR("ODBC headers sql.h and sqlext.h not found")
> fi
>
> dnl search for a library containing an ODBC function
> if test [ -n "${odbc_mgr}" ] ; then
>   AC_SEARCH_LIBS(SQLTables, ${odbc_mgr}, ,
>       AC_MSG_ERROR("ODBC driver manager ${odbc_mgr} not found"))
> else
>   AC_SEARCH_LIBS(SQLTables, odbc odbc32 iodbc, ,
>       AC_MSG_ERROR("no ODBC driver manager found"))
> fi
>
> dnl for 64-bit ODBC need SQL[U]LEN, and it is unclear where they are defined.
> AC_CHECK_TYPES([SQLLEN, SQLULEN], , , [# include <sql.h>])
> dnl for unixODBC header
> AC_CHECK_SIZEOF(long, 4)
>
> dnl substitute RODBC_CPPFLAGS and LIBS
> AC_SUBST(RODBC_CPPFLAGS)
> AC_SUBST(LIBS)
> AC_CONFIG_HEADERS([src/config.h])
> dnl and do substitution in the src/Makevars.in and src/config.h
> AC_CONFIG_FILES([src/Makevars])
> AC_OUTPUT
> ```
>
> where `src/Makevars.in` would be simply

> ```r
> PKG_CPPFLAGS = @RODBC_CPPFLAGS@
> PKG_LIBS = @LIBS@
> ```
>
> A user can then be advised to specify the location of the ODBC driver
> manager files by options like (lines broken for easier reading)

```r
R CMD INSTALL \
  --configure-args='--with-odbc-include=/opt/local/include \
  --with-odbc-lib=/opt/local/lib --with-odbc-manager=iodbc' \
  RODBC
```

or by setting the environment variables `ODBC_INCLUDE` and `ODBC_LIBS`.

---

#### 1.2.3 Using F9x code

R assumes that source files with extension `.f` are fixed-form
Fortran 90 (which includes Fortran 77), and passes them to the compiler
specified by macro '`FC`'. On known platforms the Fortran
compiler will also accept free-form Fortran 90/95 code with extension
`.f90` or `.f95`, but those are not used by R itself
so this is not required.

As from R 3.6.0 the same compiler is used for both fixed-form and
free-form Fortran code (with different file extensions and possibly
different flags). For both, macro `PKG_FFLAGS` can be used for
package-specific flags: in the unusual case that both are included in a
single package and that different flags are needed for the two forms,
macro `PKG_FCFLAGS` is also available for free-form Fortran.

The code used to build R allows a 'Fortran 90' compiler to be selected
as '`FC`', so platforms might be encountered which only support
Fortran 90. However, Fortran 95 is widely supported.

Some compilers specified by '`FC`' will accept Fortran 2003,
2008 or 2018 code: such code should still use file extension
`.f90` or `.f95`. Most platforms use `gfortran` where
you may need to include `-std=f2003`, `-std=f2008` or
(from version 8) `-std=f2018` in `PKG_FFLAGS` or `PKG_FCFLAGS`:
the default is 'GNU Fortran', Fortran 95 with non-standard extensions.
The Oracle `f95` compiler 'accepts some Fortran 2003/8 features' (search
for 'Oracle Developer Studio 12.6: Fortran User's Guide' and look for
§4.6). Intel Fortran has full Fortran 2008 support from version 17.0,
and some 2018 support in version 16.0 and more in version 19.0.

Modern versions of Fortran support modules, whereby compiling one source
file creates a module file which is then included in others. (Module
files typically have a `.mod` extension: they do depend on the
compiler used and so should never be included in a package.) This
creates a dependence which `make` will not know about and often causes
installation with a parallel make to fail. Thus it is necessary to add
explicit dependencies to `src/Makevars` to tell `make` the
constraints on the order of compilation. For example, if file
`iface.f90` creates a module '`iface`' used by files
`cmi.f90` and `dmi.f90` then `src/Makevars`
needs to contain something like

```r
cmi.o dmi.o: iface.o
```

Note that it is not portable (although some platforms do accept it) to
define a module of the same name in multiple source files.

---

#### 1.2.4 Using C++11 code

R can be built without a C++ compiler although one is available (but not
necessarily installed) on all known R platforms. For full portability
across platforms, all that can be assumed is approximate support for the
C++98 standard (the widely used `g++` deviates considerably from the
standard). Some compilers have a concept of 'C++03' ('essentially a bug
fix') or 'C++ Technical Report 1' (TR1), an optional addition to the
'C++03' revision which was published in 2007. A revised standard was
published in 2011 and compilers with pretty much complete
implementations are available. C++11 added all of the C99 features which
are not otherwise implemented in C++, and C++ compilers commonly accept
C99 extensions to C++98. A minor update[^39^](#FOOT39)
('C++14') was published in December 2014. A revision ('C++17') was
published in December 2017, and a further revision ('C++20', with many
new features) is scheduled for publication in May 2020.

What standard a C++ compiler aims to support can be hard to determine:
the value[^40^](#FOOT40) of `__cplusplus` may help but some
compilers use it to denote a standard which is partially supported and
some the latest standard which is (almost) fully supported.

The webpage <http://en.cppreference.com/w/cpp/compiler_support> gives
some information on which compilers are known to support recent C++
features. `g++` claims full C++11 support from version 4.8.1.

As from version 3.6.2[^41^](#FOOT41), R selects a default C++
compiler with options that conform as far as
possible[^42^](#FOOT42) to C++11. Packages which do not specify
'`R (>= 3.6.2)`' in their `DESCRIPTION` files need to
explicitly require C++11, hence the rest of this section.

In order to specify C++11 code in a package to be used with R versions
from 3.1.0 but before 3.6.2, the package's `Makevars` file (or
`Makevars.win` on Windows) should include the line

```r
CXX_STD = CXX11
```

Compilation and linking will then be done with the C++11 compiler (if
any).

Packages without a `src/Makevars` or `src/Makefile`
file may specify that they require C++11 for code in the `src`
directory by including '`C++11`' in the
'`SystemRequirements`' field of the `DESCRIPTION`
file, e.g.

```r
SystemRequirements: C++11
```

If a package does have a `src/Makevars[.win]` file then setting
the make variable '`CXX_STD`' is preferred, as it allows
`R CMD SHLIB` to work correctly in the package's `src`
directory.

Conversely, to ensure that the C++98 standard is assumed even when this
is not the compiler default, use

```r
SystemRequirements: C++98
```

or

```r
CXX_STD = CXX98
```

But note that this is deprecated and will be ignorwd in future versions
of R.

The C++11 compiler will be used systematically by R for all C++ code if
the environment variable `USE_CXX11` is defined (with any value). Hence
this environment variable should be defined when invoking `R CMD SHLIB`
in the absence of a `Makevars` file (or `Makevars.win`
on Windows) if a C++11 compiler is required.

Further control over compilation of C++11 code can be obtained by
specifying the macros '`CXX11`' and '`CXX11STD`' when
R is configured[^43^](#FOOT43), or in a personal or site
`Makevars` file. See [Customizing package compilation](./R-admin.html#Customizing-package-compilation) in R
Installation and Administration. If C++11 support is not available then
these macros are both empty; if it is available by default,
'`CXX11`' defaults to '`CXX`' and
'`CXX11STD`' is empty . Otherwise, '`CXX11`' defaults
to the same value as the C++ compiler '`CXX`' and the flag
'`CXX11STD`' defaults to `-std=c++11` or similar. It
is possible to specify '`CXX11`' to be a distinct compiler just
for C++11--using packages, e.g. `g++` on Solaris. Note however that
different C++ compilers (and even different versions of the same
compiler) often differ in their ABI so their outputs can rarely be
mixed. By setting '`CXX11STD`' it is also possible to choose a
different dialect of the standard such as `-std=c++11`.

As noted above, support for C++11 varies across platforms: on some
platforms, it may be possible or necessary to select a different
compiler for C++11, _via_ personal or site `Makevars` files.

There is no guarantee that C++11 can be used in a package in combination
with any other compiled language (even C), as the C++11 compiler may be
incompatible with the native compilers for the platform.

If a package using C++11 has a `configure` script it is essential that
it selects the correct compiler, _via_ something like

```r
CXX11=`"${R_HOME}/bin/R" CMD config CXX11`
if test -z "$CXX11"; then
  AC_MSG_ERROR([No C++11 compiler is available])
fi
CXX11STD=`"${R_HOME}/bin/R" CMD config CXX11STD`
CXX="${CXX11} ${CXX11STD}"
CXXFLAGS=`"${R_HOME}/bin/R" CMD config CXX11FLAGS`
AC_LANG(C++)
```

(paying attention to all the quotes required).

If you want to compile C++11 code in a subdirectory, make sure you pass
down the macros to specify that compiler, e.g. in
`src/Makevars`

```r
sublibs:
         @(cd libs && $(MAKE) \
            CXX="$(CXX11) $(CXX11STD)" CXXFLAGS="$(CXX11FLAGS) $(CXX11PICFLAGS)")
```

Note that the mechanisms described here specify C++11 for code compiled
by `R CMD SHLIB` as used by default by `R CMD INSTALL`. They do not
necessarily apply if there is a `src/Makefile` file, nor to
compilation done in vignettes or _via_ other packages.

---

#### 1.2.5 Using C++14 code

Support for a C++14 compiler (where available) was been added to R from
version 3.4.0. Similar considerations to C++11 apply, with the variables
associated with the C++14 compiler using the prefix '`CXX14`'
instead of '`CXX11`'. Hence to use C++14 code in a package, the
package's `Makevars` file (or `Makevars.win` on
Windows) should include the line

```r
CXX_STD = CXX14
```

In the absence of a `Makevars` file, C++14 support can also be
requested by the line:

```r
SystemRequirements: C++14
```

in the `DESCRIPTION` file. Finally, the C++14 compiler can be
used systematically by setting the environment variable `USE_CXX14`.

Note that code written for C++11 that emulates features of C++14 will
not necessarily compile under a C++14 compiler[^44^](#FOOT44),
since the emulation typically leads to a namespace clash. In order to
ensure that the code also compiles under C++14, something like the
following should be done:

```r
#if __cplusplus >= 201402L
using std::make_unique;
#else
// your emulation
#endif
```

Code needing C++14 features would do better to test for their presence
_via_ 'SD-6 feature tests'[^45^](#FOOT45). That test could be

```r
#include <memory> // header where this is defined
#if defined(__cpp_lib_make_unique) && (__cpp_lib_make_unique >= 201304)
using std::make_unique;
#else
// your emulation
#endif
```

Note that `g++` 4.9.x (as used for R on Windows at least up to 3.6.x)
has only partial C++14 support, and the flag to obtain that support is
not included in the default Windows build of R --- one could try
something like

```r
CXX14="$(BINPREF)g++ $(M_ARCH)"
CXX14FLAGS="-O2 -Wall"
CXX14STD=-std=gnu1y
```

in `HOME/.R/Makevars.win`.

---

#### 1.2.6 Using C++17 code

Support for C++17 was added to R version 3.4.0. The `configure`
script tests a subset of C++17 features. `clang 4.0.0` and `gcc 7.1` and
later versions passed these tests (with flag `-std=gnu++17` or
`-std=gnu++1z` chosen by the `configure` script). Note
that the C++17 feature tests are incomplete and are subject to change in
future R versions as support for the standard improves.

The variables associated with the C++17 compiler use the prefix
'`CXX17`'. Hence to use C++17 code in a package, the package's
`Makevars` file (or `Makevars.win` on Windows) should
include the line

```r
CXX_STD = CXX17
```

In the absence of a `Makevars` file, C++17 support can also be
requested by the line:

```r
SystemRequirements: C++17
```

in the `DESCRIPTION` file. Finally, the C++17 compiler can be
used systematically by setting the environment variable `USE_CXX17`.

As for C++14, feature tests can be used (and probably should be as
support is still patchy, especially library support).

No C++17 support is enabled in the current default build of R on
Windows.

---

### 1.3 Checking and building packages

Before using these tools, please check that your package can be
installed (which checked it can be loaded). `R CMD check` will _inter
alia_ do this, but you may get more detailed error messages doing the
install directly.

---

• [Checking packages](#Checking-packages)     
 • [Building package tarballs](#Building-package-tarballs)     
 • [Building binary packages](#Building-binary-packages)

---

If your package specifies an encoding in its `DESCRIPTION`
file, you should run these tools in a locale which makes use of that
encoding: they may not work at all or may work incorrectly in other
locales (although UTF-8 locales will most likely work).

> **Note:** `R CMD check` and `R CMD build` run R processes with
> `--vanilla` in which none of the user's startup files are
> read. If you need `R_LIBS` set (to find packages in a non-standard
> library) you can set it in the environment: also you can use the check
> and build environment files (as specified by the environment variables
> `R_CHECK_ENVIRON` and `R_BUILD_ENVIRON`; if unset,
> files[^46^](#FOOT46) `~/.R/check.Renviron` and
> `~/.R/build.Renviron` are used) to set environment variables
> when using these utilities.

> **Note to Windows users:** `R CMD build` may make use of the Windows
> toolset (see the "R Installation and Administration" manual) if
> present and in your path, and it is required for packages which need
> it to install (including those with `configure.win` or
> `cleanup.win` scripts or a `src` directory) and e.g.
> need vignettes built.
>
> You may need to set the environment variable `TMPDIR` to point to a
> suitable writable directory with a path not containing spaces -- use
> forward slashes for the separators. Also, the directory needs to be on
> a case-honouring file system (some network-mounted file systems are
> not).

---

#### 1.3.1 Checking packages

Using `R CMD check`, the R package checker, one can test whether
_source_ R packages work correctly. It can be run on one or more
directories, or compressed package `tar` archives with extension
`.tar.gz`, `.tgz`, `.tar.bz2` or
`.tar.xz`.

It is strongly recommended that the final checks are run on a `tar`
archive prepared by `R CMD build`.

This runs a series of checks, including

1.  The package is installed. This will warn about missing
    cross-references and duplicate aliases in help files.

2.  The file names are checked to be valid across file systems and
    supported operating system platforms.

3.  The files and directories are checked for sufficient permissions
    (Unix-alikes only).

4.  The files are checked for binary executables, using a suitable
    version of `file` if available[^47^](#FOOT47). (There may
    be rare false positives.)

5.  The `DESCRIPTION` file is checked for completeness, and
    some of its entries for correctness. Unless installation tests are
    skipped, checking is aborted if the package dependencies cannot be
    resolved at run time. (You may need to set `R_LIBS` in the
    environment if dependent packages are in a separate library tree.)
    One check is that the package name is not that of a standard
    package, nor one of the defunct standard packages
    ('`ctest`', '`eda`', '`lqs`',
    '`mle`', '`modreg`', '`mva`',
    '`nls`', '`stepfun`' and '`ts`'). Another
    check is that all packages mentioned in `library` or `require`s or
    from which the `NAMESPACE` file imports or are called _via_
    `::` or `:::` are listed (in '`Depends`',
    '`Imports`', '`Suggests`'): this is not an
    exhaustive check of the actual imports.

6.  Available index information (in particular, for demos and vignettes)
    is checked for completeness.

7.  The package subdirectories are checked for suitable file names and
    for not being empty. The checks on file names are controlled by the
    option `--check-subdirs=value`. This defaults to
    '`default`', which runs the checks only if checking a
    tarball: the default can be overridden by specifying the value as
    '`yes`' or '`no`'. Further, the check on the
    `src` directory is only run if the package does not contain
    a `configure` script (which corresponds to the value
    '`yes-maybe`') and there is no `src/Makefile` or
    `src/Makefile.in`.

    To allow a `configure` script to generate suitable files,
    files ending in '`.in`' will be allowed in the `R`
    directory.

    A warning is given for directory names that look like R package
    check directories -- many packages have been submitted to CRAN
    containing these.

8.  The R files are checked for syntax errors. Bytes which are non-ASCII
    are reported as warnings, but these should be regarded as errors
    unless it is known that the package will always be used in the same
    locale.

9.  It is checked that the package can be loaded, first with the usual
    default packages and then only with package **base** already loaded.
    It is checked that the namespace this can be loaded in an empty
    session with only the **base** namespace loaded. (Namespaces and
    packages can be loaded very early in the session, before the default
    packages are available, so packages should work then.)

10. The R files are checked for correct calls to `library.dynam`.
    Package startup functions are checked for correct argument lists and
    (incorrect) calls to functions which modify the search path or
    inappropriately generate messages. The R code is checked for
    possible problems using
    [**codetools**](https://CRAN.R-project.org/package=codetools). In
    addition, it is checked whether S3 methods have all arguments of the
    corresponding generic, and whether the final argument of replacement
    functions is called '`value`'. All foreign function calls
    (`.C`, `.Fortran`, `.Call` and `.External` calls) are tested to see
    if they have a `PACKAGE` argument, and if not, whether the
    appropriate DLL might be deduced from the namespace of the package.
    Any other calls are reported. (The check is generous, and users may
    want to supplement this by examining the output of
    `tools::checkFF("mypkg", verbose=TRUE)`, especially if the intention
    were to always use a `PACKAGE` argument)

11. The `Rd` files are checked for correct syntax and metadata,
    including the presence of the mandatory fields (`\name`, `\alias`,
    `\title` and `\description`). The `Rd` name and title are
    checked for being non-empty, and there is a check for missing
    cross-references (links).

12. A check is made for missing documentation entries, such as
    undocumented user-level objects in the package.

13. Documentation for functions, data sets, and S4 classes is checked
    for consistency with the corresponding code.

14. It is checked whether all function arguments given in `\usage`
    sections of `Rd` files are documented in the corresponding
    `\arguments` section.

15. The `data` directory is checked for non-ASCII characters
    and for the use of reasonable levels of compression.

16. C, C++ and Fortran source and header files[^48^](#FOOT48)
    are tested for portable (LF-only) line endings. If there is a
    `Makefile` or `Makefile.in` or `Makevars`
    or `Makevars.in` file under the `src` directory,
    it is checked for portable line endings and the correct use of
    '`$(BLAS_LIBS)`' and '`$(LAPACK_LIBS)`'

    Compiled code is checked for symbols corresponding to functions
    which might terminate R or write to
    `stdout`/`stderr` instead of the console. Note
    that the latter might give false positives in that the symbols might
    be pulled in with external libraries and could never be called.
    Windows[^49^](#FOOT49) users should note that the Fortran
    and C++ runtime libraries are examples of such external libraries.

17. Some checks are made of the contents of the `inst/doc`
    directory. These always include checking for files that look like
    leftovers, and if suitable tools (such as `qpdf`) are available,
    checking that the PDF documentation is of minimal size.

18. The examples provided by the package's documentation are run. (see
    [Writing R documentation files](#Writing-R-documentation-files), for
    information on using `\examples` to create executable example code.)
    If there is a file `tests/Examples/pkg-Ex.Rout.save`, the
    output of running the examples is compared to that file.

    Of course, released packages should be able to run at least their
    own examples. Each example is run in a 'clean' environment (so
    earlier examples cannot be assumed to have been run), and with the
    variables `T` and `F` redefined to generate an error unless they are
    set in the example: See [Logical
    vectors](./R-intro.html#Logical-vectors) in An Introduction to R.

19. If the package sources contain a `tests` directory then the
    tests specified in that directory are run. (Typically they will
    consist of a set of `.R` source files and target output
    files `.Rout.save`.) Please note that the comparison will
    be done in the end user's locale, so the target output files should
    be ASCII if at all possible. (The command line option
    `--test-dir=foo` may be used to specify tests in a non-standard
    location. For example, unusually slow tests could be placed in
    `inst/slowTests` and then
    `R CMD check --test-dir=inst/slowTests` would be used to run them.
    Other names that have been suggested are, for example,
    `inst/testWithOracle` for tests that require Oracle to be
    installed, `inst/randomTests` for tests which use random
    values and may occasionally fail by chance, etc.)

20. The code in package vignettes (see [Writing package
    vignettes](#Writing-package-vignettes)) is executed, and the
    vignette PDFs re-made from their sources as a check of completeness
    of the sources (unless there is a '`BuildVignettes`' field
    in the package's `DESCRIPTION` file with a false value). If
    there is a target output file `.Rout.save` in the vignette
    source directory, the output from running the code in that vignette
    is compared with the target output file and any differences are
    reported (but not recorded in the log file). (If the vignette
    sources are in the deprecated location `inst/doc`, do mark
    such target output files to not be installed in
    `.Rinstignore`.)

    If there is an error[^50^](#FOOT50) in executing the R code
    in vignette `foo.ext`, a log file `foo.ext.log` is
    created in the check directory. The vignette PDFs are re-made in a
    copy of the package sources in the `vign_test` subdirectory
    of the check directory, so for further information on errors look in
    directory `pkgname/vign_test/vignettes`. (It is only
    retained if there are errors or if environment variable
    `_R_CHECK_CLEAN_VIGN_TEST_` is set to a false value.)

21. The PDF version of the package's manual is created (to check that
    the `Rd` files can be converted successfully). This needs
    LaTeX and suitable fonts and LaTeX packages to be installed. See
    [Making the manuals](./R-admin.html#Making-the-manuals) in R
    Installation and Administration.

All these tests are run with collation set to the `C` locale, and for
the examples and tests with environment variable `LANGUAGE=en`: this is
to minimize differences between platforms.

Use [R CMD check \--help] to obtain more information about the
usage of the R package checker. A subset of the checking steps can be
selected by adding command-line options. It also allows customization by
setting environment variables `_R_CHECK_*_` as described in
[Tools](./R-ints.html#Tools) in R Internals: a set of these
customizations similar to those used by CRAN can be selected by the
option `--as-cran` (which works best if Internet access is
available). Some Windows users may need to set environment variable
`R_WIN_NO_JUNCTIONS` to a non-empty value. The test of cyclic
declarations[^51^](#FOOT51)in `DESCRIPTION` files
needs repositories (including CRAN) set: do this in
`~/.Rprofile`, by e.g.

```r
options(repos = c(CRAN="https://cran.r-project.org"))
```

One check customization which can be revealing is

```r
_R_CHECK_CODETOOLS_PROFILE_="suppressLocalUnused=FALSE"
```

which reports unused local assignments. Not only does this point out
computations which are unnecessary because their results are unused, it
also can uncover errors. (Two such are to intend to update an object by
assigning a value but mistype its name or assign in the wrong scope, for
example using `<-` where `<<-` was intended.) This can give false
positives, most commonly because of non-standard evaluation for formulae
and because the intention is to return objects in the environment of a
function for later use.

Complete checking of a package which contains a file
`README.md` needs a reasonably current version of `pandoc`
installed: see <http://johnmacfarlane.net/pandoc/installing.html>.

You do need to ensure that the package is checked in a suitable locale
if it contains non-ASCII characters. Such packages are likely to fail
some of the checks in a `C` locale, and `R CMD check` will warn if it
spots the problem. You should be able to check any package in a UTF-8
locale (if one is available). Beware that although a `C` locale is
rarely used at a console, it may be the default if logging in remotely
or for batch jobs.

> **Multiple sub-architectures:** On systems which support multiple
> sub-architectures (principally Windows), `R CMD check` will install
> and check a package which contains compiled code under all available
> sub-architectures. (Use option `--force-multiarch` to force
> this for packages without compiled code, which are otherwise only
> checked under the main sub-architecture.) This will run the loading
> tests, examples and `tests` directory under each installed
> sub-architecture in turn, and give an error if any fail. Where
> environment variables (including perhaps `PATH`) need to be set
> differently for each sub-architecture, these can be set in
> architecture-specific files such as
> `R_HOME/etc/i386/Renviron.site`.
>
> An alternative approach is to use `R CMD check --no-multiarch` to
> check the primary sub-architecture, and then to use something like
> `R --arch=x86_64 CMD check --extra-arch` or (Windows)
> `/path/to/R/bin/x64/Rcmd check --extra-arch` to run for each
> additional sub-architecture just the checks[^52^](#FOOT52)
> which differ by sub-architecture. (This approach is required for
> packages which are installed by `R CMD INSTALL --merge-multiarch`.)
>
> Where packages need additional commands to install all the
> sub-architectures these can be supplied by e.g.
> `--install-args=--force-biarch`.

---

#### 1.3.2 Building package tarballs

Packages may be distributed in source form as "tarballs"
(`.tar.gz` files) or in binary form. The source form can be
installed on all platforms with suitable tools and is the usual form for
Unix-like systems; the binary form is platform-specific, and is the more
common distribution form for the Windows and macOS platforms.

Using `R CMD build`, the R package builder, one can build R package
tarballs from their sources (for example, for subsequent release). It is
recommended that packages are built for release by the current release
version of R or '`r-patched`', to avoid inadvertently picking
up new features of a development version of R.

Prior to actually building the package in the standard gzipped tar file
format, a few diagnostic checks and cleanups are performed. In
particular, it is tested whether object indices exist and can be assumed
to be up-to-date, and C, C++ and Fortran source files and relevant
makefiles in a `src` directory are tested and converted to LF
line-endings if necessary.

Run-time checks whether the package works correctly should be performed
using `R CMD check` prior to invoking the final build procedure.

To exclude files from being put into the package, one can specify a list
of exclude patterns in file `.Rbuildignore` in the top-level
source directory. These patterns should be Perl-like regular expressions
(see the help for `regexp` in R for the precise details), one per line,
to be matched case-insensitively against the file and directory names
relative to the top-level package source directory. In addition,
directories from source control systems[^53^](#FOOT53) or from
`eclipse`[^54^](#FOOT54), directories with names ending
`.Rcheck` or `Old` or `old` and files
`GNUMakefile`[^55^](#FOOT55),
`Read-and-delete-me` or with base names starting with
'`.#`', or starting and ending with '`#`', or ending
in '`~`', '`.bak`' or '`.swp`', are excluded
by default. In addition, those files in the `R`,
`demo` and `man` directories which are flagged by
`R CMD check` as having invalid names will be excluded.

Use [R CMD build \--help] to obtain more information about the
usage of the R package builder.

Unless [R CMD build] is invoked with the
`--no-build-vignettes` option (or the package's
`DESCRIPTION` contains '`BuildVignettes: no`' or
similar), it will attempt to (re)build the vignettes (see [Writing
package vignettes](#Writing-package-vignettes)) in the package. To do so
it installs the current package into a temporary library tree, but any
dependent packages need to be installed in an available library tree
(see the Note: at the top of this section).

Similarly, if the `.Rd` documentation files contain any
`\Sexpr` macros (see [Dynamic pages](#Dynamic-pages)), the package will
be temporarily installed to execute them. Post-execution binary copies
of those pages containing build-time macros will be saved in
`build/partial.rdb`. If there are any install-time or
render-time macros, a `.pdf` version of the package manual will
be built and installed in the `build` subdirectory. (This
allows CRAN or other repositories to display the manual even if they are
unable to install the package.) This can be suppressed by the option
`--no-manual` or if package's `DESCRIPTION` contains
'`BuildManual: no`' or similar.

One of the checks that `R CMD build` runs is for empty source
directories. These are in most (but not all) cases unintentional, if
they are intentional use the option `--keep-empty-dirs` (or set
the environment variable `_R_BUILD_KEEP_EMPTY_DIRS_` to
'`TRUE`', or have a '`BuildKeepEmpty`' field with a
true value in the `DESCRIPTION` file).

The `--resave-data` option allows saved images (`.rda`
and `.RData` files) in the `data` directory to be
optimized for size. It will also compress tabular files and convert
`.R` files to saved images. It can take values `no`, `gzip`
(the default if this option is not supplied, which can be changed by
setting the environment variable `_R_BUILD_RESAVE_DATA_`) and `best`
(equivalent to giving it without a value), which chooses the most
effective compression. Using `best` adds a dependence on `R (>= 2.10)`
to the `DESCRIPTION` file if `bzip2` or `xz` compression is
selected for any of the files. If this is thought undesirable,
`--resave-data=gzip` (which is the default if that option is
not supplied) will do what compression it can with `gzip`. A package can
control how its data is resaved by supplying a
'`BuildResaveData`' field (with one of the values given earlier
in this paragraph) in its `DESCRIPTION` file.

The `--compact-vignettes` option will run `tools::compactPDF`
over the PDF files in `inst/doc` (and its subdirectories) to
losslessly compress them. This is not enabled by default (it can be
selected by environment variable `_R_BUILD_COMPACT_VIGNETTES_`) and
needs `qpdf` (<http://qpdf.sourceforge.net/>) to be available.

It can be useful to run `R CMD check --check-subdirs=yes` on the built
tarball as a final check on the contents.

Where a non-POSIX file system is in use which does not utilize execute
permissions, some care is needed with permissions. This applies on
Windows and to e.g. FAT-formatted drives and SMB-mounted file systems on
other OSes. The 'mode' of the file recorded in the tarball will be
whatever `file.info()` returns. On Windows this will record only
directories as having execute permission and on other OSes it is likely
that all files have reported 'mode' `0777`. A particular issue is
packages being built on Windows which are intended to contain executable
scripts such as `configure` and `cleanup`:
`R CMD build` ensures those two are recorded with execute permission.

Directory `build` of the package sources is reserved for use by
`R CMD build`: it contains information which may not easily be created
when the package is installed, including index information on the
vignettes and, rarely, information on the help pages and perhaps a copy
of the PDF reference manual (see above).

---

#### 1.3.3 Building binary packages

Binary packages are compressed copies of installed versions of packages.
They contain compiled shared libraries rather than C, C++ or Fortran
source code, and the R functions are included in their installed form.
The format and filename are platform-specific; for example, a binary
package for Windows is usually supplied as a `.zip` file, and
for the macOS platform the default binary package file extension is
`.tgz`.

The recommended method of building binary packages is to use

`R CMD INSTALL --build pkg` where `pkg` is either the name of a
source tarball (in the usual `.tar.gz` format) or the location
of the directory of the package source to be built. This operates by
first installing the package and then packing the installed binaries
into the appropriate binary package file for the particular platform.

By default, `R CMD INSTALL --build` will attempt to install the package
into the default library tree for the local installation of R. This has
two implications:

- If the installation is successful, it will overwrite any existing
  installation of the same package.
- The default library tree must have write permission; if not, the
  package will not install and the binary will not be created.

To prevent changes to the present working installation or to provide an
install location with write access, create a suitably located directory
with write access and use the `-l` option to build the package in the
chosen location. The usage is then

`R CMD INSTALL -l location --build pkg`

where `location` is the chosen directory with write access. The
package will be installed as a subdirectory of `location`, and
the package binary will be created in the current directory.

Other options for `R CMD INSTALL` can be found using
`R CMD INSTALL --help`, and platform-specific details for special cases
are discussed in the platform-specific FAQs.

Finally, at least one web-based service is available for building binary
packages from (checked) source code: WinBuilder (see
<https://win-builder.R-project.org/>) is able to build Windows binaries.
Note that this is intended for developers on other platforms who do not
have access to Windows but wish to provide binaries for the Windows
platform.

---

### 1.4 Writing package vignettes

---

• [Encodings and vignettes](#Encodings-and-vignettes)     
 • [Non-Sweave vignettes](#Non_002dSweave-vignettes)

---

In addition to the help files in `Rd` format, R packages allow
the inclusion of documents in arbitrary other formats. The standard
location for these is subdirectory `inst/doc` of a source
package, the contents will be copied to subdirectory `doc` when
the package is installed. Pointers from package help indices to the
installed documents are automatically created. Documents in
`inst/doc` can be in arbitrary format, however we strongly
recommend providing them in PDF format, so users on almost all platforms
can easily read them. To ensure that they can be accessed from a browser
(as an HTML index is provided), the file names should start with an
ASCII letter and be comprised entirely of ASCII letters or digits or
hyphen or underscore.

A special case is _package vignettes_. Vignettes are documents in PDF or
HTML format obtained from plain text literate source files from which R
knows how to extract R code and create output (in PDF/HTML or
intermediate LaTeX). Vignette engines do this work, using "tangle" and
"weave" functions respectively. Sweave, provided by the R distribution,
is the default engine. Other vignette engines besides Sweave are
supported; see [Non-Sweave vignettes](#Non_002dSweave-vignettes).

Package vignettes have their sources in subdirectory
`vignettes` of the package sources. Note that the location of
the vignette sources only affects `R CMD build` and `R CMD check`: the
tarball built by `R CMD build` includes in `inst/doc` the
components intended to be installed.

Sweave vignette sources are normally given the file extension
`.Rnw` or `.Rtex`, but for historical reasons
extensions[^56^](#FOOT56) `.Snw` and `.Stex`
are also recognized. Sweave allows the integration of LaTeX documents:
see the `Sweave` help page in R and the `Sweave` vignette in package
**utils** for details on the source document format.

Package vignettes are tested by `R CMD check` by executing all R code
chunks they contain (except those marked for non-evaluation, e.g., with
option `eval=FALSE` for Sweave). The R working directory for all
vignette tests in `R CMD check` is a _copy_ of the vignette source
directory. Make sure all files needed to run the R code in the vignette
(data sets, ...) are accessible by either placing them in the
`inst/doc` hierarchy of the source package or by using calls to
`system.file()`. All other files needed to re-make the vignettes (such
as LaTeX style files, BibTeX input files and files for any figures not
created by running the code in the vignette) must be in the vignette
source directory. `R CMD check` will check that vignette production has
succeeded by comparing modification times of output files in
`inst/doc` with the source in `vignettes`.

`R CMD build` will automatically[^57^](#FOOT57) create the (PDF
or HTML versions of the) vignettes in `inst/doc` for
distribution with the package sources. By including the vignette outputs
in the package sources it is not necessary that these can be re-built at
install time, i.e., the package author can use private R packages,
screen snapshots and LaTeX extensions which are only available on their
machine.[^58^](#FOOT58)

By default `R CMD build` will run `Sweave` on all Sweave vignette source
files in `vignettes`. If `Makefile` is found in the
vignette source directory, then `R CMD build` will try to run `make`
after the `Sweave` runs, otherwise `texi2pdf` is run on each
`.tex` file produced.

The first target in the `Makefile` should take care of both
creation of PDF/HTML files and cleaning up afterwards (including after
`Sweave`), i.e., delete all files that shall not appear in the final
package archive. Note that if the `make` step runs R it needs to be
careful to respect the environment values of `R_LIBS` and
`R_HOME`[^59^](#FOOT59). Finally, if there is a
`Makefile` and it has a '`clean:`' target,
`make clean` is run.

All the usual _caveats_ about including a `Makefile` apply. It
must be portable (no GNU extensions), use LF line endings and must work
correctly with a parallel `make`: too many authors have written things
like

```r
## BAD EXAMPLE
all: pdf clean

pdf: ABC-intro.pdf ABC-details.pdf

%.pdf:  %.tex
        texi2dvi --pdf $*

clean:
        rm *.tex ABC-details-*.pdf
```

which will start removing the source files whilst `pdflatex` is working.

Metadata lines can be placed in the source file, preferably in LaTeX
comments in the preamble. One such is a `\VignetteIndexEntry` of the
form

```r
%\VignetteIndexEntry{Using Animal}
```

Others you may see are `\VignettePackage` (currently ignored),
`\VignetteDepends` and `\VignetteKeyword` (which replaced
`\VignetteKeywords`). These are processed at package installation time
to create the saved data frame `Meta/vignette.rds`, but only
the `\VignetteIndexEntry` and `\VignetteKeyword` statements are
currently used. The `\VignetteEngine` statement is described in
[Non-Sweave vignettes](#Non_002dSweave-vignettes).

At install time an HTML index for all vignettes in the package is
automatically created from the `\VignetteIndexEntry` statements unless a
file `index.html` exists in directory `inst/doc`. This
index is linked from the HTML help index for the package. If you do
supply a `inst/doc/index.html` file it should contain relative
links only to files under the installed `doc` directory, or
perhaps (not really an index) to HTML help files or to the
`DESCRIPTION` file, and be valid HTML as confirmed _via_ the
[W3C Markup Validation Service](https://validator.w3.org) or
[Validator.nu](https://validator.nu/).

Sweave/Stangle allows the document to specify the `split=TRUE` option to
create a single R file for each code chunk: this will not work for
vignettes where it is assumed that each vignette source generates a
single file with the vignette extension replaced by `.R`.

Do watch that PDFs are not too large -- one in a CRAN package was 72MB!
This is usually caused by the inclusion of overly detailed figures,
which will not render well in PDF viewers. Sometimes it is much better
to generate fairly high resolution bitmap (PNG, JPEG) figures and
include those in the PDF document.

When `R CMD build` builds the vignettes, it copies these and the
vignette sources from directory `vignettes` to
`inst/doc`. To install any other files from the
`vignettes` directory, include a file
`vignettes/.install_extras` which specifies these as Perl-like
regular expressions on one or more lines. (See the description of the
`.Rinstignore` file for full details.)

---

#### 1.4.1 Encodings and vignettes

Vignettes will in general include descriptive text, R input, R output
and figures, LaTeX include files and bibliographic references. As any of
these may contain non-ASCII characters, the handling of encodings can
become very complicated.

The vignette source file should be written in ASCII or contain a
declaration of the encoding (see below). This applies even to comments
within the source file, since vignette engines process comments to look
for options and metadata lines. When an engine's weave and tangle
functions are called on the vignette source, it will be converted to the
encoding of the current R session.

`Stangle()` will produce an R code file in the current locale's
encoding: for a non-ASCII vignette what that is is recorded in a comment
at the top of the file.

`Sweave()` will produce a `.tex` file in the current encoding,
or in UTF-8 if that is declared. Non-ASCII encodings need to be declared
to LaTeX via a line like

```r
\usepackage[utf8]{inputenc}
```

(It is also possible to use the more recent '`inputenx`' LaTeX
package.) For files where this line is not needed (e.g. chapters
included within the body of a larger document, or non-Sweave vignettes),
the encoding may be declared using a comment like

```r
%\VignetteEncoding{UTF-8}
```

If the encoding is UTF-8, this can also be declared using the
declaration

```r
%\SweaveUTF8
```

If no declaration is given in the vignette, it will be assumed to be in
the encoding declared for the package. If there is no encoding declared
in either place, then it is an error to use non-ASCII characters in the
vignette.

In any case, be aware that LaTeX may require the '`usepackage`'
declaration.

`Sweave()` will also parse and evaluate the R code in each chunk. The R
output will also be in the current locale (or UTF-8 if so declared), and
should be covered by the '`inputenc`' declaration. One thing
people often forget is that the R output may not be ASCII even for ASCII
R sources, for many possible reasons. One common one is the use of
'fancy' quotes: see the R help on `sQuote`: note carefully that it is
not portable to declare UTF-8 or CP1252 to cover such quotes, as their
encoding will depend on the locale used to run `Sweave()`: this can be
circumvented by setting `options(useFancyQuotes="UTF-8")` in the
vignette.

The final issue is the encoding of figures -- this applies only to PDF
figures and not PNG etc. The PDF figures will contain declarations for
their encoding, but the Sweave option `pdf.encoding` may need to be set
appropriately: see the help for the `pdf()` graphics device.

As a real example of the complexities, consider the
[**fortunes**](https://CRAN.R-project.org/package=fortunes) package
version '`1.4-0`'. That package did not have a declared
encoding, and its vignette was in ASCII. However, the data it displays
are read from a UTF-8 CSV file and will be assumed to be in the current
encoding, so `fortunes.tex` will be in UTF-8 in any locale. Had
`read.table` been told the data were UTF-8, `fortunes.tex`
would have been in the locale's encoding.

---

#### 1.4.2 Non-Sweave vignettes

Vignettes in formats other than Sweave are supported _via_ "vignette
engines". For example
[**knitr**](https://CRAN.R-project.org/package=knitr) version 1.1 or
later can create `.tex` files from a variation on Sweave
format, and `.html` files from a variation on "markdown"
format. These engines replace the `Sweave()` function with other
functions to convert vignette source files into LaTeX files for
processing into `.pdf`, or directly into `.pdf` or
`.html` files. The `Stangle()` function is replaced with a
function that extracts the R source from a vignette.

R recognizes non-Sweave vignettes using filename extensions specified by
the engine. For example, the
[**knitr**](https://CRAN.R-project.org/package=knitr) package supports
the extension `.Rmd` (standing for "R markdown"). The user
indicates the vignette engine within the vignette source using a
`\VignetteEngine` line, for example

```r
%\VignetteEngine{knitr::knitr}
```

This specifies the name of a package and an engine to use in place of
Sweave in processing the vignette. As `Sweave` is the only engine
supplied with the R distribution, the package providing any other engine
must be specified in the '`VignetteBuilder`' field of the
package `DESCRIPTION` file, and also specified in the
'`Suggests`', '`Imports`' or '`Depends`'
field (since its namespace must be available to build or check your
package). If more than one package is specified as a builder, they will
be searched in the order given there. The **utils** package is always
implicitly appended to the list of builder packages, but may be included
earlier to change the search order.

Note that a package with non-Sweave vignettes should always have a
'`VignetteBuilder`' field in the `DESCRIPTION` file,
since this is how `R CMD check` recognizes that there are vignettes to
be checked: packages listed there are required when the package is
checked.

The vignette engine can produce `.tex`, `.pdf`, or
`.html` files as output. If it produces `.tex` files,
R will call `texi2pdf` to convert them to `.pdf` for display to
the user (unless there is a `Makefile` in the
`vignettes` directory).

Package writers who would like to supply vignette engines need to
register those engines in the package `.onLoad` function. For example,
that function could make the call

```r
tools::vignetteEngine("knitr", weave = vweave, tangle = vtangle,
                      pattern = "[.]Rmd$", package = "knitr")
```

(The actual registration in
[**knitr**](https://CRAN.R-project.org/package=knitr) is more
complicated, because it supports other input formats.) See the
`?tools::vignetteEngine` help topic for details on engine registration.

---

### 1.5 Package namespaces

R has a namespace management system for code in packages. This system
allows the package writer to specify which variables in the package
should be _exported_ to make them available to package users, and which
variables should be _imported_ from other packages.

The namespace for a package is specified by the `NAMESPACE`
file in the top level package directory. This file contains _namespace
directives_ describing the imports and exports of the namespace.
Additional directives register any shared objects to be loaded and any
S3-style methods that are provided. Note that although the file looks
like R code (and often has R-style comments) it is not processed as R
code. Only very simple conditional processing of `if` statements is
implemented.

Packages are loaded and attached to the search path by calling `library`
or `require`. Only the exported variables are placed in the attached
frame. Loading a package that imports variables from other packages will
cause these other packages to be loaded as well (unless they have
already been loaded), but they will _not_ be placed on the search path
by these implicit loads. Thus code in the package can only depend on
objects in its own namespace and its imports (including the **base**
namespace) being visible[^60^](#FOOT60).

Namespaces are _sealed_ once they are loaded. Sealing means that imports
and exports cannot be changed and that internal variable bindings cannot
be changed. Sealing allows a simpler implementation strategy for the
namespace mechanism. Sealing also allows code analysis and compilation
tools to accurately identify the definition corresponding to a global
variable reference in a function body.

The namespace controls the search strategy for variables used by
functions in the package. If not found locally, R searches the package
namespace first, then the imports, then the base namespace and then the
normal search path.

---

• [Specifying imports and exports](#Specifying-imports-and-exports)     
 • [Registering S3 methods](#Registering-S3-methods)     
 • [Load hooks](#Load-hooks)     
 • [useDynLib](#useDynLib)     
 • [An example](#An-example)     
 • [Namespaces with S4 classes and methods](#Namespaces-with-S4-classes-and-methods)

---

---

#### 1.5.1 Specifying imports and exports

Exports are specified using the `export` directive in the
`NAMESPACE` file. A directive of the form

```r
export(f, g)
```

specifies that the variables `f` and `g` are to be exported. (Note that
variable names may be quoted, and reserved words and non-standard names
such as `[<-.fractions` must be.)

For packages with many variables to export it may be more convenient to
specify the names to export with a regular expression using
`exportPattern`. The directive

```r
exportPattern("^[^\\.]")
```

exports all variables that do not start with a period. However, such
broad patterns are not recommended for production code: it is better to
list all exports or use narrowly-defined groups. (This pattern applies
to S4 classes.) Beware of patterns which include names starting with a
period: some of these are internal-only variables and should never be
exported, e.g. '`.__S3MethodsTable__.`' (and the code nowadays
excludes known cases).

Packages implicitly import the base namespace. Variables exported from
other packages with namespaces need to be imported explicitly using the
directives `import` and `importFrom`. The `import` directive imports all
exported variables from the specified package(s). Thus the directives

```r
import(foo, bar)
```

specifies that all exported variables in the packages **foo** and
**bar** are to be imported. If only some of the exported variables from
a package are needed, then they can be imported using `importFrom`. The
directive

```r
importFrom(foo, f, g)
```

specifies that the exported variables `f` and `g` of the package **foo**
are to be imported. Using `importFrom` selectively rather than `import`
is good practice and recommended notably when importing from packages
with more than a dozen exports.

To import every symbol from a package but for a few exceptions, pass the
`except` argument to `import`. The directive

```r
import(foo, except=c(bar, baz))
```

imports every symbol from **foo** except `bar` and `baz`. The value of
`except` should evaluate to something coercible to a character vector,
after substituting each symbol for its corresponding string.

It is possible to export variables from a namespace which it has
imported from other namespaces: this has to be done explicitly and not
_via_ `exportPattern`.

If a package only needs a few objects from another package it can use a
fully qualified variable reference in the code instead of a formal
import. A fully qualified reference to the function `f` in package
**foo** is of the form `foo::f`. This is slightly less efficient than a
formal import and also loses the advantage of recording all dependencies
in the `NAMESPACE` file (but they still need to be recorded in
the `DESCRIPTION` file). Evaluating `foo::f` will cause package
**foo** to be loaded, but not attached, if it was not loaded
already---this can be an advantage in delaying the loading of a rarely
used package.

Using `foo:::f` instead of `foo::f` allows access to unexported objects.
This is generally not recommended, as the semantics of unexported
objects may be changed by the package author in routine maintenance.

---

#### 1.5.2 Registering S3 methods

The standard method for S3-style `UseMethod` dispatching might fail to
locate methods defined in a package that is imported but not attached to
the search path. To ensure that these methods are available the packages
defining the methods should ensure that the generics are imported and
register the methods using `S3method` directives. If a package defines a
function `print.foo` intended to be used as a `print` method for class
`foo`, then the directive

```r
S3method(print, foo)
```

ensures that the method is registered and available for `UseMethod`
dispatch, and the function `print.foo` does not need to be exported.
Since the generic `print` is defined in **base** it does not need to be
imported explicitly.

(Note that function and class names may be quoted, and reserved words
and non-standard names such as `[<-` and `function` must be.)

It is possible to specify a third argument to S3method, the function to
be used as the method, for example

```r
S3method(print, check_so_symbols, .print.via.format)
```

when `print.check_so_symbols` is not needed.

As of R version 3.6.0, one can also use `S3method()` directives to
perform _delayed_ registration. With

```r
if(getRversion() >= "3.6.0") {
    S3method(pkg::gen, cls)
}
```

function `gen.cls` will get registered as an S3 method for class `cls`
and generic `gen` from package `pkg` only when the namespace of `pkg` is
loaded. This can be employed to deal with situations where the method is
not "immediately" needed, and having to pre-load the namespace of `pkg`
(and all its strong dependencies) in order to perform immediate
registration is considered too "costly".

---

#### 1.5.3 Load hooks

There are a number of hooks called as packages are loaded, attached,
detached, and unloaded. See `help(".onLoad")` for more details.

Since loading and attaching are distinct operations, separate hooks are
provided for each. These hook functions are called `.onLoad` and
`.onAttach`. They both take arguments[^61^](#FOOT61) `libname`
and `pkgname`; they should be defined in the namespace but not exported.

Packages can use a `.onDetach` or `.Last.lib` function (provided the
latter is exported from the namespace) when `detach` is called on the
package. It is called with a single argument, the full path to the
installed package. There is also a hook `.onUnload` which is called when
the namespace is unloaded (_via_ a call to `unloadNamespace`, perhaps
called by `detach(unload = TRUE)`) with argument the full path to the
installed package's directory. `.onUnload` and `.onDetach` should be
defined in the namespace and not exported, but `.Last.lib` does need to
be exported.

Packages are not likely to need `.onAttach` (except perhaps for a
start-up banner); code to set options and load shared objects should be
placed in a `.onLoad` function, or use made of the `useDynLib` directive
described next.

User-level hooks are also available: see the help on function `setHook`.

These hooks are often used incorrectly. People forget to export
`.Last.lib`. Compiled code should be loaded in `.onLoad` (or _via_ a
`useDynLb` directive: see below) and unloaded in `.onUnload`. Do
remember that a package's namespace can be loaded without the namespace
being attached (e.g. by `pkgname::fun`) and that a package can be
detached and re-attached whilst its namespace remains loaded.

---

#### 1.5.4 useDynLib

A `NAMESPACE` file can contain one or more `useDynLib`
directives which allows shared objects that need to be
loaded.[^62^](#FOOT62) The directive

```r
useDynLib(foo)
```

registers the shared object `foo`[^63^](#FOOT63) for loading
with `library.dynam`. Loading of registered object(s) occurs after the
package code has been loaded and before running the load hook function.
Packages that would only need a load hook function to load a shared
object can use the `useDynLib` directive instead.

The `useDynLib` directive also accepts the names of the native routines
that are to be used in R _via_ the `.C`, `.Call`, `.Fortran` and
`.External` interface functions. These are given as additional arguments
to the directive, for example,

```r
useDynLib(foo, myRoutine, myOtherRoutine)
```

By specifying these names in the `useDynLib` directive, the native
symbols are resolved when the package is loaded and R variables
identifying these symbols are added to the package's namespace with
these names. These can be used in the `.C`, `.Call`, `.Fortran` and
`.External` calls in place of the name of the routine and the `PACKAGE`
argument. For instance, we can call the routine `myRoutine` from R with
the code

```r
 .Call(myRoutine, x, y)
```

rather than

```r
 .Call("myRoutine", x, y, PACKAGE = "foo")
```

There are at least two benefits to this approach. Firstly, the symbol
lookup is done just once for each symbol rather than each time the
routine is invoked. Secondly, this removes any ambiguity in resolving
symbols that might be present in several compiled DLLs. However, this
approach is nowadays deprecated in favour of supplying registration
information (see below).

In some circumstances, there will already be an R variable in the
package with the same name as a native symbol. For example, we may have
an R function in the package named `myRoutine`. In this case, it is
necessary to map the native symbol to a different R variable name. This
can be done in the `useDynLib` directive by using named arguments. For
instance, to map the native symbol name `myRoutine` to the R variable
`myRoutine_sym`, we would use

```r
useDynLib(foo, myRoutine_sym = myRoutine, myOtherRoutine)
```

We could then call that routine from R using the command

```r
 .Call(myRoutine_sym, x, y)
```

Symbols without explicit names are assigned to the R variable with that
name.

In some cases, it may be preferable not to create R variables in the
package's namespace that identify the native routines. It may be too
costly to compute these for many routines when the package is loaded if
many of these routines are not likely to be used. In this case, one can
still perform the symbol resolution correctly using the DLL, but do this
each time the routine is called. Given a reference to the DLL as an R
variable, say `dll`, we can call the routine `myRoutine` using the
expression

```r
 .Call(dll$myRoutine, x, y)
```

The `$` operator resolves the routine with the given name in the DLL
using a call to `getNativeSymbol`. This is the same computation as above
where we resolve the symbol when the package is loaded. The only
difference is that this is done each time in the case of
`dll$myRoutine`.

In order to use this dynamic approach (e.g., `dll$myRoutine`), one needs
the reference to the DLL as an R variable in the package. The DLL can be
assigned to a variable by using the `variable = dllName` format used
above for mapping symbols to R variables. For example, if we wanted to
assign the DLL reference for the DLL `foo` in the example above to the
variable `myDLL`, we would use the following directive in the
`NAMESPACE` file:

```r
myDLL = useDynLib(foo, myRoutine_sym = myRoutine, myOtherRoutine)
```

Then, the R variable `myDLL` is in the package's namespace and available
for calls such as `myDLL$dynRoutine` to access routines that are not
explicitly resolved at load time.

If the package has registration information (see [Registering native routines](#Registering-native-routines)), then we can use that directly
rather than specifying the list of symbols again in the `useDynLib`
directive in the `NAMESPACE` file. Each routine in the
registration information is specified by giving a name by which the
routine is to be specified along with the address of the routine and any
information about the number and type of the parameters. Using the
`.registration` argument of `useDynLib`, we can instruct the namespace
mechanism to create R variables for these symbols. For example, suppose
we have the following registration information for a DLL named `myDLL`:

```r
static R_NativePrimitiveArgType foo_t[] = {
    REALSXP, INTSXP, STRSXP, LGLSXP
};

static const R_CMethodDef cMethods[] = {
   {"foo", (DL_FUNC) &foo, 4, foo_t},
   {"bar_sym", (DL_FUNC) &bar, 0},
   {NULL, NULL, 0, NULL}
};

static const R_CallMethodDef callMethods[] = {
   {"R_call_sym", (DL_FUNC) &R_call, 4},
   {"R_version_sym", (DL_FUNC) &R_version, 0},
   {NULL, NULL, 0}
};
```

Then, the directive in the `NAMESPACE` file

```r
useDynLib(myDLL, .registration = TRUE)
```

causes the DLL to be loaded and also for the R variables `foo`,
`bar_sym`, `R_call_sym` and `R_version_sym` to be defined in the
package's namespace.

Note that the names for the R variables are taken from the entry in the
registration information and do not need to be the same as the name of
the native routine. This allows the creator of the registration
information to map the native symbols to non-conflicting variable names
in R, e.g. `R_version` to `R_version_sym` for use in an R function such
as

```r
R_version <- function()
{
  .Call(R_version_sym)
}
```

Using argument `.fixes` allows an automatic prefix to be added to the
registered symbols, which can be useful when working with an existing
package. For example, package
[**KernSmooth**](https://CRAN.R-project.org/package=KernSmooth) has

```r
useDynLib(KernSmooth, .registration = TRUE, .fixes = "F_")
```

which makes the R variables corresponding to the Fortran symbols
`F_bkde` and so on, and so avoid clashes with R code in the namespace.

**NB**: Using these arguments for a package which does not register
native symbols merely slows down the package loading (although at the
time of writing 90 CRAN packages did so). Once symbols are registered,
check that the corresponding R variables are not accidentally exported
by a pattern in the `NAMESPACE` file.

---

#### 1.5.5 An example

As an example consider two packages named **foo** and **bar**. The R
code for package **foo** in file `foo.R` is

> +-----------------------------------------------------------------------+
> | |
> | `r | | x <- 1 | | f <- function(y) c(x,y) | | foo <- function(x) .Call("foo", x, PACKAGE="foo") | | print.foo <- function(x, ...) cat("<a foo>\n") | |` |
> | ::: |
> +-----------------------------------------------------------------------+

Some C code defines a C function compiled into DLL `foo` (with an
appropriate extension). The `NAMESPACE` file for this package
is

> +-----------------------------------------------------------------------+
> | |
> | `r | | useDynLib(foo) | | export(f, foo) | | S3method(print, foo) | |` |
> | ::: |
> +-----------------------------------------------------------------------+

The second package **bar** has code file `bar.R`

> +-----------------------------------------------------------------------+
> | |
> | `r | | c <- function(...) sum(...) | | g <- function(y) f(c(y, 7)) | | h <- function(y) y+9 | |` |
> | ::: |
> +-----------------------------------------------------------------------+

and `NAMESPACE` file

> +-----------------------------------------------------------------------+
> | |
> | `r | | import(foo) | | export(g, h) | |` |
> | ::: |
> +-----------------------------------------------------------------------+

Calling `library(bar)` loads **bar** and attaches its exports to the
search path. Package **foo** is also loaded but not attached to the
search path. A call to `g` produces

```r
> g(6)
[1]  1 13
```

This is consistent with the definitions of `c` in the two settings: in
**bar** the function `c` is defined to be equivalent to `sum`, but in
**foo** the variable `c` refers to the standard function `c` in
**base**.

---

#### 1.5.6 Namespaces with S4 classes and methods

Some additional steps are needed for packages which make use of formal
(S4-style) classes and methods (unless these are purely used
internally). The package should have `Depends: methods` in its
`DESCRIPTION` and `import(methods)` or
`importFrom(methods, ...)` plus any classes and methods which are to be
exported need to be declared in the `NAMESPACE` file. For
example, the **stats4** package has

```r
export(mle) # exporting methods implicitly exports the generic
importFrom("graphics", plot)
importFrom("stats", optim, qchisq)
## For these, we define methods or (AIC, BIC, nobs) an implicit generic:
importFrom("stats", AIC, BIC, coef, confint, logLik, nobs, profile,
           update, vcov)
exportClasses(mle, profile.mle, summary.mle)
## All methods for imported generics:
exportMethods(coef, confint, logLik, plot, profile, summary,
              show, update, vcov)
## implicit generics which do not have any methods here
export(AIC, BIC, nobs)
```

All S4 classes to be used outside the package need to be listed in an
`exportClasses` directive. Alternatively, they can be specified using
`exportClassPattern`[^64^](#FOOT64) in the same style as for
`exportPattern`. To export methods for generics from other packages an
`exportMethods` directive can be used.

Note that exporting methods on a generic in the namespace will also
export the generic, and exporting a generic in the namespace will also
export its methods. If the generic function is not local to this
package, either because it was imported as a generic function or because
the non-generic version has been made generic solely to add S4 methods
to it (as for functions such as `plot` in the example above), it can be
declared _via_ either or both of `export` or `exportMethods`, but the
latter is clearer (and is used in the **stats4** example above). In
particular, for primitive functions there is no generic function, so
`export` would export the primitive, which makes no sense. On the other
hand, if the generic is local to this package, it is more natural to
export the function itself using `export()`, and this _must_ be done if
an implicit generic is created without setting any methods for it (as is
the case for `AIC` in **stats4**).

A non-local generic function is only exported to ensure that calls to
the function will dispatch the methods from this package (and that is
not done or required when the methods are for primitive functions). For
this reason, you do not need to document such implicitly created generic
functions, and `undoc` in package **tools** will not report them.

If a package uses S4 classes and methods exported from another package,
but does not import the entire namespace of the other
package[^65^](#FOOT65), it needs to import the classes and
methods explicitly, with directives

```r
importClassesFrom(package, ...)
importMethodsFrom(package, ...)
```

listing the classes and functions with methods respectively. Suppose we
had two small packages **A** and **B** with **B** using **A**. Then they
could have `NAMESPACE` files

> +-----------------------------------------------------------------------+
> | |
> | `r | | export(f1, ng1) | | exportMethods("[") | | exportClasses(c1) | |` |
> | ::: |
> +-----------------------------------------------------------------------+

and

> +-----------------------------------------------------------------------+
> | |
> | `r | | importFrom(A, ng1) | | importClassesFrom(A, c1) | | importMethodsFrom(A, f1) | | export(f4, f5) | | exportMethods(f6, "[") | | exportClasses(c1, c2) | |` |
> | ::: |
> +-----------------------------------------------------------------------+

respectively.

Note that `importMethodsFrom` will also import any generics defined in
the namespace on those methods.

It is important if you export S4 methods that the corresponding generics
are available. You may for example need to import `plot` from
**graphics** to make visible a function to be converted into its
implicit generic. But it is better practice to make use of the generics
exported by **stats4** as this enables multiple packages to
unambiguously set methods on those generics.

---

### 1.6 Writing portable packages

This section contains advice on writing packages to be used on multiple
platforms or for distribution (for example to be submitted to a package
repository such as CRAN).

---

• [PDF size](#PDF-size)     
 • [Check timing](#Check-timing)     
 • [Encoding issues](#Encoding-issues)     
 • [Portable C and C++ code](#Portable-C-and-C_002b_002b-code)     
 • [Binary distribution](#Binary-distribution)

---

Portable packages should have simple file names: use only alphanumeric
ASCII characters and period (`.`), and avoid those names not allowed
under Windows (see [Package structure](#Package-structure)).

Many of the graphics devices are platform-specific: even `X11()` (aka
`x11()`) which although emulated on Windows may not be available on a
Unix-alike (and is not the preferred screen device on OS X). It is
rarely necessary for package code or examples to open a new device, but
if essential,[^66^](#FOOT66) use `dev.new()`.

Use `R CMD build` to make the release `.tar.gz` file.

`R CMD check` provides a basic set of checks, but often further problems
emerge when people try to install and use packages submitted to CRAN --
many of these involve compiled code. Here are some further checks that
you can do to make your package more portable.

- If your package has a `configure` script, provide a
  `configure.win` script to be used on Windows (an empty file
  if no actions are needed).

- If your package has a `Makevars` or `Makefile`
  file, make sure that you use only portable make features. Such files
  should be LF-terminated[^67^](#FOOT67) (including the final
  line of the file) and not make use of GNU extensions. (The POSIX
  specification is available at
  <http://pubs.opengroup.org/onlinepubs/9699919799/utilities/make.html>;
  anything not documented there should be regarded as an extension to
  be avoided. Further advice can be found at
  <https://www.gnu.org/software/autoconf/manual/autoconf.html#Portable-Make>.
  ) Commonly misused GNU extensions are conditional inclusions (`ifeq`
  and the like), `${shell ...}`, `${wildcard ...}` and similar, and
  the use of `+=`[^68^](#FOOT68) and `:=`. Also, the use of
  `$<` other than in implicit rules is a GNU extension, as is the `$^`
  macro. As is the use of `.PHONY` (some other makes ignore it).
  Unfortunately makefiles which use GNU extensions often run on other
  platforms but do not have the intended results.

  The use of `${shell ...}` can be avoided by using backticks, e.g.

```r
PKG_CPPFLAGS = `gsl-config --cflags`
```

which works in all versions of `make` known[^69^](#FOOT69)
to be used with R.

If you really must require GNU make, declare it in the
`DESCRIPTION` file by

```r
SystemRequirements: GNU make
```

and ensure that you use the value of environment variable `MAKE`
(and not just `make`) in your scripts. (On some platforms GNU make
is available under a name such as `gmake`, and there
`SystemRequirements` is used to set `MAKE`.)

If you only need GNU make for parts of the package which are rarely
needed (for example to create bibliography files under
`vignettes`), use a file called `GNUmakefile`
rather than `Makefile` as GNU make (only) will use the
former.

Since the only viable make for Windows is GNU make, it is
permissible to use GNU extensions in files `Makevars.win`
or `Makefile.win`.

- Bash extensions also need to be avoided in shell scripts, including
  expressions in Makefiles (which are passed to the shell for
  processing). Some R platforms use strict[^70^](#FOOT70)
  Bourne shells: the R toolset on Windows and some Unix-alike OSes use
  `ash` (<https://en.wikipedia.org/wiki/Almquist_shell>), a rather
  minimal shell with few builtins. Beware of assuming that all the
  POSIX command-line utilities are available, especially on Windows
  where only a minimal set is provided for use with R. (See [The
  command line tools](./R-admin.html#The-command-line-tools) in R
  Installation and Administration.) One particular issue is the use of
  `echo`, for which two behaviours are allowed
  (<http://pubs.opengroup.org/onlinepubs/9699919799/utilities/echo.html>)
  and both occur as defaults on R platforms: portable applications
  should not use `-n` (as the first argument) nor escape
  sequences. The recommended replacement for `echo -n` is the command
  `printf`. Another common issue is the construction

```r
export FOO=value
```

which is bash-specific (first set the variable then export it by
name).

Using `test -e` (or `[ -e ]`) in shell scripts is not portable: `-f`
is normally what is intended. Flags `-a` and `-o`
are nowadays declared obsolescent by POSIX and should not be used.

Use of 'brace expansion', e.g.,

```r
rm -f src/*.{o,so,d}
```

is not portable.

The `-o` flag for `set` in shell scripts is optional in
POSIX and not supported on all the platforms R is used on.

On macOS Catalina which shell `/bin/sh` invokes is user-
and platform-dependent: it might be `bash` version 3.2, `dash` or
`zsh` (for new accounts it is `zsh`, for accounts ported from an
earlier version it is usually `bash`).

- Make use of the abilities of your compilers to check the
  standards-conformance of your code. For example, `gcc` and
  `gfortran`[^71^](#FOOT71) can be used with options
  `-Wall -pedantic` to alert you to potential problems. This
  is particularly important for C++, where `g++ -Wall -pedantic` will
  alert you to the use of some of the GNU extensions which fail to
  compile on most other C++ compilers. If R was not configured
  accordingly, one can achieve this _via_ personal `Makevars`
  files. See [Customizing package
  compilation](./R-admin.html#Customizing-package-compilation) in R
  Installation and Administration,

  Portable C++ code needs to follow the 1998 standard (and not use
  features from C99), or to specify a C++11 compiler (see [Using C++11
  code](#Using-C_002b_002b11-code)) where available (which is not the
  case on all R platforms). Currently C++14 code is less portable and
  C++17 support is patchy across R platforms.

  If using Fortran with the GNU compiler, use the flags
  `-std=f95 -Wall -pedantic` which reject most GNU extensions
  and features from later standards. (Although R only requires Fortran
  90, `gfortran` does not have a way to specify that standard.)

  R has tested that `DOUBLE COMPLEX` works and so is preferred to
  `COMPLEX*16`. (One can also use something like
  `COMPLEX(KIND=KIND(0.0D0))`[^72^](#FOOT72).)

  Not all common R platforms conform to the expected standards, e.g.
  C99 for C code. One common area of problems is the `*printf`
  functions where Windows does not support `%lld`, `%Lf` and similar
  formats (and has its own formats such as `%I64d` for 64-bit
  integers). It is very rare to need to output such types, and 64-bit
  integers can usually be converted to doubles for output. However,
  the C11 standard (section 7.8.1) includes `PRIxNN`
  macros[^73^](#FOOT73) in C header `inttypes.h`
  (for example `PRId64`) so the portable approach is to test for these
  and if not available provide emulations in the package.

- `R CMD check` performs some checks for non-portable compiler/linker
  flags in `src/Makevars`. However, it cannot check the
  meaning of such flags, and some are commonly accepted but with
  compiler-specific meanings. There are other non-portable flags which
  are not checked, nor are `src/Makefile` files and makefiles
  in sub-directories. As a comment in the code says

  > It is hard to think of anything apart from `-I*` and
  > `-D*` that is safe for general use ...

  although `-pthread` is pretty close to portable. (Option
  `-U` is portable but little use on the command line as it
  will only cancel built-in defines (not portable) and those defined
  earlier on the command line (R does not use any).)

  People have used `configure` to customize `src/Makevars`,
  including for specific compilers. This is unsafe for several
  reasons. First, unintended compilers might meet the check---for
  example, several compilers other than GCC identify themselves as
  'GCC' whilst being only partially conformant. Second, future
  versions of compilers may behave differently (including updates to
  quite old series) so for example `-Werror` (and
  specializations) can make a package non-installable under a future
  version. Third, using flags to suppress diagnostic messages can hide
  important information for debugging on a platform not tested by the
  package maintainer. (`R CMD check` can optionally report on unsafe
  flags which were used.)

  Avoid the use of `-march` and especially
  `-march=native`. This allows the compiler to generate code
  that will only run on a particular class of CPUs (that of the
  compiling machine for '`native`'). People assume this is a
  'minimum' CPU specification, but that is not how it is documented
  for `gcc` (it is accepted by `clang` but apparently it is
  undocumented what precisely it does, and it can be accepted and may
  be ignored for other compilers). (For personal use `-mtune`
  is safer, but still not portable enough to be used in a public
  package.) Not even `gcc` supports '`native`' for all CPUs,
  and it can do surprising things if it finds a CPU released later
  than its version.

- Do be very careful with passing arguments between R, C and Fortran
  code. In particular, `long` in C will be 32-bit on some R platforms
  (including 64-bit Windows), but 64-bit on most modern Unix and Linux
  platforms. It is rather unlikely that the use of `long` in C code
  has been thought through: if you need a longer type than `int` you
  should use a configure test for a C99/C++11 type such as
  `int_fast64_t` (and failing that,
  `long long`[^74^](#FOOT74)) and typedef your own type, or
  use another suitable type (such as `size_t`).

  It is not safe to assume that `long` and pointer types are the same
  size, and they are not on 64-bit Windows. If you need to convert
  pointers to and from integers use the C99/C++11 integer types
  `intptr_t` and `uintptr_t` (in the headers `<stdint.h>` and
  `cstdint`: they are not required to be implemented by the standards
  but are used in C code by R itself).

  Note that `integer` in Fortran corresponds to `int` in C on all R
  platforms.

- Under no circumstances should your compiled code ever call `abort`
  or `exit`[^75^](#FOOT75): these terminate the user's R
  process, quite possibly losing all unsaved work. One usage that
  could call `abort` is the `assert` macro in C or C++ functions,
  which should never be active in production code. The normal way to
  ensure that is to define the macro `NDEBUG`, and `R CMD INSTALL`
  does so as part of the compilation flags. If you wish to use
  `assert` during development. you can include `-UNDEBUG` in
  `PKG_CPPFLAGS`. Note that your own `src/Makefile` or
  makefiles in sub-directories may also need to define `NDEBUG`.

  This applies not only to your own code but to any external software
  you compile in or link to.

- Compiled code should not write to `stdout` or
  `stderr` and C++ and Fortran I/O should not be used. As
  with the previous item such calls may come from external software
  and may never be called, but package authors are often mistaken
  about that.

- Compiled code should not call the system random number generators
  such as `rand`, `drand48` and `random`[^76^](#FOOT76), but
  rather use the interfaces to R's RNGs described in [Random
  numbers](#Random-numbers). In particular, if more than one package
  initializes the system RNG (e.g. _via_ `srand`), they will interfere
  with each other.

  Nor should the C++11 random number library be used, nor any other
  third-party random number generators such as those in GSL.

- Errors in memory allocation and reading/writing outside arrays are
  very common causes of crashes (e.g., segfaults) on some machines.
  See [Checking memory access](#Checking-memory-access) for tools
  which can be used to look for this.

- Many platforms will allow unsatisfied entry points in compiled code,
  but will crash the application (here R) if they are ever used. Some
  (notably Windows) will not. Looking at the output of

```r
nm -pg mypkg.so
```

and checking if any of the symbols marked `U` is unexpected is a
good way to avoid this.

- Linkers have a lot of freedom in how to resolve entry points in
  dynamically-loaded code, so the results may differ by platform. One
  area that has caused grief is packages including copies of standard
  system software such as `libz` (especially those already linked into
  R). In the case in point, entry point `gzgets` was sometimes
  resolved against the old version compiled into the package,
  sometimes against the copy compiled into R and sometimes against the
  system dynamic library. The only safe solution is to rename the
  entry points in the copy in the package. We have even seen problems
  with entry point name `myprintf`, which is a system entry
  point[^77^](#FOOT77) on some Linux systems.

- Conflicts between symbols in DLLs are handled in very
  platform-specific ways. Good ways to avoid trouble are to make as
  many symbols as possible static (check with `nm -pg`), and to use
  names which are clearly tied to your package (which also helps users
  if anything does go wrong). Note that symbol names starting with
  `R_` are regarded as part of R's namespace and should not be used in
  packages.

- It is good practice for DLLs to register their symbols (see
  [Registering native routines](#Registering-native-routines)),
  restrict visibility (see [Controlling
  visibility](#Controlling-visibility)) and not allow symbol search
  (see [Registering native routines](#Registering-native-routines)).
  It should be possible for a DLL to have only one visible symbol,
  `R_init_pkgname`, on suitable platforms[^78^](#FOOT78),
  which would completely avoid symbol conflicts.

- It is not portable to call compiled code in R or other packages
  _via_ `.Internal`, `.C`, `.Fortran`, `.Call` or `.External`, since
  such interfaces are subject to change without notice and will
  probably result in your code terminating the R process.

- Do not use (hard or symbolic) file links in your package sources.
  Where possible `R CMD build` will replace them by copies.

- If you do not yourself have a Windows system, consider submitting
  your source package to WinBuilder
  (<https://win-builder.r-project.org/>) before distribution.

- It is bad practice for package code to alter the search path using
  `library`, `require` or `attach` and this often does not work as
  intended. For alternatives, see [Suggested
  packages](#Suggested-packages) and `with`.

- Examples can be run interactively _via_ `example` as well as in
  batch mode when checking. So they should behave appropriately in
  both scenarios, conditioning by `interactive()` the parts which need
  an operator or observer. For instance, progress
  bars[^79^](#FOOT79) are only appropriate in interactive
  use, as is displaying help pages or calling `View()` (see below).

- Be careful with the order of entries in macros such as `PKG_LIBS`.
  Some linkers will re-order the entries, and behaviour can differ
  between dynamic and static libraries. Generally `-L`
  options should precede[^80^](#FOOT80) the libraries
  (typically specified by `-l` options) to be found from
  those directories, and libraries are searched once in the order they
  are specified. Not all linkers allow a space after `-L` .

- Care is needed with the use of `LinkingTo`. This puts one or more
  directories on the include search path ahead of system headers but
  (prior to R 3.4.0) after those specified in the `CPPFLAGS` macro of
  the R build (which normally includes `-I/usr/local/include`, but
  most platforms ignore that and include it with the system headers).

  Any confusion would be avoided by having `LinkingTo` headers in a
  directory named after the package. In any case, name conflicts of
  headers and directories under package `include` directories
  should be avoided, both between packages and between a package and
  system and third-party software.

- The `ar` utility is often used in makefiles to make static
  libraries. Its modifier `u` is defined by POSIX but is disabled in
  GNU `ar` on some recent Linux distributions which use 'deterministic
  mode'. The safest way to make a static library is to first remove
  any existing file of that name then use `ar -cr` and then `ranlib`
  if needed (which is system-dependent: on most
  systems[^81^](#FOOT81) `ar` always maintains a symbol
  table). The POSIX standard says options should be preceded by a
  hyphen (as in `-cr`), although most OSes accept them
  without. Note that on some systems `ar -cr` must have at least one
  file specified.

- Some people have a need to set a locale. Locale names are not
  portable, and e.g. '`fr_FR.utf8`' is commonly used on Linux
  but not accepted on either Solaris or macOS.
  '`fr_FR.UTF-8`' is more portable, being accepted on recent
  Linux, AIX, FreeBSD, macOS and Solaris (at least). However, some
  Linux distributions micro-package, so locales defined by **glibc**
  (including these examples) may not be installed.

- Avoid spaces in file names, not least as they can cause difficulties
  for external tools. A recent example was a package with a
  [**knitr**](https://CRAN.R-project.org/package=knitr) vignette that
  used spaces in plot names: this caused some versions of `pandoc` to
  fail with a baffling error message.

  Non-ASCII filenames can also cause problems (particularly in
  non-UTF-8 locales).

- Make sure that any version requirement for Java code is both
  declared in the '`SystemRequirements`'
  field[^82^](#FOOT82) and tested at runtime (not least as
  the Java installation when the package is installed might not be the
  same as when the package is run and will not be for binary
  packages). Java 8 is available for fewer platforms than Java 7, and
  Java 11 for fewer still (at the time of writing, only
  '`x86_64`' Linux, macOS, 64-bit Windows and 64-bit Solaris
  11 from Oracle).

  When specifying a minimum Java version please use the official
  version names, which are (confusingly)

```r
1.1 1.2 1.3 1.4 5.0 6 7 8 9 10 11 12 13
```

and as from 2018 a year.month scheme such as '`18.3`' is
also in use.

A suitable test for Java at least version 8 for packages using
[**rJava**](https://CRAN.R-project.org/package=rJava) would be
something like

```r
.jinit()
jv <- .jcall("java/lang/System", "S", "getProperty", "java.runtime.version")
if(substr(jv, 1L, 2L) == "1.") {
  jvn <- as.numeric(paste0(strsplit(jv, "[.]")[[1L]][1:2], collapse = "."))
  if(jvn < 1.8) stop("Java >= 8 is needed for this package but not available")
}
```

Java 9 changed the format of this string (which used to be something
like '`1.8.0_162-b12`'); Java 11 gives `jv` as
'`11+28`' whereas Java 10.0.2 gave '`10.0.2+10`'.
(<http://openjdk.java.net/jeps/322> details the current scheme. Note
that it is necessary to allow for pre-releases like
'`11-ea+22`'.)

Note too that the compiler used to produce a `jar` can impose a
minimum Java version, often resulting in an arcane message like

```r
java.lang.UnsupportedClassVersionError: ... Unsupported major.minor version 52.0
```

(Where <https://en.wikipedia.org/wiki/Java_class_file> maps
class-file version numbers to Java versions.) Compile with something
like `javac -target 1.6` to ensure this is avoided. (As from Java 8,
`javac` defaults to compiling for Java 8. Versions as old as
'`1.6`' are already deprecated and will give a warning with
Java 10's `javac`.) Note this also applies to packages distributing
(or even downloading) compiled Java code produced by others, so
their requirements need to be checked (they are often not documented
accurately) and accounted for. It should be possible to check the
class-file version _via_ command-line utility `javap`, if necessary
after extracting the `.class` files from a `.jar`
archive.

Some packages have stated a requirement on a particular JDK, but a
package should only be requiring a JRE unless providing its own Java
interface.

- A package with a hard-to-satisfy system requirement is by definition
  not portable, annoyingly so if this is not declared in the
  '`SystemRequirements`' field. The most common example is
  the use of `pandoc`, which is only available for a very limited
  range of platforms (and has onerous requirements to install from
  source) and has capabilities[^83^](#FOOT83) that vary by
  build but are not documented.

  Usage of external commands should always be conditional on a test
  for presence (perhaps using `Sys.which`), as well as declared in the
  '`SystemRequirements`' field. A package should pass its
  checks without warnings nor errors without the external command
  being present.

  An external command can be a (possibly optional) requirement for an
  imported or suggested package but needed for examples, tests or
  vignettes in the package itself. Such usages should always be
  declared and conditional.

  Interpreters for scripting languages such as Perl, Python and Ruby
  need to be declared as system requirements and used conditionally:
  for example macOS 10.16 has been announced not to have them. Python
  2 has passed end-of-life and been removed from some major
  distributions. This applies also to a Java interpreter (which macOS
  does not have by default).

- Be sure to use portable encoding names: none of `utf8`, `mac` and
  `macroman` is. See the help for `file` for more details.

- Do not invoke R by plain `R`, `Rscript` or (on Windows) `Rterm` in
  your examples, tests, vignettes, makefiles or other scripts. As
  pointed out in several places earlier in this manual, use something
  like

```r
"$(R_HOME)/bin/Rscript"
"$(R_HOME)/bin$(R_ARCH_BIN)/Rterm"
```

with appropriate quotes (as, although not recommended, `R_HOME` can
contain spaces).

- Do not use `R_HOME` in makefiles except when passing them to the
  shell. Specifically, do not use `R_HOME` in the argument to
  `include`, as `R_HOME` can contain spaces. Quoting the argument to
  `include` does not help. GNU `make`'s `include` accepts spaces when
  escaped using backslashes (GNU `make` syntax required):

```r
## WARNING: requires GNU make (allowed on Windows)
sp =
sp +=
sq = $(subst $(sp),\ ,$1)
include $(call sq,${R_HOME}/etc${R_ARCH}/Makeconf)
```

A portable and the recommended way to avoid the problem of spaces in
`${R_HOME}` is using option `-f` of `make`. This is easy to do with
recursive invocation of `make`, which is also the only usual
situation when `R_HOME` is needed in the argument for `include`.

```r
$(MAKE) -f "${R_HOME}/etc${R_ARCH}/Makeconf" -f Makefile.inner
```

Do be careful in what your tests (and examples) actually test. Bad
practice seen in distributed packages include:

- It is not reasonable to test the time taken by a command: you cannot
  know how fast or how heavily loaded an R platform might be. At best
  you can test a ratio of times, and even that is fraught with
  difficulties and not advisable: the just-in-time compiler (JIT) and
  the GC may trigger at unpredictable times, following heuristics that
  may change without notice.

- Do not test the exact format of R messages (from R itself or from
  other packages): They change, and they can be translated.

  Packages have even tested the exact format of system error messages,
  which are platform-dependent and perhaps locale-dependent.

- If you use functions such as `View`, remember that in testing there
  is no one to look at the output. It is better to use something like
  one of

```r
if(interactive()) View(obj) else print(head(obj))
if(interactive()) View(obj) else str(obj)
```

- Be careful when comparing file paths. There can be multiple paths to
  a single file, and some of these can be very long character strings.
  If possible canonicalize paths before comparisons, but study
  `?normalizePath` to be aware of the pitfalls.

- Only test the accuracy of results if you have done a formal error
  analysis. Things such as checking that probabilities numerically sum
  to one are silly: numerical tests should always have a tolerance.
  That the tests on your platform achieve a particular tolerance says
  little about other platforms. R is configured by default to make use
  of long doubles where available, but they may not be available or be
  too slow for routine use. Most R platforms use '`ix86`' or
  '`x86_64`' CPUs: these may use extended precision registers
  on some but not all of their FPU instructions. Thus the achieved
  precision can depend on the compiler version and optimization
  flags---our experience is that 32-bit builds tend to be less precise
  than 64-bit ones. But not all platforms use those CPUs, and not
  all[^84^](#FOOT84) which use them configure them to allow
  the use of extended precision. In particular, ARM CPUs do not
  (currently) have extended precision nor long doubles, and long
  double was 64-bit on HP/PA Linux.

  If you must try to establish a tolerance empirically, configure and
  build R with `--disable-long-double` and use appropriate
  compiler flags (such as `-ffloat-store` and
  `-fexcess-precision=standard` for `gcc`, depending on the
  CPU type[^85^](#FOOT85)) to mitigate the effects of
  extended-precision calculations.

  Tests which involve random inputs or non-deterministic algorithms
  should normally set a seed or be tested for many seeds.

---

#### 1.6.1 PDF size

There are a several tools available to reduce the size of PDF files:
often the size can be reduced substantially with no or minimal loss in
quality. Not only do large files take up space: they can stress the PDF
viewer and take many minutes to print (if they can be printed at all).

`qpdf` (<http://qpdf.sourceforge.net/>) can compress losslessly. It is
fairly readily available (e.g. it has binaries for Windows and packages
in Debian/Ubuntu/Fedora, and is installed as part of the CRAN macOS
distribution of R). `R CMD build` has an option to run `qpdf` over PDF
files under `inst/doc` and replace them if at least 10Kb and
10% is saved. The full path to the `qpdf` command can be supplied as
environment variable `R_QPDF` (and is on the CRAN binary of R for
macOS). It seems MiKTeX does not use PDF object compression and so
`qpdf` can reduce considerably the files it outputs: MiKTeX's defaults
can be overridden by code in the preamble of an Sweave or LaTeX file ---
see how this is done for the R reference manual at
<https://svn.r-project.org/R/trunk/doc/manual/refman.top>. (Although
earlier versions of `qpdf` are supported, versions 6.0.0 and later in
some cases achieve considerably better compression.)

Other tools can reduce the size of PDFs containing bitmap images at
excessively high resolution. These are often best re-generated (for
example `Sweave` defaults to 300 ppi, and 100--150 is more appropriate
for a package manual). These tools include Adobe Acrobat (not Reader),
Apple's Preview[^86^](#FOOT86) and Ghostscript (which converts
PDF to PDF by

```r
ps2pdf options -dAutoRotatePages=/None -dPrinted=false in.pdf out.pdf
```

and suitable options might be

```r
-dPDFSETTINGS=/ebook
-dPDFSETTINGS=/screen
```

; see <http://www.ghostscript.com/doc/current/Ps2pdf.htm> for more such
and consider all the options for image downsampling). There have been
examples in CRAN packages for which current versions of Ghostscript
produced much bigger reductions than earlier ones.

We come across occasionally large PDF files containing excessively
complicated figures using PDF vector graphics: such figures are often
best redesigned or failing that, output as PNG files.

Option `--compact-vignettes` to `R CMD build` defaults to value
'`qpdf`': use '`both`' to try harder to reduce the
size, provided you have Ghostscript available (see the help for
`tools::compactPDF`).

---

#### 1.6.2 Check timing

There are several ways to find out where time is being spent in the
check process. Start by setting the environment variable
`_R_CHECK_TIMINGS_` to '`0`'. This will report the total CPU
times (not Windows) and elapsed times for installation and running
examples, tests and vignettes, under each sub-architecture if
appropriate. For tests and vignettes, it reports the time for each as
well as the total.

Setting `_R_CHECK_TIMINGS_` to a positive value sets a threshold (in
seconds elapsed time) for reporting timings.

If you need to look in more detail at the timings for examples, use
option `--timings` to `R CMD check` (this is set by
`--as-cran`). This adds a summary to the check output for all
the examples with CPU or elapsed time of more than 5 seconds. It
produces a file `mypkg.Rcheck/mypkg-Ex.timings` containing
timings for each help file: it is a tab-delimited file which can be read
into R for further analysis.

Timings for the tests and vignette runs are given at the bottom of the
corresponding log file: note that log files for successful vignette runs
are only retained if environment variable
`_R_CHECK_ALWAYS_LOG_VIGNETTE_OUTPUT_` is set to a true value.

---

#### 1.6.3 Encoding issues

Care is needed if your package contains non-ASCII text, and in
particular if it is intended to be used in more than one locale. It is
possible to mark the encoding used in the `DESCRIPTION` file
and in `.Rd` files, as discussed elsewhere in this manual.

First, consider carefully if you really need non-ASCII text. Many users
of R will only be able to view correctly text in their native language
group (e.g. Western European, Eastern European, Simplified Chinese) and
ASCII.[^87^](#FOOT87). Other characters may not be rendered at
all, rendered incorrectly, or cause your R code to give an error. For
`.Rd` documentation, marking the encoding and including ASCII
transliterations is likely to do a reasonable job. The set of characters
which is commonly supported is wider than it used to be around 2000, but
non-Latin alphabets (Greek, Russian, Georgian, ...) are still often
problematic and those with double-width characters (Chinese, Japanese,
Korean, emoji) often need specialist fonts to render correctly.

Several CRAN packages have messages in their R code in French (and a few
in German). A better way to tackle this is to use the
internationalization facilities discussed elsewhere in this manual.

Function `showNonASCIIfile` in package **tools** can help in finding
non-ASCII bytes in files.

There is a portable way to have arbitrary text in character strings
(only) in your R code, which is to supply them in Unicode as
'`\uxxxx`' escapes. If there are any characters not in the
current encoding the parser will encode the character string as UTF-8
and mark it as such. This applies also to character strings in datasets:
they can be prepared using '`\uxxxx`' escapes or encoded in
UTF-8 in a UTF-8 locale, or even converted to UTF-8 _via_ `iconv()`. If
you do this, make sure you have '`R (>= 2.10)`' (or later) in
the '`Depends`' field of the `DESCRIPTION` file.

R sessions running in non-UTF-8 locales will if possible re-encode such
strings for display (and this is done by `RGui` on Windows, for
example). Suitable fonts will need to be selected or made
available[^88^](#FOOT88) both for the console/terminal and
graphics devices such as '`X11()`' and '`windows()`'.
Using '`postscript`' or '`pdf`' will choose a default
8-bit encoding depending on the language of the UTF-8 locale, and your
users would need to be told how to select the '`encoding`'
argument.

Note that the previous two paragraphs only apply to character strings in
R code. Non-ASCII characters are particularly prevalent in comments (in
the R code of the package, in examples, tests, vignettes and even in the
`NAMESPACE` file) but should be avoided there. Most commonly
people use the Windows extensions to Latin-1 (often directional single
and double quotes, ellipsis, bullet and en and em dashes) which are not
supported in strict Latin-1 locales nor in CJK locales on Windows. A
surprisingly common misuse is to use a right quote in '`don't`'
instead of the correct apostrophe.

If you want to run `R CMD check` on a Unix-alike over a package that
sets a package encoding in its `DESCRIPTION` file _and do not
use a UTF-8 locale_ you may need to specify a suitable locale _via_
environment variable `R_ENCODING_LOCALES`. The default is equivalent to
the value

```r
"latin1=en_US:latin2=pl_PL:UTF-8=en_US.UTF-8:latin9=fr_FR.iso885915@euro"
```

(which is appropriate for a system based on `glibc`: macOS requires
`latin9=fr_FR.ISO8859-15`) except that if the current locale is UTF-8
then the package code is translated to UTF-8 for syntax checking, so it
is strongly recommended to check in a UTF-8 locale.

---

#### 1.6.4 Portable C and C++ code

---

• [Common symbols](#Common-symbols)

---

Writing portable C and C++ code is mainly a matter of observing the
standards (C99, C++11 or where declared C++98/14/17) and testing that
extensions (such as POSIX functions) are supported.

**C++ standards**: As from version 3.6.0 (3.6.2 on Windows), R defaults
to C++11 where available[^89^](#FOOT89). However, in earlier
versions the default standard was that of the compiler used, often C++98
or C++14. Thus for portability it is desirable to specify the C++
standard[^90^](#FOOT90) assumed for a package. Because most
packages will be made available for earlier versions on R, comments
below about C++98 have been retained.

Note that the 'TR1' C++ extensions are not part of any of these
standards and the `<tr1/name>` headers are not supplied by some of the
compilers used for R, including on macOS. (Use the C++11 versions
instead.)

Note too that the POSIX standards only require recently-defined
functions to be declared if certain macros are defined with large enough
values, and on some compiler/OS combinations[^91^](#FOOT91)
they are not declared otherwise. So you may need to include something
like one of [^92^](#FOOT92)

```r
#define _XOPEN_SOURCE 600
```

or

```r
#ifdef __GLIBC__
# define _POSIX_C_SOURCE 200809L
#endif
```

before _any_ headers. (`strdup` and `strncasecmp` are two such
functions.)

However, some common errors are worth pointing out here. It can be
helpful to look up functions at <http://www.cplusplus.com/reference/> or
<http://en.cppreference.com/w/> and compare what is defined in the
various standards.

Both the compiler and OS (_via_ system header files, which may differ by
architecture even for nominally the same OS) affect the compilability of
C/C++ code. Compilers from the GCC, `clang`, Intel and Oracle Developer
Studio suites are routinely used with R, and both `clang` and Oracle
have more than one implementation of C++ headers and library. The range
of possibilities makes comprehensive empirical checking impossible, and
regrettably compilers are patchy at best on warning about non-standard
code.

- Mathematical functions such as `sqrt` are defined in C++11 for
  floating-point arguments: `float`, `double`, `long double` and
  possibly more. The standard specifies what happens with an argument
  of integer type but this is not always implemented, resulting in a
  report of 'overloading ambiguity': this is commonly seen on Solaris,
  but for `pow` also seen on macOS.

  A not-uncommonly-seen problem is to mistakenly call `floor(x/y)` or
  `ceil(x/y)` for `int` arguments `x` and `y`. Since `x/y` does
  integer division, the result is of type `int` and 'overloading
  ambiguity' may be reported. Some people have (pointlessly) called
  `floor` and `ceil` on arguments of integer type, which may have an
  'overloading ambiguity'.

  A surprising common misuse is things like `pow(10, -3)`: this should
  be the constant `1e-3`. Note that there are constants such as
  `M_SQRT2` defined in `Rmath.h`[^93^](#FOOT93) for
  `sqrt(2.0)`, frequently mis-coded as `sqrt(2)`.

- Function `fabs` is defined only for floating-point types, except in
  C++11 which has overloads for `std::fabs` in `<cmath>` for
  integer types. Function `abs` is defined in C99's
  `<stdlib.h>` for `int` and in C++'s `<cstdlib>`
  for integer types, overloaded in `<cmath>` for
  floating-point types. C++11 has additional overloads for `std::abs`
  in `<cmath>` for integer types. The effect of calling `abs`
  with a floating-point type is implementation-specific: it may
  truncate to an integer. For clarity and to avoid compiler warnings,
  use `abs` for integer types and `fabs` for double values.

- It is an error (and make little sense, although has been seen) to
  call macros/functions `isnan`, `isinf` and `isfinite` for integer
  arguments: a few compilers give a compilation error. Function
  `finite` is obsolete, and some compilers will warn about its use.

- The GNU C/C++ compilers support a large number of non-portable
  extensions. For example, `INFINITY` (which is a _float_ value in C99
  and C++11 but not C++98), for which R provides the portable double
  value `R_PosInf` (and `R_NegInf` for `-INFINITY`). And
  `NAN`[^94^](#FOOT94) is just one NaN _float_ value: for use
  with R, `NA_REAL` is usually what is intended, but `R_NaN` is also
  available.

  Some (but not all) extensions are listed at
  <https://gcc.gnu.org/onlinedocs/gcc/C-Extensions.html> and
  <https://gcc.gnu.org/onlinedocs/gcc/C_002b_002b-Extensions.html>.

  Other GNU extensions which have bitten package writers is the use of
  non-portable characters such as '`$`' in identifiers and
  use of C++ headers under `ext`.

  The GNU Fortran compiler also supports a large number of
  non-portable extensions, the most commonly encountered one being
  `ISNAN`[^95^](#FOOT95). Some are listed at
  <https://gcc.gnu.org/onlinedocs/gfortran/Extensions-implemented-in-GNU-Fortran.html>.
  One that frequently catches package writers is that it allows
  out-of-order declarations: in standard-conformant Fortran variables
  must be declared (explicitly or implicitly) before use in other
  declarations such as dimensions.

- Including C-style headers in C++ code is not portable. Including the
  legacy header[^96^](#FOOT96) `math.h` in C++ code
  may conflict with `cmath` which may be included by other
  headers. This is particularly problematic with C++11 compilers, as
  functions like `sqrt` and `isnan` are defined for `double` arguments
  in `math.h` and for a range of types including `double` in
  `cmath`. Similar issues have been seen for
  `stdlib.h` and `cstdlib`. Including the C++
  version first used to be a sufficient workaround but for some 2016
  compilers only one could be included.

- Be careful to include the headers which define the functions you
  use. Some compilers/OSes include other system headers in their
  headers which are not required by the standards, and so code may
  compile on such systems and not on others. (A prominent example is
  the C++ header `<random>` which is indirectly included by
  `<algorithm>` by `g++`. Another issue is the C header `<time.h>`
  which is included by other headers on Linux and Windows but not
  macOS nor Solaris.)

  Note that `malloc`, `calloc`, `realloc` and `free` are defined by
  C99 in the header `stdlib.h` and (in the `std::` namespace)
  by C++ header `cstdlib`. Some earlier implementations used
  a header `malloc.h`, but that is not portable and does not
  exist on macOS.

  This also applies to types such as `ssize_t`. The POSIX standards
  say that is declared in headers `unistd.h` and `sys/types.h`, and
  the latter is often included indirectly by other headers on some but
  not all systems.

  Similarly for constants: for example `SIZE_MAX` is defined in
  `stdint.h` alongside `size_t`.

- For C++ code, be careful to specify namespaces where needed. Many
  functions are defined by the standards to be in the `std` namespace,
  but `g++` puts many such also in the C++ main namespace. One way to
  do so is to use declarations such as

```r
using std::floor;
```

but it is usually preferable to use explicit namespace prefixes in
the code.

Examples seen in CRAN packages include

```r
abs acos atan bind calloc ceil div exp fabs floor fmod free log malloc
memcpy memset pow printf qsort round sin sprintf sqrt strcmp strcpy
strerror strlen strncmp strtol tan trunc
```

This problem is less common than it used to be, but in 2019 `clang`
did not have `bind` in the main namespace.

- Some C++ compilers refuse to compile constructs such as

```r
      if(ptr > 0) { ....}
```

which compares a pointer to the integer `0`. This could just use
`if(ptr)` (pointer addresses cannot be negative) but if needed
pointers can be tested against `nullptr` (C++11) or `NULL`.

- Macros defined by the compiler/OS can cause problems. Identifiers
  starting with an underscore followed by an upper-case letter or
  another underscore are reserved for system macros and should not be
  used in portable code (including not as guards in C/C++ headers).
  Other macros, typically upper-case, may be defined by the compiler
  or system headers and can cause problems. The most common issue
  involves the names of the Intel CPU registers such as `CS`, `DS`,
  `ES`, `FS`, `GS` and `SS` (and more with longer
  abbreviations[^97^](#FOOT97)) defined on i586/x64 Solaris
  in `<sys/regset.h>` and often included indirectly by
  `<stdlib.h>` and other core headers. Further examples are
  `ERR`, `VERSION`, `LITTLE_ENDIAN`, `zero` and `I` (which is defined
  in Solaris' `<complex.h>` as a compiler intrinsic for the
  imaginary unit). Some of these can be avoided by defining
  `_POSIX_C_SOURCE` before including any system headers, but it is
  better to only use all-upper-case names which have a unique prefix
  such as the package name.

- `typedef`s in OS headers can conflict with those in the package:
  examples include `ulong` on several OSes and `index_t` and `single`
  on Solaris. (Note that these may conflict with other uses as
  identifiers, e.g. defining a C++ function called `single`.)

- If you use OpenMP, check carefully that you have followed the advice
  in the subsection on [OpenMP support](#OpenMP-support). In
  particular, any use of OpenMP in C/C++ code will need to use

```r
#ifdef _OPENMP
# include <omp.h>
#endif
```

Any use of OpenMP functions, e.g. `omp_set_num_threads`, also needs
to be conditioned.

And do not hardcode `-lgomp`: not only is that specific to
the GCC family of compilers, using the correct linker flag often
sets up the run-time path to the library.

- Package authors commonly assume things are part of C/C++ when they
  are not: the most common example is POSIX function `strdup`. The
  most common C library on Linux, `glibc`, will hide the declarations
  of such extensions unless a 'feature-test macro' is defined
  **before** (almost) any system header is included. So for `strdup`
  you need

```r
#define _POSIX_C_SOURCE 200809L
...
#include <string.h>
...
strdup call(s)
```

where the appropriate value can be found by `man strdup` on Linux.
(Use of `strncasecmp` is similar.)

However, modes of `gcc` with 'GNU EXTENSIONS' (which are the
default, either `-std=gnu99` or `-std=gnu11`)
declare enough macros to ensure that missing declarations are rarely
seen.

This applies also to constants such as `M_PI` and `M_LN2`, which are
part of the X/Open standard: to use these define `_XOPEN_SOURCE`
before including any headers, or include the R header
`Rmath.h`.

- Similarly, package authors commonly assume things are part of C++
  when they were introduced in C++11 if at all. Recent examples from
  CRAN packages include the C99/C++11 functions

```r
erf expm1 fmin fmax lgamma lround loglp round snprintf strcasecmp trunc
```

(all of which are in the `std` namespace in C++11) and the POSIX
functions `strdup` and `strncasecmp` and constants `M_PI` and
`M_LN2` (see the previous item). R has long provided `fmax2`,
`fmin2`, `fround`, `ftrunc`, `lgammafn` and many of the X/Open
constants, declared in header `Rmath.h`. Uses of `erf` can
be replaced by `pnorm` (see the R help page for the latter).

- Using `alloca` portably is tricky: it is neither an ISO C/C++ nor a
  POSIX function. An adequately portable preamble is

```r
#ifdef __GNUC__
/* Includes GCC, clang and Intel compilers */
# undef alloca
# define alloca(x) __builtin_alloca((x))
#elif defined(__sun) || defined(_AIX)
/* this is necessary (and sufficient) for Solaris 10 and AIX 6: */
# include <alloca.h>
#endif
```

- Compiler writers feel free to implement features from later
  standards than the one specified, so for example they may implement
  or warn on C++14 or C++17 features. Portable code will not use such
  features -- it can be hard to know what they are but the most common
  warnings are

```r
'register' storage class specifier is deprecated and incompatible with C++17

ISO C++11 does not allow conversion from string literal to ‘char *’
```

(where conversion should be to `const char *`). Keyword `register`
was not mentioned in C++98, deprecated in C++11 and removed in
C++17.

There are quite a lot of other C++98 features deprecated in C++11
and removed in C++17, and `clang` 9 and later warn about them.
Examples include `bind1st`/`bind2nd` (use `std::bind` or
lambdas[^98^](#FOOT98)) `std::auto_ptr` (replaced by
`std::unique_ptr`), `std:;mem_fun_ref` and `std::ptr_fun`.

- Be careful about including C headers in C++ code. Issues include

  - Use of the `register` storage class specifier (see the previous
    item).
  - The C99 keyword `restrict` is not part
    of[^99^](#FOOT99) any C++ standard and is rejected by
    some C++ compilers.
  - Inclusion by such headers of C-style headers such as
    `math.h` (see above).

  The most portable way to interface to other software with a C API is
  to use C code (which can normally be mixed with C++ code in a
  package).

- `reinterpret_cast` in C++ is not safe for pointers: for example the
  types may have different alignment requirements. Use `memcpy` to
  copy the contents to a fresh variable of the destination type.

- Avoid platform-specific code if at all possible, but if you need to
  test for a platform ensure that all platforms are covered. For
  example, `__unix__` is not defined on all Unix-alikes, in particular
  not on macOS. A reasonably portable way to condition code for a
  Unix-alike is

```r
#if defined (__unix__) || (defined (__APPLE__) && defined (__MACH__))
#endif
```

but

```r
#ifdef _WIN32
// Windows-specific code
#else
// Unix-alike code
#endif
```

would be better. For a Unix-alike it is much better to use
`configure` to test for the functionality needed than make
assumptions about OSes (and people all too frequently forget R is
used on platforms other than Linux, Windows and macOS --- and some
forget macOS).

Some additional information for C++ is available at
<http://journal.r-project.org/archive/2011-2/RJournal_2011-2_Plummer.pdf>
by Martyn Plummer.

---

#### 1.6.4.1 Common symbols

Most OSes (including all those commonly used for R) have the concept of
'tentative definitions' where global C variables are defined without an
initializer. Traditionally the linker resolves all tentative definitions
of the same variable in different object files to the same object, or to
a non-tentative definition. However, `gcc` 10 has changed its default so
that tentative definitions cannot be merged and the linker will give an
error if the same variable is defined in more than one object file. To
avoid this, all but one of the C source files should declare the
variable `extern` --- which means that any such variables included in
header files need to be declared `extern`. A commonly used idiom
(including by R itself) is to define all global variables as `extern` in
a header, say `globals.h` (and nowhere else), and then in one
(and one only) source file use

```r
#define extern
# include "globals.h"
#undef extern
```

A cleaner approach is not to have global variables at all, but to place
in a single file common variables (declared `static`) followed by all
the functions which make use of them: this may result in more efficient
code.

The 'modern' behaviour can be seen[^100^](#FOOT100) by using
compiler flag `-fno-common` as part of '`CFLAGS`' in
earlier versions of `gcc` and also in `clang`. It is recommended that
packages are if possible checked with that flag to ensure portability.

This is not pertinent to C++ which does not permit tentative
definitions.

---

#### 1.6.5 Binary distribution

If you want to distribute a binary version of a package on Windows or
macOS, there are further checks you need to do to check it is portable:
it is all too easy to depend on external software on your own machine
that other users will not have.

For Windows, check what other DLLs your package's DLL depends on
('imports' from in the DLL tools' parlance). A convenient GUI-based tool
to do so is 'Dependency Walker' (<http://www.dependencywalker.com/>) for
both 32-bit and 64-bit DLLs -- note that this will report as missing
links to R's own DLLs such as `R.dll` and `Rblas.dll`.
For 32-bit DLLs only, the command-line tool `pedump.exe -i` (in
`Rtools*.exe`) can be used, and for the brave, the `objdump`
tool in the appropriate toolchain will also reveal what DLLs are
imported from. If you use a toolchain other than one provided by the R
developers or use your own makefiles, watch out in particular for
dependencies on the toolchain's runtime DLLs such as
`libgfortran`, `libstdc++` and `libgcc_s`.

For macOS, using `R CMD otool -L` on the package's shared object(s) in
the `libs` directory will show what they depend on: watch for
any dependencies in `/usr/local/lib` or
`/usr/local/gfortran/lib`, notably
`libgfortran.?.dylib` and `libquadmath.0.dylib`.

Many people (including the CRAN package repository) will not accept
source packages containing binary files as the latter are a security
risk. If you want to distribute a source package which needs external
software on Windows or macOS, options include

- To arrange for installation of the package to download the
  additional software from a URL, as e.g. package
  [**Cairo**](https://CRAN.R-project.org/package=Cairo) does.
- (For CRAN.) To negotiate with Uwe Ligges to host the additional
  components on WinBuilder, and write a `configure.win` file
  to install them.

Be aware that license requirements will need to be met so you may need
to supply the sources for the additional components (and will if your
package has a GPL-like license).

---

### 1.7 Diagnostic messages

Diagnostic messages can be made available for translation, so it is
important to write them in a consistent style. Using the tools described
in the next section to extract all the messages can give a useful
overview of your consistency (or lack of it). Some guidelines follow.

- Messages are sentence fragments, and not viewed in isolation. So it
  is conventional not to capitalize the first word and not to end with
  a period (or other punctuation).

- Try not to split up messages into small pieces. In C error messages
  use a single format string containing all English words in the
  messages.

  In R error messages do not construct a message with `paste` (such
  messages will not be translated) but _via_ multiple arguments to
  `stop` or `warning`, or _via_ `gettextf`.

- Do not use colloquialisms such as "can't" and "don't".

- Conventionally single quotation marks are used for quotations such
  as

```r
'ord' must be a positive integer, at most the number of knots
```

and double quotation marks when referring to an R character string
or a class, such as

```r
'format' must be "normal" or "short" - using "normal"
```

Since ASCII does not contain directional quotation marks, it is best
to use '`'`' and let the translator (including automatic
translation) use directional quotations where available. The range
of quotation styles is immense: unfortunately we cannot reproduce
them in a portable `texinfo` document. But as a taster, some
languages use 'up' and 'down' (comma) quotes rather than left or
right quotes, and some use guillemets (and some use what Adobe calls
'guillemotleft' to start and others use it to end).

In R messages it is also possible to use `sQuote` or `dQuote` as in

```r
        stop(gettextf("object must be of class %s or %s",
                      dQuote("manova"), dQuote("maov")),
             domain = NA)
```

- Occasionally messages need to be singular or plural (and in other
  languages there may be no such concept or several plural forms --
  Slovenian has four). So avoid constructions such as was once used in
  `library`

```r
if((length(nopkgs) > 0) && !missing(lib.loc)) {
    if(length(nopkgs) > 1)
        warning("libraries ",
                paste(sQuote(nopkgs), collapse = ", "),
                " contain no packages")
    else
        warning("library ", paste(sQuote(nopkgs)),
                " contains no package")
}
```

and was replaced by

```r
if((length(nopkgs) > 0) && !missing(lib.loc)) {
    pkglist <- paste(sQuote(nopkgs), collapse = ", ")
    msg <- sprintf(ngettext(length(nopkgs),
                            "library %s contains no packages",
                            "libraries %s contain no packages",
                            domain = "R-base"),
                   pkglist)
    warning(msg, domain=NA)
}
```

Note that it is much better to have complete clauses as here, since
in another language one might need to say 'There is no package in
library %s' or 'There are no packages in libraries %s'.

---

### 1.8 Internationalization

There are mechanisms to translate the R- and C-level error and warning
messages. There are only available if R is compiled with NLS support
(which is requested by `configure` option `--enable-nls`, the
default).

The procedures make use of `msgfmt` and `xgettext` which are part of GNU
`gettext` and this will need to be installed: Windows users can find
pre-compiled binaries at
<https://www.stats.ox.ac.uk/pub/Rtools/goodies/gettext-tools.zip>.

---

• [C-level messages](#C_002dlevel-messages)     
 • [R messages](#R-messages)     
 • [Preparing translations](#Preparing-translations)

---

---

#### 1.8.1 C-level messages

The process of enabling translations is

- In a header file that will be included in all the C (or C++ or
  Objective C/C++) files containing messages that should be
  translated, declare

```r
#include <R.h>  /* to include Rconfig.h */

#ifdef ENABLE_NLS
#include <libintl.h>
#define _(String) dgettext ("pkg", String)
/* replace pkg as appropriate */
#else
#define _(String) (String)
#endif
```

- For each message that should be translated, wrap it in `_(...)`, for
  example

```r
error(_("'ord' must be a positive integer"));
```

If you want to use different messages for singular and plural forms,
you need to add

```r
#ifndef ENABLE_NLS
#define dngettext(pkg, String, StringP, N) (N > 1 ? StringP : String)
#endif
```

and mark strings by

```r
dngettext("pkg", <singular string>, <plural string>, n)
```

- In the package's `src` directory run

  ```r
  xgettext --keyword=_ -o pkg.pot *.c
  ```

The file `src/pkg.pot` is the template file, and conventionally
this is shipped as `po/pkg.pot`.

---

#### 1.8.2 R messages

Mechanisms are also available to support the automatic translation of R
`stop`, `warning` and `message` messages. They make use of message
catalogs in the same way as C-level messages, but using domain `R-pkg`
rather than `pkg`. Translation of character strings inside `stop`,
`warning` and `message` calls is automatically enabled, as well as other
messages enclosed in calls to `gettext` or `gettextf`. (To suppress
this, use argument `domain=NA`.)

Tools to prepare the `R-pkg.pot` file are provided in package
**tools**: `xgettext2pot` will prepare a file from all strings occurring
inside `gettext`/`gettextf`, `stop`, `warning` and `message` calls. Some
of these are likely to be spurious and so the file is likely to need
manual editing. `xgettext` extracts the actual calls and so is more
useful when tidying up error messages.

The R function `ngettext` provides an interface to the C function of the
same name: see example in the previous section. It is safest to use
`domain="R-pkg"` explicitly in calls to `ngettext`, and necessary for
earlier versions of R unless they are calls directly from a function in
the package.

---

#### 1.8.3 Preparing translations

Once the template files have been created, translations can be made.
Conventional translations have file extension `.po` and are
placed in the `po` subdirectory of the package with a name that
is either '`ll.po`' or '`R-ll.po`' for translations of
the C and R messages respectively to language with code '`ll`'.

See [Localization of messages](./R-admin.html#Localization-of-messages)
in R Installation and Administration, for details of language codes.

There is an R function, `update_pkg_po` in package **tools**, to
automate much of the maintenance of message translations. See its help
for what it does in detail.

If this is called on a package with no existing translations, it creates
the directory `pkgdir/po`, creates a template file of R
messages, `pkgdir/po/R-pkg.pot`, within it, creates the
'`en@quot`' translation and installs that. (The
'`en@quot`' pseudo-language interprets quotes in their
directional forms in suitable (e.g. UTF-8) locales.)

If the package has C source files in its `src` directory that
are marked for translation, use

```r
touch pkgdir/po/pkg.pot
```

to create a dummy template file, then call `update_pkg_po` again (this
can also be done before it is called for the first time).

When translations to new languages are added in the `pkgdir/po`
directory, running the same command will check and then install the
translations.

If the package sources are updated, the same command will update the
template files, merge the changes into the translation `.po`
files and then installed the updated translations. You will often see
that merging marks translations as 'fuzzy' and this is reported in the
coverage statistics. As fuzzy translations are _not_ used, this is an
indication that the translation files need human attention.

The merged translations are run through `tools::checkPofile` to check
that C-style formats are used correctly: if not the mismatches are
reported and the broken translations are not installed.

This function needs the GNU `gettext-tools` installed and on the path:
see its help page.

---

### 1.9 CITATION files

An installed file named `CITATION` will be used by the
`citation()` function. (It should be in the `inst` subdirectory
of the package sources.)

The `CITATION` file is parsed as R code (in the package's
declared encoding, or in ASCII if none is declared). If no such file is
present, `citation` auto-generates citation information from the package
`DESCRIPTION` metadata, and an example of what that would look
like as a `CITATION` file can be seen in recommended package
[**nlme**](https://CRAN.R-project.org/package=nlme) (see below):
recommended packages
[**boot**](https://CRAN.R-project.org/package=boot),
[**cluster**](https://CRAN.R-project.org/package=cluster) and
[**mgcv**](https://CRAN.R-project.org/package=mgcv) have further
examples.

A `CITATION` file will contain calls to function `bibentry`.

Here is that for [**nlme**](https://CRAN.R-project.org/package=nlme):

```r
year <- sub("-.*", "", meta$Date)
note <- sprintf("R package version %s", meta$Version)

bibentry(bibtype = "Manual",
         title = "{nlme}: Linear and Nonlinear Mixed Effects Models",
         author = c(person("Jose", "Pinheiro"),
                    person("Douglas", "Bates"),
                    person("Saikat", "DebRoy"),
                    person("Deepayan", "Sarkar"),
                    person("R Core Team")),
         year = year,
         note = note,
         url = "https://CRAN.R-project.org/package=nlme")
```

Note the way that information that may need to be updated is picked up
from object `meta`, a parsed version of the `DESCRIPTION` file
-- it is tempting to hardcode such information, but it normally then
gets outdated. See `?bibentry` for further details of the information
which can be provided.

In case a bibentry contains LaTeX markup (e.g., for accented characters
or mathematical symbols), it may be necessary to provide a text
representation to be used for printing _via_ the `textVersion` argument
to `bibentry`. E.g., earlier versions of
[**nlme**](https://CRAN.R-project.org/package=nlme) additionally used

```r
         textVersion =
         paste0("Jose Pinheiro, Douglas Bates, Saikat DebRoy,",
                "Deepayan Sarkar and the R Core Team (",
                year,
                "). nlme: Linear and Nonlinear Mixed Effects Models. ",
                note, ".")
```

The `CITATION` file should itself produce no output when
`source`-d.

It is desirable (and essential for CRAN) that the `CITATION`
file does not contain calls to functions such as `packageDescription`
which assume the package is installed in a library tree on the package
search path.

---

### 1.10 Package types

The `DESCRIPTION` file has an optional field `Type` which if
missing is assumed to be '`Package`', the sort of extension
discussed so far in this chapter. Currently one other type is
recognized; there used also to be a '`Translation`' type.

---

• [Frontend](#Frontend)

---

---

#### 1.10.1 Frontend

This is a rather general mechanism, designed for adding new front-ends
such as the former **gnomeGUI** package (see the `Archive` area
on CRAN). If a `configure` file is found in the top-level
directory of the package it is executed, and then if a
`Makefile` is found (often generated by `configure`),
`make` is called. If `R CMD INSTALL --clean` is used `make clean` is
called. No other action is taken.

`R CMD build` can package up this type of extension, but `R CMD check`
will check the type and skip it.

Many packages of this type need write permission for the R installation
directory.

---

### 1.11 Services

Several members of the R project have set up services to assist those
writing R packages, particularly those intended for public distribution.

[win-builder.r-project.org](https://win-builder.r-project.org) offers
the automated preparation of (32/64-bit) Windows binaries from
well-tested source packages.

R-Forge ([R-Forge.r-project.org](https://R-Forge.r-project.org)) and
RForge ([www.rforge.net](https://www.rforge.net)) are similar services
with similar names. Both provide source-code management through SVN,
daily building and checking, mailing lists and a repository that can be
accessed _via_ `install.packages` (they can be selected by
`setRepositories` and the GUI menus that use it). Package developers
have the opportunity to present their work on the basis of project
websites or news announcements. Mailing lists, forums or wikis provide
useRs with convenient instruments for discussions and for exchanging
information between developers and/or interested useRs.

---
