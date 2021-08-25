#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##########################################################
# title:  datawrangler
# author: Josias Bruderer
# date:   26.05.2021
# desc:   this module takes care of all tasks that are
#         related to juggling files and datasets.
##########################################################

import os
import sys
from threading import Thread
from pathlib import Path
import requests
import zipfile
import codecs
import re


def averageLen(lst, excludeEmpty=True):
    if excludeEmpty:
        lengths = [len(i) for i in lst if i != "" and i != " "]
    else:
        lengths = [len(i) for i in lst]
    return 0 if len(lengths) == 0 else round((float(sum(lengths)) / len(lengths)), 2)


def daterange(lst, t="r"):
    ltmp = []
    ltmp2 = []
    if len(lst) > 0:
        for l in lst:
            ltmp += list(filter(None, l))
        for l in ltmp:
            if len(l) == 2:
                ltmp2 += ["19" + l]
            else:
                ltmp2 += [l]
        if len(ltmp2) > 2:
            if t == "e":
                return str(min(ltmp2))
            elif t == "l":
                return str(max(ltmp2))
            else:
                return str(min(ltmp2) + "-" + max(ltmp2))
        else:
            return str(ltmp2[0])
    else:
        return "nd."

class cleaner(Thread):

    def __init__(self, data_dir, data_names):
        Thread.__init__(self)
        self.data_dir = data_dir
        self.data_names = data_names
        self.data = []

    def run(self):
        for data_name in self.data_names:
            self.data = self.get_texts(Path(self.data_dir, data_name))

    def get_texts(self, dir_texts):
        """
        Sequentially stream all documents from a given folder,
        including metadata.
        """
        data = []

        # iterate over all documents
        for fname in dir_texts.glob('**/*'):  # ** = all subdirectories
            if Path(fname).is_file():
                print("processing in " + str(dir_texts.stem) + " file: " + str(fname))
                # Read file content and replace encoding erros
                content_raw = codecs.open(fname, 'r', encoding='utf-8', errors='replace').read()

                # join lines as there are hard line-breaks
                content = content_raw.replace('\r\n', ' ')
                content = content.replace('\r', ' ')
                content = content.replace('\n', ' ')
                content = content.replace('\t', ' ')
                content = content.replace('\x1a', ' ')
                content = re.sub('[^A-z0-9\ \.\'\,\!]', ' ', content)
                content = re.sub('[\\\\\^\[\]]', ' ', content)

                # add more metadata here if needed
                if len(re.findall("[^A-z]", content_raw)) == 0:
                    charratioA = 0
                else:
                    charratioA = round(len(re.findall("[A-z]", content_raw))
                                       / len(re.findall("[^A-z]", content_raw)), 2)

                if len(re.findall("[^A-z\ \.\"\,\!]", content_raw)) == 0:
                    charratioB = 0
                else:
                    charratioB = round(len(re.findall("[A-z\ \.\"\,\!]", content_raw))
                                       / len(re.findall("[^A-z\ \.\"\,\!]", content_raw)), 2)
                typ = "textfile"
                if fname.name == "declarationbarlow1996.txt":
                    typ = "declaration"

                rxdate = re.compile(
                    'copyright.{0,3}(19[6-9][0-9])|updated.{0,3}[0-1]?[0-9]?-[0-3]?[0-9]?-([6-9][0-9])|Date\:.*([6-9][0-9]).*,|(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|june|july|aug(?:ust)?|sept(?:ember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?).{0,8}(1?9?[6-9][0-9])|[0-1]?[0-9]?\/[0-3]?[0-9]?\/([6-9][0-9])|[0-1]?[0-9]?-[0-3]?[0-9]?-([6-9][0-9])|[^-](19[6-9][0-9])')

                matches = rxdate.findall(content, re.IGNORECASE)

                metadata = {'name': fname.name,
                            'length_raw': len(content_raw),
                            'length': len(content),
                            'avgcolumnsize': averageLen(content_raw.splitlines()),
                            'charratioA': charratioA,
                            'charratioB': charratioB,
                            'year': daterange(matches),
                            'eyear': daterange(matches, "e"),
                            'lyear': daterange(matches, "l"),
                            'type': typ
                            }

                # return documents one after another (sequentially)
                data.append({"content": content, "metadata": metadata})
        return data

class loader(Thread):

    def __init__(self, tmp_dir, data_dir, data_url, data_names):
        Thread.__init__(self)
        self.tmp_dir = tmp_dir
        self.data_dir = data_dir
        self.data_url = data_url
        self.data_names = data_names
        self.init()

    def init(self):
        try:
            # create tmp directory if not existing yet
            if not os.path.exists(self.tmp_dir.is_dir()):
                os.mkdir(self.tmp_dir)

            # create data directory if not existing yet
            if not os.path.exists(self.data_dir):
                os.mkdir(self.data_dir)
        except:
            print("Unexpected error: ", sys.exc_info()[0])
            raise

    def run(self):
        for data_name in self.data_names:
            url = self.data_url.replace("[name]", data_name)
            zipdir = Path(self.tmp_dir, str(data_name + ".zip"))
            self.download_zip(url, zipdir)
            self.extract_zip(zipdir)

    def download_zip(self, url, zipdir):
        try:
            if not zipdir.is_file():
                print("Downloading: " + url)
                r = requests.get(url, allow_redirects=True)
                open(zipdir, 'wb').write(r.content)
            else:
                print("Skip downloading, file already downloaded: " + url)
        except:
            print("Unexpected error: ", sys.exc_info()[0])
            raise

    def extract_zip(self, zipdir):
        try:
            if not Path(self.data_dir / zipdir.stem).is_dir():
                print("Extracting: " + str(zipdir))
                with zipfile.ZipFile(zipdir, 'r') as zip_ref:
                    zip_ref.extractall(self.data_dir)
            else:
                print("Skip extracting, file already extracted: " + str(zipdir))
        except:
            print("Unexpected error: ", sys.exc_info()[0])
            raise
