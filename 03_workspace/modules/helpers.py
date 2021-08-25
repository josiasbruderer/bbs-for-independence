#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##########################################################
# title:  helpers
# author: Josias Bruderer
# date:   TODO
# desc:   this module provides some useful functions
##########################################################

def chunker_list(seq, size):
    return (seq[i::size] for i in range(size))
