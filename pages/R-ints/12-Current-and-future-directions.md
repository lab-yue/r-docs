12 Current and future directions

---

This chapter is for notes about possible in-progress and future changes
to R: there is no commitment to release such changes, let alone to a
timescale.

---

• [Long vectors](#Long-vectors)     
 • [64-bit types](#g_t64_002dbit-types)     
 • [Large matrices](#Large-matrices)

---

---

### 12.1 Long vectors

Vectors in R 2.x.y were limited to a length of 2\^31 - 1 elements (about
2 billion), as the length is stored in the `SEXPREC` as a C `int`, and
that type is used extensively to record lengths and element numbers,
including in packages.

Note that longer vectors are effectively impossible under 32-bit
platforms because of their address limit, so this section applies only
on 64-bit platforms. The internals are unchanged on a 32-bit build of R.

A single object with 2\^31 or more elements will take up at least 8GB of
memory if integer or logical and 16GB if numeric or character, so
routine use of such objects is still some way off.

There is now some support for long vectors. This applies to raw,
logical, integer, numeric and character vectors, and lists and
expression vectors. (Elements of character vectors (`CHARSXP`s) remain
limited to 2\^31 - 1 bytes.) Some considerations:

- This has been implemented by recording the length (and true length)
  as `-1` and recording the actual length as a 64-bit field at the
  beginning of the header. Because a fair amount of code in R uses a
  signed type for the length, the 'long length' is recorded using the
  signed C99 type `ptrdiff_t`, which is typedef-ed to `R_xlen_t`.
- These can in theory have 63-bit lengths, but note that current
  64-bit OSes do not even theoretically offer 64-bit address spaces
  and there is currently a 52-bit limit (which exceeds the theoretical
  limit of current OSes and ensures that such lengths can be stored
  exactly in doubles).
- The serialization format has been changed to accommodate longer
  lengths, but vectors of lengths up to 2\^31-1 are stored in the same
  way as before. Longer vectors have their length field set to `-1`
  and followed by two 32-bit fields giving the upper and lower 32-bits
  of the actual length. There is currently a sanity check which limits
  lengths to 2\^48 on unserialization.
- The type `R_xlen_t` is made available to packages in C header
  `Rinternals.h`: this should be fine in C code since C99 is
  required. People do try to use R internals in C++, but C++98
  compilers are not required to support these types.
- Indexing can be done via the use of doubles. The internal indexing
  code used to work with positive integer indices (and negative,
  logical and matrix indices were all converted to positive integers):
  it now works with either `INTSXP` or `REALSXP` indices.
- The R function `length` returns a double value if the length exceeds
  2\^31-1. Code calling `as.integer(length(x))` before passing to
  `.C`/`.Fortran` should checks for an `NA` result.

---

### 12.2 64-bit types

There is also some desire to be able to store larger integers in R,
although the possibility of storing these as `double` is often
overlooked (and e.g. file pointers as returned by `seek` are already
stored as `double`).

Different routes have been proposed:

- Add a new type to R and use that for lengths and indices---most
  likely this would be a 64-bit signed type, say `longint`. R's usual
  implicit coercion rules would ensure that supplying an `integer`
  vector for indexing or `length<-` would work.
- A more radical alternative is to change the existing `integer` type
  to be 64-bit on 64-bit platforms (which was the approach taken by
  S-PLUS for DEC/Compaq Alpha systems). Or even on all platforms.
- Allow either `integer` or `double` values for lengths and indices,
  and return `double` only when necessary.

The third has the advantages of minimal disruption to existing code and
not increasing memory requirements. In the first and third scenarios
both R's own code and user code would have to be adapted for lengths
that were not of type `integer`, and in the third code branches for long
vectors would be tested rarely.

Most users of the `.C` and `.Fortran` interfaces use `as.integer` for
lengths and element numbers, but a few omit these in the knowledge that
these were of type `integer`. It may be reasonable to assume that these
are never intended to be used with long vectors.

The remaining interfaces will need to cope with the changed
`VECTOR_SEXPREC` types. It seems likely that in most cases lengths are
accessed by the `length` and `LENGTH` functions[^27^](#FOOT27)
The current approach is to keep these returning 32-bit lengths and
introduce 'long' versions `xlength` and `XLENGTH` which return
`R_xlen_t` values.

See also <http://homepage.cs.uiowa.edu/~luke/talks/useR10.pdf>.

---

### 12.3 Large matrices

Matrices are stored as vectors and so were also limited to 2\^31-1
elements. Now longer vectors are allowed on 64-bit platforms, matrices
with more elements are supported provided that each of the dimensions is
no more than 2\^31-1. However, not all applications can be supported.

The main problem is linear algebra done by Fortran code compiled with
32-bit `INTEGER`. Although not guaranteed, it seems that all the
compilers currently used with R on a 64-bit platform allow matrices each
of whose dimensions is less than 2\^31 but with more than 2\^31
elements, and index them correctly, and a substantial part of the
support software (such as BLAS and LAPACK) also work.

There are exceptions: for example some complex LAPACK auxiliary routines
do use a single `INTEGER` index and hence overflow silently and segfault
or give incorrect results. One example is `svd()` on a complex matrix.

Since this is implementation-dependent, it is possible that optimized
BLAS and LAPACK may have further restrictions, although none have yet
been encountered. For matrix algebra on large matrices one almost
certainly wants a machine with a lot of RAM (100s of gigabytes), many
cores and a multi-threaded BLAS.

---

## Function and variable index

---

Jump to:   [**.**](#Function-and-variable-index_vr_symbol-1){.summary-letter}  
[**\_**](#Function-and-variable-index_vr_symbol-2){.summary-letter}
 \
 [**A**](#Function-and-variable-index_vr_letter-A){.summary-letter}  
[**C**](#Function-and-variable-index_vr_letter-C){.summary-letter}  
[**D**](#Function-and-variable-index_vr_letter-D){.summary-letter}  
[**E**](#Function-and-variable-index_vr_letter-E){.summary-letter}  
[**F**](#Function-and-variable-index_vr_letter-F){.summary-letter}  
[**G**](#Function-and-variable-index_vr_letter-G){.summary-letter}  
[**I**](#Function-and-variable-index_vr_letter-I){.summary-letter}  
[**L**](#Function-and-variable-index_vr_letter-L){.summary-letter}  
[**M**](#Function-and-variable-index_vr_letter-M){.summary-letter}  
[**N**](#Function-and-variable-index_vr_letter-N){.summary-letter}  
[**P**](#Function-and-variable-index_vr_letter-P){.summary-letter}  
[**R**](#Function-and-variable-index_vr_letter-R){.summary-letter}  
[**S**](#Function-and-variable-index_vr_letter-S){.summary-letter}  
[**T**](#Function-and-variable-index_vr_letter-T){.summary-letter}  
[**U**](#Function-and-variable-index_vr_letter-U){.summary-letter}  
[**V**](#Function-and-variable-index_vr_letter-V){.summary-letter}  
[**W**](#Function-and-variable-index_vr_letter-W){.summary-letter}

---

Index Entry

Section

---

.

[`.Device`](#index-_002eDevice):

[Base environment](#Base-environment)

[`.Devices`](#index-_002eDevices):

[Base environment](#Base-environment)

[`.Internal`](#index-_002eInternal):

[.Internal vs .Primitive](#g_t_002eInternal-vs-_002ePrimitive)

[`.Last.value`](#index-_002eLast_002evalue):

[Base environment](#Base-environment)

[`.Options`](#index-_002eOptions):

[Base environment](#Base-environment)

[`.Primitive`](#index-_002ePrimitive):

[.Internal vs .Primitive](#g_t_002eInternal-vs-_002ePrimitive)

[`.Random.seed`](#index-_002eRandom_002eseed):

[Global environment](#Global-environment)

[`.SavedPlots`](#index-_002eSavedPlots):

[Global environment](#Global-environment)

[`.Traceback`](#index-_002eTraceback):

[Base environment](#Base-environment)

---

\_

[`_R_CHECK_ALL_NON_ISO_C_`](#index-_005fR_005fCHECK_005fALL_005fNON_005fISO_005fC_005f):

[Tools](#Tools)

[`_R_CHECK_ALWAYS_LOG_VIGNETTE_OUTPUT_`](#index-_005fR_005fCHECK_005fALWAYS_005fLOG_005fVIGNETTE_005fOUTPUT_005f):

[Tools](#Tools)

[`_R_CHECK_ASCII_CODE_`](#index-_005fR_005fCHECK_005fASCII_005fCODE_005f):

[Tools](#Tools)

[`_R_CHECK_ASCII_DATA_`](#index-_005fR_005fCHECK_005fASCII_005fDATA_005f):

[Tools](#Tools)

[`_R_CHECK_AUTOCONF_`](#index-_005fR_005fCHECK_005fAUTOCONF_005f):

[Tools](#Tools)

[`_R_CHECK_BUILD_VIGNETTES_ELAPSED_TIMEOUT_`](#index-_005fR_005fCHECK_005fBUILD_005fVIGNETTES_005fELAPSED_005fTIMEOUT_005f):

[Tools](#Tools)

[`_R_CHECK_BUILD_VIGNETTES_SEPARATELY_`](#index-_005fR_005fCHECK_005fBUILD_005fVIGNETTES_005fSEPARATELY_005f):

[Tools](#Tools)

[`_R_CHECK_CLEAN_VIGN_TEST_`](#index-_005fR_005fCHECK_005fCLEAN_005fVIGN_005fTEST_005f):

[Tools](#Tools)

[`_R_CHECK_CODETOOLS_PROFILE_`](#index-_005fR_005fCHECK_005fCODETOOLS_005fPROFILE_005f):

[Tools](#Tools)

[`_R_CHECK_CODE_ASSIGN_TO_GLOBALENV_`](#index-_005fR_005fCHECK_005fCODE_005fASSIGN_005fTO_005fGLOBALENV_005f):

[Tools](#Tools)

[`_R_CHECK_CODE_ATTACH_`](#index-_005fR_005fCHECK_005fCODE_005fATTACH_005f):

[Tools](#Tools)

[`_R_CHECK_CODE_DATA_INTO_GLOBALENV_`](#index-_005fR_005fCHECK_005fCODE_005fDATA_005fINTO_005fGLOBALENV_005f):

[Tools](#Tools)

[`_R_CHECK_CODE_USAGE_VIA_NAMESPACES_`](#index-_005fR_005fCHECK_005fCODE_005fUSAGE_005fVIA_005fNAMESPACES_005f):

[Tools](#Tools)

[`_R_CHECK_CODE_USAGE_WITH_ONLY_BASE_ATTACHED_`](#index-_005fR_005fCHECK_005fCODE_005fUSAGE_005fWITH_005fONLY_005fBASE_005fATTACHED_005f):

[Tools](#Tools)

[`_R_CHECK_CODOC_S4_METHODS_`](#index-_005fR_005fCHECK_005fCODOC_005fS4_005fMETHODS_005f):

[Tools](#Tools)

[`_R_CHECK_COMPACT_DATA_`](#index-_005fR_005fCHECK_005fCOMPACT_005fDATA_005f):

[Tools](#Tools)

[`_R_CHECK_COMPILATION_FLAGS_`](#index-_005fR_005fCHECK_005fCOMPILATION_005fFLAGS_005f):

[Tools](#Tools)

[`_R_CHECK_CONNECTIONS_LEFT_OPEN_`](#index-_005fR_005fCHECK_005fCONNECTIONS_005fLEFT_005fOPEN_005f):

[Tools](#Tools)

[`_R_CHECK_CRAN_INCOMING_`](#index-_005fR_005fCHECK_005fCRAN_005fINCOMING_005f):

[Tools](#Tools)

[`_R_CHECK_CRAN_INCOMING_REMOTE_`](#index-_005fR_005fCHECK_005fCRAN_005fINCOMING_005fREMOTE_005f):

[Tools](#Tools)

[`_R_CHECK_DEPENDS_ONLY_`](#index-_005fR_005fCHECK_005fDEPENDS_005fONLY_005f):

[Tools](#Tools)

[`_R_CHECK_DEPRECATED_DEFUNCT_`](#index-_005fR_005fCHECK_005fDEPRECATED_005fDEFUNCT_005f):

[Tools](#Tools)

[`_R_CHECK_DOC_SIZES2_`](#index-_005fR_005fCHECK_005fDOC_005fSIZES2_005f):

[Tools](#Tools)

[`_R_CHECK_DOC_SIZES_`](#index-_005fR_005fCHECK_005fDOC_005fSIZES_005f):

[Tools](#Tools)

[`_R_CHECK_DOT_FIRSTLIB_`](#index-_005fR_005fCHECK_005fDOT_005fFIRSTLIB_005f):

[Tools](#Tools)

[`_R_CHECK_DOT_INTERNAL_`](#index-_005fR_005fCHECK_005fDOT_005fINTERNAL_005f):

[Tools](#Tools)

[`_R_CHECK_ELAPSED_TIMEOUT_`](#index-_005fR_005fCHECK_005fELAPSED_005fTIMEOUT_005f):

[Tools](#Tools)

[`_R_CHECK_EXAMPLES_ELAPSED_TIMEOUT_`](#index-_005fR_005fCHECK_005fEXAMPLES_005fELAPSED_005fTIMEOUT_005f):

[Tools](#Tools)

[`_R_CHECK_EXAMPLE_TIMING_CPU_TO_ELAPSED_THRESHOLD_`](#index-_005fR_005fCHECK_005fEXAMPLE_005fTIMING_005fCPU_005fTO_005fELAPSED_005fTHRESHOLD_005f):

[Tools](#Tools)

[`_R_CHECK_EXAMPLE_TIMING_THRESHOLD_`](#index-_005fR_005fCHECK_005fEXAMPLE_005fTIMING_005fTHRESHOLD_005f):

[Tools](#Tools)

[`_R_CHECK_EXECUTABLES_`](#index-_005fR_005fCHECK_005fEXECUTABLES_005f):

[Tools](#Tools)

[`_R_CHECK_EXECUTABLES_EXCLUSIONS_`](#index-_005fR_005fCHECK_005fEXECUTABLES_005fEXCLUSIONS_005f):

[Tools](#Tools)

[`_R_CHECK_EXIT_ON_FIRST_ERROR_`](#index-_005fR_005fCHECK_005fEXIT_005fON_005fFIRST_005fERROR_005f):

[Tools](#Tools)

[`_R_CHECK_FF_CALLS_`](#index-_005fR_005fCHECK_005fFF_005fCALLS_005f):

[Tools](#Tools)

[`_R_CHECK_FF_DUP_`](#index-_005fR_005fCHECK_005fFF_005fDUP_005f):

[Tools](#Tools)

[`_R_CHECK_FORCE_SUGGESTS_`](#index-_005fR_005fCHECK_005fFORCE_005fSUGGESTS_005f):

[Tools](#Tools)

[`_R_CHECK_FUTURE_FILE_TIMESTAMPS_`](#index-_005fR_005fCHECK_005fFUTURE_005fFILE_005fTIMESTAMPS_005f):

[Tools](#Tools)

[`_R_CHECK_GCT_N_`](#index-_005fR_005fCHECK_005fGCT_005fN_005f):

[Tools](#Tools)

[`_R_CHECK_INSTALL_DEPENDS_`](#index-_005fR_005fCHECK_005fINSTALL_005fDEPENDS_005f):

[Tools](#Tools)

[`_R_CHECK_INSTALL_ELAPSED_TIMEOUT_`](#index-_005fR_005fCHECK_005fINSTALL_005fELAPSED_005fTIMEOUT_005f):

[Tools](#Tools)

[`_R_CHECK_LENGTH_1_CONDITION_`](#index-_005fR_005fCHECK_005fLENGTH_005f1_005fCONDITION_005f):

[Tools](#Tools)

[`_R_CHECK_LENGTH_1_LOGIC2_`](#index-_005fR_005fCHECK_005fLENGTH_005f1_005fLOGIC2_005f):

[Tools](#Tools)

[`_R_CHECK_LICENSE_`](#index-_005fR_005fCHECK_005fLICENSE_005f):

[Tools](#Tools)

[`_R_CHECK_LIMIT_CORES_`](#index-_005fR_005fCHECK_005fLIMIT_005fCORES_005f):

[Tools](#Tools)

[`_R_CHECK_NATIVE_ROUTINE_REGISTRATION_`](#index-_005fR_005fCHECK_005fNATIVE_005fROUTINE_005fREGISTRATION_005f):

[Tools](#Tools)

[`_R_CHECK_NO_RECOMMENDED_`](#index-_005fR_005fCHECK_005fNO_005fRECOMMENDED_005f):

[Tools](#Tools)

[`_R_CHECK_NO_STOP_ON_TEST_ERROR_`](#index-_005fR_005fCHECK_005fNO_005fSTOP_005fON_005fTEST_005fERROR_005f):

[Tools](#Tools)

[`_R_CHECK_ONE_TEST_ELAPSED_TIMEOUT_`](#index-_005fR_005fCHECK_005fONE_005fTEST_005fELAPSED_005fTIMEOUT_005f):

[Tools](#Tools)

[`_R_CHECK_ONE_VIGNETTE_ELAPSED_TIMEOUT_`](#index-_005fR_005fCHECK_005fONE_005fVIGNETTE_005fELAPSED_005fTIMEOUT_005f):

[Tools](#Tools)

[`_R_CHECK_OVERWRITE_REGISTERED_S3_METHODS_`](#index-_005fR_005fCHECK_005fOVERWRITE_005fREGISTERED_005fS3_005fMETHODS_005f):

[Tools](#Tools)

[`_R_CHECK_PACKAGES_USED_IN_TESTS_USE_SUBDIRS_`](#index-_005fR_005fCHECK_005fPACKAGES_005fUSED_005fIN_005fTESTS_005fUSE_005fSUBDIRS_005f):

[Tools](#Tools)

[`_R_CHECK_PERMISSIONS_`](#index-_005fR_005fCHECK_005fPERMISSIONS_005f):

[Tools](#Tools)

[`_R_CHECK_PKGMAN_ELAPSED_TIMEOUT_`](#index-_005fR_005fCHECK_005fPKGMAN_005fELAPSED_005fTIMEOUT_005f):

[Tools](#Tools)

[`_R_CHECK_PKG_SIZES_`](#index-_005fR_005fCHECK_005fPKG_005fSIZES_005f):

[Tools](#Tools)

[`_R_CHECK_PKG_SIZES_THRESHOLD_`](#index-_005fR_005fCHECK_005fPKG_005fSIZES_005fTHRESHOLD_005f):

[Tools](#Tools)

[`_R_CHECK_PRAGMAS_`](#index-_005fR_005fCHECK_005fPRAGMAS_005f):

[Tools](#Tools)

[`_R_CHECK_RD_CHECKRD_MINLEVEL_`](#index-_005fR_005fCHECK_005fRD_005fCHECKRD_005fMINLEVEL_005f):

[Tools](#Tools)

[`_R_CHECK_RD_CONTENTS_`](#index-_005fR_005fCHECK_005fRD_005fCONTENTS_005f):

[Tools](#Tools)

[`_R_CHECK_RD_EXAMPLES_T_AND_F_`](#index-_005fR_005fCHECK_005fRD_005fEXAMPLES_005fT_005fAND_005fF_005f):

[Tools](#Tools)

[`_R_CHECK_RD_LINE_WIDTHS_`](#index-_005fR_005fCHECK_005fRD_005fLINE_005fWIDTHS_005f):

[Tools](#Tools)

[`_R_CHECK_RD_STYLE_`](#index-_005fR_005fCHECK_005fRD_005fSTYLE_005f):

[Tools](#Tools)

[`_R_CHECK_RD_XREFS_`](#index-_005fR_005fCHECK_005fRD_005fXREFS_005f):

[Tools](#Tools)

[`_R_CHECK_REPLACING_IMPORTS_`](#index-_005fR_005fCHECK_005fREPLACING_005fIMPORTS_005f):

[Tools](#Tools)

[`_R_CHECK_R_DEPENDS_`](#index-_005fR_005fCHECK_005fR_005fDEPENDS_005f):

[Tools](#Tools)

[`_R_CHECK_R_ON_PATH_`](#index-_005fR_005fCHECK_005fR_005fON_005fPATH_005f):

[Tools](#Tools)

[`_R_CHECK_S3_METHODS_NOT_REGISTERED_`](#index-_005fR_005fCHECK_005fS3_005fMETHODS_005fNOT_005fREGISTERED_005f):

[Tools](#Tools)

[`_R_CHECK_SCREEN_DEVICE_`](#index-_005fR_005fCHECK_005fSCREEN_005fDEVICE_005f):

[Tools](#Tools)

[`_R_CHECK_SERIALIZATION_`](#index-_005fR_005fCHECK_005fSERIALIZATION_005f):

[Tools](#Tools)

[`_R_CHECK_SHLIB_OPENMP_FLAGS_`](#index-_005fR_005fCHECK_005fSHLIB_005fOPENMP_005fFLAGS_005f):

[Tools](#Tools)

[`_R_CHECK_SKIP_ARCH_`](#index-_005fR_005fCHECK_005fSKIP_005fARCH_005f):

[Tools](#Tools)

[`_R_CHECK_SKIP_EXAMPLES_ARCH_`](#index-_005fR_005fCHECK_005fSKIP_005fEXAMPLES_005fARCH_005f):

[Tools](#Tools)

[`_R_CHECK_SKIP_TESTS_ARCH_`](#index-_005fR_005fCHECK_005fSKIP_005fTESTS_005fARCH_005f):

[Tools](#Tools)

[`_R_CHECK_SRC_MINUS_W_IMPLICIT_`](#index-_005fR_005fCHECK_005fSRC_005fMINUS_005fW_005fIMPLICIT_005f):

[Tools](#Tools)

[`_R_CHECK_SRC_MINUS_W_UNUSED_`](#index-_005fR_005fCHECK_005fSRC_005fMINUS_005fW_005fUNUSED_005f):

[Tools](#Tools)

[`_R_CHECK_SUBDIRS_NOCASE_`](#index-_005fR_005fCHECK_005fSUBDIRS_005fNOCASE_005f):

[Tools](#Tools)

[`_R_CHECK_SUBDIRS_STRICT_`](#index-_005fR_005fCHECK_005fSUBDIRS_005fSTRICT_005f):

[Tools](#Tools)

[`_R_CHECK_SUGGESTS_ONLY_`](#index-_005fR_005fCHECK_005fSUGGESTS_005fONLY_005f):

[Tools](#Tools)

[`_R_CHECK_SYSTEM_CLOCK_`](#index-_005fR_005fCHECK_005fSYSTEM_005fCLOCK_005f):

[Tools](#Tools)

[`_R_CHECK_TESTS_ELAPSED_TIMEOUT_`](#index-_005fR_005fCHECK_005fTESTS_005fELAPSED_005fTIMEOUT_005f):

[Tools](#Tools)

[`_R_CHECK_TESTS_NLINES_`](#index-_005fR_005fCHECK_005fTESTS_005fNLINES_005f):

[Tools](#Tools)

[`_R_CHECK_TEST_TIMING_CPU_TO_ELAPSED_THRESHOLD_`](#index-_005fR_005fCHECK_005fTEST_005fTIMING_005fCPU_005fTO_005fELAPSED_005fTHRESHOLD_005f):

[Tools](#Tools)

[`_R_CHECK_THINGS_IN_TEMP_DIR_`](#index-_005fR_005fCHECK_005fTHINGS_005fIN_005fTEMP_005fDIR_005f):

[Tools](#Tools)

[`_R_CHECK_TIMINGS_`](#index-_005fR_005fCHECK_005fTIMINGS_005f):

[Tools](#Tools)

[`_R_CHECK_TOPLEVEL_FILES_`](#index-_005fR_005fCHECK_005fTOPLEVEL_005fFILES_005f):

[Tools](#Tools)

[`_R_CHECK_UNSAFE_CALLS_`](#index-_005fR_005fCHECK_005fUNSAFE_005fCALLS_005f):

[Tools](#Tools)

[`_R_CHECK_USE_CODETOOLS_`](#index-_005fR_005fCHECK_005fUSE_005fCODETOOLS_005f):

[Tools](#Tools)

[`_R_CHECK_USE_INSTALL_LOG_`](#index-_005fR_005fCHECK_005fUSE_005fINSTALL_005fLOG_005f):

[Tools](#Tools)

[`_R_CHECK_VC_DIRS_`](#index-_005fR_005fCHECK_005fVC_005fDIRS_005f):

[Tools](#Tools)

[`_R_CHECK_VIGNETTES_NLINES_`](#index-_005fR_005fCHECK_005fVIGNETTES_005fNLINES_005f):

[Tools](#Tools)

[`_R_CHECK_VIGNETTE_TIMING_CPU_TO_ELAPSED_THRESHOLD_`](#index-_005fR_005fCHECK_005fVIGNETTE_005fTIMING_005fCPU_005fTO_005fELAPSED_005fTHRESHOLD_005f):

[Tools](#Tools)

[`_R_CHECK_WALL_FORTRAN_`](#index-_005fR_005fCHECK_005fWALL_005fFORTRAN_005f):

[Tools](#Tools)

[`_R_CHECK_WINDOWS_DEVICE_`](#index-_005fR_005fCHECK_005fWINDOWS_005fDEVICE_005f):

[Tools](#Tools)

[`_R_CHECK_XREFS_REPOSITORIES_`](#index-_005fR_005fCHECK_005fXREFS_005fREPOSITORIES_005f):

[Tools](#Tools)

[`_R_CHECK_XREFS_USE_ALIASES_FROM_CRAN_`](#index-_005fR_005fCHECK_005fXREFS_005fUSE_005fALIASES_005fFROM_005fCRAN_005f):

[Tools](#Tools)

[`_R_SHLIB_BUILD_OBJECTS_SYMBOL_TABLES_`](#index-_005fR_005fSHLIB_005fBUILD_005fOBJECTS_005fSYMBOL_005fTABLES_005f):

[Tools](#Tools)

---

A

[`alloca`](#index-alloca):

[Memory allocators](#Memory-allocators)

[`ARGSUSED`](#index-ARGSUSED):

[Rest of header](#Rest-of-header)

[`ATTRIB`](#index-ATTRIB):

[Attributes](#Attributes)

[`attribute_hidden`](#index-attribute_005fhidden):

[Hiding C entry points](#Hiding-C-entry-points)

---

C

[`Calloc`](#index-Calloc):

[Memory allocators](#Memory-allocators)

[`copyMostAttrib`](#index-copyMostAttrib):

[Attributes](#Attributes)

---

D

[`DDVAL`](#index-DDVAL):

[Rest of header](#Rest-of-header)

[`debug bit`](#index-debug-bit):

[Rest of header](#Rest-of-header)

[`DispatchGeneric`](#index-DispatchGeneric):

[Argument evaluation](#Argument-evaluation)

[`DispatchOrEval`](#index-DispatchOrEval):

[Argument evaluation](#Argument-evaluation)

[`dump.frames`](#index-dump_002eframes):

[Global environment](#Global-environment)

[`DUPLICATE_ATTRIB`](#index-DUPLICATE_005fATTRIB):

[Attributes](#Attributes)

---

E

[`emacs`](#index-emacs):

[R coding standards](#R-coding-standards)

[`error`](#index-error):

[Warnings and errors](#Warnings-and-errors)

[`errorcall`](#index-errorcall):

[Warnings and errors](#Warnings-and-errors)

---

F

[`Free`](#index-Free):

[Memory allocators](#Memory-allocators)

---

G

[`gp bits`](#index-gp-bits):

[Rest of header](#Rest-of-header)

---

I

[`invisible`](#index-invisible):

[Autoprinting](#Autoprinting)

---

L

[`last.warning`](#index-last_002ewarning):

[Base environment](#Base-environment)

[`LEVELS`](#index-LEVELS):

[Rest of header](#Rest-of-header)

---

M

[`make`](#index-make):

[R coding standards](#R-coding-standards)

[`makeinfo`](#index-makeinfo):

[R coding standards](#R-coding-standards)

[`MISSING`](#index-MISSING):

[Rest of header](#Rest-of-header)

[`MISSING`](#index-MISSING-1):

[Missingness](#Missingness)

[`mkChar`](#index-mkChar):

[The CHARSXP cache](#The-CHARSXP-cache)

[`mkCharLenCE`](#index-mkCharLenCE):

[The CHARSXP cache](#The-CHARSXP-cache)

---

N

[`NAMED`](#index-NAMED):

[Rest of header](#Rest-of-header)

[`NAMED`](#index-NAMED-1):

[Argument evaluation](#Argument-evaluation)

[`NAMED`](#index-NAMED-2):

[.Internal vs .Primitive](#g_t_002eInternal-vs-_002ePrimitive)

[`named bits`](#index-named-bits):

[Rest of header](#Rest-of-header)

---

P

[`Perl`](#index-Perl):

[R coding standards](#R-coding-standards)

[`PRIMPRINT`](#index-PRIMPRINT):

[Autoprinting](#Autoprinting)

[`PRSEEN`](#index-PRSEEN):

[Rest of header](#Rest-of-header)

---

R

[`Rdll.hide`](#index-Rdll_002ehide):

[Hiding C entry points](#Hiding-C-entry-points)

[`Realloc`](#index-Realloc):

[Memory allocators](#Memory-allocators)

[`R_alloc`](#index-R_005falloc):

[Memory allocators](#Memory-allocators)

[`R_AllocStringBuffer`](#index-R_005fAllocStringBuffer):

[Memory allocators](#Memory-allocators)

[`R_BaseNamespace`](#index-R_005fBaseNamespace):

[Namespaces](#Namespaces)

[`R_CheckStack`](#index-R_005fCheckStack):

[Memory allocators](#Memory-allocators)

[`R_CheckStack2`](#index-R_005fCheckStack2):

[Memory allocators](#Memory-allocators)

[`R_FreeStringBuffer`](#index-R_005fFreeStringBuffer):

[Memory allocators](#Memory-allocators)

[`R_FreeStringBufferL`](#index-R_005fFreeStringBufferL):

[Memory allocators](#Memory-allocators)

[`R_MissingArg`](#index-R_005fMissingArg):

[Missingness](#Missingness)

[`R_Visible`](#index-R_005fVisible):

[Autoprinting](#Autoprinting)

---

S

[`SETLEVELS`](#index-SETLEVELS):

[Rest of header](#Rest-of-header)

[`SET_ARGUSED`](#index-SET_005fARGUSED):

[Rest of header](#Rest-of-header)

[`SET_ATTRIB`](#index-SET_005fATTRIB):

[Attributes](#Attributes)

[`SET_DDVAL`](#index-SET_005fDDVAL):

[Rest of header](#Rest-of-header)

[`SET_MISSING`](#index-SET_005fMISSING):

[Rest of header](#Rest-of-header)

[`SET_NAMED`](#index-SET_005fNAMED):

[Rest of header](#Rest-of-header)

[`spare bit`](#index-spare-bit):

[Rest of header](#Rest-of-header)

---

T

[`trace bit`](#index-trace-bit):

[Rest of header](#Rest-of-header)

---

U

[`UseMethod`](#index-UseMethod):

[Contexts](#Contexts)

---

V

[`vmaxget`](#index-vmaxget):

[Memory allocators](#Memory-allocators)

[`vmaxset`](#index-vmaxset):

[Memory allocators](#Memory-allocators)

---

W

[`warning`](#index-warning):

[Warnings and errors](#Warnings-and-errors)

[`warningcall`](#index-warningcall):

[Warnings and errors](#Warnings-and-errors)

---

---

Jump to:   [**.**](#Function-and-variable-index_vr_symbol-1){.summary-letter}  
[**\_**](#Function-and-variable-index_vr_symbol-2){.summary-letter}
 \
 [**A**](#Function-and-variable-index_vr_letter-A){.summary-letter}  
[**C**](#Function-and-variable-index_vr_letter-C){.summary-letter}  
[**D**](#Function-and-variable-index_vr_letter-D){.summary-letter}  
[**E**](#Function-and-variable-index_vr_letter-E){.summary-letter}  
[**F**](#Function-and-variable-index_vr_letter-F){.summary-letter}  
[**G**](#Function-and-variable-index_vr_letter-G){.summary-letter}  
[**I**](#Function-and-variable-index_vr_letter-I){.summary-letter}  
[**L**](#Function-and-variable-index_vr_letter-L){.summary-letter}  
[**M**](#Function-and-variable-index_vr_letter-M){.summary-letter}  
[**N**](#Function-and-variable-index_vr_letter-N){.summary-letter}  
[**P**](#Function-and-variable-index_vr_letter-P){.summary-letter}  
[**R**](#Function-and-variable-index_vr_letter-R){.summary-letter}  
[**S**](#Function-and-variable-index_vr_letter-S){.summary-letter}  
[**T**](#Function-and-variable-index_vr_letter-T){.summary-letter}  
[**U**](#Function-and-variable-index_vr_letter-U){.summary-letter}  
[**V**](#Function-and-variable-index_vr_letter-V){.summary-letter}  
[**W**](#Function-and-variable-index_vr_letter-W){.summary-letter}

---

---

## Concept index

---

Jump to:   [**.**](#Concept-index_cp_symbol-1){.summary-letter}
 \
 [**A**](#Concept-index_cp_letter-A){.summary-letter}  
[**B**](#Concept-index_cp_letter-B){.summary-letter}  
[**C**](#Concept-index_cp_letter-C){.summary-letter}  
[**E**](#Concept-index_cp_letter-E){.summary-letter}  
[**F**](#Concept-index_cp_letter-F){.summary-letter}  
[**G**](#Concept-index_cp_letter-G){.summary-letter}  
[**L**](#Concept-index_cp_letter-L){.summary-letter}  
[**M**](#Concept-index_cp_letter-M){.summary-letter}  
[**N**](#Concept-index_cp_letter-N){.summary-letter}  
[**P**](#Concept-index_cp_letter-P){.summary-letter}  
[**S**](#Concept-index_cp_letter-S){.summary-letter}  
[**U**](#Concept-index_cp_letter-U){.summary-letter}  
[**V**](#Concept-index_cp_letter-V){.summary-letter}  
[**W**](#Concept-index_cp_letter-W){.summary-letter}

---

Index Entry

Section

---

.

[\... argument](#index-_002e_002e_002e-argument):

[Rest of header](#Rest-of-header)

[\... argument](#index-_002e_002e_002e-argument-1):

[Dot-dot-dot arguments](#Dot_002ddot_002ddot-arguments)

[.Internal function](#index-_002eInternal-function):

[Argument evaluation](#Argument-evaluation)

---

A

[allocation classes](#index-allocation-classes):

[Allocation classes](#Allocation-classes)

[argument evaluation](#index-argument-evaluation):

[Argument evaluation](#Argument-evaluation)

[argument list](#index-argument-list):

[SEXPTYPEs](#SEXPTYPEs)

[atomic vector type](#index-atomic-vector-type):

[SEXPTYPEs](#SEXPTYPEs)

[attributes](#index-attributes):

[Attributes](#Attributes)

[attributes, preserving](#index-attributes_002c-preserving):

[Attributes](#Attributes)

[autoprinting](#index-autoprinting):

[Autoprinting](#Autoprinting)

---

B

[base environment](#index-base-environment):

[Environments and variable lookup](#Environments-and-variable-lookup)

[base environment](#index-base-environment-1):

[Base environment](#Base-environment)

[base namespace](#index-base-namespace):

[Namespaces](#Namespaces)

[builtin function](#index-builtin-function):

[Argument evaluation](#Argument-evaluation)

---

C

[coding standards](#index-coding-standards):

[R coding standards](#R-coding-standards)

[context](#index-context):

[Contexts](#Contexts)

[copying semantics](#index-copying-semantics):

[Rest of header](#Rest-of-header)

[copying semantics](#index-copying-semantics-1):

[Attributes](#Attributes)

---

E

[environment](#index-environment):

[Environments and variable lookup](#Environments-and-variable-lookup)

[environment, base](#index-environment_002c-base):

[Environments and variable lookup](#Environments-and-variable-lookup)

[environment, base](#index-environment_002c-base-1):

[Base environment](#Base-environment)

[environment, global](#index-environment_002c-global):

[Global environment](#Global-environment)

[expression](#index-expression):

[SEXPTYPEs](#SEXPTYPEs)

---

F

[function](#index-function):

[SEXPTYPEs](#SEXPTYPEs)

---

G

[garbage collector](#index-garbage-collector):

[The write barrier](#The-write-barrier)

[generic, generic](#index-generic_002c-generic):

[Argument evaluation](#Argument-evaluation)

[generic, internal](#index-generic_002c-internal):

[Argument evaluation](#Argument-evaluation)

[global environment](#index-global-environment):

[Global environment](#Global-environment)

---

L

[language object](#index-language-object):

[SEXPTYPEs](#SEXPTYPEs)

---

M

[method dispatch](#index-method-dispatch):

[Contexts](#Contexts)

[missingness](#index-missingness):

[Missingness](#Missingness)

[modules](#index-modules):

[Modules](#Modules)

---

N

[namespace](#index-namespace):

[Namespaces](#Namespaces)

[namespace, base](#index-namespace_002c-base):

[Namespaces](#Namespaces)

[node](#index-node):

[SEXPs](#SEXPs)

---

P

[preserving attributes](#index-preserving-attributes):

[Attributes](#Attributes)

[primitive function](#index-primitive-function):

[Argument evaluation](#Argument-evaluation)

[promise](#index-promise):

[Rest of header](#Rest-of-header)

---

S

[S4 type](#index-S4-type):

[SEXPTYPEs](#SEXPTYPEs)

[search path](#index-search-path):

[Search paths](#Search-paths)

[serialization](#index-serialization):

[Serialization Formats](#Serialization-Formats)

[SEXP](#index-SEXP):

[SEXPs](#SEXPs)

[SEXPRREC](#index-SEXPRREC):

[SEXPs](#SEXPs)

[SEXPTYPE](#index-SEXPTYPE):

[SEXPTYPEs](#SEXPTYPEs)

[SEXPTYPE table](#index-SEXPTYPE-table):

[SEXPTYPEs](#SEXPTYPEs)

[special function](#index-special-function):

[Argument evaluation](#Argument-evaluation)

---

U

[user databases](#index-user-databases):

[Environments and variable lookup](#Environments-and-variable-lookup)

---

V

[variable lookup](#index-variable-lookup):

[Environments and variable lookup](#Environments-and-variable-lookup)

[vector type](#index-vector-type):

[The \'data\'](#The-_0027data_0027)

[visibility](#index-visibility):

[Visibility](#Visibility)

---

W

[write barrier](#index-write-barrier):

[The write barrier](#The-write-barrier)

---

---

Jump to:   [**.**](#Concept-index_cp_symbol-1){.summary-letter}
 \
 [**A**](#Concept-index_cp_letter-A){.summary-letter}  
[**B**](#Concept-index_cp_letter-B){.summary-letter}  
[**C**](#Concept-index_cp_letter-C){.summary-letter}  
[**E**](#Concept-index_cp_letter-E){.summary-letter}  
[**F**](#Concept-index_cp_letter-F){.summary-letter}  
[**G**](#Concept-index_cp_letter-G){.summary-letter}  
[**L**](#Concept-index_cp_letter-L){.summary-letter}  
[**M**](#Concept-index_cp_letter-M){.summary-letter}  
[**N**](#Concept-index_cp_letter-N){.summary-letter}  
[**P**](#Concept-index_cp_letter-P){.summary-letter}  
[**S**](#Concept-index_cp_letter-S){.summary-letter}  
[**U**](#Concept-index_cp_letter-U){.summary-letter}  
[**V**](#Concept-index_cp_letter-V){.summary-letter}  
[**W**](#Concept-index_cp_letter-W){.summary-letter}

---

---

#### Footnotes

[(1)](#DOCF1)

strictly, a `SEXPREC` node; `VECTOR_SEXPREC` nodes are slightly smaller
but followed by data in the node.

[(2)](#DOCF2)

a pointer to a function or a symbol to look up the function by name, or
a language object to be evaluated to give a function.

[(3)](#DOCF3)

This is almost unused. The only current use is for hash tables of
environments (`VECSXP`s), where `length` is the size of the table and
`truelength` is the number of primary slots in use, and for the
reference hash tables in serialization (`VECSXP`s), where `truelength`
is the number of slots in use.

[(4)](#DOCF4)

Remember that attaching a list or a saved image actually creates and
populates an environment and attaches that.

[(5)](#DOCF5)

There is currently one other difference: when profiling builtin
functions are counted as function calls but specials are not.

[(6)](#DOCF6)

the other current example is left brace, which is implemented as a
primitive.

[(7)](#DOCF7)

only bits 0:4 are currently used for `SEXPTYPE`s but values 241:255 are
used for pseudo-`SEXPTYPE`s.

[(8)](#DOCF8)

Currently the only relevant bits are 0:1, 4, 14:15.

[(9)](#DOCF9)

See define `USE_UTF8_IF_POSSIBLE` in file `src/main/gram.c`.

[(10)](#DOCF10)

or UTF-16 if support for surrogates is enabled in the OS, which it used
not to be when encoding support was added to R.

[(11)](#DOCF11)

but not the GraphApp toolkit.

[(12)](#DOCF12)

This can also create non-S4 objects, as in `new("integer")`.

[(13)](#DOCF13)

although this is not recommended as it is less future-proof.

[(14)](#DOCF14)

but apparently not on Windows.

[(15)](#DOCF15)

The C code is in files `base.c`, `graphics.c`,
`par.c`, `plot.c` and `plot3d.c` in directory
`src/main`.

[(16)](#DOCF16)

although that needs to be handled carefully, as for example the `circle`
callback is given a radius (and that should be interpreted as in the x
units).

[(17)](#DOCF17)

It is possible for the device to find the `GEDevDesc` which points to
its `DevDesc`, and this is done often enough that there is a convenience
function `desc2GEDesc` to do so.

[(18)](#DOCF18)

Calling `R_CheckDeviceAvailable()` ensures there is a free slot or
throws an error.

[(19)](#DOCF19)

in device coordinates

[(20)](#DOCF20)

It is technically possible to use alpha-blending on metafile devices
such as printers, but it seems few drivers have support for this.

[(21)](#DOCF21)

an Xcode project, in SVN at
<https://svn.r-project.org/R-packages/trunk/Mac-GUI>.

[(22)](#DOCF22)

under Windows, junction points, or copies if environment variable
`R_WIN_NO_JUNCTIONS` has a non-empty value.

[(23)](#DOCF23)

see the previous footnote.

[(24)](#DOCF24)

The usual culprits are calls to compiled code _via_ `.Call` or
`.External` which alter their arguments.

[(25)](#DOCF25)

things which the byte compiler assumes do not change, e.g. function
bodies.

[(26)](#DOCF26)

Linux distributions tend to unbundle `texinfo.tex` from
'`texinfo`'.

[(27)](#DOCF27)

but `LENGTH` is a macro under some internal uses.

---
