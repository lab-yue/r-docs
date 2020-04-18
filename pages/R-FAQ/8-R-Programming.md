# 8 R Programming

---

---

• [How should I write summary methods?](#How-should-I-write-summary-methods_003f)     
 • [How can I debug dynamically loaded code?](#How-can-I-debug-dynamically-loaded-code_003f)     
 • [How can I inspect R objects when debugging?](#How-can-I-inspect-R-objects-when-debugging_003f)     
 • [How can I change compilation flags?](#How-can-I-change-compilation-flags_003f)     
 • [How can I debug S4 methods?](#How-can-I-debug-S4-methods_003f)

---

---

### 8.1 How should I write summary methods?

Suppose you want to provide a summary method for class `"foo"`. Then
`summary.foo()` should not print anything, but return an object of class
`"summary.foo"`, _and_ you should write a method `print.summary.foo()`
which nicely prints the summary information and invisibly returns its
object. This approach is preferred over having `summary.foo()` print
summary information and return something useful, as sometimes you need
to grab something computed by `summary()` inside a function or similar.
In such cases you don't want anything printed.

---

### 8.2 How can I debug dynamically loaded code?

Roughly speaking, you need to start R inside the debugger, load the
code, send an interrupt, and then set the required breakpoints.

See [Finding entry points in dynamically loaded code](./R-exts.html#Finding-entry-points) in Writing R Extensions.

---

### 8.3 How can I inspect R objects when debugging?

The most convenient way is to call `R_PV` from the symbolic debugger.

See [Inspecting R objects when debugging](./R-exts.html#Inspecting-R-objects) in Writing R Extensions.

---

### 8.4 How can I change compilation flags?

Suppose you have C code file for dynloading into R, but you want to use
`R CMD SHLIB` with compilation flags other than the default ones (which
were determined when R was built).

Starting with R 2.1.0, users can provide personal Makevars configuration
files in `$HOME/.R` to override the default flags. See [Add-on packages](./R-admin.html#Add_002don-packages) in R Installation and
Administration.

For earlier versions of R, you could change the file
`R_HOME/etc/Makeconf` to reflect your preferences, or (at least
for systems using GNU Make) override them by the environment variable
`MAKEFLAGS`. See [Creating shared objects](./R-exts.html#Creating-shared-objects) in Writing R Extensions.

---

### 8.5 How can I debug S4 methods?

Use the `trace()` function with argument `signature=` to add calls to
the browser or any other code to the method that will be dispatched for
the corresponding signature. See `?trace` for details.

---
