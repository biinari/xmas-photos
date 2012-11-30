#!/usr/bin/env python2
# vim: set fileencoding=utf-8 :

"""
Reprint photos

Usage: reprint filename copies
"""
import sys
import tools

def reprint(filename, copies=1):
    tools.print_image(filename, copies)

def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        print "Usage: %s filename copies" % sys.argv[0]
        sys.exit(1)
    if len(sys.argv) > 2:
        copies = sys.argv[2]
    else:
        copies = 1

    reprint(filename, copies)

if __name__ == '__main__':
    main()
