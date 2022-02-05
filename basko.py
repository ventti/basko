#
# basko - simple BASic KOmpiler
#
# "compiles" Basic code and provides automatic line numbering
# give labels as \label\ and pointers as \*label\.
#

import re
import sys

with open(sys.argv[1], "rt") as fp:
    bas = fp.read()

re_label = re.compile(r'\\([a-z]+)\\')

bas = bas.strip().split("\n")

labels = {}

compiled = []
for i, line in enumerate(bas):
    if line.lstrip().startswith("#"):
        continue
    m = re_label.match(line)
    if m:
        labels[m.group(1)] = i
        compiled.append(line.replace(m.group(0),str(i)))
    else:
        compiled.append(f"{i} {line}")

basic = "\n".join(compiled)

for label in labels:
    l = f"\\*{label}\\"
    basic = basic.replace(l, str(labels[label]))

print (basic)
