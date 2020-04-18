7 System and foreign language interfaces

---

---

• [Operating system access](#Operating-system-access)     
 • [Foreign language interfaces](#Foreign-language-interfaces)     
 • [.Internal and .Primitive](#g_t_002eInternal-and-_002ePrimitive)

---

---

### 7.1 Operating system access

Access to the operating system shell is via the R function `system`.
The details will differ by platform (see the on-line
help), and about all that can safely be assumed is that the first
argument will be a string `command` that will be passed for execution
(not necessarily by a shell) and the second argument will be `internal`
which if true will collect the output of the command into an R character
vector.

The functions `system.time` and `proc.time`
are available for timing (although the
information available may be limited on non-Unix-like platforms).

Information from the operating system
environment can be accessed and manipulated with

> ---
>
> `Sys.getenv` OS environment variables
> `Sys.putenv`  
>  `Sys.getlocale` System locale
> `Sys.putlocale`  
>  `Sys.localeconv`  
>  `Sys.time` Current time
> `Sys.timezone` Time zone
>
> ---

A uniform set of file access functions is provided on all platforms:

> ---
>
> `file.access` Ascertain File Accessibility
> `file.append` Concatenate files
> `file.choose` Prompt user for file name
> `file.copy` Copy files
> `file.create` Create or truncate a files
> `file.exists` Test for existence
> `file.info` Miscellaneous file information
> `file.remove` remove files
> `file.rename` rename files
> `file.show` Display a text file
> `unlink` Remove files or directories.
>
> ---

There are also functions for manipulating file names and paths in a
platform-independent way.

> ---
>
> `basename` File name without directory
> `dirname` Directory name
> `file.path` Construct path to file
> `path.expand` Expand `~` in Unix path
>
> ---

---

### 7.2 Foreign language interfaces

See [System and foreign language interfaces](./R-exts.html#System-and-foreign-language-interfaces) in
Writing R Extensions for the details of adding functionality to R via
compiled code.

Functions `.C` and `.Fortran` provide a standard interface to compiled
code that has been linked into R, either at build time or via
`dyn.load`. They are primarily intended for compiled **C** and FORTRAN
code respectively, but the `.C` function can be used with other
languages which can generate C interfaces, for example C++.

Functions `.Call` and `.External` provide interfaces which allow
compiled code (primarily compiled **C** code) to manipulate R objects.

---

### 7.3 .Internal and .Primitive

The `.Internal` and `.Primitive` interfaces are used to call **C** code
compiled into R at build time. See [.Internal vs
.Primitive](./R-ints.html#g_t_002eInternal-vs-_002ePrimitive) in R
Internals.

---
