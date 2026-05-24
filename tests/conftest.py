# SPDX-FileCopyrightText: 2015-2018 CERN.
# SPDX-License-Identifier: MIT
"""Pytest configuration."""

from __future__ import absolute_import, print_function

import pytest
from flask import Flask
from invenio_db import InvenioDB

from invenio_sequencegenerator.ext import InvenioSequenceGenerator


@pytest.fixture(scope='module')
def create_app():
    """Application factory fixture."""
    def factory(**config):
        app = Flask('testapp')
        app.config.update(**config)

        InvenioDB(app)
        InvenioSequenceGenerator(app)

        return app

    return factory
