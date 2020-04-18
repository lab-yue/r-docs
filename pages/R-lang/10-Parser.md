10 Parser

---

The parser is what converts the textual representation of R code into an
internal form which may then be passed to the R evaluator which causes
the specified instructions to be carried out. The internal form is
itself an R object and can be saved and otherwise manipulated within the
R system.

---

• [The parsing process](#The-parsing-process)     
 • [Comments](#Comments)     
 • [Tokens](#Tokens)     
 • [Expressions](#Expressions)     
 • [Directives](#Directives)

---

---

### 10.1 The parsing process

---

• [Modes of parsing](#Modes-of-parsing)     
 • [Internal representation](#Internal-representation)     
 • [Deparsing](#Deparsing)

---

---

#### 10.1.1 Modes of parsing

Parsing in R occurs in three different variants:

- The read-eval-print loop
- Parsing of text files
- Parsing of character strings

The read-eval-print loop forms the basic command line interface to R.
Textual input is read until a complete R expression is available.
Expressions may be split over several input lines. The primary prompt
(by default '`>`') indicates that the parser is ready for a
new expression, and a continuation prompt (by default '`+`')
indicates that the parser expects the remainder of an incomplete
expression. The expression is converted to internal form during input
and the parsed expression is passed to the evaluator and the result is
printed (unless specifically made invisible). If the parser finds itself
in a state which is incompatible with the language syntax, a "Syntax
Error" is flagged and the parser resets itself and resumes input at the
beginning of the next input line.

Text files can be parsed using the `parse` function. In particular, this
is done during execution of the `source` function, which allows commands
to be stored in an external file and executed as if they had been typed
at the keyboard. Note, though, that the entire file is parsed and syntax
checked before any evaluation takes place.

Character strings, or vectors thereof, can be parsed using the `text=`
argument to `parse`. The strings are treated exactly as if they were the
lines of an input file.

---

#### 10.1.2 Internal representation

Parsed expressions are stored in an R object containing the parse tree.
A fuller description of such objects can be found in [Language objects](#Language-objects) and [Expression objects](#Expression-objects). Briefly, every elementary R expression is
stored in function call form, as a list with the
first element containing the function name and the remainder containing
the arguments, which may in turn be further R expressions. The list
elements can be named, corresponding to tagged matching of formal and
actual arguments. Note that _all_ R syntax elements are treated in this
way, e.g. the assignment `x <- 1` is encoded as `"<-"(x, 1)`.

---

#### 10.1.3 Deparsing

Any R object can be converted to an R expression using `deparse`. This
is frequently used in connection with output of results, e.g. for
labeling plots. Notice that only objects of mode `"expression"` can be
expected to be unchanged by reparsing the output of deparsing. For
instance, the numeric vector `1:5` will deparse as `"c(1, 2, 3, 4, 5)"`,
which will reparse as a call to the function `c`. As far as possible,
evaluating the deparsed and reparsed expression gives the same result as
evaluating the original, but there are a couple of awkward exceptions,
mostly involving expressions that weren't generated from a textual
representation in the first place.

---

### 10.2 Comments

Comments in R are ignored by the parser. Any text from a
`#` character to the end of the line is taken to be a
comment, unless the `#` character is inside a quoted string. For
example,

```r
> x <- 1  # This is a comment...
> y <- "  #... but this is not."
```

---

### 10.3 Tokens

Tokens are the elementary building blocks of a programming language.
They are recognised during _lexical analysis_ which (conceptually, at
least) takes place prior to the syntactic analysis performed by the
parser itself.

---

• [Literal constants](#Literal-constants)     
 • [Identifiers](#Identifiers)     
 • [Reserved words](#Reserved-words)     
 • [Special operators](#Special-operators)     
 • [Separators](#Separators)     
 • [Operator tokens](#Operator-tokens)     
 • [Grouping](#Grouping)     
 • [Indexing tokens](#Indexing-tokens)

---

---

#### 10.3.1 Constants

There are five types of constants: integer, logical, numeric, complex
and string.

In addition, there are four special constants, `NULL`, `NA`, `Inf`, and
`NaN`.

`NULL` is used to indicate the empty object. `NA` is used for absent
("Not Available") data values. `Inf` denotes infinity and `NaN` is
not-a-number in the IEEE floating point calculus (results of the
operations respectively _1/0_ and _0/0_, for instance).

Logical constants are either `TRUE` or `FALSE`.

Numeric constants follow a similar syntax to that of the **C** language.
They consist of an integer part consisting of zero or more digits,
followed optionally by '`.`' and a fractional part of zero or
more digits optionally followed by an exponent part consisting of an
'`E`' or an '`e`', an optional sign and a string of
one or more digits. Either the fractional or the decimal part can be
empty, but not both at once.

```r
Valid numeric constants: 1 10 0.1 .2 1e-7 1.2e+7
```

Numeric constants can also be hexadecimal, starting with '`0x`'
or '`0x`' followed by zero or more digits, '`a-f`' or
'`A-F`'. Hexadecimal floating point constants are supported
using C99 syntax, e.g. '`0x1.1p1`'.

There is now a separate class of integer constants. They are created by
using the qualifier `L` at the end of the number. For example, `123L`
gives an integer value rather than a numeric value. The suffix `L` can
be used to qualify any non-complex number with the intent of creating an
integer. So it can be used with numbers given by hexadecimal or
scientific notation. However, if the value is not a valid integer, a
warning is emitted and the numeric value created. The following shows
examples of valid integer constants, values which will generate a
warning and give numeric constants and syntax errors.

```r
Valid integer constants:  1L, 0x10L, 1000000L, 1e6L
Valid numeric constants:  1.1L, 1e-3L, 0x1.1p-2
Syntax error:  12iL 0x1.1
```

A warning is emitted for decimal values that contain an unnecessary
decimal point, e.g. `1.L`. It is an error to have a decimal point in a
hexadecimal constant without the binary exponent.

Note also that a preceding sign (`+` or `-`) is treated as a unary
operator, not as part of the constant.

Up-to-date information on the currently accepted formats can be found by
`?NumericConstants`.

Complex constants have the form of a decimal numeric constant followed
by '`i`'. Notice that only purely imaginary numbers are actual
constants, other complex numbers are parsed a unary or binary operations
on numeric and imaginary numbers.

```r
Valid complex constants: 2i 4.1i 1e-2i
```

String constants are delimited by a pair of single ('`'`') or
double ('`"`') quotes and can contain all other printable
characters. Quotes and other special characters within strings are
specified using _escape sequences_:

`\'`

: single quote

`\"`

: double quote

`\n`

: newline (aka 'line feed', `LF`{.key})

`\r`

: carriage return (`CR`{.key})

`\t`

: tab character

`\b`

: backspace

`\a`

: bell

`\f`

: form feed

`\v`

: vertical tab

`\\`

: backslash itself

`\nnn`

: character with given octal code -- sequences of one, two or three
digits in the range `0 ... 7` are accepted.

`\xnn`

: character with given hex code -- sequences of one or two hex digits
(with entries `0 ... 9 A ... F a ... f`).

`\unnnn \u{nnnn}`

: (where multibyte locales are supported, otherwise an error). Unicode
character with given hex code -- sequences of up to four hex digits.
The character needs to be valid in the current locale.

`\Unnnnnnnn \U{nnnnnnnn}`

: (where multibyte locales are supported, otherwise an error). Unicode
character with given hex code -- sequences of up to eight hex
digits.

A single quote may also be embedded directly in a double-quote delimited
string and vice versa.

A 'nul' (`\0`) is not allowed in a character string, so using `\0` in a
string constant terminates the constant (usually with a warning):
further characters up to the closing quote are scanned but ignored.

---

#### 10.3.2 Identifiers

Identifiers consist of a sequence of letters, digits, the period
('`.`') and the underscore. They must not start with a digit or
an underscore, or with a period followed by a digit.

The definition of a letter depends on the current locale: the precise
set of characters allowed is given by the C expression
`(isalnum(c) || c == ‘.’ || c == ‘_’)` and will include accented letters
in many Western European locales.

Notice that identifiers starting with a period are not by default listed
by the `ls` function and that '`...`' and '`..1`',
'`..2`', etc. are special.

Notice also that objects can have names that are not identifiers. These
are generally accessed via `get` and `assign`, although they can also be
represented by text strings in some limited circumstances when there is
no ambiguity (e.g. `"x" <- 1`). As `get` and `assign` are not restricted
to names that are identifiers they do not recognise subscripting
operators or replacement functions. The following pairs are _not_
equivalent

> ---
>
> `x$a<-1` `assign("x$a",1)` > `x[[1]]` `get("x[[1]]")` > `names(x)<-nm` `assign("names(x)",nm)`
>
> ---

---

#### 10.3.3 Reserved words

The following identifiers have a special meaning and cannot be used for
object names

```r
if else repeat while function for in next break
TRUE FALSE NULL Inf NaN
NA NA_integer_ NA_real_ NA_complex_ NA_character_
... ..1 ..2 etc.
```

---

#### 10.3.4 Special operators

R allows user-defined infix operators. These have the form of a string
of characters delimited by the '`%`' character. The string can
contain any printable character except '`%`'. The escape
sequences for strings do not apply here.

Note that the following operators are predefined

```r
%% %*% %/% %in% %o% %x%
```

---

#### 10.3.5 Separators

Although not strictly tokens, stretches of whitespace characters
(spaces, tabs and formfeeds, on Windows and UTF-8 locales other Unicode
whitespace characters[^4^](#FOOT4)) serve to delimit tokens in
case of ambiguity, (compare `x<-5` and `x < -5`).

Newlines have a function which is a combination of token separator and
expression terminator. If an expression can terminate at the end of the
line the parser will assume it does so, otherwise the newline is treated
as whitespace. Semicolons ('`;`') may be used to separate
elementary expressions on the same line.

Special rules apply to the `else` keyword: inside a compound expression,
a newline before `else` is discarded, whereas at the outermost level,
the newline terminates the `if` construction and a subsequent `else`
causes a syntax error. This somewhat anomalous behaviour occurs because
R should be usable in interactive mode and then it must decide whether
the input expression is complete, incomplete, or invalid as soon as the
user presses `RET`{.key}.

The comma ('`,`') is used to separate function arguments and
multiple indices.

---

#### 10.3.6 Operator tokens

R uses the following operator tokens

> ---
>
> `+ - * / %% ^` arithmetic
> `> >= < <= == !=` relational
> `! & |` logical
> `~` model formulae
> `-> <-` assignment
> `$` list indexing
> `:` sequence
>
> ---

(Several of the operators have different meaning inside model formulas)

---

#### 10.3.7 Grouping

Ordinary parentheses---'`(`' and '`)`'---are used for
explicit grouping within expressions and to delimit the argument lists
for function definitions and function calls.

Braces---'`{`' and '`}`'---delimit blocks of
expressions in function definitions, conditional expressions, and
iterative constructs.

---

#### 10.3.8 Indexing tokens

Indexing of arrays and vectors is performed using the single and double
brackets, '`[]`' and '`[[]]`'. Also, indexing tagged
lists may be done using the '`$`' operator.

---

### 10.4 Expressions

An R program consists of a sequence of R expressions. An expression can
be a simple expression consisting of only a constant or an identifier,
or it can be a compound expression constructed from other parts (which
may themselves be expressions).

The following sections detail the various syntactical constructs that
are available.

---

• [Function calls (expressions)](#Function-calls-_0028expressions_0029)     
 • [Infix and prefix operators](#Infix-and-prefix-operators)     
 • [Index constructions](#Index-constructions)     
 • [Compound expressions](#Compound-expressions)     
 • [Flow control elements](#Flow-control-elements)     
 • [Function definitions](#Function-definitions)

---

---

#### 10.4.1 Function calls

A function call takes the form of a function reference followed by a
comma-separated list of arguments within a set of parentheses.

```r
function_reference ( arg1, arg2, ...... , argn )
```

The function reference can be either

- an identifier (the name of the function)
- a text string (ditto, but handy if the function has a name which is
  not a valid identifier)
- an expression (which should evaluate to a function object)

Each argument can be tagged (`tag=expr`), or just be a simple
expression. It can also be empty or it can be one of the special tokens
'`...`', '`..2`', etc.

A tag can be an identifier or a text string.

Examples:

```r
f(x)
g(tag = value, , 5)
"odd name"("strange tag" = 5, y)
(function(x) x^2)(5)
```

---

#### 10.4.2 Infix and prefix operators

The order of precedence (highest first) of the operators is

```r
::
$ @
^
- +                (unary)
:
%xyz%
* /
+ -                (binary)
> >= < <= == !=
!
& &&
| ||
~                  (unary and binary)
-> ->>
=                  (as assignment)
<- <<-
```

Note that `:` precedes binary +/-, but not `^`. Hence, `1:3-1` is _0 1
2_, but `1:2^3` is `1:8`.

The exponentiation operator '`^`' and the
left assignment plus minus operators
'`<- - = <<-`' group right to left, all other operators group
left to right. That is, `2 ^ 2 ^ 3` is _2 \^ 8_, not _4 \^ 3_, whereas
`1 - 1 - 1` is _-1_, not 1.

Notice that the operators `%%` and `%/%` for integer remainder and
divide have higher precedence than multiply and divide.

Although it is not strictly an operator, it also needs mentioning that
the '`=`' sign is used for tagging arguments in function calls
and for assigning default values in function definitions.

The '`$`' sign is in some sense an operator, but does not allow
arbitrary right hand sides and is discussed under [Index constructions](#Index-constructions). It has higher precedence than any
of the other operators.

The parsed form of a unary or binary operation is completely equivalent
to a function call with the operator as the function name and the
operands as the function arguments.

Parentheses are recorded as equivalent to a unary operator, with name
`"("`, even in cases where the parentheses could be inferred from
operator precedence (e.g., `a * (b + c)`).

Notice that the assignment symbols are
operators just like the arithmetic, relational, and logical ones. Any
expression is allowed also on the target side of an assignment, as far
as the parser is concerned (`2 + 2 <- 5` is a valid expression as far as
the parser is concerned. The evaluator will object, though). Similar
comments apply to the model formula operator.

---

#### 10.4.3 Index constructions

R has three indexing constructs, two of which are syntactically similar
although with somewhat different semantics:

```r
object [ arg1, ...... , argn ]
object [[ arg1, ...... , argn ]]
```

The `object`{.variable} can formally be any valid expression, but it is
understood to denote or evaluate to a subsettable object. The arguments
generally evaluate to numerical or character indices, but other kinds of
arguments are possible (notably `drop = FALSE`).

Internally, these index constructs are stored as function calls with
function name `"["` respectively `"[["`.

The third index construction is

```r
object $ tag
```

Here, `object`{.variable} is as above, whereas `tag`{.variable} is an
identifier or a text string. Internally, it is stored as a function call
with name `"$"`

---

#### 10.4.4 Compound expressions

A compound expression is of the form

```r
{ expr1 ; expr2 ; ...... ; exprn }
```

The semicolons may be replaced by newlines. Internally, this is stored
as a function call with `"{"` as the function name and the expressions
as arguments.

---

#### 10.4.5 Flow control elements

R contains the following control structures as special syntactic
constructs

```r
if ( cond ) expr
if ( cond ) expr1 else expr2
while ( cond ) expr
repeat expr
for ( var in list ) expr
```

The expressions in these constructs will typically be compound
expressions.

Within the loop constructs (`while`, `repeat`, `for`), one may use
`break` (to terminate the loop) and `next` (to skip to the next
iteration).

Internally, the constructs are stored as function calls:

```r
"if"(cond, expr)
"if"(cond, expr1, expr2)
"while"(cond, expr)
"repeat"(expr)
"for"(var, list, expr)
"break"()
"next"()
```

---

#### 10.4.6 Function definitions

A function definition is of the form

```r
function ( arglist ) body
```

The function body is an expression, often a compound expression. The
`arglist`{.variable} is a comma-separated list of items each of which
can be an identifier, or of the form '`identifier = default`',
or the special token '`...`'. The `default`{.variable} can be
any valid expression.

Notice that function arguments unlike list tags, etc., cannot have
"strange names" given as text strings.

Internally, a function definition is stored as a function call with
function name `function` and two arguments, the `arglist`{.variable} and
the `body`{.variable}. The `arglist`{.variable} is stored as a tagged
pairlist where the tags are the argument names and the values are the
default expressions.

---

### 10.5 Directives

The parser currently only supports one directive, `#line`. This is
similar to the C-preprocessor directive of the same name. The syntax is

```r
#line nn [ "filename" ]
```

where `nn`{.variable} is an integer line number, and the optional
`filename`{.variable} (in required double quotes) names the source file.

Unlike the C directive, `#line` must appear as the first five characters
on a line. As in C, `nn`{.variable} and `"filename"` entries may be
separated from it by whitespace. And unlike C, any following text on the
line will be treated as a comment and ignored.

This directive tells the parser that the following line should be
assumed to be line `nn`{.variable} of file `filename`{.variable}. (If
the filename is not given, it is assumed to be the same as for the

## Function and Variable Index

---

Jump to:   [**\#**](#Function-and-Variable-Index_vr_symbol-1){.summary-letter}  
[**\$**](#Function-and-Variable-Index_vr_symbol-2){.summary-letter}  
[**.**](#Function-and-Variable-Index_vr_symbol-3){.summary-letter}  
[**\[**](#Function-and-Variable-Index_vr_symbol-4){.summary-letter}
 \
 [**A**](#Function-and-Variable-Index_vr_letter-A){.summary-letter}  
[**B**](#Function-and-Variable-Index_vr_letter-B){.summary-letter}  
[**D**](#Function-and-Variable-Index_vr_letter-D){.summary-letter}  
[**E**](#Function-and-Variable-Index_vr_letter-E){.summary-letter}  
[**F**](#Function-and-Variable-Index_vr_letter-F){.summary-letter}  
[**G**](#Function-and-Variable-Index_vr_letter-G){.summary-letter}  
[**I**](#Function-and-Variable-Index_vr_letter-I){.summary-letter}  
[**M**](#Function-and-Variable-Index_vr_letter-M){.summary-letter}  
[**N**](#Function-and-Variable-Index_vr_letter-N){.summary-letter}  
[**O**](#Function-and-Variable-Index_vr_letter-O){.summary-letter}  
[**P**](#Function-and-Variable-Index_vr_letter-P){.summary-letter}  
[**Q**](#Function-and-Variable-Index_vr_letter-Q){.summary-letter}  
[**R**](#Function-and-Variable-Index_vr_letter-R){.summary-letter}  
[**S**](#Function-and-Variable-Index_vr_letter-S){.summary-letter}  
[**T**](#Function-and-Variable-Index_vr_letter-T){.summary-letter}  
[**U**](#Function-and-Variable-Index_vr_letter-U){.summary-letter}  
[**W**](#Function-and-Variable-Index_vr_letter-W){.summary-letter}

---

Index Entry

Section

---

\#

[`#`](#index-_0023):

[Comments](#Comments)

---

\$

[`$`](#index-_0024):

[Indexing](#Indexing)

[`$`](#index-_0024-1):

[Index constructions](#Index-constructions)

---

.

[`.C`](#index-_002eC):

[Foreign language interfaces](#Foreign-language-interfaces)

[`.Call`](#index-_002eCall):

[Foreign language interfaces](#Foreign-language-interfaces)

[`.External`](#index-_002eExternal):

[Foreign language interfaces](#Foreign-language-interfaces)

[`.Fortran`](#index-_002eFortran):

[Foreign language interfaces](#Foreign-language-interfaces)

[`.Internal`](#index-_002eInternal-1):

[.Internal and .Primitive](#g_t_002eInternal-and-_002ePrimitive)

[`.Primitive`](#index-_002ePrimitive-1):

[.Internal and .Primitive](#g_t_002eInternal-and-_002ePrimitive)

---

\[

[`[`](#index-\_005b):

[Indexing](#Indexing)

[`[`](#index-\_005b-1):

[Index constructions](#Index-constructions)

[`[[`](#index-\_005b_005b):

[Indexing](#Indexing)

[`[[`](#index-\_005b_005b-1):

[Index constructions](#Index-constructions)

---

A

[`as.call`](#index-as_002ecall):

[Language objects](#Language-objects)

[`as.character`](#index-as_002echaracter):

[Symbol objects](#Symbol-objects)

[`as.function`](#index-as_002efunction):

[Function objects](#Function-objects)

[`as.list`](#index-as_002elist):

[Language objects](#Language-objects)

[`as.name`](#index-as_002ename):

[Symbol objects](#Symbol-objects)

[`assign`](#index-assign):

[Identifiers](#Identifiers)

[`attr`](#index-attr):

[Attributes](#Attributes)

[`attr<-`](#index-attr_003c_002d):

[Attributes](#Attributes)

[`attributes`](#index-attributes-1):

[Attributes](#Attributes)

[`attributes<-`](#index-attributes_003c_002d):

[Attributes](#Attributes)

---

B

[`baseenv`](#index-baseenv):

[Environment objects](#Environment-objects)

[`basename`](#index-basename):

[Operating system access](#Operating-system-access)

[`body`](#index-body):

[Function objects](#Function-objects)

[`body`](#index-body-1):

[Manipulation of functions](#Manipulation-of-functions)

[`body<-`](#index-body_003c_002d):

[Manipulation of functions](#Manipulation-of-functions)

[`break`](#index-break):

[Looping](#Looping)

[`browser`](#index-browser):

[browser](#browser)

---

D

[`debug`](#index-debug):

[debug/undebug](#debug_002fundebug)

[`dirname`](#index-dirname):

[Operating system access](#Operating-system-access)

[`do.call`](#index-do_002ecall):

[Manipulation of function calls](#Manipulation-of-function-calls)

---

E

[`emptyenv`](#index-emptyenv):

[Environment objects](#Environment-objects)

[`environment`](#index-environment-20):

[Function objects](#Function-objects)

[`environment`](#index-environment-21):

[Manipulation of functions](#Manipulation-of-functions)

[`environment<-`](#index-environment_003c_002d):

[Manipulation of functions](#Manipulation-of-functions)

[`eval`](#index-eval):

[More on evaluation](#More-on-evaluation)

---

F

[`file.access`](#index-file_002eaccess):

[Operating system access](#Operating-system-access)

[`file.append`](#index-file_002eappend):

[Operating system access](#Operating-system-access)

[`file.choose`](#index-file_002echoose):

[Operating system access](#Operating-system-access)

[`file.copy`](#index-file_002ecopy):

[Operating system access](#Operating-system-access)

[`file.create`](#index-file_002ecreate):

[Operating system access](#Operating-system-access)

[`file.exists`](#index-file_002eexists):

[Operating system access](#Operating-system-access)

[`file.info`](#index-file_002einfo):

[Operating system access](#Operating-system-access)

[`file.path`](#index-file_002epath):

[Operating system access](#Operating-system-access)

[`file.remove`](#index-file_002eremove):

[Operating system access](#Operating-system-access)

[`file.rename`](#index-file_002erename):

[Operating system access](#Operating-system-access)

[`file.show`](#index-file_002eshow):

[Operating system access](#Operating-system-access)

[`for`](#index-for):

[for](#for)

[`formals`](#index-formals):

[Function objects](#Function-objects)

[`formals`](#index-formals-1):

[Manipulation of functions](#Manipulation-of-functions)

[`formals<-`](#index-formals_003c_002d):

[Manipulation of functions](#Manipulation-of-functions)

---

G

[`get`](#index-get):

[Identifiers](#Identifiers)

---

I

[`is.na`](#index-is_002ena):

[NA handling](#NA-handling)

[`is.nan`](#index-is_002enan):

[NA handling](#NA-handling)

---

M

[`match.arg`](#index-match_002earg):

[Argument matching](#Argument-matching)

[`match.call`](#index-match_002ecall):

[Argument matching](#Argument-matching)

[`match.call`](#index-match_002ecall-1):

[Manipulation of function calls](#Manipulation-of-function-calls)

[`match.fun`](#index-match_002efun):

[Argument matching](#Argument-matching)

[`missing`](#index-missing):

[NA handling](#NA-handling)

[`mode`](#index-mode-3):

[Objects](#Objects)

---

N

[`NA`](#index-NA):

[NA handling](#NA-handling)

[`NA`](#index-NA-1):

[Indexing by vectors](#Indexing-by-vectors)

[`names`](#index-names):

[Names](#Names)

[`names<-`](#index-names_003c_002d):

[Names](#Names)

[`NaN`](#index-NaN):

[NA handling](#NA-handling)

[`new.env`](#index-new_002eenv):

[Environment objects](#Environment-objects)

[`next`](#index-next):

[Looping](#Looping)

[`NextMethod`](#index-NextMethod):

[NextMethod](#NextMethod)

[`NULL`](#index-NULL):

[NULL object](#NULL-object)

---

O

[`on.exit`](#index-on_002eexit):

[on.exit](#on_002eexit)

---

P

[`pairlist`](#index-pairlist):

[Pairlist objects](#Pairlist-objects)

[`path.expand`](#index-path_002eexpand):

[Operating system access](#Operating-system-access)

[`proc.time`](#index-proc_002etime):

[Operating system access](#Operating-system-access)

---

Q

[`quote`](#index-quote):

[Language objects](#Language-objects)

---

R

[`repeat`](#index-repeat):

[repeat](#repeat)

---

S

[`stop`](#index-stop):

[stop](#stop)

[`storage.mode`](#index-storage_002emode):

[Objects](#Objects)

[`substitute`](#index-substitute):

[Substitutions](#Substitutions)

[`switch`](#index-switch):

[switch](#switch)

[`Sys.getenv`](#index-Sys_002egetenv):

[Operating system access](#Operating-system-access)

[`Sys.getlocale`](#index-Sys_002egetlocale):

[Operating system access](#Operating-system-access)

[`Sys.localeconv`](#index-Sys_002elocaleconv):

[Operating system access](#Operating-system-access)

[`Sys.putenv`](#index-Sys_002eputenv):

[Operating system access](#Operating-system-access)

[`Sys.putlocale`](#index-Sys_002eputlocale):

[Operating system access](#Operating-system-access)

[`Sys.time`](#index-Sys_002etime):

[Operating system access](#Operating-system-access)

[`Sys.timezone`](#index-Sys_002etimezone):

[Operating system access](#Operating-system-access)

[`system`](#index-system):

[Operating system access](#Operating-system-access)

[`system.time`](#index-system_002etime):

[Operating system access](#Operating-system-access)

---

T

[`trace`](#index-trace):

[trace/untrace](#trace_002funtrace)

[`traceback`](#index-traceback):

[traceback](#traceback)

[`typeof`](#index-typeof):

[Objects](#Objects)

---

U

[`undebug`](#index-undebug):

[debug/undebug](#debug_002fundebug)

[`unlink`](#index-unlink):

[Operating system access](#Operating-system-access)

[`untrace`](#index-untrace):

[trace/untrace](#trace_002funtrace)

[`UseMethod`](#index-UseMethod):

[UseMethod](#UseMethod)

---

W

[`warning`](#index-warning):

[warning](#warning)

[`warnings`](#index-warnings):

[warning](#warning)

[`while`](#index-while):

[while](#while)

---

---

Jump to:   [**\#**](#Function-and-Variable-Index_vr_symbol-1){.summary-letter}  
[**\$**](#Function-and-Variable-Index_vr_symbol-2){.summary-letter}  
[**.**](#Function-and-Variable-Index_vr_symbol-3){.summary-letter}  
[**\[**](#Function-and-Variable-Index_vr_symbol-4){.summary-letter}
 \
 [**A**](#Function-and-Variable-Index_vr_letter-A){.summary-letter}  
[**B**](#Function-and-Variable-Index_vr_letter-B){.summary-letter}  
[**D**](#Function-and-Variable-Index_vr_letter-D){.summary-letter}  
[**E**](#Function-and-Variable-Index_vr_letter-E){.summary-letter}  
[**F**](#Function-and-Variable-Index_vr_letter-F){.summary-letter}  
[**G**](#Function-and-Variable-Index_vr_letter-G){.summary-letter}  
[**I**](#Function-and-Variable-Index_vr_letter-I){.summary-letter}  
[**M**](#Function-and-Variable-Index_vr_letter-M){.summary-letter}  
[**N**](#Function-and-Variable-Index_vr_letter-N){.summary-letter}  
[**O**](#Function-and-Variable-Index_vr_letter-O){.summary-letter}  
[**P**](#Function-and-Variable-Index_vr_letter-P){.summary-letter}  
[**Q**](#Function-and-Variable-Index_vr_letter-Q){.summary-letter}  
[**R**](#Function-and-Variable-Index_vr_letter-R){.summary-letter}  
[**S**](#Function-and-Variable-Index_vr_letter-S){.summary-letter}  
[**T**](#Function-and-Variable-Index_vr_letter-T){.summary-letter}  
[**U**](#Function-and-Variable-Index_vr_letter-U){.summary-letter}  
[**W**](#Function-and-Variable-Index_vr_letter-W){.summary-letter}

---

---

## Concept Index

---

Jump to:   [**\#**](#Concept-Index_cp_symbol-1){.summary-letter}  
[**.**](#Concept-Index_cp_symbol-2){.summary-letter}  \
 [**A**](#Concept-Index_cp_letter-A){.summary-letter}  
[**B**](#Concept-Index_cp_letter-B){.summary-letter}  
[**C**](#Concept-Index_cp_letter-C){.summary-letter}  
[**E**](#Concept-Index_cp_letter-E){.summary-letter}  
[**F**](#Concept-Index_cp_letter-F){.summary-letter}  
[**I**](#Concept-Index_cp_letter-I){.summary-letter}  
[**M**](#Concept-Index_cp_letter-M){.summary-letter}  
[**N**](#Concept-Index_cp_letter-N){.summary-letter}  
[**O**](#Concept-Index_cp_letter-O){.summary-letter}  
[**P**](#Concept-Index_cp_letter-P){.summary-letter}  
[**S**](#Concept-Index_cp_letter-S){.summary-letter}  
[**T**](#Concept-Index_cp_letter-T){.summary-letter}  
[**V**](#Concept-Index_cp_letter-V){.summary-letter}

---

Index Entry

Section

---

\#

[\#line](#index-_0023line):

[Directives](#Directives)

---

.

[.Internal](#index-_002eInternal):

[Builtin objects and special forms](#Builtin-objects-and-special-forms)

[.Primitive](#index-_002ePrimitive):

[Builtin objects and special forms](#Builtin-objects-and-special-forms)

---

A

[argument](#index-argument):

[Function objects](#Function-objects)

[argument](#index-argument-1):

[Syntax and examples](#Syntax-and-examples)

[argument, default values](#index-argument_002c-default-values):

[Arguments](#Arguments)

[assignment](#index-assignment):

[Function objects](#Function-objects)

[assignment](#index-assignment-1):

[Function calls](#Function-calls)

[assignment](#index-assignment-2):

[Operators](#Operators)

[assignment](#index-assignment-3):

[Subset assignment](#Subset-assignment)

[assignment](#index-assignment-4):

[Global environment](#Global-environment)

[assignment](#index-assignment-5):

[Argument evaluation](#Argument-evaluation)

[assignment](#index-assignment-6):

[Scope](#Scope)

[assignment](#index-assignment-7):

[UseMethod](#UseMethod)

[assignment](#index-assignment-8):

[UseMethod](#UseMethod)

[assignment](#index-assignment-9):

[More on evaluation](#More-on-evaluation)

[assignment](#index-assignment-10):

[Manipulation of function calls](#Manipulation-of-function-calls)

[assignment](#index-assignment-11):

[Infix and prefix operators](#Infix-and-prefix-operators)

[assignment](#index-assignment-12):

[Infix and prefix operators](#Infix-and-prefix-operators)

[atomic](#index-atomic):

[Vector objects](#Vector-objects)

[attributes](#index-attributes):

[Attributes](#Attributes)

---

B

[binding](#index-binding):

[Scope](#Scope)

[binding](#index-binding-1):

[Scope](#Scope)

---

C

[call](#index-call):

[Language objects](#Language-objects)

[call stack](#index-call-stack):

[Stacks](#Stacks)

[coercion](#index-coercion):

[Objects](#Objects)

[coercion](#index-coercion-1):

[Symbol objects](#Symbol-objects)

[coercion](#index-coercion-2):

[Any-type](#Any_002dtype)

[coercion](#index-coercion-3):

[Classes](#Classes)

[coercion](#index-coercion-4):

[NA handling](#NA-handling)

[comments](#index-comments):

[Comments](#Comments)

[complex assignment](#index-complex-assignment):

[Subset assignment](#Subset-assignment)

---

E

[environment](#index-environment):

[Function objects](#Function-objects)

[environment](#index-environment-1):

[Function objects](#Function-objects)

[environment](#index-environment-2):

[Promise objects](#Promise-objects)

[environment](#index-environment-3):

[Environment objects](#Environment-objects)

[environment](#index-environment-4):

[Control structures](#Control-structures)

[environment](#index-environment-5):

[Global environment](#Global-environment)

[environment](#index-environment-6):

[Lexical environment](#Lexical-environment)

[environment](#index-environment-7):

[Stacks](#Stacks)

[environment](#index-environment-8):

[Search path](#Search-path)

[environment](#index-environment-9):

[Evaluation environment](#Evaluation-environment)

[environment](#index-environment-10):

[Argument evaluation](#Argument-evaluation)

[environment](#index-environment-11):

[Argument evaluation](#Argument-evaluation)

[environment](#index-environment-12):

[Scope](#Scope)

[environment](#index-environment-13):

[UseMethod](#UseMethod)

[environment](#index-environment-14):

[UseMethod](#UseMethod)

[environment](#index-environment-15):

[More on evaluation](#More-on-evaluation)

[environment](#index-environment-16):

[Manipulation of functions](#Manipulation-of-functions)

[environment](#index-environment-17):

[Operating system access](#Operating-system-access)

[environment](#index-environment-18):

[Debugging](#Debugging)

[environment](#index-environment-19):

[Debugging](#Debugging)

[environment, evaluation](#index-environment_002c-evaluation):

[Lexical environment](#Lexical-environment)

[environment, evaluation](#index-environment_002c-evaluation-1):

[Lexical environment](#Lexical-environment)

[environment, evaluation](#index-environment_002c-evaluation-2):

[Argument evaluation](#Argument-evaluation)

[evaluation](#index-evaluation):

[Stacks](#Stacks)

[evaluation](#index-evaluation-1):

[Evaluation environment](#Evaluation-environment)

[evaluation](#index-evaluation-2):

[Argument evaluation](#Argument-evaluation)

[evaluation](#index-evaluation-3):

[Scope](#Scope)

[evaluation](#index-evaluation-4):

[Inheritance](#Inheritance)

[evaluation](#index-evaluation-5):

[UseMethod](#UseMethod)

[evaluation](#index-evaluation-6):

[More on evaluation](#More-on-evaluation)

[evaluation](#index-evaluation-7):

[Manipulation of function calls](#Manipulation-of-function-calls)

[evaluation, argument](#index-evaluation_002c-argument):

[Argument evaluation](#Argument-evaluation)

[evaluation, expression](#index-evaluation_002c-expression):

[Expression objects](#Expression-objects)

[evaluation, expression](#index-evaluation_002c-expression-1):

[Promise objects](#Promise-objects)

[evaluation, expression](#index-evaluation_002c-expression-2):

[Arguments](#Arguments)

[evaluation, lazy](#index-evaluation_002c-lazy):

[Objects](#Objects)

[evaluation, lazy](#index-evaluation_002c-lazy-1):

[Substitutions](#Substitutions)

[evaluation, lazy](#index-evaluation_002c-lazy-2):

[Substitutions](#Substitutions)

[evaluation, statement](#index-evaluation_002c-statement):

[Control structures](#Control-structures)

[evaluation, symbol](#index-evaluation_002c-symbol):

[Attributes](#Attributes)

[evaluation, symbol](#index-evaluation_002c-symbol-1):

[Symbol lookup](#Symbol-lookup)

[evaluation, symbol](#index-evaluation_002c-symbol-2):

[Scope](#Scope)

[expression](#index-expression):

[Introduction](#Introduction)

[expression](#index-expression-1):

[Language objects](#Language-objects)

[expression](#index-expression-2):

[Separators](#Separators)

[expression object](#index-expression-object):

[Expression objects](#Expression-objects)

[expression object](#index-expression-object-1):

[Expression objects](#Expression-objects)

---

F

[frame](#index-frame):

[Lexical environment](#Lexical-environment)

[function](#index-function):

[Function objects](#Function-objects)

[function](#index-function-1):

[Function objects](#Function-objects)

[function](#index-function-2):

[Function objects](#Function-objects)

[function](#index-function-3):

[Builtin objects and special forms](#Builtin-objects-and-special-forms)

[function](#index-function-4):

[Builtin objects and special forms](#Builtin-objects-and-special-forms)

[function](#index-function-5):

[Promise objects](#Promise-objects)

[function](#index-function-6):

[Dot-dot-dot](#Dot_002ddot_002ddot)

[function](#index-function-7):

[Function calls](#Function-calls)

[function](#index-function-8):

[Lexical environment](#Lexical-environment)

[function](#index-function-9):

[Lexical environment](#Lexical-environment)

[function](#index-function-10):

[Stacks](#Stacks)

[function](#index-function-11):

[Writing functions](#Writing-functions)

[function](#index-function-12):

[Syntax and examples](#Syntax-and-examples)

[function](#index-function-13):

[Syntax and examples](#Syntax-and-examples)

[function](#index-function-14):

[Arguments](#Arguments)

[function](#index-function-15):

[Evaluation environment](#Evaluation-environment)

[function](#index-function-16):

[Argument matching](#Argument-matching)

[function](#index-function-17):

[Argument evaluation](#Argument-evaluation)

[function](#index-function-18):

[Argument evaluation](#Argument-evaluation)

[function](#index-function-19):

[Argument evaluation](#Argument-evaluation)

[function](#index-function-20):

[Argument evaluation](#Argument-evaluation)

[function](#index-function-21):

[Scope](#Scope)

[function](#index-function-22):

[Scope](#Scope)

[function](#index-function-23):

[Scope](#Scope)

[function](#index-function-24):

[Object-oriented programming](#Object_002doriented-programming)

[function](#index-function-25):

[Definition](#Definition)

[function](#index-function-26):

[Manipulation of function calls](#Manipulation-of-function-calls)

[function](#index-function-27):

[Manipulation of functions](#Manipulation-of-functions)

[function](#index-function-28):

[Manipulation of functions](#Manipulation-of-functions)

[function](#index-function-29):

[Internal representation](#Internal-representation)

[function](#index-function-30):

[Function calls (expressions)](#Function-calls-_0028expressions_0029)

[function](#index-function-31):

[Function definitions](#Function-definitions)

[function argument](#index-function-argument):

[Promise objects](#Promise-objects)

[function argument](#index-function-argument-1):

[Dot-dot-dot](#Dot_002ddot_002ddot)

[function arguments](#index-function-arguments):

[Function calls](#Function-calls)

[function invocation](#index-function-invocation):

[Function calls](#Function-calls)

[function, accessor](#index-function_002c-accessor):

[Attributes](#Attributes)

[function, anonymous](#index-function_002c-anonymous):

[Syntax and examples](#Syntax-and-examples)

[function, assignment](#index-function_002c-assignment):

[Function calls](#Function-calls)

[function, generic](#index-function_002c-generic):

[Object-oriented programming](#Object_002doriented-programming)

[function, generic](#index-function_002c-generic-1):

[Definition](#Definition)

[function, generic](#index-function_002c-generic-2):

[Definition](#Definition)

[function, generic](#index-function_002c-generic-3):

[Definition](#Definition)

[function, generic](#index-function_002c-generic-4):

[Inheritance](#Inheritance)

[function, generic](#index-function_002c-generic-5):

[Method dispatching](#Method-dispatching)

[function, generic](#index-function_002c-generic-6):

[Writing methods](#Writing-methods)

[function, generic](#index-function_002c-generic-7):

[Writing methods](#Writing-methods)

[function, internal](#index-function_002c-internal):

[Argument evaluation](#Argument-evaluation)

[function, internal](#index-function_002c-internal-1):

[Group methods](#Group-methods)

[function, modeling](#index-function_002c-modeling):

[Factors](#Factors)

---

I

[identifier](#index-identifier):

[Identifiers](#Identifiers)

[index](#index-index):

[Vector objects](#Vector-objects)

[index](#index-index-1):

[List objects](#List-objects)

[index](#index-index-2):

[Indexing](#Indexing)

[index](#index-index-3):

[Indexing by vectors](#Indexing-by-vectors)

[index](#index-index-4):

[Indexing matrices and arrays](#Indexing-matrices-and-arrays)

[index](#index-index-5):

[Indexing matrices and arrays](#Indexing-matrices-and-arrays)

---

M

[mode](#index-mode):

[Objects](#Objects)

[mode](#index-mode-1):

[Vector objects](#Vector-objects)

[mode](#index-mode-2):

[Symbol objects](#Symbol-objects)

[modeling function](#index-modeling-function):

[Factors](#Factors)

---

N

[name](#index-name):

[Language objects](#Language-objects)

[name](#index-name-1):

[Symbol objects](#Symbol-objects)

[name](#index-name-2):

[Symbol lookup](#Symbol-lookup)

[name](#index-name-3):

[Propagation of names](#Propagation-of-names)

[name](#index-name-4):

[Scope of variables](#Scope-of-variables)

[name](#index-name-5):

[Arguments](#Arguments)

[name](#index-name-6):

[Argument matching](#Argument-matching)

[name](#index-name-7):

[Argument evaluation](#Argument-evaluation)

[name](#index-name-8):

[Method dispatching](#Method-dispatching)

[name](#index-name-9):

[NextMethod](#NextMethod)

[name](#index-name-10):

[Direct manipulation of language objects](#Direct-manipulation-of-language-objects)

[name](#index-name-11):

[Debugging](#Debugging)

[namespace](#index-namespace):

[Search path](#Search-path)

---

O

[object](#index-object):

[Objects](#Objects)

[object](#index-object-1):

[Objects](#Objects)

[object](#index-object-2):

[Symbol objects](#Symbol-objects)

[object](#index-object-3):

[Attributes](#Attributes)

[object](#index-object-4):

[Method dispatching](#Method-dispatching)

[object-oriented](#index-object_002doriented):

[Object-oriented programming](#Object_002doriented-programming)

[object-oriented](#index-object_002doriented-1):

[Definition](#Definition)

---

P

[parsing](#index-parsing):

[Language objects](#Language-objects)

[parsing](#index-parsing-1):

[Symbol objects](#Symbol-objects)

[parsing](#index-parsing-2):

[Evaluation of expressions](#Evaluation-of-expressions)

[parsing](#index-parsing-3):

[Computing on the language](#Computing-on-the-language)

[parsing](#index-parsing-4):

[Direct manipulation of language objects](#Direct-manipulation-of-language-objects)

[parsing](#index-parsing-5):

[Substitutions](#Substitutions)

[parsing](#index-parsing-6):

[Parser](#Parser)

[parsing](#index-parsing-7):

[Internal representation](#Internal-representation)

[partial matching](#index-partial-matching):

[Indexing by vectors](#Indexing-by-vectors)

[promise](#index-promise):

[Promise objects](#Promise-objects)

---

S

[scope](#index-scope):

[Scope of variables](#Scope-of-variables)

[scope](#index-scope-1):

[Stacks](#Stacks)

[scope](#index-scope-2):

[Scope](#Scope)

[scope](#index-scope-3):

[Scope](#Scope)

[scope](#index-scope-4):

[Scope](#Scope)

[scope](#index-scope-5):

[More on evaluation](#More-on-evaluation)

[search path](#index-search-path):

[Search path](#Search-path)

[statement](#index-statement):

[Language objects](#Language-objects)

[symbol](#index-symbol):

[Symbol objects](#Symbol-objects)

[symbol](#index-symbol-1):

[Symbol objects](#Symbol-objects)

[symbol](#index-symbol-2):

[Symbol lookup](#Symbol-lookup)

[symbol](#index-symbol-3):

[Scope](#Scope)

[symbol](#index-symbol-4):

[Substitutions](#Substitutions)

[symbol](#index-symbol-5):

[Manipulation of function calls](#Manipulation-of-function-calls)

---

T

[token](#index-token):

[Expression objects](#Expression-objects)

[type](#index-type):

[Objects](#Objects)

[type](#index-type-1):

[Objects](#Objects)

[type](#index-type-2):

[Basic types](#Basic-types)

[type](#index-type-3):

[Vector objects](#Vector-objects)

[type](#index-type-4):

[Names](#Names)

[type](#index-type-5):

[NA handling](#NA-handling)

---

V

[value](#index-value):

[Symbol lookup](#Symbol-lookup)

[variable](#index-variable):

[Objects](#Objects)

[vector](#index-vector):

[Vector objects](#Vector-objects)

[vector](#index-vector-1):

[Dimensions](#Dimensions)

[vector](#index-vector-2):

[Operators](#Operators)

---

---

Jump to:   [**\#**](#Concept-Index_cp_symbol-1){.summary-letter}  
[**.**](#Concept-Index_cp_symbol-2){.summary-letter}  \
 [**A**](#Concept-Index_cp_letter-A){.summary-letter}  
[**B**](#Concept-Index_cp_letter-B){.summary-letter}  
[**C**](#Concept-Index_cp_letter-C){.summary-letter}  
[**E**](#Concept-Index_cp_letter-E){.summary-letter}  
[**F**](#Concept-Index_cp_letter-F){.summary-letter}  
[**I**](#Concept-Index_cp_letter-I){.summary-letter}  
[**M**](#Concept-Index_cp_letter-M){.summary-letter}  
[**N**](#Concept-Index_cp_letter-N){.summary-letter}  
[**O**](#Concept-Index_cp_letter-O){.summary-letter}  
[**P**](#Concept-Index_cp_letter-P){.summary-letter}  
[**S**](#Concept-Index_cp_letter-S){.summary-letter}  
[**T**](#Concept-Index_cp_letter-T){.summary-letter}  
[**V**](#Concept-Index_cp_letter-V){.summary-letter}

---

---

## Appendix A References

Richard A. Becker, John M. Chambers and Allan R. Wilks (1988), _The New
S Language._ Chapman & Hall, New York. This book is often called the
"_Blue Book_".

---

#### Footnotes

[(1)](#DOCF1)

actually two, but this draft manual predates the **methods** package.

[(2)](#DOCF2)

Evaluation always takes place in an
environment. See [Scope of variables](#Scope-of-variables) for more
details.

[(3)](#DOCF3)

Looping is the repeated evaluation of a statement or block of
statements.

[(4)](#DOCF4)

such as `U+A0`, non-breaking space, and `U+3000`, ideographic space.

---
