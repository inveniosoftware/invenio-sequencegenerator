# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
"""Utilities for template strings."""

from __future__ import absolute_import, print_function

import re

from flask import current_app
from werkzeug.utils import import_string

from ._compat import string_types


def obj_or_import_string(value, default=None):
    """Import string or return object.

    :params value: Import path or class object to instantiate.
    :params default: Default object to return if the import fails.
    :returns: The imported object.
    """
    if isinstance(value, string_types):
        return import_string(value)
    elif value:
        return value
    return default


def load_or_import_from_config(key, app=None, default=None):
    """Load or import value from config.

    :returns: The loaded value.
    """
    app = app or current_app
    imp = app.config.get(key)
    return obj_or_import_string(imp, default=default)


def extract_placeholders(template):
    """Extract the template's placeholder names."""
    return re.findall(r'{(.*?)}', template)


def double_counter(template, regex):
    """Double brackets around the 'counter' for 2-step formatting."""
    return re.sub(regex, r'{\1}', template)
