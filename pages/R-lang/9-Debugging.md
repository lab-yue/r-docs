9 Debugging

---

Debugging code has always been a bit of an art. R provides several tools
that help users find problems in their code. These tools halt execution
at particular points in the code and the current state of the
computation can be inspected.

Most debugging takes place either through calls to `browser` or `debug`.
Both of these functions rely on the same internal mechanism and both
provide the user with a special prompt. Any command can be typed at the
prompt. The evaluation environment for the
command is the currently active environment. This allows you to examine
the current state of any variables etc.

There are five special commands that R interprets differently. They are,

'`RET`'

: Go to the next statement if the function is being debugged. Continue
execution if the browser was invoked.

'`c`'\
'`cont`'

: Continue the execution.

'`n`'

: Execute the next statement in the function. This works from the
browser as well.

'`where`'

: Show the call stack

'`Q`'

: Halt execution and jump to the top-level immediately.

If there is a local variable with the same name as one of the special
commands listed above then its value can be accessed by using `get`. A
call to `get` with the name in quotes will retrieve the value in the
current environment.

The debugger provides access only to interpreted expressions. If a
function calls a foreign language (such as **C**) then no access to the
statements in that language is provided. Execution will halt on the next
statement that is evaluated in R. A symbolic debugger such as `gdb` can
be used to debug compiled code.

---

• [browser](#browser)     
 • [debug/undebug](#debug_002fundebug)     
 • [trace/untrace](#trace_002funtrace)     
 • [traceback](#traceback)

---

---

### 9.1 browser

A call to the function `browser` causes R to halt execution at that
point and to provide the user with a special prompt. Arguments to
`browser` are ignored.

```r
> foo <- function(s) {
+ c <- 3
+ browser()
+ }
> foo(4)
Called from: foo(4)
Browse[1]> s
[1] 4
Browse[1]> get("c")
[1] 3
Browse[1]>
```

---

### 9.2 debug/undebug

The debugger can be invoked on any function by using the command
`debug(fun)`. Subsequently, each time that function is evaluated the
debugger is invoked. The debugger allows you to control the evaluation
of the statements in the body of the function. Before each statement is
executed the statement is printed out and a special prompt provided. Any
command can be given, those in the table above have special meaning.

Debugging is turned off by a call to `undebug` with the function as an
argument.

```r
> debug(mean.default)
> mean(1:10)
debugging in: mean.default(1:10)
debug: {
    if (na.rm)
        x <- x[!is.na(x)]
    trim <- trim[1]
    n <- length(c(x, recursive = TRUE))
    if (trim > 0) {
        if (trim >= 0.5)
            return(median(x, na.rm = FALSE))
        lo <- floor(n * trim) + 1
        hi <- n + 1 - lo
        x <- sort(x, partial = unique(c(lo, hi)))[lo:hi]
        n <- hi - lo + 1
    }
    sum(x)/n
}
Browse[1]>
debug: if (na.rm) x <- x[!is.na(x)]
Browse[1]>
debug: trim <- trim[1]
Browse[1]>
debug: n <- length(c(x, recursive = TRUE))
Browse[1]> c
exiting from: mean.default(1:10)
[1] 5.5
```

---

### 9.3 trace/untrace

Another way of monitoring the behaviour of R is through the `trace`
mechanism. `trace` is called with a single argument that is the name of
the function you want to trace. The name does not need to be quoted but
for some functions you will need to quote the name in order to avoid a
syntax error.

When `trace` has been invoked on a function then every time that
function is evaluated the call to it is printed out. This mechanism is
removed by calling `untrace` with the function as an argument.

```r
> trace("[<-")
> x <- 1:10
> x[3] <- 4
trace: "[<-"(*tmp*, 3, value = 4)
```

---

### 9.4 traceback

When an error has caused a jump to top-level a special variable called
`.Traceback` is placed into the base environment. `.Traceback` is a
character vector with one entry for each function call that was active
at the time the error occurred. An examination of `.Traceback` can be
carried out by a call to `traceback`.

---
