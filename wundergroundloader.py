#!/bin/env python
import requests
from string import Template
from optparse import OptionParser
from datetime import datetime
from datetime import timedelta
import logging
import os
import re
import time
import sys

logging.basicConfig()
logger = logging.getLogger('root')
logger.setLevel(logging.INFO)

weatherurl = Template("http://www.wunderground.com/history/airport/$airportcode/$year/$month/$day/DailyHistory.html?req_city=NA&req_state=NA&req_statename=NA&theprefset=SHOWMETAR&theprefvalue=1&format=1")

def parseOptions():
    parser = OptionParser()
    parser.add_option("-l", "--location", dest="location",
                     help="Location - Airport Code", metavar="PHL")
    parser.add_option("-s", "--start", dest="start",
                     help="Start date.", metavar="2014-01-31")
    parser.add_option("-e", "--end", dest="end",
                     help="End date.", metavar="2014-12-31")
    parser.add_option("-d", "--dir", dest="save_dir",
                     help="Save Directory (defaults to current dir)", metavar="~/weatherdata")
    parser.add_option("--strip-headers", action="store_true", dest="stripheaders",
                     help="Strip headers from downloaded csv files.")
# # if only 1 argument, it's the script name
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    return parser.parse_args()

def download_data(url):
    logger.info("Getting URL: %s" % url)
    r = requests.get(url)

    if r.status_code == requests.codes.ok:
        return r.text
    else:
        r.raise_for_status()

def save_data(date, data, location=None, stripheaders=False):
    if location is None:
        location = "."
    if not os.path.exists(os.path.join(location, str(date.year))):
        os.mkdir(os.path.join(location, str(date.year)))
    if not os.path.exists(os.path.join(location, str(date.year), str(date.month))):
        os.mkdir(os.path.join(location, str(date.year), str(date.month)))

    # strip headers for appended data
    if os.path.exists(os.path.join(location, str(date.year), str(date.month), "data.csv")):
        fileinfo = os.stat(os.path.join(location, str(date.year), str(date.month), "data.csv"))
        if fileinfo.st_size > 0:
            stripheaders=True

    logger.info("Saving data for %s" % date)
    data = data.split("\n")
    with open(os.path.join(location, str(date.year), str(date.month), "data.csv"), "a") as file:
        for line in data:
            if re.search("TemperatureF", line) and stripheaders:
                continue
            if line == '':
                continue
            file.write(line.strip("<br />")+"\n")


if __name__ == '__main__':
    (options, args) = parseOptions()

    start_date = datetime.strptime(options.start, '%Y-%m-%d')
    end_date = datetime.strptime(options.end, '%Y-%m-%d')

    current_date = start_date
    while current_date <= end_date:
        current_url = weatherurl.substitute(airportcode=options.location,
                                            year=current_date.year,
                                            month=current_date.month,
                                            day=current_date.day)
        try:
            data = download_data(current_url)
            save_data(current_date, data, options.save_dir, options.stripheaders)
        except requests.exceptions.HTTPError, e:
            logger.warn("Couldn't get data for date: %s, %s" % (current_date, e))
        except Exception, e:
            raise


        logger.info("...done")
        # Sleep so we don't get blocked by weather underground
        if current_date == end_date:
            sys.exit(0)
        else:
            time.sleep(7)

        current_date += timedelta(days=1)
