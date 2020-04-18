# 8 Choosing between 32- and 64-bit builds

---

Almost all current CPUs have both 32- and 64-bit sets of instructions.
Most OSes running on such CPUs offer the choice of building a 32-bit or
a 64-bit version of R (and details are given below under specific OSes).
For most a 32-bit version is the default, but for some (e.g.,
'`x86_64`' Linux and macOS ≥ 10.6) 64-bit is.

All current versions of R use 32-bit integers (this is enforced in the
build) and ISO/IEC 60559[^37^](#FOOT37) double-precision reals,
and so compute to the same precision[^38^](#FOOT38) and with
the same limits on the sizes of numerical quantities. The principal
difference is in the size of the pointers.

64-bit builds have both advantages and disadvantages:

- The total virtual memory space made available to a 32-bit process is
  limited by the pointer size to 4GB, and on most OSes to 3GB (or even
  2GB). The limits for 64-bit processes are much larger (e.g.
  8--128TB).

  R allocates memory for large objects as needed, and removes any
  unused ones at garbage collection. When the sizes of objects become
  an appreciable fraction of the address limit, fragmentation of the
  address space becomes an issue and there may be no hole available
  that is the size requested. This can cause more frequent garbage
  collection or the inability to allocate large objects. As a guide,
  this will become an issue for 32-bit builds with objects more than
  10% of the size of the address space (around 300Mb) or when the
  total size of objects in use is around one third (around 1Gb).

- Only 64-bit builds support 'long vectors', those with _2\^{31}_ or
  more elements (which needs at least 16GB of storage for each numeric
  vector).

- Most 32-bit OSes by default limit file sizes to 2GB (and this may
  also apply to 32-bit builds on 64-bit OSes). This can often be
  worked around: `configure` selects suitable defines if this is
  possible. (We have also largely worked around that limit on 32-bit
  Windows.) 64-bit builds have much larger limits.

- Because the pointers are larger, R's basic structures are larger.
  This means that R objects take more space and (usually) more time to
  manipulate. So 64-bit builds of R will, all other things being
  equal, run slower than 32-bit builds. (On Sparc Solaris the
  difference was 15-20%.)

- However, 'other things' may not be equal. In the specific case of
  '`x86_64`' _vs_ '`ix86`', the 64-bit CPU has
  features (such as SSE2 instructions) which are guaranteed to be
  present but are optional on the 32-bit CPU, and also has more
  general-purpose registers. This means that on chips like a desktop
  Intel i7 the vanilla 64-bit version of R has been around 10% faster
  on both Linux and macOS. (Laptop CPUs are usually relatively slower
  in 64-bit mode.)

So, for speed you may want to use a 32-bit build (especially on a
laptop), but to handle large datasets (and perhaps large files) a 64-bit
build. You can often build both and install them in the same place: See
[Sub-architectures](#Sub_002darchitectures). (This is done for the
Windows binary distributions.)

Even on 64-bit builds of R there are limits on the size of R objects
(see `help("Memory-limits")`), some of which stem from the use of 32-bit
integers (especially in Fortran code). For example, each dimension of an
array is limited to _2\^{31} - 1_.

---
