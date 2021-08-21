#!/usr/bin/env python
import os
import sys
import time

import environ
from django.db.utils import OperationalError

environ.Env.read_env()

DB_TIMEOUT = 30


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pycon.settings.prod")

    from django.core.management import execute_from_command_line

    start = time.time()
    try:
        execute_from_command_line(sys.argv)
    except OperationalError:
        while True:
            print("Database not up yet, giving it a second!")
            time.sleep(1)

            try:
                execute_from_command_line(sys.argv)
                break
            except OperationalError:
                pass

            if time.time() - start > DB_TIMEOUT:
                raise
