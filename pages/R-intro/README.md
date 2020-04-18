---
Generator: texi2any
description: An Introduction to R
distribution: global
keywords: An Introduction to R
resource-type: document
title: An Introduction to R
---

# An Introduction to R

## Table of Contents

- [Preface](#Preface)
- [1 Introduction and
  preliminaries](#Introduction-and-preliminaries)
  - [1.1 The R
    environment](#The-R-environment)
  - [1.2 Related software and
    documentation](#Related-software-and-documentation)
  - [1.3 R and
    statistics](#R-and-statistics)
  - [1.4 R and the window
    system](#R-and-the-window-system)
  - [1.5 Using R
    interactively](#Using-R-interactively)
  - [1.6 An introductory
    session](#An-introductory-session)
  - [1.7 Getting help with functions and
    features](#Getting-help)
  - [1.8 R commands, case sensitivity,
    etc.](#R-commands_003b-case-sensitivity-etc)
  - [1.9 Recall and correction of previous
    commands](#Recall-and-correction-of-previous-commands)
  - [1.10 Executing commands from or diverting output to a
    file](#Executing-commands-from-or-diverting-output-to-a-file)
  - [1.11 Data permanency and removing
    objects](#Data-permanency-and-removing-objects)
- [2 Simple manipulations; numbers and
  vectors](#Simple-manipulations-numbers-and-vectors)
  - [2.1 Vectors and
    assignment](#Vectors-and-assignment)
  - [2.2 Vector
    arithmetic](#Vector-arithmetic)
  - [2.3 Generating regular
    sequences](#Generating-regular-sequences)
  - [2.4 Logical vectors](#Logical-vectors)
  - [2.5 Missing values](#Missing-values)
  - [2.6 Character
    vectors](#Character-vectors)
  - [2.7 Index vectors; selecting and modifying subsets of a data
    set](#Index-vectors)
  - [2.8 Other types of
    objects](#Other-types-of-objects)
- [3 Objects, their modes and
  attributes](#Objects)
  - [3.1 Intrinsic attributes: mode and
    length](#The-intrinsic-attributes-mode-and-length)
  - [3.2 Changing the length of an
    object](#Changing-the-length-of-an-object)
  - [3.3 Getting and setting
    attributes](#Getting-and-setting-attributes)
  - [3.4 The class of an
    object](#The-class-of-an-object)
- [4 Ordered and unordered
  factors](#Factors)
  - [4.1 A specific
    example](#A-specific-example)
  - [4.2 The function `tapply()` and ragged
    arrays](#The-function-tapply_0028_0029-and-ragged-arrays)
  - [4.3 Ordered factors](#Ordered-factors)
- [5 Arrays and
  matrices](#Arrays-and-matrices)
  - [5.1 Arrays](#Arrays)
  - [5.2 Array indexing. Subsections of an
    array](#Array-indexing)
  - [5.3 Index matrices](#Index-matrices)
  - [5.4 The `array()`
    function](#The-array_0028_0029-function)
    - [5.4.1 Mixed vector and array arithmetic. The recycling
      rule](#The-recycling-rule)
  - [5.5 The outer product of two
    arrays](#The-outer-product-of-two-arrays)
  - [5.6 Generalized transpose of an
    array](#Generalized-transpose-of-an-array)
  - [5.7 Matrix
    facilities](#Matrix-facilities)
    - [5.7.1 Matrix
      multiplication](#Multiplication)
    - [5.7.2 Linear equations and
      inversion](#Linear-equations-and-inversion)
    - [5.7.3 Eigenvalues and
      eigenvectors](#Eigenvalues-and-eigenvectors)
    - [5.7.4 Singular value decomposition and
      determinants](#Singular-value-decomposition-and-determinants)
    - [5.7.5 Least squares fitting and the QR
      decomposition](#Least-squares-fitting-and-the-QR-decomposition)
  - [5.8 Forming partitioned matrices, `cbind()` and
    `rbind()`](#Forming-partitioned-matrices)
  - [5.9 The concatenation function, `c()`, with
    arrays](#The-concatenation-function-c_0028_0029-with-arrays)
  - [5.10 Frequency tables from
    factors](#Frequency-tables-from-factors)
- [6 Lists and data
  frames](#Lists-and-data-frames)
  - [6.1 Lists](#Lists)
  - [6.2 Constructing and modifying
    lists](#Constructing-and-modifying-lists)
    - [6.2.1 Concatenating
      lists](#Concatenating-lists)
  - [6.3 Data frames](#Data-frames)
    - [6.3.1 Making data
      frames](#Making-data-frames)
    - [6.3.2 `attach()` and
      `detach()`](#attach_0028_0029-and-detach_0028_0029)
    - [6.3.3 Working with data
      frames](#Working-with-data-frames)
    - [6.3.4 Attaching arbitrary
      lists](#Attaching-arbitrary-lists)
    - [6.3.5 Managing the search
      path](#Managing-the-search-path)
- [7 Reading data from
  files](#Reading-data-from-files)
  - [7.1 The `read.table()`
    function](#The-read_002etable_0028_0029-function)
  - [7.2 The `scan()`
    function](#The-scan_0028_0029-function)
  - [7.3 Accessing builtin
    datasets](#Accessing-builtin-datasets)
    - [7.3.1 Loading data from other R
      packages](#Loading-data-from-other-R-packages)
  - [7.4 Editing data](#Editing-data)
- [8 Probability
  distributions](#Probability-distributions)
  - [8.1 R as a set of statistical
    tables](#R-as-a-set-of-statistical-tables)
  - [8.2 Examining the distribution of a set of
    data](#Examining-the-distribution-of-a-set-of-data)
  - [8.3 One- and two-sample
    tests](#One_002d-and-two_002dsample-tests)
- [9 Grouping, loops and conditional
  execution](#Loops-and-conditional-execution)
  - [9.1 Grouped
    expressions](#Grouped-expressions)
  - [9.2 Control
    statements](#Control-statements)
    - [9.2.1 Conditional execution: `if`
      statements](#Conditional-execution)
    - [9.2.2 Repetitive execution: `for` loops, `repeat` and
      `while`](#Repetitive-execution)
- [10 Writing your own
  functions](#Writing-your-own-functions)
  - [10.1 Simple examples](#Simple-examples)
  - [10.2 Defining new binary
    operators](#Defining-new-binary-operators)
  - [10.3 Named arguments and
    defaults](#Named-arguments-and-defaults)
  - [10.4 The '`…`'
    argument](#The-three-dots-argument)
  - [10.5 Assignments within
    functions](#Assignment-within-functions)
  - [10.6 More advanced
    examples](#More-advanced-examples)
    - [10.6.1 Efficiency factors in block
      designs](#Efficiency-factors-in-block-designs)
    - [10.6.2 Dropping all names in a printed
      array](#Dropping-all-names-in-a-printed-array)
    - [10.6.3 Recursive numerical
      integration](#Recursive-numerical-integration)
  - [10.7 Scope](#Scope)
  - [10.8 Customizing the
    environment](#Customizing-the-environment)
  - [10.9 Classes, generic functions and object
    orientation](#Object-orientation)
- [11 Statistical models in
  R](#Statistical-models-in-R)
  - [11.1 Defining statistical models;
    formulae](#Formulae-for-statistical-models)
    - [11.1.1 Contrasts](#Contrasts)
  - [11.2 Linear models](#Linear-models)
  - [11.3 Generic functions for extracting model
    information](#Generic-functions-for-extracting-model-information)
  - [11.4 Analysis of variance and model
    comparison](#Analysis-of-variance-and-model-comparison)
    - [11.4.1 ANOVA tables](#ANOVA-tables)
  - [11.5 Updating fitted
    models](#Updating-fitted-models)
  - [11.6 Generalized linear
    models](#Generalized-linear-models)
    - [11.6.1 Families](#Families)
    - [11.6.2 The `glm()`
      function](#The-glm_0028_0029-function)
  - [11.7 Nonlinear least squares and maximum likelihood
    models](#Nonlinear-least-squares-and-maximum-likelihood-models)
    - [11.7.1 Least squares](#Least-squares)
    - [11.7.2 Maximum
      likelihood](#Maximum-likelihood)
  - [11.8 Some non-standard
    models](#Some-non_002dstandard-models)
- [12 Graphical procedures](#Graphics)
  - [12.1 High-level plotting
    commands](#High_002dlevel-plotting-commands)
    - [12.1.1 The `plot()`
      function](#The-plot_0028_0029-function)
    - [12.1.2 Displaying multivariate
      data](#Displaying-multivariate-data)
    - [12.1.3 Display
      graphics](#Display-graphics)
    - [12.1.4 Arguments to high-level plotting
      functions](#Arguments-to-high_002dlevel-plotting-functions)
  - [12.2 Low-level plotting
    commands](#Low_002dlevel-plotting-commands)
    - [12.2.1 Mathematical
      annotation](#Mathematical-annotation)
    - [12.2.2 Hershey vector
      fonts](#Hershey-vector-fonts)
  - [12.3 Interacting with
    graphics](#Interacting-with-graphics)
  - [12.4 Using graphics
    parameters](#Using-graphics-parameters)
    - [12.4.1 Permanent changes: The `par()`
      function](#The-par_0028_0029-function)
    - [12.4.2 Temporary changes: Arguments to graphics
      functions](#Arguments-to-graphics-functions)
  - [12.5 Graphics parameters
    list](#Graphics-parameters)
    - [12.5.1 Graphical
      elements](#Graphical-elements)
    - [12.5.2 Axes and tick
      marks](#Axes-and-tick-marks)
    - [12.5.3 Figure
      margins](#Figure-margins)
    - [12.5.4 Multiple figure
      environment](#Multiple-figure-environment)
  - [12.6 Device drivers](#Device-drivers)
    - [12.6.1 PostScript diagrams for typeset
      documents](#PostScript-diagrams-for-typeset-documents)
    - [12.6.2 Multiple graphics
      devices](#Multiple-graphics-devices)
  - [12.7 Dynamic
    graphics](#Dynamic-graphics)
- [13 Packages](#Packages)
  - [13.1 Standard
    packages](#Standard-packages)
  - [13.2 Contributed packages and
    CRAN](#Contributed-packages-and-CRAN)
  - [13.3 Namespaces](#Namespaces)
- [14 OS facilities](#OS-facilities)
  - [14.1 Files and
    directories](#Files-and-directories)
  - [14.2 Filepaths](#Filepaths)
  - [14.3 System commands](#System-commands)
  - [14.4 Compression and
    Archives](#Compression-and-Archives)
- [Appendix A A sample
  session](#A-sample-session)
- [Appendix B Invoking R](#Invoking-R)
  - [B.1 Invoking R from the command
    line](#Invoking-R-from-the-command-line)
  - [B.2 Invoking R under
    Windows](#Invoking-R-under-Windows)
  - [B.3 Invoking R under
    macOS](#Invoking-R-under-macOS)
  - [B.4 Scripting with
    R](#Scripting-with-R)
- [Appendix C The command-line
  editor](#The-command_002dline-editor)
  - [C.1 Preliminaries](#Preliminaries)
  - [C.2 Editing actions](#Editing-actions)
  - [C.3 Command-line editor
    summary](#Command_002dline-editor-summary)
- [Appendix D Function and variable
  index](#Function-and-variable-index)
- [Appendix E Concept index](#Concept-index)
- [Appendix F References](#References)

# An Introduction to R

This is an introduction to R ("GNU S"), a language and environment for
statistical computing and graphics. R is similar to the
award-winning[^1^](#FOOT1) S system, which was developed at Bell
Laboratories by John Chambers et al. It provides a wide variety of
statistical and graphical techniques (linear and nonlinear modelling,
statistical tests, time series analysis, classification, clustering,
\...).

This manual provides information on data types, programming elements,
statistical modelling and graphics.

This manual is for R, version 3.6.3 (2020-02-29).

Copyright © 1990 W. N. Venables\
Copyright © 1992 W. N. Venables & D. M. Smith\
Copyright © 1997 R. Gentleman & R. Ihaka\
Copyright © 1997, 1998 M. Maechler\
Copyright © 1999--2018 R Core Team

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

• [Preface](#Preface)     
 • [Introduction and preliminaries](#Introduction-and-preliminaries)     
 • [Simple manipulations numbers and vectors](#Simple-manipulations-numbers-and-vectors)     
 • [Objects](#Objects)     
 • [Factors](#Factors)     
 • [Arrays and matrices](#Arrays-and-matrices)     
 • [Lists and data frames](#Lists-and-data-frames)     
 • [Reading data from files](#Reading-data-from-files)     
 • [Probability distributions](#Probability-distributions)     
 • [Loops and conditional execution](#Loops-and-conditional-execution)     
 • [Writing your own functions](#Writing-your-own-functions)     
 • [Statistical models in R](#Statistical-models-in-R)     
 • [Graphics](#Graphics)     
 • [Packages](#Packages)     
 • [OS facilities](#OS-facilities)     
 • [A sample session](#A-sample-session)     
 • [Invoking R](#Invoking-R)     
 • [The command-line editor](#The-command_002dline-editor)     
 • [Function and variable index](#Function-and-variable-index)     
 • [Concept index](#Concept-index)     
 • [References](#References)

---

---

## Preface

This introduction to R is derived from an original set of notes
describing the S and [S-PLUS] environments written in 1990--2 by
Bill Venables and David M. Smith when at the University of Adelaide. We
have made a number of small changes to reflect differences between the R
and S programs, and expanded some of the material.

We would like to extend warm thanks to Bill Venables (and David Smith)
for granting permission to distribute this modified version of the notes
in this way, and for being a supporter of R from way back.

Comments and corrections are always welcome. Please address email
correspondence to <R-core@R-project.org>.

#### Suggestions to the reader

Most R novices will start with the introductory session in Appendix A.
This should give some familiarity with the style of R sessions and more
importantly some instant feedback on what actually happens.

Many users will come to R mainly for its graphical facilities. See
[Graphics](#Graphics), which can be read at almost any time and need not
wait until all the preceding sections have been digested.

---

• [Introduction and preliminaries](#Introduction-and-preliminaries)

---

---
