9 Reading Excel spreadsheets

---

The most common R data import/export question seems to be 'how do I read
an Excel spreadsheet'. This chapter collects together advice and options
given earlier. Note that most of the advice is for pre-Excel 2007
spreadsheets and not the later `.xlsx` format.

The first piece of advice is to avoid doing so if possible! If you have
access to Excel, export the data you want from Excel in tab-delimited or
comma-separated form, and use `read.delim` or `read.csv` to import it
into R. (You may need to use `read.delim2` or `read.csv2` in a locale
that uses comma as the decimal point.) Exporting a DIF file and reading
it using `read.DIF` is another possibility.

If you do not have Excel, many other programs are able to read such
spreadsheets and export in a text format on both Windows and Unix, for
example Gnumeric (<http://www.gnome.org/projects/gnumeric/>) and
OpenOffice (<https://www.openoffice.org>). You can also cut-and-paste
between the display of a spreadsheet in such a program and R:
`read.table` will read from the R console or, under Windows, from the
clipboard (via `file = "clipboard"` or `readClipboard`). The `read.DIF`
function can also read from the clipboard.

Note that an Excel `.xls` file is not just a spreadsheet: such
files can contain many sheets, and the sheets can contain formulae,
macros and so on. Not all readers can read other than the first sheet,
and may be confused by other contents of the file.

Windows users (of 32-bit R) can use `odbcConnectExcel` in package
[**RODBC**](https://CRAN.R-project.org/package=RODBC). This can select
rows and columns from any of the sheets in an Excel spreadsheet file (at
least from Excel 97--2003, depending on your ODBC drivers: by calling
`odbcConnect` directly versions back to Excel 3.0 can be read). The
version `odbcConnectExcel2007` will read the Excel 2007 formats as well
as earlier ones (provided the drivers are installed, including with
64-bit Windows R: see [RODBC](#RODBC)). macOS users can also use
[**RODBC**](https://CRAN.R-project.org/package=RODBC) if they have a
suitable driver (e.g. that from Actual Technologies).

`Perl` users have contributed a module `OLE::SpreadSheet::ParseExcel`
and a program `xls2csv.pl` to convert Excel 95--2003 spreadsheets to CSV
files. Package [**gdata**](https://CRAN.R-project.org/package=gdata)
provides a basic wrapper in its `read.xls` function. With suitable
`Perl` modules installed this function can also read Excel 2007
spreadsheets.

Packages
[**dataframes2xls**](https://CRAN.R-project.org/package=dataframes2xls)
and [**WriteXLS**](https://CRAN.R-project.org/package=WriteXLS) each
contain a function to _write_ one or more data frames to an
`.xls` file, using Python and Perl respectively.

Packages [**xlsx**](https://CRAN.R-project.org/package=xlsx) can read
and and manipulate Excel 2007 and later spreadsheets: it requires Java.

Package [**XLConnect**](https://CRAN.R-project.org/package=XLConnect)
can read, write and manipulate both Excel 97--2003 and Excel 2007/10
spreadsheets, using Java.

Package [**readxl**](https://CRAN.R-project.org/package=readxl) can read
both Excel 97--2003 and Excel 2007/10 spreadsheets, using an included C
library.

---

## Appendix A References

R. A. Becker, J. M. Chambers and A. R. Wilks (1988) _The New S Language.
A Programming Environment for Data Analysis and Graphics._ Wadsworth &
Brooks/Cole.

J. Bowman, S. Emberson and M. Darnovsky (1996) _The Practical SQL
Handbook. Using Structured Query Language._ Addison-Wesley.

J. M. Chambers (1998) _Programming with Data. A Guide to the S
Language._ Springer-Verlag.

P. Dubois (2000) _MySQL._ New Riders.

M. Henning and S. Vinoski (1999) _Advanced CORBA Programming with C++._
Addison-Wesley.

K. Kline and D. Kline (2001) _SQL in a Nutshell._ O'Reilly.

B. Momjian (2000) _PostgreSQL: Introduction and Concepts._
Addison-Wesley. Also available at
<http://momjian.us/main/writings/pgsql/aw_pgsql_book/>.

B. D. Ripley (2001) Connections. _R News_, **1/1**, 16--7.
<https://www.r-project.org/doc/Rnews/Rnews_2001-1.pdf>

T. M. Therneau and P. M. Grambsch (2000) _Modeling Survival Data.
Extending the Cox Model._ Springer-Verlag.

E. J. Yarger, G. Reese and T. King (1999) _MySQL & mSQL_. O'Reilly.

---

## Function and variable index

---

Jump to:   [**.**](#Function-and-variable-index_vr_symbol-1){.summary-letter}
 \
 [**B**](#Function-and-variable-index_vr_letter-B){.summary-letter}  
[**C**](#Function-and-variable-index_vr_letter-C){.summary-letter}  
[**D**](#Function-and-variable-index_vr_letter-D){.summary-letter}  
[**F**](#Function-and-variable-index_vr_letter-F){.summary-letter}  
[**G**](#Function-and-variable-index_vr_letter-G){.summary-letter}  
[**H**](#Function-and-variable-index_vr_letter-H){.summary-letter}  
[**I**](#Function-and-variable-index_vr_letter-I){.summary-letter}  
[**M**](#Function-and-variable-index_vr_letter-M){.summary-letter}  
[**N**](#Function-and-variable-index_vr_letter-N){.summary-letter}  
[**O**](#Function-and-variable-index_vr_letter-O){.summary-letter}  
[**P**](#Function-and-variable-index_vr_letter-P){.summary-letter}  
[**R**](#Function-and-variable-index_vr_letter-R){.summary-letter}  
[**S**](#Function-and-variable-index_vr_letter-S){.summary-letter}  
[**T**](#Function-and-variable-index_vr_letter-T){.summary-letter}  
[**U**](#Function-and-variable-index_vr_letter-U){.summary-letter}  
[**W**](#Function-and-variable-index_vr_letter-W){.summary-letter}  
[**X**](#Function-and-variable-index_vr_letter-X){.summary-letter}

---

Index Entry

Section

---

.

[`.dbf`](#index-_002edbf):

[RODBC](#RODBC)

[`.xls`](#index-_002exls):

[RODBC](#RODBC)

[`.xls`](#index-_002exls-1):

[Reading Excel spreadsheets](#Reading-Excel-spreadsheets)

[`.xlsx`](#index-_002exlsx):

[Reading Excel spreadsheets](#Reading-Excel-spreadsheets)

---

B

[`bzfile`](#index-bzfile):

[Types of connections](#Types-of-connections)

---

C

[`cat`](#index-cat):

[Export to text files](#Export-to-text-files)

[`cat`](#index-cat-1):

[Output to connections](#Output-to-connections)

[`close`](#index-close):

[RODBC](#RODBC)

[`close`](#index-close-1):

[Types of connections](#Types-of-connections)

[`close.socket`](#index-close_002esocket):

[Reading from sockets](#Reading-from-sockets)

[`count.fields`](#index-count_002efields):

[Variations on read.table](#Variations-on-read_002etable)

---

D

[`data.restore`](#index-data_002erestore):

[EpiInfo Minitab SAS S-PLUS SPSS Stata Systat](#EpiInfo-Minitab-SAS-S_002dPLUS-SPSS-Stata-Systat)

[`dataframes2xls`](#index-dataframes2xls):

[Reading Excel spreadsheets](#Reading-Excel-spreadsheets)

[`dbClearResult`](#index-dbClearResult):

[DBI](#DBI)

[`dbConnect`](#index-dbConnect):

[DBI](#DBI)

[`dbDisconnect`](#index-dbDisconnect):

[DBI](#DBI)

[`dbDriver`](#index-dbDriver):

[DBI](#DBI)

[`dbExistsTable`](#index-dbExistsTable):

[DBI](#DBI)

[`dbGetQuery`](#index-dbGetQuery):

[DBI](#DBI)

[`dbReadTable`](#index-dbReadTable):

[DBI](#DBI)

[`dbRemoveTable`](#index-dbRemoveTable):

[DBI](#DBI)

[`dbSendQuery`](#index-dbSendQuery):

[DBI](#DBI)

[`dbWriteTable`](#index-dbWriteTable):

[DBI](#DBI)

---

F

[`fetch`](#index-fetch):

[DBI](#DBI)

[`file`](#index-file):

[Types of connections](#Types-of-connections)

[`format`](#index-format):

[Export to text files](#Export-to-text-files)

[`ftable`](#index-ftable):

[Flat contingency tables](#Flat-contingency-tables)

---

G

[`gzfile`](#index-gzfile):

[Types of connections](#Types-of-connections)

---

H

[`hdf5`](#index-hdf5):

[Binary data formats](#Binary-data-formats)

---

I

[`isSeekable`](#index-isSeekable):

[Listing and manipulating connections](#Listing-and-manipulating-connections)

---

M

[`make.socket`](#index-make_002esocket):

[Reading from sockets](#Reading-from-sockets)

---

N

[`netCDF`](#index-netCDF):

[Binary data formats](#Binary-data-formats)

---

O

[`odbcClose`](#index-odbcClose):

[RODBC](#RODBC)

[`odbcConnect`](#index-odbcConnect):

[RODBC](#RODBC)

[`odbcConnectDbase`](#index-odbcConnectDbase):

[dBase files (DBF)](#dBase-files-_0028DBF_0029)

[`odbcConnectExcel`](#index-odbcConnectExcel):

[RODBC](#RODBC)

[`odbcConnectExcel`](#index-odbcConnectExcel-1):

[Reading Excel spreadsheets](#Reading-Excel-spreadsheets)

[`odbcConnectExcel2007`](#index-odbcConnectExcel2007):

[Reading Excel spreadsheets](#Reading-Excel-spreadsheets)

[`odbcDriverConnect`](#index-odbcDriverConnect):

[RODBC](#RODBC)

[`odbcGetInfo`](#index-odbcGetInfo):

[RODBC](#RODBC)

[`odbcQuery`](#index-odbcQuery):

[RODBC](#RODBC)

[`open`](#index-open):

[Types of connections](#Types-of-connections)

---

P

[`pipe`](#index-pipe):

[Types of connections](#Types-of-connections)

[`pushBack.`](#index-pushBack_002e):

[Pushback](#Pushback)

[`pushBackLength`](#index-pushBackLength):

[Pushback](#Pushback)

---

R

[`read.csv`](#index-read_002ecsv):

[Variations on read.table](#Variations-on-read_002etable)

[`read.csv`](#index-read_002ecsv-1):

[Reading Excel spreadsheets](#Reading-Excel-spreadsheets)

[`read.csv2`](#index-read_002ecsv2):

[Variations on read.table](#Variations-on-read_002etable)

[`read.dbf`](#index-read_002edbf):

[dBase files (DBF)](#dBase-files-_0028DBF_0029)

[`read.delim`](#index-read_002edelim):

[Variations on read.table](#Variations-on-read_002etable)

[`read.delim`](#index-read_002edelim-1):

[Reading Excel spreadsheets](#Reading-Excel-spreadsheets)

[`read.delim2`](#index-read_002edelim2):

[Variations on read.table](#Variations-on-read_002etable)

[`read.DIF`](#index-read_002eDIF):

[Data Interchange Format (DIF)](#Data-Interchange-Format-_0028DIF_0029)

[`read.DIF`](#index-read_002eDIF-1):

[Reading Excel spreadsheets](#Reading-Excel-spreadsheets)

[`read.dta`](#index-read_002edta):

[EpiInfo Minitab SAS S-PLUS SPSS Stata Systat](#EpiInfo-Minitab-SAS-S_002dPLUS-SPSS-Stata-Systat)

[`read.epiinfo`](#index-read_002eepiinfo):

[EpiInfo Minitab SAS S-PLUS SPSS Stata Systat](#EpiInfo-Minitab-SAS-S_002dPLUS-SPSS-Stata-Systat)

[`read.fortran`](#index-read_002efortran):

[Fixed-width-format files](#Fixed_002dwidth_002dformat-files)

[`read.ftable`](#index-read_002eftable):

[Flat contingency tables](#Flat-contingency-tables)

[`read.fwf`](#index-read_002efwf):

[Fixed-width-format files](#Fixed_002dwidth_002dformat-files)

[`read.mtp`](#index-read_002emtp):

[EpiInfo Minitab SAS S-PLUS SPSS Stata Systat](#EpiInfo-Minitab-SAS-S_002dPLUS-SPSS-Stata-Systat)

[`read.octave`](#index-read_002eoctave):

[Octave](#Octave)

[`read.S`](#index-read_002eS):

[EpiInfo Minitab SAS S-PLUS SPSS Stata Systat](#EpiInfo-Minitab-SAS-S_002dPLUS-SPSS-Stata-Systat)

[`read.socket`](#index-read_002esocket):

[Reading from sockets](#Reading-from-sockets)

[`read.spss`](#index-read_002espss):

[EpiInfo Minitab SAS S-PLUS SPSS Stata Systat](#EpiInfo-Minitab-SAS-S_002dPLUS-SPSS-Stata-Systat)

[`read.systat`](#index-read_002esystat):

[EpiInfo Minitab SAS S-PLUS SPSS Stata Systat](#EpiInfo-Minitab-SAS-S_002dPLUS-SPSS-Stata-Systat)

[`read.table`](#index-read_002etable):

[Variations on read.table](#Variations-on-read_002etable)

[`read.table`](#index-read_002etable-1):

[Input from connections](#Input-from-connections)

[`read.table`](#index-read_002etable-2):

[Reading Excel spreadsheets](#Reading-Excel-spreadsheets)

[`read.xls`](#index-read_002exls):

[Reading Excel spreadsheets](#Reading-Excel-spreadsheets)

[`read.xport`](#index-read_002export):

[EpiInfo Minitab SAS S-PLUS SPSS Stata Systat](#EpiInfo-Minitab-SAS-S_002dPLUS-SPSS-Stata-Systat)

[`readBin`](#index-readBin):

[Binary connections](#Binary-connections)

[`readChar`](#index-readChar):

[Binary connections](#Binary-connections)

[`readClipboard`](#index-readClipboard):

[Reading Excel spreadsheets](#Reading-Excel-spreadsheets)

[`readLines`](#index-readLines):

[Using scan directly](#Using-scan-directly)

[`readLines`](#index-readLines-1):

[Input from connections](#Input-from-connections)

[`readxl`](#index-readxl):

[Reading Excel spreadsheets](#Reading-Excel-spreadsheets)

[`reshape`](#index-reshape):

[Re-shaping data](#Re_002dshaping-data)

---

S

[`scan`](#index-scan):

[Imports](#Imports)

[`scan`](#index-scan-1):

[Using scan directly](#Using-scan-directly)

[`scan`](#index-scan-2):

[Input from connections](#Input-from-connections)

[`seek`](#index-seek):

[Listing and manipulating connections](#Listing-and-manipulating-connections)

[`showConnections`](#index-showConnections):

[Listing and manipulating connections](#Listing-and-manipulating-connections)

[`sink`](#index-sink):

[Export to text files](#Export-to-text-files)

[`sink`](#index-sink-1):

[Output to connections](#Output-to-connections)

[`socketConnection`](#index-socketConnection):

[Types of connections](#Types-of-connections)

[`sqlCopy`](#index-sqlCopy):

[RODBC](#RODBC)

[`sqlFetch`](#index-sqlFetch):

[RODBC](#RODBC)

[`sqlFetchMore`](#index-sqlFetchMore):

[RODBC](#RODBC)

[`sqlGetResults`](#index-sqlGetResults):

[RODBC](#RODBC)

[`sqlQuery`](#index-sqlQuery):

[RODBC](#RODBC)

[`sqlSave`](#index-sqlSave):

[RODBC](#RODBC)

[`sqlTables`](#index-sqlTables):

[RODBC](#RODBC)

[`stack`](#index-stack):

[Re-shaping data](#Re_002dshaping-data)

[`stderr`](#index-stderr):

[Types of connections](#Types-of-connections)

[`stdin`](#index-stdin):

[Types of connections](#Types-of-connections)

[`stdout`](#index-stdout):

[Types of connections](#Types-of-connections)

[`Sys.localeconv`](#index-Sys_002elocaleconv):

[Variations on read.table](#Variations-on-read_002etable)

---

T

[`textConnection`](#index-textConnection):

[Types of connections](#Types-of-connections)

[`truncate`](#index-truncate):

[Listing and manipulating connections](#Listing-and-manipulating-connections)

---

U

[`unstack.`](#index-unstack_002e):

[Re-shaping data](#Re_002dshaping-data)

[`url`](#index-url):

[Types of connections](#Types-of-connections)

---

W

[`write`](#index-write):

[Export to text files](#Export-to-text-files)

[`write`](#index-write-1):

[Output to connections](#Output-to-connections)

[`write.csv`](#index-write_002ecsv):

[Export to text files](#Export-to-text-files)

[`write.csv2`](#index-write_002ecsv2):

[Export to text files](#Export-to-text-files)

[`write.dbf`](#index-write_002edbf):

[dBase files (DBF)](#dBase-files-_0028DBF_0029)

[`write.dta`](#index-write_002edta):

[EpiInfo Minitab SAS S-PLUS SPSS Stata Systat](#EpiInfo-Minitab-SAS-S_002dPLUS-SPSS-Stata-Systat)

[`write.foreign`](#index-write_002eforeign):

[Export to text files](#Export-to-text-files)

[`write.matrix`](#index-write_002ematrix):

[Export to text files](#Export-to-text-files)

[`write.socket`](#index-write_002esocket):

[Reading from sockets](#Reading-from-sockets)

[`write.table`](#index-write_002etable):

[Export to text files](#Export-to-text-files)

[`write.table`](#index-write_002etable-1):

[Output to connections](#Output-to-connections)

[`writeBin`](#index-writeBin):

[Binary connections](#Binary-connections)

[`writeChar`](#index-writeChar):

[Binary connections](#Binary-connections)

[`writeLines`](#index-writeLines):

[Output to connections](#Output-to-connections)

[`WriteXLS`](#index-WriteXLS):

[Reading Excel spreadsheets](#Reading-Excel-spreadsheets)

---

X

[`XLConnect`](#index-XLConnect):

[Reading Excel spreadsheets](#Reading-Excel-spreadsheets)

[`xlsx`](#index-xlsx):

[Reading Excel spreadsheets](#Reading-Excel-spreadsheets)

---

---

Jump to:   [**.**](#Function-and-variable-index_vr_symbol-1){.summary-letter}
 \
 [**B**](#Function-and-variable-index_vr_letter-B){.summary-letter}  
[**C**](#Function-and-variable-index_vr_letter-C){.summary-letter}  
[**D**](#Function-and-variable-index_vr_letter-D){.summary-letter}  
[**F**](#Function-and-variable-index_vr_letter-F){.summary-letter}  
[**G**](#Function-and-variable-index_vr_letter-G){.summary-letter}  
[**H**](#Function-and-variable-index_vr_letter-H){.summary-letter}  
[**I**](#Function-and-variable-index_vr_letter-I){.summary-letter}  
[**M**](#Function-and-variable-index_vr_letter-M){.summary-letter}  
[**N**](#Function-and-variable-index_vr_letter-N){.summary-letter}  
[**O**](#Function-and-variable-index_vr_letter-O){.summary-letter}  
[**P**](#Function-and-variable-index_vr_letter-P){.summary-letter}  
[**R**](#Function-and-variable-index_vr_letter-R){.summary-letter}  
[**S**](#Function-and-variable-index_vr_letter-S){.summary-letter}  
[**T**](#Function-and-variable-index_vr_letter-T){.summary-letter}  
[**U**](#Function-and-variable-index_vr_letter-U){.summary-letter}  
[**W**](#Function-and-variable-index_vr_letter-W){.summary-letter}  
[**X**](#Function-and-variable-index_vr_letter-X){.summary-letter}

---

---

## Concept index

---

Jump to:   [**A**](#Concept-index_cp_letter-A){.summary-letter}   [**B**](#Concept-index_cp_letter-B){.summary-letter}   [**C**](#Concept-index_cp_letter-C){.summary-letter}   [**D**](#Concept-index_cp_letter-D){.summary-letter}   [**E**](#Concept-index_cp_letter-E){.summary-letter}   [**F**](#Concept-index_cp_letter-F){.summary-letter}   [**H**](#Concept-index_cp_letter-H){.summary-letter}   [**I**](#Concept-index_cp_letter-I){.summary-letter}   [**L**](#Concept-index_cp_letter-L){.summary-letter}   [**M**](#Concept-index_cp_letter-M){.summary-letter}   [**N**](#Concept-index_cp_letter-N){.summary-letter}   [**O**](#Concept-index_cp_letter-O){.summary-letter}   [**P**](#Concept-index_cp_letter-P){.summary-letter}   [**Q**](#Concept-index_cp_letter-Q){.summary-letter}   [**R**](#Concept-index_cp_letter-R){.summary-letter}   [**S**](#Concept-index_cp_letter-S){.summary-letter}   [**T**](#Concept-index_cp_letter-T){.summary-letter}   [**U**](#Concept-index_cp_letter-U){.summary-letter}   [**X**](#Concept-index_cp_letter-X){.summary-letter}   [**Y**](#Concept-index_cp_letter-Y){.summary-letter}

---

Index Entry

Section

---

A

[awk](#index-awk):

[Introduction](#Introduction)

---

B

[Binary files](#index-Binary-files):

[Binary files](#Binary-files)

[Binary files](#index-Binary-files-1):

[Binary connections](#Binary-connections)

---

C

[comma separated values](#index-comma-separated-values):

[Export to text files](#Export-to-text-files)

[Compressed files](#index-Compressed-files):

[Types of connections](#Types-of-connections)

[Connections](#index-Connections):

[Connections](#Connections)

[Connections](#index-Connections-1):

[Types of connections](#Types-of-connections)

[Connections](#index-Connections-2):

[Output to connections](#Output-to-connections)

[Connections](#index-Connections-3):

[Listing and manipulating connections](#Listing-and-manipulating-connections)

[CSV files](#index-CSV-files):

[Export to text files](#Export-to-text-files)

[CSV files](#index-CSV-files-1):

[Variations on read.table](#Variations-on-read_002etable)

---

D

[Data Interchange Format
(DIF)](#index-Data-Interchange-Format-_0028DIF_0029):

[Data Interchange Format (DIF)](#Data-Interchange-Format-_0028DIF_0029)

[Dbase](#index-Dbase):

[RODBC](#RODBC)

[dBase](#index-dBase):

[dBase files (DBF)](#dBase-files-_0028DBF_0029)

[DBF files](#index-DBF-files):

[dBase files (DBF)](#dBase-files-_0028DBF_0029)

[DBMS](#index-DBMS):

[Relational databases](#Relational-databases)

---

E

[Encodings](#index-Encodings):

[Encodings](#Encodings)

[Encodings](#index-Encodings-1):

[Export to text files](#Export-to-text-files)

[EpiData](#index-EpiData):

[EpiInfo Minitab SAS S-PLUS SPSS Stata Systat](#EpiInfo-Minitab-SAS-S_002dPLUS-SPSS-Stata-Systat)

[EpiInfo](#index-EpiInfo):

[EpiInfo Minitab SAS S-PLUS SPSS Stata Systat](#EpiInfo-Minitab-SAS-S_002dPLUS-SPSS-Stata-Systat)

[Excel](#index-Excel):

[RODBC](#RODBC)

[Excel](#index-Excel-1):

[RODBC](#RODBC)

[Exporting to a text file](#index-Exporting-to-a-text-file):

[Export to text files](#Export-to-text-files)

---

F

[File connections](#index-File-connections):

[Types of connections](#Types-of-connections)

[Fixed-width-format files](#index-Fixed_002dwidth_002dformat-files):

[Fixed-width-format files](#Fixed_002dwidth_002dformat-files)

[Flat contingency tables](#index-Flat-contingency-tables):

[Flat contingency tables](#Flat-contingency-tables)

---

H

[Hierarchical Data Format](#index-Hierarchical-Data-Format):

[Binary data formats](#Binary-data-formats)

---

I

[Importing from other statistical systems](#index-Importing-from-other-statistical-systems):

[Importing from other statistical systems](#Importing-from-other-statistical-systems)

---

L

[locales](#index-locales):

[Variations on read.table](#Variations-on-read_002etable)

---

M

[Minitab](#index-Minitab):

[EpiInfo Minitab SAS S-PLUS SPSS Stata Systat](#EpiInfo-Minitab-SAS-S_002dPLUS-SPSS-Stata-Systat)

[Missing values](#index-Missing-values):

[Export to text files](#Export-to-text-files)

[Missing values](#index-Missing-values-1):

[Variations on read.table](#Variations-on-read_002etable)

[MySQL database system](#index-MySQL-database-system):

[DBI](#DBI)

[MySQL database system](#index-MySQL-database-system-1):

[RODBC](#RODBC)

---

N

[network Common Data Form](#index-network-Common-Data-Form):

[Binary data formats](#Binary-data-formats)

---

O

[Octave](#index-Octave):

[Octave](#Octave)

[ODBC](#index-ODBC):

[Overview of RDBMSs](#Overview-of-RDBMSs)

[ODBC](#index-ODBC-1):

[RODBC](#RODBC)

[Open Database Connectivity](#index-Open-Database-Connectivity):

[Overview of RDBMSs](#Overview-of-RDBMSs)

[Open Database Connectivity](#index-Open-Database-Connectivity-1):

[RODBC](#RODBC)

---

P

[perl](#index-perl):

[Introduction](#Introduction)

[perl](#index-perl-1):

[Fixed-width-format files](#Fixed_002dwidth_002dformat-files)

[Pipe connections](#index-Pipe-connections):

[Types of connections](#Types-of-connections)

[PostgreSQL database system](#index-PostgreSQL-database-system):

[RODBC](#RODBC)

[Pushback on a connection](#index-Pushback-on-a-connection):

[Pushback](#Pushback)

---

Q

[Quoting strings](#index-Quoting-strings):

[Export to text files](#Export-to-text-files)

[Quoting strings](#index-Quoting-strings-1):

[Variations on read.table](#Variations-on-read_002etable)

---

R

[Re-shaping data](#index-Re_002dshaping-data):

[Re-shaping data](#Re_002dshaping-data)

[Relational databases](#index-Relational-databases):

[Relational databases](#Relational-databases)

---

S

[S-PLUS](#index-S_002dPLUS):

[EpiInfo Minitab SAS S-PLUS SPSS Stata Systat](#EpiInfo-Minitab-SAS-S_002dPLUS-SPSS-Stata-Systat)

[SAS](#index-SAS):

[EpiInfo Minitab SAS S-PLUS SPSS Stata Systat](#EpiInfo-Minitab-SAS-S_002dPLUS-SPSS-Stata-Systat)

[Sockets](#index-Sockets):

[Types of connections](#Types-of-connections)

[Sockets](#index-Sockets-1):

[Reading from sockets](#Reading-from-sockets)

[Spreadsheet-like data](#index-Spreadsheet_002dlike-data):

[Spreadsheet-like data](#Spreadsheet_002dlike-data)

[SPSS](#index-SPSS):

[EpiInfo Minitab SAS S-PLUS SPSS Stata Systat](#EpiInfo-Minitab-SAS-S_002dPLUS-SPSS-Stata-Systat)

[SPSS Data Entry](#index-SPSS-Data-Entry):

[EpiInfo Minitab SAS S-PLUS SPSS Stata Systat](#EpiInfo-Minitab-SAS-S_002dPLUS-SPSS-Stata-Systat)

[SQL queries](#index-SQL-queries):

[SQL queries](#SQL-queries)

[Stata](#index-Stata):

[EpiInfo Minitab SAS S-PLUS SPSS Stata Systat](#EpiInfo-Minitab-SAS-S_002dPLUS-SPSS-Stata-Systat)

[Systat](#index-Systat):

[EpiInfo Minitab SAS S-PLUS SPSS Stata Systat](#EpiInfo-Minitab-SAS-S_002dPLUS-SPSS-Stata-Systat)

---

T

[Terminal connections](#index-Terminal-connections):

[Types of connections](#Types-of-connections)

[Text connections](#index-Text-connections):

[Types of connections](#Types-of-connections)

---

U

[Unix tools](#index-Unix-tools):

[Introduction](#Introduction)

[URL connections](#index-URL-connections):

[Types of connections](#Types-of-connections)

[URL connections](#index-URL-connections-1):

[Input from connections](#Input-from-connections)

---

X

[XML](#index-XML):

[XML](#XML)

---

Y

[yaml](#index-yaml):

[XML](#XML)

---

---

Jump to:   [**A**](#Concept-index_cp_letter-A){.summary-letter}   [**B**](#Concept-index_cp_letter-B){.summary-letter}   [**C**](#Concept-index_cp_letter-C){.summary-letter}   [**D**](#Concept-index_cp_letter-D){.summary-letter}   [**E**](#Concept-index_cp_letter-E){.summary-letter}   [**F**](#Concept-index_cp_letter-F){.summary-letter}   [**H**](#Concept-index_cp_letter-H){.summary-letter}   [**I**](#Concept-index_cp_letter-I){.summary-letter}   [**L**](#Concept-index_cp_letter-L){.summary-letter}   [**M**](#Concept-index_cp_letter-M){.summary-letter}   [**N**](#Concept-index_cp_letter-N){.summary-letter}   [**O**](#Concept-index_cp_letter-O){.summary-letter}   [**P**](#Concept-index_cp_letter-P){.summary-letter}   [**Q**](#Concept-index_cp_letter-Q){.summary-letter}   [**R**](#Concept-index_cp_letter-R){.summary-letter}   [**S**](#Concept-index_cp_letter-S){.summary-letter}   [**T**](#Concept-index_cp_letter-T){.summary-letter}   [**U**](#Concept-index_cp_letter-U){.summary-letter}   [**X**](#Concept-index_cp_letter-X){.summary-letter}   [**Y**](#Concept-index_cp_letter-Y){.summary-letter}

---

---

#### Footnotes

[(1)](#DOCF1)

the distinction is subtle, <https://en.wikipedia.org/wiki/UTF-16/UCS-2>,
and the use of surrogate pairs is very rare.

[(2)](#DOCF2)

Even then, Windows applications may expect a Byte Order Mark which the
implementation of `iconv` used by R may or may not add depending on the
platform.

[(3)](#DOCF3)

This is normally fast as looking at the first entry rules out most of
the possibilities.

[(4)](#DOCF4)

and forks, notably MariaDB.

---
