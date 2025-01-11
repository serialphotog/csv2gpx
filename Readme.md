# csv2gpx

**DEPRECATED:** This project is extremely old and, frankly, extremely flawed. I'm not going to be updating this, but I did create a much better tool that I recommend you use instead: [GPX Tools](https://github.com/serialphotog/GPX-Tools).

This is a super simple command line utility to fulfil an extremely niche usecase I had.

This utility will take a CSV file containing GPS coordinates and convert the file into a GPX file that can be imported into a GPS. Currently, this program just assumes that each waypoint is in the format of:
```
lat,lon,name
```

# Usage

```
$ python csv2gpx --input CSV_FILE.csv --output OUTPUT_FILE.gpx
```

# License

DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE Version 2, December 2004

Copyright (C) 2018 Adam Thompson adam@serialphotog.com

Everyone is permitted to copy and distribute verbatim or modified copies of this license document, and changing it is allowed as long as the name is changed.

```
 DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
 ```

TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
    0. You just DO WHAT THE FUCK YOU WANT TO.
