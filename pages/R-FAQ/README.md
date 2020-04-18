---
Generator: texi2any
description: R FAQ
distribution: global
keywords: R FAQ
resource-type: document
title: R FAQ
---

# R FAQ

## Frequently Asked Questions on R

### Version 2018-10-18

### Kurt Hornik

---

## Table of Contents

- [1 Introduction](#Introduction)
  - [1.1 Legalese](#Legalese)
  - [1.2 Obtaining this
    document](#Obtaining-this-document)
  - [1.3 Citing this
    document](#Citing-this-document)
  - [1.4 Notation](#Notation)
  - [1.5 Feedback](#Feedback)
- [2 R Basics](#R-Basics)
  - [2.1 What is R?](#What-is-R_003f)
  - [2.2 What machines does R run
    on?](#What-machines-does-R-run-on_003f)
  - [2.3 What is the current version of
    R?](#What-is-the-current-version-of-R_003f)
  - [2.4 How can R be
    obtained?](#How-can-R-be-obtained_003f)
  - [2.5 How can R be
    installed?](#How-can-R-be-installed_003f)
    - [2.5.1 How can R be installed
      (Unix-like)](#How-can-R-be-installed-_0028Unix_002dlike_0029)
    - [2.5.2 How can R be installed
      (Windows)](#How-can-R-be-installed-_0028Windows_0029)
    - [2.5.3 How can R be installed
      (Mac)](#How-can-R-be-installed-_0028Mac_0029)
  - [2.6 Are there Unix-like binaries for
    R?](#Are-there-Unix_002dlike-binaries-for-R_003f)
  - [2.7 What documentation exists for
    R?](#What-documentation-exists-for-R_003f)
  - [2.8 Citing R](#Citing-R)
  - [2.9 What mailing lists exist for
    R?](#What-mailing-lists-exist-for-R_003f)
  - [2.10 What is
    CRAN?](#What-is-CRAN_003f)
  - [2.11 Can I use R for commercial
    purposes?](#Can-I-use-R-for-commercial-purposes_003f)
  - [2.12 Why is R named
    R?](#Why-is-R-named-R_003f)
  - [2.13 What is the R
    Foundation?](#What-is-the-R-Foundation_003f)
  - [2.14 What is
    R-Forge?](#What-is-R_002dForge_003f)
- [3 R and S](#R-and-S)
  - [3.1 What is S?](#What-is-S_003f)
  - [3.2 What is
    [S-PLUS]?](#What-is-S_002dPLUS_003f)
  - [3.3 What are the differences between R and
    S?](#What-are-the-differences-between-R-and-S_003f)
    - [3.3.1 Lexical
      scoping](#Lexical-scoping)
    - [3.3.2 Models](#Models)
    - [3.3.3 Others](#Others)
  - [3.4 Is there anything R can do that [S-PLUS]
    cannot?](#Is-there-anything-R-can-do-that-S_002dPLUS-cannot_003f)
  - [3.5 What is
    R-plus?](#What-is-R_002dplus_003f)
- [4 R Web Interfaces](#R-Web-Interfaces)
- [5 R Add-On
  Packages](#R-Add_002dOn-Packages)
  - [5.1 Which add-on packages exist for
    R?](#Which-add_002don-packages-exist-for-R_003f)
    - [5.1.1 Add-on packages in
      R](#Add_002don-packages-in-R)
    - [5.1.2 Add-on packages from
      CRAN](#Add_002don-packages-from-CRAN)
    - [5.1.3 Add-on packages from
      Omegahat](#Add_002don-packages-from-Omegahat)
    - [5.1.4 Add-on packages from
      Bioconductor](#Add_002don-packages-from-Bioconductor)
    - [5.1.5 Other add-on
      packages](#Other-add_002don-packages)
  - [5.2 How can add-on packages be
    installed?](#How-can-add_002don-packages-be-installed_003f)
  - [5.3 How can add-on packages be
    used?](#How-can-add_002don-packages-be-used_003f)
  - [5.4 How can add-on packages be
    removed?](#How-can-add_002don-packages-be-removed_003f)
  - [5.5 How can I create an R
    package?](#How-can-I-create-an-R-package_003f)
  - [5.6 How can I contribute to
    R?](#How-can-I-contribute-to-R_003f)
- [6 R and Emacs](#R-and-Emacs)
  - [6.1 Is there Emacs support for
    R?](#Is-there-Emacs-support-for-R_003f)
  - [6.2 Should I run R from within
    Emacs?](#Should-I-run-R-from-within-Emacs_003f)
  - [6.3 Debugging R from within
    Emacs](#Debugging-R-from-within-Emacs)
- [7 R Miscellanea](#R-Miscellanea)
  - [7.1 How can I set components of a list to
    NULL?](#How-can-I-set-components-of-a-list-to-NULL_003f)
  - [7.2 How can I save my
    workspace?](#How-can-I-save-my-workspace_003f)
  - [7.3 How can I clean up my
    workspace?](#How-can-I-clean-up-my-workspace_003f)
  - [7.4 How can I get eval() and D() to
    work?](#How-can-I-get-eval_0028_0029-and-D_0028_0029-to-work_003f)
  - [7.5 Why do my matrices lose
    dimensions?](#Why-do-my-matrices-lose-dimensions_003f)
  - [7.6 How does autoloading
    work?](#How-does-autoloading-work_003f)
  - [7.7 How should I set
    options?](#How-should-I-set-options_003f)
  - [7.8 How do file names work in
    Windows?](#How-do-file-names-work-in-Windows_003f)
  - [7.9 Why does plotting give a color allocation
    error?](#Why-does-plotting-give-a-color-allocation-error_003f)
  - [7.10 How do I convert factors to
    numeric?](#How-do-I-convert-factors-to-numeric_003f)
  - [7.11 Are Trellis displays implemented in
    R?](#Are-Trellis-displays-implemented-in-R_003f)
  - [7.12 What are the enclosing and parent
    environments?](#What-are-the-enclosing-and-parent-environments_003f)
  - [7.13 How can I substitute into a plot
    label?](#How-can-I-substitute-into-a-plot-label_003f)
  - [7.14 What are valid
    names?](#What-are-valid-names_003f)
  - [7.15 Are GAMs implemented in
    R?](#Are-GAMs-implemented-in-R_003f)
  - [7.16 Why is the output not printed when I source() a
    file?](#Why-is-the-output-not-printed-when-I-source_0028_0029-a-file_003f)
  - [7.17 Why does outer() behave strangely with my
    function?](#Why-does-outer_0028_0029-behave-strangely-with-my-function_003f)
  - [7.18 Why does the output from anova() depend on the order of
    factors in the
    model?](#Why-does-the-output-from-anova_0028_0029-depend-on-the-order-of-factors-in-the-model_003f)
  - [7.19 How do I produce PNG graphics in batch
    mode?](#How-do-I-produce-PNG-graphics-in-batch-mode_003f)
  - [7.20 How can I get command line editing to
    work?](#How-can-I-get-command-line-editing-to-work_003f)
  - [7.21 How can I turn a string into a
    variable?](#How-can-I-turn-a-string-into-a-variable_003f)
  - [7.22 Why do lattice/trellis graphics not
    work?](#Why-do-lattice_002ftrellis-graphics-not-work_003f)
  - [7.23 How can I sort the rows of a data
    frame?](#How-can-I-sort-the-rows-of-a-data-frame_003f)
  - [7.24 Why does the help.start() search engine not
    work?](#Why-does-the-help_002estart_0028_0029-search-engine-not-work_003f)
  - [7.25 Why did my .Rprofile stop working when I updated
    R?](#Why-did-my-_002eRprofile-stop-working-when-I-updated-R_003f)
  - [7.26 Where have all the methods
    gone?](#Where-have-all-the-methods-gone_003f)
  - [7.27 How can I create rotated axis
    labels?](#How-can-I-create-rotated-axis-labels_003f)
  - [7.28 Why is read.table() so
    inefficient?](#Why-is-read_002etable_0028_0029-so-inefficient_003f)
  - [7.29 What is the difference between package and
    library?](#What-is-the-difference-between-package-and-library_003f)
  - [7.30 I installed a package but the functions are not
    there](#I-installed-a-package-but-the-functions-are-not-there)
  - [7.31 Why doesn't R think these numbers are
    equal?](#Why-doesn_0027t-R-think-these-numbers-are-equal_003f)
  - [7.32 How can I capture or ignore errors in a long
    simulation?](#How-can-I-capture-or-ignore-errors-in-a-long-simulation_003f)
  - [7.33 Why are powers of negative numbers
    wrong?](#Why-are-powers-of-negative-numbers-wrong_003f)
  - [7.34 How can I save the result of each iteration in a loop into
    a separate
    file?](#How-can-I-save-the-result-of-each-iteration-in-a-loop-into-a-separate-file_003f)
  - [7.35 Why are _p_-values not displayed when using
    lmer()?](#Why-are-p_002dvalues-not-displayed-when-using-lmer_0028_0029_003f)
  - [7.36 Why are there unwanted borders, lines or grid-like
    artifacts when viewing a plot saved to a PS or PDF
    file?](#Why-are-there-unwanted-borders)
  - [7.37 Why does backslash behave strangely inside
    strings?](#Why-does-backslash-behave-strangely-inside-strings_003f)
  - [7.38 How can I put error bars or confidence bands on my
    plot?](#How-can-I-put-error-bars-or-confidence-bands-on-my-plot_003f)
  - [7.39 How do I create a plot with two
    y-axes?](#How-do-I-create-a-plot-with-two-y_002daxes_003f)
  - [7.40 How do I access the source code for a
    function?](#How-do-I-access-the-source-code-for-a-function_003f)
  - [7.41 Why does summary() report strange results for the R\^2
    estimate when I fit a linear model with no
    intercept?](#Why-does-summary_0028_0029-report-strange-results-for-the-R_005e2-estimate-when-I-fit-a-linear-model-with-no-intercept_003f)
  - [7.42 Why is R apparently not releasing
    memory?](#Why-is-R-apparently-not-releasing-memory_003f)
  - [7.43 How can I enable secure https downloads in
    R?](#How-can-I-enable-secure-https-downloads-in-R_003f)
  - [7.44 How can I get CRAN package binaries for outdated versions
    of
    R?](#How-can-I-get-CRAN-package-binaries-for-outdated-versions-of-R_003f)
- [8 R Programming](#R-Programming)
  - [8.1 How should I write summary
    methods?](#How-should-I-write-summary-methods_003f)
  - [8.2 How can I debug dynamically loaded
    code?](#How-can-I-debug-dynamically-loaded-code_003f)
  - [8.3 How can I inspect R objects when
    debugging?](#How-can-I-inspect-R-objects-when-debugging_003f)
  - [8.4 How can I change compilation
    flags?](#How-can-I-change-compilation-flags_003f)
  - [8.5 How can I debug S4
    methods?](#How-can-I-debug-S4-methods_003f)
- [9 R Bugs](#R-Bugs)
  - [9.1 What is a
    bug?](#What-is-a-bug_003f)
  - [9.2 How to report a
    bug](#How-to-report-a-bug)
- [10 Acknowledgments](#Acknowledgments)

# R FAQ

---

• [Introduction](#Introduction)     
 • [R Basics](#R-Basics)     
 • [R and S](#R-and-S)     
 • [R Web Interfaces](#R-Web-Interfaces)     
 • [R Add-On Packages](#R-Add_002dOn-Packages)     
 • [R and Emacs](#R-and-Emacs)     
 • [R Miscellanea](#R-Miscellanea)     
 • [R Programming](#R-Programming)     
 • [R Bugs](#R-Bugs)     
 • [Acknowledgments](#Acknowledgments)

---

---
