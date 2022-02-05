# Basko

## Introduction

Basko is a simple CBM Basic 2.0 preprocessor. 

It aims to enable writing basic code with any modern text editor with dynamic line numbers.

## Pre-requisites

* Python 3.6 or later
* [Petcat](http://manpages.ubuntu.com/manpages/bionic/man1/petcat.1.html)

## Modified Basic syntax

* Line numbers can be omitted. The script creates running line number from 0 onwards. This makes programming more simple.
* Instead of line numbers, labels can be used. Set a `\label\` in the code and you can point to it with `\*label\` pointer.
* Petcat mnemonics can be used as-is to represent the unprintable characters.
* comment lines start with `#`. They are omitted from conversion. If you want your comments into the basic code, use `rem` instead
`\` was eccentrically chosen as the magic character to define the labels. Rationale is, it is not available in PETSCII nor reserved by petcat.

### Example

```
\loop\ print"{grn}hello {wht}wr0ld ";:
goto \*loop\
```

## Usage

Convert Basic code to an executable Basic v2.0 program.

```
./basko input.bas output.prg
```
