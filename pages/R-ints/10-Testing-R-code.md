10 Testing R code

---

When you (as R developer) add new functions to the R base (all the
packages distributed with R), be careful to check if [make
test-Specific]{.kbd} or particularly, [cd tests; make
no-segfault.Rout]{.kbd} still works (without interactive user
intervention, and on a standalone computer). If the new function, for
example, accesses the Internet, or requires GUI interaction, please add
its name to the "stop list" in `tests/no-segfault.Rin`.

\[To be revised: use `make check-devel`, check the write barrier if you
change internal structures.\]

---
