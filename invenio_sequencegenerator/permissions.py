# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
"""Sequence generator permissions."""
from __future__ import absolute_import, print_function

from functools import wraps

from flask import abort, current_app
from flask_login import current_user


def allow_all(*args, **kwargs):
    """Return permission that always allow an access.

    :returns: A object instance with a ``can()`` method.
    """
    return type('Allow', (), {'can': lambda self: True})()


def default_permission_factory(action, template, keywords):
    """Default sequence generator permission factory."""
    return allow_all()


def check_permission(permission):
    """Abort if permission is not allowed.

    :param permission: The permission to check.
    """
    if permission is not None and not permission.can():
        if current_user.is_authenticated:
            abort(403)
        abort(401)


def need_permission(action):
    """View decorator to check permissions for the given action or abort.

    :param action: The action needed.
    """
    def decorator_builder(f):
        @wraps(f)
        def decorate(self, template, keywords, *args, **kwargs):
            factory = current_app.extensions[
                'invenio-sequencegenerator'].permission_factory
            permission = factory(action, template, keywords)
            check_permission(permission)
            return f(self, template, keywords, *args, **kwargs)

        return decorate

    return decorator_builder
