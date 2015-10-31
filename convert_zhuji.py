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
file_zhuji = "base_data\GREHe Xin Ci Hui Zhu Ji Yu Jing - Cao Tian Cheng.txt"
match_escape_char_re = re.compile(r'\\(?=[\[\]()*+])')
match_zhuji_list_start_re = re.compile(ur'### List \d+', re.M)
def get_etyma_block_d_l_l(list_data_l):
    match_etyma_block_start = re.compile(r'^\d+\.(.*)$\n|^Unit \d+$', re.M)
    etyma_block_d_l_l = []
    for list_index, base_list_str in enumerate(list_data_l):
        if list_index > 38:
            break
        etyma_block_d_l = []
        base_list_str = base_list_str.split(u'小结&复习')[0]
        etyma_block_str_l = extract_content_between(base_list_str, match_etyma_block_start)
        for etyma_index, etyma_block_str in enumerate(etyma_block_str_l):
            ety_str = match_etyma_block_start.search(etyma_block_str).group(1)
            if ety_str is None:
                ety_str = ''
            ety_str = ety_str.strip()
            if  ety_str == u'其他':
                #print u'词根是其他'
                ety_str = ''
            if list_index == 36-1:
                ety_str = u'与动物有关的单词，' + ety_str
            ety_str = ety_str.strip()
            etyma_block_str_and_summary_str = etyma_block_str.split(u'小结')
            summary_str = etyma_block_str_and_summary_str[1] if len(etyma_block_str_and_summary_str) == 2 else ''
            etyma_block_str = match_etyma_block_start.sub('', etyma_block_str_and_summary_str[0])
            # revise surg, cit
            if ety_str == 'surg, cit':
                temp_str_l = etyma_block_str.split('\n')
                #iter_print(temp_str_l)
                # insert line 5 after line 0
                modified_str_l = [temp_str_l[0], temp_str_l[5]] + temp_str_l[1:5] + temp_str_l[6:]
                etyma_block_str = '\n'.join(modified_str_l)
                #print etyma_block_str
            # revise rejoice
            if ety_str == u'欢乐与喜悦':
                temp_str_l = etyma_block_str.split('\n')
                #iter_print(temp_str_l)
                modified_str_l = [temp_str_l[0], temp_str_l[9]] + temp_str_l[1:9]
                etyma_block_str = '\n'.join(modified_str_l)
                #print etyma_block_str
            etyma_block_d = {'pos':(list_index+1, etyma_index+1), 
                             'ety': ety_str,
                             'ety_block_str': etyma_block_str,
                             'summary': summary_str}
            etyma_block_d_l.append(etyma_block_d)
        etyma_block_d_l_l.append(etyma_block_d_l)
    return etyma_block_d_l_l
def revise_miss_etyma(base_d_l_l):
    # revise list 25 etyma 3 revise tum
    base_d_l_l[25-1][3-1]['ety'] = 'tum'
    # revise list 5 etyma 4 revise post, pound
    base_d_l_l[5-1][4-1]['ety'] = 'post, pound'
    # revise list 6 etyma 7 revise vad, vag, ced
    base_d_l_l[6-1][7-1]['ety'] = 'vad, vag, ced'
match_cognate_block_start_re = re.compile(ur'^([a-zéï-]+)(.*?)(\[.*\])$', re.M|re.I)
def process_ety_block_str(base_d_l_l):
    path_to_ety_block_str = [('all','',True),('all','',True),('key','ety_block_str',False)]
    for list_index, ety_index, ety_block_str in iter_through_general(base_d_l_l, 
                                                                     path_to_ety_block_str):
        etyma_block_d = base_d_l_l[list_index][ety_index]
        returned_l = extract_content_between(ety_block_str, match_cognate_block_start_re, True)
        ety_group_exp = returned_l.pop(0).strip()
        etyma_block_d['etyma_group_explanation'] = ety_group_exp
        etyma_block_d['cognate_block_str_l'] = returned_l
# revise List 13, ety 3 revise scru
def revise_scru(base_d_l_l):
    '''
    please only call it one time
    or re-run the code cells starting from 
        "zhuji_base_d_l_l = get_etyma_block_d_l_l(zhuji_base_list_l)"
    '''
    to_revise_l = base_d_l_l[13-1][3-1]['cognate_block_str_l']
    #iter_print(to_revise_l)
    # remove element 3-5 and build new dict
    new_l = to_revise_l[3:]
    to_revise_l[2] = to_revise_l[2].replace(u'以下的4个单词可以将scru按照读音联想成“四顾”，表示“ (顾虑地) 看”。', '')
    to_revise_l = to_revise_l[:3]
    new_ety = 'scru'
    new_ety_group_exp = u'将scru按照读音联想成“四顾”，表示“ (顾虑地) 看”'
    new_ety_d = {'cognate_block_str_l': new_l, 'pos': (13, 3),
                 'ety': new_ety, 
                 'etyma_group_explanation': new_ety_group_exp,
                 'summary':'', 'ety_block_str':''}
    base_d_l_l[13-1].append(new_ety_d)
def process_cognate_block(cognate_block_str):
    cognate_dict = {}
    cognate_lines_l = cognate_block_str.split('\n')
    first_line_match = match_cognate_block_start_re.match(cognate_lines_l.pop(0))
    word = first_line_match.group(1)
    if (word == '') or (word is None):
        print 'Warning!'
    cognate_dict['word'] = word
    phon = first_line_match.group(3)
    cognate_dict['phon'] = phon if not (phon is None) else ''
    
    modified_cognate_lines_l = []
    for cognate_line in cognate_lines_l:
        cognate_line = cognate_line.strip()
        if cognate_line == '':
            pass
        elif cognate_line.startswith(u'源'):
            # revise 源
            cognate_line = cognate_line.replace(u'源', u'[源]')
            # print cognate_line
        elif cognate_dict['word'] == u'facilitate':
            pass
        elif cognate_dict['word'] in ['jocular', 'jocund', 'jovial', 'rejoice']:
            pass
        elif cognate_line.startswith(u'以下两个单词中'):
            pass
        elif not cognate_line.startswith(u'['):
            # test
            print 'current line:', cognate_line, '\ncurrent block\n', cognate_block_str
            break
        else:
            pass
        modified_cognate_lines_l.append(cognate_line)
    cognate_dict['content'] = '\n'.join(modified_cognate_lines_l)
    return cognate_dict
def process_all_cognate_block(base_data_d_l_l):
    base_word_d = {}
    path_to_cognate_block_str = [('all','',True),('all','',True),
                                 ('key','cognate_block_str_l',False),('all','',True)]
    for list_index, eytma_index, cognate_index, cognate_block_str in iter_through_general(base_data_d_l_l, 
                                                                                          path_to_cognate_block_str):
        one_word_d = process_cognate_block(cognate_block_str)
        word = one_word_d['word']
        for _key in ['pos', 'ety', 'etyma_group_explanation', 'summary']:
            one_word_d[_key] = base_data_d_l_l[list_index][eytma_index][_key]
        one_word_d['pos'] = ', '.join([unicode(i) for i in one_word_d['pos']])
        one_word_d['etyma_cognates_l'] = '' # waiting to be filled later
        if word in base_word_d:
            print 'Warning! word already exists!', word
        base_word_d[word] = one_word_d
    return base_word_d
def add_etyma_cognates_l(base_word_d, base_d_l_l):
    path_to_etyma_d = [('all','',False),('all','',False)]
    for etyma_d, in iter_through_general(base_d_l_l, path_to_etyma_d):
        ety_str = etyma_d['ety']
        ety_group_exp = etyma_d['etyma_group_explanation']
        if ety_str != '' or ety_group_exp != '':
            if ety_str == '':
                # test
                print ety_group_exp
            etyma_cognates_l = []
            for cognate_block_str in etyma_d['cognate_block_str_l']:
                word = match_cognate_block_start_re.match(cognate_block_str).group(1)
                etyma_cognates_l.append(word)
            for word in etyma_cognates_l:
                base_word_d[word]['etyma_cognates_l'] = ', '.join(etyma_cognates_l)
def main(file_name=None):
    if file_name is None:
        file_name = file_zhuji
    # for module call
    if not os.path.isfile(file_name):
        return
    zhuji_base_str = codecs_open_r_utf8(file_zhuji)
    zhuji_base_str = match_escape_char_re.sub('', zhuji_base_str)
    zhuji_base_str = collapse_blank_line(zhuji_base_str)
    with codecs.open('temp_zhuji_base_str.txt', 'w', encoding='utf-8') as f:
        f.write(zhuji_base_str)
    zhuji_base_str = zhuji_base_str.split(u'# 第二篇 核心词汇练习')[0]
    zhuji_base_list_l = extract_content_between(zhuji_base_str, match_zhuji_list_start_re)
    zhuji_base_d_l_l = get_etyma_block_d_l_l(zhuji_base_list_l)
    revise_miss_etyma(zhuji_base_d_l_l)
    process_ety_block_str(zhuji_base_d_l_l)
    revise_scru(zhuji_base_d_l_l)
    zhuji_base_word_d = process_all_cognate_block(zhuji_base_d_l_l)
    add_etyma_cognates_l(zhuji_base_word_d, zhuji_base_d_l_l)
    with codecs.open('zhuji_base_d.txt', 'w', encoding='utf-8') as f:
        json.dump(zhuji_base_word_d, f)

if __name__ == '__main__':
    main()