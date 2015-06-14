#!/usr/bin/env python
import fileinput
import re
import sys

root = "main"
ignore = None
infiles = []

i = 1
while i < len(sys.argv):
    if sys.argv[i] == "--ignore":
        ignore = re.compile(sys.argv[i + 1])
        i += 1
    elif sys.argv[i] == "--root":
        root = sys.argv[i + 1]
        i += 1
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
        print >> sys.stderr, "Ambiguous function name", current 
    else:
        calls[current] = {}

def call(func, facility):
    global current, calls
    if calls[current].get(func, None) is not None and calls[current][func] != facility:
        print >> sys.stderr, "Ambiguous calling reference to ", func
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
            if ignore is None or re.match(ignore, ref) is None:
                print '"%s" -> "%s";' % (func, ref)
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

print "digraph callgraph {"
dump(root)
print "}"
