#    Author      : Abhay Jain
#    Language    : Python3.2
#    File        : mountains.py
#    Description : This module parses the XML format of wikipedia page (List of highest mountains)
#            to find list of highest peaks of the world and saves them in a KML file format.
#
##-----------------------------------------------------------------------------------------------------

import urllib.request
import types
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup

current_rank = '0'

def generate_soup(url):
    """ Function takes as input a web url, opens it
        convert it into HTML format and beautifies
        using BeautifulSoup libraries """
    
    socket = urllib.request.urlopen(url)
    html_page = socket.read()
    return BeautifulSoup(html_page)

def get_peak_color(rank):
    """ For given rank as input, this function
        returns the color to be displayed in KML
        file """
    rank = int(rank)
    if rank > 75:
        ## Green color if rank > 75
        return 'cc008000'
    elif rank > 50:
        ## Red color if rank > 50
        return 'ccFF0000'
    elif rank > 25:
        ## Lime color if rank > 25
        return 'cc00FF00'
    else:
        ## Blue color if rank <= 25
        return 'cc0000FF'


def get_peak_info(peak):
    """ This is main utility function which does actual
        parsing of XML data for a peak. For given table row
        it finds name, coordinates, rank of peak in that row
        and calls other function to format in KML """
    
    global current_rank
    rank = peak[0].text
    
    if rank == 'Rank':
        ## This is first row of table which contains heading of columns
        return ''
    else:
        if rank == None:
            ## Few rows of wiki table dont have rank column because height of this
            ## peak is almost same as peak above it, so its rank is taken same as
            ## the rank of peak above it
            rank = current_rank
        else:
            ## Otherwise update the current peak rank
            current_rank = rank
            
        color = get_peak_color(rank)
        name = peak[1].findall("./a[@title]")[0].text
        coordinates = (peak[5].findall(".//span[@class='geo']")[0].text).split('; ')
        
        xml_peak_info = peak_info_in_xml(color, name, coordinates)
        return xml_peak_info


def peak_info_in_xml(color, name, coordinates):
    """ This function takes as input the color, name and coordinates
        of peak. It generates tags like <name>, <coordinates>, <Style>, <Placemark>
        etc for this given peak. It returns <Placemark> element which will be saved
        in KML file as the marker of this peak for Google Map """
    
    xml_peak_linestyle = '\t\t\t\t<LineStyle>\n\t\t\t\t\t<color>' + color + '</color>\n\t\t\t\t\t<width>5.0</width>\n\t\t\t\t</LineStyle>\n'
    xml_peak_style = '\t\t\t<Style>\n' + xml_peak_linestyle + '\t\t\t</Style>\n'
    xml_peak_name = '\t\t\t<name>' + name + '</name>\n'
    xml_peak_coordinates = '\t\t\t\t<coordinates>' + coordinates[1] + ',' + coordinates[0] + ',0</coordinates>\n'
    xml_peak_point = '\t\t\t<Point>\n' + xml_peak_coordinates + '\t\t\t</Point>\n'
    xml_peak_placemark = '\t\t<Placemark>\n' + xml_peak_style + xml_peak_name + xml_peak_point + '\t\t</Placemark>\n'
    return xml_peak_placemark


# Wikipedia url for 'List of Highest Mountains' in XML format
wiki_url = 'http://en.wikipedia.org/w/api.php?action=parse&prop=text&format=xml&page=List_of_highest_mountains'
url_soup = generate_soup(wiki_url)

# Added a root tag for XML file to be parsed by ElementTree python module
wiki_xml = '<data>' + url_soup.text + '</data>'
root = ET.fromstring(wiki_xml)

# Parsed ranking Table from XML page of wikipedia
wiki_table=root.findall("./table[@class='wikitable sortable']")

# Saved header info in KML file
file_obj = open('mountains.kml', 'w')
kml_header = '<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://earth.google.com/kml/2.0">\n\t<Folder>\n'
kml_name = '\t\t<name>\n\t\t\tPeaks of highest mountains visualizer\n\t\t</name>\n'
file_obj.write(kml_header)
file_obj.write(kml_name)

# Generate info XML for each peak and save in KML file
for ranking_table in wiki_table:
    for row in ranking_table:
        td_list = row.findall("./td")
        if len(td_list) >= 6:
            info = get_peak_info(td_list)
            file_obj.write(info)

# Finally add footer for KML file and close it
kml_footer = '\t</Folder>\n</kml>'
file_obj.write(kml_footer)
file_obj.close()
