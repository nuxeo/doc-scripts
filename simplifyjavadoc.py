#!/usr/bin/python
# Strips cruft from a Javadoc file and keeps only the type doc
# Works with Javadoc up to Java 6 and also Java 7
#
# Copyright (c) 2011-2012 Nuxeo SA (http://nuxeo.com/)
# Licensed under the Apache License, Version 2.0
# Author: Florent Guillaume

import sys, re

def gen(filename):
    file = open(filename)
    step = 0
    lines = []
    for line in file:
        line = line.rstrip()
        if step == 0:
            if line == '<!-- ======== START OF CLASS DATA ======== -->':
              step = 1
            continue
        if step == 1:
            if line == '<HR>':
              step = 2
              continue
            elif line.startswith('<div class="block">'):
              step = 3
              # fall through
            else:
              continue
        if step == 2:
            if line == '</PRE>':
              step = 3
            continue

        if line.endswith('>Serialized Form</A></DL>'):
            line = '</DL>'
        elif (line.startswith('<DT><B>See Also:</B>') or
              line.startswith('<dt><span class="strong">See Also:</span>')):
            break # stop after See Also (may be multi-line)

        if (line == '<DT><B>Author:</B></DT>' or
            line == '<dl><dt><span class="strong">Author:</span></dt>'):
            step = 4
            continue
        if step == 4:
            step = 3 # skip author
            continue
        
        if (line == '<HR>' or
            line == '<div class="summary">'):
            break

        lines.append(line)

    file.close()

    # strip some stuff at beginning and end

    while len(lines) and (lines[0] == '' or lines[0] == '<P>'):
        del lines[0]

    if len(lines) >= 2 and lines[len(lines)-2] == '<DL>' and lines[len(lines)-1] == '</DL>':
        del lines[len(lines)-2:]

    while len(lines) and (lines[len(lines)-1] == '' or lines[len(lines)-1] == '<P>' or lines[len(lines)-1] == '<DL>'):
        del lines[len(lines)-1]

    # output result

    newfilename = filename[:-(len('.html'))] + '.type.html'
    print "Generating " + newfilename
    out = open(newfilename, 'w+')
    for line in lines:
        print >> out, line
    out.close()


# MAIN 

for filename in sys.argv[1:]:
    # skip non-html
    if not filename.endswith('.html'):
        continue
    # skip generated files
    if filename.endswith('.type.html'):
        continue
    # skin index.html
    if filename.endswith('/index.html'):
        continue
    # skip package-frame.html, package-summary.html, package-tree.html, package-use.html ...
    if '-' in filename[filename.rindex('/'):]:
        continue
    # skip class-use
    if '/class-use/' in filename:
        continue

    gen(filename)

sys.exit(0)

