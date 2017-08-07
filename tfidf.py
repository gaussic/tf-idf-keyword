#!/usr/bin/python
# -*- coding: utf-8 -*-

import jieba
from collections import Counter


class IDFLoader(object):
    def __init__(self, idf_path):
        self.idf_path = idf_path
        self.load_idf()

    def load_idf(self):
        self.idf_freq = {}
        with open(self.idf_path, 'r', encoding='utf-8') as f:
            for line in f:
                word, freq = line.strip().split(' ')
                self.idf_freq[word] = float(freq)
        self.median_idf = sorted(
            self.idf_freq.values())[len(self.idf_freq) // 2]


class TFIDF(object):
    def __init__(self, idf_path):
        self.idf_loader = IDFLoader(idf_path)
        self.idf_freq = self.idf_loader.idf_freq
        self.median_idf = self.idf_loader.median_idf

    def extract_keywords(self, sentence, topK=20):
        seg_list = jieba.cut(sentence, cut_all=True)
        freq = {}
        for w in seg_list:
            freq[w] = freq.get(w, 0.0) + 1.0
        del freq['']
        total = sum(freq.values())


        for k in freq:
            freq[k] *= self.idf_freq.get(w, self.median_idf) / total

        tags = sorted(freq, key=freq.__getitem__, reverse=True)

        if topK:
            return tags[:topK]
        else:
            return tags

if __name__ == "__main__":
    tdidf = TFIDF('idf.txt')
    sentence = open('corpus/THUCNews/教育/284485.txt', 'r', encoding='utf-8').read().replace('\n', '')
    tags = tdidf.extract_keywords(sentence)
    for tag in tags:
        print(tag)

