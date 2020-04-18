# 8 Exception handling

---

The exception handling facilities in R are provided through two
mechanisms. Functions such as `stop` or `warning` can be called directly
or options such as `"warn"` can be used to control the handling of
problems.

---

• [stop](#stop)     
 • [warning](#warning)     
 • [on.exit](#on_002eexit)     
 • [Error options](#Error-options)

---

---

### 8.1 stop

A call to `stop` halts the evaluation of the current expression, prints
the message argument and returns execution to top-level.

---

### 8.2 warning

The function `warning` takes a single argument that is a character
string. The behaviour of a call to `warning` depends on the value of the
option `"warn"`. If `"warn"` is negative warnings are ignored. If it is
zero, they are stored and printed after the top-level function has
completed. If it is one, they are printed as they occur and if it is 2
(or larger) warnings are turned into errors.

If `"warn"` is zero (the default), a variable `last.warning` is created
and the messages associated with each call to `warning` are stored,
sequentially, in this vector. If there are fewer than 10 warnings they
are printed after the function has finished evaluating. If there are
more than 10 then a message indicating how many warnings occurred is
printed. In either case `last.warning` contains the vector of messages,
and `warnings` provides a way to access and print it.

---

### 8.3 on.exit

A function can insert a call to `on.exit` at any point in the body of a
function. The effect of a call to `on.exit` is to store the value of the
body so that it will be executed when the function exits. This allows
the function to change some system parameters and to ensure that they
are reset to appropriate values when the function is finished. The
`on.exit` is guaranteed to be executed when the function exits either
directly or as the result of a warning.

An error in the evaluation of the `on.exit` code causes an immediate
jump to top-level without further processing of the `on.exit` code.

`on.exit` takes a single argument which is an expression to be evaluated
when the function is exited.

---

### 8.4 Error options

There are a number of `options` variables that can be used to control
how R handles errors and warnings. They are listed in the table below.

'`warn`'

: Controls the printing of warnings.

'`warning.expression`'

: Sets an expression that is to be evaluated when a warning occurs.
The normal printing of warnings is suppressed if this option is set.

'`error`'

: Installs an expression that will be evaluated when an error occurs.
The normal printing of error messages and warning messages precedes
the evaluation of the expression.

Expressions installed by `options("error")` are evaluated before calls
to `on.exit` are carried out.

One can use `options(error = expression(q("yes")))` to get R to quit
when an error has been signalled. In this case an error will cause R to
shut down and the global environment will be saved.

---
