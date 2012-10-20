Highest-mountains-Google-map-visualizer
=======================================

This python module parses XML link of wikipedia and generates KML file which can be uploaded on Google map to see the marking of list of highest mountains of the word on Google Map.

Description
===========

Wikipedia gives a tabular list of highest mountains of the world here: http://en.wikipedia.org/wiki/List_of_highest_mountains#List . But does not allow bots to scrape their pages directly so XML format of wiki page available on MediaWiki API (http://en.wikipedia.org/w/api.php?action=parse&prop=text&format=xml&page=List_of_highest_mountains) was used.

Installation
============

Run this command to install: python3 mountains.py install . This will produce mountains.kml file. Go to google map and click on 'create map', upload this KML file there and save map. You can easily see marking on map there. You can also visit my google map link here: https://maps.google.com/maps/ms?msid=217071541089558915301.0004cc7857954c7979f30&msa=0&ll=34.488448,81.606445&spn=20.474617,43.286133&iwloc=0004cc785854cb208075b