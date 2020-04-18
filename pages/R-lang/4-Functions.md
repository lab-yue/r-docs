4 Functions

---

---

• [Writing functions](#Writing-functions)     
 • [Functions as objects](#Functions-as-objects)     
 • [Evaluation](#Evaluation)

---

---

### 4.1 Writing functions

While R can be very useful as a data analysis tool most users very
quickly find themselves wanting to write their own
functions. This is one of the real advantages of
R. Users can program it and they can, if they want to, change the system
level functions to functions that they find more appropriate.

R also provides facilities that make it easy to document any functions
that you have created. See [Writing R documentation](./R-exts.html#Writing-R-documentation) in Writing R
Extensions.

---

• [Syntax and examples](#Syntax-and-examples)     
 • [Arguments](#Arguments)

---

---

#### 4.1.1 Syntax and examples

The syntax for writing a function is

```r
function ( arglist ) body
```

The first component of the function declaration is the keyword
`function` which indicates to R that you want to create a function.

An argument list is a comma separated list of
formal arguments. A formal argument can be a symbol, a statement of the
form '`symbol = expression`', or the special formal argument
'`...`'.

The _body_ can be any valid R expression. Generally, the body is a group
of expressions contained in curly braces ('`{`' and
'`}`').

Generally functions are assigned to symbols but
they don't need to be. The value returned by the call to `function` is a
function. If this is not given a name it is referred to as an
anonymous function. Anonymous
functions are most frequently used as arguments to other functions such
as the `apply` family or `outer`.

Here is a simple function: `echo <- function(x) print(x)`. So `echo` is
a function that takes a single argument and when `echo` is invoked it
prints its argument.

---

#### 4.1.2 Arguments

The formal arguments to the function define the variables whose values
will be supplied at the time the function is invoked. The names of these
arguments can be used within the function body where they obtain the
value supplied at the time of function invocation.

Default values for arguments can be specified using the special form
'`name = expression`'. In this case, if the user does not
specify a value for the argument when the function is invoked the
expression will be associated with the corresponding symbol. When a
value is needed the `expression`{.variable} is
evaluated in the evaluation
frame of the function.

Default behaviours can also be specified by using the function
`missing`. When `missing` is called with the name of a
formal argument it returns `TRUE` if the formal argument was not matched
with any actual argument and has not been subsequently modified in the
body of the function. An argument that is `missing` will thus have its
default value, if any. The `missing` function does not force evaluation
of the argument.

The special type of argument '`...`' can contain any number of
supplied arguments. It is used for a variety of purposes. It allows you
to write a function that takes an arbitrary
number of arguments. It can be used to absorb some arguments into an
intermediate function which can then be extracted by functions called
subsequently.

---

### 4.2 Functions as objects

Functions are first class objects in R. They can be used anywhere that
an R object is required. In particular they can be passed as arguments
to functions and returned as values from functions. See [Function objects](#Function-objects) for the details.

---

### 4.3 Evaluation

---

• [Evaluation environment](#Evaluation-environment)     
 • [Argument matching](#Argument-matching)     
 • [Argument evaluation](#Argument-evaluation)     
 • [Scope](#Scope)

---

---

#### 4.3.1 Evaluation environment

When a function is called or invoked a new
evaluation frame is created. In this frame the
formal arguments are matched with the supplied arguments according to
the rules given in [Argument matching](#Argument-matching). The
statements in the body of the function are evaluated sequentially in
this environment frame.

The enclosing frame of the evaluation frame is the environment frame
associated with the function being invoked. This may be different from
S. While many functions have `.GlobalEnv` as their environment this does
not have to be true and functions defined in packages with namespaces
(normally) have the package namespace as their environment.

---

#### 4.3.2 Argument matching

This subsection applies to closures but not to primitive functions. The
latter typically ignore tags and do positional matching, but their help
pages should be consulted for exceptions, which include `log`, `round`,
`signif`, `rep` and `seq.int`.

The first thing that occurs in a function
evaluation is the matching of formal to the actual or supplied
arguments. This is done by a three-pass process:

1.  **Exact matching on tags**. For each named
    supplied argument the list of formal arguments is searched for an
    item whose name matches exactly. It is an error to have the same
    formal argument match several actuals or vice versa.
2.  **Partial matching on tags**. Each remaining named supplied argument
    is compared to the remaining formal arguments using partial
    matching. If the name of the supplied argument matches exactly with
    the first part of a formal argument then the two arguments are
    considered to be matched. It is an error to have multiple partial
    matches. Notice that if `f <- function(fumble, fooey) fbody`, then
    `f(f = 1, fo = 2)` is illegal, even though the 2nd actual argument
    only matches `fooey`. `f(f = 1, fooey = 2)` _is_ legal though since
    the second argument matches exactly and is removed from
    consideration for partial matching. If the formal arguments contain
    '`...`' then partial matching is only applied to arguments
    that precede it.
3.  **Positional matching**. Any unmatched formal arguments are bound to
    _unnamed_ supplied arguments, in order. If there is a
    '`...`' argument, it will take up the remaining arguments,
    tagged or not.

If any arguments remain unmatched an error is declared.

Argument matching is augmented by the functions `match.arg`,
`match.call` and `match.fun`.
Access to the partial
matching algorithm used by R is via `pmatch`.

---

#### 4.3.3 Argument evaluation

One of the most important things to know about the
evaluation of arguments to a
function is that supplied arguments and default
arguments are treated differently. The supplied arguments to a function
are evaluated in the evaluation frame of the calling function. The
default arguments to a function are evaluated in the evaluation frame of
the function.

The semantics of invoking a function in R argument are _call-by-value_.
In general, supplied arguments behave as if they are local variables
initialized with the value supplied and the name of
the corresponding formal argument. Changing the value of a supplied
argument within a function will not affect the value of the variable in
the calling frame.

R has a form of lazy evaluation of function arguments. Arguments are not
evaluated until needed. It is important to realize that in some cases
the argument will never be evaluated. Thus, it is bad style to use
arguments to functions to cause side-effects. While in **C** it is
common to use the form, `foo(x = y)` to invoke `foo` with the value of
`y` and simultaneously to assign the value of `y` to `x` this same style
should not be used in R. There is no guarantee that the argument will
ever be evaluated and hence the assignment may
not take place.

It is also worth noting that the effect of `foo(x <- y)` if the argument
is evaluated is to change the value of `x` in the calling
environment and not in the
evaluation environment of
`foo`.

It is possible to access the actual (not default) expressions used as
arguments inside the function. The mechanism is implemented via
promises. When a function is being evaluated the
actual expression used as an argument is stored in the promise together
with a pointer to the environment the function was called from. When
(if) the argument is evaluated the stored expression is evaluated in the
environment that the function was called from. Since only a pointer to
the environment is used any changes made to that environment will be in
effect during this evaluation. The resulting value is then also stored
in a separate spot in the promise. Subsequent evaluations retrieve this
stored value (a second evaluation is not carried out). Access to the
unevaluated expression is also available using `substitute`.

When a function is called, each formal argument
is assigned a promise in the local environment of the call with the
expression slot containing the actual argument (if it exists) and the
environment slot containing the environment of the caller. If no actual
argument for a formal argument is given in the call and there is a
default expression, it is similarly assigned to the expression slot of
the formal argument, but with the environment
set to the local environment.

The process of filling the value slot of a promise by
evaluating the contents of the expression slot
in the promise's environment is called _forcing_ the promise. A promise
will only be forced once, the value slot content being used directly
later on.

A promise is forced when its value is needed. This usually happens
inside internal
functions, but a promise can also be forced by direct evaluation of the
promise itself. This is occasionally useful when a default expression
depends on the value of another formal argument or other variable in the
local environment. This is seen in the following example where the lone
`label` ensures that the label is based on the value of `x` before it is
changed in the next line.

```r
function(x, label = deparse(x)) {
    label
    x <- x + 1
    print(label)
}
```

The expression slot of a promise can itself involve other promises. This
happens whenever an unevaluated argument is passed as an argument to
another function. When forcing a promise, other promises in its
expression will also be forced recursively as they are evaluated.

---

#### 4.3.4 Scope

Scope or the scoping rules are simply the set of rules used by the
evaluator to find a value for a
symbol. Every computer language has a set of such
rules. In R the rules are fairly simple but there do exist mechanisms
for subverting the usual, or default rules.

R adheres to a set of rules that are called _lexical scope_. This means
the variable bindings in effect at the time the
expression was created are used to provide values for any unbound
symbols in the expression.

Most of the interesting properties of scope are
involved with evaluating functions and we
concentrate on this issue. A symbol can be either
bound or unbound. All of the formal arguments to a function provide
bound symbols in the body of the function. Any other symbols in the body
of the function are either local variables or unbound variables. A local
variable is one that is defined within the function. Because R has no
formal definition of variables, they are simply used as needed, it can
be difficult to determine whether a variable is local or not. Local
variables must first be defined, this is typically done by having them
on the left-hand side of an assignment.

During the evaluation process if an unbound symbol is detected then R
attempts to find a value for it. The scoping rules determine how this
process proceeds. In R the environment of the
function is searched first, then its enclosure and so on until the
global environment is reached.

The global environment heads a search list of environments that are
searched sequentially for a matching symbol. The value of the first
match is then used.

When this set of rules is combined with the fact that
functions can be returned as values from other
functions then some rather nice, but at first glance peculiar,
properties obtain.

A simple example:

```r
f <- function() {
    y <- 10
    g <- function(x) x + y
    return(g)
}
h <- f()
h(3)
```

A rather interesting question is what happens when `h` is evaluated. To
describe this we need a bit more notation. Within a
function body variables can be bound, local or
unbound. The bound variables are those that match the formal arguments
to the function. The local variables are those that were created or
defined within the function body. The unbound variables are those that
are neither local nor bound. When a function body is evaluated there is
no problem determining values for local variables or for bound
variables. Scoping rules determine how the language will find values for
the unbound variables.

When `h(3)` is evaluated we see that its body is that of `g`. Within
that body `x` is bound to the formal argument and `y` is unbound. In a
language with lexical scope `x` will be associated
with the value 3 and `y` with the value 10 local to `f` so `h(3)` should
return the value 13. In R this is indeed what happens.

In S, because of the different scoping rules one will get an error
indicating that `y` is not found, unless there is a variable `y` in your
workspace in which case its value will be used.

---
