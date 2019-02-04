# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
"""Test views."""

from __future__ import absolute_import, print_function

import json

import mock
from flask import url_for

from invenio_sequencegenerator.api import Sequence, Template


def test_sequence_next(base_app, db):
    """Test sequence next."""

    with base_app.app_context(), base_app.test_client() as client:
        pl = Template.create('PL', 'C-{year}-{counter}')
        fl = Template.create('FL', '{PL}:{counter}')

        url = url_for('invenio_sequencegenerator.sequence', template_name='PL')
        res = client.post(
            url,
            content_type='application/json',
            data=json.dumps({
                'year': 2015
            }))
        assert res.status == '201 CREATED'
        pl15_0 = json.loads(res.data.decode('utf-8'))
        assert pl15_0 == 'C-2015-0'

        url = url_for('invenio_sequencegenerator.sequence', template_name='FL')
        res = client.post(
            url,
            content_type='application/json',
            data=json.dumps({
                'PL': pl15_0
            }))
        assert res.status == '201 CREATED'
        pl15_0 = json.loads(res.data.decode('utf-8'))
        assert pl15_0 == 'C-2015-0:0'


@mock.patch('invenio_sequencegenerator.permissions.allow_all',
            lambda *args, **kwargs:
            type('Deny', (), {'can': lambda self: False})())
def test_sequence_next_access_denied(base_app, db):
    """Test sequence next access denied."""
    with base_app.app_context(), base_app.test_client() as client:
        pl = Template.create('PL', 'C-{year}-{counter}')
        fl = Template.create('FL', '{PL}:{counter}')

        url = url_for('invenio_sequencegenerator.sequence', template_name='PL')
        res = client.post(
            url,
            content_type='application/json',
            data=json.dumps({
                'year': 2015
            }))
        assert res.status == '401 UNAUTHORIZED'
