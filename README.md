# Basko

Basko by [Vent](https://csdb.dk/scener/?id=1073).

## Introduction

Basko is a simple CBM Basic 2.0 preprocessor. 

Basko aims to enable writing basic code with any modern text editor with dynamic line numbers.

In addition Basko supports Python inline scripting. Such a nice feature for doing precalc.

## Pre-requisites

* Python 3.6 or later
* [Petcat](http://manpages.ubuntu.com/manpages/bionic/man1/petcat.1.html)

## .basko file format - Modified Basic syntax

* Line numbers can be omitted. The script creates running line number from 0 onwards. This makes programming more simple.
* Instead of line numbers, labels can be used. Set a `\label\` in the code and you can point to it with `\*label\` pointer.
* [Petcat mnemonics](https://www.c64-wiki.com/wiki/PETSCII_Codes_in_Listings) can be used as-is to represent the unprintable characters.
* comment lines start with `#`. They are omitted from conversion. If you want your comments into the basic code, use `rem` instead
`\` was eccentrically chosen as the magic character to define the labels. Rationale is, it is not available in PETSCII nor reserved by petcat.
* Python code blocks can be embedded to the basic code. Executable blocks are defined with ``` characters. Such blocks are [executed](https://docs.python.org/3/library/functions.html#exec)
* Inline expressions are defined between ` characters. Such expressions are [evaluated](https://docs.python.org/3/library/functions.html#eval).

### Examples

#### Labels and pointers
```
\loop\ print"{grn}hello {wht}wr0ld ";:
goto \*loop\
```

#### Code blocks
````` 
```
# this code is executed
x = 1 + 1
```

# these variables are evaluated
print "i have `x` hands and `5 * x` fingers"

````` 
will result as

```
0 print "i have 2 hands and 10 fingers"
```

## Usage

Convert Basic code to an executable Basic v2.0 program.

```
./basko input.basko output.prg
```
