#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import math
import re
import datetime
import sys, getopt

from segmenter import segment

class MyDocuments(object):    # memory efficient data streaming
    def __init__(self, dirname):
        self.dirname = dirname
        if not os.path.isdir(dirname):
            print(dirname, '- not a directory!')
            sys.exit()

    def __iter__(self):
        for dirfile in os.walk(self.dirname):
            for fname in dirfile[2]:
                text = open(os.path.join(dirfile[0], fname),
                            'r', encoding='utf-8', errors='ignore').read()
                yield segment(text)   # time consuming


def main(argv):   # idf generator
    inputdir = ''
    outputfile = ''

    usage = 'usage: python gen_idf.py -i <inputdir> -o <outputfile>'
    if len(argv) < 4:
        print(usage)
        sys.exit()
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["idir=","ofile="])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)

    for opt, arg in opts:   # parsing arguments
        if opt == '-h':
            print(usage)
            sys.exit()
        elif opt in ("-i", "--idir"):
            inputdir = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    documents = MyDocuments(inputdir)

    ignored = {'', ' ', '', '。', '：', '，', '）', '（', '！', '?', '”', '“'}
    id_freq = {}
    i = 0
    for doc in documents:
        doc = set(x for x in doc if x not in ignored)
        for x in doc:
            id_freq[x] = id_freq.get(x, 0) + 1
        if i % 1000 == 0:
            print('Documents processed: ', i, ', time: ',
                datetime.datetime.now())
        i += 1

    with open(outputfile, 'w', encoding='utf-8') as f:
        for key, value in id_freq.items():
            f.write(key + ' ' + str(math.log(i / value, 2)) + '\n')


if __name__ == "__main__":
   main(sys.argv[1:])
