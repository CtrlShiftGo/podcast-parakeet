#!/usr/bin/env python

import math
import sys
import urllib2
from datetime import datetime
from lxml import etree

class Episode(object):
    def __init__(self, duration, pubDate):
        self.duration = duration.split(":")
        if len(self.duration) > 2:
            self.duration = float(int(self.duration[0]))*60 + float(int(self.duration[1])) + float(int(self.duration[2]))/60
        else:
            self.duration = float(int(self.duration[0])) + float(int(self.duration[1]))/60

        self.pubDate = pubDate.split(" ")[0:-2]
        self.pubDate = " ".join(self.pubDate)
        self.pubDate = datetime.strptime(self.pubDate, "%a, %d %b %Y")
        # print type(self.pubDate)

def calc_podcast_rate(episode_list):
    rate_array = []
    end_date = datetime.today()
    for episode in episode_list:
        period = end_date - episode.pubDate
        rate = episode.duration/period.days
        rate_array.append(rate * 7)
        end_date = episode.pubDate
    return rate_array

def parse_url(url):
    socket = urllib2.urlopen(url)
    raw_xml = socket.read()
    parsed_xml = etree.fromstring(raw_xml)

    if(parsed_xml.tag != "rss" and parsed_xml[0].tag != "channel"):
        print "Incorrect XML format."
        return 0

    episode_list = []
    for episode in parsed_xml[0].findall('item'):
        if(episode.find('itunes:duration', parsed_xml.nsmap) != None):
            duration = episode.find('itunes:duration', parsed_xml.nsmap).text
            pubDate = episode.find('pubDate').text
            new_episode = Episode(duration, pubDate)
            episode_list.append(new_episode)

    rate_array = calc_podcast_rate(episode_list)
    print sum(rate_array)/float(len(rate_array))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: ./podcastAnalyzer.py \"URL\""
        sys.exit(1)

    url = sys.argv[1]
    if url[0] != '"' or url[-1:] != '"':
        print "Error: The URL must be surrounded by quotation marks."
        sys.exit(1)
    url = url[1:-1]
    parse_url(url)
