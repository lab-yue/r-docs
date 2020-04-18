# 11 Use of TeX dialects

---

Various dialects of TeX are used for different purposes in R. The policy
is that manuals be written in '`texinfo`', and for convenience
the main and Windows FAQs are also. This has the advantage that is is
easy to produce HTML and plain text versions as well as typeset manuals.

LaTeX is not used directly, but rather as an intermediate format for
typeset help documents and for vignettes.

Care needs to be taken about the assumptions made about the R user's
system: it may not have either '`texinfo`' or a TeX system
installed. We have attempted to abstract out the cross-platform
differences, and almost all the setting of typeset documents is done by
`tools::texi2dvi`. This is used for offline printing of help documents,
preparing vignettes and for package manuals via `R CMD Rd2pdf`. It is
not currently used for the R manuals created in directory
`doc/manual`.

`tools::texi2dvi` makes use of a system command `texi2dvi` where
available. On a Unix-alike this is usually part of '`texinfo`',
whereas on Windows if it exists at all it would be an executable, part
of MiKTeX. If none is available, the R code runs a sequence of
`(pdf)latex`, `bibtex` and `makeindex` commands.

This process has been rather vulnerable to the versions of the external
software used: particular issues have been `texi2dvi` and
`texinfo.tex` updates, mismatches between the
two[^26^](#FOOT26), versions of the LaTeX package
'`hyperref`' and quirks in index production. The licenses used
for LaTeX and latterly '`texinfo`' prohibit us from including
'known good' versions in the R distribution.

On a Unix-alike `configure` looks for the executables for TeX and
friends and if found records the absolute paths in the system
`Renviron` file. This used to record '`false`' if no
command was found, but it nowadays records the name for looking up on
the path at run time. The latter can be important for binary
distributions: one does not want to be tied to, for example, TeX Live 2007.

---
