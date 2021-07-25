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


class DataWrangler:
    def __init__(self, tmp_dir, data_dir):
        self.tmp_dir = tmp_dir
        self.data_dir = data_dir
        self.init()

    def init(self):
        try:
            # create tmp directory if not existing yet
            if not os.path.exists(self.tmp_dir):
                os.mkdir(self.tmp_dir)
        except:
            print("Unexpected error: ", sys.exc_info()[0])
            raise

        try:
            # create data directory if not existing yet
            if not os.path.exists(self.data_dir):
                os.mkdir(self.data_dir)
        except:
            print("Unexpected error: ", sys.exc_info()[0])
            raise

    def process_zip(self, data_url, name):
        try:
            # download zip file
            r = requests.get(data_url, allow_redirects=True)
            open(self.tmp_dir + "/" + name + ".zip", 'wb').write(r.content)
        except:
            print("Unexpected error: ", sys.exc_info()[0])
            raise

        try:
            # extract zip file to data directory
            with zipfile.ZipFile(self.tmp_dir + "/" + name + ".zip", 'r') as zip_ref:
                zip_ref.extractall(self.data_dir)
        except:
            print("Unexpected error: ", sys.exc_info()[0])
            raise

    def get_texts(self, dir_texts):
        """
        Sequentially stream all documents from a given folder,
        including metadata.
        """
        p = Path(dir_texts)  # set base dir

        # iterate over all documents
        for fname in p.glob('**/*'):  # ** = all subdirectories
            if Path(fname).is_file():
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
                charratioA = round(len(re.findall("[A-z]", content_raw)) / len(re.findall("[^A-z]", content_raw)), 2)
                charratioB = round(
                    len(re.findall("[A-z\ \.\"\,\!]", content_raw)) / len(re.findall("[^A-z\ \.\"\,\!]", content_raw)),
                    2)
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
                yield content, metadata
