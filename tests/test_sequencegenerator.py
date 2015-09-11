# -*- coding: utf-8 -*-
#
# This file is part of Invenio Demosite.
# Copyright (C) 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012 CERN.
#
# Invenio Demosite is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio Demosite is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

""" Test unit for the miscutil/sequtils module. """

from mock import patch

from invenio.testsuite import InvenioTestCase

from invenio_sequencegenerator.backend import SequenceGenerator


def get_bibrecord_mock(_):
    return {'001': [([], ' ', ' ', '1086086', 1)],
            '111': [([('a',
            'Mock conference'),
            ('d', '14-16 Sep 2011'),
            ('x', '2050-09-14'),
            ('c', 'xxxxx')],
            ' ',
            ' ',
            '',
            3)],
            '270': [([('m', 'dummy@dummy.com')], ' ', ' ', '', 5)],
            '856': [([('u', 'http://dummy.com/')], '4', ' ', '', 6)],
            '970': [([('a', 'CONF-XXXXXX')], ' ', ' ', '', 2)],
            '980': [([('a', 'CONFERENCES')], ' ', ' ', '', 7)]}


class IntSeq(SequenceGenerator):
    seq_name = 'test_int'

    def _next_value(self, x):
        return x + 1


class TestIntSequenceGeneratorClass(InvenioTestCase):

    def test_sequence_next_int(self):
        from invenio_sequencegenerator.cnum import CnumSeq
        int_seq = IntSeq()
        next_int = int_seq.next_value(1)
        self.assertEqual(next_int, 2)

        # Check if the value was stored in the DB
        res = SeqSTORE.query.filter(
            SeqSTORE.seq_value == 2,
            SeqSTORE.seq_name == int_seq.seq_name
        ).one()
        self.assertEqual(res.seq_value, 2)

        # Clean DB entries
        SeqSTORE.query.filter(SeqSTORE.seq_name == int_seq.seq_name).delete()


class TestCnumSequenceGeneratorClass(InvenioTestCase):

    @patch('invenio.legacy.bibedit.utils.get_bibrecord',
        get_bibrecord_mock)
    def test_get_next_cnum(self):
        from invenio_sequencegenerator.cnum import CnumSeq
        from invenio_sequencegenerator.models import SeqSTORE

        cnum_seq = CnumSeq()
        res = cnum_seq.next_value('xx')
        self.assertEqual(res, 'C50-09-14')
        res = cnum_seq.next_value('xx')
        self.assertEqual(res, 'C50-09-14.1')

        # Clean DB entries
        SeqSTORE.query.filter(
            SeqSTORE.seq_name == 'cnum',
            SeqSTORE.seq_value.in_(
                'C50-09-14', 'C50-09-14.1'
            )
        ).delete()
