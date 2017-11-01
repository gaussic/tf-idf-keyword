#!/usr/bin/python
# -*- coding: utf-8 -*-

from segmenter import segment
import sys, getopt


class IDFLoader(object):
    def __init__(self, idf_path):
        self.idf_path = idf_path
        self.idf_freq = {}     # idf
        self.mean_idf = 0.0    # 均值
        self.load_idf()

    def load_idf(self):       # 从文件中载入idf
        cnt = 0
        with open(self.idf_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    word, freq = line.strip().split(' ')
                    cnt += 1
                except Exception as e:
                    pass
                self.idf_freq[word] = float(freq)

        print('Vocabularies loaded: %d' % cnt)
        self.mean_idf = sum(self.idf_freq.values()) / cnt


class TFIDF(object):
    def __init__(self, idf_path):
        self.idf_loader = IDFLoader(idf_path)
        self.idf_freq = self.idf_loader.idf_freq
        self.mean_idf = self.idf_loader.mean_idf

    def extract_keywords(self, sentence, topK=20):    # 提取关键词
        # 过滤
        seg_list = segment(sentence)

        freq = {}
        for w in seg_list:
            freq[w] = freq.get(w, 0.0) + 1.0
        total = sum(freq.values())

        for k in freq:   # 计算 TF-IDF
            freq[k] *= self.idf_freq.get(k, self.mean_idf) / total

        tags = sorted(freq, key=freq.__getitem__, reverse=True)  # 排序

        if topK:
            return tags[:topK]
        else:
            return tags

def main(argv):
    idffile = ''
    document = ''
    topK = None

    usage = 'usage: python tfidf.py -i <idffile> -d <document> -t <topK>'
    if len(argv) < 4:
        print(usage)
        sys.exit()
    try:
        opts, args = getopt.getopt(argv,"hi:d:t:",
            ["idffile=","document=", "topK="])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)

    for opt, arg in opts:   # parsing arguments
        if opt == '-h':
            print(usage)
            sys.exit()
        elif opt in ("-i", "--idffile"):
            idffile = arg
        elif opt in ("-d", "--document"):
            document = arg
        elif opt in ("-t", "--topK"):
            topK = int(arg)

    tdidf = TFIDF(idffile)
    sentence = open(document, 'r', encoding='utf-8', errors='ignore').read()
    tags = tdidf.extract_keywords(sentence, topK)

    for tag in tags:
        print(tag)


if __name__ == "__main__":
    main(sys.argv[1:])
