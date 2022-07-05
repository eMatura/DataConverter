#!/usr/bin/env python3

from parser import parse
import sys, json

def main(argv):

    for filepath in argv:
        print(json.dumps(parse(filepath)))

if __name__ == "__main__":
    main(sys.argv[1:])