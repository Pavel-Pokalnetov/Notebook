#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import interactive_mode
from arg_parser import argParser



if __name__ == '__main__':

    if len(sys.argv) == 1:
        interactive_mode.start()

    arg = argParser(sys.argv[1:])
    


