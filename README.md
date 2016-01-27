`wundergroundloader.py` is a script to automate the downloading of wether data from www.wunderground.com

Note: wunderground will block your IP if you download more than one file per 6 seconds, hence the 7 second sleep command at the end of this script.

## Usage

```
wundergroundloader.py [options]

Options:
  -h, --help            show this help message and exit
  -l PHL, --location=PHL
                        Location - Airport Code
  -s 2014-01-31, --start=2014-01-31
                        Start date.
  -e 2014-12-31, --end=2014-12-31
                        End date.
  -d ~/weatherdata, --dir=~/weatherdata
                        Save Directory (defaults to current dir)
```
