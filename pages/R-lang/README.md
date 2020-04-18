---
Generator: texi2any
description: R Language Definition
distribution: global
keywords: R Language Definition
resource-type: document
title: R Language Definition
---

# R Language Definition

## Table of Contents

- [1 Introduction](#Introduction)
- [2 Objects](#Objects)
  - [2.1 Basic types](#Basic-types)
    - [2.1.1 Vectors](#Vector-objects)
    - [2.1.2 Lists](#List-objects)
    - [2.1.3 Language
      objects](#Language-objects)
      - [2.1.3.1 Symbol
        objects](#Symbol-objects)
    - [2.1.4 Expression
      objects](#Expression-objects)
    - [2.1.5 Function
      objects](#Function-objects)
    - [2.1.6 NULL](#NULL-object)
    - [2.1.7 Builtin objects and special
      forms](#Builtin-objects-and-special-forms)
    - [2.1.8 Promise
      objects](#Promise-objects)
    - [2.1.9
      Dot-dot-dot](#Dot_002ddot_002ddot)
    - [2.1.10
      Environments](#Environment-objects)
    - [2.1.11 Pairlist
      objects](#Pairlist-objects)
    - [2.1.12 The "Any"
      type](#Any_002dtype)
  - [2.2 Attributes](#Attributes)
    - [2.2.1 Names](#Names)
    - [2.2.2 Dimensions](#Dimensions)
    - [2.2.3 Dimnames](#Dimnames)
    - [2.2.4 Classes](#Classes)
    - [2.2.5 Time series
      attributes](#Time-series-attributes)
    - [2.2.6 Copying of
      attributes](#Copying-of-attributes)
  - [2.3 Special compound
    objects](#Special-compound-objects)
    - [2.3.1 Factors](#Factors)
    - [2.3.2 Data frame
      objects](#Data-frame-objects)
- [3 Evaluation of
  expressions](#Evaluation-of-expressions)
  - [3.1 Simple
    evaluation](#Simple-evaluation)
    - [3.1.1 Constants](#Constants)
    - [3.1.2 Symbol lookup](#Symbol-lookup)
    - [3.1.3 Function
      calls](#Function-calls)
    - [3.1.4 Operators](#Operators)
  - [3.2 Control
    structures](#Control-structures)
    - [3.2.1 if](#if)
    - [3.2.2 Looping](#Looping)
    - [3.2.3 repeat](#repeat)
    - [3.2.4 while](#while)
    - [3.2.5 for](#for)
    - [3.2.6 switch](#switch)
  - [3.3 Elementary arithmetic
    operations](#Elementary-arithmetic-operations)
    - [3.3.1 Recycling
      rules](#Recycling-rules)
    - [3.3.2 Propagation of
      names](#Propagation-of-names)
    - [3.3.3 Dimensional
      attributes](#Dimensional-attributes)
    - [3.3.4 NA handling](#NA-handling)
  - [3.4 Indexing](#Indexing)
    - [3.4.1 Indexing by
      vectors](#Indexing-by-vectors)
    - [3.4.2 Indexing matrices and
      arrays](#Indexing-matrices-and-arrays)
    - [3.4.3 Indexing other
      structures](#Indexing-other-structures)
    - [3.4.4 Subset
      assignment](#Subset-assignment)
  - [3.5 Scope of
    variables](#Scope-of-variables)
    - [3.5.1 Global
      environment](#Global-environment)
    - [3.5.2 Lexical
      environment](#Lexical-environment)
    - [3.5.3 The call stack](#Stacks)
    - [3.5.4 Search path](#Search-path)
- [4 Functions](#Functions)
  - [4.1 Writing
    functions](#Writing-functions)
    - [4.1.1 Syntax and
      examples](#Syntax-and-examples)
    - [4.1.2 Arguments](#Arguments)
  - [4.2 Functions as
    objects](#Functions-as-objects)
  - [4.3 Evaluation](#Evaluation)
    - [4.3.1 Evaluation
      environment](#Evaluation-environment)
    - [4.3.2 Argument
      matching](#Argument-matching)
    - [4.3.3 Argument
      evaluation](#Argument-evaluation)
    - [4.3.4 Scope](#Scope)
- [5 Object-oriented
  programming](#Object_002doriented-programming)
  - [5.1 Definition](#Definition)
  - [5.2 Inheritance](#Inheritance)
  - [5.3 Method
    dispatching](#Method-dispatching)
  - [5.4 UseMethod](#UseMethod)
  - [5.5 NextMethod](#NextMethod)
  - [5.6 Group methods](#Group-methods)
  - [5.7 Writing methods](#Writing-methods)
- [6 Computing on the
  language](#Computing-on-the-language)
  - [6.1 Direct manipulation of language
    objects](#Direct-manipulation-of-language-objects)
  - [6.2 Substitutions](#Substitutions)
  - [6.3 More on
    evaluation](#More-on-evaluation)
  - [6.4 Evaluation of expression
    objects](#Evaluation-of-expression-objects)
  - [6.5 Manipulation of function
    calls](#Manipulation-of-function-calls)
  - [6.6 Manipulation of
    functions](#Manipulation-of-functions)
- [7 System and foreign language
  interfaces](#System-and-foreign-language-interfaces)
  - [7.1 Operating system
    access](#Operating-system-access)
  - [7.2 Foreign language
    interfaces](#Foreign-language-interfaces)
  - [7.3 .Internal and
    .Primitive](#g_t_002eInternal-and-_002ePrimitive)
- [8 Exception
  handling](#Exception-handling)
  - [8.1 stop](#stop)
  - [8.2 warning](#warning)
  - [8.3 on.exit](#on_002eexit)
  - [8.4 Error options](#Error-options)
- [9 Debugging](#Debugging)
  - [9.1 browser](#browser)
  - [9.2
    debug/undebug](#debug_002fundebug)
  - [9.3
    trace/untrace](#trace_002funtrace)
  - [9.4 traceback](#traceback)
- [10 Parser](#Parser)
  - [10.1 The parsing
    process](#The-parsing-process)
    - [10.1.1 Modes of
      parsing](#Modes-of-parsing)
    - [10.1.2 Internal
      representation](#Internal-representation)
    - [10.1.3 Deparsing](#Deparsing)
  - [10.2 Comments](#Comments)
  - [10.3 Tokens](#Tokens)
    - [10.3.1 Constants](#Literal-constants)
    - [10.3.2 Identifiers](#Identifiers)
    - [10.3.3 Reserved
      words](#Reserved-words)
    - [10.3.4 Special
      operators](#Special-operators)
    - [10.3.5 Separators](#Separators)
    - [10.3.6 Operator
      tokens](#Operator-tokens)
    - [10.3.7 Grouping](#Grouping)
    - [10.3.8 Indexing
      tokens](#Indexing-tokens)
  - [10.4 Expressions](#Expressions)
    - [10.4.1 Function
      calls](#Function-calls-_0028expressions_0029)
    - [10.4.2 Infix and prefix
      operators](#Infix-and-prefix-operators)
    - [10.4.3 Index
      constructions](#Index-constructions)
    - [10.4.4 Compound
      expressions](#Compound-expressions)
    - [10.4.5 Flow control
      elements](#Flow-control-elements)
    - [10.4.6 Function
      definitions](#Function-definitions)
  - [10.5 Directives](#Directives)
- [Function and Variable
  Index](#Function-and-Variable-Index)
- [Concept Index](#Concept-Index)
- [Appendix A References](#References)

# R Language Definition

This is an introduction to the R language, explaining evaluation,
parsing, object oriented programming, computing on the language, and so
forth.

This manual is for R, version 3.6.3 (2020-02-29).

Copyright © 2000--2018 R Core Team

> Permission is granted to make and distribute verbatim copies of this
> manual provided the copyright notice and this permission notice are
> preserved on all copies.
>
> Permission is granted to copy and distribute modified versions of this
> manual under the conditions for verbatim copying, provided that the
> entire resulting derived work is distributed under the terms of a
> permission notice identical to this one.
>
> Permission is granted to copy and distribute translations of this
> manual into another language, under the above conditions for modified
> versions, except that this permission notice may be stated in a
> translation approved by the R Core Team.

---

• [Introduction](#Introduction)     
 • [Objects](#Objects)     
 • [Evaluation of expressions](#Evaluation-of-expressions)     
 • [Functions](#Functions)     
 • [Object-oriented programming](#Object_002doriented-programming)     
 • [Computing on the language](#Computing-on-the-language)     
 • [System and foreign language interfaces](#System-and-foreign-language-interfaces)     
 • [Exception handling](#Exception-handling)     
 • [Debugging](#Debugging)     
 • [Parser](#Parser)     
 • [Function and Variable Index](#Function-and-Variable-Index)     
 • [Concept Index](#Concept-Index)     
 • [References](#References)

---

---
