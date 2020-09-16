import csv

from database_lib import *

with open('CS010_BLDC_FAN_JC.csv') as bom:
    bom_reader = csv.reader(bom, delimiter=',')
    header = next(bom_reader)
    print(header)
    for row in bom_reader:
        print(row[1])
        add_product()

