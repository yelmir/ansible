# -*- coding: utf-8 -*-
# Copyright (c) 2018 Ansible Project
# Simplified BSD License (see licenses/simplified_bsd.txt or https://opensource.org/licenses/BSD-2-Clause)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import json
import os
import sys


from ansible.module_utils.six import PY2, PY3
from ansible.module_utils._text import container_to_bytes

# Internal global holding passed in params.  This is consulted in case
# multiple AnsibleModules are created.  Otherwise each AnsibleModule would
# attempt to read from stdin.  Other code should not use this directly as it
# is an internal implementation detail
_ANSIBLE_ARGS = None


class Validator(object):
    @staticmethod
    def foo():
        return 'yes'


def load_params():
    ''' read the modules parameters and store them globally.

    This function may be needed for certain very dynamic custom modules which
    want to process the parameters that are being handed the module.  Since
    this is so closely tied to the implementation of modules we cannot
    guarantee API stability for it (it may change between versions) however we
    will try not to break it gratuitously.  It is certainly more future-proof
    to call this function and consume its outputs than to implement the logic
    inside it as a copy in your own code.
    '''
    global _ANSIBLE_ARGS
    if _ANSIBLE_ARGS is not None:

        buffer = _ANSIBLE_ARGS
    else:

        # debug overrides to read args from file or cmdline

        # Avoid tracebacks when locale is non-utf8
        # We control the args and we pass them as utf8
        if len(sys.argv) > 1:
            if os.path.isfile(sys.argv[1]):

                fd = open(sys.argv[1], 'rb')
                buffer = fd.read()
                fd.close()
            else:

                buffer = sys.argv[1]
                if PY3:
                    buffer = buffer.encode('utf-8', errors='surrogateescape')
        # default case, read from stdin
        else:
            if PY2:
                buffer = sys.stdin.read()
            else:
                buffer = sys.stdin.buffer.read()
        _ANSIBLE_ARGS = buffer

    try:
        params = json.loads(buffer.decode('utf-8'))
    except ValueError:

        # This helper used too early for fail_json to work.
        print('\n{"msg": "Error: Module unable to decode valid JSON on stdin. Unable to figure out what parameters were passed", "failed": true}')
        sys.exit(1)

    if PY2:
        params = container_to_bytes(params)

    try:
        return params['ANSIBLE_MODULE_ARGS']
    except KeyError:
        # This helper does not have access to fail_json so we have to print
        # json output on our own.
        print('\n{"msg": "Error: Module unable to locate ANSIBLE_MODULE_ARGS in json data from stdin. Unable to figure out what parameters were passed", '
              '"failed": true}')
        sys.exit(1)
