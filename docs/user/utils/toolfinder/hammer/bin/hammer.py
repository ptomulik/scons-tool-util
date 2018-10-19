#!/usr/bin/env python3
import sys
with open(sys.argv[2], 'rt') as ifile, open(sys.argv[1], 'wt') as ofile:
    ofile.write(ifile.read().replace('nail', 'drived in nail'))
