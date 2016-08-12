# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016 CERN.
#
# Invenio is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""Models for storing counters for each pattern."""

import re

from invenio_db import db
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
from sqlalchemy.orm.exc import MultipleResultsFound

from .errors import InvalidResetCall, InvalidTemplate
from .utils import double_counter, extract_placeholders


class TemplateDefinition(db.Model, object):
    """Representation of a template definition."""

    __tablename__ = 'sequencegenerator_template'

    COUNTER_REGEX = re.compile(r'({counter(!.)?(:.*)?})')
    """Regular expression matching the counter inside the template string."""

    name = db.Column(db.String(255), primary_key=True)
    """The identifier of the template definition."""

    _meta_template = db.Column('meta_template', db.String(255), unique=True)
    """The template generator."""

    parent_name = db.Column(db.ForeignKey(name))
    """Indicate that the template depends on another one."""

    start = db.Column(db.Integer, default=0)
    """The starting counter of sequences generated from ``meta_template``."""

    step = db.Column(db.Integer, default=1)
    """The incremental step of sequences generated from ``meta_template``."""

    children = db.relationship(
        'TemplateDefinition',
        backref=db.backref('parent', remote_side=name)
    )

    @validates('_meta_template')
    def validate_meta_template(self, key, value):
        """Validate template string of template definition."""
        if not self.COUNTER_REGEX.search(value):
            raise InvalidTemplate('No counter placeholder')
        value = double_counter(value, self.COUNTER_REGEX)
        return value

    @hybrid_property
    def meta_template(self):
        """The template string of the template definition."""
        return self._meta_template

    @meta_template.setter
    def meta_template(self, meta_template):
        """Automatically derive parent from template string."""
        placeholders = extract_placeholders(meta_template)

        # Check if parent sequence exists
        try:
            parent = TemplateDefinition.query.filter(
                TemplateDefinition.name.in_(placeholders)
            ).one_or_none() if placeholders else None
        except MultipleResultsFound:
            raise InvalidTemplate('More than 1 parents in template')

        self.parent = parent
        self._meta_template = meta_template

    def counter(self, **kwargs):
        """Get counter of this template definition, based on given kwargs."""
        counter = Counter.get(self.meta_template, kwargs)
        if counter is None:
            with db.session.begin_nested():
                counter = Counter.create(
                    meta_template=self.meta_template,
                    ctx=kwargs,
                    counter=self.start,
                    template_definition=self,
                )
                db.session.add(counter)

        return counter


class Counter(db.Model):
    """Stores generated identifiers."""

    __tablename__ = 'sequencegenerator_counter'

    template_instance = db.Column(db.String(255), nullable=False,
                                  primary_key=True, index=True)
    """The template string to use."""

    definition_name = db.Column(db.ForeignKey(TemplateDefinition.name))
    """Link to the template definition."""

    counter = db.Column(db.Integer, nullable=False)
    """Running counter."""

    template_definition = db.relationship(
        TemplateDefinition,
        lazy='joined',
        backref=db.backref('counters', cascade='all, delete-orphan')
    )

    # Optimistic concurrency control
    __mapper_args__ = {
        'version_id_col': counter,
        'version_id_generator': False
    }

    @classmethod
    def create(cls, meta_template, ctx=None, **kwargs):
        """Initialize a counter."""
        assert 'meta_template' not in kwargs
        return cls(
            template_instance=meta_template.format(**ctx or {}),
            **kwargs
        )

    @classmethod
    def get(cls, definition, ctx=None):
        """Get a ``Counter``."""
        return cls.query.get(definition.format(**ctx or {}))

    def increment(self):
        """Generate next identifier."""
        next_identifier = self.template_instance.format(counter=self.counter)
        with db.session.begin_nested():
            self.counter += self.template_definition.step
            return next_identifier

    def reset(self, start=0):
        """Reset counter."""
        with db.session.begin_nested():
            # Ensure no children exist
            for child in self.template_definition.children:
                if child.counters:
                    raise InvalidResetCall()

            self.counter = start
