9 R coding standards

---

R is meant to run on a wide variety of platforms, including Linux and
most variants of Unix as well as Windows and macOS. Therefore, when
extending R by either adding to the R base distribution or by providing
an add-on package, one should not rely on features specific to only a
few supported platforms, if this can be avoided. In particular, although
most R developers use GNU tools, they should not employ the GNU
extensions to standard tools. Whereas some other software packages
explicitly rely on e.g. GNU make or the GNU C++ compiler, R does not.
Nevertheless, R is a GNU project, and the spirit of the GNU Coding
Standards should be followed if possible.

The following tools can "safely be assumed" for R extensions.

- An ISO C99 C compiler. Note that extensions such as POSIX 1003.1
  must be tested for, typically using Autoconf unless you are sure
  they are supported on all mainstream R platforms (including Windows
  and macOS).

- A fixed-form Fortran compiler.

- A simple `make`, considering the features of `make` in 4.2 BSD
  systems as a baseline.

  GNU or other extensions, including pattern rules using
  '`%`', the automatic variable '`$^`', the
  '`+=`' syntax to append to the value of a variable, the
  ("safe") inclusion of makefiles with no error, conditional
  execution, and many more, must not be used (see Chapter "Features"
  in the GNU Make Manual for more information). On the other hand,
  building R in a separate directory (not containing the sources)
  should work provided that `make` supports the `VPATH` mechanism.

  Windows-specific makefiles can assume GNU `make` 3.79 or later, as
  no other `make` is viable on that platform.

- A Bourne shell and the "traditional" Unix programming tools,
  including `grep`, `sed`, and `awk`.

  There are POSIX standards for these tools, but these may not be
  fully supported. Baseline features could be determined from a book
  such as The UNIX Programming Environment by Brian W. Kernighan & Rob
  Pike. Note in particular that '`|`' in a regexp is an
  extended regexp, and is not supported by all versions of `grep` or
  `sed`. The Open Group Base Specifications, Issue 7, which are
  technically identical to IEEE Std 1003.1 (POSIX), 2008, are
  available at
  <http://pubs.opengroup.org/onlinepubs/9699919799/mindex.html>.

Under Windows, most users will not have these tools installed, and you
should not require their presence for the operation of your package.
However, users who install your package from source will have them, as
they can be assumed to have followed the instructions in "the Windows
toolset" appendix of the "R Installation and Administration" manual to
obtain them. Redirection cannot be assumed to be available via `system`
as this does not use a standard shell (let alone a Bourne shell).

In addition, the following tools are needed for certain tasks.

- Perl version 5 is only needed for the maintainer-only script
  `tools/help2man.pl`.
- Makeinfo version 4.7 or later is needed to build the Info files for
  the R manuals written in the GNU Texinfo system.

It is also important that code is written in a way that allows others to
understand it. This is particularly helpful for fixing problems, and
includes using self-descriptive variable names, commenting the code, and
also formatting it properly. The R Core Team recommends to use a basic
indentation of 4 for R and C (and most likely also Perl) code, and 2 for
documentation in Rd format. Emacs (21 or later) users can implement this
indentation style by putting the following in one of their startup
files, and using customization to set the `c-default-style` to `"bsd"`
and `c-basic-offset` to `4`.)

```r
;;; ESS
(add-hook 'ess-mode-hook
          (lambda ()
            (ess-set-style 'C++ 'quiet)
            ;; Because
            ;;                                 DEF GNU BSD K&R C++
            ;; ess-indent-level                  2   2   8   5   4
            ;; ess-continued-statement-offset    2   2   8   5   4
            ;; ess-brace-offset                  0   0  -8  -5  -4
            ;; ess-arg-function-offset           2   4   0   0   0
            ;; ess-expression-offset             4   2   8   5   4
            ;; ess-else-offset                   0   0   0   0   0
            ;; ess-close-brace-offset            0   0   0   0   0
            (add-hook 'local-write-file-hooks
                      (lambda ()
                        (ess-nuke-trailing-whitespace)))))
(setq ess-nuke-trailing-whitespace-p 'ask)
;; or even
;; (setq ess-nuke-trailing-whitespace-p t)
```

```r
;;; Perl
(add-hook 'perl-mode-hook
          (lambda () (setq perl-indent-level 4)))
```

(The 'GNU' styles for Emacs' C and R modes use a basic indentation of 2,
which has been determined not to display the structure clearly enough
when using narrow fonts.)

---
