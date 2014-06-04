#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from server import app
from server import sched
from bottle import debug, run

debug(True)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    sched.start()
    run(app, reloader=True, host='0.0.0.0', port=port)