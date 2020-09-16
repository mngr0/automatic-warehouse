import csv

from database_lib import *

DBM = DBmanager()
DBM.create_db()


with open('CS010_BLDC_FAN_JC.csv') as bom:
    bom_reader = csv.reader(bom, delimiter=',')
    header = next(bom_reader)
    print(header)
    for row in bom_reader:
        print(len(row))
        print("row=",row)
        DBM.add_product(
                42, #row[11], #header.index(' Manufacturer_Part_Number '),
                row[0], #.index(' Description '),
                row[2], #.index(' Footprint '),
                row[1], #.index(' Value '),
                row[3]
                )

