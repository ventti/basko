# coding=utf-8
""" basko - a simple CBM Basic preprocessor

"compiles" Basic code and provides automatic line numbering
- give labels as \label\ and pointers as \*label\.
- include python blocks to be executed:
  ```
  myexpr = "hello" * 5
  ```
- include in-line python to be evaluated with `myexpr`

"""

import re
import sys
import os
import logging
import tempfile

logger = logging.getLogger(name="BASKO")
logging.basicConfig(level=logging.DEBUG)

with open(sys.argv[1], "rt") as fp:
    bas = fp.read()

re_label = re.compile(r'\\([a-z]+)\\')

def eval_inline(line):
    """ Find and evaluate expression between two grave accents.

    Args:
        line (str): line of code to be evaluated.

    """
    while True:
        p = line.find("`", 0)
        if p < 0:  # no inline code
            return line
        q = line.find("`", p + 1)
        if q < 0:
            raise ValueError(f"Invalid line: {line}")
        inline_code = line[p+1:q]
        val = str(eval(inline_code))
        line = line.replace(f"`{inline_code}`", val)

def compile_asm(src):
    """ Compile asm source lines

    Args:
        src (list): asm source lines
    Returns:
        assembled code (bytes)

    """
    # TODO srcfile = tmpfile
    _, srcfile = tempfile.mkstemp(suffix='.asm', text=True)
    with open(srcfile, "wt") as fp:
        fp.write("\n".join(src))
    # fp.close()

    _, prgfile = tempfile.mkstemp(suffix='.prg')
    #_fd.close()  # we don't need this now

    try:
        _do_compile(srcfile, prgfile)
        with open(prgfile, 'rb') as fp:
            prg = fp.read()
        # TODO remove tmpfile
    finally:
        os.remove(prgfile)
        os.remove(srcfile)
    return prg

def _do_compile(srcfile, prgfile, compiler='64tass -Wall -b -a {srcfile} -o {prgfile} 1>&2'):
    """ Does asm compilation with default flags

    Args:
        srcfile (str):
        prgfile (str):

    """
    logger.info(f"Compiling {srcfile} to {prgfile}")
    ret = os.system(compiler.format(srcfile=srcfile, prgfile=prgfile))
    if ret > 0:
        raise RuntimeError(f"Compilation failed: Return code {ret}")

bas = bas.strip().split("\n")

labels = {}

compiled = []
i = 0
is_py = False
is_asm = False
asmblock = []
pyblock =[] 
asm = {}  # all asm blocks
for _i, line in enumerate(bas):
    if i > 65535:
        raise RuntimeError("Too many lines - can't convert")
    _line = line.strip()
    if _line == "":  # skip empty lines
        continue
    elif _line.startswith("```asm="):
        asmblock_key = _line.split("=")[1]  # variable name
        logger.info(f"{_i}: Detected Asm block, storing to asm['{asmblock_key}']")
        is_asm = True
        continue
    elif _line == "```py":
        logger.info(f"{_i}: Detected Python block")
        is_py = True
        continue
    elif _line == "```":
        logger.debug(f"{_i}: End of block detected")
        if is_py:
            logger.info(f"{_i}: End of Python block")
            # exec python block
            exec("\n".join(pyblock))
            pyblock = []
            is_py = False
        elif is_asm:
            logger.info(f"{_i}: End of Asm block")
            asm[asmblock_key] = compile_asm(asmblock)  # asm code as bytes
            logger.info(f"{_i}: Compilation successful")
            asmblock=[]  # reset asm block
            is_asm = False
        else:
            is_py = not is_py
        continue
    if is_asm:
        asmblock.append(line)
        continue
    elif is_py:
        pyblock.append(line)
        continue
    elif _line[0] == "#":
        continue
    line = eval_inline(line)

    m = re_label.match(line)
    if m:
        labels[m.group(1)] = i
        line = line.replace(m.group(0), str(i))
    else:
        line = f"{i} {line}"
    compiled.append(line)
    i += 1

basic = "\n".join(compiled)

for label in labels:
    l = f"\\*{label}\\"
    basic = basic.replace(l, str(labels[label]))
print (basic)
