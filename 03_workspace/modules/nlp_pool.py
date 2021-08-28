#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##########################################################
# title:  helpers
# author: Josias Bruderer
# date:   28.08.2021
# desc:   this module provides nlp functions
##########################################################

from multiprocessing import Pool
from multiprocessing.managers import BaseManager
import textacy
import spacy
# run: ./.envs/bin/python -m spacy download en_core_web_sm


class PoolCorpus(object):

    def __init__(self):
        model = spacy.load('en_core_web_sm')
        self.corpus = textacy.corpus.Corpus(lang=model)

    def add(self, data):
        self.corpus.add(data)

    def get(self):
        return self.corpus

    def add_dataset(self, dataset):
        for key in dataset:
            for d in dataset[key]:
                self.add(textacy.make_spacy_doc((d["content"], d["metadata"]), lang="en_core_web_sm"))
        print("corpus loaded")

    def save(self, path):
        self.corpus.save(path)


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
