5 Object-oriented programming

---

Object-oriented programming is a style of programming that has become
popular in recent years. Much of the popularity comes from the fact that
it makes it easier to write and maintain complicated systems. It does
this through several different mechanisms.

Central to any object-oriented language are the concepts of class and of
methods. A _class_ is a definition of an object. Typically a class
contains several _slots_ that are used to hold class-specific
information. An object in the language must be an instance of some
class. Programming is based on objects or instances of classes.

Computations are carried out via _methods_. Methods are basically
functions that are specialized to carry out
specific calculations on objects, usually of a specific class. This is
what makes the language object oriented. In R, _generic functions_ are
used to determine the appropriate method. The generic function is
responsible for determining the class of its argument(s) and uses that
information to select the appropriate method.

Another feature of most object-oriented languages is the concept of
inheritance. In most programming problems there are usually many objects
that are related to one another. The programming is considerably
simplified if some components can be reused.

If a class inherits from another class then generally it gets all the
slots in the parent class and can extend it by adding new slots. On
method dispatching (via the generic functions) if a method for the class
does not exist then a method for the parent is sought.

In this chapter we discuss how this general strategy has been
implemented in R and discuss some of the limitations within the current
design. One of the advantages that most object systems impart is greater
consistency. This is achieved via the rules that are checked by the
compiler or interpreter. Unfortunately because of the way that the
object system is incorporated into R this advantage does not obtain.
Users are cautioned to use the object system in a straightforward
manner. While it is possible to perform some rather interesting feats
these tend to lead to obfuscated code and may depend on implementation
details that will not be carried forward.

The greatest use of object oriented programming in R is through `print`
methods, `summary` methods and `plot` methods. These methods allow us to
have one generic function call, `plot`
say, that dispatches on the type of its argument and calls a plotting
function that is specific to the data supplied.

In order to make the concepts clear we will consider the implementation
of a small system designed to teach students about probability. In this
system the objects are probability functions and the methods we will
consider are methods for finding moments and for plotting. Probabilities
can always be represented in terms of the cumulative distribution
function but can often be represented in other ways. For example as a
density, when it exists or as a moment generating function when it
exists.

---

• [Definition](#Definition)     
 • [Inheritance](#Inheritance)     
 • [Method dispatching](#Method-dispatching)     
 • [UseMethod](#UseMethod)     
 • [NextMethod](#NextMethod)     
 • [Group methods](#Group-methods)     
 • [Writing methods](#Writing-methods)

---

---

### 5.1 Definition

Rather than having a full-fledged
object-oriented system R has a class system and a mechanism for
dispatching based on the class of an object. The dispatch mechanism for
interpreted code relies on four special objects that are stored in the
evaluation frame. These special objects are `.Generic`, `.Class`,
`.Method` and `.Group`. There is a separate dispatch mechanism used for
internal functions and types that will be discussed elsewhere.

The class system is facilitated through the `class` attribute. This
attribute is a character vector of class names. So to create an object
of class `"foo"` one simply attaches a class attribute with the string
'`"foo"`' in it. Thus, virtually anything can be turned in to
an object of class `"foo"`.

The object system makes use of
_generic functions_ via two dispatching functions, `UseMethod` and
`NextMethod`. The typical use of the object system is to begin by
calling a generic function. This is typically a very simple function and
consists of a single line of code. The system function `mean` is just
such a function,

```r
> mean
function (x, ...)
UseMethod("mean")
```

When `mean` is called it can have any number of arguments but its first
argument is special and the class of that first argument is used to
determine which method should be called. The variable `.Class` is set to
the class attribute of `x`, `.Generic` is set to the string `"mean"` and
a search is made for the correct method to invoke. The class attributes
of any other arguments to `mean` are ignored.

Suppose that `x` had a class attribute that contained `"foo"` and
`"bar"`, in that order. Then R would first search for a function called
`mean.foo` and if it did not find one it would then search for a
function `mean.bar` and if that search was also unsuccessful then a
final search for `mean.default` would be made. If the last search is
unsuccessful R reports an error. It is a good idea to always write a
default method. Note that the functions `mean.foo` etc. are referred to,
in this context, as methods.

`NextMethod` provides another mechanism for dispatching. A
function may have a call to `NextMethod` anywhere
in it. The determination of which method should then be invoked is based
primarily on the current values of `.Class` and `.Generic`. This is
somewhat problematic since the method is really an ordinary function and
users may call it directly. If they do so then there will be no values
for `.Generic` or `.Class`.

If a method is invoked directly and it contains a call to `NextMethod`
then the first argument to `NextMethod` is used to determine the
generic function. An error is
signalled if this argument has not been supplied; it is therefore a good
idea to always supply this argument.

In the case that a method is invoked directly the class attribute of the
first argument to the method is used as the value of `.Class`.

Methods themselves employ `NextMethod` to provide a form of inheritance.
Commonly a specific method performs a few operations to set up the data
and then it calls the next appropriate method through a call to
`NextMethod`.

Consider the following simple example. A point in two-dimensional
Euclidean space can be specified by its Cartesian (x-y) or polar
(r-theta) coordinates. Hence, to store information about the location of
the point, we could define two classes, `"xypoint"` and `"rthetapoint"`.
All the 'xypoint' data structures are lists with an x-component and a
y-component. All 'rthetapoint' objects are lists with an r-component and
a theta-component.

Now, suppose we want to get the x-position from either type of object.
This can easily be achieved through
generic functions. We define the generic function `xpos` as follows.

```r
xpos <- function(x, ...)
    UseMethod("xpos")
```

Now we can define methods:

```r
xpos.xypoint <- function(x) x$x
xpos.rthetapoint <- function(x) x$r * cos(x$theta)
```

The user simply calls the function `xpos` with either representation as
the argument. The internal dispatching method finds the class of the
object and calls the appropriate methods.

It is pretty easy to add other representations. One need not write a new
generic function only the methods. This makes it easy to add to existing
systems since the user is only responsible for dealing with the new
representation and not with any of the existing representations.

The bulk of the uses of this methodology are to provide specialized
printing for objects of different types; there are about 40 methods for
`print`.

---

### 5.2 Inheritance

The class attribute of an object can have several elements. When a
generic function is called the first
inheritance is mainly handled through `NextMethod`. `NextMethod`
determines the method currently being evaluated, finds the next class
from th

FIXME: something is missing here

---

### 5.3 Method dispatching

Generic functions should consist of a single statement. They should
usually be of the form `foo <- function(x, ...) UseMethod("foo", x)`.
When `UseMethod` is called, it determines the appropriate method and
then that method is invoked with the same arguments, in the same order
as the call to the generic, as if the call had been made directly to the
method.

In order to determine the correct method the class attribute of the
first argument to the generic is obtained and used to find the correct
method. The name of the generic function is combined
with the first element of the class attribute into the form,
`generic.class` and a function with that name is sought. If the function
is found then it is used. If no such function is found then the second
element of the class attribute is used, and so on until all the elements
of the class attribute have been exhausted. If no method has been found
at that point then the method `generic.default` is used. If the first
argument to the generic function has no class attribute then
`generic.default` is used. Since the introduction of namespaces the
methods may not be accessible by their names (i.e.
`get("generic.class")` may fail), but they will be accessible by
`getS3method("generic","class")`.

Any object can have a `class` attribute. This attribute can have any
number of elements. Each of these is a string that defines a class. When
a generic function is invoked the class of its first argument is
examined.

---

### 5.4 UseMethod

`UseMethod` is a special function and it behaves differently from other
function calls. The syntax of a call to it is
`UseMethod(generic, object)`, where `generic`{.variable} is the name of
the generic function, `object`{.variable} is the object used to
determine which method should be chosen. `UseMethod` can only be called
from the body of a function.

`UseMethod` changes the evaluation model in two ways. First, when it is
invoked it determines the next method (function) to be called. It then
invokes that function using the current evaluation
environment; this process will be described
shortly. The second way in which `UseMethod` changes the evaluation
environment is that it does not return control to the calling function.
This means, that any statements after a call to `UseMethod` are
guaranteed not to be executed.

When `UseMethod` is invoked the generic function is the specified value
in the call to `UseMethod`. The object to dispatch on is either the
supplied second argument or the first argument to the current function.
The class of the argument is determined and the first element of it is
combined with the name of the generic to determine the appropriate
method. So, if the generic had name `foo` and the class of the object is
`"bar"`, then R will search for a method named `foo.bar`. If no such
method exists then the inheritance mechanism described above is used to
locate an appropriate method.

Once a method has been determined R invokes it in a special way. Rather
than creating a new evaluation environment R
uses the environment of the current function call (the call to the
generic). Any assignments or evaluations that
were made before the call to `UseMethod` will be in effect. The
arguments that were used in the call to the generic are rematched to the
formal arguments of the selected method.

When the method is invoked it is called with arguments that are the same
in number and have the same names as in the call to the generic. They
are matched to the arguments of the method according to the standard R
rules for argument matching. However the object, i.e. the first argument
has been evaluated.

The call to `UseMethod` has the effect of placing some special objects
in the evaluation frame. They are `.Class`, `.Generic` and `.Method`.
These special objects are used to by R to handle the method dispatch and
inheritance. `.Class` is the class of the object, `.Generic` is the name
of the generic function and `.Method` is the name of the method
currently being invoked. If the method was invoked through one of the
internal interfaces then there may also be an object called `.Group`.
This will be described in Section [Group methods](#Group-methods). After
the initial call to `UseMethod` these special variables, not the object
itself, control the selection of subsequent methods.

The body of the method is then evaluated in the standard fashion. In
particular variable look-up in the body follows the rules for the
method. So if the method has an associated environment then that is
used. In effect we have replaced the call to the generic by a call to
the method. Any local assignments in the frame
of the generic will be carried forward into the call to the method. Use
of this _feature_ is discouraged. It is important to realize that
control will never return to the generic and hence any expressions after
a call to `UseMethod` will never be executed.

Any arguments to the generic that were evaluated prior to the call to
`UseMethod` remain evaluated.

If the first argument to `UseMethod` is not supplied it is assumed to be
the name of the current function. If two arguments are supplied to
`UseMethod` then the first is the name of the method and the second is
assumed to be the object that will be dispatched on. It is evaluated so
that the required method can be determined. In this case the first
argument in the call to the generic is not evaluated and is discarded.
There is no way to change the other arguments in the call to the method;
these remain as they were in the call to the generic. This is in
contrast to `NextMethod` where the arguments in the call to the next
method can be altered.

---

### 5.5 NextMethod

`NextMethod` is used to provide a simple inheritance mechanism.

Methods invoked as a result of a call to `NextMethod` behave as if they
had been invoked from the previous method. The arguments to the
inherited method are in the same order and have the same names as the
call to the current method. This means that they are the same as for the
call to the generic. However, the expressions for the arguments are the
names of the corresponding formal arguments of the current method. Thus
the arguments will have values that correspond to their value at the
time NextMethod was invoked.

Unevaluated arguments remain unevaluated. Missing arguments remain
missing.

The syntax for a call to `NextMethod` is
`NextMethod(generic, object, ...)`. If the `generic` is not supplied the
value of `.Generic` is used. If the `object` is not supplied the first
argument in the call to the current method is used. Values in the
'`...`' argument are used to modify the arguments of the next
method.

It is important to realize that the choice of the next method depends on
the current values of `.Generic` and `.Class` and not on the object. So
changing the object in a call to `NextMethod` affects the arguments
received by the next method but does not affect the choice of the next
method.

Methods can be called directly. If they are then there will be no
`.Generic`, `.Class` or `.Method`. In this case the `generic` argument
of `NextMethod` must be specified. The value of `.Class` is taken to be
the class attribute of the object which is the first argument to the
current function. The value of `.Method` is the name of the current
function. These choices for default values ensure that the behaviour of
a method doesn't change depending on whether it is called directly or
via a call to a generic.

An issue for discussion is the behaviour of the '`...`'
argument to `NextMethod`. The White Book describes the behaviour as
follows:

\- named arguments replace the corresponding arguments in the call to
the current method. Unnamed arguments go at the start of the argument
list.

What I would like to do is:

-first do the argument matching for NextMethod; -if the object or
generic are changed fine -first if a named list element matches an
argument (named or not) the list value replaces the argument value. -
the first unnamed list element

Values for lookup: Class: comes first from .Class, second from the first
argument to the method and last from the object specified in the call to

### 5.6 Group methods

For several types of internal
functions R provides a dispatching mechanism for operators. This means
that operators such as `==` or `<` can have their behaviour modified for
members of special classes. The functions and operators have been
grouped into three categories and group methods can be written for each
of these categories. There is currently no mechanism to add groups. It
is possible to write methods specific to any function within a group.

The following table lists the functions for the different Groups.

'`Math`'

: abs, acos, acosh, asin, asinh, atan, atanh, ceiling, cos, cosh,
cospi, cumsum, exp, floor, gamma, lgamma, log, log10, round, signif,
sin, sinh, sinpi, tan, tanh, tanpi, trunc

'`Summary`'

: all, any, max, min, prod, range, sum

'`Ops`'

: `+`, `-`, `*`, `/`, `^`, `<` , `>`, `<=`, `>=`, `!=`, `==`, `%%`,
`%/%`, `&`, `|`, `!`

For operators in the Ops group a special method is invoked if the two
operands taken together suggest a single method. Specifically, if both
operands correspond to the same method or if one operand corresponds to
a method that takes precedence over that of the other operand. If they
do not suggest a single method then the default method is used. Either a
group method or a class method dominates if the other operand has no
corresponding method. A class method dominates a group method.

When the group is Ops the special variable `.Method` is a string vector
with two elements. The elements of `.Method` are set to the name of the
method if the corresponding argument is a member of the class that was
used to determine the method. Otherwise the corresponding element of
`.Method` is set to the zero length string, `""`.

---

### 5.7 Writing methods

Users can easily write their own methods and generic functions. A
generic function is simply a function
with a call to `UseMethod`. A method is simply a function that has been
invoked via method dispatch. This can be as a result of a call to either
`UseMethod` or `NextMethod`.

It is worth remembering that methods can be called directly. That means
that they can be entered without a call to `UseMethod` having been made
and hence the special variables `.Generic`, `.Class` and `.Method` will
not have been instantiated. In that case the default rules detailed
above will be used to determine these.

The most common use of generic
functions is to provide `print` and `summary` methods for statistical
objects, generally the output of some model fitting process. To do this,
each model attaches a class attribute to its output and then provides a
special method that takes that output and provides a nice readable
version of it. The user then needs only remember that `print` or
`summary` will provide nice output for the results of any analysis.

---
