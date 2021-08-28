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
import textacy
import spacy
#run: ./.envs/bin/python -m spacy download en_core_web_sm


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

number_of_threads = 24
skip_steps = ["download", "cleaning", "metadata-filtering"]
data_url = "http://archives.textfiles.com/[name].zip"
data_names = ["100", "adventure", "anarchy", "apple", "art", "artifacts", "bbs", "computers", "conspiracy", "digest",
              "drugs", "etext", "exhibits", "floppies", "food", "fun", "games", "groups", "hacking", "hamradio",
              "history", "holiday", "humor", "internet", "law", "magazines", "media", "messages", "music", "news",
              "occult", "phreak", "piracy", "politics", "programming", "reports", "rpg", "science", "sex", "sf",
              "stories", "survival", "tap", "ufo", "uploads", "virus", "fidonet-on-the-internet"]  # categories to download
data_names_exclude = ["fidonet-on-the-internet", "tap", "floppies", "exhibits", "artifacts",
                      "piracy", "art"] # categories that are excluded and removed from data_names
file_filter = "^.*(\.(jpe?g|png|gif|bmp|zip|mp3|wav))|index\.html?$" # use this to exlude by filenames
metadata_file_filter = "x['metadata']['charratioB'] > 0.95" #
data_dir = Path(project_path / "02_datasets/")
tmp_dir = Path(project_path / ".tmp/")

threads = []

if "download" not in skip_steps:
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

    print("data downloaded successfully")

if "cleaning" not in skip_steps:
    # prepare the threads for cleaning up stuff
    threads = []
    dataset = {}

    # prepare the threads
    for names in helpers.chunker_list(data_names, number_of_threads):
        threads.append(wrangler.cleaner(data_dir, names, file_filter))

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

    helpers.save_object(dataset, tmp_dir.joinpath("dataset_full.pkl"))

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

    print("data cleaned successfully")
elif "metadata-filtering" not in skip_steps:
    # load dataset_full.pkl because it was not generate during runtime
    dataset = helpers.load_object(tmp_dir.joinpath("dataset_full.pkl"))
    print("data loaded from dataset_full.pkl")

if "metadata-filtering" not in skip_steps:
    for key in data_names_exclude:
        if key in dataset:
            del dataset[key]

    for key in dataset:
        d_tmp = []
        for x in dataset[key]:
            if eval(metadata_file_filter):
                d_tmp.append(x)
        dataset[key] = d_tmp

    helpers.save_object(dataset, tmp_dir.joinpath("dataset_filtered.pkl"))
elif "modeling" not in skip_steps:
    # load dataset_filtered.pkl because it was not generate during runtime
    dataset = helpers.load_object(tmp_dir.joinpath("dataset_filtered.pkl"))
    print("data loaded from dataset_filtered.pkl")

if "modeling" not in skip_steps:
    print("lets get modeling started")

    en = textacy.load_spacy_lang("en_core_web_sm")

    # create corpus from processed documents
    corpus = textacy.Corpus(en, data=None)
    for key in dataset:
        for d in dataset[key]:
            corpus.add(textacy.make_spacy_doc((d["content"], d["metadata"]), lang="en_core_web_sm"))

    print("corpus loaded")
    corpus.save(tmp_dir.joinpath("corpus.bin.gz"))
elif "analysis" not in skip_steps:
    # load corpus.bin.gz because it was not generate during runtime
    corpus = textacy.Corpus.load("en_core_web_sm", tmp_dir.joinpath("corpus.bin.gz"))
    print("data loaded from corpus.bin.gz")

if "analysis" not in skip_steps:
    # get lowercased and filtered corpus vocabulary (R3.3.1)
    vocab = corpus.word_counts(by='lemma_', filter_stops = True, filter_punct = True, filter_nums = True)

    # sort vocabulary by descending frequency
    vocab_sorted = sorted(vocab.items(), key=lambda x: x[1], reverse=True)

    # write to file, one word and its frequency per line
    with open(tmp_dir.joinpath('vocab_frq.txt'), 'w') as f:
        for word, frq in vocab_sorted:
            line = f"{word}\t{frq}\n"
            f.write(line)
