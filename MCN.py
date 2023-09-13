import requests
from bs4 import BeautifulSoup
import json;
import config

url = "https://motocampnerd.com/pages/motorcycle-campgrounds"
  
# raw HTML content
html_content = requests.get(url).text

# Parse the html content using any parser 
soup = BeautifulSoup(html_content,"html.parser")

links = soup.select('main p a')

points = []

searchBase = "https://maps.googleapis.com/maps/api/geocode/json?key="+config.GOOGLE_API_KEY+"&address="

links.pop(0)

nonBreakSpace = u'\xa0'

for link in links:
    point = {
        "name": link.text.replace("’", "'").replace("–", "-").replace(nonBreakSpace, ' '),
        "website": link['href']
    }

    if len(point["name"]) != 0:
        search = point["name"].replace(' ','+')
        searchUri = searchBase+search
        response = requests.get(searchUri).text
        data = json.loads(response)

        if(len(data["results"]) > 0):
            coords = data["results"][0]["geometry"]["location"]

            point["lat"] = coords["lat"]
            point["long"] = coords["lng"]

            points.append(point)


f = open("MCN.gpx", "w")

header = """<?xml version="1.0" encoding="utf-8"?><gpx creator="PoppedBit" version="1.1" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd http://www.garmin.com/xmlschemas/WaypointExtension/v1 http://www8.garmin.com/xmlschemas/WaypointExtensionv1.xsd http://www.garmin.com/xmlschemas/TrackPointExtension/v1 http://www.garmin.com/xmlschemas/TrackPointExtensionv1.xsd http://www.garmin.com/xmlschemas/GpxExtensions/v3 http://www8.garmin.com/xmlschemas/GpxExtensionsv3.xsd http://www.garmin.com/xmlschemas/ActivityExtension/v1 http://www8.garmin.com/xmlschemas/ActivityExtensionv1.xsd http://www.garmin.com/xmlschemas/AdventuresExtensions/v1 http://www8.garmin.com/xmlschemas/AdventuresExtensionv1.xsd http://www.garmin.com/xmlschemas/PressureExtension/v1 http://www.garmin.com/xmlschemas/PressureExtensionv1.xsd http://www.garmin.com/xmlschemas/TripExtensions/v1 http://www.garmin.com/xmlschemas/TripExtensionsv1.xsd http://www.garmin.com/xmlschemas/TripMetaDataExtensions/v1 http://www.garmin.com/xmlschemas/TripMetaDataExtensionsv1.xsd http://www.garmin.com/xmlschemas/ViaPointTransportationModeExtensions/v1 http://www.garmin.com/xmlschemas/ViaPointTransportationModeExtensionsv1.xsd http://www.garmin.com/xmlschemas/CreationTimeExtension/v1 http://www.garmin.com/xmlschemas/CreationTimeExtensionsv1.xsd http://www.garmin.com/xmlschemas/AccelerationExtension/v1 http://www.garmin.com/xmlschemas/AccelerationExtensionv1.xsd http://www.garmin.com/xmlschemas/PowerExtension/v1 http://www.garmin.com/xmlschemas/PowerExtensionv1.xsd http://www.garmin.com/xmlschemas/VideoExtension/v1 http://www.garmin.com/xmlschemas/VideoExtensionv1.xsd" xmlns="http://www.topografix.com/GPX/1/1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:wptx1="http://www.garmin.com/xmlschemas/WaypointExtension/v1" xmlns:gpxtrx="http://www.garmin.com/xmlschemas/GpxExtensions/v3" xmlns:gpxtpx="http://www.garmin.com/xmlschemas/TrackPointExtension/v1" xmlns:gpxx="http://www.garmin.com/xmlschemas/GpxExtensions/v3" xmlns:trp="http://www.garmin.com/xmlschemas/TripExtensions/v1" xmlns:adv="http://www.garmin.com/xmlschemas/AdventuresExtensions/v1" xmlns:prs="http://www.garmin.com/xmlschemas/PressureExtension/v1" xmlns:tmd="http://www.garmin.com/xmlschemas/TripMetaDataExtensions/v1" xmlns:vptm="http://www.garmin.com/xmlschemas/ViaPointTransportationModeExtensions/v1" xmlns:ctx="http://www.garmin.com/xmlschemas/CreationTimeExtension/v1" xmlns:gpxacc="http://www.garmin.com/xmlschemas/AccelerationExtension/v1" xmlns:gpxpx="http://www.garmin.com/xmlschemas/PowerExtension/v1" xmlns:vidx1="http://www.garmin.com/xmlschemas/VideoExtension/v1">
    <metadata>
        <link href="http://www.poppedbit.com">
            <text>Garmin International</text>
        </link>
        <time>2023-09-12T21:37:03Z</time>
        <bounds maxlat="45.65348569303751" maxlon="-114.7166636120528" minlat="45.65348569303751" minlon="-114.7166636120528" />
    </metadata>"""

gpx = []
for point in points:
    pointGPX = """
        <wpt lat=\""""+str(point["lat"])+"""\" lon=\""""+str(point["long"])+"""\">
            <time>2023-09-12T21:36:04Z</time>
            <name>"""+point["name"]+"""</name>
            <sym>Campground</sym>
            <type>user</type>
            <extensions>
            <gpxx:WaypointExtension>
                <gpxx:DisplayMode>SymbolAndName</gpxx:DisplayMode>
            </gpxx:WaypointExtension>
            <wptx1:WaypointExtension>
                <wptx1:DisplayMode>SymbolAndName</wptx1:DisplayMode>
            </wptx1:WaypointExtension>
            <ctx:CreationTimeExtension>
                <ctx:CreationTime>2023-09-12T21:36:04Z</ctx:CreationTime>
            </ctx:CreationTimeExtension>
            </extensions>
        </wpt>
    """
    gpx.append(pointGPX)


footer = "</gpx>"

f.write(header + ' '.join(gpx) + footer)

f.close()
