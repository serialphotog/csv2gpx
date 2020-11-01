import argparse
import csv
import logging
import os
import sys
import xml.etree.ElementTree as ET

# Configure the logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def getYesNo(question, default="yes"):
    """
    Prompts the user for a Yes/No answer.
    """
    valid = {"yes": True, "y": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif prompt == "yes":
        prompt = " [Y/n] "
    elif dfault == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("Invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()

        if default is None and choice == '':
            return valid[default]
        elif choice is valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with a 'yes' or a 'no' (or 'y' or 'n').\n")

def parseCSV(csv_path):
    """
    Parses the waypoints out of a CSV file.
    This just assumes that the CSV is in a simple format:
    lat, lon, name

    There is currently no flexibility to this...
    """
    waypoints = [] # Stores the waypoints found in the CSV file
    rows = [] # Stores each data row from the CSV

    # Parse the CSV
    with open(csv_path, encoding='utf-8-sig') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            rows.append(row)

        logger.debug("Found %d data rows in %s" % (reader.line_num, csv_path))

    # Parse the waypoints
    for row in rows:
        waypoint = {}
        waypoint['lat'] = row[1]
        waypoint['lon'] = row[0]
        waypoint['name'] = row[2]

        # Skip malformed waypoints
        if waypoint['lat'] == '' or waypoint['lon'] == '' or waypoint['name'] == '':
            logger.debug("Skipping malformed waypoint: (%s, %s): %s" % (waypoint['lat'], waypoint['lon'], waypoint['name']))
            continue
        else:
            logger.debug("Parse waypoint: (%s, %s): %s" % (waypoint['lat'], waypoint['lon'], waypoint['name']))
            waypoints.append(waypoint)

    return waypoints

def convertCSV(csv_path, gpx_path, overwriteGPX=False):
    """
    Performs the conversion of a CSV file into a GPX file.
    """
    if os.path.isfile(gpx_path) and not overwriteGPX:
        logger.error(gpx_path + " already exists. Exiting...")
        sys.exit()
    if not os.path.isfile(csv_path):
        logger.error(csv_path + " does not exist. Exiting...")
        sys.exit()

    if os.path.isfile(gpx_path):
        os.remove(gpx_path)

    # Get the waypoints from the CSV file
    waypoints = parseCSV(csv_path)

    # Generate the GPX
    gpx_head = ET.Element('gpx')
    gpx_head.set('xmlns', 'http://www.topografix.com/GPX/1/1')
    gpx_head.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    gpx_head.set('xsi:schemaLocation', 'http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd')

    for waypoint in waypoints:
        waypoint_elem = ET.SubElement(gpx_head, 'wpt')
        waypoint_elem.set('lat', waypoint['lat'])
        waypoint_elem.set('lon', waypoint['lon'])
        name_elem = ET.SubElement(waypoint_elem, 'name')
        name_elem.text = waypoint['name']

    # Write the GPX file data to disk
    xml = ET.tostring(gpx_head)
    with open(gpx_path, "wb") as f:
        f.write(xml)

# Handle the command line args
parser = argparse.ArgumentParser(description="A simple utility to convert CSV files of GPS locations to a GPX file.")
parser.add_argument("--input", dest="csv_path", help="Path to the CSV file of locations")
parser.add_argument("--output", dest="gpx_path", help="Path to the generated GPX file.")
args = parser.parse_args()

# Rather or not to overwrite an existing GPX file
overwriteGPX = False

if not args.csv_path or not args.gpx_path:
    logger.error("You must supply an input and output!")
elif not os.path.isfile(args.csv_path):
    logger.error("The input CSV file " + args.csv_path + " does not exist")
elif os.path.isfile(args.gpx_path):
    if getYesNo("'%s' exists. Overwrite it?" % args.gpx_path):
        overwriteGPX = True
    else:
        sys.exit()
else:
    logger.info("Covnerting CSV file " + args.csv_path + " to a GPX file...")
    convertCSV(args.csv_path, args.gpx_path, overwriteGPX)
