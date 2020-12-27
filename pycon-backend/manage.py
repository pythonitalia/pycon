#!/usr/bin/env python
import os
import sys

import environ

environ.Env.read_env()


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pycon.settings.prod")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
