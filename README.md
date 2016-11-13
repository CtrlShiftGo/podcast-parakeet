# Podcast Analyzer

## Synopsis

Reads podcast RSS feeds to determine average number of minutes uploaded per week to better adjust listening habits. Optimize the number of podcasts to which you subscribe so as to never run out or fall behind in your listening.

## Example Usage and Output
```
./podcastAnalyzer.py http://www.hellointernet.fm/podcast?format=rss http://feeds.soundcloud.com/users/soundcloud:users:156542883/sounds.rss https://www.relay.fm/cortex/feed http://feeds.wnyc.org/radiolab http://feeds.wnyc.org/moreperfect http://feeds.99percentinvisible.org/99percentinvisible http://atp.fm/episodes?format=rss
Unable to parse: https://www.relay.fm/cortex/feed
Unable to parse: http://feeds.99percentinvisible.org/99percentinvisible

Dear Hank and John:
	47.77 Minutes per Week
Hello Internet:
	73.31 Minutes per Week
Accidental Tech Podcast:
	121.74 Minutes per Week
Radiolab:
	20.35 Minutes per Week
Radiolab Presents: More Perfect:
	39.02 Minutes per Week
Total:
	302.20 Minutes per Week
```

## Dependencies

* Python 2
* lxml

## Licencing

See `LICENCE` for details.
