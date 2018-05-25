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

    def test_parse_xml_result_must_contains(self):
        links_matching = parse_links_matching_xml(self.XML_PATH)
        assert len(links_matching) == 19, 'Result size is not 19'

        assert links_matching[1] == []
        assert links_matching[2] == []
        assert links_matching[3] == []

        assert links_matching[21] == [268160, 268159], 'Array does not contains necessary element '

    def test_parse_xml_must_not_contains(self):
        links_matching = parse_links_matching_xml(self.XML_PATH)
        assert len(links_matching) == 19, 'Result size is not 19'

        assert 7 not in links_matching, 'Array contains unnecessary element '
