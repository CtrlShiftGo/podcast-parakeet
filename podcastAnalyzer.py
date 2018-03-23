#!/usr/bin/env python

import math
import sys
import urllib2
from datetime import datetime
from lxml import etree
import traceback

fileMode = False

class Episode(object):
    def __init__(self, duration, pubDate):
        if(":" in duration):
            # Check for colon separated date format
            self.duration = duration.split(":")
            if len(self.duration) > 2:
                self.duration = float(int(self.duration[0]))*60 + float(int(self.duration[1])) + float(int(self.duration[2]))/60
            else:
                self.duration = float(int(self.duration[0])) + float(int(self.duration[1]))/60
        else:
            # Assuming time format is in seconds
            self.duration = float(duration)/60
        self.pubDate = pubDate.split(" ")[0:-2]
        self.pubDate = " ".join(self.pubDate)
        self.pubDate = datetime.strptime(self.pubDate, "%a, %d %b %Y")

def calc_podcast_rate(episode_list):
    rate_array = []
    end_date = datetime.today()
    SECONDS_IN_DAY = 86400.0
    for episode in episode_list:
        period = end_date - episode.pubDate
        if(period.total_seconds() > 0):
            rate = episode.duration/(period.total_seconds()/SECONDS_IN_DAY)
            rate_array.append(rate * 7)
            end_date = episode.pubDate
    return rate_array

def parse_url(url):
    user_agent = 'podcast-parakeet/0.1.0 (+https://github.com/CtrlShiftGo/podcast-parakeet)'
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

def read_custom_podfile(textFile, rate_dictionary):
    for line in textFile:
                try:
                    line = line.strip("\n")
                    if(line[0] != "#"):
                        podcast_information = parse_url(line)
                        rate_dictionary[podcast_information[0]] = podcast_information[1]
                except Exception, e:
                    print "Unable to parse: " + str(line)
                    if(debugMode):
                        traceback.print_exc()
                        print "============================================="

def read_opml(opmlFile, rate_dictionary):
    return 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: ./podcastAnalyzer.py \"URL\""
        sys.exit(1)

    # Parse command list
    rate_dictionary = {}
    debugMode = False
    for command in sys.argv[1:]:
        if(command == "-v" or command == "--verbose"):
            debugMode = True
            sys.argv.remove(command)
        elif(command == "-f" or command == "--verbose"):
            fileMode = True
            sys.argv.remove(command)
    # Opens file
    if(fileMode):
        for fileName in sys.argv[1:]:
            # Determine filetype
            textFile = open(fileName)
            read_custom_podfile(textFile, rate_dictionary)
    else:
        for url in sys.argv[1:]:
            try:
                podcast_information = parse_url(url)
                rate_dictionary[podcast_information[0]] = podcast_information[1]
            except Exception, e:
                print "Unable to parse: " + str(url)
                if(debugMode):
                    traceback.print_exc()
                    print "============================================="

    # Display Ouput
    print
    total_minutes_per_week = 0
    for key, value in rate_dictionary.iteritems():
        print "{}:\n\t{:.2f} Minutes per Week".format(key, value)
        total_minutes_per_week += value
    print "\nTotal:\n\t{:.2f} Minutes per Week".format(total_minutes_per_week)
    print "\t{:.0f}h {:.0f}m".format(total_minutes_per_week/60, total_minutes_per_week%60)
