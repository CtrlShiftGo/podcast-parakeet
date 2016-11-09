#!/usr/bin/env python

import math
import sys
import urllib2
from lxml import etree

def parse_url(url):
    socket = urllib2.urlopen(url)
    raw_xml = socket.read()
    parsed_xml = etree.fromstring(raw_xml)

    for episode in parsed_xml[0].findall('item'):
        print episode.find('title').text
        print episode.find('itunes:duration', parsed_xml.nsmap).text
        print episode.find('pubDate').text

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: ./podcastAnalyzer.py \"URL\""
        sys.exit(1)

    url = sys.argv[1]
    if url[0] != '"' or url[-1:] != '"':
        print "Error: The URL must be surrounded by quotation marks."
        sys.exit(1)

    parse_url(url)
