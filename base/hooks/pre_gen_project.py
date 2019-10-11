from __future__ import print_function

import re
import sys


MODULE_REGEX = r"^[_a-zA-Z][_a-zA-Z0-9]+$"
DATABASE_REGEX = (
    r"^[_a-zA-Z][-_a-zA-Z0-9]+$"
)  # hyphens allowed, but then quotes are required.


app_name = "{{ cookiecutter.app_name }}"
container_name = "{{ cookiecutter.container_name }}"

problems = []

if not re.match(MODULE_REGEX, app_name):
    problems.append(
        'The app_name "{0}" is not a valid Python module name'.format(app_name)
    )

if problems:
    print("Problems creating project:", file=sys.stderr)
    for problem in problems:
        print(" -", problem, file=sys.stderr)

    sys.exit(1)
