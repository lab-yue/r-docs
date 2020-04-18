---
Generator: texi2any
description: R Installation and Administration
distribution: global
keywords: R Installation and Administration
resource-type: document
title: R Installation and Administration
---

# R Installation and Administration

## Table of Contents

- [1 Obtaining R](#Obtaining-R)
  - [1.1 Getting and unpacking the
    sources](#Getting-and-unpacking-the-sources)
  - [1.2 Getting patched and development
    versions](#Getting-patched-and-development-versions)
    - [1.2.1 Using Subversion and
      rsync](#Using-Subversion-and-rsync)
- [2 Installing R under
  Unix-alikes](#Installing-R-under-Unix_002dalikes)
  - [2.1 Simple
    compilation](#Simple-compilation)
  - [2.2 Help options](#Help-options)
  - [2.3 Making the
    manuals](#Making-the-manuals)
  - [2.4 Installation](#Installation)
  - [2.5 Uninstallation](#Uninstallation)
  - [2.6
    Sub-architectures](#Sub_002darchitectures)
    - [2.6.1 Multilib](#Multilib)
  - [2.7 Other Options](#Other-Options)
    - [2.7.1 Debugging
      Symbols](#Debugging-Symbols)
    - [2.7.2 OpenMP
      Support](#OpenMP-Support)
    - [2.7.3 C++
      Support](#C_002b_002b-Support)
    - [2.7.4 Link-Time
      Optimization](#Link_002dTime-Optimization)
  - [2.8 Testing an
    Installation](#Testing-a-Unix_002dalike-Installation)
- [3 Installing R under
  Windows](#Installing-R-under-Windows)
  - [3.1 Building from
    source](#Building-from-source)
    - [3.1.1 Getting the
      tools](#Getting-the-tools)
    - [3.1.2 Getting the source
      files](#Getting-the-source-files)
    - [3.1.3 Building the core
      files](#Building-the-core-files)
    - [3.1.4 Building the cairo
      devices](#Building-the-cairo-devices-files)
    - [3.1.5 Using ICU for
      collation](#Using-ICU-for-collation)
    - [3.1.6 Support for
      libcurl](#Support-for-libcurl)
    - [3.1.7 Checking the
      build](#Checking-the-build)
    - [3.1.8 Building the
      manuals](#Building-the-manuals)
    - [3.1.9 Building the Inno Setup
      installer](#Building-the-Inno-Setup-installer)
    - [3.1.10 Building the MSI
      installer](#Building-the-MSI-installer)
    - [3.1.11 64-bit Windows
      builds](#g_t64_002dbit-Windows-builds)
  - [3.2 Testing an
    Installation](#Testing-a-Windows-Installation)
- [4 Installing R under
  macOS](#Installing-R-under-macOS)
  - [4.1 Running R under
    macOS](#Running-R-under-macOS)
  - [4.2 Uninstalling under
    macOS](#Uninstalling-under-macOS)
  - [4.3 Multiple
    versions](#Multiple-versions)
- [5 Running R](#Running-R)
- [6 Add-on
  packages](#Add_002don-packages)
  - [6.1 Default
    packages](#Default-packages)
  - [6.2 Managing
    libraries](#Managing-libraries)
  - [6.3 Installing
    packages](#Installing-packages)
    - [6.3.1 Windows](#Windows-packages)
    - [6.3.2 macOS](#macOS-packages)
    - [6.3.3 Customizing package
      compilation](#Customizing-package-compilation)
    - [6.3.4 Multiple
      sub-architectures](#Multiple-sub_002darchitectures)
    - [6.3.5
      Byte-compilation](#Byte_002dcompilation)
    - [6.3.6 External
      software](#External-software)
  - [6.4 Updating
    packages](#Updating-packages)
  - [6.5 Removing
    packages](#Removing-packages)
  - [6.6 Setting up a package
    repository](#Setting-up-a-package-repository)
  - [6.7 Checking installed source
    packages](#Checking-installed-source-packages)
- [7 Internationalization and
  Localization](#Internationalization)
  - [7.1 Locales](#Locales)
    - [7.1.1 Locales under
      Unix-alikes](#Locales-under-Unix_002dalikes)
    - [7.1.2 Locales under
      Windows](#Locales-under-Windows)
    - [7.1.3 Locales under
      macOS](#Locales-under-macOS)
  - [7.2 Localization of
    messages](#Localization-of-messages)
- [8 Choosing between 32- and 64-bit
  builds](#Choosing-between-32_002d-and-64_002dbit-builds)
- [9 The standalone Rmath
  library](#The-standalone-Rmath-library)
  - [9.1
    Unix-alikes](#Unix_002dalike-standalone)
  - [9.2 Windows](#Windows-standalone)
- [Appendix A Essential and useful other programs under a
  Unix-alike](#Essential-and-useful-other-programs-under-a-Unix_002dalike)
  - [A.1 Essential programs and
    libraries](#Essential-programs-and-libraries)
  - [A.2 Useful libraries and
    programs](#Useful-libraries-and-programs)
    - [A.2.1 Tcl/Tk](#Tcl_002fTk)
    - [A.2.2 Java support](#Java-support)
    - [A.2.3 Other compiled
      languages](#Other-compiled-languages)
  - [A.3 Linear algebra](#Linear-algebra)
    - [A.3.1 BLAS](#BLAS)
      - [A.3.1.1 ATLAS](#ATLAS)
      - [A.3.1.2 OpenBLAS](#OpenBLAS)
      - [A.3.1.3 Intel MKL](#MKL)
      - [A.3.1.4 Shared BLAS](#Shared-BLAS)
    - [A.3.2 LAPACK](#LAPACK)
    - [A.3.3 Caveats](#Caveats)
- [Appendix B Configuration on a
  Unix-alike](#Configuration-on-a-Unix_002dalike)
  - [B.1 Configuration
    options](#Configuration-options)
  - [B.2 Internationalization
    support](#Internationalization-support)
  - [B.3 Configuration
    variables](#Configuration-variables)
    - [B.3.1 Setting paper
      size](#Setting-paper-size)
    - [B.3.2 Setting the
      browsers](#Setting-the-browsers)
    - [B.3.3 Compilation
      flags](#Compilation-flags)
    - [B.3.4 Making
      manuals](#Making-manuals)
  - [B.4 Setting the
    shell](#Setting-the-shell)
  - [B.5 Using make](#Using-make)
  - [B.6 Using Fortran](#Using-Fortran)
  - [B.7 Compile and load
    flags](#Compile-and-load-flags)
  - [B.8 Maintainer mode](#Maintainer-mode)
- [Appendix C Platform notes](#Platform-notes)
  - [C.1 X11 issues](#X11-issues)
  - [C.2 Linux](#Linux)
    - [C.2.1 Clang](#Clang)
    - [C.2.2 Intel
      compilers](#Intel-compilers)
  - [C.3 macOS](#macOS)
    - [C.3.1 Prerequisites](#Prerequisites)
      - [C.3.1.1 Note for Catalina
        users](#Note-for-Catalina-users)
    - [C.3.2 Recommended C/C++
      compilers](#Recommended-C_002fC_002b_002b-compilers)
    - [C.3.3 Other
      libraries](#Other-libraries)
    - [C.3.4 Tcl/Tk headers and
      libraries](#Tcl_002fTk-headers-and-libraries)
    - [C.3.5 Java](#Java-_0028macOS_0029)
    - [C.3.6 Frameworks](#Frameworks)
    - [C.3.7 Building
      R.app](#Building-R_002eapp)
  - [C.4 Solaris](#Solaris)
    - [C.4.1 64-bit
      builds](#g_t64_002dbit-builds)
    - [C.4.2 Using gcc](#Using-gcc)
  - [C.5 FreeBSD](#FreeBSD)
  - [C.6 OpenBSD](#OpenBSD)
  - [C.7 Cygwin](#Cygwin)
  - [C.8 New platforms](#New-platforms)
- [Appendix D The Windows
  toolset](#The-Windows-toolset)
  - [D.1 LaTeX](#LaTeX)
  - [D.2 The Inno Setup
    installer](#The-Inno-Setup-installer)
  - [D.3 The command line
    tools](#The-command-line-tools)
  - [D.4 The MinGW-w64
    toolchain](#The-MinGW_002dw64-toolchain)
  - [D.5 Useful additional
    programs](#Useful-additional-programs)
- [Function and variable
  index](#Function-and-variable-index)
- [Concept index](#Concept-index)
- [Environment variable
  index](#Environment-variable-index)

# R Installation and Administration

This is a guide to installation and administration for R.

This manual is for R, version 3.6.3 (2020-02-29).

Copyright © 2001--2018 R Core Team

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

• [Obtaining R](#Obtaining-R)     
 • [Installing R under Unix-alikes](#Installing-R-under-Unix_002dalikes)     
 • [Installing R under Windows](#Installing-R-under-Windows)     
 • [Installing R under macOS](#Installing-R-under-macOS)     
 • [Running R](#Running-R)     
 • [Add-on packages](#Add_002don-packages)     
 • [Internationalization](#Internationalization)     
 • [Choosing between 32- and 64-bit builds](#Choosing-between-32_002d-and-64_002dbit-builds)     
 • [The standalone Rmath library](#The-standalone-Rmath-library)     
 • [Essential and useful other programs under a Unix-alike](#Essential-and-useful-other-programs-under-a-Unix_002dalike)     
 • [Configuration on a Unix-alike](#Configuration-on-a-Unix_002dalike)     
 • [Platform notes](#Platform-notes)     
 • [The Windows toolset](#The-Windows-toolset)     
 • [Function and variable index](#Function-and-variable-index)     
 • [Concept index](#Concept-index)     
 • [Environment variable index](#Environment-variable-index)

---

---
