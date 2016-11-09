import math
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
