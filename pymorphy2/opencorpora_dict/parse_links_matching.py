# -*- coding: utf-8 -*-
"""
:mod:`pymorphy2.opencorpora_dict.parse_links_matching_xml` for parsing allowed links matching.
"""
from __future__ import absolute_import, unicode_literals, division

import logging
import collections

try:
    from lxml import etree

    print("running with lxml.etree")
    from lxml.etree import iterparse


    def xml_clear_elem(elem):
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]

except ImportError:
    try:
        from xml.etree.cElementTree import iterparse
    except ImportError:
        from xml.etree.ElementTree import iterparse


    def xml_clear_elem(elem):
        elem.clear()


logger = logging.getLogger(__name__)

ParsedDictionary = collections.namedtuple('ParsedDictionary', 'lexemes links grammemes version revision')


def parse_links_matching_xml(filename):

    allowed_link_types = {}

    logger.info("Parsing file links matching dictionary v%s", filename)

    root = etree.parse(filename).getroot()
    if does_element_contain_allowed_link_types_tag(root):
        add_allowed_link_types(allowed_link_types, root)
    return allowed_link_types


def add_allowed_link_types(allowed_link_types, element):
    for allowed_link_type in element.getchildren():
        links = []
        if does_element_contain_link_types_tag(allowed_link_type):
            id = get_id_from_element(allowed_link_type)
            allowed_link_types[id] = links
            add_links_from_linktype(allowed_link_type, links)


def add_links_from_linktype(allowed_link_type, links):
    for link in allowed_link_type.getchildren():
        id = get_id_from_element(link)
        links.append(id)
        logger.info("%s => %s" % (link.tag, link.text))


def get_id_from_element(link):
    id = int(link.get('id'))
    return id


def does_element_contain_allowed_link_types_tag(element):
    return element.tag == "allowed_link_types"


def does_element_contain_link_types_tag(element):
    return element.tag == "link_type"
