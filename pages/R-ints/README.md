---
Generator: texi2any
description: R Internals
distribution: global
keywords: R Internals
resource-type: document
title: R Internals
---

# R Internals

## Table of Contents

- [1 R Internal
  Structures](#R-Internal-Structures)
  - [1.1 SEXPs](#SEXPs)
    - [1.1.1 SEXPTYPEs](#SEXPTYPEs)
    - [1.1.2 Rest of
      header](#Rest-of-header)
    - [1.1.3 The
      'data'](#The-_0027data_0027)
    - [1.1.4 Allocation
      classes](#Allocation-classes)
  - [1.2 Environments and variable
    lookup](#Environments-and-variable-lookup)
    - [1.2.1 Search paths](#Search-paths)
    - [1.2.2 Namespaces](#Namespaces)
    - [1.2.3 Hash table](#Hash-table)
  - [1.3 Attributes](#Attributes)
  - [1.4 Contexts](#Contexts)
  - [1.5 Argument
    evaluation](#Argument-evaluation)
    - [1.5.1 Missingness](#Missingness)
    - [1.5.2 Dot-dot-dot
      arguments](#Dot_002ddot_002ddot-arguments)
  - [1.6 Autoprinting](#Autoprinting)
  - [1.7 The write barrier and the garbage
    collector](#The-write-barrier)
  - [1.8 Serialization
    Formats](#Serialization-Formats)
  - [1.9 Encodings for
    CHARSXPs](#Encodings-for-CHARSXPs)
  - [1.10 The CHARSXP
    cache](#The-CHARSXP-cache)
  - [1.11 Warnings and
    errors](#Warnings-and-errors)
  - [1.12 S4 objects](#S4-objects)
    - [1.12.1 Representation of S4
      objects](#Representation-of-S4-objects)
    - [1.12.2 S4 classes](#S4-classes)
    - [1.12.3 S4 methods](#S4-methods)
    - [1.12.4 Mechanics of S4
      dispatch](#Mechanics-of-S4-dispatch)
  - [1.13 Memory
    allocators](#Memory-allocators)
    - [1.13.1 Internals of
      R_alloc](#Internals-of-R_005falloc)
  - [1.14 Internal use of global and base
    environments](#Internal-use-of-global-and-base-environments)
    - [1.14.1 Base
      environment](#Base-environment)
    - [1.14.2 Global
      environment](#Global-environment)
  - [1.15 Modules](#Modules)
  - [1.16 Visibility](#Visibility)
    - [1.16.1 Hiding C entry
      points](#Hiding-C-entry-points)
    - [1.16.2 Variables in Windows
      DLLs](#Variables-in-Windows-DLLs)
  - [1.17 Lazy loading](#Lazy-loading)
- [2 `.Internal` vs
  `.Primitive`](#g_t_002eInternal-vs-_002ePrimitive)
  - [2.1 Special
    primitives](#Special-primitives)
  - [2.2 Special
    internals](#Special-internals)
  - [2.3 Prototypes for
    primitives](#Prototypes-for-primitives)
  - [2.4 Adding a
    primitive](#Adding-a-primitive)
- [3 Internationalization in the R
  sources](#Internationalization-in-the-R-sources)
  - [3.1 R code](#R-code)
  - [3.2 Main C code](#Main-C-code)
  - [3.3 Windows-GUI-specific
    code](#Windows_002dGUI_002dspecific-code)
  - [3.4 macOS GUI](#macOS-GUI)
  - [3.5 Updating](#Updating)
- [4 Structure of an Installed
  Package](#Package-Structure)
  - [4.1 Metadata](#Metadata)
  - [4.2 Help](#Help)
- [5 Files](#Files)
- [6 Graphics](#Graphics-Devices)
  - [6.1 Graphics
    Devices](#Graphics-devices)
    - [6.1.1 Device
      structures](#Device-structures)
    - [6.1.2 Device
      capabilities](#Device-capabilities)
    - [6.1.3 Handling text](#Handling-text)
    - [6.1.4 Conventions](#Conventions)
    - [6.1.5 'Mode'](#g_t_0027Mode_0027)
    - [6.1.6 Graphics
      events](#Graphics-events)
    - [6.1.7 Specific
      devices](#Specific-devices)
      - [6.1.7.1 X11()](#X11_0028_0029)
      - [6.1.7.2
        windows()](#windows_0028_0029)
  - [6.2 Colours](#Colours)
  - [6.3 Base graphics](#Base-graphics)
    - [6.3.1 Arguments and
      parameters](#Arguments-and-parameters)
  - [6.4 Grid graphics](#Grid-graphics)
- [7 GUI consoles](#GUI-consoles)
  - [7.1 R.app](#R_002eapp)
- [8 Tools](#Tools)
- [9 R coding
  standards](#R-coding-standards)
- [10 Testing R code](#Testing-R-code)
- [11 Use of TeX
  dialects](#Use-of-TeX-dialects)
- [12 Current and future
  directions](#Current-and-future-directions)
  - [12.1 Long vectors](#Long-vectors)
  - [12.2 64-bit
    types](#g_t64_002dbit-types)
  - [12.3 Large matrices](#Large-matrices)
- [Function and variable
  index](#Function-and-variable-index)
- [Concept index](#Concept-index)

# R Internals

This is a guide to the internal structures of R and coding standards for
the core team working on R itself.

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

• [R Internal Structures](#R-Internal-Structures)     
 • [.Internal vs .Primitive](#g_t_002eInternal-vs-_002ePrimitive)     
 • [Internationalization in the R sources](#Internationalization-in-the-R-sources)     
 • [Package Structure](#Package-Structure)     
 • [Files](#Files)     
 • [Graphics Devices](#Graphics-Devices)     
 • [GUI consoles](#GUI-consoles)     
 • [Tools](#Tools)     
 • [R coding standards](#R-coding-standards)     
 • [Testing R code](#Testing-R-code)     
 • [Use of TeX dialects](#Use-of-TeX-dialects)     
 • [Current and future directions](#Current-and-future-directions)     
 • [Function and variable index](#Function-and-variable-index)     
 • [Concept index](#Concept-index)

---

---
