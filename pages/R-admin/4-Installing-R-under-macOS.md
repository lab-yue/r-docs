# 4 Installing R under macOS

---

('macOS' was known as 'OS X' from 2012--2016 and as 'Mac OS X' before
that.)

The front page of a CRAN site has a link 'Download R for (Mac) OS X'.
Click on that, then download the file `R-3.6.3.pkg` and install
it. This runs on macOS 10.11 and later (El Capitan, Sierra, High Sierra,
Mojave, Catalina, ...).

Installers for R-patched and R-devel are usually available from
<https://mac.R-project.org>. (Some of these packages are unsigned/not
notarized: to install those Control/right/two-finger click, select
'`Open With`' and '`Installer`'.)

For some older versions of the OS you can in principle (it is little
tested) install R from the sources (see [macOS](#macOS)).

It is important that if you use a binary installer package that your OS
is fully updated: look at 'Updates' from the 'App Store' to be sure. (If
using XQuartz, check that is current.)

To install, just double-click on the icon of the file you downloaded. At
the 'Installation Type' stage, note the option to 'Customize'. This
currently shows four components: everyone will need the 'R Framework'
component: the remaining components are optional. (The 'Tcl/Tk'
component is needed to use package **tcltk**. The 'Texinfo' component is
only needed by those installing source packages or R from its sources.)

This is an Apple Installer package. If you encounter any problem during
the installation, please check the Installer log by clicking on the
"Window" menu and item "Installer Log". The full output (select "Show
All Log") is useful for tracking down problems. Note the the installer
is clever enough to try to upgrade the last-installed version of the
application where you installed it (which may not be where you want this
time ...).

Various parts of the build require XQuartz to be installed: see
<https://xquartz.macosforge.org/>. These include the **tcltk** package
and the `X11` device: attempting to use these without XQuartz will
remind you. Also for the cairographics-based devices (which are not
often used on macOS) such as `png(type = "cairo")`.

If you update your macOS version, you should re-install R (and perhaps
XQuartz): the installer may tailor the installation to the current
version of the OS.

For building R from source, see [macOS](#macOS).

---

• [Running R under macOS](#Running-R-under-macOS)     
 • [Uninstalling under macOS](#Uninstalling-under-macOS)     
 • [Multiple versions](#Multiple-versions)

---

---

### 4.1 Running R under macOS

There are two ways to run R on macOS from a CRAN binary distribution.

There is a GUI console normally installed with the R icon in
`/Applications` which you can run by double-clicking (e.g. from
Launchpad or Finder). (If you cannot find it there it was possibly
installed elsewhere so try searching for it in Spotlight.) This is
usually referred to as [R.APP] to distinguish it from
command-line R: its user manual is currently part of the macOS FAQ at
<https://cran.r-project.org/bin/macosx/RMacOSX-FAQ.html> and can be
viewed from [R.APP]'s 'Help' menu.

You can run command-line R and `Rscript` from a
Terminal[^20^](#FOOT20) so these can be typed as commands like
any other Unix-alike: see the next chapter of this manual. There are
some small differences which may surprise users of R on other platforms,
notably the default location of the personal library directory (under
`~/Library/R`, e.g. `~/Library/R/3.6/library`), and
that warnings, messages and other output to `stderr` are
highlighted in bold.

It has been reported that running [R.APP] may fail if no
preferences are stored, so if it fails when launched for the very first
time, try it again (the first attempt will store some preferences).

Users of [R.APP] need to be aware of the 'App Nap' feature
(<https://developer.apple.com/library/mac/releasenotes/MacOSX/WhatsNewInOSX/Articles/MacOSX10_9.html>)
which can cause R tasks to appear to run very slowly when not producing
output in the console. Here are ways to avoid it:

- Ensure that the console is completely visible (or at least the
  activity indicator at the top right corner is visible).

- In a Terminal, run

```r
defaults write org.R-project.R NSAppSleepDisabled -bool YES
```

(see
<https://developer.apple.com/library/mac/releasenotes/MacOSX/WhatsNewInOSX/Articles/MacOSX10_9.html>).

Using the `X11` device or the X11-based versions of `View()` and
`edit()` for data frames and matrices (the latter are the default for
command-line R but not [R.APP]) requires an X sub-system to be
installed: see [macOS](#macOS). So do the **tcltk** package and some
third-party packages.

---

### 4.2 Uninstalling under macOS

R for macOS consists of two parts: the GUI ([R.APP]) and the R
framework. The un-installation is as simple as removing those folders
(e.g. by dragging them onto the Trash). The typical installation will
install the GUI into the `/Applications/R.app` folder and the R
framework into the `/Library/Frameworks/R.framework` folder.
The links to `R` and `Rscript` in
`/usr/local/bin` should also be removed.

If you want to get rid of R more completely using a Terminal, simply
run:

```r
sudo rm -Rf /Library/Frameworks/R.framework /Applications/R.app \
   /usr/local/bin/R /usr/local/bin/Rscript
```

The installation consists of up to four Apple
packages:[^21^](#FOOT21) `org.r-project.R.el-capitan.fw.pkg`,
`org.r-project.R.el-capitan.GUI.pkg`, `org.r-project.x86_64.tcltk.x11`
and `org.r-project.x86_64.texinfo`. You can use `pkgutil --forget` if
you want the Apple Installer to forget about the package without
deleting its files (useful for the R framework when installing multiple
R versions in parallel), or after you have deleted the files.

Uninstalling the Tcl/Tk or Texinfo components (which are installed under
`/usr/local`) is not as simple. You can list the files they
installed in a Terminal by

```r
pkgutil --files org.r-project.x86_64.tcltk.x11
pkgutil --files org.r-project.x86_64.texinfo
```

These are paths relative to `/`, the root of the file system.

---

### 4.3 Multiple versions

The installer will remove any previous version[^22^](#FOOT22)
of the R framework which it finds installed. This can be avoided by
using `pkgutil --forget` (see the previous section). However, note that
different versions are installed under
`/Library/Frameworks/R.framework/Versions` as `3.5`,
`3.6` and so on, so it is not possible to have different
'`3.x.y`' versions installed for the same '`x`'.

A version of R can be run directly from the command-line as e.g.

```r
/Library/Frameworks/R.framework/Versions/3.6/Resources/bin/R
```

However, [R.APP] will always run the 'current' version, that is
the last installed version. A small utility, `Rswitch.app` (available at
<https://mac.R-project.org/#other>: it is 32-bit so not usable on
Catalina), can be used to change the 'current' version. This is of
limited use as [R.APP] is compiled against a particular version
of R and will likely crash if switched to an earlier version. This may
allow you to install a development version of R (de-selecting
[R.APP]) and then switch back to the release version.

---
