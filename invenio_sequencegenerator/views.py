# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
"""Sequence Generator REST-API."""
from __future__ import absolute_import, print_function

from functools import wraps

from flask import Blueprint, jsonify, request
from invenio_db import db
from invenio_rest import ContentNegotiatedMethodView

from .api import Sequence
from .permissions import need_permission

blueprint = Blueprint(
    'invenio_sequencegenerator',
    __name__,
    template_folder='templates'
)


def pass_keywords(f):
    """Decorator to retrieve the keywords to be used from the request."""
    @wraps(f)
    def inner(self, template_name, *args, **kwargs):
        keywords = request.get_json()
        return f(self, template_name, keywords)

    return inner


class SequenceResource(ContentNegotiatedMethodView):
    """Sequence resource."""

    view_name = 'sequence'

    @pass_keywords
    @need_permission('sequence-next')
    def post(self, template_name, keywords):
        """Obtain a new number of a sequence.

        :param template_name:
        :param keywords: dictionary with the key value pairs to be used to fill
            sequence template.
        """
        next_counter = Sequence(template_name, **keywords).next()
        db.session.commit()
        response = jsonify(next_counter)
        response.status_code = 201
        return response


blueprint.add_url_rule(
    '/sequencegenerator/<string:template_name>',
    view_func=SequenceResource.as_view(SequenceResource.view_name))
