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

bas = bas.strip().split("\n")

labels = {}

compiled = []
i = 0
py = False
for line in bas:
    if i > 65535:
        raise RuntimeError("Too many lines - can't convert")
    if line.strip() == ("```"):
        py = not py
        continue
    if py:
        exec(line)  # TODO a little bit of security needed?
        continue
    if line.lstrip().startswith("#"):
        continue
    if line.strip() == "":
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
