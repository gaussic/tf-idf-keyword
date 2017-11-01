#!/usr/bin/python
# -*- coding: utf-8 -*-

import jieba
import re

def segment(sentence, cut_all=False):
    sentence = sentence.replace('\n', '').replace('\u3000', '').replace('\u00A0', '')
    sentence = ' '.join(jieba.cut(sentence, cut_all=cut_all))
    return re.sub('[a-zA-Z0-9.。:：,，)）(（！!??”“\"]', '', sentence).split()
