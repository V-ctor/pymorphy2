# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os

import pytest

import pymorphy2
from pymorphy2.opencorpora_dict.compile import (
    _to_paradigm,
    convert_to_pymorphy2
)
from pymorphy2.opencorpora_dict.parse import parse_opencorpora_xml
from pymorphy2.dawg import assert_can_create
from pymorphy2 import lang
from pymorphy2.opencorpora_dict.parse_links_matching import parse_links_matching_xml


class TestToyDictionary:
    XML_PATH = os.path.join(
        os.path.dirname(__file__),
        '..',
        'dev_data',
        'links_matching.xml'
    )

    def test_parse_xml(self):
        links_matching = parse_links_matching_xml(self.XML_PATH)

        assert links_matching[1] == []
        assert links_matching[2] == []
        assert links_matching[3] == []
        # assert links_matching[7] is None
        assert 7 not in links_matching, 'Array contains unnecessary element '
        links = links_matching[21]

        assert 268164 in links, 'Array does not contains necessary element '
        assert 268221 in links, 'Array does not contains necessary element '
        assert len(links) == 2, 'Array size is not 2'