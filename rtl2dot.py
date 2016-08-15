#!/usr/bin/env python3
#
# Author: cbdev <cb@cbcdn.com>
# Reference: https://github.com/cbdevnet/rtl2dot 
#
#This program is free software. It comes without any warranty, to
#the extent permitted by applicable law. You can redistribute it
#and/or modify it under the terms of the Do What The Fuck You Want
#To Public License, Version 2, as published by Sam Hocevar and 
#reproduced below.
#
#DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE 
#Version 2, December 2004 
#
#Copyright (C) 2004 Sam Hocevar <sam@hocevar.net> 
#
#	Everyone is permitted to copy and distribute verbatim or modified 
#	copies of this license document, and changing it is allowed as long 
#	as the name is changed. 
#
#DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE 
#TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION 
#
#	0. You just DO WHAT THE FUCK YOU WANT TO.
#

import fileinput
import re
import sys

root = "main"
ignore = None
infiles = []
local = False

i = 1
# There probably should be sanity checks here, but lets face it: If you cant pass arguments right, this isnt for you
while i < len(sys.argv):
    if sys.argv[i] == "--ignore":
        ignore = re.compile(sys.argv[i + 1])
        i += 1
    elif sys.argv[i] == "--root":
        root = sys.argv[i + 1]
        i += 1
    elif sys.argv[i] == "--local":
        local = True
    elif sys.argv[i] == "--help" or sys.argv[i] == "-h":
        print("Generate call graphs of C programs from gcc rtldumps")
        print("Options:")
        print("\t--ignore <regex>\t\tFunctions to omit from the resulting graph")
        print("\t--root <function>\t\tWhich function to use as root node (default: main)")
        print("\t--local\t\t\t\tOmit functions not defined in the dump (eg. library calls)")
        sys.exit(0)
    else:
        infiles.append(sys.argv[i])
    i+=1

current = ""
calls = {}

func_old = re.compile("^;; Function (?P<func>\S+)\s*$")
func_new = re.compile("^;; Function (?P<mangle>.*)\s+\((?P<func>\S+)(,.*)?\).*$")
funcall = re.compile("^.*\(call.*\"(?P<target>.*)\".*$")
symref = re.compile("^.*\(symbol_ref.*\"(?P<target>.*)\".*$")

def enter(func):
    global current, calls
    current = func
    if calls.get(current, None) is not None:
        print("Ambiguous function name " + current, file=sys.stderr)
    else:
        calls[current] = {}

def call(func, facility):
    global current, calls
    if calls[current].get(func, None) is not None and calls[current][func] != facility:
        print("Ambiguous calling reference to " + func, file=sys.stderr)
    calls[current][func] = facility

def dump(func):
    global calls
    if calls.get(func, None) is None:
        # edge node
        return
    for ref in calls[func].keys():
        if calls[func][ref] == "call":
            # Invalidate the reference to avoid loops
            calls[func][ref] = None
            if local and calls.get(ref, None) is None:
                # non-local function
                continue
            if ignore is None or re.match(ignore, ref) is None:
                print('"' + func + '" -> "' + ref + '";')
                dump(ref)

# Scan the rtl dump into the dict
for line in fileinput.input(infiles):
    if re.match(func_old, line) is not None:
        # print "OLD", re.match(func_old, line).group("func")
        enter(re.match(func_old, line).group("func"))
    elif re.match(func_new, line) is not None:
        # print "NEW", re.match(func_new, line).group("func"), "Mangled:", re.match(func_new, line).group("mangle")
        enter(re.match(func_new, line).group("func"))
    elif re.match(funcall, line) is not None:
        # print "CALL", re.match(funcall, line).group("target")
        call(re.match(funcall, line).group("target"), "call")
    elif re.match(symref, line) is not None:
        # print "REF", re.match(symref, line).group("target")
        call(re.match(symref, line).group("target"), "ref")

print("digraph callgraph {")
dump(root)
print("}")
