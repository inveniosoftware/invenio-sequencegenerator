# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
"""Flask extension for Invenio-SequenceGenerator."""

from __future__ import absolute_import, print_function

from flask import Blueprint
from werkzeug.utils import cached_property

from . import config
from .utils import load_or_import_from_config


class InvenioSequenceGenerator(object):
    """Invenio-SequenceGenerator extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.app = app
            self.init_app(app)

    @cached_property
    def permission_factory(self):
        """Permission factory from config."""
        return load_or_import_from_config(
            'SEQUENCE_GENERATOR_PERMISSION_FACTORY', app=self.app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        app.extensions['invenio-sequencegenerator'] = self

    def init_config(self, app):
        """Initialize configuration."""
        for k in dir(config):
            if k.startswith('SEQUENCE_GENERATOR_'):
                app.config.setdefault(k, getattr(config, k))
