#!/usr/bin/python
# -*- coding: utf-8 -*-

import jieba
import re

def segment(sentence, cut_all=True):
    sentence = re.sub('[a-zA-Z0-9]', '', sentence.replace('\n', '')) # 过滤
    return jieba.cut(sentence, cut_all=cut_all) # 分词
