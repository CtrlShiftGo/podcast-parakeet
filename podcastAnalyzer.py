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
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    request = urllib2.Request(url, headers={'User-Agent':user_agent})
    parsed_xml = etree.fromstring(urllib2.urlopen(request).read())

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
    return (parsed_xml[0].find('title').text , sum(rate_array)/float(len(rate_array)))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: ./podcastAnalyzer.py \"URL\""
        sys.exit(1)

    rate_dictionary = {}
    for url in sys.argv[1:]:
        try:
            podcast_information = parse_url(url)
            rate_dictionary[podcast_information[0]] = podcast_information[1]
        except:
            print "Unable to parse: " + url

    # Display Ouput
    print
    total_minutes_per_week = 0
    for key, value in rate_dictionary.iteritems():
        print "{}:\n\t{:.2f} Minutes per Week".format(key, value)
        total_minutes_per_week += value
    print "Total:\n\t{:.2f} Minutes per Week".format(total_minutes_per_week)
