# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
"""Python 2/3 compatibility helpers."""

from __future__ import absolute_import, print_function

import sys

PY3 = sys.version_info[0] == 3

string_types = str if PY3 else basestring
