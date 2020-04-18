---
Generator: texi2any
description: Writing R Extensions
distribution: global
keywords: Writing R Extensions
resource-type: document
title: Writing R Extensions
---

# Writing R Extensions

## Table of Contents

- [Acknowledgements](#Acknowledgements)
- [1 Creating R
  packages](#Creating-R-packages)
  - [1.1 Package
    structure](#Package-structure)
    - [1.1.1 The `DESCRIPTION`
      file](#The-DESCRIPTION-file)
    - [1.1.2 Licensing](#Licensing)
    - [1.1.3 Package
      Dependencies](#Package-Dependencies)
      - [1.1.3.1 Suggested
        packages](#Suggested-packages)
    - [1.1.4 The `INDEX`
      file](#The-INDEX-file)
    - [1.1.5 Package
      subdirectories](#Package-subdirectories)
    - [1.1.6 Data in
      packages](#Data-in-packages)
    - [1.1.7 Non-R scripts in
      packages](#Non_002dR-scripts-in-packages)
    - [1.1.8 Specifying
      URLs](#Specifying-URLs)
  - [1.2 Configure and
    cleanup](#Configure-and-cleanup)
    - [1.2.1 Using
      `Makevars`](#Using-Makevars)
      - [1.2.1.1 OpenMP
        support](#OpenMP-support)
      - [1.2.1.2 Using
        pthreads](#Using-pthreads)
      - [1.2.1.3 Compiling in
        sub-directories](#Compiling-in-sub_002ddirectories)
    - [1.2.2 Configure
      example](#Configure-example)
    - [1.2.3 Using F9x
      code](#Using-F9x-code)
    - [1.2.4 Using C++11
      code](#Using-C_002b_002b11-code)
    - [1.2.5 Using C++14
      code](#Using-C_002b_002b14-code)
    - [1.2.6 Using C++17
      code](#Using-C_002b_002b17-code)
  - [1.3 Checking and building
    packages](#Checking-and-building-packages)
    - [1.3.1 Checking
      packages](#Checking-packages)
    - [1.3.2 Building package
      tarballs](#Building-package-tarballs)
    - [1.3.3 Building binary
      packages](#Building-binary-packages)
  - [1.4 Writing package
    vignettes](#Writing-package-vignettes)
    - [1.4.1 Encodings and
      vignettes](#Encodings-and-vignettes)
    - [1.4.2 Non-Sweave
      vignettes](#Non_002dSweave-vignettes)
  - [1.5 Package
    namespaces](#Package-namespaces)
    - [1.5.1 Specifying imports and
      exports](#Specifying-imports-and-exports)
    - [1.5.2 Registering S3
      methods](#Registering-S3-methods)
    - [1.5.3 Load hooks](#Load-hooks)
    - [1.5.4 useDynLib](#useDynLib)
    - [1.5.5 An example](#An-example)
    - [1.5.6 Namespaces with S4 classes and
      methods](#Namespaces-with-S4-classes-and-methods)
  - [1.6 Writing portable
    packages](#Writing-portable-packages)
    - [1.6.1 PDF size](#PDF-size)
    - [1.6.2 Check timing](#Check-timing)
    - [1.6.3 Encoding
      issues](#Encoding-issues)
    - [1.6.4 Portable C and C++
      code](#Portable-C-and-C_002b_002b-code)
      - [1.6.4.1 Common
        symbols](#Common-symbols)
    - [1.6.5 Binary
      distribution](#Binary-distribution)
  - [1.7 Diagnostic
    messages](#Diagnostic-messages)
  - [1.8
    Internationalization](#Internationalization)
    - [1.8.1 C-level
      messages](#C_002dlevel-messages)
    - [1.8.2 R messages](#R-messages)
    - [1.8.3 Preparing
      translations](#Preparing-translations)
  - [1.9 CITATION files](#CITATION-files)
  - [1.10 Package types](#Package-types)
    - [1.10.1 Frontend](#Frontend)
  - [1.11 Services](#Services)
- [2 Writing R documentation
  files](#Writing-R-documentation-files)
  - [2.1 Rd format](#Rd-format)
    - [2.1.1 Documenting
      functions](#Documenting-functions)
    - [2.1.2 Documenting data
      sets](#Documenting-data-sets)
    - [2.1.3 Documenting S4 classes and
      methods](#Documenting-S4-classes-and-methods)
    - [2.1.4 Documenting
      packages](#Documenting-packages)
  - [2.2 Sectioning](#Sectioning)
  - [2.3 Marking text](#Marking-text)
  - [2.4 Lists and
    tables](#Lists-and-tables)
  - [2.5
    Cross-references](#Cross_002dreferences)
  - [2.6 Mathematics](#Mathematics)
  - [2.7 Figures](#Figures)
  - [2.8 Insertions](#Insertions)
  - [2.9 Indices](#Indices)
  - [2.10 Platform-specific
    documentation](#Platform_002dspecific-sections)
  - [2.11 Conditional
    text](#Conditional-text)
  - [2.12 Dynamic pages](#Dynamic-pages)
  - [2.13 User-defined
    macros](#User_002ddefined-macros)
  - [2.14 Encoding](#Encoding)
  - [2.15 Processing documentation
    files](#Processing-documentation-files)
  - [2.16 Editing Rd
    files](#Editing-Rd-files)
- [3 Tidying and profiling R
  code](#Tidying-and-profiling-R-code)
  - [3.1 Tidying R code](#Tidying-R-code)
  - [3.2 Profiling R code for
    speed](#Profiling-R-code-for-speed)
  - [3.3 Profiling R code for memory
    use](#Profiling-R-code-for-memory-use)
    - [3.3.1 Memory statistics from
      `Rprof`](#Memory-statistics-from-Rprof)
    - [3.3.2 Tracking memory
      allocations](#Tracking-memory-allocations)
    - [3.3.3 Tracing copies of an
      object](#Tracing-copies-of-an-object)
  - [3.4 Profiling compiled
    code](#Profiling-compiled-code)
    - [3.4.1 Linux](#Linux)
      - [3.4.1.1 sprof](#sprof)
      - [3.4.1.2 oprofile and
        operf](#oprofile-and-operf)
    - [3.4.2 Solaris](#Solaris)
    - [3.4.3 macOS](#macOS)
- [4 Debugging](#Debugging)
  - [4.1 Browsing](#Browsing)
  - [4.2 Debugging R
    code](#Debugging-R-code)
  - [4.3 Checking memory
    access](#Checking-memory-access)
    - [4.3.1 Using
      gctorture](#Using-gctorture)
    - [4.3.2 Using
      valgrind](#Using-valgrind)
    - [4.3.3 Using the Address
      Sanitizer](#Using-Address-Sanitizer)
      - [4.3.3.1 Using the Leak
        Sanitizer](#Using-Leak-Sanitizer)
    - [4.3.4 Using the Undefined Behaviour
      Sanitizer](#Using-Undefined-Behaviour-Sanitizer)
    - [4.3.5 Other analyses with
      'clang'](#Other-analyses-with-_0060clang_0027)
    - [4.3.6 Using 'Dr.
      Memory'](#Using-_0060Dr_002e-Memory_0027)
    - [4.3.7 Fortran array bounds
      checking](#Fortran-array-bounds-checking)
  - [4.4 Debugging compiled
    code](#Debugging-compiled-code)
    - [4.4.1 Finding entry points in dynamically loaded
      code](#Finding-entry-points)
    - [4.4.2 Inspecting R objects when
      debugging](#Inspecting-R-objects)
  - [4.5 Using Link-time
    Optimization](#Using-Link_002dtime-Optimization)
- [5 System and foreign language
  interfaces](#System-and-foreign-language-interfaces)
  - [5.1 Operating system
    access](#Operating-system-access)
  - [5.2 Interface functions `.C` and
    `.Fortran`](#Interface-functions-_002eC-and-_002eFortran)
  - [5.3 `dyn.load` and
    `dyn.unload`](#dyn_002eload-and-dyn_002eunload)
  - [5.4 Registering native
    routines](#Registering-native-routines)
    - [5.4.1 Speed
      considerations](#Speed-considerations)
    - [5.4.2 Example: converting a package to use
      registration](#Converting-a-package-to-use-registration)
    - [5.4.3 Linking to native routines in other
      packages](#Linking-to-native-routines-in-other-packages)
  - [5.5 Creating shared
    objects](#Creating-shared-objects)
  - [5.6 Interfacing C++
    code](#Interfacing-C_002b_002b-code)
    - [5.6.1 External C++
      code](#External-C_002b_002b-code)
  - [5.7 Fortran I/O](#Fortran-I_002fO)
  - [5.8 Linking to other
    packages](#Linking-to-other-packages)
    - [5.8.1
      Unix-alikes](#Unix_002dalikes)
    - [5.8.2 Windows](#Windows)
  - [5.9 Handling R objects in
    C](#Handling-R-objects-in-C)
    - [5.9.1 Handling the effects of garbage
      collection](#Garbage-Collection)
    - [5.9.2 Allocating
      storage](#Allocating-storage)
    - [5.9.3 Details of R
      types](#Details-of-R-types)
    - [5.9.4 Attributes](#Attributes)
    - [5.9.5 Classes](#Classes)
    - [5.9.6 Handling
      lists](#Handling-lists)
    - [5.9.7 Handling character
      data](#Handling-character-data)
    - [5.9.8 Finding and setting
      variables](#Finding-and-setting-variables)
    - [5.9.9 Some convenience
      functions](#Some-convenience-functions)
      - [5.9.9.1 Semi-internal convenience
        functions](#Semi_002dinternal-convenience-functions)
    - [5.9.10 Named objects and
      copying](#Named-objects-and-copying)
  - [5.10 Interface functions `.Call` and
    `.External`](#Interface-functions-_002eCall-and-_002eExternal)
    - [5.10.1 Calling
      `.Call`](#Calling-_002eCall)
    - [5.10.2 Calling
      `.External`](#Calling-_002eExternal)
    - [5.10.3 Missing and special
      values](#Missing-and-special-values)
  - [5.11 Evaluating R expressions from
    C](#Evaluating-R-expressions-from-C)
    - [5.11.1
      Zero-finding](#Zero_002dfinding)
    - [5.11.2 Calculating numerical
      derivatives](#Calculating-numerical-derivatives)
  - [5.12 Parsing R code from
    C](#Parsing-R-code-from-C)
    - [5.12.1 Accessing source
      references](#Accessing-source-references)
  - [5.13 External pointers and weak
    references](#External-pointers-and-weak-references)
    - [5.13.1 An
      example](#An-external-pointer-example)
  - [5.14 Vector accessor
    functions](#Vector-accessor-functions)
  - [5.15 Character encoding
    issues](#Character-encoding-issues)
- [6 The R API: entry points for C
  code](#The-R-API)
  - [6.1 Memory
    allocation](#Memory-allocation)
    - [6.1.1 Transient storage
      allocation](#Transient-storage-allocation)
    - [6.1.2 User-controlled
      memory](#User_002dcontrolled-memory)
  - [6.2 Error signaling](#Error-signaling)
    - [6.2.1 Error signaling from
      Fortran](#Error-signaling-from-Fortran)
  - [6.3 Random number
    generation](#Random-numbers)
  - [6.4 Missing and IEEE special
    values](#Missing-and-IEEE-values)
  - [6.5 Printing](#Printing)
    - [6.5.1 Printing from
      Fortran](#Printing-from-Fortran)
  - [6.6 Calling C from Fortran and vice
    versa](#Calling-C-from-Fortran-and-vice-versa)
    - [6.6.1 Fortran character
      strings](#Fortran-character-strings)
    - [6.6.2 Fortran
      LOGICAL](#Fortran-LOGICAL)
  - [6.7 Numerical analysis
    subroutines](#Numerical-analysis-subroutines)
    - [6.7.1 Distribution
      functions](#Distribution-functions)
    - [6.7.2 Mathematical
      functions](#Mathematical-functions)
    - [6.7.3 Numerical
      Utilities](#Numerical-Utilities)
    - [6.7.4 Mathematical
      constants](#Mathematical-constants)
  - [6.8 Optimization](#Optimization)
  - [6.9 Integration](#Integration)
  - [6.10 Utility
    functions](#Utility-functions)
  - [6.11 Re-encoding](#Re_002dencoding)
  - [6.12 Condition handling and cleanup
    code](#Condition-handling-and-cleanup-code)
  - [6.13 Allowing
    interrupts](#Allowing-interrupts)
  - [6.14 Platform and version
    information](#Platform-and-version-information)
  - [6.15 Inlining C
    functions](#Inlining-C-functions)
  - [6.16 Controlling
    visibility](#Controlling-visibility)
  - [6.17 Using these functions in your own C
    code](#Standalone-Mathlib)
  - [6.18 Organization of header
    files](#Organization-of-header-files)
- [7 Generic functions and
  methods](#Generic-functions-and-methods)
  - [7.1 Adding new
    generics](#Adding-new-generics)
- [8 Linking GUIs and other front-ends to
  R](#Linking-GUIs-and-other-front_002dends-to-R)
  - [8.1 Embedding R under
    Unix-alikes](#Embedding-R-under-Unix_002dalikes)
    - [8.1.1 Compiling against the R
      library](#Compiling-against-the-R-library)
    - [8.1.2 Setting R
      callbacks](#Setting-R-callbacks)
    - [8.1.3 Registering
      symbols](#Registering-symbols)
    - [8.1.4 Meshing event
      loops](#Meshing-event-loops)
    - [8.1.5 Threading
      issues](#Threading-issues)
  - [8.2 Embedding R under
    Windows](#Embedding-R-under-Windows)
    - [8.2.1 Using
      (D)COM](#Using-_0028D_0029COM)
    - [8.2.2 Calling R.dll
      directly](#Calling-R_002edll-directly)
    - [8.2.3 Finding
      R_HOME](#Finding-R_005fHOME)
- [Function and variable
  index](#Function-and-variable-index)
- [Concept index](#Concept-index)

# Writing R Extensions

This is a guide to extending R, describing the process of creating R
add-on packages, writing R documentation, R's system and foreign
language interfaces, and the R API.

This manual is for R, version 3.6.3 (2020-02-29).

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

• [Acknowledgements](#Acknowledgements)     
 • [Creating R packages](#Creating-R-packages)     
 • [Writing R documentation files](#Writing-R-documentation-files)     
 • [Tidying and profiling R code](#Tidying-and-profiling-R-code)     
 • [Debugging](#Debugging)     
 • [System and foreign language interfaces](#System-and-foreign-language-interfaces)     
 • [The R API](#The-R-API)     
 • [Generic functions and methods](#Generic-functions-and-methods)     
 • [Linking GUIs and other front-ends to R](#Linking-GUIs-and-other-front_002dends-to-R)     
 • [Function and variable index](#Function-and-variable-index)     
 • [Concept index](#Concept-index)

---

---

## Acknowledgements

The contributions to early versions of this manual by Saikat DebRoy (who
wrote the first draft of a guide to using `.Call` and `.External`) and
Adrian Trapletti (who provided information on the C++ interface) are
gratefully acknowledged.

---
