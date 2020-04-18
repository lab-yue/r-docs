5 Binary files

---

---

• [Binary data formats](#Binary-data-formats)     
 • [dBase files (DBF)](#dBase-files-_0028DBF_0029)

---

Binary connections ([Connections](#Connections)) are now the preferred
way to handle binary files.

---

### 5.1 Binary data formats

Packages [**h5**](https://CRAN.R-project.org/package=h5), Bioconductor's
**rhdf5**, [**RNetCDF**](https://CRAN.R-project.org/package=RNetCDF) and
[**ncdf4**](https://CRAN.R-project.org/package=ncdf4) on CRAN provide
interfaces to NASA's HDF5 (Hierarchical Data Format, see
<https://www.hdfgroup.org/HDF5/>) and to UCAR's netCDF data files
(network Common Data Form, see
<http://www.unidata.ucar.edu/software/netcdf/>).

Both of these are systems to store scientific data in array-oriented
ways, including descriptions, labels, formats, units, .... HDF5 also
allows _groups_ of arrays, and the R interface maps lists to HDF5
groups, and can write numeric and character vectors and matrices.

NetCDF's version 4 format (confusingly, implemented in netCDF 4.1.1 and
later, but not in 4.0.1) includes the use of various HDF5 formats. This
is handled by package
[**ncdf4**](https://CRAN.R-project.org/package=ncdf4) whereas
[**RNetCDF**](https://CRAN.R-project.org/package=RNetCDF) handles
version 3 files.

The availability of software to support these formats is somewhat
limited by platform, especially on Windows.

---

### 5.2 dBase files (DBF)

`dBase` was a DOS program written by Ashton-Tate and later owned by
Borland which has a binary flat-file format that became popular, with
file extension `.dbf`. It has been adopted for the 'Xbase'
family of databases, covering dBase, Clipper, FoxPro and their Windows
equivalents Visual dBase, Visual Objects and Visual FoxPro (see
<http://www.e-bachmann.dk/docs/xbase.htm>). A dBase file contains a
header and then a series of fields and so is most similar to an R data
frame. The data itself is stored in text format, and can include
character, logical and numeric fields, and other types in later versions
(see for example
<http://www.digitalpreservation.gov/formats/fdd/fdd000325.shtml> and
<http://www.clicketyclick.dk/databases/xbase/format/index.html>).

Functions `read.dbf` and `write.dbf` provide ways to read and write
basic DBF files on all R platforms. For Windows users `odbcConnectDbase`
in package [**RODBC**](https://CRAN.R-project.org/package=RODBC)
provides more comprehensive facilities to read DBF files _via_
Microsoft's dBase ODBC driver (and the Visual FoxPro driver can also be
used via `odbcDriverConnect`).

---
