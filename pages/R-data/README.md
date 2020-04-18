---
Generator: texi2any
description: R Data Import/Export
distribution: global
keywords: R Data Import/Export
resource-type: document
title: R Data Import/Export
---

# R Data Import/Export

## Table of Contents

- [Acknowledgements](#Acknowledgements)
- [1 Introduction](#Introduction)
  - [1.1 Imports](#Imports)
    - [1.1.1 Encodings](#Encodings)
  - [1.2 Export to text
    files](#Export-to-text-files)
  - [1.3 XML](#XML)
- [2 Spreadsheet-like
  data](#Spreadsheet_002dlike-data)
  - [2.1 Variations on
    `read.table`](#Variations-on-read_002etable)
  - [2.2 Fixed-width-format
    files](#Fixed_002dwidth_002dformat-files)
  - [2.3 Data Interchange Format
    (DIF)](#Data-Interchange-Format-_0028DIF_0029)
  - [2.4 Using `scan`
    directly](#Using-scan-directly)
  - [2.5 Re-shaping
    data](#Re_002dshaping-data)
  - [2.6 Flat contingency
    tables](#Flat-contingency-tables)
- [3 Importing from other statistical
  systems](#Importing-from-other-statistical-systems)
  - [3.1 EpiInfo, Minitab, S-PLUS, SAS, SPSS, Stata,
    Systat](#EpiInfo-Minitab-SAS-S_002dPLUS-SPSS-Stata-Systat)
  - [3.2 Octave](#Octave)
- [4 Relational
  databases](#Relational-databases)
  - [4.1 Why use a
    database?](#Why-use-a-database_003f)
  - [4.2 Overview of
    RDBMSs](#Overview-of-RDBMSs)
    - [4.2.1 SQL queries](#SQL-queries)
    - [4.2.2 Data types](#Data-types)
  - [4.3 R interface
    packages](#R-interface-packages)
    - [4.3.1 Packages using DBI](#DBI)
    - [4.3.2 Package RODBC](#RODBC)
- [5 Binary files](#Binary-files)
  - [5.1 Binary data
    formats](#Binary-data-formats)
  - [5.2 dBase files
    (DBF)](#dBase-files-_0028DBF_0029)
- [6 Image files](#Image-files)
- [7 Connections](#Connections)
  - [7.1 Types of
    connections](#Types-of-connections)
  - [7.2 Output to
    connections](#Output-to-connections)
  - [7.3 Input from
    connections](#Input-from-connections)
    - [7.3.1 Pushback](#Pushback)
  - [7.4 Listing and manipulating
    connections](#Listing-and-manipulating-connections)
  - [7.5 Binary
    connections](#Binary-connections)
    - [7.5.1 Special
      values](#Special-values)
- [8 Network
  interfaces](#Network-interfaces)
  - [8.1 Reading from
    sockets](#Reading-from-sockets)
  - [8.2 Using
    `download.file`](#Using-download_002efile)
- [9 Reading Excel
  spreadsheets](#Reading-Excel-spreadsheets)
- [Appendix A References](#References)
- [Function and variable
  index](#Function-and-variable-index)
- [Concept index](#Concept-index)

# R Data Import/Export

This is a guide to importing and exporting data to and from R.

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

• [Acknowledgements](#Acknowledgements)     
 • [Introduction](#Introduction)     
 • [Spreadsheet-like data](#Spreadsheet_002dlike-data)     
 • [Importing from other statistical systems](#Importing-from-other-statistical-systems)     
 • [Relational databases](#Relational-databases)     
 • [Binary files](#Binary-files)     
 • [Image files](#Image-files)     
 • [Connections](#Connections)     
 • [Network interfaces](#Network-interfaces)     
 • [Reading Excel spreadsheets](#Reading-Excel-spreadsheets)     
 • [References](#References)     
 • [Function and variable index](#Function-and-variable-index)     
 • [Concept index](#Concept-index)

---

---

## Acknowledgements

The relational databases part of this manual is based in part on an
earlier manual by Douglas Bates and Saikat DebRoy. The principal author
of this manual was Brian Ripley.

Many volunteers have contributed to the packages used here. The
principal authors of the packages mentioned are

> ---
>
> [**DBI**](https://CRAN.R-project.org/package=DBI) David A. James
> [**dataframes2xls**](https://CRAN.R-project.org/package=dataframes2xls) Guido van Steen
> [**foreign**](https://CRAN.R-project.org/package=foreign) Thomas Lumley, Saikat DebRoy, Douglas Bates, Duncan Murdoch and Roger Bivand
> [**gdata**](https://CRAN.R-project.org/package=gdata) Gregory R. Warnes
> [**ncdf4**](https://CRAN.R-project.org/package=ncdf4) David Pierce
> [**rJava**](https://CRAN.R-project.org/package=rJava) Simon Urbanek
> [**RJDBC**](https://CRAN.R-project.org/package=RJDBC) Simon Urbanek
> [**RMySQL**](https://CRAN.R-project.org/package=RMySQL) David James and Saikat DebRoy
> [**RNetCDF**](https://CRAN.R-project.org/package=RNetCDF) Pavel Michna
> [**RODBC**](https://CRAN.R-project.org/package=RODBC) Michael Lapsley and Brian Ripley
> [**ROracle**](https://CRAN.R-project.org/package=ROracle) David A, James
> [**RPostgreSQL**](https://CRAN.R-project.org/package=RPostgreSQL) Sameer Kumar Prayaga and Tomoaki Nishiyama
> **RSPerl** Duncan Temple Lang
> **RSPython** Duncan Temple Lang
> [**RSQLite**](https://CRAN.R-project.org/package=RSQLite) David A, James
> **SJava** John Chambers and Duncan Temple Lang
> [**WriteXLS**](https://CRAN.R-project.org/package=WriteXLS) Marc Schwartz
> [**XLConnect**](https://CRAN.R-project.org/package=XLConnect) Mirai Solutions GmbH
> [**XML**](https://CRAN.R-project.org/package=XML) Duncan Temple Lang
>
> ---

Brian Ripley is the author of the support for connections.

---
