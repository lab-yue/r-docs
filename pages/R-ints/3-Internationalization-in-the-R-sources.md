3 Internationalization in the R sources

---

The process of marking messages (errors, warnings etc) for translation
in an R package is described in
[Internationalization](./R-exts.html#Internationalization) in Writing R
Extensions, and the standard packages included with R have (with an
exception in **grDevices** for the menus of the `windows()` device) been
internationalized in the same way as other packages.

---

• [R code](#R-code)     
 • [Main C code](#Main-C-code)     
 • [Windows-GUI-specific code](#Windows_002dGUI_002dspecific-code)     
 • [macOS GUI](#macOS-GUI)     
 • [Updating](#Updating)

---

---

### 3.1 R code

Internationalization for R code is done in exactly the same way as for
extension packages. As all standard packages which have R code also have
a namespace, it is never necessary to specify `domain`, but for
efficiency calls to `message`, `warning` and `stop` should include
`domain = NA` when the message is constructed _via_ `gettextf`,
`gettext` or `ngettext`.

For each package, the extracted messages and translation sources are
stored under package directory `po` in the source package, and
compiled translations under `inst/po` for installation to
package directory `po` in the installed package. This also
applies to C code in packages.

---

### 3.2 Main C code

The main C code (e.g. that in files `src/*/*.c` and in the
modules) is where R is closest to the sort of application for which
'`gettext`' was written. Messages in the main C code are in
domain `R` and stored in the top-level directory `po` with
compiled translations under `share/locale`.

The list of files covered by the R domain is specified in file
`po/POTFILES.in`.

The normal way to mark messages for translation is via `_("msg")` just
as for packages. However, sometimes one needs to mark passages for
translation without wanting them translated at the time, for example
when declaring string constants. This is the purpose of the `N_` macro,
for example

```r
{ ERROR_ARGTYPE,           N_("invalid argument type")},
```

from file `src/main/errors.c`.

The `P_` macro

```r
#ifdef ENABLE_NLS
#define P_(StringS, StringP, N) ngettext (StringS, StringP, N)
#else
#define P_(StringS, StringP, N) (N > 1 ? StringP: StringS)
#endif
```

may be used as a wrapper for `ngettext`: however in some cases the
preferred approach has been to conditionalize (on `ENABLE_NLS`) code
using `ngettext`.

The macro `_("msg")` can safely be used in directory
`src/appl`; the header for standalone '`nmath`' skips
possible translation. (This does not apply to `N_` or `P_`).

---

### 3.3 Windows-GUI-specific code

Messages for the Windows GUI are in a separate domain '`RGui`'.
This was done for two reasons:

- The translators for the Windows version of R might be separate from
  those for the rest of R (familiarity with the GUI helps), and
- Messages for Windows are most naturally handled in the native
  charset for the language, and in the case of CJK languages the
  charset is Windows-specific. (It transpires that as the `iconv` we
  ported works well under Windows, this is less important than
  anticipated.)

Messages for the '`RGui`' domain are marked by `G_("msg")`, a
macro that is defined in header file `src/gnuwin32/win-nls.h`.
The list of files that are considered is hardcoded in the
`RGui.pot-update` target of file `po/Makefile.in.in`: note that
this includes `devWindows.c` as the menus on the `windows`
device are considered to be part of the GUI. (There is also
`GN_("msg")`, the analogue of `N_("msg")`.)

The template and message catalogs for the '`RGui`' domain are
in the top-level `po` directory.

---

### 3.4 macOS GUI

This is handled separately: see
<https://developer.r-project.org/Translations30.html>.

---

### 3.5 Updating

See file `po/README` for how to update the message templates
and catalogs.

---
