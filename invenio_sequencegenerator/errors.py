# SPDX-FileCopyrightText: 2016-2018 CERN.
# SPDX-License-Identifier: MIT

"""Errors for sequence generation."""

from __future__ import absolute_import, print_function


class SequenceGeneratorError(Exception):
    """Base class for errors in SequenceGenerator module."""


class SequenceNotFound(SequenceGeneratorError):
    """No such sequence error."""


class InvalidTemplate(SequenceGeneratorError):
    """Invalid template error."""

    def __init__(self, reason):
        """Initialize exception."""
        self.reason = reason

    def __str__(self):
        """String representation of error."""
        return self.reason


class InvalidResetCall(SequenceGeneratorError):
    """Invalid reset call error."""

    def __str__(self):
        """String representation of error."""
        return 'Cannot reset sequence: children exist'
