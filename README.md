# Tiquets [![Build Status](https://travis-ci.org/angellandros/tiquets.svg?branch=master)](https://travis-ci.org/angellandros/tiquets)
Interview Assignment

## Installation
The script works fine with following Python versions:
  - 2.6
  - 2.7
  - 3.3
  - 3.4
  - 3.5
  - 3.6
 
And it doesn't require any additional libraries to install.

## Usage
The usage manual of the script could be accessed through command line 
`python tiquets.py --help`: 

```
usage: tiquets.py [-h] [-o ORDERS] [-b BARCODES] [-O OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -o ORDERS, --orders ORDERS
                        CSV file containing data of orders, default=orders.csv
  -b BARCODES, --barcodes BARCODES
                        CSV file containing data of barcodes,
                        default=barcodes.csv
  -O OUTPUT, --output OUTPUT
                        output CSV file, default=output.csv
```

## DB Storage
A possible solution for storing the data in a database,
is to use a no-SQL DB, and have two collections analogous
to the CSV files that we have here, with an index on both
attributes of the barcode assignments.
