# 4 Relational databases

---

---

• [Why use a database?](#Why-use-a-database_003f)     
 • [Overview of RDBMSs](#Overview-of-RDBMSs)     
 • [R interface packages](#R-interface-packages)

---

---

### 4.1 Why use a database?

There are limitations on the types of data that R handles well. Since
all data being manipulated by R are resident in memory, and several
copies of the data can be created during execution of a function, R is
not well suited to extremely large data sets. Data objects that are more
than a (few) hundred megabytes in size can cause R to run out of memory,
particularly on a 32-bit operating system.

R does not easily support concurrent access to data. That is, if more
than one user is accessing, and perhaps updating, the same data, the
changes made by one user will not be visible to the others.

R does support persistence of data, in that you can save a data object
or an entire worksheet from one session and restore it at the subsequent
session, but the format of the stored data is specific to R and not
easily manipulated by other systems.

Database management systems (DBMSs) and, in particular, relational DBMSs
(RDBMSs) _are_ designed to do all of these things well. Their strengths
are

1.  To provide fast access to selected parts of large databases.
2.  Powerful ways to summarize and cross-tabulate columns in databases.
3.  Store data in more organized ways than the rectangular grid model of
    spreadsheets and R data frames.
4.  Concurrent access from multiple clients running on multiple hosts
    while enforcing security constraints on access to the data.
5.  Ability to act as a server to a wide range of clients.

The sort of statistical applications for which DBMS might be used are to
extract a 10% sample of the data, to cross-tabulate data to produce a
multi-dimensional contingency table, and to extract data group by group
from a database for separate analysis.

Increasingly OSes are themselves making use of DBMSs for these reasons,
so it is nowadays likely that one will be already installed on your
(non-Windows) OS. [Akonadi](https://en.wikipedia.org/wiki/Akonadi) is
used by KDE4 to store personal information. Several macOS applications,
including Mail and Address Book, use SQLite.

---

### 4.2 Overview of RDBMSs

Traditionally there had been large (and expensive) commercial RDBMSs
([Informix](http://www.informix.com); [Oracle](https://www.oracle.com);
[Sybase](http://www.sybase.com); [IBM's DB2](http://www.ibm.com/db2);
[Microsoft SQL Server](https://www.microsoft.com/SQL/default.mspx) on
Windows) and academic and small-system databases (such as
MySQL[^4^](#FOOT4), PostgreSQL, Microsoft Access, ...), the
former marked out by much greater emphasis on data security features.
The line is blurring, with MySQL and PostgreSQL having more and more
high-end features, and free 'express' versions being made available for
the commercial DBMSs.

There are other commonly used data sources, including spreadsheets,
non-relational databases and even text files (possibly compressed). Open
Database Connectivity (ODBC) is a standard to use all of these data
sources. It originated on Windows (see
<https://msdn.microsoft.com/en-us/library/ms710252%28v=vs.85%29.aspx>)
but is also implemented on Linux/Unix/macOS.

All of the packages described later in this chapter provide clients to
client/server databases. The database can reside on the same machine or
(more often) remotely. There is an ISO standard (in fact several: SQL92
is ISO/IEC 9075, also known as ANSI X3.135-1992, and SQL99 is coming
into use) for an interface language called SQL (Structured Query
Language, sometimes pronounced 'sequel': see Bowman _et al._ 1996 and
Kline and Kline 2001) which these DBMSs support to varying degrees.

---

• [SQL queries](#SQL-queries)     
 • [Data types](#Data-types)

---

---

#### 4.2.1 SQL queries

The more comprehensive R interfaces generate SQL behind the scenes for
common operations, but direct use of SQL is needed for complex
operations in all. Conventionally SQL is written in upper case, but many
users will find it more convenient to use lower case in the R interface
functions.

A relational DBMS stores data as a database of _tables_ (or _relations_)
which are rather similar to R data frames, in that they are made up of
_columns_ or _fields_ of one type (numeric, character, date, currency,
...) and _rows_ or _records_ containing the observations for one entity.

SQL 'queries' are quite general operations on a relational database. The
classical query is a SELECT statement of the type

```r
SELECT State, Murder FROM USArrests WHERE Rape > 30 ORDER BY Murder

SELECT t.sch, c.meanses, t.sex, t.achieve
  FROM student as t, school as c WHERE t.sch = c.id

SELECT sex, COUNT(*) FROM student GROUP BY sex

SELECT sch, AVG(sestat) FROM student GROUP BY sch LIMIT 10
```

The first of these selects two columns from the R data frame `USArrests`
that has been copied across to a database table, subsets on a third
column and asks the results be sorted. The second performs a database
_join_ on two tables `student` and `school` and returns four columns.
The third and fourth queries do some cross-tabulation and return counts
or averages. (The five aggregation functions are COUNT(\*) and SUM, MAX,
MIN and AVG, each applied to a single column.)

SELECT queries use FROM to select the table, WHERE to specify a
condition for inclusion (or more than one condition separated by AND or
OR), and ORDER BY to sort the result. Unlike data frames, rows in RDBMS
tables are best thought of as unordered, and without an ORDER BY
statement the ordering is indeterminate. You can sort (in
lexicographical order) on more than one column by separating them by
commas. Placing DESC after an ORDER BY puts the sort in descending
order.

SELECT DISTINCT queries will only return one copy of each distinct row
in the selected table.

The GROUP BY clause selects subgroups of the rows according to the
criterion. If more than one column is specified (separated by commas)
then multi-way cross-classifications can be summarized by one of the
five aggregation functions. A HAVING clause allows the select to include
or exclude groups depending on the aggregated value.

If the SELECT statement contains an ORDER BY statement that produces a
unique ordering, a LIMIT clause can be added to select (by number) a
contiguous block of output rows. This can be useful to retrieve rows a
block at a time. (It may not be reliable unless the ordering is unique,
as the LIMIT clause can be used to optimize the query.)

There are queries to create a table (CREATE TABLE, but usually one
copies a data frame to the database in these interfaces), INSERT or
DELETE or UPDATE data. A table is destroyed by a DROP TABLE 'query'.

Kline and Kline (2001) discuss the details of the implementation of SQL
in Microsoft SQL Server 2000, Oracle, MySQL and PostgreSQL.

---

#### 4.2.2 Data types

Data can be stored in a database in various data types. The range of
data types is DBMS-specific, but the SQL standard defines many types,
including the following that are widely implemented (often not by the
SQL name).

`float(p)`

: Real number, with optional precision. Often called `real` or
`double` or `double precision`.

`integer`

: 32-bit integer. Often called `int`.

`smallint`

: 16-bit integer

`character(n)`

: fixed-length character string. Often called `char`.

`character varying(n)`

: variable-length character string. Often called `varchar`. Almost
always has a limit of 255 chars.

`boolean`

: true or false. Sometimes called `bool` or `bit`.

`date`

: calendar date

`time`

: time of day

`timestamp`

: date and time

There are variants on `time` and `timestamp`, `with timezone`. Other
types widely implemented are `text` and `blob`, for large blocks of text
and binary data, respectively.

The more comprehensive of the R interface packages hide the type
conversion issues from the user.

---

### 4.3 R interface packages

There are several packages available on CRAN to help R communicate with
DBMSs. They provide different levels of abstraction. Some provide means
to copy whole data frames to and from databases. All have functions to
select data within the database via SQL queries, and to retrieve the
result as a whole as a data frame or in pieces (usually as groups of
rows).

All except [**RODBC**](https://CRAN.R-project.org/package=RODBC) are
tied to one DBMS, but there has been a proposal for a unified
'front-end' package [**DBI**](https://CRAN.R-project.org/package=DBI)
(<https://developer.r-project.org/db>) in conjunction with a 'back-end',
the most developed of which is
[**RMySQL**](https://CRAN.R-project.org/package=RMySQL). Also on CRAN
are the back-ends
[**ROracle**](https://CRAN.R-project.org/package=ROracle),
[**RPostgreSQL**](https://CRAN.R-project.org/package=RPostgreSQL) and
[**RSQLite**](https://CRAN.R-project.org/package=RSQLite) (which works
with the bundled DBMS `SQLite`, <https://www.sqlite.org>) and
[**RJDBC**](https://CRAN.R-project.org/package=RJDBC) (which uses Java
and can connect to any DBMS that has a JDBC driver).

**PL/R**
([`http://www.joeconway.com/plr/`](http://www.joeconway.com/plr/)) is a
project to embed R into PostgreSQL.

Package [**RMongo**](https://CRAN.R-project.org/package=RMongo) provides
an R interface to a Java client for 'MongoDB'
(<https://en.wikipedia.org/wiki/MongoDB>) databases, which are queried
using JavaScript rather than SQL. Package
[**mongolite**](https://CRAN.R-project.org/package=mongolite) is another
client using **mongodb**'s C driver.

---

• [DBI](#DBI)     
 • [RODBC](#RODBC)

---

---

#### 4.3.1 Packages using DBI

Package [**RMySQL**](https://CRAN.R-project.org/package=RMySQL) on CRAN
provides an interface to the MySQL database system (see
<https://www.mysql.com> and Dubois, 2000) or its fork MariaDB (see
<https://mariadb.org/>). The description here applies to versions
`0.5-0` and later: earlier versions had a substantially different
interface. The current version requires the
[**DBI**](https://CRAN.R-project.org/package=DBI) package, and this
description will apply with minor changes to all the other back-ends to
[**DBI**](https://CRAN.R-project.org/package=DBI).

MySQL exists on Unix/Linux/macOS and Windows: there is a 'Community
Edition' released under GPL but commercial licenses are also available.
MySQL was originally a 'light and lean' database. (It preserves the case
of names where the operating file system is case-sensitive, so not on
Windows.)

The call `dbDriver("MySQL")` returns a database connection manager
object, and then a call to `dbConnect` opens a database connection which
can subsequently be closed by a call to the generic function
`dbDisconnect`. Use `dbDriver("Oracle")`, `dbDriver("PostgreSQL")` or
`dbDriver("SQLite")` with those DBMSs and packages
[**ROracle**](https://CRAN.R-project.org/package=ROracle),
[**RPostgreSQL**](https://CRAN.R-project.org/package=RPostgreSQL) or
[**RSQLite**](https://CRAN.R-project.org/package=RSQLite) respectively.

SQL queries can be sent by either `dbSendQuery` or `dbGetQuery`.
`dbGetquery` sends the query and retrieves the results as a data frame.
`dbSendQuery` sends the query and returns an object of class inheriting
from `"DBIResult"` which can be used to retrieve the results, and
subsequently used in a call to `dbClearResult` to remove the result.

Function `fetch` is used to retrieve some or all of the rows in the
query result, as a list. The function `dbHasCompleted` indicates if all
the rows have been fetched, and `dbGetRowCount` returns the number of
rows in the result.

These are convenient interfaces to read/write/test/delete tables in the
database. `dbReadTable` and `dbWriteTable` copy to and from an R data
frame, mapping the row names of the data frame to the field `row_names`
in the `MySQL` table.

```r
> library(RMySQL) # will load DBI as well
## open a connection to a MySQL database
> con <- dbConnect(dbDriver("MySQL"), dbname = "test")
## list the tables in the database
> dbListTables(con)
## load a data frame into the database, deleting any existing copy
> data(USArrests)
> dbWriteTable(con, "arrests", USArrests, overwrite = TRUE)
TRUE
> dbListTables(con)
[1] "arrests"
## get the whole table
> dbReadTable(con, "arrests")
               Murder Assault UrbanPop Rape
Alabama          13.2     236       58 21.2
Alaska           10.0     263       48 44.5
Arizona           8.1     294       80 31.0
Arkansas          8.8     190       50 19.5
...
## Select from the loaded table
> dbGetQuery(con, paste("select row_names, Murder from arrests",
                        "where Rape > 30 order by Murder"))
   row_names Murder
1   Colorado    7.9
2    Arizona    8.1
3 California    9.0
4     Alaska   10.0
5 New Mexico   11.4
6   Michigan   12.1
7     Nevada   12.2
8    Florida   15.4
> dbRemoveTable(con, "arrests")
> dbDisconnect(con)
```

---

#### 4.3.2 Package RODBC

Package [**RODBC**](https://CRAN.R-project.org/package=RODBC) on CRAN
provides an interface to database sources supporting an ODBC interface.
This is very widely available, and allows the same R code to access
different database systems.
[**RODBC**](https://CRAN.R-project.org/package=RODBC) runs on
Unix/Linux, Windows and macOS, and almost all database systems provide
support for ODBC. We have tested Microsoft SQL Server, Access, MySQL,
PostgreSQL, Oracle and IBM DB2 on Windows and MySQL, MariaDB, Oracle,
PostgreSQL and SQLite on Linux.

ODBC is a client-server system, and we have happily connected to a DBMS
running on a Unix server from a Windows client, and _vice versa_.

On Windows ODBC support is part of the OS. On Unix/Linux you will need
an ODBC Driver Manager such as unixODBC (<http://www.unixODBC.org>) or
iOBDC (<http://www.iODBC.org>: this is pre-installed in macOS) and an
installed driver for your database system.

Windows provides drivers not just for DBMSs but also for Excel
(`.xls`) spreadsheets, DBase (`.dbf`) files and even
text files. (The named applications do _not_ need to be installed. Which
file formats are supported depends on the versions of the drivers.)
There are versions for Excel and Access 2007/2010 (go to
<https://www.microsoft.com/en-us/download/default.aspx>, and search for
'Office ODBC', which will lead to `AccessDatabaseEngine.exe`),
the '2007 Office System Driver' (the latter has a version for 64-bit
Windows, and that will also read earlier versions).

On macOS the Actual Technologies
(<https://www.actualtech.com/product_access.php>) drivers provide ODBC
interfaces to Access databases and to Excel spreadsheets (not including
Excel 2007/2010).

Many simultaneous connections are possible. A connection is opened by a
call to `odbcConnect` or `odbcDriverConnect` (which on the Windows GUI
allows a database to be selected via dialog boxes) which returns a
handle used for subsequent access to the database. Printing a connection
will provide some details of the ODBC connection, and calling
`odbcGetInfo` will give details on the client and server.

A connection is closed by a call to `close` or `odbcClose`, and also
(with a warning) when not R object refers to it and at the end of an R
session.

Details of the tables on a connection can be found using `sqlTables`.

Function `sqlSave` copies an R data frame to a table in the database,
and `sqlFetch` copies a table in the database to an R data frame.

An SQL query can be sent to the database by a call to `sqlQuery`. This
returns the result in an R data frame. (`sqlCopy` sends a query to the
database and saves the result as a table in the database.) A finer level
of control is attained by first calling `odbcQuery` and then
`sqlGetResults` to fetch the results. The latter can be used within a
loop to retrieve a limited number of rows at a time, as can function
`sqlFetchMore`.

Here is an example using PostgreSQL, for which the ODBC driver maps
column and data frame names to lower case. We use a database `testdb` we
created earlier, and had the DSN (data source name) set up in
`~/.odbc.ini` under `unixODBC`. Exactly the same code worked
using MyODBC to access a MySQL database under Linux or Windows (where
MySQL also maps names to lowercase). Under Windows, DSNs are set up in
the ODBC applet in the Control Panel ('Data Sources (ODBC)' in the
'Administrative Tools' section).

```r
> library(RODBC)
## tell it to map names to l/case
> channel <- odbcConnect("testdb", uid="ripley", case="tolower")
## load a data frame into the database
> data(USArrests)
> sqlSave(channel, USArrests, rownames = "state", addPK = TRUE)
> rm(USArrests)
## list the tables in the database
> sqlTables(channel)
  TABLE_QUALIFIER TABLE_OWNER TABLE_NAME TABLE_TYPE REMARKS
1                              usarrests      TABLE
## list it
> sqlFetch(channel, "USArrests", rownames = "state")
               murder assault urbanpop rape
Alabama          13.2     236       58 21.2
Alaska           10.0     263       48 44.5
    ...
## an SQL query, originally on one line
> sqlQuery(channel, "select state, murder from USArrests
           where rape > 30 order by murder")
       state murder
1 Colorado      7.9
2 Arizona       8.1
3 California    9.0
4 Alaska       10.0
5 New Mexico   11.4
6 Michigan     12.1
7 Nevada       12.2
8 Florida      15.4
## remove the table
> sqlDrop(channel, "USArrests")
## close the connection
> odbcClose(channel)
```

As a simple example of using ODBC under Windows with a Excel
spreadsheet, we can read from a spreadsheet by

```r
> library(RODBC)
> channel <- odbcConnectExcel("bdr.xls")
## list the spreadsheets
> sqlTables(channel)
  TABLE_CAT TABLE_SCHEM        TABLE_NAME   TABLE_TYPE REMARKS
1 C:\\bdr            NA           Sheet1$ SYSTEM TABLE      NA
2 C:\\bdr            NA           Sheet2$ SYSTEM TABLE      NA
3 C:\\bdr            NA           Sheet3$ SYSTEM TABLE      NA
4 C:\\bdr            NA Sheet1$Print_Area        TABLE      NA
## retrieve the contents of sheet 1, by either of
> sh1 <- sqlFetch(channel, "Sheet1")
> sh1 <- sqlQuery(channel, "select * from [Sheet1$]")
```

Notice that the specification of the table is different from the name
returned by `sqlTables`: `sqlFetch` is able to map the differences.

---
