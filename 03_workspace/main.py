#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##########################################################
# title:    BBS for Independence - data analysis using NLP
# subtitle: HSA in the ABC of Computational Text Analysis
# author:   Josias Bruderer, Universität Luzern
# date:     25. August 2021
# desc:
##########################################################

# Preparations [R1]
"""
The following lines of code is used for preparing our environment.
"""

# load the necessary libraries

import sys
import time
from pathlib import Path


project_path = Path.cwd()

# prepare to load project specific libraries
if project_path not in sys.path:
    sys.path.append(str(project_path))

# import modules
from modules import wrangler
from modules import helpers


# Data Wrangling [R2]
"""
In this section the required data is downloaded and preprocessed (f.E. unzipped).
The module data_wrangler will be used for this.
"""

number_of_threads = 16
data_url = "http://archives.textfiles.com/[name].zip"
data_names = ["100"]
"""
data_names_exclude = ["fidonet-on-the-internet"]

# to use the full list: 
data_names = ["100", "adventure", "anarchy", "apple", "art", "artifacts", "bbs", "computers", "conspiracy", "digest",
              "drugs", "etext", "exhibits", "floppies", "food", "fun", "games", "groups",
              "hacking", "hamradio", "history", "holiday", "humor", "internet", "law", "magazines", "media", "messages",
              "music", "news", "occult", "phreak", "piracy", "politics", "programming", "reports", "rpg", "science",
              "sex", "sf", "stories", "survival", "tap", "ufo", "uploads", "virus"]  # the categories to download
"""
data_dir = Path(project_path / "02_datasets/")
tmp_dir = Path(project_path / ".tmp/")

threads = []

# prepare the threads for loading data
for names in helpers.chunker_list(data_names, number_of_threads):
    threads.append(wrangler.loader(tmp_dir, data_dir, data_url, names))

# start all threads
for thread in threads:
    thread.start()

# wait for all threads to finish their work
running = True
while running:
    running = False
    for thread in threads:
        if thread.is_alive():
            running = True
            print("waiting for threads to finish...")
            time.sleep(1)

# prepare the threads for cleaning up stuff
threads = []
dataset = {}

# prepare the threads
for names in helpers.chunker_list(data_names, number_of_threads):
    threads.append(wrangler.cleaner(data_dir, names))

# start all threads
for thread in threads:
    thread.start()

# wait for all threads to finish their work
running = True
while running:
    running = False
    for thread in threads:
        if thread.is_alive():
            running = True
            print("waiting for threads to finish...")
            time.sleep(1)
        else:
            if thread.data:
                dataset.update(thread.data)
                for d in thread.data:
                    helpers.save_object(thread.data[d], tmp_dir.joinpath(str(d + ".pkl")))

helpers.save_object(dataset, tmp_dir.joinpath("dataset.pkl"))

# write metadata to csv file
print("Write dataset to csv")
f = open(tmp_dir.joinpath("dataset.csv"), "w+")
f.write("category,name,path,length,length_raw,avgcolumnsize,charratioA,charratioB,year,eyear,lyear,type\r\n")
for d in dataset:
    for item in dataset[d]:
        f.write("\"" + d + "\",\"" + str(item["metadata"]["name"])+"\",\""+
                str(item["metadata"]["path"])+"\","+
                str(item["metadata"]["length"])+","+
                str(item["metadata"]["length_raw"])+","+
                str(item["metadata"]["avgcolumnsize"])+","+
                str(item["metadata"]["charratioA"])+","+
                str(item["metadata"]["charratioB"])+",\""+
                str(item["metadata"]["year"])+"\","+
                str(item["metadata"]["eyear"])+","+
                str(item["metadata"]["lyear"])+",\""+
                str(item["metadata"]["type"])+"\"\r\n")
f.close()

print("data downloaded successfully")