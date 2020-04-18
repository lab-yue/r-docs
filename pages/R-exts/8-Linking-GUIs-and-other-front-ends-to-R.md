# 8 Linking GUIs and other front-ends to R

---

There are a number of ways to build front-ends to R: we take this to
mean a GUI or other application that has the ability to submit commands
to R and perhaps to receive results back (not necessarily in a text
format). There are other routes besides those described here, for
example the package
[**Rserve**](https://CRAN.R-project.org/package=Rserve) (from CRAN, see
also <https://www.rforge.net/Rserve/>) and connections to Java in
'`JRI`' (part of the
[**rJava**](https://CRAN.R-project.org/package=rJava) package on CRAN)
and the Omegahat/Bioconductor package '`SJava`'.

Note that the APIs described in this chapter are only intended to be
used in an alternative front-end: they are not part of the API made
available for R packages and can be dangerous to use in a conventional
package (although packages may contain alternative front-ends).
Conversely some of the functions from the API (such as `R_alloc`) should
not be used in front-ends.

---

• [Embedding R under Unix-alikes](#Embedding-R-under-Unix_002dalikes)     
 • [Embedding R under Windows](#Embedding-R-under-Windows)

---

---

### 8.1 Embedding R under Unix-alikes

R can be built as a shared library[^156^](#FOOT156) if
configured with `--enable-R-shlib`. This shared library can be
used to run R from alternative front-end programs. We will assume this
has been done for the rest of this section. Also, it can be built as a
static library if configured with `--enable-R-static-lib`, and
that can be used in a very similar way (at least on Linux: on other
platforms one needs to ensure that all the symbols exported by
`libR.a` are linked into the front-end).

The command-line R front-end, `R_HOME/bin/exec/R`, is one such
example, and the former GNOME (see package **gnomeGUI** on CRAN's
'`Archive`' area) and macOS consoles are others. The source for
`R_HOME/bin/exec/R` is in file `src/main/Rmain.c` and
is very simple

```r
int Rf_initialize_R(int ac, char **av); /* in ../unix/system.c */
void Rf_mainloop();                     /* in main.c */

extern int R_running_as_main_program;   /* in ../unix/system.c */

int main(int ac, char **av)
{
    R_running_as_main_program = 1;
    Rf_initialize_R(ac, av);
    Rf_mainloop(); /* does not return */
    return 0;
}
```

indeed, misleadingly simple. Remember that `R_HOME/bin/exec/R`
is run from a shell script `R_HOME/bin/R` which sets up the
environment for the executable, and this is used for

- Setting `R_HOME` and checking it is valid, as well as the path
  `R_SHARE_DIR` and `R_DOC_DIR` to the installed `share` and
  `doc` directory trees. Also setting `R_ARCH` if needed.
- Setting `LD_LIBRARY_PATH` to include the directories used in
  linking R. This is recorded as the default setting of
  `R_LD_LIBRARY_PATH` in the shell script
  `R_HOME/etcR_ARCH/ldpaths`.
- Processing some of the arguments, for example to run R under a
  debugger and to launch alternative front-ends to provide GUIs.

The first two of these can be achieved for your front-end by running it
_via_ `R CMD`. So, for example

```r
R CMD /usr/local/lib/R/bin/exec/R
R CMD exec/R
```

will both work in a standard R installation. (`R CMD` looks first for
executables in `R_HOME/bin`. These command-lines need
modification if a sub-architecture is in use.) If you do not want to run
your front-end in this way, you need to ensure that `R_HOME` is set and
`LD_LIBRARY_PATH` is suitable. (The latter might well be, but modern
Unix/Linux systems do not normally include `/usr/local/lib`
(`/usr/local/lib64` on some architectures), and R does look
there for system components.)

The other senses in which this example is too simple are that all the
internal defaults are used and that control is handed over to the R main
loop. There are a number of small examples[^157^](#FOOT157) in
the `tests/Embedding` directory. These make use of
`Rf_initEmbeddedR` in `src/main/Rembedded.c`, and essentially
use

```r
#include <Rembedded.h>

int main(int ac, char **av)
{
    /* do some setup */
    Rf_initEmbeddedR(argc, argv);
    /* do some more setup */

    /* submit some code to R, which is done interactively via
        run_Rmainloop();

        A possible substitute for a pseudo-console is

        R_ReplDLLinit();
        while(R_ReplDLLdo1() > 0) {
        /* add user actions here if desired */
       }

     */
    Rf_endEmbeddedR(0);
    /* final tidying up after R is shutdown */
    return 0;
}
```

If you do not want to pass R arguments, you can fake an `argv` array,
for example by

```r
    char *argv[]= {"REmbeddedPostgres", "--silent"};
    Rf_initEmbeddedR(sizeof(argv)/sizeof(argv[0]), argv);
```

However, to make a GUI we usually do want to run `run_Rmainloop` after
setting up various parts of R to talk to our GUI, and arranging for our
GUI callbacks to be called during the R mainloop.

One issue to watch is that on some platforms `Rf_initEmbeddedR` and
`Rf_endEmbeddedR` change the settings of the FPU (e.g. to allow errors
to be trapped and to make use of extended precision registers).

The standard code sets up a session temporary directory in the usual
way, _unless_ `R_TempDir` is set to a non-NULL value before
`Rf_initEmbeddedR` is called. In that case the value is assumed to
contain an existing writable directory (no check is done), and it is not
cleaned up when R is shut down.

`Rf_initEmbeddedR` sets R to be in interactive mode: you can set
`R_Interactive` (defined in `Rinterface.h`) subsequently to
change this.

Note that R expects to be run with the locale category
'`LC_NUMERIC`' set to its default value of `C`, and so should
not be embedded into an application which changes that.

It is the user's responsibility to attempt to initialize only once. To
protect the R interpreter, `Rf_initialize_R` will exit the process if
re-initialization is attempted.

---

• [Compiling against the R library](#Compiling-against-the-R-library)     
 • [Setting R callbacks](#Setting-R-callbacks)     
 • [Registering symbols](#Registering-symbols)     
 • [Meshing event loops](#Meshing-event-loops)     
 • [Threading issues](#Threading-issues)

---

---

#### 8.1.1 Compiling against the R library

Suitable flags to compile and link against the R (shared or static)
library can be found by

```r
R CMD config --cppflags
R CMD config --ldflags
```

(These apply only to an uninstalled copy or a standard install.)

If R is installed, `pkg-config` is available and neither
sub-architectures nor a macOS framework have been used, alternatives for
a shared R library are

```r
pkg-config --cflags libR
pkg-config --libs libR
```

and for a static R library

```r
pkg-config --cflags libR
pkg-config --libs --static libR
```

(This may work for an installed OS framework if `pkg-config` is taught
where to look for `libR.pc`: it is installed inside the
framework.)

However, a more comprehensive way is to set up a `Makefile` to
compile the front-end. Suppose file `myfe.c` is to be compiled
to `myfe`. A suitable `Makefile` might be

```r
## WARNING: does not work when ${R_HOME} contains spaces
include ${R_HOME}/etc${R_ARCH}/Makeconf
all: myfe

## The following is not needed, but avoids PIC flags.
myfe.o: myfe.c
        $(CC) $(ALL_CPPFLAGS) $(CFLAGS) -c myfe.c -o $@

## replace $(LIBR) $(LIBS) by $(STATIC_LIBR) if R was build with a static libR
myfe: myfe.o
        $(MAIN_LINK) -o $@ myfe.o $(LIBR) $(LIBS)
```

invoked as

```r
R CMD make
R CMD myfe
```

Even though not recommended, `${R_HOME}` may contain spaces. In that
case, it cannot be passed as an argument to `include` in the makefile.
Instead, one can instruct `make` using the `-f` option to include
`Makeconf`, for example _via_ recursive invocation of `make`,
see [Writing portable packages](#Writing-portable-packages).

```r
all:
      $(MAKE) -f "${R_HOME}/etc${R_ARCH}/Makeconf" -f Makefile.inner
```

Additional flags which `$(MAIN_LINK)` includes are, amongst others,
those to select OpenMP and `--export-dynamic` for the GNU
linker on some platforms. In principle `$(LIBS)` is not needed when
using a shared R library as `libR` is linked against those
libraries, but some platforms need the executable also linked against
them.

---

#### 8.1.2 Setting R callbacks

For Unix-alikes there is a public header file `Rinterface.h`
that makes it possible to change the standard callbacks used by R in a
documented way. This defines pointers (if `R_INTERFACE_PTRS` is defined)

```r
extern void (*ptr_R_Suicide)(const char *);
extern void (*ptr_R_ShowMessage)(const char *);
extern int  (*ptr_R_ReadConsole)(const char *, unsigned char *, int, int);
extern void (*ptr_R_WriteConsole)(const char *, int);
extern void (*ptr_R_WriteConsoleEx)(const char *, int, int);
extern void (*ptr_R_ResetConsole)();
extern void (*ptr_R_FlushConsole)();
extern void (*ptr_R_ClearerrConsole)();
extern void (*ptr_R_Busy)(int);
extern void (*ptr_R_CleanUp)(SA_TYPE, int, int);
extern int  (*ptr_R_ShowFiles)(int, const char **, const char **,
                               const char *, Rboolean, const char *);
extern int  (*ptr_R_ChooseFile)(int, char *, int);
extern int  (*ptr_R_EditFile)(const char *);
extern void (*ptr_R_loadhistory)(SEXP, SEXP, SEXP, SEXP);
extern void (*ptr_R_savehistory)(SEXP, SEXP, SEXP, SEXP);
extern void (*ptr_R_addhistory)(SEXP, SEXP, SEXP, SEXP);
// added in R 3.0.0
extern int  (*ptr_R_EditFiles)(int, const char **, const char **, const char *);
extern SEXP (*ptr_do_selectlist)(SEXP, SEXP, SEXP, SEXP);
extern SEXP (*ptr_do_dataentry)(SEXP, SEXP, SEXP, SEXP);
extern SEXP (*ptr_do_dataviewer)(SEXP, SEXP, SEXP, SEXP);
extern void (*ptr_R_ProcessEvents)();
```

which allow standard R callbacks to be redirected to your GUI. What
these do is generally documented in the file
`src/unix/system.txt`.

Function: _void_ **R_ShowMessage** _(char \*`message`)_

: This should display the message, which may have multiple lines: it
should be brought to the user's attention immediately.

Function: _void_ **R_Busy** _(int `which`)_

: This function invokes actions (such as change of cursor) when R
embarks on an extended computation (`which=1`) and when such a state
terminates (`which=0`).

Function: _int_ **R_ReadConsole** _(const char \*`prompt`, unsigned char \*`buf`, int `buflen`, int `hist`)_\
Function: _void_ **R_WriteConsole** _(const char \*`buf`, int `buflen`)_\
Function: _void_ **R_WriteConsoleEx** _(const char \*`buf`, int `buflen`, int `otype`)_\
Function: _void_ **R_ResetConsole** _()_\
Function: _void_ **R_FlushConsole** _()_\
Function: _void_ **R_ClearErrConsole** _()_

: These functions interact with a console.

    `R_ReadConsole` prints the given prompt at the console and then does
    a `fgets(3)`--like operation, transferring up to `buflen`
    characters into the buffer `buf`. The last two bytes
    should be set to '`"\n\0"`' to preserve sanity. If
    `hist` is non-zero, then the line should be added to any
    command history which is being maintained. The return value is 0 is
    no input is available and \>0 otherwise.

    `R_WriteConsoleEx` writes the given buffer to the console,
    `otype` specifies the output type (regular output or
    warning/error). Call to `R_WriteConsole(buf, buflen)` is equivalent
    to `R_WriteConsoleEx(buf, buflen, 0)`. To ensure backward
    compatibility of the callbacks, `ptr_R_WriteConsoleEx` is used only
    if `ptr_R_WriteConsole` is set to `NULL`. To ensure that `stdout()`
    and `stderr()` connections point to the console, set the
    corresponding files to `NULL` *via*


    ``` r
          R_Outputfile = NULL;
          R_Consolefile = NULL;
    ```

    `R_ResetConsole` is called when the system is reset after an error.
    `R_FlushConsole` is called to flush any pending output to the system
    console. `R_ClearerrConsole` clears any errors associated with
    reading from the console.

Function: _int_ **R_ShowFiles** _(int `nfile`, const char \*\*`file`, const char \*\*`headers`, const char \*`wtitle`, Rboolean `del`, const char \*`pager`)_

: This function is used to display the contents of files.

Function: _int_ **R_ChooseFile** _(int `new`, char \*`buf`, int `len`)_

: Choose a file and return its name in `buf` of length
`len`. Return value is 0 for success, \> 0 otherwise.

Function: _int_ **R_EditFile** _(const char \*`buf`)_

: Send a file to an editor window.

Function: _int_ **R_EditFiles** _(int `nfile`, const char \*\*`file`, const char \*\*`title`, const char \*`editor`)_

: Send `nfile` files to an editor, with titles possibly to
be used for the editor window(s).

Function: _SEXP_ **R_loadhistory** _(SEXP, SEXP, SEXP, SEXP);_\
Function: _SEXP_ **R_savehistory** _(SEXP, SEXP, SEXP, SEXP);_\
Function: _SEXP_ **R_addhistory** _(SEXP, SEXP, SEXP, SEXP);_

: `.Internal` functions for `loadhistory`, `savehistory` and
`timestamp`.

    If the console has no history mechanism these can be as simple as


    ``` r
    SEXP R_loadhistory (SEXP call, SEXP op, SEXP args, SEXP env)
    {
        errorcall(call, "loadhistory is not implemented");
        return R_NilValue;
    }
    SEXP R_savehistory (SEXP call, SEXP op , SEXP args, SEXP env)
    {
        errorcall(call, "savehistory is not implemented");
        return R_NilValue;
    }
    SEXP R_addhistory (SEXP call, SEXP op , SEXP args, SEXP env)
    {
        return R_NilValue;
    }
    ```

    The `R_addhistory` function should return silently if no history
    mechanism is present, as a user may be calling `timestamp` purely to
    write the time stamp to the console.

Function: _void_ **R_Suicide** _(const char \*`message`)_

: This should abort R as rapidly as possible, displaying the message.
A possible implementation is

    ``` r
    void R_Suicide (const char *message)
    {
        char  pp[1024];
        snprintf(pp, 1024, "Fatal error: %s\n", s);
        R_ShowMessage(pp);
        R_CleanUp(SA_SUICIDE, 2, 0);
    }
    ```

Function: _void_ **R_CleanUp** _(SA_TYPE `saveact`, int `status`, int `RunLast`)_

: This function invokes any actions which occur at system termination.
It needs to be quite complex:

    ``` r
    #include <Rinterface.h>
    #include <Rembedded.h>    /* for Rf_KillAllDevices */

    void R_CleanUp (SA_TYPE saveact, int status, int RunLast)
    {
        if(saveact == SA_DEFAULT) saveact = SaveAction;
        if(saveact == SA_SAVEASK) {
           /* ask what to do and set saveact */
        }
        switch (saveact) {
        case SA_SAVE:
            if(runLast) R_dot_Last();
            if(R_DirtyImage) R_SaveGlobalEnv();
            /* save the console history in R_HistoryFile */
            break;
        case SA_NOSAVE:
            if(runLast) R_dot_Last();
            break;
        case SA_SUICIDE:
        default:
            break;
        }

        R_RunExitFinalizers();
        /* clean up after the editor e.g. CleanEd() */

        R_CleanTempDir();

        /* close all the graphics devices */
        if(saveact != SA_SUICIDE) Rf_KillAllDevices();
        fpu_setup(FALSE);

        exit(status);
    }
    ```

These callbacks should never be changed in a running R session (and
hence cannot be called from an extension package).

Function: _SEXP_ **R_dataentry** _(SEXP, SEXP, SEXP, SEXP);_\
Function: _SEXP_ **R_dataviewer** _(SEXP, SEXP, SEXP, SEXP);_\
Function: _SEXP_ **R_selectlist** _(SEXP, SEXP, SEXP, SEXP);_

: `.External` functions for `dataentry` (and `edit` on matrices and
data frames), `View` and `select.list`. These can be changed if they
are not currently in use.

---

#### 8.1.3 Registering symbols

An application embedding R needs a different way of registering symbols
because it is not a dynamic library loaded by R as would be the case
with a package. Therefore R reserves a special `DllInfo` entry for the
embedding application such that it can register symbols to be used with
`.C`, `.Call` etc. This entry can be obtained by calling
`getEmbeddingDllInfo`, so a typical use is

```r
DllInfo *info = R_getEmbeddingDllInfo();
R_registerRoutines(info, cMethods, callMethods, NULL, NULL);
```

The native routines defined by `cMethods` and `callMethods` should be
present in the embedding application. See [Registering native routines](#Registering-native-routines) for details on registering
symbols in general.

---

#### 8.1.4 Meshing event loops

One of the most difficult issues in interfacing R to a front-end is the
handling of event loops, at least if a single thread is used. R uses
events and timers for

- Running X11 windows such as the graphics device and data editor, and
  interacting with them (e.g., using `locator()`).
- Supporting Tcl/Tk events for the **tcltk** package (for at least the
  X11 version of Tk).
- Preparing input.
- Timing operations, for example for profiling R code and
  `Sys.sleep()`.
- Interrupts, where permitted.

Specifically, the Unix-alike command-line version of R runs separate
event loops for

- Preparing input at the console command-line, in file
  `src/unix/sys-unix.c`.
- Waiting for a response from a socket in the internal functions
  underlying FTP and HTTP transfers in `download.file()` and for
  direct socket access, in files
  `src/modules/internet/nanoftp.c`,
  `src/modules/internet/nanohttp.c` and
  `src/modules/internet/Rsock.c`
- Mouse and window events when displaying the X11-based dataentry
  window, in file `src/modules/X11/dataentry.c`. This is
  regarded as _modal_, and no other events are serviced whilst it is
  active.

There is a protocol for adding event handlers to the first two types of
event loops, using types and functions declared in the header
`R_ext/eventloop.h` and described in comments in file
`src/unix/sys-std.c`. It is possible to add (or remove) an
input handler for events on a particular file descriptor, or to set a
polling interval (_via_ `R_wait_usec`) and a function to be called
periodically _via_ `R_PolledEvents`: the polling mechanism is used by
the **tcltk** package.

It is not intended that these facilities are used by packages, but if
they are needed exceptionally, the package should ensure that it cleans
up and removes its handlers when its namespace is unloaded. Note that
the header `sys/select.h` is needed[^158^](#FOOT158):
users should check this is available and define `HAVE_SYS_SELECT_H`
before including `R_ext/eventloop.h`. (It is often the case
that another header will include `sys/select.h` before
`eventloop.h` is processed, but this should not be relied on.)

An alternative front-end needs both to make provision for other R events
whilst waiting for input, and to ensure that it is not frozen out during
events of the second type. The ability to add a polled handler as
`R_timeout_handler` is used by the **tcltk** package.

---

#### 8.1.5 Threading issues

Embedded R is designed to be run in the main thread, and all the testing
is done in that context. There is a potential issue with the
stack-checking mechanism where threads are involved. This uses two
variables declared in `Rinterface.h` (if `CSTACK_DEFNS` is
defined) as

```r
extern uintptr_t R_CStackLimit; /* C stack limit */
extern uintptr_t R_CStackStart; /* Initial stack address */
```

Note that `uintptr_t` is an optional C99 type for which a substitute is
defined in R, so your code needs to define `HAVE_UINTPTR_T`
appropriately. To do so, test if the type is defined in C header
`stdint.h` or C++ header `cstdint` and if so include
the header and define `HAVE_UINTPTR_T` before including
`Rinterface.h`. (For C code one can simply include
`Rconfig.h`, possibly _via_ `R.h`, and for C++11 code
`Rinterface.h` will include the header `cstdint`.)

These will be set[^159^](#FOOT159) when `Rf_initialize_R` is
called, to values appropriate to the main thread. Stack-checking can be
disabled by setting `R_CStackLimit = (uintptr_t)-1` immediately after
`Rf_initialize_R` is called, but it is better to if possible set
appropriate values. (What these are and how to determine them are
OS-specific, and the stack size limit may differ for secondary threads.
If you have a choice of stack size, at least 10Mb is recommended.)

You may also want to consider how signals are handled: R sets signal
handlers for several signals, including `SIGINT`, `SIGSEGV`, `SIGPIPE`,
`SIGUSR1` and `SIGUSR2`, but these can all be suppressed by setting the
variable `R_SignalHandlers` (declared in `Rinterface.h`) to
`0`.

Note that these variables must not be changed by an R **package**: a
package should not call R internals which makes use of the
stack-checking mechanism on a secondary thread.

---

### 8.2 Embedding R under Windows

All Windows interfaces to R call entry points in the DLL
`R.dll`, directly or indirectly. Simpler applications may find
it easier to use the indirect route _via_ (D)COM.

---

• [Using (D)COM](#Using-_0028D_0029COM)     
 • [Calling R.dll directly](#Calling-R_002edll-directly)     
 • [Finding R_HOME](#Finding-R_005fHOME)

---

---

#### 8.2.1 Using (D)COM

(D)COM is a standard Windows mechanism used for communication between
Windows applications. One application (here R) is run as COM server
which offers services to clients, here the front-end calling
application. The services are described in a 'Type Library' and are
(more or less) language-independent, so the calling application can be
written in C or C++ or Visual Basic or Perl or Python and so on. The 'D'
in (D)COM refers to 'distributed', as the client and server can be
running on different machines.

The basic R distribution is not a (D)COM server, but two addons are
currently available that interface directly with R and provide a (D)COM
server:

- There is a (D)COM server called `StatConnector` written by Thomas
  Baier available _via_ <http://www.autstat.com/>, which works with R
  packages to support transfer of data to and from R and remote
  execution of R commands, as well as embedding of an R graphics
  window.

  Recent versions have usage restrictions.

- Another (D)COM server, `RDCOMServer`, may be available from
  Omegahat, <http://www.omegahat.net/>. Its philosophy is discussed in
  <http://www.omegahat.net/RDCOMServer/Docs/Paradigm.html> and is very
  different from the purpose of this section.

---

#### 8.2.2 Calling R.dll directly

The `R` DLL is mainly written in C and has `_cdecl` entry points.
Calling it directly will be tricky except from C code (or C++ with a
little care).

There is a version of the Unix-alike interface calling

```r
int Rf_initEmbeddedR(int ac, char **av);
void Rf_endEmbeddedR(int fatal);
```

which is an entry point in `R.dll`. Examples of its use (and a
suitable `Makefile.win`) can be found in the
`tests/Embedding` directory of the sources. You may need to
ensure that `R_HOME/bin` is in your `PATH` so the R DLLs are
found.

Examples of calling `R.dll` directly are provided in the
directory `src/gnuwin32/front-ends`, including a simple
command-line front end `rtest.c` whose code is

```r
#define Win32
#include <windows.h>
#include <stdio.h>
#include <Rversion.h>
#define LibExtern __declspec(dllimport) extern
#include <Rembedded.h>
#include <R_ext/RStartup.h>
/* for askok and askyesnocancel */
#include <graphapp.h>

/* for signal-handling code */
#include <psignal.h>

/* simple input, simple output */

/* This version blocks all events: a real one needs to call ProcessEvents
   frequently. See rterm.c and ../system.c for one approach using
   a separate thread for input.
*/
int myReadConsole(const char *prompt, char *buf, int len, int addtohistory)
{
    fputs(prompt, stdout);
    fflush(stdout);
    if(fgets(buf, len, stdin)) return 1; else return 0;
}

void myWriteConsole(const char *buf, int len)
{
    printf("%s", buf);
}

void myCallBack(void)
{
    /* called during i/o, eval, graphics in ProcessEvents */
}

void myBusy(int which)
{
    /* set a busy cursor ... if which = 1, unset if which = 0 */
}

static void my_onintr(int sig) { UserBreak = 1; }

int main (int argc, char **argv)
{
    structRstart rp;
    Rstart Rp = &rp;
    char Rversion[25], *RHome;

    sprintf(Rversion, "%s.%s", R_MAJOR, R_MINOR);
    if(strcmp(getDLLVersion(), Rversion) != 0) {
        fprintf(stderr, "Error: R.DLL version does not match\n");
        exit(1);
    }

    R_setStartTime();
    R_DefParams(Rp);
    if((RHome = get_R_HOME()) == NULL) {
        fprintf(stderr, "R_HOME must be set in the environment or Registry\n");
        exit(1);
    }
    Rp->rhome = RHome;
    Rp->home = getRUser();
    Rp->CharacterMode = LinkDLL;
    Rp->ReadConsole = myReadConsole;
    Rp->WriteConsole = myWriteConsole;
    Rp->CallBack = myCallBack;
    Rp->ShowMessage = askok;
    Rp->YesNoCancel = askyesnocancel;
    Rp->Busy = myBusy;

    Rp->R_Quiet = TRUE;        /* Default is FALSE */
    Rp->R_Interactive = FALSE; /* Default is TRUE */
    Rp->RestoreAction = SA_RESTORE;
    Rp->SaveAction = SA_NOSAVE;
    R_SetParams(Rp);
    R_set_command_line_arguments(argc, argv);

    FlushConsoleInputBuffer(GetStdHandle(STD_INPUT_HANDLE));

    signal(SIGBREAK, my_onintr);
    GA_initapp(0, 0);
    readconsolecfg();
    setup_Rmainloop();
#ifdef SIMPLE_CASE
    run_Rmainloop();
#else
    R_ReplDLLinit();
    while(R_ReplDLLdo1() > 0) {
/* add user actions here if desired */
    }
/* only get here on EOF (not q()) */
#endif
    Rf_endEmbeddedR(0);
    return 0;
}
```

The ideas are

- Check that the front-end and the linked `R.dll` match --
  other front-ends may allow a looser match.
- Find and set the R home directory and the user's home directory. The
  former may be available from the Windows Registry: it will be in
  `HKEY_LOCAL_MACHINE\Software\R-core\R\InstallPath` from an
  administrative install and
  `HKEY_CURRENT_USER\Software\R-core\R\InstallPath` otherwise, if
  selected during installation (as it is by default).
- Define startup conditions and callbacks _via_ the `Rstart`
  structure. `R_DefParams` sets the defaults, and `R_SetParams` sets
  updated values.
- Record the command-line arguments used by
  `R_set_command_line_arguments` for use by the R function
  `commandArgs()`.
- Set up the signal handler and the basic user interface.
- Run the main R loop, possibly with our actions intermeshed.
- Arrange to clean up.

An underlying theme is the need to keep the GUI 'alive', and this has
not been done in this example. The R callback `R_ProcessEvents` needs to
be called frequently to ensure that Windows events in R windows are
handled expeditiously. Conversely, R needs to allow the GUI code (which
is running in the same process) to update itself as needed -- two ways
are provided to allow this:

- `R_ProcessEvents` calls the callback registered by `Rp->callback`. A
  version of this is used to run package Tcl/Tk for **tcltk** under
  Windows, for the code is

  ```r
  void R_ProcessEvents(void)
  {
      while (peekevent()) doevent(); /* Windows events for GraphApp */
      if (UserBreak) { UserBreak = FALSE; onintr(); }
      R_CallBackHook();
      if(R_tcldo) R_tcldo();
  }
  ```

- The mainloop can be split up to allow the calling application to
  take some action after each line of input has been dealt with: see
  the alternative code below `#ifdef SIMPLE_CASE`.

It may be that no R GraphApp windows need to be considered, although
these include pagers, the `windows()` graphics device, the R data and
script editors and various popups such as `choose.file()` and
`select.list()`. It would be possible to replace all of these, but it
seems easier to allow GraphApp to handle most of them.

It is possible to run R in a GUI in a single thread (as
`RGui.exe` shows) but it will normally be
easier[^160^](#FOOT160) to use multiple threads.

Note that R's own front ends use a stack size of 10Mb, whereas MinGW
executables default to 2Mb, and Visual C++ ones to 1Mb. The latter stack
sizes are too small for a number of R applications, so general-purpose
front-ends should use a larger stack size.

---

#### 8.2.3 Finding R_HOME

Both applications which embed R and those which use a `system` call to
invoke R (as `Rscript.exe`, `Rterm.exe` or `R.exe`) need to be able to
find the R `bin` directory. The simplest way to do so is the
ask the user to set an environment variable `R_HOME` and use that, but
naive users may be flummoxed as to how to do so or what value to use.

The R for Windows installers have for a long time allowed the value of
`R_HOME` to be recorded in the Windows Registry: this is optional but
selected by default. _Where_ it is recorded has changed over the years
to allow for multiple versions of R to be installed at once, and to
allow 32- and 64-bit versions of R to be installed on the same machine.

The basic Registry location is `Software\R-core\R`. For an
administrative install this is under `HKEY_LOCAL_MACHINE` and on a
64-bit OS `HKEY_LOCAL_MACHINE\Software\R-core\R` is by default
redirected for a 32-bit application, so a 32-bit application will see
the information for the last 32-bit install, and a 64-bit application
that for the last 64-bit install. For a personal install, the
information is under `HKEY_CURRENT_USER\Software\R-core\R` which is seen
by both 32-bit and 64-bit applications and so records the last install
of either architecture. To circumvent this, there are locations
`Software\R-core\R32` and `Software\R-core\R64` which always refer to
one architecture.

When R is installed and recording is not disabled then two string values
are written at that location for keys `InstallPath` and
`Current Version`, and these keys are removed when R is uninstalled. To
allow information about other installed versions to be retained, there
is also a key named something like `3.0.0` or `3.0.0 patched` or
`3.1.0 Pre-release` with a value for `InstallPath`.

So a comprehensive algorithm to search for `R_HOME` is something like

- Decide which of personal or administrative installs should have
  precedence. There are arguments both ways: we find that with roaming
  profiles that `HKEY_CURRENT_USER\Software` often gets reverted to an
  earlier version. Do the following for one or both of
  `HKEY_CURRENT_USER` and `HKEY_LOCAL_MACHINE`.
- If the desired architecture is known, look in `Software\R-core\R32`
  or `Software\R-core\R64`, and if that does not exist or the
  architecture is immaterial, in `Software\R-core\R`.
- If key `InstallPath` exists then this is `R_HOME` (recorded using
  backslashes). If it does not, look for version-specific keys like
  `2.11.0 alpha`, pick the latest (which is of itself a complicated
  algorithm as `2.11.0 patched > 2.11.0 > 2.11.0 alpha > 2.8.1`) and
  use its value for `InstallPath`.

---

## Function and variable index

---

Jump to:   [**.**](#Function-and-variable-index_vr_symbol-1){.summary-letter}  
[**\\**](#Function-and-variable-index_vr_symbol-2){.summary-letter}
 \
 [**A**](#Function-and-variable-index_vr_letter-A){.summary-letter}  
[**B**](#Function-and-variable-index_vr_letter-B){.summary-letter}  
[**C**](#Function-and-variable-index_vr_letter-C){.summary-letter}  
[**D**](#Function-and-variable-index_vr_letter-D){.summary-letter}  
[**E**](#Function-and-variable-index_vr_letter-E){.summary-letter}  
[**F**](#Function-and-variable-index_vr_letter-F){.summary-letter}  
[**G**](#Function-and-variable-index_vr_letter-G){.summary-letter}  
[**I**](#Function-and-variable-index_vr_letter-I){.summary-letter}  
[**L**](#Function-and-variable-index_vr_letter-L){.summary-letter}  
[**M**](#Function-and-variable-index_vr_letter-M){.summary-letter}  
[**N**](#Function-and-variable-index_vr_letter-N){.summary-letter}  
[**O**](#Function-and-variable-index_vr_letter-O){.summary-letter}  
[**P**](#Function-and-variable-index_vr_letter-P){.summary-letter}  
[**Q**](#Function-and-variable-index_vr_letter-Q){.summary-letter}  
[**R**](#Function-and-variable-index_vr_letter-R){.summary-letter}  
[**S**](#Function-and-variable-index_vr_letter-S){.summary-letter}  
[**T**](#Function-and-variable-index_vr_letter-T){.summary-letter}  
[**U**](#Function-and-variable-index_vr_letter-U){.summary-letter}  
[**V**](#Function-and-variable-index_vr_letter-V){.summary-letter}

---

Index Entry

Section

---

.

[`.C`](#index-_002eC):

[Interface functions .C and
.Fortran](#Interface-functions-_002eC-and-_002eFortran)

[`.Call`](#index-_002eCall):

[Handling R objects in C](#Handling-R-objects-in-C)

[`.Call`](#index-_002eCall-1):

[Calling .Call](#Calling-_002eCall)

[`.External`](#index-_002eExternal):

[Handling R objects in C](#Handling-R-objects-in-C)

[`.External`](#index-_002eExternal-1):

[Calling .External](#Calling-_002eExternal)

[`.Fortran`](#index-_002eFortran):

[Interface functions .C and
.Fortran](#Interface-functions-_002eC-and-_002eFortran)

[`.Last.lib`](#index-_002eLast_002elib):

[Load hooks](#Load-hooks)

[`.onAttach`](#index-_002eonAttach):

[Load hooks](#Load-hooks)

[`.onDetach`](#index-_002eonDetach):

[Load hooks](#Load-hooks)

[`.onLoad`](#index-_002eonLoad):

[Load hooks](#Load-hooks)

[`.onUnload`](#index-_002eonUnload):

[Load hooks](#Load-hooks)

[`.Random.seed`](#index-_002eRandom_002eseed):

[Random numbers](#Random-numbers)

---

\\

[`\acronym`](#index-_005cacronym):

[Marking text](#Marking-text)

[`\alias`](#index-_005calias):

[Documenting functions](#Documenting-functions)

[`\arguments`](#index-_005carguments):

[Documenting functions](#Documenting-functions)

[`\author`](#index-_005cauthor):

[Documenting functions](#Documenting-functions)

[`\bold`](#index-_005cbold):

[Marking text](#Marking-text)

[`\cite`](#index-_005ccite):

[Marking text](#Marking-text)

[`\code`](#index-_005ccode):

[Marking text](#Marking-text)

[`\command`](#index-_005ccommand):

[Marking text](#Marking-text)

[`\concept`](#index-_005cconcept):

[Indices](#Indices)

[`\cr`](#index-_005ccr):

[Sectioning](#Sectioning)

[`\CRANpkg{pkg}`](#index-_005cCRANpkg_007bpkg_007d):

[User-defined macros](#User_002ddefined-macros)

[`\deqn`](#index-_005cdeqn):

[Mathematics](#Mathematics)

[`\describe`](#index-_005cdescribe):

[Lists and tables](#Lists-and-tables)

[`\description`](#index-_005cdescription):

[Documenting functions](#Documenting-functions)

[`\details`](#index-_005cdetails):

[Documenting functions](#Documenting-functions)

[`\dfn`](#index-_005cdfn):

[Marking text](#Marking-text)

[`\doi{numbers}`](#index-_005cdoi_007bnumbers_007d):

[User-defined macros](#User_002ddefined-macros)

[`\dontrun`](#index-_005cdontrun):

[Documenting functions](#Documenting-functions)

[`\dontshow`](#index-_005cdontshow):

[Documenting functions](#Documenting-functions)

[`\dots`](#index-_005cdots):

[Insertions](#Insertions)

[`\dQuote`](#index-_005cdQuote):

[Marking text](#Marking-text)

[`\email`](#index-_005cemail):

[Marking text](#Marking-text)

[`\emph`](#index-_005cemph):

[Marking text](#Marking-text)

[`\enc`](#index-_005cenc):

[Insertions](#Insertions)

[`\enumerate`](#index-_005cenumerate):

[Lists and tables](#Lists-and-tables)

[`\env`](#index-_005cenv):

[Marking text](#Marking-text)

[`\eqn`](#index-_005ceqn):

[Mathematics](#Mathematics)

[`\examples`](#index-_005cexamples):

[Documenting functions](#Documenting-functions)

[`\figure`](#index-_005cfigure):

[Figures](#Figures)

[`\file`](#index-_005cfile):

[Marking text](#Marking-text)

[`\format`](#index-_005cformat):

[Documenting data sets](#Documenting-data-sets)

[`\href`](#index-_005chref):

[Marking text](#Marking-text)

[`\if`](#index-_005cif):

[Conditional text](#Conditional-text)

[`\ifelse`](#index-_005cifelse):

[Conditional text](#Conditional-text)

[`\itemize`](#index-_005citemize):

[Lists and tables](#Lists-and-tables)

[`\kbd`](#index-_005ckbd):

[Marking text](#Marking-text)

[`\keyword`](#index-_005ckeyword):

[Documenting functions](#Documenting-functions)

[`\ldots`](#index-_005cldots):

[Insertions](#Insertions)

[`\link`](#index-_005clink):

[Cross-references](#Cross_002dreferences)

[`\method`](#index-_005cmethod):

[Documenting functions](#Documenting-functions)

[`\name`](#index-_005cname):

[Documenting functions](#Documenting-functions)

[`\newcommand`](#index-_005cnewcommand):

[User-defined macros](#User_002ddefined-macros)

[`\note`](#index-_005cnote):

[Documenting functions](#Documenting-functions)

[`\option`](#index-_005coption):

[Marking text](#Marking-text)

[`\out`](#index-_005cout):

[Conditional text](#Conditional-text)

[`\packageAuthor`](#index-_005cpackageAuthor):

[User-defined macros](#User_002ddefined-macros)

[`\packageDescription`](#index-_005cpackageDescription):

[User-defined macros](#User_002ddefined-macros)

[`\packageDESCRIPTION`](#index-_005cpackageDESCRIPTION):

[User-defined macros](#User_002ddefined-macros)

[`\packageIndices`](#index-_005cpackageIndices):

[User-defined macros](#User_002ddefined-macros)

[`\packageMaintainer`](#index-_005cpackageMaintainer):

[User-defined macros](#User_002ddefined-macros)

[`\packageTitle`](#index-_005cpackageTitle):

[User-defined macros](#User_002ddefined-macros)

[`\pkg`](#index-_005cpkg):

[Marking text](#Marking-text)

[`\preformatted`](#index-_005cpreformatted):

[Marking text](#Marking-text)

[`\R`](#index-_005cR):

[Insertions](#Insertions)

[`\RdOpts`](#index-_005cRdOpts):

[Dynamic pages](#Dynamic-pages)

[`\references`](#index-_005creferences):

[Documenting functions](#Documenting-functions)

[`\renewcommand`](#index-_005crenewcommand):

[User-defined macros](#User_002ddefined-macros)

[`\S3method`](#index-_005cS3method):

[Documenting functions](#Documenting-functions)

[`\samp`](#index-_005csamp):

[Marking text](#Marking-text)

[`\section`](#index-_005csection):

[Sectioning](#Sectioning)

[`\seealso`](#index-_005cseealso):

[Documenting functions](#Documenting-functions)

[`\Sexpr`](#index-_005cSexpr):

[Dynamic pages](#Dynamic-pages)

[`\source`](#index-_005csource):

[Documenting data sets](#Documenting-data-sets)

[`\sQuote`](#index-_005csQuote):

[Marking text](#Marking-text)

[`\sspace`](#index-_005csspace):

[User-defined macros](#User_002ddefined-macros)

[`\strong`](#index-_005cstrong):

[Marking text](#Marking-text)

[`\tabular`](#index-_005ctabular):

[Lists and tables](#Lists-and-tables)

[`\title`](#index-_005ctitle):

[Documenting functions](#Documenting-functions)

[`\url`](#index-_005curl):

[Marking text](#Marking-text)

[`\usage`](#index-_005cusage):

[Documenting functions](#Documenting-functions)

[`\value`](#index-_005cvalue):

[Documenting functions](#Documenting-functions)

[`\var`](#index-_005cvar):

[Marking text](#Marking-text)

[`\verb`](#index-_005cverb):

[Marking text](#Marking-text)

---

A

[`allocVector`](#index-allocVector):

[Allocating storage](#Allocating-storage)

[`AUTHORS`](#index-AUTHORS):

[Package subdirectories](#Package-subdirectories)

---

B

[`bessel_i`](#index-bessel_005fi):

[Mathematical functions](#Mathematical-functions)

[`bessel_i`](#index-bessel_005fi-1):

[Mathematical functions](#Mathematical-functions)

[`bessel_j`](#index-bessel_005fj):

[Mathematical functions](#Mathematical-functions)

[`bessel_j`](#index-bessel_005fj-1):

[Mathematical functions](#Mathematical-functions)

[`bessel_k`](#index-bessel_005fk):

[Mathematical functions](#Mathematical-functions)

[`bessel_k`](#index-bessel_005fk-1):

[Mathematical functions](#Mathematical-functions)

[`bessel_y`](#index-bessel_005fy):

[Mathematical functions](#Mathematical-functions)

[`bessel_y`](#index-bessel_005fy-1):

[Mathematical functions](#Mathematical-functions)

[`beta`](#index-beta):

[Mathematical functions](#Mathematical-functions)

[`beta`](#index-beta-1):

[Mathematical functions](#Mathematical-functions)

[`BLAS_LIBS`](#index-BLAS_005fLIBS):

[Using Makevars](#Using-Makevars)

[`browser`](#index-browser):

[Browsing](#Browsing)

---

C

[`Calloc`](#index-Calloc):

[User-controlled memory](#User_002dcontrolled-memory)

[`CAR`](#index-CAR):

[Calling .External](#Calling-_002eExternal)

[`CDR`](#index-CDR):

[Calling .External](#Calling-_002eExternal)

[`cgmin`](#index-cgmin):

[Optimization](#Optimization)

[`choose`](#index-choose):

[Mathematical functions](#Mathematical-functions)

[`choose`](#index-choose-1):

[Mathematical functions](#Mathematical-functions)

[`CITATION`](#index-CITATION):

[Package subdirectories](#Package-subdirectories)

[`CITATION`](#index-CITATION-1):

[Preparing translations](#Preparing-translations)

[`COPYRIGHTS`](#index-COPYRIGHTS):

[The DESCRIPTION file](#The-DESCRIPTION-file)

[`COPYRIGHTS`](#index-COPYRIGHTS-1):

[Package subdirectories](#Package-subdirectories)

[`cospi`](#index-cospi):

[Numerical Utilities](#Numerical-Utilities)

[`cPsort`](#index-cPsort):

[Utility functions](#Utility-functions)

---

D

[`debug`](#index-debug):

[Debugging R code](#Debugging-R-code)

[`debugger`](#index-debugger):

[Debugging R code](#Debugging-R-code)

[`defineVar`](#index-defineVar):

[Finding and setting variables](#Finding-and-setting-variables)

[`digamma`](#index-digamma):

[Mathematical functions](#Mathematical-functions)

[`digamma`](#index-digamma-1):

[Mathematical functions](#Mathematical-functions)

[`dump.frames`](#index-dump_002eframes):

[Debugging R code](#Debugging-R-code)

[`duplicate`](#index-duplicate):

[Named objects and copying](#Named-objects-and-copying)

[`dyn.load`](#index-dyn_002eload):

[dyn.load and dyn.unload](#dyn_002eload-and-dyn_002eunload)

[`dyn.unload`](#index-dyn_002eunload):

[dyn.load and dyn.unload](#dyn_002eload-and-dyn_002eunload)

---

E

[`expm1`](#index-expm1):

[Numerical Utilities](#Numerical-Utilities)

[`export`](#index-export):

[Specifying imports and exports](#Specifying-imports-and-exports)

[`exportClasses`](#index-exportClasses):

[Namespaces with S4 classes and methods](#Namespaces-with-S4-classes-and-methods)

[`exportClassPattern`](#index-exportClassPattern):

[Namespaces with S4 classes and methods](#Namespaces-with-S4-classes-and-methods)

[`exportMethods`](#index-exportMethods):

[Namespaces with S4 classes and methods](#Namespaces-with-S4-classes-and-methods)

[`exportPattern`](#index-exportPattern):

[Specifying imports and exports](#Specifying-imports-and-exports)

[`exportPattern`](#index-exportPattern-1):

[Namespaces with S4 classes and methods](#Namespaces-with-S4-classes-and-methods)

[`exp_rand`](#index-exp_005frand):

[Random numbers](#Random-numbers)

---

F

[`FALSE`](#index-FALSE):

[Mathematical constants](#Mathematical-constants)

[`findInterval`](#index-findInterval):

[Utility functions](#Utility-functions)

[`findInterval2(double*`](#index-findInterval2_0028double_002a):

[Utility functions](#Utility-functions)

[`findVar`](#index-findVar):

[Finding and setting variables](#Finding-and-setting-variables)

[`FLIBS`](#index-FLIBS):

[Using Makevars](#Using-Makevars)

[`fmax2`](#index-fmax2):

[Numerical Utilities](#Numerical-Utilities)

[`fmin2`](#index-fmin2):

[Numerical Utilities](#Numerical-Utilities)

[`fprec`](#index-fprec):

[Numerical Utilities](#Numerical-Utilities)

[`Free`](#index-Free):

[User-controlled memory](#User_002dcontrolled-memory)

[`fround`](#index-fround):

[Numerical Utilities](#Numerical-Utilities)

[`fsign`](#index-fsign):

[Numerical Utilities](#Numerical-Utilities)

[`ftrunc`](#index-ftrunc):

[Numerical Utilities](#Numerical-Utilities)

---

G

[`gammafn`](#index-gammafn):

[Mathematical functions](#Mathematical-functions)

[`gammafn`](#index-gammafn-1):

[Mathematical functions](#Mathematical-functions)

[`gctorture`](#index-gctorture):

[Using gctorture](#Using-gctorture)

[`getAttrib`](#index-getAttrib):

[Attributes](#Attributes)

[`getCharCE`](#index-getCharCE):

[Character encoding issues](#Character-encoding-issues)

[`GetRNGstate`](#index-GetRNGstate):

[Random numbers](#Random-numbers)

---

I

[`imax2`](#index-imax2):

[Numerical Utilities](#Numerical-Utilities)

[`imin2`](#index-imin2):

[Numerical Utilities](#Numerical-Utilities)

[`import`](#index-import):

[Specifying imports and exports](#Specifying-imports-and-exports)

[`importClassesFrom`](#index-importClassesFrom):

[Namespaces with S4 classes and methods](#Namespaces-with-S4-classes-and-methods)

[`importFrom`](#index-importFrom):

[Specifying imports and exports](#Specifying-imports-and-exports)

[`importMethodsFrom`](#index-importMethodsFrom):

[Namespaces with S4 classes and methods](#Namespaces-with-S4-classes-and-methods)

[`install`](#index-install):

[Attributes](#Attributes)

[`iPsort`](#index-iPsort):

[Utility functions](#Utility-functions)

[`ISNA`](#index-ISNA):

[Missing and special values](#Missing-and-special-values)

[`ISNA`](#index-ISNA-1):

[Missing and IEEE values](#Missing-and-IEEE-values)

[`ISNAN`](#index-ISNAN):

[Missing and special values](#Missing-and-special-values)

[`ISNAN`](#index-ISNAN-1):

[Missing and IEEE values](#Missing-and-IEEE-values)

---

L

[`LAPACK_LIBS`](#index-LAPACK_005fLIBS):

[Using Makevars](#Using-Makevars)

[`lbeta`](#index-lbeta):

[Mathematical functions](#Mathematical-functions)

[`lbeta`](#index-lbeta-1):

[Mathematical functions](#Mathematical-functions)

[`lbfgsb`](#index-lbfgsb):

[Optimization](#Optimization)

[`lchoose`](#index-lchoose):

[Mathematical functions](#Mathematical-functions)

[`lchoose`](#index-lchoose-1):

[Mathematical functions](#Mathematical-functions)

[`lgamma1p`](#index-lgamma1p):

[Numerical Utilities](#Numerical-Utilities)

[`lgammafn`](#index-lgammafn):

[Mathematical functions](#Mathematical-functions)

[`lgammafn`](#index-lgammafn-1):

[Mathematical functions](#Mathematical-functions)

[`library.dynam`](#index-library_002edynam):

[Package subdirectories](#Package-subdirectories)

[`library.dynam`](#index-library_002edynam-1):

[dyn.load and dyn.unload](#dyn_002eload-and-dyn_002eunload)

[`log1p`](#index-log1p):

[Numerical Utilities](#Numerical-Utilities)

[`log1pexp`](#index-log1pexp):

[Numerical Utilities](#Numerical-Utilities)

[`log1pmx`](#index-log1pmx):

[Numerical Utilities](#Numerical-Utilities)

[`logspace_add`](#index-logspace_005fadd):

[Numerical Utilities](#Numerical-Utilities)

[`logspace_sub`](#index-logspace_005fsub):

[Numerical Utilities](#Numerical-Utilities)

[`logspace_sum`](#index-logspace_005fsum):

[Numerical Utilities](#Numerical-Utilities)

---

M

[`mkChar`](#index-mkChar):

[Handling character data](#Handling-character-data)

[`mkCharCE`](#index-mkCharCE):

[Character encoding issues](#Character-encoding-issues)

[`mkCharLen`](#index-mkCharLen):

[Handling character data](#Handling-character-data)

[`mkCharLenCE`](#index-mkCharLenCE):

[Character encoding issues](#Character-encoding-issues)

[`M_E`](#index-M_005fE):

[Mathematical constants](#Mathematical-constants)

[`M_PI`](#index-M_005fPI):

[Mathematical constants](#Mathematical-constants)

---

N

[`NA_REAL`](#index-NA_005fREAL):

[Missing and IEEE values](#Missing-and-IEEE-values)

[`NEWS.Rd`](#index-NEWS_002eRd):

[Package subdirectories](#Package-subdirectories)

[`nmmin`](#index-nmmin):

[Optimization](#Optimization)

[`norm_rand`](#index-norm_005frand):

[Random numbers](#Random-numbers)

---

O

[`OBJECTS`](#index-OBJECTS):

[Using Makevars](#Using-Makevars)

[`OBJECTS`](#index-OBJECTS-1):

[Creating shared objects](#Creating-shared-objects)

---

P

[`pentagamma`](#index-pentagamma):

[Mathematical functions](#Mathematical-functions)

[`pentagamma`](#index-pentagamma-1):

[Mathematical functions](#Mathematical-functions)

[`PKG_CFLAGS`](#index-PKG_005fCFLAGS):

[Creating shared objects](#Creating-shared-objects)

[`PKG_CPPFLAGS`](#index-PKG_005fCPPFLAGS):

[Creating shared objects](#Creating-shared-objects)

[`PKG_CXXFLAGS`](#index-PKG_005fCXXFLAGS):

[Creating shared objects](#Creating-shared-objects)

[`PKG_FCFLAGS`](#index-PKG_005fFCFLAGS):

[Using F9x code](#Using-F9x-code)

[`PKG_FFLAGS`](#index-PKG_005fFFLAGS):

[Creating shared objects](#Creating-shared-objects)

[`PKG_LIBS`](#index-PKG_005fLIBS):

[Creating shared objects](#Creating-shared-objects)

[`PKG_OBJCFLAGS`](#index-PKG_005fOBJCFLAGS):

[Creating shared objects](#Creating-shared-objects)

[`PKG_OBJCXXFLAGS`](#index-PKG_005fOBJCXXFLAGS):

[Creating shared objects](#Creating-shared-objects)

[`prompt`](#index-prompt):

[Rd format](#Rd-format)

[`PROTECT`](#index-PROTECT):

[Garbage Collection](#Garbage-Collection)

[`PROTECT_WITH_INDEX`](#index-PROTECT_005fWITH_005fINDEX):

[Garbage Collection](#Garbage-Collection)

[`psigamma`](#index-psigamma):

[Mathematical functions](#Mathematical-functions)

[`psigamma`](#index-psigamma-1):

[Mathematical functions](#Mathematical-functions)

[`PutRNGstate`](#index-PutRNGstate):

[Random numbers](#Random-numbers)

---

Q

[`qsort3`](#index-qsort3):

[Utility functions](#Utility-functions)

[`qsort4`](#index-qsort4):

[Utility functions](#Utility-functions)

---

R

[`R CMD build`](#index-R-CMD-build):

[Building package tarballs](#Building-package-tarballs)

[`R CMD check`](#index-R-CMD-check):

[Checking packages](#Checking-packages)

[`R CMD config`](#index-R-CMD-config):

[Configure and cleanup](#Configure-and-cleanup)

[`R CMD Rd2pdf`](#index-R-CMD-Rd2pdf):

[Processing documentation files](#Processing-documentation-files)

[`R CMD Rdconv`](#index-R-CMD-Rdconv):

[Processing documentation files](#Processing-documentation-files)

[`R CMD SHLIB`](#index-R-CMD-SHLIB):

[Creating shared objects](#Creating-shared-objects)

[`R CMD Stangle`](#index-R-CMD-Stangle):

[Processing documentation files](#Processing-documentation-files)

[`R CMD Sweave`](#index-R-CMD-Sweave):

[Processing documentation files](#Processing-documentation-files)

[`Rdqagi`](#index-Rdqagi):

[Integration](#Integration)

[`Rdqags`](#index-Rdqags):

[Integration](#Integration)

[`Realloc`](#index-Realloc):

[User-controlled memory](#User_002dcontrolled-memory)

[`recover`](#index-recover):

[Debugging R code](#Debugging-R-code)

[`reEnc`](#index-reEnc):

[Character encoding issues](#Character-encoding-issues)

[`REprintf`](#index-REprintf):

[Printing](#Printing)

[`REPROTECT`](#index-REPROTECT):

[Garbage Collection](#Garbage-Collection)

[`REvprintf`](#index-REvprintf):

[Printing](#Printing)

[`revsort`](#index-revsort):

[Utility functions](#Utility-functions)

[`Riconv`](#index-Riconv):

[Re-encoding](#Re_002dencoding)

[`Riconv_close`](#index-Riconv_005fclose):

[Re-encoding](#Re_002dencoding)

[`Riconv_open`](#index-Riconv_005fopen):

[Re-encoding](#Re_002dencoding)

[`Rprintf`](#index-Rprintf):

[Printing](#Printing)

[`Rprof`](#index-Rprof):

[Profiling R code for speed](#Profiling-R-code-for-speed)

[`Rprof`](#index-Rprof-1):

[Memory statistics from Rprof](#Memory-statistics-from-Rprof)

[`Rprofmem`](#index-Rprofmem):

[Tracking memory allocations](#Tracking-memory-allocations)

[`rPsort`](#index-rPsort):

[Utility functions](#Utility-functions)

[`rsort_with_index`](#index-rsort_005fwith_005findex):

[Utility functions](#Utility-functions)

[`Rvprintf`](#index-Rvprintf):

[Printing](#Printing)

[`R_addhistory`](#index-R_005faddhistory):

[Setting R callbacks](#Setting-R-callbacks)

[`R_alloc`](#index-R_005falloc):

[Transient storage allocation](#Transient-storage-allocation)

[`R_allocLD`](#index-R_005fallocLD):

[Transient storage allocation](#Transient-storage-allocation)

[`R_Busy`](#index-R_005fBusy):

[Setting R callbacks](#Setting-R-callbacks)

[`R_ChooseFile`](#index-R_005fChooseFile):

[Setting R callbacks](#Setting-R-callbacks)

[`R_CleanUp`](#index-R_005fCleanUp):

[Setting R callbacks](#Setting-R-callbacks)

[`R_ClearErrConsole`](#index-R_005fClearErrConsole):

[Setting R callbacks](#Setting-R-callbacks)

[`R_csort`](#index-R_005fcsort):

[Utility functions](#Utility-functions)

[`R_dataentry`](#index-R_005fdataentry):

[Setting R callbacks](#Setting-R-callbacks)

[`R_dataviewer`](#index-R_005fdataviewer):

[Setting R callbacks](#Setting-R-callbacks)

[`R_EditFile`](#index-R_005fEditFile):

[Setting R callbacks](#Setting-R-callbacks)

[`R_EditFiles`](#index-R_005fEditFiles):

[Setting R callbacks](#Setting-R-callbacks)

[`R_ExpandFileName`](#index-R_005fExpandFileName):

[Utility functions](#Utility-functions)

[`R_FINITE`](#index-R_005fFINITE):

[Missing and IEEE values](#Missing-and-IEEE-values)

[`R_FlushConsole`](#index-R_005fFlushConsole):

[Setting R callbacks](#Setting-R-callbacks)

[`R_forceSymbols`](#index-R_005fforceSymbols):

[Registering native routines](#Registering-native-routines)

[`R_GetCCallable`](#index-R_005fGetCCallable):

[Linking to native routines in other packages](#Linking-to-native-routines-in-other-packages)

[`R_GetCurrentSrcref`](#index-R_005fGetCurrentSrcref):

[Accessing source references](#Accessing-source-references)

[`R_GetSrcFilename`](#index-R_005fGetSrcFilename):

[Accessing source references](#Accessing-source-references)

[`R_INLINE`](#index-R_005fINLINE):

[Inlining C functions](#Inlining-C-functions)

[`R_IsNaN`](#index-R_005fIsNaN):

[Missing and IEEE values](#Missing-and-IEEE-values)

[`R_isort`](#index-R_005fisort):

[Utility functions](#Utility-functions)

[`R_LIBRARY_DIR`](#index-R_005fLIBRARY_005fDIR):

[Configure and cleanup](#Configure-and-cleanup)

[`R_loadhistory`](#index-R_005floadhistory):

[Setting R callbacks](#Setting-R-callbacks)

[`R_max_col`](#index-R_005fmax_005fcol):

[Utility functions](#Utility-functions)

[`R_NegInf`](#index-R_005fNegInf):

[Missing and IEEE values](#Missing-and-IEEE-values)

[`R_NewPreciousMSet`](#index-R_005fNewPreciousMSet):

[Garbage Collection](#Garbage-Collection)

[`R_orderVector`](#index-R_005forderVector):

[Utility functions](#Utility-functions)

[`R_orderVector1`](#index-R_005forderVector1):

[Utility functions](#Utility-functions)

[`R_PACKAGE_DIR`](#index-R_005fPACKAGE_005fDIR):

[Configure and cleanup](#Configure-and-cleanup)

[`R_PACKAGE_NAME`](#index-R_005fPACKAGE_005fNAME):

[Configure and cleanup](#Configure-and-cleanup)

[`R_ParseVector`](#index-R_005fParseVector):

[Parsing R code from C](#Parsing-R-code-from-C)

[`R_PosInf`](#index-R_005fPosInf):

[Missing and IEEE values](#Missing-and-IEEE-values)

[`R_pow`](#index-R_005fpow):

[Numerical Utilities](#Numerical-Utilities)

[`R_pow_di`](#index-R_005fpow_005fdi):

[Numerical Utilities](#Numerical-Utilities)

[`R_PreserveInMSet`](#index-R_005fPreserveInMSet):

[Garbage Collection](#Garbage-Collection)

[`R_PreserveObject`](#index-R_005fPreserveObject):

[Garbage Collection](#Garbage-Collection)

[`R_qsort`](#index-R_005fqsort):

[Utility functions](#Utility-functions)

[`R_qsort_I`](#index-R_005fqsort_005fI):

[Utility functions](#Utility-functions)

[`R_qsort_int`](#index-R_005fqsort_005fint):

[Utility functions](#Utility-functions)

[`R_qsort_int_I`](#index-R_005fqsort_005fint_005fI):

[Utility functions](#Utility-functions)

[`R_ReadConsole`](#index-R_005fReadConsole):

[Setting R callbacks](#Setting-R-callbacks)

[`R_RegisterCCallable`](#index-R_005fRegisterCCallable):

[Linking to native routines in other packages](#Linking-to-native-routines-in-other-packages)

[`R_registerRoutines`](#index-R_005fregisterRoutines):

[Registering native routines](#Registering-native-routines)

[`R_ReleaseFromMSet`](#index-R_005fReleaseFromMSet):

[Garbage Collection](#Garbage-Collection)

[`R_ReleaseObject`](#index-R_005fReleaseObject):

[Garbage Collection](#Garbage-Collection)

[`R_ResetConsole`](#index-R_005fResetConsole):

[Setting R callbacks](#Setting-R-callbacks)

[`R_rsort`](#index-R_005frsort):

[Utility functions](#Utility-functions)

[`R_savehistory`](#index-R_005fsavehistory):

[Setting R callbacks](#Setting-R-callbacks)

[`R_selectlist`](#index-R_005fselectlist):

[Setting R callbacks](#Setting-R-callbacks)

[`R_ShowFiles`](#index-R_005fShowFiles):

[Setting R callbacks](#Setting-R-callbacks)

[`R_ShowMessage`](#index-R_005fShowMessage):

[Setting R callbacks](#Setting-R-callbacks)

[`R_Srcref`](#index-R_005fSrcref):

[Accessing source references](#Accessing-source-references)

[`R_Suicide`](#index-R_005fSuicide):

[Setting R callbacks](#Setting-R-callbacks)

[`R_tmpnam`](#index-R_005ftmpnam):

[Utility functions](#Utility-functions)

[`R_tmpnam2`](#index-R_005ftmpnam2):

[Utility functions](#Utility-functions)

[`R_unif_index`](#index-R_005funif_005findex):

[Random numbers](#Random-numbers)

[`R_useDynamicSymbols`](#index-R_005fuseDynamicSymbols):

[Registering native routines](#Registering-native-routines)

[`R_Version`](#index-R_005fVersion):

[Platform and version information](#Platform-and-version-information)

[`R_WriteConsole`](#index-R_005fWriteConsole):

[Setting R callbacks](#Setting-R-callbacks)

[`R_WriteConsoleEx`](#index-R_005fWriteConsoleEx):

[Setting R callbacks](#Setting-R-callbacks)

---

S

[`S3method`](#index-S3method):

[Registering S3 methods](#Registering-S3-methods)

[`SAFE_FFLAGS`](#index-SAFE_005fFFLAGS):

[Using Makevars](#Using-Makevars)

[`samin`](#index-samin):

[Optimization](#Optimization)

[`seed_in`](#index-seed_005fin):

[Random numbers](#Random-numbers)

[`seed_out`](#index-seed_005fout):

[Random numbers](#Random-numbers)

[`setAttrib`](#index-setAttrib):

[Attributes](#Attributes)

[`setVar`](#index-setVar):

[Finding and setting variables](#Finding-and-setting-variables)

[`sign`](#index-sign):

[Numerical Utilities](#Numerical-Utilities)

[`sinpi`](#index-sinpi):

[Numerical Utilities](#Numerical-Utilities)

[`summaryRprof`](#index-summaryRprof):

[Memory statistics from Rprof](#Memory-statistics-from-Rprof)

[`system`](#index-system):

[Operating system access](#Operating-system-access)

[`system.time`](#index-system_002etime):

[Operating system access](#Operating-system-access)

[`system2`](#index-system2):

[Operating system access](#Operating-system-access)

[`S_alloc`](#index-S_005falloc):

[Transient storage allocation](#Transient-storage-allocation)

[`S_realloc`](#index-S_005frealloc):

[Transient storage allocation](#Transient-storage-allocation)

---

T

[`tanpi`](#index-tanpi):

[Numerical Utilities](#Numerical-Utilities)

[`tetragamma`](#index-tetragamma):

[Mathematical functions](#Mathematical-functions)

[`tetragamma`](#index-tetragamma-1):

[Mathematical functions](#Mathematical-functions)

[`trace`](#index-trace):

[Debugging R code](#Debugging-R-code)

[`traceback`](#index-traceback):

[Debugging R code](#Debugging-R-code)

[`tracemem`](#index-tracemem):

[Tracing copies of an object](#Tracing-copies-of-an-object)

[`translateChar`](#index-translateChar):

[Character encoding issues](#Character-encoding-issues)

[`translateCharUTF8`](#index-translateCharUTF8):

[Character encoding issues](#Character-encoding-issues)

[`trigamma`](#index-trigamma):

[Mathematical functions](#Mathematical-functions)

[`trigamma`](#index-trigamma-1):

[Mathematical functions](#Mathematical-functions)

[`TRUE`](#index-TRUE):

[Mathematical constants](#Mathematical-constants)

---

U

[`undebug`](#index-undebug):

[Debugging R code](#Debugging-R-code)

[`unif_rand`](#index-unif_005frand):

[Random numbers](#Random-numbers)

[`UNPROTECT`](#index-UNPROTECT):

[Garbage Collection](#Garbage-Collection)

[`UNPROTECT_PTR`](#index-UNPROTECT_005fPTR):

[Garbage Collection](#Garbage-Collection)

[`untracemem`](#index-untracemem):

[Tracing copies of an object](#Tracing-copies-of-an-object)

[`useDynLib`](#index-useDynLib):

[useDynLib](#useDynLib)

---

V

[`vmaxget`](#index-vmaxget):

[Transient storage allocation](#Transient-storage-allocation)

[`vmaxset`](#index-vmaxset):

[Transient storage allocation](#Transient-storage-allocation)

[`vmmin`](#index-vmmin):

[Optimization](#Optimization)

---

---

Jump to:   [**.**](#Function-and-variable-index_vr_symbol-1){.summary-letter}  
[**\\**](#Function-and-variable-index_vr_symbol-2){.summary-letter}
 \
 [**A**](#Function-and-variable-index_vr_letter-A){.summary-letter}  
[**B**](#Function-and-variable-index_vr_letter-B){.summary-letter}  
[**C**](#Function-and-variable-index_vr_letter-C){.summary-letter}  
[**D**](#Function-and-variable-index_vr_letter-D){.summary-letter}  
[**E**](#Function-and-variable-index_vr_letter-E){.summary-letter}  
[**F**](#Function-and-variable-index_vr_letter-F){.summary-letter}  
[**G**](#Function-and-variable-index_vr_letter-G){.summary-letter}  
[**I**](#Function-and-variable-index_vr_letter-I){.summary-letter}  
[**L**](#Function-and-variable-index_vr_letter-L){.summary-letter}  
[**M**](#Function-and-variable-index_vr_letter-M){.summary-letter}  
[**N**](#Function-and-variable-index_vr_letter-N){.summary-letter}  
[**O**](#Function-and-variable-index_vr_letter-O){.summary-letter}  
[**P**](#Function-and-variable-index_vr_letter-P){.summary-letter}  
[**Q**](#Function-and-variable-index_vr_letter-Q){.summary-letter}  
[**R**](#Function-and-variable-index_vr_letter-R){.summary-letter}  
[**S**](#Function-and-variable-index_vr_letter-S){.summary-letter}  
[**T**](#Function-and-variable-index_vr_letter-T){.summary-letter}  
[**U**](#Function-and-variable-index_vr_letter-U){.summary-letter}  
[**V**](#Function-and-variable-index_vr_letter-V){.summary-letter}

---

---

## Concept index

---

Jump to:   [**.**](#Concept-index_cp_symbol-1){.summary-letter}  
[**\\**](#Concept-index_cp_symbol-2){.summary-letter}
 \
 [**A**](#Concept-index_cp_letter-A){.summary-letter}  
[**B**](#Concept-index_cp_letter-B){.summary-letter}  
[**C**](#Concept-index_cp_letter-C){.summary-letter}  
[**D**](#Concept-index_cp_letter-D){.summary-letter}  
[**E**](#Concept-index_cp_letter-E){.summary-letter}  
[**F**](#Concept-index_cp_letter-F){.summary-letter}  
[**G**](#Concept-index_cp_letter-G){.summary-letter}  
[**H**](#Concept-index_cp_letter-H){.summary-letter}  
[**I**](#Concept-index_cp_letter-I){.summary-letter}  
[**L**](#Concept-index_cp_letter-L){.summary-letter}  
[**M**](#Concept-index_cp_letter-M){.summary-letter}  
[**N**](#Concept-index_cp_letter-N){.summary-letter}  
[**O**](#Concept-index_cp_letter-O){.summary-letter}  
[**P**](#Concept-index_cp_letter-P){.summary-letter}  
[**R**](#Concept-index_cp_letter-R){.summary-letter}  
[**S**](#Concept-index_cp_letter-S){.summary-letter}  
[**T**](#Concept-index_cp_letter-T){.summary-letter}  
[**U**](#Concept-index_cp_letter-U){.summary-letter}  
[**V**](#Concept-index_cp_letter-V){.summary-letter}  
[**W**](#Concept-index_cp_letter-W){.summary-letter}  
[**Z**](#Concept-index_cp_letter-Z){.summary-letter}

---

Index Entry

Section

---

.

[.install_extras file](#index-_002einstall_005fextras-file):

[Writing package vignettes](#Writing-package-vignettes)

[.Rbuildignore file](#index-_002eRbuildignore-file):

[Building package tarballs](#Building-package-tarballs)

[.Rinstignore file](#index-_002eRinstignore-file):

[Package subdirectories](#Package-subdirectories)

---

\\

[\\linkS4class](#index-_005clinkS4class):

[Cross-references](#Cross_002dreferences)

---

A

[Allocating storage](#index-Allocating-storage):

[Allocating storage](#Allocating-storage)

[Attributes](#index-Attributes):

[Attributes](#Attributes)

---

B

[Bessel functions](#index-Bessel-functions):

[Mathematical functions](#Mathematical-functions)

[Beta function](#index-Beta-function):

[Mathematical functions](#Mathematical-functions)

[Building binary packages](#index-Building-binary-packages):

[Building binary packages](#Building-binary-packages)

[Building source packages](#index-Building-source-packages):

[Building package tarballs](#Building-package-tarballs)

---

C

[C++ code, interfacing](#index-C_002b_002b-code_002c-interfacing):

[Interfacing C++ code](#Interfacing-C_002b_002b-code)

[Calling C from Fortran and vice versa](#index-Calling-C-from-Fortran-and-vice-versa):

[Calling C from Fortran and vice versa](#Calling-C-from-Fortran-and-vice-versa)

[Checking packages](#index-Checking-packages):

[Checking packages](#Checking-packages)

[citation](#index-citation):

[Package subdirectories](#Package-subdirectories)

[citation](#index-citation-1):

[Preparing translations](#Preparing-translations)

[Classes](#index-Classes):

[Classes](#Classes)

[Cleanup code](#index-Cleanup-code):

[Condition handling and cleanup code](#Condition-handling-and-cleanup-code)

[cleanup file](#index-cleanup-file):

[Package structure](#Package-structure)

[Condition handling](#index-Condition-handling):

[Condition handling and cleanup code](#Condition-handling-and-cleanup-code)

[conditionals](#index-conditionals):

[Conditional text](#Conditional-text)

[configure file](#index-configure-file):

[Package structure](#Package-structure)

[Copying objects](#index-Copying-objects):

[Named objects and copying](#Named-objects-and-copying)

[CRAN](#index-CRAN):

[Creating R packages](#Creating-R-packages)

[Creating packages](#index-Creating-packages):

[Creating R packages](#Creating-R-packages)

[Creating shared objects](#index-Creating-shared-objects):

[Creating shared objects](#Creating-shared-objects)

[Cross-references in documentation](#index-Cross_002dreferences-in-documentation):

[Cross-references](#Cross_002dreferences)

[cumulative hazard](#index-cumulative-hazard):

[Distribution functions](#Distribution-functions)

---

D

[Debugging](#index-Debugging):

[Debugging compiled code](#Debugging-compiled-code)

[DESCRIPTION file](#index-DESCRIPTION-file):

[The DESCRIPTION file](#The-DESCRIPTION-file)

[Details of R types](#index-Details-of-R-types):

[Details of R types](#Details-of-R-types)

[Distribution functions from C](#index-Distribution-functions-from-C):

[Distribution functions](#Distribution-functions)

[Documentation, writing](#index-Documentation_002c-writing):

[Writing R documentation files](#Writing-R-documentation-files)

[Dynamic loading](#index-Dynamic-loading):

[dyn.load and dyn.unload](#dyn_002eload-and-dyn_002eunload)

[dynamic pages](#index-dynamic-pages):

[Dynamic pages](#Dynamic-pages)

---

E

[Editing Rd files](#index-Editing-Rd-files):

[Editing Rd files](#Editing-Rd-files)

[encoding](#index-encoding):

[Encoding](#Encoding)

[Error handling](#index-Error-handling):

[Condition handling and cleanup code](#Condition-handling-and-cleanup-code)

[Error signaling from C](#index-Error-signaling-from-C):

[Error signaling](#Error-signaling)

[Error signaling from Fortran](#index-Error-signaling-from-Fortran):

[Error signaling from Fortran](#Error-signaling-from-Fortran)

[Evaluating R expressions from C](#index-Evaluating-R-expressions-from-C):

[Evaluating R expressions from C](#Evaluating-R-expressions-from-C)

[external pointer](#index-external-pointer):

[External pointers and weak references](#External-pointers-and-weak-references)

---

F

[Figures in documentation](#index-Figures-in-documentation):

[Figures](#Figures)

[finalizer](#index-finalizer):

[External pointers and weak references](#External-pointers-and-weak-references)

[Finding variables](#index-Finding-variables):

[Finding and setting variables](#Finding-and-setting-variables)

---

G

[Gamma function](#index-Gamma-function):

[Mathematical functions](#Mathematical-functions)

[Garbage collection](#index-Garbage-collection):

[Garbage Collection](#Garbage-Collection)

[Generic functions](#index-Generic-functions):

[Generic functions and methods](#Generic-functions-and-methods)

---

H

[handling character data](#index-handling-character-data):

[Handling character data](#Handling-character-data)

[Handling lists](#index-Handling-lists):

[Handling lists](#Handling-lists)

[Handling R objects in C](#index-Handling-R-objects-in-C):

[Handling R objects in C](#Handling-R-objects-in-C)

---

I

[IEEE special values](#index-IEEE-special-values):

[Missing and special values](#Missing-and-special-values)

[IEEE special values](#index-IEEE-special-values-1):

[Missing and IEEE values](#Missing-and-IEEE-values)

[INDEX file](#index-INDEX-file):

[The INDEX file](#The-INDEX-file)

[Indices](#index-Indices):

[Indices](#Indices)

[Inspecting R objects when debugging](#index-Inspecting-R-objects-when-debugging):

[Inspecting R objects](#Inspecting-R-objects)

[integration](#index-integration):

[Integration](#Integration)

[Interfaces to compiled code](#index-Interfaces-to-compiled-code):

[Interface functions .C and
.Fortran](#Interface-functions-_002eC-and-_002eFortran)

[Interfaces to compiled code](#index-Interfaces-to-compiled-code-1):

[Interface functions .Call and
.External](#Interface-functions-_002eCall-and-_002eExternal)

[Interfacing C++ code](#index-Interfacing-C_002b_002b-code):

[Interfacing C++ code](#Interfacing-C_002b_002b-code)

[Interrupts](#index-Interrupts):

[Allowing interrupts](#Allowing-interrupts)

---

L

[LICENCE file](#index-LICENCE-file):

[Licensing](#Licensing)

[LICENSE file](#index-LICENSE-file):

[Licensing](#Licensing)

[Lists and tables in documentation](#index-Lists-and-tables-in-documentation):

[Lists and tables](#Lists-and-tables)

---

M

[Marking text in documentation](#index-Marking-text-in-documentation):

[Marking text](#Marking-text)

[Mathematics in documentation](#index-Mathematics-in-documentation):

[Mathematics](#Mathematics)

[Memory allocation from C](#index-Memory-allocation-from-C):

[Memory allocation](#Memory-allocation)

[Memory use](#index-Memory-use):

[Profiling R code for memory use](#Profiling-R-code-for-memory-use)

[Method functions](#index-Method-functions):

[Generic functions and methods](#Generic-functions-and-methods)

[Missing values](#index-Missing-values):

[Missing and special values](#Missing-and-special-values)

[Missing values](#index-Missing-values-1):

[Missing and IEEE values](#Missing-and-IEEE-values)

---

N

[namespaces](#index-namespaces):

[Package namespaces](#Package-namespaces)

[news](#index-news):

[Package subdirectories](#Package-subdirectories)

[Numerical analysis subroutines from C](#index-Numerical-analysis-subroutines-from-C):

[Numerical analysis subroutines](#Numerical-analysis-subroutines)

[Numerical derivatives](#index-Numerical-derivatives):

[Calculating numerical derivatives](#Calculating-numerical-derivatives)

---

O

[OpenMP](#index-OpenMP):

[OpenMP support](#OpenMP-support)

[OpenMP](#index-OpenMP-1):

[Platform and version information](#Platform-and-version-information)

[Operating system access](#index-Operating-system-access):

[Operating system access](#Operating-system-access)

[optimization](#index-optimization):

[Optimization](#Optimization)

---

P

[Package builder](#index-Package-builder):

[Building package tarballs](#Building-package-tarballs)

[Package structure](#index-Package-structure):

[Package structure](#Package-structure)

[Package subdirectories](#index-Package-subdirectories):

[Package subdirectories](#Package-subdirectories)

[Packages](#index-Packages):

[Creating R packages](#Creating-R-packages)

[Parsing R code from C](#index-Parsing-R-code-from-C):

[Parsing R code from C](#Parsing-R-code-from-C)

[Platform-specific documentation](#index-Platform_002dspecific-documentation):

[Platform-specific sections](#Platform_002dspecific-sections)

[Printing from C](#index-Printing-from-C):

[Printing](#Printing)

[Printing from Fortran](#index-Printing-from-Fortran):

[Printing from Fortran](#Printing-from-Fortran)

[Processing Rd format](#index-Processing-Rd-format):

[Processing documentation files](#Processing-documentation-files)

[Profiling](#index-Profiling):

[Profiling R code for speed](#Profiling-R-code-for-speed)

[Profiling](#index-Profiling-1):

[Profiling R code for memory use](#Profiling-R-code-for-memory-use)

[Profiling](#index-Profiling-2):

[Profiling compiled code](#Profiling-compiled-code)

---

R

[Random numbers in C](#index-Random-numbers-in-C):

[Random numbers](#Random-numbers)

[Random numbers in C](#index-Random-numbers-in-C-1):

[Distribution functions](#Distribution-functions)

[Random numbers in Fortran](#index-Random-numbers-in-Fortran):

[Calling C from Fortran and vice versa](#Calling-C-from-Fortran-and-vice-versa)

[Registering native routines](#index-Registering-native-routines):

[Registering native routines](#Registering-native-routines)

---

S

[Setting variables](#index-Setting-variables):

[Finding and setting variables](#Finding-and-setting-variables)

[Sort functions from C](#index-Sort-functions-from-C):

[Utility functions](#Utility-functions)

[Sweave](#index-Sweave):

[Writing package vignettes](#Writing-package-vignettes)

---

T

[tarballs](#index-tarballs):

[Building package tarballs](#Building-package-tarballs)

[Tidying R code](#index-Tidying-R-code):

[Tidying R code](#Tidying-R-code)

---

U

[user-defined macros](#index-user_002ddefined-macros):

[User-defined macros](#User_002ddefined-macros)

---

V

[Version information from C](#index-Version-information-from-C):

[Platform and version information](#Platform-and-version-information)

[vignettes](#index-vignettes):

[Writing package vignettes](#Writing-package-vignettes)

[Visibility](#index-Visibility):

[Controlling visibility](#Controlling-visibility)

---

W

[weak reference](#index-weak-reference):

[External pointers and weak references](#External-pointers-and-weak-references)

---

Z

[Zero-finding](#index-Zero_002dfinding):

[Zero-finding](#Zero_002dfinding)

---

---

Jump to:   [**.**](#Concept-index_cp_symbol-1){.summary-letter}  
[**\\**](#Concept-index_cp_symbol-2){.summary-letter}
 \
 [**A**](#Concept-index_cp_letter-A){.summary-letter}  
[**B**](#Concept-index_cp_letter-B){.summary-letter}  
[**C**](#Concept-index_cp_letter-C){.summary-letter}  
[**D**](#Concept-index_cp_letter-D){.summary-letter}  
[**E**](#Concept-index_cp_letter-E){.summary-letter}  
[**F**](#Concept-index_cp_letter-F){.summary-letter}  
[**G**](#Concept-index_cp_letter-G){.summary-letter}  
[**H**](#Concept-index_cp_letter-H){.summary-letter}  
[**I**](#Concept-index_cp_letter-I){.summary-letter}  
[**L**](#Concept-index_cp_letter-L){.summary-letter}  
[**M**](#Concept-index_cp_letter-M){.summary-letter}  
[**N**](#Concept-index_cp_letter-N){.summary-letter}  
[**O**](#Concept-index_cp_letter-O){.summary-letter}  
[**P**](#Concept-index_cp_letter-P){.summary-letter}  
[**R**](#Concept-index_cp_letter-R){.summary-letter}  
[**S**](#Concept-index_cp_letter-S){.summary-letter}  
[**T**](#Concept-index_cp_letter-T){.summary-letter}  
[**U**](#Concept-index_cp_letter-U){.summary-letter}  
[**V**](#Concept-index_cp_letter-V){.summary-letter}  
[**W**](#Concept-index_cp_letter-W){.summary-letter}  
[**Z**](#Concept-index_cp_letter-Z){.summary-letter}

---

---

#### Footnotes

[(1)](#DOCF1)

although this is a persistent mis-usage. It seems to stem from S, whose
analogues of R's packages were officially known as _library sections_
and later as _chapters_, but almost always referred to as _libraries_.

[(2)](#DOCF2)

This seems to be commonly used for a file in 'markdown' format. Be aware
that most users of R will not know that, nor know how to view such a
file: platforms such as macOS and Windows do not have a default viewer
set in their file associations. The CRAN package web pages render such
files in HTML: the converter used expects the file to be encoded in
UTF-8.

[(3)](#DOCF3)

currently, top-level files `.Rbuildignore` and
`.Rinstignore`, and `vignettes/.install_extras`.

[(4)](#DOCF4)

false positives are possible, but only a handful have been seen so far.

[(5)](#DOCF5)

at least if this is done in a locale which matches the package encoding.

[(6)](#DOCF6)

and required by CRAN, so checked by `R CMD check --as-cran`.

[(7)](#DOCF7)

But it is checked for Open Source packages by `R CMD check --as-cran`.

[(8)](#DOCF8)

Duplicate definitions may trigger a warning: see [User-defined macros](#User_002ddefined-macros).

[(9)](#DOCF9)

`bug.report` will try to extract an email address from a `Contact` field
if there is no `BugReports` field.

[(10)](#DOCF10)

CRAN expands them to e.g. `GPL-2 | GPL-3`.

[(11)](#DOCF11)

even one wrapped in `\donttest`.

[(12)](#DOCF12)

This includes all packages directly called by `library` and `require`
calls, as well as data obtained _via_
`data(theirdata, package = "somepkg")` calls: `R CMD check` will warn
about all of these. But there are subtler uses which it may not detect:
e.g. if package A uses package B and makes use of functionality in
package B which uses package C which package B suggests or enhances,
then package C needs to be in the '`Suggests`' list for package
A. Nor will undeclared uses in included files be reported, nor
unconditional uses of packages listed under '`Enhances`'.
`R CMD check --as-cran` will detect more of the subtler uses, especially
for re-building of vignettes as from R 3.5.0.

[(13)](#DOCF13)

Extensions `.S` and `.s` arise from code originally
written for S(-PLUS), but are commonly used for assembler code.
Extension `.q` was used for S, which at one time was
tentatively called QPE.

[(14)](#DOCF14)

but they should be in the encoding declared in the
`DESCRIPTION` file.

[(15)](#DOCF15)

This is true for OSes which implement the '`C`' locale:
Windows' idea of the '`C`' locale uses the WinAnsi charset.

[(16)](#DOCF16)

More precisely, they can contain the English alphanumeric characters and
the symbols '`$ - _ . + ! ' ( ) , ; = &`'.

[(17)](#DOCF17)

either or both of which may not be supported on particular platforms

[(18)](#DOCF18)

Using `.hpp` is not guaranteed to be portable.

[(19)](#DOCF19)

There is also '`__APPLE_CC__`', but that indicates a compiler
with Apple-specific features, not the OS. It is used in
`Rinlinedfuns.h`.

[(20)](#DOCF20)

the POSIX terminology, called 'make variables' by GNU make.

[(21)](#DOCF21)

The best way to generate such a file is to copy the `.Rout`
from a successful run of `R CMD check`. If you want to generate it
separately, do run R with options `--vanilla --slave` and with
environment variable `LANGUAGE=en` set to get messages in English. Be
careful not to use output with the option `--timings` (and note
that `--as-cran` sets it).

[(22)](#DOCF22)

e.g. <https://tools.ietf.org/html/rfc4180>.

[(23)](#DOCF23)

People who have trouble with case are advised to use `.rda` as
a common error is to refer to `abc.RData` as
`abc.Rdata`!

[(24)](#DOCF24)

The script should only assume a POSIX-compliant `/bin/sh` -- see
<http://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html>.
In particular `bash` extensions must not be used, and not all R
platforms have a `bash` command, let alone one at `/bin/bash`.
All known shells used with R support the use of backticks, but not all
support '`$(cmd)`'. However, real-world shells are not fully
POSIX-compliant and omissions and idiosyncrasies need to be worked
around---which Autoconf will do for you. Arithmetic expansion is a known
issue: see
<https://www.gnu.org/software/autoconf/manual/autoconf.html#Portable-Shell>
for this and others. Some checks can be done by the `checkbashisms` Perl
script at <https://sourceforge.net/projects/checkbaskisms/files>, also
available in most Linux distributions in a package named either
'`devscripts`' or '`devscripts-checkbashisms`'.

[(25)](#DOCF25)

but it is available on the machines used to produce the CRAN binary
packages.

[(26)](#DOCF26)

but not all projects get this right when only a static library is
installed, so it is often necessary to try in turn `pkg-config --libs`
and `pkg-config --static --libs`.

[(27)](#DOCF27)

a decade ago Autoconf used `configure.in`: this is still
accepted but should be renamed and `autoreconf` as used by
`R CMD check --as-cran` will report as such.

[(28)](#DOCF28)

in POSIX parlance: GNU `make` calls these 'make variables'.

[(29)](#DOCF29)

at least on Unix-alikes: the Windows build currently resolves such
dependencies to a static Fortran library when `Rblas.dll` is
built.

[(30)](#DOCF30)

<http://www.openmp.org/>, <https://en.wikipedia.org/wiki/OpenMP>,
<https://computing.llnl.gov/tutorials/openMP/>

[(31)](#DOCF31)

Default builds of `clang` 3.8.0 and later have support for OpenMP, but
the `libomp` run-time library may not be installed.

[(32)](#DOCF32)

In most implementations the `_OPENMP` macro has value a date which can
be mapped to an OpenMP version: for example, value `201307` is the date
of version 4.0 (July 2013). However this may be used to denote the
latest version which is partially supported, not that which is fully
implemented.

[(33)](#DOCF33)

as did the GCC-based Apple implementation, but not the Intel/LLVM OpenMP
runtime on macOS.

[(34)](#DOCF34)

Windows default, not MinGW-w64 default.

[(35)](#DOCF35)

Which it was at the time of writing with GCC, Oracle, Intel and Clang
compilers. The count may include the thread running the main process.

[(36)](#DOCF36)

Be careful not to declare `nthreads` as `const int`: the Oracle compiler
requires it to be 'an lvalue'.

[(37)](#DOCF37)

some Windows toolchains had the typo '`_REENTRANCE`' instead.

[(38)](#DOCF38)

A few OSes (AIX, IRIX, Windows) do not need special flags for such code,
but most do---although compilers will often generate PIC code when not
asked to do so.

[(39)](#DOCF39)

The changes are linked from
<https://isocpp.org/std/standing-documents/sd-6-sg10-feature-test-recommendations>.

[(40)](#DOCF40)

Values `199711`, `201103L` and `201402L` are most commonly used for
C++98, C++11 and C++14 respectively, but some compilers set `1L`. The
official value for C++17 is `201703L` but some compiler versions have
smaller values so a test of `__cplusplus > 201402L` is safer.

[(41)](#DOCF41)

version 3.6.0 except on Windows.

[(42)](#DOCF42)

allowing 'GNU extensions', but if possible excluding C++14 features.

[(43)](#DOCF43)

For details of these and related macros, see file `config.site`
in the R sources.

[(44)](#DOCF44)

As from R 3.4.0, `configure` attempts to supply a C++14 compiler only if
explicitly requested. However, earlier versions of R will use the
default C++14 mode of `g++` 6 and later.

[(45)](#DOCF45)

See
<https://isocpp.org/std/standing-documents/sd-6-sg10-feature-test-recommendations>
or <http://en.cppreference.com/w/cpp/experimental/feature_test>. It
seems a reasonable assumption that any compiler promising some C++14
conformance will provide these---e.g. `g++` 4.9.x did but 4.8.5 did not.

[(46)](#DOCF46)

On systems which use sub-architectures, architecture-specific versions
such as `~/.R/check.Renviron.i386` take precedence.

[(47)](#DOCF47)

A suitable `file.exe` is part of the Windows toolset: it checks for
`gfile` if a suitable `file` is not found: the latter is available in
the OpenCSW collection for Solaris at <http://www.opencsw.org>. The
source repository is <ftp://ftp.astron.com/pub/file/>.

[(48)](#DOCF48)

An exception is made for subdirectories with names starting
'`win`' or '`Win`'.

[(49)](#DOCF49)

on most other platforms such runtime libraries are dynamic, but static
libraries are currently used on Windows because the toolchain is not a
standard part of the OS.

[(50)](#DOCF50)

or if option `--use-valgrind` is used or environment variable
`_R_CHECK_ALWAYS_LOG_VIGNETTE_OUTPUT_` is set to a true value or if
there are differences from a target output file

[(51)](#DOCF51)

For example, in early 2014
[**gdata**](https://CRAN.R-project.org/package=gdata) declared
'`Imports: gtools`' and
[**gtools**](https://CRAN.R-project.org/package=gtools) declared
'`Imports: gdata`'.

[(52)](#DOCF52)

loading, examples, tests, running vignette code

[(53)](#DOCF53)

called `CVS` or `.svn` or `.arch-ids` or
`.bzr` or `.git` (but not files called
`.git`) or `.hg`.

[(54)](#DOCF54)

called `.metadata`.

[(55)](#DOCF55)

which is an error: GNU make uses `GNUmakefile`.

[(56)](#DOCF56)

and to avoid problems with case-insensitive file systems, lower-case
versions of all these extensions.

[(57)](#DOCF57)

unless inhibited by using '`BuildVignettes: no`' in the
`DESCRIPTION` file.

[(58)](#DOCF58)

provided the conditions of the package's license are met: many,
including CRAN, see the omission of source components as incompatible
with an Open Source license.

[(59)](#DOCF59)

`R_HOME/bin` is prepended to the `PATH` so that references to `R` or
`Rscript` in the `Makefile` do make use of the currently
running version of R.

[(60)](#DOCF60)

Note that lazy-loaded datasets are _not_ in the package's namespace so
need to be accessed _via_ `::`, e.g. `survival::survexp.us`.

[(61)](#DOCF61)

they will be called with two unnamed arguments, in that order.

[(62)](#DOCF62)

NB: this will only be read in all versions of R if the package contains
R code in a `R` directory.

[(63)](#DOCF63)

Note that this is the basename of the shared object, and the appropriate
extension (`.so` or `.dll`) will be added.

[(64)](#DOCF64)

This defaults to the same pattern as `exportPattern`: use something like
`exportClassPattern("^$")` to override this.

[(65)](#DOCF65)

if it does, there will be opaque warnings about replacing imports if the
classes/methods are also imported.

[(66)](#DOCF66)

People use `dev.new()` to open a device at a particular size: that is
not portable but using `dev.new(noRStudioGD = TRUE)` helps.

[(67)](#DOCF67)

Solaris `make` does not accept CRLF-terminated Makefiles; Solaris warns
about and some other `make`s ignore incomplete final lines.

[(68)](#DOCF68)

This was apparently introduced in SunOS 4, and is available elsewhere
_provided_ it is surrounded by spaces.

[(69)](#DOCF69)

GNU make, BSD make and other variants of `pmake` in FreeBSD, NetBSD and
formerly in macOS, AT&T make as implemented on Solaris and 'Distributed
Make' (`dmake`), part of Oracle Developer Studio and available in other
versions including from Apache OpenOffice.

[(70)](#DOCF70)

For example, `test` options `-a` and `-e` are not
portable, and not supported in the AT&T Bourne shell used on Solaris
10/11, even though they are in the POSIX standard. Nor does Solaris
support '`$(cmd)`'.

[(71)](#DOCF71)

<http://fortranwiki.org/fortran/show/Modernizing+Old+Fortran> may help
explain some of the warnings from `gfortran -Wall -pedantic`.

[(72)](#DOCF72)

See <http://people.ds.cam.ac.uk/nmm1/fortran/paper_07.pdf>.

[(73)](#DOCF73)

These are optional because the corresponding types are, but must be
provided if the types are.

[(74)](#DOCF74)

but note that `long long` is not a standard C++98 type, and C++
compilers for earlier versions of R set up for strict C++98 conformance
will reject it. C++11 (the default since R 3.6.2) includes `long long`.

[(75)](#DOCF75)

or where supported the variants `_Exit` and `_exit`.

[(76)](#DOCF76)

This and `srandom` are in any case not portable. They are in POSIX but
not in the C99 standard, and not available on Windows.

[(77)](#DOCF77)

in `libselinux`.

[(78)](#DOCF78)

At least Linux and Windows, but not macOS.

[(79)](#DOCF79)

except perhaps the simplest kind as used by `download.file()` in
non-interactive use.

[(80)](#DOCF80)

Whereas the GNU linker reorders so `-L` options are processed
first, the Solaris one does not.

[(81)](#DOCF81)

some versions of macOS did not.

[(82)](#DOCF82)

If a Java interpreter is required directly (not _via_
[**rJava**](https://CRAN.R-project.org/package=rJava)) this must be
declared and its presence tested like any other external command.

[(83)](#DOCF83)

For example, the ability to handle '`https://`' URLs, which
even the build in some major Linux distributions in 2018 did not
possess. Further, Linux and macOS builds from late 2017 with
'`https://`' support were unable to download from some sites
using or redirecting to '`https://`' URLs.

[(84)](#DOCF84)

Not doing so is the default on Windows, overridden for the R
executables. It is also the default on some Solaris compilers.

[(85)](#DOCF85)

These are not needed for the default compiler settings on
'`x86_64`' but are likely to be needed on '`ix86`'.

[(86)](#DOCF86)

Select 'Save as', and select 'Reduce file size' from the 'Quartz filter'
menu': this can be accessed in other ways, for example by Automator.

[(87)](#DOCF87)

except perhaps some special characters such as backslash and hash which
may be taken over for currency symbols.

[(88)](#DOCF88)

Typically on a Unix-alike this is done by telling `fontconfig` where to
find suitable fonts to select glyphs from.

[(89)](#DOCF89)

which it is on all known platforms

[(90)](#DOCF90)

For C++98 this is only possible since R 3.5.0, for C++11 since R 3.1.0.

[(91)](#DOCF91)

This is seen on Linux, Solaris and FreeBSD, although each has other ways
to turn on all extensions, e.g. defining `_GNU_SOURCE`, `__EXTENSIONS__`
or `_BSD_SOURCE`: the GCC compilers by default define `_GNU_SOURCE`
unless a strict standard such as `-std=c99` is used. On macOS
extensions are declared unless one of these macros is given too small a
value.

[(92)](#DOCF92)

Solaris 10 does not recognize this value of `_POSIX_C_SOURCE`, nor
values of `_XOPEN_SOURCE` beyond 600 (700 corresponds to POSIX 2008).
Further, the value of 500 is not allowed in C99 mode, R's default for C
code.

[(93)](#DOCF93)

often taken from the toolchain's headers.

[(94)](#DOCF94)

also part of C++11 and later.

[(95)](#DOCF95)

There is a portable way to do this in Fortran 2003 (`ieee_is_nan()` in
module `ieee_arithmetic`), but ironically that is not supported in the
commonly-used versions 4.x of GNU Fortran. A pretty robust alternative
is to test `if(my_var /= my_var)`.

[(96)](#DOCF96)

which often is the same as the header included by the C compiler, but
some compilers have wrappers for some of the C headers.

[(97)](#DOCF97)

including `EAX`, `EBP`, `EBX`, `ECX`, `EDI`,`EDX`, `EFL`, `EIP`, `ESI`
and `ESP` .

[(98)](#DOCF98)

<https://stackoverflow.com/questions/32739018/a-replacement-for-stdbind2nd>

[(99)](#DOCF99)

it is allowed but ignored in system headers.

[(100)](#DOCF100)

In principle this could depend on the OS, but has been checked on Linux
and macOS.

[(101)](#DOCF101)

e.g. `\alias`, `\keyword` and `\note` sections.

[(102)](#DOCF102)

There can be exceptions: for example `Rd` files are not allowed
to start with a dot, and have to be uniquely named on a case-insensitive
file system.

[(103)](#DOCF103)

in the current locale, and with special treatment for LaTeX special
characters and with any '`pkgname-package`' topic moved to the
top of the list.

[(104)](#DOCF104)

Text between or after list items is discouraged.

[(105)](#DOCF105)

as defined by the R function `trimws`.

[(106)](#DOCF106)

Currently it is rendered differently only in HTML conversions, and LaTeX
conversion outside '`\usage`' and '`\examples`'
environments.

[(107)](#DOCF107)

a common example in CRAN packages is `\link[mgcv]{gam}`.

[(108)](#DOCF108)

There is only a fine distinction between `\dots` and `\ldots`. It is
technically incorrect to use `\ldots` in code blocks and
`tools::checkRd` will warn about this---on the other hand the current
converters treat them the same way in code blocks, and elsewhere apart
from the small distinction between the two in LaTeX.

[(109)](#DOCF109)

See the examples section in the file `Paren.Rd` for an example.

[(110)](#DOCF110)

R 2.9.0 added support for UTF-8 Cyrillic characters in LaTeX, but on
some OSes this will need Cyrillic support added to LaTeX, so environment
variable `_R_CYRILLIC_TEX_` may need to be set to a non-empty value to
enable this.

[(111)](#DOCF111)

R has to be built to enable this, but the option
`--enable-R-profiling` is the default.

[(112)](#DOCF112)

For Unix-alikes these are intervals of CPU time, and for Windows of
elapsed time.

[(113)](#DOCF113)

With the exceptions of the commands listed below: an object of such a
name can be printed _via_ an explicit call to `print`.

[(114)](#DOCF114)

Those in some numeric, logical, integer, raw, complex vectors and in
memory allocated by `R_alloc`.

[(115)](#DOCF115)

including using the data sections of R vectors after they are freed.

[(116)](#DOCF116)

small fixed-size arrays by default in `gfortran`, for example.

[(117)](#DOCF117)

currently on Linux and macOS (including the builds from Xcode 7 and
later), with some support for Solaris. On some platforms the runtime
library, **libasan**, needs to be installed separately, and for checking
C++ you may also need **libubsan**.

[(118)](#DOCF118)

see
<http://llvm.org/devmtg/2014-04/PDFs/LightningTalks/EuroLLVM%202014%20--%20container%20overflow.pdf>.

[(119)](#DOCF119)

part of the LLVM project and in distributed in `llvm` RPMs and `.deb`s
on Linux. It is not currently shipped by Apple.

[(120)](#DOCF120)

as Ubuntu has been said to do.

[(121)](#DOCF121)

installed on some Linux systems as `asan_symbolize`, and obtainable from
<https://llvm.org/svn/llvm-project/compiler-rt/trunk/lib/asan/scripts/asan_symbolize.py>:
it makes use of `llvm-symbolizer` if available.

[(122)](#DOCF122)

including `gcc` 7.1 and `clang` 4.0.0: for `gcc` it is implied by
`-fsanitize=address`.

[(123)](#DOCF123)

for example, X11/GL libraries on Linux, seen when checking package
[**rgl**](https://CRAN.R-project.org/package=rgl) and some others using
it---a workaround is to set environment variable `RGL_USE_NULL=true`.

[(124)](#DOCF124)

On some platforms the runtime library, **libubsan**, needs to be
installed separately.

[(125)](#DOCF125)

but works better if inlining and frame pointer optimizations are
disabled.

[(126)](#DOCF126)

possibly after some platform-specific translation, e.g. adding leading
or trailing underscores.

[(127)](#DOCF127)

Note that this is then not checked for over-runs by option
`CBoundsCheck = TRUE`.

[(128)](#DOCF128)

Strictly this is OS-specific, but no exceptions have been seen for many
years.

[(129)](#DOCF129)

For calls from within a namespace the search is confined to the DLL
loaded for that package.

[(130)](#DOCF130)

For unregistered entry points the OS's `dlsym` routine is used to find
addresses. Its performance varies considerably by OS and even in the
best case it will need to search a much larger symbol table than, say,
the table of `.Call` entry points.

[(131)](#DOCF131)

Because it is a standard package, one would need to rename it before
attempting to reproduce the account here.

[(132)](#DOCF132)

This was added on 2019-05-09, just after release as 9.1.

[(133)](#DOCF133)

whether or not '`LinkingTo`' is used.

[(134)](#DOCF134)

so there needs to be a corresponding `import` or `importFrom` entry in
the `NAMESPACE` file.

[(135)](#DOCF135)

Even including C system headers in such a block has caused compilation
errors.

[(136)](#DOCF136)

<https://en.wikipedia.org/wiki/Application_binary_interface>.

[(137)](#DOCF137)

For example, '`_GLIBCXX_USE_CXX11_ABI`' in `g++` 5.1 and later:
<https://gcc.gnu.org/onlinedocs/libstdc++/manual/using_dual_abi.html>.

[(138)](#DOCF138)

`dyld` on macOS, and `DYLD_LIBRARY_PATHS` below.

[(139)](#DOCF139)

That is, similar to those defined in S version 4 from the 1990s: these
are not kept up to date and are not recommended for new projects.

[(140)](#DOCF140)

see [The R API](#The-R-API): note that these are not all part of the
API.

[(141)](#DOCF141)

SEXP is an acronym for *S*imple *EXP*ression, common in LISP-like
language syntaxes.

[(142)](#DOCF142)

If no coercion was required, `coerceVector` would have passed the old
object through unchanged.

[(143)](#DOCF143)

You can assign a _copy_ of the object in the environment frame `rho`
using `defineVar(symbol, duplicate(value), rho)`).

[(144)](#DOCF144)

see [Character encoding issues](#Character-encoding-issues) for why this
might not be what is required.

[(145)](#DOCF145)

This is only guaranteed to show the current interface: it is liable to
change.

[(146)](#DOCF146)

Known problems are redefining `LENGTH`, `error`, `length`, `vector` and
`warning`

[(147)](#DOCF147)

also part of C++11.

[(148)](#DOCF148)

The '`F77_`' in the names is historical and dates back to usage
in S.

[(149)](#DOCF149)

These started to be implemented in compilers _ca_ 2007, e.g. in
`gfortran` 4.3.

[(150)](#DOCF150)

It is an optional C11 extension.

[(151)](#DOCF151)

but see the second paragraph of see [Portable C and C++ code](#Portable-C-and-C_002b_002b-code).

[(152)](#DOCF152)

<https://en.wikipedia.org/wiki/Endianness>.

[(153)](#DOCF153)

It is defined by the Intel compilers, but also hides unsatisfied
references and so cannot be used with R. It is not supported by the AIX
nor Solaris compilers.

[(154)](#DOCF154)

As from R 3.5.2: This applies to the compiler for the default C++
dialect (currently normally C++11) and not necessarily to other
dialects.

[(155)](#DOCF155)

'`F77_VISIBILITY`' was used prior to R 3.6.0 and is still
available (but deprecated). In some cases the Fortran compilers accept
the flag but do not actually hide their symbols.

[(156)](#DOCF156)

In the parlance of macOS this is a _dynamic_ library, and is the normal
way to build R on that platform.

[(157)](#DOCF157)

but these are not part of the automated test procedures and so little
tested.

[(158)](#DOCF158)

At least according to POSIX 2004 and later. Earlier standards prescribed
`sys/time.h`: `R_ext/eventloop.h` will include it if
`HAVE_SYS_TIME_H` is defined.

[(159)](#DOCF159)

at least on platforms where the values are available, that is having
`getrlimit` and on Linux or having `sysctl` supporting `KERN_USRSTACK`,
including FreeBSD and OS X.

[(160)](#DOCF160)

An attempt to use only threads in the late 1990s failed to work
correctly under Windows 95, the predominant version of Windows at that
time.

---
