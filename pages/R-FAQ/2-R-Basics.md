# 2 R Basics

---

---

• [What is R?](#What-is-R_003f)     
 • [What machines does R run on?](#What-machines-does-R-run-on_003f)     
 • [What is the current version of R?](#What-is-the-current-version-of-R_003f)     
 • [How can R be obtained?](#How-can-R-be-obtained_003f)     
 • [How can R be installed?](#How-can-R-be-installed_003f)     
 • [Are there Unix-like binaries for R?](#Are-there-Unix_002dlike-binaries-for-R_003f)     
 • [What documentation exists for R?](#What-documentation-exists-for-R_003f)     
 • [Citing R](#Citing-R)     
 • [What mailing lists exist for R?](#What-mailing-lists-exist-for-R_003f)     
 • [What is CRAN?](#What-is-CRAN_003f)     
 • [Can I use R for commercial purposes?](#Can-I-use-R-for-commercial-purposes_003f)     
 • [Why is R named R?](#Why-is-R-named-R_003f)     
 • [What is the R Foundation?](#What-is-the-R-Foundation_003f)     
 • [What is R-Forge?](#What-is-R_002dForge_003f)

---

---

### 2.1 What is R?

R is a system for statistical computation and graphics. It consists of a
language plus a run-time environment with graphics, a debugger, access
to certain system functions, and the ability to run programs stored in
script files.

The design of R has been heavily influenced by two existing languages:
Becker, Chambers & Wilks' S (see [What is S?](#What-is-S_003f)) and
Sussman's
[Scheme](https://www.cs.indiana.edu/scheme-repository/home.html).
Whereas the resulting language is very similar in appearance to S, the
underlying implementation and semantics are derived from Scheme. See
[What are the differences between R and
S?](#What-are-the-differences-between-R-and-S_003f), for further
details.

The core of R is an interpreted computer language which allows branching
and looping as well as modular programming using functions. Most of the
user-visible functions in R are written in R. It is possible for the
user to interface to procedures written in the C, C++, or FORTRAN
languages for efficiency. The R distribution contains functionality for
a large number of statistical procedures. Among these are: linear and
generalized linear models, nonlinear regression models, time series
analysis, classical parametric and nonparametric tests, clustering and
smoothing. There is also a large set of functions which provide a
flexible graphical environment for creating various kinds of data
presentations. Additional modules ("add-on packages") are available for
a variety of specific purposes (see [R Add-On Packages](#R-Add_002dOn-Packages)).

R was initially written by [Ross Ihaka](mailto:Ross.Ihaka@R-project.org)
and [Robert Gentleman](mailto:Robert.Gentleman@R-project.org) at the
Department of Statistics of the University of Auckland in Auckland, New
Zealand. In addition, a large group of individuals has contributed to R
by sending code and bug reports.

Since mid-1997 there has been a core group (the "R Core Team") who can
modify the R source code archive. The group currently consists of Doug
Bates, John Chambers, Peter Dalgaard, Robert Gentleman, Kurt Hornik,
Ross Ihaka, Tomas Kalibera, Michael Lawrence, Friedrich Leisch, Uwe
Ligges, Thomas Lumley, Martin Maechler, Martin Morgan, Paul Murrell,
Martyn Plummer, Brian Ripley, Deepayan Sarkar, Duncan Temple Lang, Luke
Tierney, and Simon Urbanek.

R has a home page at <https://www.R-project.org/>. It is [free software](https://www.gnu.org/philosophy/free-sw.html) distributed under
a GNU-style [copyleft](https://www.gnu.org/copyleft/copyleft.html), and
an official part of the [GNU](https://www.gnu.org/) project ("GNU S").

---

### 2.2 What machines does R run on?

R is being developed for the Unix-like, Windows and Mac families of
operating systems. Support for Mac OS Classic ended with R 1.7.1.

The current version of R will configure and build under a number of
common Unix-like (e.g., <https://en.wikipedia.org/wiki/Unix-like>)
platforms including `cpu`-linux-gnu for the i386,
amd64/x86_64, alpha, arm, arm64, hppa, mips/mipsel, powerpc, s390x and
sparc CPUs (e.g., <https://buildd.debian.org/build.php?&pkg=r-base>),
i386-hurd-gnu, `cpu`-kfreebsd-gnu for i386 and amd64,
i386-pc-solaris, rs6000-ibm-aix, sparc-sun-solaris,
x86_64-apple-darwin, x86_64-unknown-freebsd and
x86_64-unknown-openbsd.

If you know about other platforms, please drop us a note.

---

### 2.3 What is the current version of R?

R uses a 'major.minor.patchlevel' numbering scheme. Based on this, there
are the current release version of R ('r-release') as well as two
development versions of R, a patched version of the current release
('r-patched') and one working towards the next minor or eventually major
('r-devel') releases of R, respectively. New features are typically
introduced in r-devel, while r-patched is for bug fixes mostly.

See <https://CRAN.R-project.org/sources.html> for the current versions
of r-release, r-patched and r-devel.

---

### 2.4 How can R be obtained?

Sources, binaries and documentation for R can be obtained via CRAN, the
"Comprehensive R Archive Network" (see [What is
CRAN?](#What-is-CRAN_003f)).

Sources are also available via <https://svn.R-project.org/R/>, the R
Subversion repository, but currently not via anonymous rsync (nor CVS).

Tarballs with daily snapshots of the r-devel and r-patched development
versions of R can be found at <https://stat.ethz.ch/R/daily>.

---

### 2.5 How can R be installed?

---

• [How can R be installed (Unix-like)](#How-can-R-be-installed-_0028Unix_002dlike_0029)     
 • [How can R be installed (Windows)](#How-can-R-be-installed-_0028Windows_0029)     
 • [How can R be installed (Mac)](#How-can-R-be-installed-_0028Mac_0029)

---

---

#### 2.5.1 How can R be installed (Unix-like)

If R is already installed, it can be started by typing [R] at the
shell prompt (of course, provided that the executable is in your path).

If binaries are available for your platform (see [Are there Unix-like
binaries for R?](#Are-there-Unix_002dlike-binaries-for-R_003f)), you can
use these, following the instructions that come with them.

Otherwise, you can compile and install R yourself, which can be done
very easily under a number of common Unix-like platforms (see [What
machines does R run on?](#What-machines-does-R-run-on_003f)). The file
`INSTALL` that comes with the R distribution contains a brief
introduction, and the "R Installation and Administration" guide (see
[What documentation exists for
R?](#What-documentation-exists-for-R_003f)) has full details.

Note that you need a FORTRAN compiler or perhaps `f2c` in addition to a
C compiler to build R.

In the simplest case, untar the R source code, change to the directory
thus created, and issue the following commands (at the shell prompt):

```r
$ ./configure
$ make
```

If these commands execute successfully, the R binary and a shell script
front-end called `R` are created and copied to the
`bin` directory. You can copy the script to a place where users
can invoke it, for example to `/usr/local/bin`. In addition,
plain text help pages as well as HTML and LaTeX versions of the
documentation are built.

Use [make dvi] to create DVI versions of the R manuals, such as
`refman.dvi` (an R object reference index) and
`R-exts.dvi`, the "R Extension Writers Guide", in the
`doc/manual` subdirectory. These files can be previewed and
printed using standard programs such as `xdvi` and `dvips`. You can also
use [make pdf] to build PDF (Portable Document Format) version of
the manuals, and view these using e.g. Acrobat. Manuals written in the
GNU Texinfo system can also be converted to info files suitable for
reading online with Emacs or stand-alone GNU Info; use [make info]
to create these versions (note that this requires Makeinfo version 4.5).

Finally, use [make check] to find out whether your R system works
correctly.

You can also perform a "system-wide" installation using [make
install]. By default, this will install to the following
directories:

`${prefix}/bin`

: the front-end shell script

`${prefix}/man/man1`

: the man page

`${prefix}/lib/R`

: all the rest (libraries, on-line help system, ...). This is the "R
Home Directory" (`R_HOME`) of the installed system.

In the above, `prefix` is determined during configuration (typically
`/usr/local`) and can be set by running `configure` with the
option

```r
$ ./configure --prefix=/where/you/want/R/to/go
```

(E.g., the R executable will then be installed into
`/where/you/want/R/to/go/bin`.)

To install DVI, info and PDF versions of the manuals, use [make
install-dvi], [make install-info] and [make
install-pdf], respectively.

---

#### 2.5.2 How can R be installed (Windows)

The `bin/windows` directory of a CRAN site contains binaries
for a base distribution and add-on packages from CRAN to run on Windows
7 and later (including 64-bit versions of Windows) on ix86 and x86_64
chips. The Windows version of R was created by Robert Gentleman and
Guido Masarotto, Brian D. Ripley and Duncan Murdoch made substantial
contributions and it is now being maintained by other members of the R
Core team.

The same directory has links to snapshots of the r-patched and r-devel
versions of R.

See the ["R for Windows
FAQ"](https://CRAN.R-project.org/bin/windows/base/rw-FAQ.html) for more
details.

---

#### 2.5.3 How can R be installed (Mac)

The `bin/macosx` directory of a CRAN site contains a standard
Apple installer package to run on macOS 10.9 ('Mavericks') and later.
Once downloaded and executed, the installer will install the current
release of R and R.app, the macOS GUI. This port of R for macOS is
maintained by [Simon Urbanek](mailto:Simon.Urbanek@R-project.org) (and

### 2.6 Are there Unix-like binaries for R?

The `bin/linux` directory of a CRAN site contains the following
packages.

>            CPU          Versions               Provider
>
> ---
>
> Debian i386/amd64 squeeze/wheezy Johannes Ranke
> armel wheezy Johannes Ranke
> Ubuntu i386/amd64 lucid/precise/trusty Michael Rutter

Debian packages, maintained by Dirk Eddelbuettel, have long been part of
the Debian distribution, and can be accessed through APT, the Debian
package maintenance tool. Use e.g.
`apt-get install r-base r-recommended` to install the R environment and
recommended packages. If you also want to build R packages from source,
also run `apt-get install r-base-dev` to obtain the additional tools
required for this. So-called "backports" of the current R packages for
at least the _stable_ distribution of Debian are provided by Johannes
Ranke, and available from CRAN. See
<https://CRAN.R-project.org/bin/linux/debian/index.html> for details on
R Debian packages and installing the backports, which should also be
suitable for other Debian derivatives. Native backports for Ubuntu are
provided by Michael Rutter.

R binaries for Fedora, maintained by Tom "Spot" Callaway, are provided
as part of the Fedora distribution and can be accessed through `yum`,
the RPM installer/updater. Note that the "Software" application
(gnome-software), which is the default GUI for software installation in
Fedora 20, cannot be used to install R. It is therefore recommended to
use the yum command line tool. The Fedora R RPM is a "meta-package"
which installs all the user and developer components of R (available
separately as `R-core` and `R-devel`), as well as `R-java`, which
ensures that R is configured for use with Java. The R RPM also installs
the standalone R math library (`libRmath` and `libRmath-devel`),
although this is not necessary to use R. When a new version of R is
released, there may be a delay of up to 2 weeks until the Fedora RPM
becomes publicly available, as it must pass through the statutory Fedora
review process. RPMs for a selection of R packages are also provided by
Fedora. The Extra Packages for Enterprise Linux (EPEL) project
(<https://fedoraproject.org/wiki/EPEL>) provides ports of the Fedora
RPMs for RedHat Enterprise Linux and compatible distributions (e.g.,
Centos, Scientific Linux, Oracle Linux).

See <https://CRAN.R-project.org/bin/linux/suse/README.html> for
information about RPMs for openSUSE.

No other binary distributions are currently publically available via
CRAN.

---

### 2.7 What documentation exists for R?

Online documentation for most of the functions and variables in R
exists, and can be printed on-screen by typing
[help(`name`)] (or [?`name`]) at the R
prompt, where `name` is the name of the topic help is sought
for. (In the case of unary and binary operators and control-flow special
forms, the name may need to be be quoted.)

This documentation can also be made available as one reference manual
for on-line reading in HTML and PDF formats, and as hardcopy via LaTeX,
see [How can R be installed?](#How-can-R-be-installed_003f). An
up-to-date HTML version is always available for web browsing at
<https://stat.ethz.ch/R-manual/>.

Printed copies of the R reference manual for some version(s) are
available from Network Theory Ltd, at
<http://www.network-theory.co.uk/R/base/>. For each set of manuals sold,
the publisher donates USD 10 to the R Foundation (see [What is the R
Foundation?](#What-is-the-R-Foundation_003f)).

The R distribution also comes with the following manuals.

- "An Introduction to R" (`R-intro`) includes information on
  data types, programming elements, statistical modeling and graphics.
  This document is based on the "Notes on [S-PLUS]" by Bill
  Venables and David Smith.
- "Writing R Extensions" (`R-exts`) currently describes the
  process of creating R add-on packages, writing R documentation, R's
  system and foreign language interfaces, and the R API.
- "R Data Import/Export" (`R-data`) is a guide to importing
  and exporting data to and from R.
- "The R Language Definition" (`R-lang`), a first version of
  the "Kernighan & Ritchie of R", explains evaluation, parsing, object
  oriented programming, computing on the language, and so forth.
- "R Installation and Administration" (`R-admin`).
- "R Internals" (`R-ints`) is a guide to R's internal
  structures. (Added in R 2.4.0.)

An annotated bibliography (BibTeX format) of R-related publications can
be found at

```
https://www.R-project.org/doc/bib/R.bib
```

Books on R by R Core Team members include

> John M. Chambers (2008), "Software for Data Analysis: Programming with
> R". Springer, New York, ISBN 978-0-387-75935-7,
> <http://statweb.stanford.edu/~jmc4/Rbook/>.
>
> Peter Dalgaard (2008), "Introductory Statistics with R", 2nd edition.
> Springer, ISBN 978-0-387-79053-4,
> <http://publicifsv.sund.ku.dk/~pd/ISwR.html>.
>
> Robert Gentleman (2008), "R Programming for Bioinformatics". Chapman &
> Hall/CRC, Boca Raton, FL, ISBN 978-1-420-06367-7,
> <https://www.bioconductor.org/pub/RBioinf/>.
>
> Stefano M. Iacus (2008), "Simulation and Inference for Stochastic
> Differential Equations: With R Examples". Springer, New York, ISBN
> 978-0-387-75838-1.
>
> Deepayan Sarkar (2007), "Lattice: Multivariate Data Visualization with
> R". Springer, New York, ISBN 978-0-387-75968-5.
>
> W. John Braun and Duncan J. Murdoch (2007), "A First Course in
> Statistical Programming with R". Cambridge University Press,
> Cambridge, ISBN 978-0521872652.
>
> P. Murrell (2005), "R Graphics", Chapman & Hall/CRC, ISBN:
> 1-584-88486-X,
> <https://www.stat.auckland.ac.nz/~paul/RGraphics/rgraphics.html>.
>
> William N. Venables and Brian D. Ripley (2002), "Modern Applied
> Statistics with S" (4th edition). Springer, ISBN 0-387-95457-0,
> <https://www.stats.ox.ac.uk/pub/MASS4/>.
>
> Jose C. Pinheiro and Douglas M. Bates (2000), "Mixed-Effects Models in
> S and S-Plus". Springer, ISBN 0-387-98957-0.

Last, but not least, Ross' and Robert's experience in designing and
implementing R is described in Ihaka & Gentleman (1996), "R: A Language
for Data Analysis and Graphics", [_Journal of Computational and
Graphical Statistics_](http://www.amstat.org/publications/jcgs/), **5**,
299--314.

---

### 2.8 Citing R

To cite R in publications, use

```r
@Manual{,
  title        = {R: A Language and Environment for Statistical
                  Computing},
  author       = {{R Core Team}},
  organization = {R Foundation for Statistical Computing},
  address      = {Vienna, Austria},
  year         = YEAR,
  url          = {https://www.R-project.org}
}
```

where `YEAR` is the release year of the version of R used and
can determined as `R.version$year`.

Citation strings (or BibTeX entries) for R and R packages can also be
obtained by `citation()`.

---

### 2.9 What mailing lists exist for R?

Thanks to [Martin Maechler](mailto:Martin.Maechler@R-project.org), there
are several mailing lists devoted to R, including the following:

`R-announce`

: A moderated list for major announcements about the development of R
and the availability of new code.

`R-packages`

: A moderated list for announcements on the availability of new or
enhanced contributed packages.

`R-help`

: The 'main' R mailing list, for discussion about problems and
solutions using R, announcements (not covered by 'R-announce' and
'R-packages') about the development of R and the availability of new
code.

`R-devel`

: This list is for questions and discussion about code development
in R.

`R-package-devel`

: A list which provides a forum for learning about the R package
development process.

Please read the [posting guide](https://www.R-project.org/posting-guide.html) _before_ sending
anything to any mailing list.

Note in particular that R-help is intended to be comprehensible to
people who want to use R to solve problems but who are not necessarily
interested in or knowledgeable about programming. Questions likely to
prompt discussion unintelligible to non-programmers (e.g., questions
involving C or C++) should go to R-devel.

Convenient access to information on these lists, subscription, and
archives is provided by the web interface at
<https://stat.ethz.ch/mailman/listinfo/>. One can also subscribe (or
unsubscribe) via email, e.g. to R-help by sending '`subscribe`'
(or '`unsubscribe`') in the _body_ of the message (not in the
subject!) to <R-help-request@lists.R-project.org>.

Send email to <R-help@lists.R-project.org> to send a message to everyone
on the R-help mailing list. Subscription and posting to the other lists
is done analogously, with '`R-help`' replaced by
'`R-announce`', '`R-packages`', and
'`R-devel`', respectively. Note that the R-announce and
R-packages lists are gatewayed into R-help. Hence, you should subscribe
to either of them only in case you are not subscribed to R-help.

It is recommended that you send mail to R-help rather than only to the R
Core developers (who are also subscribed to the list, of course). This
may save them precious time they can use for constantly improving R, and
will typically also result in much quicker feedback for yourself.

Of course, in the case of bug reports it would be very helpful to have
code which reliably reproduces the problem. Also, make sure that you
include information on the system and version of R being used. See [R Bugs](#R-Bugs) for more details.

See <https://www.R-project.org/mail.html> for more information on the R
mailing lists.

The R Core Team can be reached at <R-core@lists.R-project.org> for
comments and reports.

---

### 2.10 What is CRAN?

The "Comprehensive R Archive Network" (CRAN) is a collection of sites
which carry identical material, consisting of the R distribution(s), the
contributed extensions, documentation for R, and binaries.

The CRAN master site at WU (Wirtschaftsuniversität Wien) in Austria can
be found at the URL

> <https://CRAN.R-project.org/>

and is mirrored daily to many sites around the world. See
<https://CRAN.R-project.org/mirrors.html> for a complete list of
mirrors. Please use the CRAN site closest to you to reduce network load.

From CRAN, you can obtain the latest official release of R, daily
snapshots of R (copies of the current source trees), as gzipped and
bzipped tar files, a wealth of additional contributed code, as well as
prebuilt binaries for various operating systems (Linux, Mac OS Classic,
macOS, and MS Windows). CRAN also provides access to documentation on R,
existing mailing lists and the R Bug Tracking system.

Since March 2016, "old" material is made available from a central CRAN
archive server (<https://CRAN-archive.R-project.org/>).

Please always use the URL of the master site when referring to CRAN.

---

### 2.11 Can I use R for commercial purposes?

R is released under the [GNU General Public License (GPL), version
2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html). If you have
any questions regarding the legality of using R in any particular
situation you should bring it up with your legal counsel. We are in no
position to offer legal advice.

It is the opinion of the R Core Team that one can use R for commercial
purposes (e.g., in business or in consulting). The GPL, like all Open
Source licenses, permits all and any use of the package. It only
restricts distribution of R or of other programs containing code from R.
This is made clear in clause 6 ("No Discrimination Against Fields of
Endeavor") of the [Open Source Definition](https://opensource.org/docs/definition.html):

> The license must not restrict anyone from making use of the program in
> a specific field of endeavor. For example, it may not restrict the
> program from being used in a business, or from being used for genetic
> research.

It is also explicitly stated in clause 0 of the GPL, which says in part

> Activities other than copying, distribution and modification are not
> covered by this License; they are outside its scope. The act of
> running the Program is not restricted, and the output from the Program
> is covered only if its contents constitute a work based on the
> Program.

Most add-on packages, including all recommended ones, also explicitly
allow commercial use in this way. A few packages are restricted to
"non-commercial use"; you should contact the author to clarify whether
these may be used or seek the advice of your legal counsel.

None of the discussion in this section constitutes legal advice. The R
Core Team does not provide legal advice under any circumstances.

---

### 2.12 Why is R named R?

The name is partly based on the (first) names of the first two R authors
(Robert Gentleman and Ross Ihaka), and partly a play on the name of the
Bell Labs language 'S' (see [What is S?](#What-is-S_003f)).

---

### 2.13 What is the R Foundation?

The R Foundation is a not for profit organization working in the public
interest. It was founded by the members of the R Core Team in order to
provide support for the R project and other innovations in statistical
computing, provide a reference point for individuals, institutions or
commercial enterprises that want to support or interact with the R
development community, and to hold and administer the copyright of R
software and documentation. See <https://www.R-project.org/foundation/>
for more information.

---

### 2.14 What is R-Forge?

R-Forge (<https://R-Forge.R-project.org/>) offers a central platform for
the development of R packages, R-related software and further projects.
It is based on [GForge](https://en.wikipedia.org/wiki/GForge) offering
easy access to the best in SVN, daily built and checked packages,
mailing lists, bug tracking, message boards/forums, site hosting,
permanent file archival, full backups, and total web-based
administration. For more information, see the R-Forge web page and
Stefan Theußl and Achim Zeileis (2009), "Collaborative software
development using R-Forge", [_The R
Journal_](https://journal.R-project.org/), **1**(1):9--14.

---
