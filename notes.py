#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
from package.controller import Controller
from package.model import Model

DB = './data/notes.db'

if __name__ == '__main__':
    model = Model(DB)
    app = Controller(model)
    if len(sys.argv) == 1:
        app.interactive_start()
    else:
        app.cli_start(sys.argv[1:])
