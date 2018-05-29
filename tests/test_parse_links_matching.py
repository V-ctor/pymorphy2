# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import io
import os

import pytest

from pymorphy2.opencorpora_dict.parse_links_matching import parse_links_matching_xml, get_id_from_element, \
    does_element_contain_allowed_link_types_tag, add_links_from_link_type, add_allowed_link_types

try:
    from lxml import etree

    print("running with lxml.etree")
    from lxml.etree import iterparse, XMLSyntaxError


    def xml_clear_elem(elem):
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]

except ImportError:
    try:
        from xml.etree.cElementTree import iterparse
    except ImportError:
        from xml.etree.ElementTree import iterparse


@pytest.mark.parametrize("tag, attr, attr_value, expected", [
    ("link", "id", "1", 1),
    ("links", "id", "1", 1),
    ("link", "_id", "1", None),
    ("link", "id", "0.5", None),
    ("link", "id", "", None)
])
def test_id_parser(tag, attr, attr_value, expected):
    element = etree.Element(tag)
    element.set(attr, attr_value)
    actual = get_id_from_element(element)
    assert expected == actual


@pytest.mark.parametrize("tag, expected", [
    ("allowed_link_types", True),
    ("allowed_link_type", False),
    ("allowed_link", False)
])
def test_does_element_contain_allowed_link_types_tag_test(tag, expected):
    element = etree.Element(tag)
    actual = does_element_contain_allowed_link_types_tag(element)
    assert expected == actual


@pytest.mark.parametrize("xml, expected", [
    ("<link_type id=\"1\"/>", []),
    ("<link_type id=\"1\"></link_type>", []),
    ("""<link_type id="21">
            <link id="1"/>
        </link_type>
    """, [1]),
    ("""<link_type id="21">
            <link id="1"/>
            <link id="2"/>
        </link_type>
    """, [1, 2])
])
def test_add_links_from_link_type(xml, expected):
    element = etree.fromstring(xml)
    actual = add_links_from_link_type(element)
    assert expected == actual


@pytest.mark.parametrize("xml, expected", [
    ("""<allowed_link_types>
        </allowed_link_types>
    """, {}),
    ("""<allowed_link_types>
            <link_type id="1"/> <!--all connections with link type id 1 is allowed-->
        </allowed_link_types>
    """, {1: []}),
    ("""<allowed_link_types>
            <link_type id="1"/> <!--all connections with link type id 1 is allowed-->
            <link_type id="2"/>
        </allowed_link_types>
    """, {1: [], 2: []}),
    ("""<allowed_link_types>
            <link_type id="1"/> <!--all connections with link type id 1 is allowed-->
            <link_type id="2"/>
            <link_type id="21">
                <link id="100"/> <!--these links are allowed-->
                <link id="200"/>
            </link_type>
        </allowed_link_types>
    """, {1: [], 2: [], 21: [100, 200]})
])
def test_add_allowed_link_types(xml, expected):
    element = etree.fromstring(xml)
    actual = add_allowed_link_types(element)
    assert expected == actual


@pytest.mark.parametrize("xml, expected", [
    ("""<unknown_tag>
        </unknown_tag>
    """, {}),
    ("""<allowed_link_types>
        </allowed_link_types>
    """, {}),
    ("""<allowed_link_types>
            <link_type id="1"/> <!--all connections with link type id 1 is allowed-->
        </allowed_link_types>
    """, {1: []}),
    ("""<allowed_link_types>
            <link_type id="1"/> <!--all connections with link type id 1 is allowed-->
            <link_type id="2"/>
        </allowed_link_types>
    """, {1: [], 2: []}),
    ("""<allowed_link_types>
            <link_type id="1"/> <!--all connections with link type id 1 is allowed-->
            <link_type id="2"/>
            <link_type id="21">
                <link id="100"/> <!--these links are allowed-->
                <link id="200"/>
            </link_type>
        </allowed_link_types>
    """, {1: [], 2: [], 21: [100, 200]})
])
def test_parse_links_matching_xml(xml, expected):
    file = io.StringIO(xml)
    actual = parse_links_matching_xml(file)
    assert expected == actual


@pytest.mark.parametrize("xml", [
    ""
])
def test_parse_links_matching_xml(xml):
    file = io.StringIO(xml)
    with pytest.raises(XMLSyntaxError):
        parse_links_matching_xml(file)


class TestLinksMatchingParser:
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
