#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##########################################################
# title:    pkl-to-csv
# author:   Josias Bruderer, Universität Luzern
# date:     27. August 2021
# desc:     converts pkl (pickle dump) to csv
#           Param1: input.pkl
#           Param2: output.csv
##########################################################

import sys
import time
from pathlib import Path


project_path = Path.cwd()

# prepare to load project specific libraries
if project_path not in sys.path:
    sys.path.append(str(project_path))

# import modules
from modules import helpers

tmp = helpers.load_object(sys.argv[1])

if tmp[0]["metadata"]:
    dataset = {}
    dataset["unknown"] = tmp
else:
    dataset = tmp

# write metadata to csv file
print("Write dataset to csv")
f = open(sys.argv[2], "w+")
f.write("category,name,length,length_raw,avgcolumnsize,charratioA,charratioB,year,eyear,lyear,type\r\n")
for d in dataset:
    for item in dataset[d]:
        f.write(d + "," + str(item["metadata"]["name"])+","+
                str(item["metadata"]["length"])+","+
                str(item["metadata"]["length_raw"])+","+
                str(item["metadata"]["avgcolumnsize"])+","+
                str(item["metadata"]["charratioA"])+","+
                str(item["metadata"]["charratioB"])+","+
                str(item["metadata"]["year"])+","+
                str(item["metadata"]["eyear"])+","+
                str(item["metadata"]["lyear"])+","+
                str(item["metadata"]["type"])+","+
                "\r\n")
f.close()

print("data downloaded successfully")