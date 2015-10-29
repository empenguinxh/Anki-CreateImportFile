
# coding:utf-8
import re
import json
import codecs
import functools
import os.path
from random import random
from random import randint
from pprint import pprint
from copy import deepcopy
from my_helpers import *
file_duanyu = "base_data\GREGao Fen Bi Bei Duan Yu Da Pe - Yan Yu Zhen ,Gao Yu ,Chen Qi.txt"

def extract_dy_unit(base_str):
    base_str = base_str.split(u"# 索引\n")[0]
    match_dy_unit_start_re = re.compile(ur'^# Unit \d+', re.M)
    base_unit_str_l = extract_content_between(base_str, match_dy_unit_start_re)
    base_unit_str_l = [base_unit_str.split(u'## 检测练习\n')[0] for base_unit_str in base_unit_str_l]
    return base_unit_str_l


def extract_dy_index_content(base_str):
    match_dy_index_cn_start_re = re.compile(u' (?=[\u4e00-\u9fa5\u3010])')
    index_str = base_str.split(u"# 索引\n")[1]
    index_d = {}
    for line_str in index_str.split('\n'):
        if line_str == '':
            continue
        line_str = strF2H(line_str)
        en_cn = match_dy_index_cn_start_re.split(line_str)
        if len(en_cn) == 2:
            index_d[en_cn[0]] = en_cn[1]
        else:
            print 'Warning, no en or no cn:', en_cn
    return index_d


def extract_dy_phrase_d(base_unit_str_l):
    base_phrase_d = {}
    for unit_index, base_unit_str in enumerate(base_unit_str_l):
        match_phrase_start_re = re.compile(ur'^\*\*([a-z].*?)([\u3000\u4e00-\u9fa5].*)?\*\*$', 
                                        re.M|re.I)
        phrase_block_str_l = extract_content_between(base_unit_str, match_phrase_start_re)
        for phrase_block_str in phrase_block_str_l:
            match_result = match_phrase_start_re.match(phrase_block_str)
            if match_result is None:
                print phrase_block_str
            phrase_en = match_result.group(1)
            phrase_exp_cn = match_result.group(2)
            if phrase_exp_cn is None:
                phrase_exp_cn = ''
            else:
                phrase_exp_cn = phrase_exp_cn.strip(u'\u3000 ')
            phrase_block_str = phrase_block_str[match_result.end():].strip('\n ')
            base_phrase_d[phrase_en] = {'exp_cn': phrase_exp_cn, 
                                        'phrase_block_str': phrase_block_str,
                                        'pos': unit_index}
    return base_phrase_d


def process_dy_phrase_block_str(base_d):
    processed_phrase_d = {}
    for phrase, base_phrase_d in base_d.iteritems():
        phrase_block_str = base_phrase_d['phrase_block_str']
        has_multiple_cn_exp = base_phrase_d['exp_cn'] == ''
        match_dy_multi_cn_exp_start_re = re.compile(ur'^\*\*\d+\. (.*)\*\*$', re.M)
        if has_multiple_cn_exp:
            exp_cn_l = match_dy_multi_cn_exp_start_re.findall(phrase_block_str)
            phrase_block_str_l = extract_content_between(phrase_block_str, 
                                                         match_dy_multi_cn_exp_start_re)
        else:
            exp_cn_l = [base_phrase_d['exp_cn']]
            phrase_block_str_l = [phrase_block_str]
        
        match_en_exp_re = re.compile(ur'^\*\*释\*\* (.*)$', re.M)
        match_example_re = re.compile(ur'^\*\*例\*\* (.*)$', re.M)
        match_gre_example = re.compile(ur'\*\*题\*\* (.*)$', re.S)
        
        for usage_index, phrase_block_str in enumerate(phrase_block_str_l):

            phrase_detailed_d = {}
            exp_en = match_en_exp_re.search(phrase_block_str).group(1)
            example = match_example_re.search(phrase_block_str).group(1)
            gre_example_en_cn = match_gre_example.search(phrase_block_str).group(1).split('\n')
            gre_example_en = gre_example_en_cn[0]
            gre_example_cn = gre_example_en_cn[2]
            phrase_detailed_d = {'en_exp': exp_en, 
                                 'cn_exp': exp_cn_l[usage_index],
                                 'example': example,
                                 'gre_example_en': gre_example_en,
                                 'gre_example_cn': gre_example_cn,
                                 'pos': base_phrase_d['pos']
                                }
            phrase_uid = phrase + unicode(usage_index+1)
            processed_phrase_d[phrase_uid] = phrase_detailed_d
    return processed_phrase_d

def main(file_name=None):
    if file_name is None:
        file_name = file_duanyu
    # for module call
    if not os.path.isfile(file_name):
        return
    dy_base_str = codecs_open_r_utf8(file_duanyu)
    match_escape_char_re = re.compile(r'\\(?=[\[\]()*+])')
    dy_base_str = match_escape_char_re.sub('', dy_base_str)
    dy_base_unit_str_l = extract_dy_unit(dy_base_str)
    dy_index_d = extract_dy_index_content(dy_base_str)
    dy_phrase_d = extract_dy_phrase_d(dy_base_unit_str_l)
    # revise ’'
    dy_phrase_d['under one\'s control'] = dy_phrase_d[u'under one’s control']
    dy_phrase_d['on one\'s own'] = dy_phrase_d[u'on one’s own']
    del dy_phrase_d[u'under one’s control'], dy_phrase_d[u'on one’s own']
    dy_phrase_processed_d = process_dy_phrase_block_str(dy_phrase_d)
    with codecs.open('duanyu_base_d.txt', 'w', encoding='utf-8') as f:
        json.dump(dy_phrase_processed_d, f)
if __name__ == '__main__':
    main()