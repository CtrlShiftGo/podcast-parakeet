#!/usr/bin/env python

import math
import sys
import urllib2
from datetime import datetime
from lxml import etree

class Epsiode(object):
    def __init__(self, duration, pubDate):
        self.duration = duration
        date_string = pubDate.split(" ")[0:-2]
        date_string = " ".join(date_string)
        self.pubDate = datetime.strptime(date_string, "%a, %d %b %Y")
        # print type(self.pubDate)

def calc_podcast_rate(episode_list):
  rate_array = []
  end_date = datetime.today()
  for episode in episode_list:
    period = end_date - episode.pubDate
    rate = episode.duration/period.days
    rate_array.append_rate
    end_date = episode.pubDate
  return rate_array

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
    url = url[1:-1]
    print url
    parse_url(url)
