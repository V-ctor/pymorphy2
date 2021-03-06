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


    def xml_clear_elem(elem):
        elem.clear()

logger = logging.getLogger(__name__)

ParsedDictionary = collections.namedtuple('ParsedDictionary', 'lexemes links grammemes version revision')


def parse_links_matching_xml(filename):

    logger.info("Parsing file links matching dictionary v%s", filename)

    try:
        root = etree.parse(filename).getroot()
    except XMLSyntaxError:
        logger.error("Error during parsing root element in links matching file. Please correct the xml and try again.")
        raise

    return add_allowed_link_types(root) if does_element_contain_allowed_link_types_tag(root) else {}


def add_allowed_link_types(element):
    allowed_link_types = {}
    for allowed_link_type in element.getchildren():
        if does_element_contain_link_types_tag(allowed_link_type):
            id = get_id_from_link_type(allowed_link_type)
            allowed_link_types[id] = add_links_from_link_type(allowed_link_type)
    return allowed_link_types


def add_links_from_link_type(parent_element):
    links = []
    for link in parent_element.getchildren():
        id = get_id_from_link(link)
        if id is not None:
            links.append(id)
        logger.info("%s => %s" % (link.tag, link.text))
    return links


def get_id_from_link_type(element):
    return None if element.tag != "link_type" else get_id_from_element(element)


def get_id_from_link(element):
    return None if element.tag != "link" else get_id_from_element(element)


def get_id_from_element(element):
    return None if element.get('id') is None else try_parse_int(element.get('id'))


def does_element_contain_allowed_link_types_tag(element):
    return element.tag == "allowed_link_types"


def does_element_contain_link_types_tag(element):
    return element.tag == "link_type"


def try_parse_int(s, base=10, val=None):
    try:
        return int(s, base)
    except ValueError:
        return val
