# 7 GUI consoles

---

The standard R front-ends are programs which run in a terminal, but
there are several ways to provide a GUI console.

This can be done by a package which is loaded from terminal-based R and
launches a console as part of its startup code or by the user running a
specific function: package
[**Rcmdr**](https://CRAN.R-project.org/package=Rcmdr) is a well-known
example with a Tk-based GUI.

There used to be a Gtk-based console invoked by `R --gui=GNOME`: this
relied on special-casing in the front-end shell script to launch a
different executable. There still is `R --gui=Tk`, which starts
terminal-based R and runs `tcltk::tkStartGui()` as part of the modified
startup sequence.

However, the main way to run a GUI console is to launch a separate
program which runs embedded R: this is done by `Rgui.exe` on Windows and
`R.app` on macOS. The first is an integral part of R and the code for
the console is currently in `R.dll`.

---

• [R.app](#R_002eapp)

---

---

### 7.1 R.app

`R.app` is a macOS application which provides a console. Its sources are
a separate project[^21^](#FOOT21), and its binaries link to an
R installation which it runs as a dynamic library `libR.dylib`.
The standard CRAN distribution of R for macOS bundles the GUI and R
itself, but installing the GUI is optional and either component can be
updated separately.

`R.app` relies on `libR.dylib` being in a specific place, and
hence on R having been built and installed as a Mac macOS 'framework'.
Specifically, it uses `/Library/Frameworks/R.framework/R`. This
is a symbolic link, as frameworks can contain multiple versions of R. It
eventually resolves to
`/Library/Frameworks/R.framework/Versions/Current/Resources/lib/libR.dylib`,
which is (in the CRAN distribution) a 'fat' binary containing multiple
sub-architectures.

macOS applications are directory trees: each `R.app` contains a
front-end written in Objective-C for one sub-architecture: in the
standard distribution there are separate applications for 32- and 64-bit
Intel architectures.

Originally the R sources contained quite a lot of code used only by the
macOS GUI, but this was migrated to the `R.app` sources.

`R.app` starts R as an embedded application with a command-line which
includes `--gui=aqua` (see below). It uses most of the
interface pointers defined in the header `Rinterface.h`, plus a
private interface pointer in file `src/main/sysutils.c`. It
adds an environment it names `tools:RGUI` to the second position in the
search path. This contains a number of utility functions used to support
the menu items, for example `package.manager()`, plus functions `q()`
and `quit()` which mask those in package **base**---the custom versions
save the history in a way specific to `R.app`.

There is a `configure` option `--with-aqua` for R which
customizes the way R is built: this is distinct from the
`--enable-R-framework` option which causes `make install` to
install R as the framework needed for use with `R.app`. (The option
`--with-aqua` is the default on macOS.) It sets the macro
`HAVE_AQUA` in `config.h` and the make variable
`BUILD_AQUA_TRUE`. These have several consequences:

- The `quartz()` device is built (other than as a stub) in package
  **grDevices**: this needs an Objective-C compiler. Then `quartz()`
  can be used with terminal R provided the latter has access to the
  macOS screen.
- File `src/unix/aqua.c` is compiled. This now only contains
  an interface pointer for the `quartz()` device(s).
- `capabilities("aqua")` is set to `TRUE`.
- The default path for a personal library directory is set as
  `~/Library/R/x.y/library`.
- There is support for setting a 'busy' indicator whilst waiting for
  `system()` to return.
- `R_ProcessEvents` is inhibited in a forked child from package
  **parallel**. The associated callback in `R.app` does things which
  should not be done in a child, and forking forks the whole process
  including the console.
- There is support for starting the embedded R with the option
  `--gui=aqua`: when this is done the global C variable
  `useaqua` is set to a true value. This has consequences:
  - The R session is asserted to be interactive _via_
    `R_Interactive`.
  - `.Platform$GUI` is set to `"AQUA"`. That has consequences:
    - The environment variable `DISPLAY` is set to '`:0`'
      if not already set.
    - `/usr/local/bin` is appended to `PATH` since that
      is where `gfortran` is installed.
    - The default HTML browser is switched to the one in `R.app`.
    - Various widgets are switched to the versions provided in
      `R.app`: these include graphical menus, the data editor (but
      not the data viewer used by `View()`) and the workspace
      browser invoked by `browseEnv()`.
    - The **grDevices** package when loaded knows that it is being
      run under `R.app` and so informs any `quartz` devices that a
      Quartz event loop is already running.
  - The use of the OS's `system` function (including by `system()`
    and `system2()`, and to launch editors and pagers) is replaced
    by a version in `R.app` (which by default just calls the OS's
    `system` with various signal handlers reset).
- If either R was started by `--gui=aqua` or R is running in
  a terminal which is not of type '`dumb`', the standard
  output to files `stdout` and `stderr` is directed
  through the C function `Rstd_WriteConsoleEx`. This uses ANSI
  terminal escapes to render lines sent to `stderr` as bold on
  `stdout`.
- For historical reasons the startup option `-psn` is allowed but
  ignored. (It seems that in 2003, '`r27492`', this was added
  by Finder.)

---
