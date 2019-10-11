"""
Confirm your environment meets the minimum requirements for this workshop
"""

import logging
import sys

# pylint: disable=unused-variable


def main():
    """Confirm local environment is setup correctly"""

    try:
        # Ensure the Python version is greater than 3.5
        assert sys.version_info >= (3, 5, 2)
    except AssertionError:
        logging.error(
            "\n\nYour Python version is incompatible with this workshop. You're running "
            + f"{sys.version_info[0]}.{sys.version_info[1]}\n"
        )
        return

    try:
        # Check that Pip is installed.
        import pip
    except ImportError:
        logging.error(
            "\n\nYou don't have Pip installed. Make sure it's installed and configured correctly\n"
        )
        return

    try:
        # Check that Virtualenv is installed.
        import virtualenv
    except ImportError:
        logging.error(
            "\n\nYou don't have Virtualenv installed. Make sure it's installed and configured correctly\n"
        )
        return

    try:
        # Check that Cookiecutter is installed.
        import cookiecutter
    except ImportError:
        logging.error(
            "\n\nYou don't have Cookiecutter installed. Make sure it's installed and configured correctly\n"
        )
        return

    print(
        "\nSuccess! Your local environment is configured correctly and you're ready for this workshop!\n"
    )


if __name__ == "__main__":
    sys.exit(main())
