
"""
.. module:: desktop_security_assistant.utils
   :synopsis: Security Assistant

"""

# Released under AGPLv3+ license, see LICENSE

import pkg_resources
import os


def get_resource(*a):
    if 'DEVELOPMENT' in os.environ:
        p = '.'
    else:
        p = pkg_resources.resource_filename(__name__, '.')

    ap = os.path.abspath(p)
    return os.path.join(ap, *a)
