#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
from controller import Controller

DB='notes.db'

if __name__ == '__main__':
    model = Model(DB)
    app = Controller(model)
    if len(sys.argv) == 1:
        app.interactive_start()
    else:
        app.cli_start(sys.argv[1:])
