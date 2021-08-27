#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##########################################################
# title:  helpers
# author: Josias Bruderer
# date:   25.08.2021
# desc:   this module provides some useful functions
##########################################################

import pickle


def save_object(obj, filename):
    with open(filename, 'wb') as outp:  # Overwrites any existing file.
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)

def load_object(filename):
    with open(filename, 'rb') as inp:
        return pickle.load(inp)

def chunker_list(seq, size):
    return (seq[i::size] for i in range(size))
