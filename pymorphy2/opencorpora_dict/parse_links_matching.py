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

    page = etree.parse(filename)
    root = page.getroot()
    print(root)
    if root.tag == "allowed_link_types":
        print(root.getchildren())
        for allowed_link_type in root.getchildren():
            links = []
            if allowed_link_type.tag == "link_type":
                id = int(allowed_link_type.get('id'))
                allowed_link_types[id] = links
                for link in allowed_link_type.getchildren():
                    id = int(link.get('id'))
                    links.append(id)
                    print("%s => %s" % (link.tag, link.text))
                print()
    print(allowed_link_types)
    return allowed_link_types
