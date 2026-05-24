# SPDX-FileCopyrightText: 2016-2018 CERN.
# SPDX-License-Identifier: MIT

"""Utilities for template strings."""

from __future__ import absolute_import, print_function

import re


def extract_placeholders(template):
    """Extract the template's placeholder names."""
    return re.findall(r'{(.*?)}', template)


def double_counter(template, regex):
    """Double brackets around the 'counter' for 2-step formatting."""
    return re.sub(regex, r'{\1}', template)
