import sys
import csv

gpxHeader = """<?xml version="1.0" encoding="utf-8"?><gpx creator="PoppedBit" version="1.1" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd http://www.garmin.com/xmlschemas/WaypointExtension/v1 http://www8.garmin.com/xmlschemas/WaypointExtensionv1.xsd http://www.garmin.com/xmlschemas/TrackPointExtension/v1 http://www.garmin.com/xmlschemas/TrackPointExtensionv1.xsd http://www.garmin.com/xmlschemas/GpxExtensions/v3 http://www8.garmin.com/xmlschemas/GpxExtensionsv3.xsd http://www.garmin.com/xmlschemas/ActivityExtension/v1 http://www8.garmin.com/xmlschemas/ActivityExtensionv1.xsd http://www.garmin.com/xmlschemas/AdventuresExtensions/v1 http://www8.garmin.com/xmlschemas/AdventuresExtensionv1.xsd http://www.garmin.com/xmlschemas/PressureExtension/v1 http://www.garmin.com/xmlschemas/PressureExtensionv1.xsd http://www.garmin.com/xmlschemas/TripExtensions/v1 http://www.garmin.com/xmlschemas/TripExtensionsv1.xsd http://www.garmin.com/xmlschemas/TripMetaDataExtensions/v1 http://www.garmin.com/xmlschemas/TripMetaDataExtensionsv1.xsd http://www.garmin.com/xmlschemas/ViaPointTransportationModeExtensions/v1 http://www.garmin.com/xmlschemas/ViaPointTransportationModeExtensionsv1.xsd http://www.garmin.com/xmlschemas/CreationTimeExtension/v1 http://www.garmin.com/xmlschemas/CreationTimeExtensionsv1.xsd http://www.garmin.com/xmlschemas/AccelerationExtension/v1 http://www.garmin.com/xmlschemas/AccelerationExtensionv1.xsd http://www.garmin.com/xmlschemas/PowerExtension/v1 http://www.garmin.com/xmlschemas/PowerExtensionv1.xsd http://www.garmin.com/xmlschemas/VideoExtension/v1 http://www.garmin.com/xmlschemas/VideoExtensionv1.xsd" xmlns="http://www.topografix.com/GPX/1/1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:wptx1="http://www.garmin.com/xmlschemas/WaypointExtension/v1" xmlns:gpxtrx="http://www.garmin.com/xmlschemas/GpxExtensions/v3" xmlns:gpxtpx="http://www.garmin.com/xmlschemas/TrackPointExtension/v1" xmlns:gpxx="http://www.garmin.com/xmlschemas/GpxExtensions/v3" xmlns:trp="http://www.garmin.com/xmlschemas/TripExtensions/v1" xmlns:adv="http://www.garmin.com/xmlschemas/AdventuresExtensions/v1" xmlns:prs="http://www.garmin.com/xmlschemas/PressureExtension/v1" xmlns:tmd="http://www.garmin.com/xmlschemas/TripMetaDataExtensions/v1" xmlns:vptm="http://www.garmin.com/xmlschemas/ViaPointTransportationModeExtensions/v1" xmlns:ctx="http://www.garmin.com/xmlschemas/CreationTimeExtension/v1" xmlns:gpxacc="http://www.garmin.com/xmlschemas/AccelerationExtension/v1" xmlns:gpxpx="http://www.garmin.com/xmlschemas/PowerExtension/v1" xmlns:vidx1="http://www.garmin.com/xmlschemas/VideoExtension/v1">
    <metadata>
        <link href="http://www.poppedbit.com">
            <text>Garmin International</text>
        </link>
        <time>2023-09-12T21:37:03Z</time>
        <bounds maxlat="45.65348569303751" maxlon="-114.7166636120528" minlat="45.65348569303751" minlon="-114.7166636120528" />
    </metadata>"""

gpxFooter = "</gpx>"

class Campsite:
    def __init__(
        self, 
        name, 
        address, 
        city, 
        state, 
        zip, 
        latitude,
        longitude,
        phone,
        website,
        amenities,
        notes
    ):
        self.name  = name
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.latitude = latitude
        self.longitude = longitude
        self.phone = phone
        self.website = website
        self.amenities = amenities
        self.notes = notes

def getCampsitesFromCSV(fileName = "campgrounds.csv"):
    campsites = []
    with open(fileName, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(reader)
        for row in reader:
            campsites.append(Campsite(
                row[2].strip(), 
                row[3].strip(),
                row[4].strip(),
                row[5].strip(),
                row[6].strip(),
                (float)(row[7].split(",")[0].strip()),
                (float)(row[7].split(",")[1].strip()),
                row[8].strip(),
                row[9].strip(),
                row[10].strip(),
                row[11].strip()
            ))
    return campsites
            
def getWaypointsFromCampsites(campsites = []):
    waypoints = []
    for campsite in campsites:
        waypoint = """
            <wpt lat=\""""+str(campsite.latitude)+"""\" lon=\""""+str(campsite.longitude)+"""\">
                <time>2023-09-12T21:36:04Z</time>
                <name>"""+campsite.name+"""</name>
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
        waypoints.append(waypoint)
    return waypoints

def writeWaypointsToGPX(waypoints = [], gpxFile = ""):
    f = open(gpxFile, "w")
    f.write(gpxHeader + ' '.join(waypoints) + gpxFooter)
    f.close()

if __name__ == "__main__":
    campsitesCSV = sys.argv[1]
    gpxFile = sys.argv[2]

    campsites = getCampsitesFromCSV(campsitesCSV)
    waypoints = getWaypointsFromCampsites(campsites)
    writeWaypointsToGPX(waypoints, gpxFile)

