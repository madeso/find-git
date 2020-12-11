#!/usr/bin/env python3
import os
import subprocess

d = '.'
dirs = [os.path.join(d, o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]
gd = []

for dd in dirs:
    gf = os.path.join(dd, '.git')
    if os.path.isdir(gf):
        remote = subprocess.check_output(["git", "remote", '-v'], cwd=dd, universal_newlines=True)
        print(dd)
        print(remote)
        print()
    else:
        gd.append(dd)

print()
print('non git:')
for dd in gd:
    print(dd)
