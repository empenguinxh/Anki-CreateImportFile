# -*- coding: utf-8 -*-

from multiprocessing import Pool
from wagnerfischerpp import WagnerFischer
import codecs
import json


with codecs.open('new3000_base_d.txt') as f:
    new3000_base_d = json.load(f,encoding='utf-8')


def get_similar_word(word_a, threshold=2):
    distance_l = []
    for word_b in new3000_base_d:
        if word_b == word_a:
            continue
        cost_a_b = WagnerFischer(word_a, word_b).cost
        if cost_a_b <= threshold:
            distance_l.append((cost_a_b, word_b))
    distance_l.sort()
    return distance_l


def gen_brief_exp(word):
    brief_exp_l = []
    for usage_d in new3000_base_d[word]['usages']:
        brief_exp_l.append(usage_d['exp_d']['cn'])
    return word + ': ' + u'；'.join(brief_exp_l)


def add_similar_word_single_word(word):
    similar_word_l = get_similar_word(word)
    exp_l = []
    for cost, similar_word in similar_word_l:
        exp_l.append(gen_brief_exp(similar_word))
    #new3000_base_d[word]['similar_word'] = ' | '.join(exp_l)
    print '+',
    return word, ' | '.join(exp_l)


def add_similar_word_multiprocessing():
    pool = Pool(4)
    result = pool.map(add_similar_word_single_word, new3000_base_d.iterkeys())
    pool.close()
    with codecs.open('similar_word.txt', 'w', encoding='utf-8') as f:
        json.dump(result, f)

if __name__ == '__main__':
    add_similar_word_multiprocessing()