#! /usr/bin/env python

import sys
import re

fo = open(sys.argv[1],'r')

last_line = None
for l in fo:
    if 'QD' in l:
        a = l.replace('QD','HD1')
        b = l.replace('QD','HD2')
        if 'QG' in a:
            s = a.replace('QG','HG1')
            t = a.replace('QG','HG2')
            print s,
            print t,
            last_line = s
            continue
        if 'QG' in b:
            s = b.replace('QG','HG1')
            t = b.replace('QG','HG2')
            print s,
            print t,
            last_line = s
            continue
        print a,
        print b,
        continue
    if 'QG' in l:
        a = l.replace('QG','HG1')
        b = l.replace('QG','HG2')
        print a,
        print b,
        last_line = a
        continue
    if last_line == "\n" and l == "\n":
        continue
    print l,
    last_line = l
