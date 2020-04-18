# 1 Obtaining R

---

Sources, binaries and documentation for R can be obtained via CRAN, the
"Comprehensive R Archive Network" whose current members are listed at
<https://CRAN.R-project.org/mirrors.html>.

---

• [Getting and unpacking the sources](#Getting-and-unpacking-the-sources)     
 • [Getting patched and development versions](#Getting-patched-and-development-versions)

---

---

### 1.1 Getting and unpacking the sources

The simplest way is to download the most recent
`R-x.y.z.tar.gz` file, and unpack it with

```r
tar -xf R-x.y.z.tar.gz
```

on systems that have a suitable[^1^](#FOOT1) `tar` installed. On
other systems you need to have the `gzip` program installed, when you
can use

```r
gzip -dc R-x.y.z.tar.gz | tar -xf -
```

The pathname of the directory into which the sources are unpacked should
not contain spaces, as most `make` programs (and specifically GNU
`make`) do not expect spaces.

If you want the build to be usable by a group of users, set `umask`
before unpacking so that the files will be readable by the target group
(e.g., `umask 022` to be usable by all users). Keep this setting of
`umask` whilst building and installing.

If you use a fairly recent GNU version of `tar` and do this as a root
account (which on Windows includes accounts with administrator
privileges) you may see many warnings about changing ownership. In which
case you can use

```r
tar --no-same-owner -xf R-x.y.z.tar.gz
```

and perhaps also include the option `--no-same-permissions`.
(These options can also be set in the
`TAR_OPTIONS` environment variable: if more than one option is included
they should be separated by spaces.)

---

### 1.2 Getting patched and development versions

A patched version of the current release, '`r-patched`', and
the current development version, '`r-devel`', are available as
daily tarballs and via access to the R Subversion repository. (For the
two weeks prior to the release of a minor (3.x.0) version,
'`r-patched`' tarballs may refer to beta/release candidates of
the upcoming release, the patched version of the current release being
available via Subversion.)

The tarballs are available from <https://stat.ethz.ch/R/daily>. Download
`R-patched.tar.gz` or `R-devel.tar.gz` (or the
`.tar.bz2` versions) and unpack as described in the previous
section. They are built in exactly the same way as distributions of R
releases.

---

• [Using Subversion and rsync](#Using-Subversion-and-rsync)

---

---

#### 1.2.1 Using Subversion and rsync

Sources are also available via <https://svn.R-project.org/R/>, the R
Subversion repository. If you have a Subversion client (see
<https://subversion.apache.org/>), you can check out and update the
current '`r-devel`' from <https://svn.r-project.org/R/trunk/>
and the current '`r-patched`' from
'`https://svn.r-project.org/R/branches/R-x-y-branch/`' (where
`x` and `y` are the major and minor number of the
current released version of R). E.g., use

```r
svn checkout https://svn.r-project.org/R/trunk/ path
```

to check out '`r-devel`' into directory `path`
(which will be created if necessary). The alpha, beta and RC versions of
an upcoming `x.y.0` release are available from
'`https://svn.r-project.org/R/branches/R-x-y-branch/`' in the
four-week period prior to the release.

Note that '`https:`' is required[^2^](#FOOT2), and that
the SSL certificate for the Subversion server of the R project should be
recognized as from a trusted source.

Note that retrieving the sources by e.g. `wget -r` or `svn export` from
that URL will not work (and will give a error early in the `make`
process): the Subversion information is needed to build R.

The Subversion repository does not contain the current sources for the
recommended packages, which can be obtained by `rsync` or downloaded
from CRAN. To use `rsync` to install the appropriate sources for the
recommended packages, run `./tools/rsync-recommended` from the top-level
directory of the R sources.

If downloading manually from CRAN, do ensure that you have the correct
versions of the recommended packages: if the number in the file
`VERSION` is '`x.y.z`' you need to download the
contents of '`https://CRAN.R-project.org/src/contrib/dir`',
where `dir` is '`x.y.z/Recommended`' for r-devel or
`x.y-patched/Recommended` for r-patched, respectively, to
directory `src/library/Recommended` in the sources you have
unpacked. After downloading manually you need to execute
`tools/link-recommended` from the top level of the sources to make the
requisite links in `src/library/Recommended`. A suitable
incantation from the top level of the R sources using `wget` might be
(for the correct value of `dir`)

```r
wget -r -l1 --no-parent -A\*.gz -nd -P src/library/Recommended \
  https://CRAN.R-project.org/src/contrib/dir
./tools/link-recommended
```

---
