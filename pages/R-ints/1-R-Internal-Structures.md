1 R Internal Structures

---

This chapter is the beginnings of documentation about R internal
structures. It is written for the core team and others studying the code
in the `src/main` directory.

It is a work-in-progress and should be checked against the current
version of the source code. Versions for R 2.x.y contain historical
comments about when features were introduced: this version is for the
3.x.y series.

---

• [SEXPs](#SEXPs)     
 • [Environments and variable lookup](#Environments-and-variable-lookup)     
 • [Attributes](#Attributes)     
 • [Contexts](#Contexts)     
 • [Argument evaluation](#Argument-evaluation)     
 • [Autoprinting](#Autoprinting)     
 • [The write barrier](#The-write-barrier)     
 • [Serialization Formats](#Serialization-Formats)     
 • [Encodings for CHARSXPs](#Encodings-for-CHARSXPs)     
 • [The CHARSXP cache](#The-CHARSXP-cache)     
 • [Warnings and errors](#Warnings-and-errors)     
 • [S4 objects](#S4-objects)     
 • [Memory allocators](#Memory-allocators)     
 • [Internal use of global and base environments](#Internal-use-of-global-and-base-environments)     
 • [Modules](#Modules)     
 • [Visibility](#Visibility)     
 • [Lazy loading](#Lazy-loading)

---

---

### 1.1 SEXPs

What R users think of as _variables_ or _objects_ are symbols which are
bound to a value. The value can be thought of as either a `SEXP` (a
pointer), or the structure it points to, a `SEXPREC` (and there are
alternative forms used for vectors, namely `VECSXP` pointing to
`VECTOR_SEXPREC` structures). So the basic building blocks of R objects
are often called _nodes_, meaning `SEXPREC`s or `VECTOR_SEXPREC`s.

Note that the internal structure of the `SEXPREC` is not made available
to R Extensions: rather `SEXP` is an opaque pointer, and the internals
can only be accessed by the functions provided.

Both types of node structure have as their first three fields a 64-bit
`sxpinfo` header and then three pointers (to the attributes and the

#### 1.1.1 SEXPTYPEs

Currently `SEXPTYPE`s 0:10 and 13:25 are in use. Values 11 and 12 were
used for internal factors and ordered factors and have since been
withdrawn. Note that the `SEXPTYPE` numbers are stored in `save`d
objects and that the ordering of the types is used, so the gap cannot
easily be reused.

> no SEXPTYPE Description
>
> ---
>
> `0` `NILSXP` `NULL` > `1` `SYMSXP` symbols
> `2` `LISTSXP` pairlists
> `3` `CLOSXP` closures
> `4` `ENVSXP` environments
> `5` `PROMSXP` promises
> `6` `LANGSXP` language objects
> `7` `SPECIALSXP` special functions
> `8` `BUILTINSXP` builtin functions
> `9` `CHARSXP` internal character strings
> `10` `LGLSXP` logical vectors
> `13` `INTSXP` integer vectors
> `14` `REALSXP` numeric vectors
> `15` `CPLXSXP` complex vectors
> `16` `STRSXP` character vectors
> `17` `DOTSXP` dot-dot-dot object
> `18` `ANYSXP` make "any" args work
> `19` `VECSXP` list (generic vector)
> `20` `EXPRSXP` expression vector
> `21` `BCODESXP` byte code
> `22` `EXTPTRSXP` external pointer
> `23` `WEAKREFSXP` weak reference
> `24` `RAWSXP` raw vector
> `25` `S4SXP` S4 classes not of simple type

Many of these will be familiar from R level: the atomic vector types are
`LGLSXP`, `INTSXP`, `REALSXP`, `CPLXSP`, `STRSXP` and `RAWSXP`. Lists
are `VECSXP` and names (also known as symbols) are `SYMSXP`. Pairlists
(`LISTSXP`, the name going back to the origins of R as a Scheme-like
language) are rarely seen at R level, but are for example used for
argument lists. Character vectors are effectively lists all of whose
elements are `CHARSXP`, a type that is rarely visible at R level.

Language objects (`LANGSXP`) are calls (including formulae and so on).
Internally they are pairlists with first element a
reference[^2^](#FOOT2) to the function to be called with
remaining elements the actual arguments for the call (and with the tags
if present giving the specified argument names). Although this is not
enforced, many places in the code assume that the pairlist is of length
one or more, often without checking.

Expressions are of type `EXPRSXP`: they are a vector of (usually
language) objects most often seen as the result of `parse()`.

The functions are of types `CLOSXP`, `SPECIALSXP` and `BUILTINSXP`:
where `SEXPTYPE`s are stored in an integer these are sometimes lumped
into a pseudo-type `FUNSXP` with code 99. Functions defined via
`function` are of type `CLOSXP` and have formals, body and environment.

The `SEXPTYPE` `S4SXP` is for S4 objects which do not consist solely of
a simple type such as an atomic vector or function.

---

#### 1.1.2 Rest of header

Note that the size and structure of the header changed in R 3.5.0: see
earlier editions of this manual for the previous layout.

The `sxpinfo` header is defined as a 64-bit C structure by

```r
#define NAMED_BITS 16
struct sxpinfo_struct {
    SEXPTYPE type      :  5;  /* discussed above */
    unsigned int scalar:  1;  /* is this a numeric vector of length 1?
    unsigned int obj   :  1;  /* is this an object with a class attribute? */
    unsigned int alt   :  1;  /* is this an ALTREP object? */
    unsigned int gp    : 16;  /* general purpose, see below */
    unsigned int mark  :  1;  /* mark object as ‘in use’ in GC */
    unsigned int debug :  1;
    unsigned int trace :  1;
    unsigned int spare :  1;  /* debug once and with reference counting */
    unsigned int gcgen :  1;  /* generation for GC */
    unsigned int gccls :  3;  /* class of node for GC */
    unsigned int named : NAMED_BITS; /* used to control copying */
    unsigned int extra : 32 - NAMED_BITS;
}; /*           Tot: 64 */
```

The `debug` bit is used for closures and environments. For closures it
is set by `debug()` and unset by `undebug()`, and indicates that
evaluations of the function should be run under the browser. For
environments it indicates whether the browsing is in single-step mode.

The `trace` bit is used for functions for `trace()` and for other
objects when tracing duplications (see `tracemem`).

The `spare` bit is used for closures to mark them for one-time
debugging.

The `named` field is set and accessed by the `SET_NAMED` and `NAMED`
macros, and take values `0`, `1` and `2`, or possibly higher if
`NAMEDMAX` is set to a higher value. R has a 'call by value' illusion,
so an assignment like

```r
b <- a
```

appears to make a copy of `a` and refer to it as `b`. However, if
neither `a` nor `b` are subsequently altered there is no need to copy.
What really happens is that a new symbol `b` is bound to the same value
as `a` and the `named` field on the value object is set (in this case to
`2`). When an object is about to be altered, the `named` field is
consulted. A value of `2` or more means that the object must be
duplicated before being changed. (Note that this does not say that it is
necessary to duplicate, only that it should be duplicated whether
necessary or not.) A value of `0` means that it is known that no other
`SEXP` shares data with this object, and so it may safely be altered. A
value of `1` is used for situations like

```r
dim(a) <- c(7, 2)
```

where in principle two copies of `a` exist for the duration of the
computation as (in principle)

```r
a <- `dim<-`(a, c(7, 2))
```

but for no longer, and so some primitive functions can be optimized to
avoid a copy in this case.

The `gp` bits are by definition 'general purpose'. We label these from 0
to 15. Bits 0--5 and bits 14--15 have been used as described below
(mainly from detective work on the sources).

The bits can be accessed and set by the `LEVELS` and `SETLEVELS` macros,
which names appear to date back to the internal factor and ordered types
and are now used in only a few places in the code. The `gp` field is
serialized/unserialized for the `SEXPTYPE`s other than `NILSXP`,
`SYMSXP` and `ENVSXP`.

Bits 14 and 15 of `gp` are used for 'fancy bindings'. Bit 14 is used to
lock a binding or an environment, and bit 15 is used to indicate an
active binding. (For the definition of an 'active binding' see the
header comments in file `src/main/envir.c`.) Bit 15 is used for
an environment to indicate if it participates in the global cache.

The macros `ARGUSED` and `SET_ARGUSED` are used when matching actual and
formal function arguments, and take the values 0, 1 and 2.

The macros `MISSING` and `SET_MISSING` are used for pairlists of
arguments. Four bits are reserved, but only two are used (and exactly
what for is not explained). It seems that bit 0 is used by `matchArgs`
to mark missingness on the returned argument list, and bit 1 is used to
mark the use of a default value for an argument copied to the evaluation
frame of a closure.

Bit 0 is used by macros `DDVAL` and `SET_DDVAL`. This indicates that a
`SYMSXP` is one of the symbols `..n` which are implicitly created when
`...` is processed, and so indicates that it may need to be looked up in
a `DOTSXP`.

Bit 0 is used for `PRSEEN`, a flag to indicate if a promise has already
been seen during the evaluation of the promise (and so to avoid
recursive loops).

Bit 0 is used for `HASHASH`, on the `PRINTNAME` of the `TAG` of the
frame of an environment. (This bit is not serialized for `CHARSXP`
objects.)

Bits 0 and 1 are used for weak references (to indicate 'ready to
finalize', 'finalize on exit').

Bit 0 is used by the condition handling system (on a `VECSXP`) to
indicate a calling handler.

Bit 4 is turned on to mark S4 objects.

Bits 1, 2, 3, 5 and 6 are used for a `CHARSXP` to denote its encoding.
Bit 1 indicates that the `CHARSXP` should be treated as a set of bytes,
not necessarily representing a character in any known encoding. Bits 2,
3 and 6 are used to indicate that it is known to be in Latin-1, UTF-8 or
ASCII respectively.

Bit 5 for a `CHARSXP` indicates that it is hashed by its address, that
is `NA_STRING` or is in the `CHARSXP` cache (this is not serialized).
Only exceptionally is a `CHARSXP` not hashed, and this should never
happen in end-user code.

---

#### 1.1.3 The 'data'

A `SEXPREC` is a C structure containing the 32-bit header as described
above, three pointers (to the attributes, previous and next node) and
the node data, a union

```r
union {
    struct primsxp_struct primsxp;
    struct symsxp_struct symsxp;
    struct listsxp_struct listsxp;
    struct envsxp_struct envsxp;
    struct closxp_struct closxp;
    struct promsxp_struct promsxp;
} u;
```

All of these alternatives apart from the first (an `int`) are three
pointers, so the union occupies three words.

The vector types are `RAWSXP`, `CHARSXP`, `LGLSXP`, `INTSXP`, `REALSXP`,
`CPLXSXP`, `STRSXP`, `VECSXP`, `EXPRSXP` and `WEAKREFSXP`. Remember that
such types are a `VECTOR_SEXPREC`, which again consists of the header
and the same three pointers, but followed by two integers giving the
length and 'true length'[^3^](#FOOT3) of the vector, and then
followed by the data (aligned as required: on most 32-bit systems with a
24-byte `VECTOR_SEXPREC` node the data can follow immediately after the
node). The data are a block of memory of the appropriate length to store
'true length' elements (rounded up to a multiple of 8 bytes, with the
8-byte blocks being the 'Vcells' referred in the documentation for
`gc()`).

The 'data' for the various types are given in the table below. A lot of
this is interpretation, i.e. the types are not checked.

`NILSXP`

: There is only one object of type `NILSXP`, `R_NilValue`, with no
data.

`SYMSXP`

: Pointers to three nodes, the name, value and internal, accessed by
`PRINTNAME` (a `CHARSXP`), `SYMVALUE` and `INTERNAL`. (If the
symbol's value is a `.Internal` function, the last is a pointer to
the appropriate `SEXPREC`.) Many symbols have `SYMVALUE`
`R_UnboundValue`.

`LISTSXP`

: Pointers to the CAR, CDR (usually a `LISTSXP` or `NULL`) and TAG (a
`SYMSXP` or `NULL`).

`CLOSXP`

: Pointers to the formals (a pairlist), the body and the environment.

`ENVSXP`

: Pointers to the frame, enclosing environment and hash table (`NULL`
or a `VECSXP`). A frame is a tagged pairlist with tag the symbol and
CAR the bound value.

`PROMSXP`

: Pointers to the value, expression and environment (in which to
evaluate the expression). Once an promise has been evaluated, the
environment is set to `NULL`.

`LANGSXP`

: A special type of `LISTSXP` used for function calls. (The CAR
references the function (perhaps via a symbol or language object),
and the CDR the argument list with tags for named arguments.)
R-level documentation references to 'expressions' / 'language
objects' are mainly `LANGSXP`s, but can be symbols (`SYMSXP`s) or
expression vectors (`EXPRSXP`s).

`SPECIALSXP`\
`BUILTINSXP`

: An integer giving the offset into the table of
primitives/`.Internal`s.

`CHARSXP`

: `length`, `truelength` followed by a block of bytes (allowing for
the `nul` terminator).

`LGLSXP`\
`INTSXP`

: `length`, `truelength` followed by a block of C `int`s (which are 32
bits on all R platforms).

`REALSXP`

: `length`, `truelength` followed by a block of C `double`s.

`CPLXSXP`

: `length`, `truelength` followed by a block of C99 `double complex`s.

`STRSXP`

: `length`, `truelength` followed by a block of pointers (`SEXP`s
pointing to `CHARSXP`s).

`DOTSXP`

: A special type of `LISTSXP` for the value bound to a `...` symbol: a
pairlist of promises.

`ANYSXP`

: This is used as a place holder for any type: there are no actual
objects of this type.

`VECSXP`\
`EXPRSXP`

: `length`, `truelength` followed by a block of pointers. These are
internally identical (and identical to `STRSXP`) but differ in the
interpretations placed on the elements.

`BCODESXP`

: For the 'byte-code' objects generated by the compiler.

`EXTPTRSXP`

: Has three pointers, to the pointer, the protection value (an R
object which if alive protects this object) and a tag (a `SYMSXP`?).

`WEAKREFSXP`

: A `WEAKREFSXP` is a special `VECSXP` of length 4, with elements
'`key`', '`value`', '`finalizer`' and
'`next`'. The '`key`' is `NULL`, an environment or
an external pointer, and the '`finalizer`' is a function or
`NULL`.

`RAWSXP`

: `length`, `truelength` followed by a block of bytes.

`S4SXP`

: two unused pointers and a tag.

---

#### 1.1.4 Allocation classes

As we have seen, the field `gccls` in the header is three bits to label
up to 8 classes of nodes. Non-vector nodes are of class 0, and 'small'
vector nodes are of classes 1 to 5, with a class for custom allocator
vector nodes 6 and 'large' vector nodes being of class 7. The 'small'
vector nodes are able to store vector data of up to 8, 16, 32, 64 and
128 bytes: larger vectors are `malloc`-ed individually whereas the
'small' nodes are allocated from pages of about 2000 bytes. Vector nodes
allocated using custom allocators (via `allocVector3`) are not counted
in the gc memory usage statistics since their memory semantics is not
under R's control and may be non-standard (e.g., memory could be
partially shared across nodes).

---

### 1.2 Environments and variable lookup

What users think of as 'variables' are symbols which are bound to
objects in 'environments'. The word 'environment' is used ambiguously in
R to mean _either_ the frame of an `ENVSXP` (a pairlist of symbol-value
pairs) _or_ an `ENVSXP`, a frame plus an enclosure.

There are additional places that 'variables' can be looked up, called
'user databases' in comments in the code. These seem undocumented in the
R sources, but apparently refer to the **RObjectTable** package at
<http://www.omegahat.net/RObjectTables/>.

The base environment is special. There is an `ENVSXP` environment with
enclosure the empty environment `R_EmptyEnv`, but the frame of that
environment is not used. Rather its bindings are part of the global
symbol table, being those symbols in the global symbol table whose
values are not `R_UnboundValue`. When R is started the internal
functions are installed (by C code) in the symbol table, with primitive
functions having values and `.Internal` functions having what would be
their values in the field accessed by the `INTERNAL` macro. Then
`.Platform` and `.Machine` are computed and the base package is loaded
into the base environment followed by the system profile.

The frames of environments (and the symbol table) are normally hashed
for faster access (including insertion and deletion).

By default R maintains a (hashed) global cache of 'variables' (that is
symbols and their bindings) which have been found, and this refers only
to environments which have been marked to participate, which consists of
the global environment (aka the user workspace), the base environment
plus environments[^4^](#FOOT4) which have been `attach`ed. When
an environment is either `attach`ed or `detach`ed, the names of its
symbols are flushed from the cache. The cache is used whenever searching
for variables from the global environment (possibly as part of a
recursive search).

---

• [Search paths](#Search-paths)     
 • [Namespaces](#Namespaces)     
 • [Hash table](#Hash-table)

---

---

#### 1.2.1 Search paths

S has the notion of a 'search path': the lookup for a 'variable' leads
(possibly through a series of frames) to the 'session frame' the
'working directory' and then along the search path. The search path is a
series of databases (as returned by `search()`) which contain the system
functions (but not necessarily at the end of the path, as by default the
equivalent of packages are added at the end).

R has a variant on the S model. There is a search path (also returned by
`search()`) which consists of the global environment (aka user
workspace) followed by environments which have been attached and finally
the base environment. Note that unlike S it is not possible to attach
environments before the workspace nor after the base environment.

However, the notion of variable lookup is more general in R, hence the
plural in the title of this subsection. Since environments have
enclosures, from any environment there is a search path found by looking
in the frame, then the frame of its enclosure and so on. Since loops are
not allowed, this process will eventually terminate: it can terminate at
either the base environment or the empty environment. (It can be
conceptually simpler to think of the search always terminating at the
empty environment, but with an optimization to stop at the base
environment.) So the 'search path' describes the chain of environments
which is traversed once the search reaches the global environment.

---

#### 1.2.2 Namespaces

Namespaces are environments associated with packages (and once again the
base package is special and will be considered separately). A package
`pkg` defines two environments `namespace:pkg` and `package:pkg`: it is
`package:pkg` that can be `attach`ed and form part of the search path.

The objects defined by the R code in the package are symbols with
bindings in the `namespace:pkg` environment. The `package:pkg`
environment is populated by selected symbols from the `namespace:pkg`
environment (the exports). The enclosure of this environment is an
environment populated with the explicit imports from other namespaces,
and the enclosure of _that_ environment is the base namespace. (So the
illusion of the imports being in the namespace environment is created
via the environment tree.) The enclosure of the base namespace is the
global environment, so the search from a package namespace goes via the
(explicit and implicit) imports to the standard 'search path'.

The base namespace environment `R_BaseNamespace` is another `ENVSXP`
that is special-cased. It is effectively the same thing as the base
environment `R_BaseEnv` _except_ that its enclosure is the global
environment rather than the empty environment: the internal code diverts
lookups in its frame to the global symbol table.

---

#### 1.2.3 Hash table

Environments in R usually have a hash table, and nowadays that is the
default in `new.env()`. It is stored as a `VECSXP` where `length` is
used for the allocated size of the table and `truelength` is the number
of primary slots in use---the pointer to the `VECSXP` is part of the
header of a `SEXP` of type `ENVSXP`, and this points to `R_NilValue` if
the environment is not hashed.

For the pros and cons of hashing, see a basic text on Computer Science.

The code to implement hashed environments is in
`src/main/envir.c`. Unless set otherwise (e.g. by the `size`
argument of `new.env()`) the initial table size is `29`. The table will
be resized by a factor of 1.2 once the load factor (the proportion of
primary slots in use) reaches 85%.

The hash chains are stored as pairlist elements of the `VECSXP`: items
are inserted at the front of the pairlist. Hashing is principally
designed for fast searching of environments, which are from time to time
added to but rarely deleted from, so items are not actually deleted but
have their value set to `R_UnboundValue`.

---

### 1.3 Attributes

As we have seen, every `SEXPREC` has a pointer to the attributes of the
node (default `R_NilValue`). The attributes can be accessed/set by the
macros/functions `ATTRIB` and `SET_ATTRIB`, but such direct access is
normally only used to check if the attributes are `NULL` or to reset
them. Otherwise access goes through the functions `getAttrib` and
`setAttrib` which impose restrictions on the attributes. One thing to
watch is that if you copy attributes from one object to another you may
(un)set the `"class"` attribute and so need to copy the object and S4
bits as well. There is a macro/function `DUPLICATE_ATTRIB` to automate
this.

Note that the 'attributes' of a `CHARSXP` are used as part of the
management of the `CHARSXP` cache: of course `CHARSXP`'s are not
user-visible but C-level code might look at their attributes.

The code assumes that the attributes of a node are either `R_NilValue`
or a pairlist of non-zero length (and this is checked by `SET_ATTRIB`).
The attributes are named (via tags on the pairlist). The replacement
function `attributes<-` ensures that `"dim"` precedes `"dimnames"` in
the pairlist. Attribute `"dim"` is one of several that is treated
specially: the values are checked, and any `"names"` and `"dimnames"`
attributes are removed. Similarly, you cannot set `"dimnames"` without
having set `"dim"`, and the value assigned must be a list of the correct
length and with elements of the correct lengths (and all zero-length
elements are replaced by `NULL`).

The other attributes which are given special treatment are `"names"`,
`"class"`, `"tsp"`, `"comment"` and `"row.names"`. For pairlist-like
objects the names are not stored as an attribute but (as symbols) as the
tags: however the R interface makes them look like conventional
attributes, and for one-dimensional arrays they are stored as the first
element of the `"dimnames"` attribute. The C code ensures that the
`"tsp"` attribute is an `REALSXP`, the frequency is positive and the
implied length agrees with the number of rows of the object being
assigned to. Classes and comments are restricted to character vectors,
and assigning a zero-length comment or class removes the attribute.
Setting or removing a `"class"` attribute sets the object bit
appropriately. Integer row names are converted to and from the internal
compact representation.

Care needs to be taken when adding attributes to objects of the types
with non-standard copying semantics. There is only one object of type
`NILSXP`, `R_NilValue`, and that should never have attributes (and this
is enforced in `installAttrib`). For environments, external pointers and
weak references, the attributes should be relevant to all uses of the
object: it is for example reasonable to have a name for an environment,
and also a `"path"` attribute for those environments populated from R
code in a package.

When should attributes be preserved under operations on an object?
Becker, Chambers & Wilks (1988, pp. 144--6) give some guidance. Scalar
functions (those which operate element-by-element on a vector and whose
output is similar to the input) should preserve attributes (except
perhaps class, and if they do preserve class they need to preserve the
`OBJECT` and S4 bits). Binary operations normally call
`copyMostAttrib` to copy most attributes from
the longer argument (and if they are of the same length from both,
preferring the values on the first). Here 'most' means all except the
`names`, `dim` and `dimnames` which are set appropriately by the code
for the operator.

Subsetting (other than by an empty index) generally drops all attributes
except `names`, `dim` and `dimnames` which are reset as appropriate. On
the other hand, subassignment generally preserves such attributes even
if the length is changed. Coercion drops all attributes. For example:

```r
> x <- structure(1:8, names=letters[1:8], comm="a comment")
> x[]
a b c d e f g h
1 2 3 4 5 6 7 8
attr(,"comm")
[1] "a comment"
> x[1:3]
a b c
1 2 3
> x[3] <- 3
> x
a b c d e f g h
1 2 3 4 5 6 7 8
attr(,"comm")
[1] "a comment"
> x[9] <- 9
> x
a b c d e f g h
1 2 3 4 5 6 7 8 9
attr(,"comm")
[1] "a comment"
```

---

### 1.4 Contexts

_Contexts_ are the internal mechanism used to keep track of where a
computation has got to (and from where), so that control-flow constructs
can work and reasonable information can be produced on error conditions
(such as _via_ traceback), and otherwise (the `sys.xxx` functions).

Execution contexts are a stack of C `structs`:

```r
typedef struct RCNTXT {
    struct RCNTXT *nextcontext; /* The next context up the chain */
    int callflag;               /* The context ‘type’ */
    JMP_BUF cjmpbuf;            /* C stack and register information */
    int cstacktop;              /* Top of the pointer protection stack */
    int evaldepth;              /* Evaluation depth at inception */
    SEXP promargs;              /* Promises supplied to closure */
    SEXP callfun;               /* The closure called */
    SEXP sysparent;             /* Environment the closure was called from */
    SEXP call;                  /* The call that effected this context */
    SEXP cloenv;                /* The environment */
    SEXP conexit;               /* Interpreted on.exit code */
    void (*cend)(void *);       /* C on.exit thunk */
    void *cenddata;             /* Data for C on.exit thunk */
    char *vmax;                 /* Top of the R_alloc stack */
    int intsusp;                /* Interrupts are suspended */
    SEXP handlerstack;          /* Condition handler stack */
    SEXP restartstack;          /* Stack of available restarts */
    struct RPRSTACK *prstack;   /* Stack of pending promises */
} RCNTXT, *context;
```

plus additional fields for the byte-code compiler. The 'types' are from

```r
enum {
    CTXT_TOPLEVEL = 0,  /* toplevel context */
    CTXT_NEXT     = 1,  /* target for next */
    CTXT_BREAK    = 2,  /* target for break */
    CTXT_LOOP     = 3,  /* break or next target */
    CTXT_FUNCTION = 4,  /* function closure */
    CTXT_CCODE    = 8,  /* other functions that need error cleanup */
    CTXT_RETURN   = 12, /* return() from a closure */
    CTXT_BROWSER  = 16, /* return target on exit from browser */
    CTXT_GENERIC  = 20, /* rather, running an S3 method */
    CTXT_RESTART  = 32, /* a call to restart was made from a closure */
    CTXT_BUILTIN  = 64  /* builtin internal function */
};
```

where the `CTXT_FUNCTION` bit is on wherever function closures are
involved.

Contexts are created by a call to `begincontext` and ended by a call to
`endcontext`: code can search up the stack for a particular type of
context via `findcontext` (and jump there) or jump to a specific context
via `R_JumpToContext`. `R_ToplevelContext` is the 'idle' state (normally
the command prompt), and `R_GlobalContext` is the top of the stack.

Note that whilst calls to closures and builtins set a context, those to
special internal functions never do.

Dispatching from a S3 generic (via `UseMethod` or its internal
equivalent) or calling `NextMethod` sets the context type to
`CTXT_GENERIC`. This is used to set the `sysparent` of the method call
to that of the `generic`, so the method appears to have been called in
place of the generic rather than from the generic.

The R `sys.frame` and `sys.call` functions work by counting calls to
closures (type `CTXT_FUNCTION`) from either end of the context stack.

Note that the `sysparent` element of the structure is not the same thing
as `sys.parent()`. Element `sysparent` is primarily used in managing
changes of the function being evaluated, i.e. by `Recall` and method
dispatch.

`CTXT_CCODE` contexts are currently used in `cat()`, `load()`, `scan()`
and `write.table()` (to close the connection on error), by `PROTECT`,
serialization (to recover from errors, e.g. free buffers) and within the
error handling code (to raise the C stack limit and reset some
variables).

---

### 1.5 Argument evaluation

As we have seen, functions in R come in three types, closures
(`SEXPTYPE` `CLOSXP`), specials (`SPECIALSXP`) and builtins
(`BUILTINSXP`). In this section we consider when (and if) the actual
arguments of function calls are evaluated. The rules are different for
the internal (special/builtin) and R-level functions (closures).

For a call to a closure, the actual and formal arguments are matched and
a matched call (another `LANGSXP`) is constructed. This process first
replaces the actual argument list by a list of promises to the values
supplied. It then constructs a new environment which contains the names
of the formal parameters matched to actual or default values: all the
matched values are promises, the defaults as promises to be evaluated in
the environment just created. That environment is then used for the
evaluation of the body of the function, and promises will be forced (and
hence actual or default arguments evaluated) when they are encountered.
(Evaluating a promise sets `NAMED = NAMEDMAX` on its
value, so if the argument was a symbol its binding is regarded as having
multiple references during the evaluation of the closure call.)

If the closure is an S3 generic (that is, contains a call to
`UseMethod`) the evaluation process is the same until the `UseMethod`
call is encountered. At that point the argument on which to do dispatch
(normally the first) will be evaluated if it has not been already. If a
method has been found which is a closure, a new evaluation environment
is created for it containing the matched arguments of the method plus
any new variables defined so far during the evaluation of the body of
the generic. (Note that this means changes to the values of the formal
arguments in the body of the generic are discarded when calling the
method, but _actual_ argument promises which have been forced retain the
values found when they were forced. On the other hand, missing arguments
have values which are promises to use the default supplied by the method
and not by the generic.) If the method found is a primitive it is called
with the matched argument list of promises (possibly already forced)
used for the generic.

The essential difference[^5^](#FOOT5) between special and
builtin functions is that the arguments of specials are not evaluated
before the C code is called, and those of builtins are. Note that being
a special/builtin is separate from being primitive or `.Internal`:
`quote` is a special primitive, `+` is a builtin primitive, `cbind` is a
special `.Internal` and `grep` is a builtin `.Internal`.

Many of the internal functions are internal generics, which for specials
means that they do not evaluate their arguments on call, but the C code
starts with a call to `DispatchOrEval`. The latter evaluates the first
argument, and looks for a method based on its class. (If S4 dispatch is
on, S4 methods are looked for first, even for S3 classes.) If it finds a
method, it dispatches to that method with a call based on promises to
evaluate the remaining arguments. If no method is found, the remaining
arguments are evaluated before return to the internal generic.

The other way that internal functions can be generic is to be group
generic. Most such functions are builtins (so immediately evaluate all
their arguments), and all contain a call to the C function
`DispatchGeneric`. There are some peculiarities over the number of
arguments for the `"Math"` group generic, with some members allowing
only one argument, some having two (with a default for the second) and
`trunc` allows one or more but the default method only accepts one.

---

• [Missingness](#Missingness)     
 • [Dot-dot-dot arguments](#Dot_002ddot_002ddot-arguments)

---

---

#### 1.5.1 Missingness

Actual arguments to (non-internal) R functions can be fewer than are
required to match the formal arguments of the function. Having unmatched
formal arguments will not matter if the argument is never used (by lazy
evaluation), but when the argument is evaluated, either its default
value is evaluated (within the evaluation environment of the function)
or an error is thrown with a message along the lines of

```r
argument "foobar" is missing, with no default
```

Internally missingness is handled by two mechanisms. The object
`R_MissingArg` is used to indicate that a formal argument has no
(default) value. When matching the actual arguments to the formal
arguments, a new argument list is constructed from the formals all of
whose values are `R_MissingArg` with the first `MISSING` bit set. Then
whenever a formal argument is matched to an actual argument, the
corresponding member of the new argument list has its value set to that
of the matched actual argument, and if that is not `R_MissingArg` the
missing bit is unset.

This new argument list is used to form the evaluation frame for the
function, and if named arguments are subsequently given a new value
(before they are evaluated) the missing bit is cleared.

Missingness of arguments can be interrogated via the `missing()`
function. An argument is clearly missing if its missing bit is set or if
the value is `R_MissingArg`. However, missingness can be passed on from
function to function, for using a formal argument as an actual argument
in a function call does not count as evaluation. So `missing()` has to
examine the value (a promise) of a non-yet-evaluated formal argument to
see if it might be missing, which might involve investigating a promise
and so on ....

Special primitives also need to handle missing arguments, and in some
case (e.g. `log`) that is why they are special and not builtin. This is
usually done by testing if an argument's value is `R_MissingArg`.

---

#### 1.5.2 Dot-dot-dot arguments

Dot-dot-dot arguments are convenient when writing functions, but
complicate the internal code for argument evaluation.

The formals of a function with a `...` argument represent that as a
single argument like any other argument, with tag the symbol
`R_DotsSymbol`. When the actual arguments are matched to the formals,
the value of the `...` argument is of `SEXPTYPE` `DOTSXP`, a pairlist of
promises (as used for matched arguments) but distinguished by the
`SEXPTYPE`.

Recall that the evaluation frame for a function initially contains the
`name=value` pairs from the matched call, and hence this will be true
for `...` as well. The value of `...` is a (special) pairlist whose
elements are referred to by the special symbols `..1`, `..2`, ... which
have the `DDVAL` bit set: when one of these is encountered it is looked
up (via `ddfindVar`) in the value of the `...` symbol in the evaluation
frame.

Values of arguments matched to a `...` argument can be missing.

Special primitives may need to handle `...` arguments: see for example
the internal code of `switch` in file `src/main/builtin.c`.

---

### 1.6 Autoprinting

Whether the returned value of a top-level R expression is printed is
controlled by the global boolean variable `R_Visible`. This is set (to
true or false) on entry to all primitive and internal functions based on
the `eval` column of the table in file `src/main/names.c`: the
appropriate setting can be extracted by the macro `PRIMPRINT`.

The R primitive function `invisible` makes use of this mechanism: it
just sets `R_Visible = FALSE` before entry and returns its argument.

For most functions the intention will be that the setting of `R_Visible`
when they are entered is the setting used when they return, but there
need to be exceptions. The R functions `identify`, `options`, `system`
and `writeBin` determine whether the result should be visible from the
arguments or user action. Other functions themselves dispatch functions
which may change the visibility flag: examples[^6^](#FOOT6) are
`.Internal`, `do.call`, `eval`, `withVisible`, `if`, `NextMethod`,
`Recall`, `recordGraphics`, `standardGeneric`, `switch` and `UseMethod`.

'Special' primitive and internal functions evaluate their arguments
internally _after_ `R_Visible` has been set, and evaluation of the
arguments (e.g. an assignment as in PR\#9263) can change the value of
the flag.

The `R_Visible` flag can also get altered during the evaluation of a
function, with comments in the code about `warning`, `writeChar` and
graphics functions calling `GText` (PR\#7397). (Since the C-level
function `eval` sets `R_Visible`, this could apply to any function
calling it. Since it is called when evaluating promises, even object
lookup can change `R_Visible`.) Internal and primitive functions force
the documented setting of `R_Visible` on return, unless the C code is
allowed to change it (the exceptions above are indicated by `PRIMPRINT`
having value 2).

The actual autoprinting is done by `PrintValueEnv` in file
`print.c`. If the object to be printed has the S4 bit set and
S4 methods dispatch is on, `show` is called to print the object.
Otherwise, if the object bit is set (so the object has a `"class"`
attribute), `print` is called to dispatch methods: for objects without a
class the internal code of `print.default` is called.

---

### 1.7 The write barrier and the garbage collector

R has long had a generational garbage collector, and bit `gcgen` in the
`sxpinfo` header is used in the implementation of this. This is used in
conjunction with the `mark` bit to identify two previous generations.

There are three levels of collections. Level 0 collects only the
youngest generation, level 1 collects the two youngest generations and
level 2 collects all generations. After 20 level-0 collections the next
collection is at level 1, and after 5 level-1 collections at level 2.
Further, if a level-`n`{.variable} collection fails to provide 20% free
space (for each of nodes and the vector heap), the next collection will
be at level `n+1`{.variable}. (The R-level function `gc()` performs a
level-2 collection.)

A generational collector needs to efficiently 'age' the objects,
especially list-like objects (including `STRSXP`s). This is done by
ensuring that the elements of a list are regarded as at least as old as
the list _when they are assigned_. This is handled by the functions
`SET_VECTOR_ELT` and `SET_STRING_ELT`, which is why they are functions
and not macros. Ensuring the integrity of such operations is termed the
_write barrier_ and is done by making the `SEXP` opaque and only
providing access via functions (which cannot be used as lvalues in
assignments in C).

All code in R extensions is by default behind the write barrier. The
only way to obtain direct access to the internals of the `SEXPREC`s is
to define '`USE_RINTERNALS`' before including header file
`Rinternals.h`, which is normally defined in `Defn.h`.
To enable a check on the way that the access is used, R can be compiled
with flag `--enable-strict-barrier` which ensures that header
`Defn.h` does not define '`USE_RINTERNALS`' and hence
that `SEXP` is opaque in most of R itself. (There are some necessary
exceptions: foremost in file `memory.c` where the accessor
functions are defined and also in file `size.c` which needs
access to the sizes of the internal structures.)

For background papers see
<http://homepage.stat.uiowa.edu/~luke/R/barrier.html> and
<http://homepage.stat.uiowa.edu/~luke/R/gengcnotes.html>.

---

### 1.8 Serialization Formats

Serialized versions of R objects are used by `load`/`save` and also at a
slightly lower level by `saveRDS`/`readRDS` (and their earlier
'internal' dot-name versions) and `serialize`/`unserialize`. These
differ in what they serialize to (a file, a connection, a raw vector)
and whether they are intended to serialize a single object or a
collection of objects (typically the workspace). `save` writes a header
at the beginning of the file (a single LF-terminated line) which the
lower-level versions do not.

`save` and `saveRDS` allow various forms of compression, and `gzip`
compression is the default (except for ASCII saves). Compression is
applied to the whole file stream, including the headers, so serialized
files can be uncompressed or re-compressed by external programs. Both
`load` and `readRDS` can read `gzip`, `bzip2` and `xz` forms of
compression when reading from a file, and `gzip` compression when
reading from a connection.

R has used the same serialization format called 'version 2' from R 1.4.0
in December 2001 until R 3.5.3 in March 2019. It has been expanded in
back-compatible ways since its inception, for example to support
additional `SEXPTYPE`s. Earlier formats are still supported via `load`
and `save` but such formats are not described here. The current default
serialization format is called 'version 3', and has been introduced in R
3.5.0.

`save` works by writing a single-line header (typically `RDX2\n` for a
binary save: the only other current value is `RDA2\n` for
`save(files=TRUE)`), then creating a tagged pairlist of the objects to
be saved and serializing that single object. `load` reads the header
line, unserializes a single object (a pairlist or a vector list) and
assigns the elements of the object in the specified environment. The
header line serves two purposes in R: it identifies the serialization
format so `load` can switch to the appropriate reader code, and the
newline `\n` allows the detection of files which have been subjected to
a non-binary transfer which re-mapped line endings. It can also be
thought of as a 'magic number' in the sense used by the `file` program
(although R save files are not yet by default known to that program).

Serialization in R needs to take into account that objects may contain
references to environments, which then have enclosing environments and
so on. (Environments recognized as package or name space environments
are saved by name.) There are 'reference objects' which are not
duplicated on copy and should remain shared on unserialization. These
are weak references, external pointers and environments other than those
associated with packages, namespaces and the global environment. These
are handled via a hash table, and references after the first are written
out as a reference marker indexed by the table entry.

Version-2 serialization first writes a header indicating the format
(normally '`X\n`' for an XDR format binary save, but
'`A\n`', ASCII, and '`B\n`', native word-order binary,
can also occur) and then three integers giving the version of the format
and two R versions (packed by the `R_Version` macro from
`Rversion.h`). (Unserialization interprets the two versions as
the version of R which wrote the file followed by the minimal version of
R needed to read the format.) Serialization then writes out the object
recursively using function `WriteItem` in file
`src/main/serialize.c`.

Some objects are written as if they were `SEXPTYPE`s: such
pseudo-`SEXPTYPE`s cover `R_NilValue`, `R_EmptyEnv`, `R_BaseEnv`,
`R_GlobalEnv`, `R_UnboundValue`, `R_MissingArg` and `R_BaseNamespace`.

For all `SEXPTYPE`s except `NILSXP`, `SYMSXP` and `ENVSXP` serialization
starts with an integer with the `SEXPTYPE` in bits
0:7[^7^](#FOOT7) followed by the object bit, two bits indicating
if there are any attributes and if there is a tag (for the pairlist
types), an unused bit and then the `gp` field[^8^](#FOOT8) in
bits 12:27. Pairlist-like objects write their attributes (if any), tag
(if any), CAR and then CDR (using tail recursion): other objects write
their attributes after themselves. Atomic vector objects write their
length followed by the data: generic vector-list objects write their
length followed by a call to `WriteItem` for each element. The code for
`CHARSXP`s special-cases `NA_STRING` and writes it as length `-1` with
no data. Lengths no more than `2^31 - 1` are written in that way and
larger lengths (which only occur on 64-bit systems) as `-1` followed by
the upper and lower 32-bits as integers (regarded as unsigned).

Environments are treated in several ways: as we have seen, some are
written as specific pseudo-`SEXPTYPE`s. Package and namespace
environments are written with pseudo-`SEXPTYPE`s followed by the name.
'Normal' environments are written out as `ENVSXP`s with an integer
indicating if the environment is locked followed by the enclosure,
frame, 'tag' (the hash table) and attributes.

In the 'XDR' format integers and doubles are written in bigendian order:
however the format is not fully XDR (as defined in RFC 1832) as byte
quantities (such as the contents of `CHARSXP` and `RAWSXP` types) are
written as-is and not padded to a multiple of four bytes.

The 'ASCII' format writes 7-bit characters. Integers are formatted with
`%d` (except that `NA_integer_` is written as `NA`), doubles formatted
with `%.16g` (plus `NA`, `Inf` and `-Inf`) and bytes with `%02x`.
Strings are written using standard escapes (e.g. `\t` and `\013`) for
non-printing and non-ASCII bytes.

Version-3 serialization extends version-2 by support for custom
serialization of `ALTREP` framework objects. It also stores the current
native encoding at serialization time, so that unflagged strings can be
converted if unserialized in R running under different native encoding.

---

### 1.9 Encodings for CHARSXPs

Character data in R are stored in the sexptype `CHARSXP`.

There is support for encodings other than that of the current locale, in
particular UTF-8 and the multi-byte encodings used on Windows for CJK
languages. A limited means to indicate the encoding of a `CHARSXP` is
_via_ two of the 'general purpose' bits which are used to declare the
encoding to be either Latin-1 or UTF-8. (Note that it is possible for a
character vector to contain elements in different encodings.) Both
printing and plotting notice the declaration and convert the string to
the current locale (possibly using `<xx>` to display in hexadecimal
bytes that are not valid in the current locale). Many (but not all) of
the character manipulation functions will either preserve the
declaration or re-encode the character string.

Strings that refer to the OS such as file names need to be passed
through a wide-character interface on some OSes (e.g. Windows).

When are character strings declared to be of known encoding? One way is
to do so directly via `Encoding`. The parser declares the encoding if
this is known, either via the `encoding` argument to `parse` or from the
locale within which parsing is being done at the R command line. (Other
ways are recorded on the help page for `Encoding`.)

It is not necessary to declare the encoding of ASCII strings as they
will work in any locale. ASCII strings should never have a marked
encoding, as any encoding will be ignored when entering such strings
into the `CHARSXP` cache.

The rationale behind considering only UTF-8 and Latin-1 was that most
systems are capable of producing UTF-8 strings and this is the nearest
we have to a universal format. For those that do not (for example those
lacking a powerful enough `iconv`), it is likely that they work in
Latin-1, the old R assumption. Then the parser can return a
UTF-8-encoded string if it encounters a '`\uxxxx`' escape for a
Unicode point that cannot be represented in the current charset. (This
needs MBCS support, and was only enabled[^9^](#FOOT9) on
Windows.) This is enabled for all platforms, and a '`\uxxxx`'
or '`\Uxxxxxxxx`' escape ensures that the parsed string will be
marked as UTF-8.

Most of the character manipulation functions now preserve UTF-8
encodings: there are some notes as to which at the top of file
`src/main/character.c` and in file
`src/library/base/man/Encoding.Rd`.

Graphics devices are offered the possibility of handing UTF-8-encoded
strings without re-encoding to the native character set, by setting
`hasTextUTF8` to be '`TRUE`' and supplying functions `textUTF8`
and `strWidthUTF8` that expect UTF-8-encoded inputs. Normally the symbol
font is encoded in Adobe Symbol encoding, but that can be re-encoded to
UTF-8 by setting `wantSymbolUTF8` to '`TRUE`'. The Windows'
port of cairographics has a rather peculiar assumption: it wants the
symbol font to be encoded in UTF-8 as if it were encoded in Latin-1
rather than Adobe Symbol: this is selected by
`wantSymbolUTF8 = NA_LOGICAL`.

Windows has no UTF-8 locales, but rather expects to work with
UCS-2[^10^](#FOOT10) strings. R (being written in standard C)
would not work internally with UCS-2 without extensive changes. The
`Rgui` console[^11^](#FOOT11) uses UCS-2 internally,
but communicates with the R engine in the native encoding. To allow
UTF-8 strings to be printed in UTF-8 in `Rgui.exe`, an escape
convention is used (see header file `rgui_UTF8.h`) by `cat`,
`print` and autoprinting.

'Unicode' (UCS-2LE) files are common in the Windows world, and
`readLines` and `scan` will read them into UTF-8 strings on Windows if
the encoding is declared explicitly on an unopened connection passed to
those functions.

---

### 1.10 The CHARSXP cache

There is a global cache for `CHARSXP`s created by `mkChar` --- the cache
ensures that most `CHARSXP`s with the same contents share storage
('contents' including any declared encoding). Not all `CHARSXP`s are
part of the cache -- notably '`NA_STRING`' is not. `CHARSXP`s
reloaded from the `save` formats of R prior to 0.99.0 are not cached
(since the code used is frozen and very few examples still exist).

The cache records the encoding of the string as well as the bytes: all
requests to create a `CHARSXP` should be _via_ a call to `mkCharLenCE`.
Any encoding given in `mkCharLenCE` call will be ignored if the string's
bytes are all ASCII characters.

---

### 1.11 Warnings and errors

Each of `warning` and `stop` have two C-level equivalents, `warning`,
`warningcall`, `error` and `errorcall`. The relationship between the
pairs is similar: `warning` tries to fathom out a suitable call, and
then calls `warningcall` with that call as the first argument if it
succeeds, and with `call = R_NilValue` if it does not. When
`warningcall` is called, it includes the deparsed call in its printout
unless `call = R_NilValue`.

`warning` and `error` look at the context stack. If the topmost context
is not of type `CTXT_BUILTIN`, it is used to provide the call, otherwise
the next context provides the call. This means that when these functions
are called from a primitive or `.Internal`, the imputed call will not be
to primitive/`.Internal` but to the function calling the
primitive/`.Internal` . This is exactly what one wants for a
`.Internal`, as this will give the call to the closure wrapper.
(Further, for a `.Internal`, the call is the argument to `.Internal`,
and so may not correspond to any R function.) However, it is unlikely to
be what is needed for a primitive.

The upshot is that that `warningcall` and `errorcall` should normally be
used for code called from a primitive, and `warning` and `error` should
be used for code called from a `.Internal` (and necessarily from
`.Call`, `.C` and so on, where the call is not passed down). However,
there are two complications. One is that code might be called from
either a primitive or a `.Internal`, in which case probably
`warningcall` is more appropriate. The other involves replacement
functions, where the call was once of the form

```r
> length(x) <- y ~ x
Error in "length<-"(`*tmp*`, value = y ~ x) : invalid value
```

which is unpalatable to the end user. For replacement functions there
will be a suitable context at the top of the stack, so `warning` should
be used. (The results for `.Internal` replacement functions such as
`substr<-` are not ideal.)

---

### 1.12 S4 objects

\[This section is currently a preliminary draft and should not be taken
as definitive. The description assumes that `R_NO_METHODS_TABLES` has
not been set.\]

---

• [Representation of S4 objects](#Representation-of-S4-objects)     
 • [S4 classes](#S4-classes)     
 • [S4 methods](#S4-methods)     
 • [Mechanics of S4 dispatch](#Mechanics-of-S4-dispatch)

---

---

#### 1.12.1 Representation of S4 objects

S4 objects can be of any `SEXPTYPE`. They are either an object of a
simple type (such as an atomic vector or function) with S4 class
information or of type `S4SXP`. In all cases, the 'S4 bit' (bit 4 of the
'general purpose' field) is set, and can be tested by the macro/function
`IS_S4_OBJECT`.

S4 objects are created via `new()`[^12^](#FOOT12) and thence
via the C function `R_do_new_object`. This duplicates the prototype of
the class, adds a class attribute and sets the S4 bit. All S4 class
attributes should be character vectors of length one with an attribute
giving (as a character string) the name of the package (or `.GlobalEnv`)
containing the class definition. Since S4 objects have a class
attribute, the `OBJECT` bit is set.

It is currently unclear what should happen if the class attribute is
removed from an S4 object, or if this should be allowed.

---

#### 1.12.2 S4 classes

S4 classes are stored as R objects in the environment in which they are
created, with names `.__C__classname`: as such they are not listed by
default by `ls`.

The objects are S4 objects of class `"classRepresentation"` which is
defined in the **methods** package.

Since these are just objects, they are subject to the normal scoping
rules and can be imported and exported from namespaces like other
objects. The directives `importClassesFrom` and `exportClasses` are
merely convenient ways to refer to class objects without needing to know
their internal 'metaname' (although `exportClasses` does a little sanity
checking via `isClass`).

---

#### 1.12.3 S4 methods

Details of the methods are stored in environments (typically hidden in
the respective namespace) with a non-syntactic name of the form
`.__T__generic:package` containing objects of class `MethodDefinition`
for all methods defined in the current environment for the named generic
derived from a specific package (which might be `.GlobalEnv`). This is
sometimes referred to as a 'methods table'.

For example,

```r
 length(nM <- asNamespace("Matrix") )                    # 941 for Matrix 1.2-6
 length(meth <- grep("^[.]__T__", names(nM), value=TRUE))# 107 generics with methods
 length(meth.Ops <- nM$`.__T__Ops:base‘) # 71 methods for the ’Ops' (group)generic
 head(sort(names(meth.Ops))) ## "abIndex#abIndex" ... "ANY#ddiMatrix" "ANY#ldiMatrix" "ANY#Matrix"
```

During an R session there is an environment associated with each
non-primitive generic containing objects `.AllMTable`, `.Generic`,
`.Methods`, `.MTable`, `.SigArgs` and `.SigLength`. `.MTable` and
`AllMTable` are merged methods tables containing all the methods defined
directly and via inheritance respectively. `.Methods` is a merged
methods list.

Exporting methods from a namespace is more complicated than exporting a
class. Note first that you do not export a method, but rather the
directive `exportMethods` will export all the methods defined in the
namespace for a specified generic: the code also adds to the list of
generics any that are exported directly. For generics which are listed
via `exportMethods` or exported themselves, the corresponding
environment is exported and so will appear (as hidden object) in the
package environment.

Methods for primitives which are internally S4 generic (see below) are
always exported, whether mentioned in the `NAMESPACE` file or
not.

Methods can be imported either via the directive `importMethodsFrom` or
via importing a namespace by `import`. Also, if a generic is imported
via `importFrom`, its methods are also imported. In all cases the
generic will be imported if it is in the namespace, so
`importMethodsFrom` is most appropriate for methods defined on generics
in other packages. Since methods for a generic could be imported from
several different packages, the methods tables are merged.

When a package is attached `methods:::cacheMetaData` is called to update
the internal tables: only the visible methods will be cached.

---

#### 1.12.4 Mechanics of S4 dispatch

This subsection does not discuss how S4 methods are chosen: see
<https://developer.r-project.org/howMethodsWork.pdf>.

For all but primitive functions, setting a method on an existing
function that is not itself S4 generic creates a new object in the
current environment which is a call to `standardGeneric` with the old
definition as the default method. Such S4 generics can also be created
_via_ a call to `setGeneric`[^13^](#FOOT13) and are standard
closures in the R language, with environment the environment within
which they are created. With the advent of namespaces this is somewhat
problematic: if `myfn` was previously in a package with a name space
there will be two functions called `myfn` on the search paths, and which
will be called depends on which search path is in use. This is starkest
for functions in the base namespace, where the original will be found
ahead of the newly created function from any other package.

Primitive functions are treated quite differently, for efficiency
reasons: this results in different semantics. `setGeneric` is disallowed
for primitive functions. The **methods** namespace contains a list
`.BasicFunsList` named by primitive functions: the entries are either
`FALSE` or a standard S4 generic showing the effective definition. When
`setMethod` (or `setReplaceMethod`) is called, it either fails (if the
list entry is `FALSE`) or a method is set on the effective generic given
in the list.

Actual dispatch of S4 methods for almost all primitives piggy-backs on
the S3 dispatch mechanism, so S4 methods can only be dispatched for
primitives which are internally S3 generic. When a primitive that is
internally S3 generic is called with a first argument which is an S4
object and S4 dispatch is on (that is, the **methods** namespace is
loaded), `DispatchOrEval` calls `R_possible_dispatch` (defined in file
`src/main/objects.c`). (Members of the S3 group generics, which
includes all the generic operators, are treated slightly differently:
the first two arguments are checked and `DispatchGroup` is called.)
`R_possible_dispatch` first checks an internal table to see if any S4
methods are set for that generic (and S4 dispatch is currently enabled
for that generic), and if so proceeds to S4 dispatch using methods
stored in another internal table. All primitives are in the base
namespace, and this mechanism means that S4 methods can be set for
(some) primitives and will always be used, in contrast to setting
methods on non-primitives.

The exception is `%*%`, which is S4 generic but not S3 generic as its C
code contains a direct call to `R_possible_dispatch`.

The primitive `as.double` is special, as `as.numeric` and `as.real` are
copies of it. The **methods** package code partly refers to generics by
name and partly by function, and maps `as.double` and `as.real` to
`as.numeric` (since that is the name used by packages exporting methods
for it).

Some elements of the language are implemented as primitives, for example
`}`. This includes the subset and subassignment 'functions' and they are
S4 generic, again piggybacking on S3 dispatch.

`.BasicFunsList` is generated when **methods** is installed, by
computing all primitives, initially disallowing methods on all and then
setting generics for members of `.GenericArgsEnv`, the S4 group generics
and a short exceptions list in file `BasicFunsList.R`: this
currently contains the subsetting and subassignment operators and an
override for `c`.

---

### 1.13 Memory allocators

R's memory allocation is almost all done via routines in file
`src/main/memory.c`. It is important to keep track of where
memory is allocated, as the Windows port (by default) makes use of a
memory allocator that differs from `malloc` etc as provided by MinGW.
Specifically, there are entry points `Rm_malloc`, `Rm_free`, `Rm_calloc`
and `Rm_free` provided by file `src/gnuwin32/malloc.c`. This
was done for two reasons. The primary motivation was performance: the
allocator provided by MSVCRT _via_ MinGW was far too slow at handling
the many small allocations that the allocation system for `SEXPREC`s
uses. As a side benefit, we can set a limit on the amount of allocated
memory: this is useful as whereas Windows does provide virtual memory it
is relatively far slower than many other R platforms and so limiting R's
use of swapping is highly advantageous. The high-performance allocator
is only called from `src/main/memory.c`,
`src/main/regex.c`, `src/extra/pcre` and
`src/extra/xdr`: note that this means that it is not used in
packages.

The rest of R should where possible make use of the allocators made
available by file `src/main/memory.c`, which are also the
methods recommended in [Memory allocation](./R-exts.html#Memory-allocation) in Writing R Extensions

for use in R packages, namely the use of `R_alloc`,
`Calloc`, `Realloc` and `Free`. Memory allocated by `R_alloc` is freed
by the garbage collector once the 'watermark' has been reset by calling
`vmaxset`. This is done automatically by the wrapper
code calling primitives and `.Internal` functions (and also by the
wrapper code to `.Call` and `.External`), but
`vmaxget` and `vmaxset` can be used to reset the watermark from within
internal code if the memory is only required for a short time.

All of the methods of memory allocation mentioned so far are relatively
expensive. All R platforms support `alloca`, and in almost all
cases[^14^](#FOOT14) this is managed by the compiler, allocates
memory on the C stack and is very efficient.

There are two disadvantages in using `alloca`. First, it is fragile and
care is needed to avoid writing (or even reading) outside the bounds of
the allocation block returned. Second, it increases the danger of
overflowing the C stack. It is suggested that it is only used for
smallish allocations (up to tens of thousands of bytes), and that

```r
    R_CheckStack();
```

is called immediately after the allocation (as R's stack checking
mechanism will warn far enough from the stack limit to allow for modest
use of alloca). (`do_makeunique` in file `src/main/unique.c`
provides an example of both points.)

There is an alternative check,

```r
    R_CheckStack2(size_t extra);
```

to be called immediately _before_ trying an allocation of `extra` bytes.

An alternative strategy has been used for various functions which
require intermediate blocks of storage of varying but usually small
size, and this has been consolidated into the routines in the header
file `src/main/RBufferUtils.h`. This uses a structure which
contains a buffer, the current size and the default size. A call to

```r
    R_AllocStringBuffer(size_t blen, R_StringBuffer *buf);
```

sets `buf->data` to a memory area of at least `blen+1` bytes. At least
the default size is used, which means that for small allocations the
same buffer can be reused. A call to
`R_FreeStringBufferL` releases memory
if more than the default has been allocated whereas a call to
`R_FreeStringBuffer` frees any memory allocated.

The `R_StringBuffer` structure needs to be initialized, for example by

```r
static R_StringBuffer ex_buff = {NULL, 0, MAXELTSIZE};
```

which uses a default size of `MAXELTSIZE = 8192` bytes. Most current
uses have a static `R_StringBuffer` structure, which allows the
(default-sized) buffer to be shared between calls to e.g. `grep` and
even between functions: this will need to be changed if R ever allows
concurrent evaluation threads. So the idiom is

```r
static R_StringBuffer ex_buff = {NULL, 0, MAXELTSIZE};
...
    char *buf;
    for(i = 0; i < n; i++) {
        compute len
        buf = R_AllocStringBuffer(len, &ex_buff);
        use buf
    }
    /*  free allocation if larger than the default, but leave
        default allocated for future use */
   R_FreeStringBufferL(&ex_buff);
```

---

• [Internals of R_alloc](#Internals-of-R_005falloc)

---

---

#### 1.13.1 Internals of R_alloc

The memory used by `R_alloc` is allocated as R vectors, of type
`RAWSXP`. Thus the allocation is in units of 8 bytes, and is rounded up.
A request for zero bytes currently returns `NULL` (but this should not
be relied on). For historical reasons, in all other cases 1 byte is
added before rounding up so the allocation is always 1--8 bytes more
than was asked for: again this should not be relied on.

The vectors allocated are protected via the setting of `R_VStack`, as
the garbage collector marks everything that can be reached from that
location. When a vector is `R_alloc`ated, its `ATTRIB` pointer is set to
the current `R_VStack`, and `R_VStack` is set to the latest allocation.
Thus `R_VStack` is a single-linked chain of the vectors currently
allocated via `R_alloc`. Function `vmaxset` resets the location
`R_VStack`, and should be to a value that has previously be obtained
_via_ `vmaxget`: allocations after the value was obtained will no longer
be protected and hence available for garbage collection.

---

### 1.14 Internal use of global and base environments

This section notes known use by the system of these environments: the
intention is to minimize or eliminate such uses.

---

• [Base environment](#Base-environment)     
 • [Global environment](#Global-environment)

---

---

#### 1.14.1 Base environment

The graphics devices system maintains two variables `.Device` and
`.Devices` in the base environment: both are always set. The variable
`.Devices` gives a list of character vectors of the names of open
devices, and `.Device` is the element corresponding to the currently
active device. The null device will always be open.

There appears to be a variable `.Options`, a pairlist giving the current
options settings. But in fact this is just a symbol with a value
assigned, and so shows up as a base variable.

Similarly, the evaluator creates a symbol `.Last.value` which appears as
a variable in the base environment.

Errors can give rise to objects `.Traceback` and `last.warning` in the
base environment.

---

#### 1.14.2 Global environment

The seed for the random number generator is stored in object
`.Random.seed` in the global environment.

Some error handlers may give rise to objects in the global environment:
for example `dump.frames` by default produces `last.dump`.

The `windows()` device makes use of a variable `.SavedPlots` to store
display lists of saved plots for later display. This is regarded as a
variable created by the user.

---

### 1.15 Modules

R makes use of a number of shared objects/DLLs stored in the
`modules` directory. These are parts of the code which have
been chosen to be loaded 'on demand' rather than linked as dynamic
libraries or incorporated into the main executable/dynamic library.

For the remaining modules the motivation has been the amount of (often
optional) code they will bring in _via_ libraries to which they are
linked.

`internet`

: The internal HTTP and FTP clients and socket support, which link to
system-specific support libraries. This may load `libcurl` and on
Windows will load `wininet.dll` and `ws2_32.dll`.

`lapack`

: The code which makes use of the LAPACK library, and is linked to
`libRlapack` or an external LAPACK library.

`X11`

: (Unix-alikes only.) The `X11()`, `jpeg()`, `png()` and `tiff()`
devices. These are optional, and links to some or all of the `X11`,
`pango`, `cairo`, `jpeg`, `libpng` and `libtiff` libraries.

---

### 1.16 Visibility

---

• [Hiding C entry points](#Hiding-C-entry-points)     
 • [Variables in Windows DLLs](#Variables-in-Windows-DLLs)

---

---

#### 1.16.1 Hiding C entry points

We make use of the visibility mechanisms discussed in [Controlling visibility](./R-exts.html#Controlling-visibility) in Writing R
Extensions, C entry points not needed outside the main R
executable/dynamic library (and in particular in no package nor module)
should be prefixed by `attribute_hidden`.
Minimizing the visibility of symbols in
the R dynamic library will speed up linking to it (which packages will
do) and reduce the possibility of linking to the wrong entry points of
the same name. In addition, on some platforms reducing the number of
entry points allows more efficient versions of PIC to be used: somewhat
over half the entry points are hidden. A convenient way to hide
variables (as distinct from functions) is to declare them `extern0` in
header file `Defn.h`.

The visibility mechanism used is only available with some compilers and
platforms, and in particular not on Windows, where an alternative
mechanism is used. Entry points will not be made available in
`R.dll` if they are listed in the file
`src/gnuwin32/Rdll.hide`. Entries in
that file start with a space and must be strictly in alphabetic order in
the C locale (use `sort` on the file to ensure this if you change it).
It is possible to hide Fortran as well as C entry points via this file:
the former are lower-cased and have an underline as suffix, and the
suffixed name should be included in the file. Some entry points exist
only on Windows or need to be visible only on Windows, and some notes on
these are provided in file `src/gnuwin32/Maintainters.notes`.

Because of the advantages of reducing the number of visible entry
points, they should be declared `attribute_hidden` where possible. Note
that this only has an effect on a shared-R-library build, and so care is
needed not to hide entry points that are legitimately used by packages.
So it is best if the decision on visibility is made when a new entry
point is created, including the decision if it should be included in
header file `Rinternals.h`. A list of the visible entry points
on shared-R-library build on a reasonably standard Unix-alike can be
made by something like

```r
nm -g libR.so | grep ‘ [BCDT] ’ | cut -b20-
```

---

#### 1.16.2 Variables in Windows DLLs

Windows is unique in that it conventionally treats importing variables
differently from functions: variables that are imported from a DLL need
to be specified by a prefix (often '`_imp_`') when being linked
to ('imported') but not when being linked from ('exported'). The details
depend on the compiler system, and have changed for MinGW during the
lifetime of that port. They are in the main hidden behind some macros
defined in header file `R_ext/libextern.h`.

A (non-function) variable in the main R sources that needs to be
referred to outside `R.dll` (in a package, module or another
DLL such as `Rgraphapp.dll`) should be declared with prefix
`LibExtern`. The main use is in `Rinternals.h`, but it needs to
be considered for any public header and also `Defn.h`.

It would nowadays be possible to make use of the 'auto-import' feature
of the MinGW port of `ld` to fix up imports from DLLs (and if R is built
for the Cygwin platform this is what happens). However, this was not
possible when the MinGW build of R was first constructed in ca 1998,
allows less control of visibility and would not work for other Windows
compiler suites.

It is only possible to check if this has been handled correctly by
compiling the R sources on Windows.

---

### 1.17 Lazy loading

Lazy loading is always used for code in packages but is optional
(selected by the package maintainer) for datasets in packages. When a
package/namespace which uses it is loaded, the package/namespace
environment is populated with promises for all the named objects: when
these promises are evaluated they load the actual code from a database.

There are separate databases for code and data, stored in the
`R` and `data` subdirectories. The database consists
of two files, `name.rdb` and `name.rdx`. The
`.rdb` file is a concatenation of serialized objects, and the
`.rdx` file contains an index. The objects are stored in
(usually) a `gzip`-compressed format with a 4-byte header giving the
uncompressed serialized length (in XDR, that is big-endian, byte order)
and read by a call to the primitive `lazyLoadDBfetch`. (Note that this
makes lazy-loading unsuitable for really large objects: the unserialized
length of an R object can exceed 4GB.)

The index or 'map' file `name.rdx` is a compressed serialized R
object to be read by `readRDS`. It is a list with three elements
`variables`, `references` and `compressed`. The first two are named
lists of integer vectors of length 2 giving the offset and length of the
serialized object in the `name.rdb` file. Element `variables`
has an entry for each named object: `references` serializes a temporary
environment used when named environments are added to the database.
`compressed` is a logical indicating if the serialized objects were
compressed: compression is always used nowadays. We later added the
values `compressed = 2` and `3` for `bzip2` and `xz` compression (with
the possibility of future expansion to other methods): these formats add
a fifth byte to the header for the type of compression, and store
serialized objects uncompressed if compression expands them.

The loader for a lazy-load database of code or data is function
`lazyLoad` in the **base** package, but note that there is a separate
copy to load **base** itself in file `R_HOME/base/R/base`.

Lazy-load databases are created by the code in
`src/library/tools/R/makeLazyLoad.R`: the main tool is the
unexported function `makeLazyLoadDB` and the insertion of database
entries is done by calls to `.Call("R_lazyLoadDBinsertValue", ...)`.

Lazy-load databases of less than 10MB are cached in memory at first use:
this was found necessary when using file systems with high latency
(removable devices and network-mounted file systems on Windows).

Lazy-load databases are loaded into the exports for a package, but not
into the namespace environment itself. Thus they are visible when the
package is _attached_, and also _via_ the `::` operator. This was a
deliberate design decision, as packages mostly make datasets available
for use by the end user (or other packages), and they should not be
found preferentially from functions in the package, surprising users who
expected the normal search path to be used. (There is an alternative
mechanism, `sysdata.rda`, for 'system datasets' that are
intended primarily to be used within the package.)

The same database mechanism is used to store parsed `Rd` files.
One or all of the parsed objects is fetched by a call to
`tools:::fetchRdDB`.

---
