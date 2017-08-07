#!/usr/bin/python
# -*- coding: utf-8 -*-

# 使用结巴分词

import jieba
import os
from collections import Counter
import numpy as np
import datetime

class MyDocuments(object):
    def __init__(self, dirname):
        self.dirname = dirname
 
    def __iter__(self):
        for dirfile in os.walk(self.dirname):
            for fname in dirfile[2]:
                text = open(os.path.join(dirfile[0], fname), 'r', 
                    encoding='UTF-8').read().replace('\n', '')
                yield list(set(jieba.cut(text, cut_all=True)))

documents = MyDocuments('./corpus/THUCNews/')

ignore = {'\n', ''}
counter = Counter()
word_list = []
i = 0
for doc in documents:
    word_list.extend(doc)
    if i % 1000 == 0:
        counter += Counter(x for x in word_list if x not in ignore)
        word_list = []
        print('Documents processed: ', i, 'time: ', datetime.datetime.now())
    i += 1

counter += Counter(x for x in word_list if x not in ignore)


with open('idf.txt', 'w', encoding='utf-8') as f:
    for key, value in counter.items():
        f.write(key + ' ' + str(np.log2(i / value)) + '\n')

    


