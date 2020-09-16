import csv

from database_lib import *

DBM = DBmanager(restart=0)


with open('CS010_BLDC_FAN_JC.csv') as bom:
    bom_reader = csv.reader(bom, delimiter=',')
    header = next(bom_reader)
    #for el in header:
    #    print(".",el.strip(),". -> ", header.index(el))
    #print(header)
    for row in bom_reader:
        #print(len(row))
        DBM.add_product(
                42, #row[11], #header.index(' Manufacturer_Part_Number '),
                row[0], #.index(' Description '),
                row[2], #.index(' Footprint '),
                row[1], #.index(' Value '),
                row[3]
                )

    DBM.search_cassetto(forma=1)
DBM.close()
