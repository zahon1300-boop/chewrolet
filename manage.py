#!/usr/bin/env python
"""Django management utility."""

import os
import sys


def main() -> None:
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chevrolet_uz.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django topilmadi. Virtual muhitni faollashtiring va "
            "'pip install -r requirements.txt' ni bajargan ekanligingizga ishonch hosil qiling."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
