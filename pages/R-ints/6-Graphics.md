6 Graphics

---

R's graphics internals were re-designed to enable multiple graphics
systems to be installed on top on the graphics 'engine' -- currently
there are two such systems, one supporting 'base' graphics (based on
that in S and whose R code[^15^](#FOOT15) is in package
**graphics**) and one implemented in package **grid**.

Some notes on the historical changes can be found at
<https://www.stat.auckland.ac.nz/~paul/R/basegraph.html> and
<https://www.stat.auckland.ac.nz/~paul/R/graphicsChanges.html>.

At the lowest level is a graphics device, which manages a plotting
surface (a screen window or a representation to be written to a file).
This implements a set of graphics primitives, to 'draw'

- a circle, optionally filled
- a rectangle, optionally filled
- a line
- a set of connected lines
- a polygon, optionally filled
- a paths, optionally filled using a winding rule
- text
- a raster image (optional)
- and to set a clipping rectangle

as well as requests for information such as

- the width of a string if plotted
- the metrics (width, ascent, descent) of a single character
- the current size of the plotting surface

and requests/opportunities to take action such as

- start a new 'page', possibly after responding to a request to ask
  the user for confirmation.
- return the position of the device pointer (if any).
- when a device become the current device or stops being the current
  device (this is usually used to change the window title on a screen
  device).
- when drawing starts or finishes (e.g. used to flush graphics to the
  screen when drawing stops).
- wait for an event, for example a mouse click or keypress.
- an 'onexit' action, to clean up if plotting is interrupted (by an
  error or by the user).
- capture the current contents of the device as a raster image.
- close the device.

The device also sets a number of variables, mainly Boolean flags
indicating its capabilities. Devices work entirely in 'device units'
which are up to its developer: they can be in pixels, big points (1/72
inch), twips, ..., and can differ[^16^](#FOOT16) in the
'`x`' and '`y`' directions.

The next layer up is the graphics 'engine' that is the main interface to
the device (although the graphics subsystems do talk directly to
devices). This is responsible for clipping lines, rectangles and
polygons, converting the `pch` values `0...26` to sets of lines/circles,
centring (and otherwise adjusting) text, rendering mathematical
expressions ('plotmath') and mapping colour descriptions such as names
to the internal representation.

Another function of the engine is to manage display lists and snapshots.
Some but not all instances of graphics devices maintain display lists, a
'list' of operations that have been performed on the device to produce
the current plot (since the device was opened or the plot was last
cleared, e.g. by `plot.new`). Screen devices generally maintain a
display list to handle repaint and resize events whereas file-based
formats do not---display lists are also used to implement `dev.copy()`
and friends. The display list is a pairlist of `.Internal` (base
graphics) or `.Call.graphics` (grid graphics) calls, which means that
the C code implementing a graphics operation will be re-called when the
display list is replayed: apart from the part which records the
operation if successful.

Snapshots of the current graphics state are taken by `GEcreateSnapshot`
and replayed later in the session by `GEplaySnapshot`. These are used by
`recordPlot()`, `replayPlot()` and the GUI menus of the `windows()`
device. The 'state' includes the display list.

The top layer comprises the graphics subsystems. Although there is
provision for 24 subsystems since about 2001, currently still only two
exist, 'base' and 'grid'. The base subsystem is registered with the
engine when R is initialized, and unregistered (via `KillAllDevices`)
when an R session is shut down. The grid subsystem is registered in its
`.onLoad` function and unregistered in the `.onUnload` function. The
graphics subsystem may also have 'state' information saved in a snapshot
(currently base does and grid does not).

Package **grDevices** was originally created to contain the basic
graphics devices (although `X11` is in a separate load-on-demand module
because of the volume of external libraries it brings in). Since then it
has been used for other functionality that was thought desirable for use
with **grid**, and hence has been transferred from package **graphics**
to **grDevices**. This is principally concerned with the handling of
colours and recording and replaying plots.

---

• [Graphics devices](#Graphics-devices)     
 • [Colours](#Colours)     
 • [Base graphics](#Base-graphics)     
 • [Grid graphics](#Grid-graphics)

---

---

### 6.1 Graphics Devices

R ships with several graphics devices, and there is support for
third-party packages to provide additional devices---several packages
now do. This section describes the device internals from the viewpoint
of a would-be writer of a graphics device.

---

• [Device structures](#Device-structures)     
 • [Device capabilities](#Device-capabilities)     
 • [Handling text](#Handling-text)     
 • [Conventions](#Conventions)     
 • [\'Mode\'](#g_t_0027Mode_0027)     
 • [Graphics events](#Graphics-events)     
 • [Specific devices](#Specific-devices)

---

---

#### 6.1.1 Device structures

There are two types used internally which are pointers to structures
related to graphics devices.

The `DevDesc` type is a structure defined in the header file
`R_ext/GraphicsDevice.h` (which is included by
`R_ext/GraphicsEngine.h`). This describes the physical
characteristics of a device, the capabilities of the device driver and
contains a set of callback functions that will be used by the graphics
engine to obtain information about the device and initiate actions (e.g.
a new page, plotting a line or some text). Type `pDevDesc` is a pointer
to this type.

The following callbacks can be omitted (or set to the null pointer,
their default value) when appropriate default behaviour will be taken by
the graphics engine: `activate`, `cap`, `deactivate`, `locator`,
`holdflush` (API version 9), `mode`, `newFrameConfirm`, `path`, `raster`
and `size`.

The relationship of device units to physical dimensions is set by the
element `ipr` of the `DevDesc` structure: a '`double`' array of
length 2.

The `GEDevDesc` type is a structure defined in
`R_ext/GraphicsEngine.h` (with comments in the file) as

```r
typedef struct _GEDevDesc GEDevDesc;
struct _GEDevDesc {
    pDevDesc dev;
    Rboolean displayListOn;
    SEXP displayList;
    SEXP DLlastElt;
    SEXP savedSnapshot;
    Rboolean dirty;
    Rboolean recordGraphics;
    GESystemDesc *gesd[MAX_GRAPHICS_SYSTEMS];
    Rboolean ask;
}
```

So this is essentially a device structure plus information about the
device maintained by the graphics engine and
normally[^17^](#FOOT17) visible to the engine and not to the
device. Type `pGEDevDesc` is a pointer to this type.

The graphics engine maintains an array of devices, as pointers to
`GEDevDesc` structures. The array is of size 64 but the first element is
always occupied by the `"null device"` and the final element is kept as
NULL as a sentinel.[^18^](#FOOT18) This array is reflected in
the R variable '`.Devices`'. Once a device is killed its
element becomes available for reallocation (and its name will appear as
`""` in '`.Devices`'). Exactly one of the devices is 'active':
this is the the null device if no other device has been opened and not
killed.

Each instance of a graphics device needs to set up a `GEDevDesc`
structure by code very similar to

```r
    pGEDevDesc gdd;

    R_GE_checkVersionOrDie(R_GE_version);
    R_CheckDeviceAvailable();
    BEGIN_SUSPEND_INTERRUPTS {
        pDevDesc dev;
        /* Allocate and initialize the device driver data */
        if (!(dev = (pDevDesc) calloc(1, sizeof(DevDesc))))
            return 0; /* or error() */
        /* set up device driver or free ‘dev’ and error() */
        gdd = GEcreateDevDesc(dev);
        GEaddDevice2(gdd, "dev_name");
    } END_SUSPEND_INTERRUPTS;
```

The `DevDesc` structure contains a `void *` pointer
'`deviceSpecific`' which is used to store data specific to the
device. Setting up the device driver includes initializing all the
non-zero elements of the `DevDesc` structure.

Note that the device structure is zeroed when allocated: this provides
some protection against future expansion of the structure since the
graphics engine can add elements that need to be non-NULL/non-zero to be
'on' (and the structure ends with 64 reserved bytes which will be zeroed
and allow for future expansion).

Rather more protection is provided by the version number of the
engine/device API, `R_GE_version` defined in
`R_ext/GraphicsEngine.h` together with access functions

```r
int R_GE_getVersion(void);
void R_GE_checkVersionOrDie(int version);
```

If a graphics device calls `R_GE_checkVersionOrDie(R_GE_version)` it can
ensure it will only be used in versions of R which provide the API it
was designed for and compiled against.

---

#### 6.1.2 Device capabilities

The following 'capabilities' can be defined for the device's `DevDesc`
structure.

- `canChangeGamma` -- `Rboolean`: can the display gamma be adjusted?
  This is now ignored, as gamma support has been removed.
- `canHadj` -- `integer`: can the device do horizontal adjustment of
  text _via_ the `text` callback, and if so, how precisely? 0 = no
  adjustment, 1 = {0, 0.5, 1} (left, centre, right justification) or 2
  = continuously variable (in \[0,1\]) between left and right
  justification.
- `canGenMouseDown` -- `Rboolean`: can the device handle mouse down
  events? This flag and the next three are not currently used by R,
  but are maintained for back compatibility.
- `canGenMouseMove` -- `Rboolean`: ditto for mouse move events.
- `canGenMouseUp` -- `Rboolean`: ditto for mouse up events.
- `canGenKeybd` -- `Rboolean`: ditto for keyboard events.
- `hasTextUTF8` -- `Rboolean`: should non-symbol text be sent (in
  UTF-8) to the `textUTF8` and `strWidthUTF8` callbacks, and sent as
  Unicode points (negative values) to the `metricInfo` callback?
- `wantSymbolUTF8` -- `Rboolean`: should symbol text be handled in
  UTF-8 in the same way as other text? Requires `textUTF8 = TRUE`.
- `haveTransparency`: does the device support semi-transparent
  colours?
- `haveTransparentBg`: can the background be fully or
  semi-transparent?
- `haveRaster`: is there support for rendering raster images?
- `haveCapture`: is there support for `grid::grid.cap`?
- `haveLocator`: is there an interactive locator?

The last three can often be deduced to be false from the presence of
`NULL` entries instead of the corresponding functions.

---

#### 6.1.3 Handling text

Handling text is probably the hardest task for a graphics device, and
the design allows for the device to optionally indicate that it has
additional capabilities. (If the device does not, these will if possible
be handled in the graphics engine.)

The three callbacks for handling text that must be in all graphics
devices are `text`, `strWidth` and `metricInfo` with declarations

```r
void text(double x, double y, const char *str, double rot, double hadj,
          pGgcontext gc, pDevDesc dd);

double strWidth(const char *str, pGEcontext gc, pDevDesc dd);

void metricInfo(int c, pGEcontext gc,
               double* ascent, double* descent, double* width,
               pDevDesc dd);
```

The '`gc`' parameter provides the graphics context, most
importantly the current font and fontsize, and '`dd`' is a
pointer to the active device's structure.

The `text` callback should plot '`str`' at
'`(x, y)`'[^19^](#FOOT19) with an anti-clockwise
rotation of '`rot`' degrees. (For '`hadj`' see below.)
The interpretation for horizontal text is that the baseline is at `y`
and the start is a `x`, so any left bearing for the first character will
start at `x`.

The `strWidth` callback computes the width of the string which it would
occupy if plotted horizontally in the current font. (Width here is
expected to include both (preferably) or neither of left and right
bearings.)

The `metricInfo` callback computes the size of a single character:
`ascent` is the distance it extends above the baseline and `descent` how
far it extends below the baseline. `width` is the amount by which the
cursor should be advanced when the character is placed. For `ascent` and
`descent` this is intended to be the bounding box of the 'ink' put down
by the glyph and not the box which might be used when assembling a line
of conventional text (it needs to be for e.g. `hat(beta)` to work
correctly). However, the `width` is used in plotmath to advance to the

In addition, if device capability `hasTextUTF8` (see below) is true,
Unicode points will be passed as negative values: the code snippet above
shows how to handle this. (This applies to the symbol font only if
device capability `wantSymbolUTF8` is true.)

If possible, the graphics device should handle clipping of text. It
indicates this by the structure element `canClip` which if true will
result in calls to the callback `clip` to set the clipping region. If
this is not done, the engine will clip very crudely (by omitting any
text that does not appear to be wholly inside the clipping region).

The device structure has an integer element `canHadj`, which indicates
if the device can do horizontal alignment of text. If this is one,
argument '`hadj`' to `text` will be called as `0 ,0.5, 1` to
indicate left-, centre- and right-alignment at the indicated position.
If it is two, continuous values in the range `[0, 1]` are assumed to be
supported.

Capability `hasTextUTF8` if true, it has two consequences. First, there
are callbacks `textUTF8` and `strWidthUTF8` that should behave
identically to `text` and `strWidth` except that '`str`' is
assumed to be in UTF-8 rather than the current locale's encoding. The
graphics engine will call these for all text except in the symbol font.
Second, Unicode points will be passed to the `metricInfo` callback as
negative integers. If your device would prefer to have UTF-8-encoded
symbols, define `wantSymbolUTF8` as well as `hasTextUTF8`. In that case
text in the symbol font is sent to `textUTF8` and `strWidthUTF8`.

Some devices can produce high-quality rotated text, but those based on
bitmaps often cannot. Those which can should set
`useRotatedTextInContour` to be true from graphics API version 4.

Several other elements relate to the precise placement of text by the
graphics engine:

```r
double xCharOffset;
double yCharOffset;
double yLineBias;
double cra[2];
```

These are more than a little mysterious. Element `cra` provides an
indication of the character size, `par("cra")` in base graphics, in
device units. The mystery is what is meant by 'character size': which
character, which font at which size? Some help can be obtained by
looking at what this is used for. The first element, 'width', is not
used by R except to set the graphical parameters. The second, 'height',
is use to set the line spacing, that is the relationship between
`par("mai")` and `par("mai")` and so on. It is suggested that a good
choice is

```r
dd->cra[0] = 0.9 * fnsize;
dd->cra[1] = 1.2 * fnsize;
```

where '`fnsize`' is the 'size' of the standard font (`cex=1`)
on the device, in device units. So for a 12-point font (the usual
default for graphics devices), '`fnsize`' should be 12 points
in device units.

The remaining elements are yet more mysterious. The `postscript()`
device says

```r
    /* Character Addressing Offsets */
    /* These offsets should center a single */
    /* plotting character over the plotting point. */
    /* Pure guesswork and eyeballing ... */

    dd->xCharOffset =  0.4900;
    dd->yCharOffset =  0.3333;
    dd->yLineBias = 0.2;
```

It seems that `xCharOffset` is not currently used, and `yCharOffset` is
used by the base graphics system to set vertical alignment in `text()`
when `pos` is specified, and in `identify()`. It is occasionally used by
the graphic engine when attempting exact centring of text, such as
character string values of `pch` in `points()` or
`grid.points()`---however, it is only used when precise character metric
information is not available or for multi-line strings.

`yLineBias` is used in the base graphics system in `axis()` and
`mtext()` to provide a default for their '`padj`' argument.

---

#### 6.1.4 Conventions

The aim is to make the (default) output from graphics devices as similar
as possible. Generally people follow the model of the `postscript` and
`pdf` devices (which share most of their internal code).

The following conventions have become established:

- The default size of a device should be 7 inches square.
- There should be a '`pointsize`' argument which defaults to
  12, and it should give the pointsize in big points (1/72 inch). How
  exactly this is interpreted is font-specific, but it should use a
  font which works with lines packed 1/6 inch apart, and looks good
  with lines 1/5 inch apart (that is with 2pt leading).
- The default font family should be a sans serif font, e.g Helvetica
  or similar (e.g. Arial on Windows).
- `lwd = 1` should correspond to a line width of 1/96 inch. This will
  be a problem with pixel-based devices, and generally there is a
  minimum line width of 1 pixel (although this may not be appropriate
  where anti-aliasing of lines is used, and `cairo` prefers a minimum
  of 2 pixels).
- Even very small circles should be visible, e.g. by using a minimum
  radius of 1 pixel or replacing very small circles by a single filled
  pixel.
- How RGB colour values will be interpreted should be documented, and
  preferably be sRGB.
- The help page should describe its policy on these conventions.

These conventions are less clear-cut for bitmap devices, especially
where the bitmap format does not have a design resolution.

The interpretation of the line texture (`par("lty"`) is described in the
header `GraphicsEngine.h` and in the help for `par`: note that
the 'scale' of the pattern should be proportional to the line width (at
least for widths above the default).

---

#### 6.1.5 'Mode'

One of the device callbacks is a function `mode`, documented in the
header as

```r
     * device_Mode is called whenever the graphics engine
     * starts drawing (mode=1) or stops drawing (mode=0)
     * GMode (in graphics.c) also says that
     * mode = 2 (graphical input on) exists.
     * The device is not required to do anything
```

Since `mode = 2` has only recently been documented at device level. It
could be used to change the graphics cursor, but devices currently do
that in the `locator` callback. (In base graphics the mode is set for
the duration of a `locator` call, but if `type != "n"` is switched back
for each point whilst annotation is being done.)

Many devices do indeed do nothing on this call, but some screen devices
ensure that drawing is flushed to the screen when called with
`mode = 0`. It is tempting to use it for some sort of buffering, but
note that 'drawing' is interpreted at quite a low level and a typical
single figure will stop and start drawing many times. The buffering
introduced in the `X11()` device makes use of `mode = 0` to indicate
activity: it updates the screen after _ca_ 100ms of inactivity.

This callback need not be supplied if it does nothing.

---

#### 6.1.6 Graphics events

Graphics devices may be designed to handle user interaction: not all
are.

Users may use `grDevices::setGraphicsEventEnv` to set the `eventEnv`
environment in the device driver to hold event handlers. When the user
calls `grDevices::getGraphicsEvent`, R will take three steps. First, it
sets the device driver member `gettingEvent` to `true` for each device
with a non-`NULL` `eventEnv` entry, and calls `initEvent(dd, true)` if
the callback is defined. It then enters an event loop. Each time through
the loop R will process events once, then check whether any device has
set the `result` member of `eventEnv` to a non-`NULL` value, and will
save the first such value found to be returned. C functions
`doMouseEvent` and `doKeybd` are provided to call the R event handlers
`onMouseDown`, `onMouseMove`, `onMouseUp`, and `onKeybd` and set
`eventEnv$result` during this step. Finally, `initEvent` is called again
with `init=false` to inform the devices that the loop is done, and the
result is returned to the user.

---

#### 6.1.7 Specific devices

Specific devices are mostly documented by comments in their sources,
although for devices of many years' standing those comments can be in
need of updating. This subsection is a repository of notes on design
decisions.

---

• [X11()](#X11_0028_0029)     
 • [windows()](#windows_0028_0029)

---

---

#### 6.1.7.1 X11()

The `X11(type="Xlib")` device dates back to the mid 1990's and was
written then in `Xlib`, the most basic X11 toolkit. It has since
optionally made use of a few features from other toolkits: `libXt` is
used to read X11 resources, and `libXmu` is used in the handling of
clipboard selections.

Using basic `Xlib` code makes drawing fast, but is limiting. There is no
support of translucent colours (that came in the `Xrender` toolkit of

2000. nor for rotated text (which R implements by rendering text to a
      bitmap and rotating the latter).

The hinting for the X11 window asks for backing store to be used, and
some windows managers may use it to handle repaints, but it seems that
most repainting is done by replaying the display list (and here the fast
drawing is very helpful).

There are perennial problems with finding fonts. Many users fail to
realize that fonts are a function of the X server and not of the machine
that R is running on. After many difficulties, R tries first to find the
nearest size match in the sizes provided for Adobe fonts in the standard
75dpi and 100dpi X11 font packages---even that will fail to work when
users of near-100dpi screens have only the 75dpi set installed. The
75dpi set allows sizes down to 6 points on a 100dpi screen, but some
users do try to use smaller sizes and even 6 and 8 point bitmapped fonts
do not look good.

Introduction of UTF-8 locales has caused another wave of difficulties.
X11 has very few genuine UTF-8 fonts, and produces composite fontsets
for the `iso10646-1` encoding. Unfortunately these seem to have low
coverage apart from a few monospaced fonts in a few sizes (which are not
suitable for graph annotation), and where glyphs are missing what is
plotted is often quite unsatisfactory.

The current approach is to make use of more modern toolkits, namely
`cairo` for rendering and `Pango` for font management---because these
are associated with `Gtk+2` they are widely available. Cairo supports
translucent colours and alpha-blending (_via_ `Xrender`), and
anti-aliasing for the display of lines and text. Pango's font management
is based on `fontconfig` and somewhat mysterious, but it seems mainly to
use Type 1 and TrueType fonts on the machine running R and send
grayscale bitmaps to cairo.

---

#### 6.1.7.2 windows()

The `windows()` device is a family of devices: it supports plotting to
Windows (enhanced) metafiles, `BMP`, `JPEG`, `PNG` and `TIFF` files as
well as to Windows printers.

In most of these cases the primary plotting is to a bitmap: this is used
for the (default) buffering of the screen device, which also enables the
current plot to be saved to BMP, JPEG, PNG or TIFF (it is the internal
bitmap which is copied to the file in the appropriate format).

The device units are pixels (logical ones on a metafile device).

The code was originally written by Guido Masarotto with extensive use of
macros, which can make it hard to disentangle.

For a screen device, `xd->gawin` is the canvas of the screen, and
`xd->bm` is the off-screen bitmap. So macro `DRAW` arranges to plot to
`xd->bm`, and if buffering is off, also to `xd->gawin`. For all other
device, `xd->gawin` is the canvas, a bitmap for the `jpeg()` and `png()`
device, and an internal representation of a Windows metafile for the
`win.metafile()` and `win.print` device. Since 'plotting' is done by
Windows GDI calls to the appropriate canvas, its precise nature is
hidden by the GDI system.

Buffering on the screen device is achieved by running a timer, which
when it fires copies the internal bitmap to the screen. This is set to
fire every 500ms (by default) and is reset to 100ms after plotting
activity.

Repaint events are handled by copying the internal bitmap to the screen
canvas (and then reinitializing the timer), unless there has been a
resize. Resizes are handled by replaying the display list: this might
not be necessary if a fixed canvas with scrollbars is being used, but
that is the least popular of the three forms of resizing.

Text on the device has moved to 'Unicode' (UCS-2) in recent years. UTF-8
is requested (`hasTextUTF8 = TRUE`) for standard text, and converted to
UCS-2 in the plotting functions in file
`src/extra/graphapp/gdraw.c`. However, GDI has no support for
Unicode symbol fonts, and symbols are handled in Adobe Symbol encoding.

There is support for translucent colours (with alpha channel between 0
and 255) was introduced on the screen device and bitmap
devices.[^20^](#FOOT20) This is done by drawing on a further
internal bitmap, `xd->bm2`, in the opaque version of the colour then
alpha-blending that bitmap to `xd->bm`. The alpha-blending routine is in
a separate DLL, `msimg32.dll`, which is loaded on first use. As
small a rectangular region as reasonably possible is alpha-blended (this
is rectangle `r` in the code), but things like mitre joins make
estimation of a tight bounding box too much work for lines and polygonal
boundaries. Translucent-coloured lines are not common, and the
performance seems acceptable.

The support for a transparent background in `png()` predates full
alpha-channel support in `libpng` (let alone in PNG viewers), so makes
use of the limited transparency support in earlier versions of PNG.
Where 24-bit colour is used, this is done by marking a single colour to
be rendered as transparent. R chose '`#fdfefd`', and uses this
as the background colour (in `GA_NewPage` if the specified background
colour is transparent (and all non-opaque background colours are treated
as transparent). So this works by marking that colour in the PNG file,
and viewers without transparency support see a slightly-off-white
background, as if there were a near-white canvas. Where a palette is
used in the PNG file (if less than 256 colours were used) then this
colour is recorded with full transparency and the remaining colours as
opaque. If 32-bit colour were available then we could add a full alpha
channel, but this is dependent on the graphics hardware and undocumented
properties of GDI.

---

### 6.2 Colours

Devices receive colours as a `typedef` `rcolor` (an `unsigned int`)
defined in the header `R_ext/GraphicsEngine.h`). The 4 bytes
are _R_ ,_G_, _B_ and _alpha_ from least to most significant. So each of
RGB has 256 levels of luminosity from 0 to 255. The alpha byte
represents opacity, so value 255 is fully opaque and 0 fully
transparent: many but not all devices handle semi-transparent colours.

Colors can be created in C via the macro `R_RGBA`, and a set of macros
are defined in `R_ext/GraphicsDevice.h` to extract the various
components.

Colours in the base graphics system were originally adopted from S (and
before that the GRZ library from Bell Labs), with the concept of a
(variable-sized) palette of colours referenced by numbers
'`1...N`' plus '`0`' (the background colour of the
current device). R introduced the idea of referring to colours by
character strings, either in the forms '`#RRGGBB`' or
'`#RRGGBBAA`' (representing the bytes in hex) as given by
function `rgb()` or via names: the 657 known names are given in the
character vector `colors` and in a table in file `colors.c` in
package **grDevices**. Note that semi-transparent colours are not
'premultiplied', so 50% transparent white is '`#ffffff80`'.

Integer or character `NA` colours are mapped internally to transparent
white, as is the character string `"NA"`.

Negative colour numbers are an error. Colours greater than
'`N`' are wrapped around, so that for example with the default
palette of size 8, colour '`10`' is colour '`2`' in
the palette.

Integer colours have been used more widely than the base graphics
sub-system, as they are supported by package **grid** and hence by
[**lattice**](https://CRAN.R-project.org/package=lattice) and
[**ggplot2**](https://CRAN.R-project.org/package=ggplot2). (They are
also used by package [**rgl**](https://CRAN.R-project.org/package=rgl).)
**grid** did re-define colour '`0`' to be transparent white,
but [**rgl**](https://CRAN.R-project.org/package=rgl) used `col2rgb` and
hence the background colour of base graphics.

Note that positive integer colours refer to the current palette and
colour '`0`' to the current device (and a device is opened if
needs be). These are mapped to type `rcolor` at the time of use: this
matters when re-playing the display list, e.g. when a device is resized
or `dev.copy` is used. The palette should be thought of as per-session:
it is stored in package **grDevices**.

The convention is that devices use the colorspace 'sRGB'. This is an
industry standard: it is used by Web browsers and JPEGs from all but
high-end digital cameras. The interpretation is a matter for graphics
devices and for code that manipulates colours, but not for the graphics
engine or subsystems.

R uses a painting model similar to PostScript and PDF. This means that
where shapes (circles, rectangles and polygons) can both be filled and
have a stroked border, the fill should be painted first and then the
border (or otherwise only half the border will be visible). Where both
the fill and the border are semi-transparent there is some room for
interpretation of the intention. Most devices first paint the fill and
then the border, alpha-blending at each step. However, PDF does some
automatic grouping of objects, and _when the fill and the border have
the same alpha_, they are painted onto the same layer and then
alpha-blended in one step. (See p. 569 of the PDF Reference Sixth
Edition, version 1.7. Unfortunately, although this is what the PDF
standard says should happen, it is not correctly implemented by some
viewers.)

The mapping from colour numbers to type `rcolor` is primarily done by
function `RGBpar3`: this is exported from the R binary but linked to
code in package **grDevices**. The first argument is a `SEXP` pointing
to a character, integer or double vector, and the second is the `rcolor`
value for colour `0` (or `"0"`). C entry point `RGBpar` is a wrapper
that takes `0` to be transparent white: it is often used to set colour
defaults for devices. The R-level wrapper is `col2rgb`.

There is also `R_GE_str2col` which takes a C string and converts to type
`rcolor`: `"0'` is converted to transparent white.

There is a R-level conversion of colours to '`##RRGGBBAA`' by
`image.default(useRaster = TRUE)`.

The other color-conversion entry point in the API is `name2col` which
takes a colour name (a C string) and returns a value of type `rcolor`.
This handles `"NA"`, `"transparent"` and the 657 colours known to the R
function `colors()`.

---

### 6.3 Base graphics

The base graphics system was migrated to package **graphics** in R
3.0.0: it was previously implemented in files in `src/main`.

For historical reasons it is largely implemented in two layers. Files
`plot.c`, `plot3d.c` and `par.c` contain the
code for the around 30 `.External` calls that implement the basic
graphics operations. This code then calls functions with names starting
with `G` and declared in header `Rgraphics.h` in file
`graphics.c`, which in turn call the graphics engine (whose
functions almost all have names starting with `GE`).

A large part of the infrastructure of the base graphics subsystem are
the graphics parameters (as set/read by `par()`). These are stored in a
`GPar` structure declared in the private header `Graphics.h`.
This structure has two variables (`state` and `valid`) tracking the
state of the base subsystem on the device, and many variables recording
the graphics parameters and functions of them.

The base system state is contained in `baseSystemState` structure
defined in `R_ext/GraphicsBase.h`. This contains three `GPar`
structures and a Boolean variable used to record if `plot.new()` (or
`persp`) has been used successfully on the device.

The three copies of the `GPar` structure are used to store the current
parameters (accessed via `gpptr`), the 'device copy' (accessed via
`dpptr`) and space for a saved copy of the 'device copy' parameters. The
current parameters are, clearly, those currently in use and are copied
from the 'device copy' whenever `plot.new()` is called (whether or not
that advances to the next 'page'). The saved copy keeps the state when
the device was last completely cleared (e.g. when `plot.new()` was
called with `par(new=TRUE)`), and is used to replay the display list.

The separation is not completely clean: the 'device copy' is altered if
a plot with log scale(s) is set up via `plot.window()`.

There is yet another copy of most of the graphics parameters in `static`
variables in `graphics.c` which are used to preserve the
current parameters across the processing of inline parameters in
high-level graphics calls (handled by `ProcessInlinePars`).

Snapshots of the base subsystem record the 'saved device copy' of the
`GPar` structure.

---

• [Arguments and parameters](#Arguments-and-parameters)

---

---

#### 6.3.1 Arguments and parameters

There is an unfortunate confusion between some of the graphical
parameters (as set by `par`) and arguments to base graphic functions of
the same name. This description may help set the record straight.

Most of the high-level plotting functions accept graphical parameters as
additional arguments, which are then often passed to lower-level
functions if not already named arguments (which is the main source of
confusion).

Graphical parameter `bg` is the background colour of the plot. Argument
`bg` refers to the fill colour for the filled symbols `21` to `25`. It
is an argument to the function `plot.xy`, but normally passed by the
default method of `points`, often from a `plot` method.

Graphics parameters `cex`, `col`, `lty`, `lwd` and `pch` also appear as
arguments of `plot.xy` and so are often passed as arguments from
higher-level plot functions such as `lines`, `points` and `plot`
methods. They appear as arguments of `legend`, `col`, `lty` and `lwd`
are arguments of `arrows` and `segments`. When used as arguments they
can be vectors, recycled to control the various lines, points and
segments. When set a graphical parameters they set the default
rendering: in addition `par(cex=)` sets the overall character expansion
which subsequent calls (as arguments or on-line graphical parameters)
multiply.

The handling of missing values differs in the two classes of uses.
Generally these are errors when used in `par` but cause the
corresponding element of the plot to be omitted when used as an element
of a vector argument. Originally the interpretation of arguments was
mainly left to the device, but nowadays some of this is pre-empted in
the graphics engine (but for example the handling of `lwd = 0` remains
device-specific, with some interpreting it as a 'thinnest possible'
line).

---

### 6.4 Grid graphics

\[At least pointers to documentation.\]

---
