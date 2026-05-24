# SPDX-FileCopyrightText: 2015-2018 CERN.
# SPDX-License-Identifier: MIT


"""Test version."""

from __future__ import absolute_import, print_function


def test_version():
    """Test version import."""
    from invenio_sequencegenerator import __version__
    assert __version__
