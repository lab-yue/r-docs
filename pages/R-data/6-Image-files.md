# 6 Image files

---

A particular class of binary files are those representing images, and a
not uncommon request is to read such a file into R as a matrix.

There are many formats for image files (most with lots of variants), and
it may be necessary to use external conversion software to first convert
the image into one of the formats for which a package currently provides
an R reader. A versatile example of such software is ImageMagick and its
fork GraphicsMagick. These provide command-line programs `convert` and
`gm convert` to convert images from one format to another: what formats
they can input is determined when they are compiled, and the supported
formats can be listed by e.g. `convert -list format`.

Package [**pixmap**](https://CRAN.R-project.org/package=pixmap) has a
function `read.pnm` to read 'portable anymap' images in PBM
(black/white), PGM (grey) and PPM (RGB colour) formats. These are also
known as 'netpbm' formats.

Packages [**bmp**](https://CRAN.R-project.org/package=bmp),
[**jpeg**](https://CRAN.R-project.org/package=jpeg) and
[**png**](https://CRAN.R-project.org/package=png) read the formats after
which they are named. See also packages
[**biOps**](https://CRAN.R-project.org/package=biOps) and
[**Momocs**](https://CRAN.R-project.org/package=Momocs), and
Bioconductor package **EBImage**.

TIFF is more a meta-format, a wrapper within which a very large variety
of image formats can be embedded. Packages
[**rtiff**](https://CRAN.R-project.org/package=rtiff) and
[**tiff**](https://CRAN.R-project.org/package=tiff) can read some of the
sub-formats (depending on the external `libtiff` software against which
they are compiled). There some facilities for specialized sub-formats,
for example in Bioconductor package **beadarray**.

Raster files are common in the geographical sciences, and package
[**rgdal**](https://CRAN.R-project.org/package=rgdal) provides an
interface to GDAL which provides some facilities of its own to read
raster files and links to many others. Which formats it supports is
determined when GDAL is compiled: use `gdalDrivers()` to see what these
are for the build you are using. It can be useful for uncommon formats
such as JPEG 2000 (which is a different format from JPEG, and not
currently supported in the macOS nor Windows binary versions of
[**rgdal**](https://CRAN.R-project.org/package=rgdal)).

---
