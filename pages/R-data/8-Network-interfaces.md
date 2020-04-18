8 Network interfaces

---

---

• [Reading from sockets](#Reading-from-sockets)     
 • [Using download.file](#Using-download_002efile)

---

Some limited facilities are available to exchange data at a lower level
across network connections.

---

### 8.1 Reading from sockets

Base R comes with some facilities to communicate _via_ BSD sockets on
systems that support them (including the common Linux, Unix and Windows
ports of R). One potential problem with using sockets is that these
facilities are often blocked for security reasons or to force the use of
Web caches, so these functions may be more useful on an intranet than
externally. For new projects it is suggested that socket connections are
used instead.

The earlier low-level interface is given by functions `make.socket`,
`read.socket`, `write.socket` and `close.socket`.

---

### 8.2 Using `download.file`

Function `download.file` is provided to read a file from a Web resource
via FTP or HTTP (including HTTPS) and write it to a file. Often this can
be avoided, as functions such as `read.table` and `scan` can read
directly from a URL, either by explicitly using `url` to open a
connection, or implicitly using it by giving a URL as the `file`
argument.

---
