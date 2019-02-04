# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
"""General module tests."""
from __future__ import absolute_import, print_function

from flask import Flask
from flask_babelex import Babel

from invenio_sequencegenerator import InvenioSequenceGenerator
from invenio_sequencegenerator.permissions import default_permission_factory
from invenio_sequencegenerator.views import blueprint


def test_version():
    """Test version import."""
    from invenio_sequencegenerator import __version__
    assert __version__


def test_init():
    """Test extension initialization."""
    app = Flask('testapp')
    ext = InvenioSequenceGenerator(app)
    assert 'invenio-sequencegenerator' in app.extensions
    assert ext.permission_factory == default_permission_factory

    app = Flask('testapp')
    ext = InvenioSequenceGenerator()
    assert 'invenio-sequencegenerator' not in app.extensions
    ext.init_app(app)
    assert 'invenio-sequencegenerator' in app.extensions


def test_view(base_app):
    """Test view."""
    InvenioSequenceGenerator(base_app)
    base_app.register_blueprint(blueprint)
