# 7 Internationalization and Localization

---

_Internationalization_ refers to the process of enabling support for
many human languages, and _localization_ to adapting to a specific
country and language.

Current builds of R support all the character sets that the underlying
OS can handle. These are interpreted according to the
current `locale`, a sufficiently complicated topic to merit a separate
section. Note though that R has no built-in support for right-to-left
languages and bidirectional output, relying on the OS services. For
example, how character vectors in UTF-8 containing both English digits
and Hebrew characters are printed is OS-dependent (and perhaps
locale-dependent).

The other aspect of the internationalization is support for the
translation of messages. This is enabled in almost all builds of R.

---

• [Locales](#Locales)     
 • [Localization of messages](#Localization-of-messages)

---

---

### 7.1 Locales

A _locale_ is a description of the local environment of the user,
including the preferred language, the encoding of characters, the
currency used and its conventions, and so on. Aspects of the locale are
accessed by the R functions `Sys.getlocale` and `Sys.localeconv`.

The system of naming locales is OS-specific. There is quite wide
agreement on schemes, but not on the details of their implementation. A
locale needs to specify

- A human language. These are generally specified by a lower-case
  two-character abbreviation following ISO 639 (see e.g.
  <https://en.wikipedia.org/wiki/ISO_639-1>).
- A 'territory', used mainly to specify the currency. These are
  generally specified by an upper-case two-character abbreviation
  following ISO 3166 (see e.g.
  <https://en.wikipedia.org/wiki/ISO_3166>).
- A charset encoding, which determines both how a byte stream should
  be divided into characters, and which characters the subsequences of
  bytes represent. Sometimes the combination of language and territory
  is used to specify the encoding, for example to distinguish between
  traditional and simplified Chinese.
- Optionally, a modifier, for example to indicate that Austria is to
  be considered pre- or post-Euro. The modifier is also used to
  indicate the script (`@latin`, `@cyrillic` for Serbian, `@iqtelif`)
  or language dialect (e.g. `@saaho`, a dialect of Afar, and `@bokmal`
  and `@nynorsk`, dialects of Norwegian regarded by some OSes as
  separate languages, `no` and `nn`).

R is principally concerned with the first (for translations) and third.
Note that the charset may be deducible from the language, as some OSes
offer only one charset per language.

---

• [Locales under Unix-alikes](#Locales-under-Unix_002dalikes)     
 • [Locales under Windows](#Locales-under-Windows)     
 • [Locales under macOS](#Locales-under-macOS)

---

---

#### 7.1.1 Locales under Unix-alikes

Modern Linux uses the XPG[^32^](#FOOT32) locale specifications
which have the form '`en_GB`', '`en_GB.UTF-8`',
'`aa_ER.UTF-8@saaho`', '`de_AT.iso885915@euro`', the
components being in the order listed above. (See `man locale` and
`locale -a` for more details.) Similar schemes are used by most
Unix-alikes: some (including some distributions of Linux) use
'`.utf8`' rather than '`.UTF-8`'.

Note that whereas UTF-8 locales are nowadays almost universally used,
locales such as '`en_GB`' use 8-bit encodings for backwards
compatibility.

---

#### 7.1.2 Locales under Windows

Windows also uses locales, but specified in a rather less concise way.
Most users will encounter locales only via drop-down menus, but more
information and lists can be found by searching for
'`Windows language country strings`').

It offers only one encoding per language.

Some care is needed with Windows' locale names. For example, `chinese`
is Traditional Chinese and not Simplified Chinese as used in most of the
Chinese-speaking world.

---

#### 7.1.3 Locales under macOS

macOS supports locales in its own particular way, but the R GUI tries to
make this easier for users. See
<https://developer.apple.com/library/content/documentation/MacOSX/Conceptual/BPInternational/>
for how users can set their locales. As with Windows, end users will
generally only see lists of languages/territories. Users of R in a
terminal may need to set the locale to something like
'`en_GB.UTF-8`' if it defaults to '`C`' (as it
sometimes does when logging in remotely and for batch jobs: note whether
`Terminal` sets the `LANG` environment variable is an (advanced)
preference, but does so by default).

Internally macOS uses a form similar to Linux: the main difference from
other Unix-alikes is that where a character set is not specified it is
assumed to be `UTF-8`.

---

### 7.2 Localization of messages

The preferred language for messages is by default taken from the locale.
This can be overridden first by the setting of the environment variable

by the
environment variables `LC_ALL`, `LC_MESSAGES` and `LANG`. (The last
three are normally used to set the locale and so should not be needed,
but the first is only used to select the language for messages.) The
code tries hard to map locales to languages, but on some systems
(notably Windows) the locale names needed for the environment variable
`LC_ALL` do not all correspond to XPG language names and so `LANGUAGE`
may need to be set. (One example is '`LC_ALL=es`' on Windows
which sets the locale to Estonian and the language to Spanish.)

It is usually possible to change the language once R is running _via_
(not Windows) `Sys.setlocale("LC_MESSAGES", "new_locale")`, or by
setting an environment variable such as `LANGUAGE`,
_provided_[^34^](#FOOT34) the language you are changing to can
be output in the current character set. But this is OS-specific, and has
been known to stop working on an OS upgrade.

Messages are divided into _domains_, and translations may be available
for some or all messages in a domain. R makes use of the following
domains.

- Domain `R` for the C-level error and warning messages from the R
  interpreter.
- Domain `R-pkg` for the R `stop`, `warning` and `message` messages in
  each package, including `R-base` for the **base** package.
- Domain `pkg` for the C-level messages in each package.
- Domain `RGui` for the menus etc of the R for Windows GUI front-end.

Dividing up the messages in this way allows R to be extensible: as
packages are loaded, their message translation catalogues can be loaded
too.

R can be built without support for translations, but it is enabled by
default.

R-level and C-level domains are subtly different, for example in the way
strings are canonicalized before being passed for translation.

Translations are looked for by domain according to the currently
specified language, as specifically as possible, so for example an
Austrian ('`de_AT`') translation catalogue will be used in
preference to a generic German one ('`de`') for an Austrian
user. However, if a specific translation catalogue exists but does not
contain a translation, the less specific catalogues are consulted. For
example, R has catalogues for '`en_GB`' that translate the
Americanisms (e.g., '`gray`') in the standard messages into
English.[^35^](#FOOT35) Two other examples: there are
catalogues for '`es`', which is Spanish as written in Spain and
these will by default also be used in Spanish-speaking Latin American
countries, and also for '`pt_BR`', which are used for Brazilian
locales but not for locales specifying Portugal.

Translations in the right language but the wrong charset are made use of
by on-the-fly re-encoding. The `LANGUAGE` variable
(only) can be a colon-separated list, for example '`se:de`',
giving a set of languages in decreasing order of preference. One special
value is '`en@quot`', which can be used in a UTF-8 locale to
have American error messages with pairs of single quotes translated to
Unicode directional quotes.

If no suitable translation catalogue is found or a particular message is
not translated in any suitable catalogue,
'English'[^36^](#FOOT36) is used.

See <https://developer.r-project.org/Translations30.html> for how to
prepare and install translation catalogues.

---
