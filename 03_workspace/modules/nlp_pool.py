#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##########################################################
# title:  helpers
# author: Josias Bruderer
# date:   28.08.2021
# desc:   this module provides nlp functions
##########################################################

import textacy
import spacy
# run: ./.envs/bin/python -m spacy download en_core_web_sm


class PoolCorpus(object):

    def __init__(self):
        model = spacy.load('en_core_web_sm', disable=["parser"])
        model.max_length = 10000000  # enable utilization of ~ 100GB RAM
        self.corpus = textacy.corpus.Corpus(lang=model)
        self.totalFilesTarget = 1
        self.processedFiles = 0

    def add(self, data):
        self.corpus.add(data)
        self.processedFiles = self.processedFiles + 1
        print("Processed ", self.processedFiles, " of ", self.totalFilesTarget, "files: ",
              round(100/self.totalFilesTarget*self.processedFiles, 4), "%")

    def get(self):
        return self.corpus

    def save(self, path):
        self.corpus.save(path)

    def set_totalFilesTarget(self, n):
        self.totalFilesTarget = n

"""
texts = {
        'key1': 'First text 1.',
        'key2': 'Second text 2.',
        'key3': 'Third text 3.',
        'key4': 'Fourth text 4.',
    }

BaseManager.register('PoolCorpus', PoolCorpus)

if __name__ == '__main__':
    with BaseManager() as manager:
        corpus = manager.PoolCorpus()

        with Pool(processes=2) as pool:
            pool.map(corpus.add, ((v, {'key': k}) for k, v in texts.items()))

        print(corpus.get())
"""