
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
file_new_3000 = "base_data\GREHe Xin Ci Hui Kao Fa Jing Xi  (Xin Dong Fang Da Yu Ying Yu Xue Xi Cong Shu ) - Chen Qi.txt"

match_new3000_list_start_re = re.compile(ur'^# List \d+', re.M)


def strip_last_list(list_data):
    strip_start_re = re.compile(ur'# Word List 1　与说有关的词根构成的单词(.|\n)*$')
    return strip_start_re.sub('', list_data)


match_unit_start_re = re.compile(ur'^## Unit \d+', re.M)


match_word_block_start = re.compile(ur'^\*\*(?P<word>[a-z\-éï]+)\*\*(?P<phon>［.+］)?', re.U|re.M)
# phon represent phonetic symbol


def get_word_of_one_unit(unit_block_str, list_index, unit_index):
    returned_words_d_d = {}
    word_block_str_l = extract_content_between(unit_block_str, match_word_block_start)
    for word_block_str in word_block_str_l:
        first_line_match = match_word_block_start.match(word_block_str)
        word = first_line_match.group('word')
        phon = first_line_match.group('phon')
        one_word_d = {'word_block_str': match_word_block_start.sub('', word_block_str), 
                      'phon': strF2H(phon) if phon else u'', 
                      'pos':(list_index, unit_index)}
        returned_words_d_d[word] = one_word_d
    return returned_words_d_d


def get_new3000_base_d(base_unit_data_l_l):
    _new3000_base_d = {}
    for list_index, unit_data_l in enumerate(base_unit_data_l_l):
        for unit_index, unit_data in enumerate(unit_data_l):
            _new3000_base_d.update(get_word_of_one_unit(unit_data, list_index+1, unit_index+1))
    return _new3000_base_d


# revise
def revise_word_base_data(word_d):
    # revise anarchist
    word_block_str = 'word_block_str'
    to_revise_word_d = word_d['anarchist']
    to_revise_str = to_revise_word_d[word_block_str]
    to_revise_word_d[word_block_str] = to_revise_str.replace(u'同', u'近')
    # revise compliment
    to_revise_word_d = word_d['compliment']
    to_revise_str = to_revise_word_d[word_block_str]
    to_revise_word_d['phon'] = [strF2H(phon) for phon in re.findall(ur'［.+?］', to_revise_str)]
    to_revise_word_d[word_block_str] = '\n'.join(to_revise_str.split('\n')[1:])
    # reviseantediluvian, revise anecdote
    for to_revise_word in ['antediluvian', 'anecdote']:
        to_revise_word_d = word_d[to_revise_word]
        to_revise_str = to_revise_word_d[word_block_str]
        temp_index = 0
        for match_result in re.finditer(ur'\n\n', to_revise_str):
            if temp_index == 2:
                to_revise_str = to_revise_str[0:match_result.start()] + u'‖' + to_revise_str[match_result.end():]
                break
            temp_index += 1
        to_revise_word_d[word_block_str] = to_revise_str
    return word_d


character_start = {'examples': '例', 
                   'syns': '近', 
                   'ants': '反', 
                   'der': '派'}


is_str_start_with_character_fun_d = {}
for key, value in character_start.iteritems():
    def gen_match_fun_closure(_value):
        return lambda s: s[0] == _value.decode('utf-8')
    is_str_start_with_character_fun_d[key] = gen_match_fun_closure(value)


def revise_entry_name(words_d):
    # revise random
    words_d['random']['word_block_str'] = words_d['random']['word_block_str'].replace(u'例　aimless',
                                                                                      u'近　aimless')
    # revise sordid
    words_d['sordid']['word_block_str'] = words_d['random']['word_block_str'].replace(u'近　Behind his generous',
                                                                                      u'例　Behind his generous')
    # revise clan
    words_d['clan']['word_block_str'] = words_d['clan']['word_block_str'] .replace(u'反　clannish', 
                                                                                   u'派　clannish')


match_usage_start_re = re.compile(ur'^【考(?:法|点)\d?】(.*)$', re.M|re.U)
match_der = re.compile(ur'^')


def wb_str_2_usages_d_l(word_block_str):
    '''
    convert word block (string) to usages like structure
    input: the 'word_block_str' attribute of a word dictionary
    return: two lists, 
            the first with its 'i'th element indicating whether 
                the 'i'th usage has a complex der
            the second is the list of usages
    '''
    usage_template = {'exp': '',
                      'examples': '',
                      'syns': '',
                      'ants': '',
                      'der': ''}
    usages_str_l = extract_content_between(word_block_str, match_usage_start_re)
    usages_d_l = []
    is_complex_der_l = []
    
    for one_usage_str in usages_str_l:
        one_usage_d = deepcopy(usage_template)
        is_complex_der = False
        has_der = False
        one_usage_lines = one_usage_str.split('\n')
        one_usage_d['exp'] = match_usage_start_re.match(one_usage_lines[0]).group(1)
        
        for line in one_usage_lines[1:]:
            has_been_matched = False
            
            if line == '' or line == '\n':
                continue
            # match "例" "反", etc.
            for field_name, match_func in is_str_start_with_character_fun_d.iteritems():
                if match_func(line):
                    has_been_matched = True
                    if has_der:
                        one_usage_d['der'] += '\n' + line.strip()
                        is_complex_der = True
                    else:
                        # test
                        if one_usage_d[field_name] != '':
                            print '****Multi line field!****'
                            print word_block_str
                            pass
                        one_usage_d[field_name] = line.strip()
                    if field_name == 'der':
                        # test
                        if has_der:
                            # print 'Warning! der in der!'
                            # print one_usage_str
                            pass
                        has_der = True
                    break
            if not has_been_matched:
                # after printed out, it can be seen that these lines are all aphorisms
                # so, useless for our purpose
                #print line
                pass
        usages_d_l.append(one_usage_d)
        is_complex_der_l.append(is_complex_der)
    return is_complex_der_l, usages_d_l


def gen_usages_for_all_words(words_d):
    match_der_word = re.compile(ur'^派 ([a-z,/\-éï]+)', re.M)
    complex_ders_d = {}
    for word in words_d:
        if words_d[word]['word_block_str'] == '':
            print 'Empty word:', word
            continue
        is_complex_der_l, words_d[word]['usages'] = wb_str_2_usages_d_l(words_d[word]['word_block_str'])
        if True in is_complex_der_l:
            for i, one_usage in enumerate(words_d[word]['usages']):
                # revise plumb
                if i == 2 and word == u'plumb':
                    one_usage['example'] = one_usage['der']
                    one_usage['der'] = ''
                    continue
                if is_complex_der_l[i]:
                    whole_der_block_str = strF2H(one_usage['der'])
                    der_block_str_l = extract_content_between(whole_der_block_str, match_der_word)
                    for der_block_str in der_block_str_l:
                        # revise daunt
                        if word == 'daunt':
                            der_block_str = der_block_str.replace(', ',  '/')
                        der_word = match_der_word.match(der_block_str).group(1)
                        der_block_str = match_der_word.sub(ur'【考法】', der_block_str)
                        complex_ders_d[der_word] = {}
                        _, complex_ders_d[der_word]['usages'] = wb_str_2_usages_d_l(der_block_str)
                        if len(complex_ders_d[der_word]['usages']) != 1:
                            print 'Warning! Not unqiue explanation!'
                            continue
                        complex_ders_d[der_word]['usages'][0]['der'] = u'源 ' + word
                        complex_ders_d[der_word]['phon'] = u''
                        complex_ders_d[der_word]['pos'] = words_d[word]['pos']
                        complex_ders_d[der_word]['word_block_str'] = u''
                        # test
                        #print der_word
                        #iter_print(complex_ders_d[der_word]['usages'])
        #del words_d[word]['word_block_str']
    return complex_ders_d, words_d


match_phon_re = re.compile(ur'［.*］', re.U)
match_pspeech_re = re.compile(ur'\*([a-z\/.]+\.)\*')
has_cn_char_fun = lambda _str: re.compile(ur'[\u4e00-\u9fa5]').search(_str) is not None


def process_exp(exp_field_str):
    '''
    input: a unicode object corresponding the explanation line of the word
    return: dict {exp, pspeech, ph_symbl}
    '''
    if exp_field_str == '':
        print 'Warning! No explanation!'
        return
    returned_d = {'exp': {'en': '', 'cn': '', 'en_cn': ''}, 
                  'pspeech': '',
                  'ph_symbl': ''}
    
    result = match_pspeech_re.search(exp_field_str)
    if result:
        returned_d['pspeech'] = result.group(1)
        exp_field_str = match_pspeech_re.sub('', exp_field_str, 1)
    
    result = match_phon_re.search(exp_field_str)
    if result:
        returned_d['ph_symbl'] = result.group()
        exp_field_str = match_phon_re.sub('', exp_field_str, 1).strip()
    
    returned_d['exp']['en_cn'] = exp_field_str.strip()
    
    # seperate en and cn
    spered_str_l = [_str.strip() for _str in strF2H(exp_field_str).split(u':')]
    seperator_count = len(spered_str_l) - 1
    if seperator_count == 0:
        # test whether no seperator guarantees no chinese explanation
        # print 'No sep', spered_str_l
        returned_d['exp']['cn'] = spered_str_l[0]
    elif seperator_count == 1:
        returned_d['exp']['cn'], returned_d['exp']['en'] = spered_str_l
    elif seperator_count == 2:
        # test
        # print 'Two sep: ', spered_str_l
        has_char_cn_boo_l = map(has_cn_char_fun, spered_str_l)
        returned_d['exp']['cn'] = u':'.join([spered_str_l[i] for i in range(seperator_count+1) if has_char_cn_boo_l[i]])
        returned_d['exp']['en'] = u':'.join([spered_str_l[i] for i in range(seperator_count+1) if not has_char_cn_boo_l[i]])
        # test
        #iter_print(returned_d['exp'])
    else:
        # test 
        #print 'More than two sep: ', exp_field_str
        pass
    return returned_d


def process_exp_field_for_all_words(words_d):
    for word, usage_index, exp_str in iter_value_of_key_through_d_l_d_d(words_d, 'usages', 'exp', 
                                                                        yield_top_key=True, yield_list_index=True):
        base_exp_d = None
        # get base_exp_d
        # revise abuse
        if word == 'abuse' and usage_index == 1:
            exp_str_l = exp_str.split(';')
            base_exp_d, extra_exp_d = map(process_exp, exp_str_l)
            base_exp_d['exp']['en'] = base_exp_d['exp']['en'] + ';' + extra_exp_d['exp']['en']
            base_exp_d['exp']['cn'] = base_exp_d['exp']['cn'] + ';' + extra_exp_d['exp']['cn']
            # test
            #iter_print(base_exp_d)

        # revise disaffected
        if word == 'disaffect':
            base_exp_d = process_exp(exp_str.split(';')[0])
            # test
            #iter_print(base_exp_d)

        else:    
            base_exp_d = process_exp(exp_str)
        
        # get phonic symbol from parent field
        if base_exp_d['ph_symbl'] == u'':
            # revise compliment
            if word == 'compliment':
                if usage_index == 0:
                    base_exp_d['ph_symbl'] = 'n. ' + words_d[word]['phon'][0] + \
                                             ' v. ' + words_d[word]['phon'][1]
                else:
                    base_exp_d['ph_symbl'] = words_d[word]['phon'][0]
            else:
                # test
                if usage_index > 2:
                    #print word
                    pass
                base_exp_d['ph_symbl'] = words_d[word]['phon']
        one_usage = words_d[word]['usages'][usage_index]
        one_usage['ph_symbl'] = base_exp_d['ph_symbl']
        del base_exp_d['ph_symbl']
        one_usage['pspeech'] = base_exp_d['pspeech']
        del base_exp_d['pspeech']
        one_usage['exp_d'] = base_exp_d['exp']
    return words_d


match_all_cn_re = ur' ?[a-z0-9：。；，“”（）、？《》]*?[\u4e00-\u9fa5]+.*?(?=$|[a-z]+ [a-z]+)'
match_all_cn_re = re.compile(match_all_cn_re, re.I)


match_cn_punc_with_en_char_fun = lambda _str: re.search(ur'[。？]( )?(?=[a-z])', _str, re.I)


match_cn_char_with_en_char_fun = lambda _str: re.search(ur'[\u4e00-\u9fa5](?=[a-z])', _str, re.I)


# revise
def revise_no_sep(words_d):
    path_to_example = [('all', '', True), ('key', 'usages', False), ('all','',True),('key','examples',False)]
    example_iter = iter_through_general(words_d, path_to_example)
    for word, usage_index, example_str in example_iter:
        if example_str == '':
            continue
        example_str = example_str[2:]
        if u'\u2016' not in example_str:
            results = match_all_cn_re.findall(example_str)
            if len(results) > 1:
                index_to_add_sep = None
                one_result = match_cn_punc_with_en_char_fun(example_str)
                if one_result:
                    index_to_add_sep = one_result.end()
                elif word in [u'heckle', u'carefree']:
                    one_result = match_cn_char_with_en_char_fun(example_str)
                    index_to_add_sep = one_result.end()
                elif word == 'clarify':
                    example_str = example_str.replace(u';', u'\u2016')
                if index_to_add_sep:
                    example_str = example_str[:index_to_add_sep] + u'\u2016' + example_str[index_to_add_sep:]
        words_d[word]['usages'][usage_index]['examples'] = u'例 ' + example_str       
    return words_d


match_sentence_en_part_re = re.compile(ur'[a-z0-9éï\'";:,?!%()$ⅠⅡ.*/\- —　‘’“”（）]+(?=[＜《〈\u4e00-\u9fa5])', re.I)


def sep_en_cn_sentence(sentences_str):
    if sentences_str == '':
        return '', '', '',
    sentences_str = sentences_str[2:].replace(u'\!', u'!')
    is_number_fun = lambda _str: re.match('\d', _str)
    en_str_l = []
    cn_str_l = []
    en_cn_str_l= []
    for sentence in sentences_str.split(u'\u2016'):
        sentence = sentence.strip(u' 　\n')
        en_cn_str_l.append(sentence)
        result = match_sentence_en_part_re.match(sentence)
        if result:
            en_str = result.group()
            # test
            if not (en_str[-1] in [' ', '.', u'）', u'”']):
                if en_str[-1] == u'“':
                    #print en_str
                    en_str = en_str[:-1]
                    #print en_str
                elif is_number_fun(en_str[-1]) or (en_str[-2:] in ['RE', 'IT', 'on', 'NA']):
                    #print en_str
                    last_blank_space = len(en_str) - 1
                    while en_str[last_blank_space] != ' ':
                        last_blank_space -= 1
                    en_str = en_str[:last_blank_space]
                    #print en_str
                elif en_str[-2:] == u'“‘':
                    #print en_str
                    en_str = en_str[:-2]
                    #print en_str
                else:
                    #print en_str
                    #print sentence
                    pass
            en_str_l.append(strF2H(en_str).strip())
            cn_str_l.append(sentence.replace(en_str, ''))
        else:
            print sentence
            raise ValueError('Warning! No en part!')
    return new_line_join(en_str_l), new_line_join(cn_str_l), new_line_join(en_cn_str_l)


def process_examples(words_d):
    path_to_example = [('all', '', True), ('key', 'usages', False), ('all','',True),('key','examples',False)]
    example_iter = iter_through_general(words_d, path_to_example)
    for word, usage_index, example_str in example_iter:
        examples_en, examples_cn, examples_encn = sep_en_cn_sentence(example_str)
        words_d[word]['usages'][usage_index]['examples_d'] = {'en': examples_en, 'cn': examples_cn, 'en_cn': examples_encn}
    return words_d


match_ants_en_part_re = re.compile(ur'[a-zéï][a-zéï ,-/]+(?=[　\u4e00-\u9fa5（]|$)', re.I)


def sep_en_cn_ants(ants_str):
    if ants_str == '':
        return '', '', '', 0
    ants_str = ants_str[2:]
    num_ants_of_explanations = 0
    en_str_l = match_ants_en_part_re.findall(ants_str)
    num_ants_of_explanations = len(en_str_l)
    # test
    if num_ants_of_explanations == 0:
        print 'Warning! No en part!', ants_str
    cn_str = match_ants_en_part_re.sub('', ants_str).strip(' \n')
    search_en_fun = lambda _str: re.search(r'[a-z]', _str, re.I)
    if search_en_fun(cn_str):
        print 'Warning! en in cn part!', cn_str
    en_cn = ants_str.strip(' \n')
    return '; '.join(en_str_l), cn_str, en_cn, num_ants_of_explanations


def process_all_ants(words_d):
    path_to_ants = [('all','',True),('key','usages',False),('all','',True),('key','ants',False)]
    ants_iter = iter_through_general(words_d, path_to_ants)
    for word, usage_index, ant_str in ants_iter:
        en_str, cn_str, en_cn_str, num_exps = sep_en_cn_ants(ant_str)
        words_d[word]['usages'][usage_index]['ants_d'] = {'en': en_str, 'cn': cn_str, 'en_cn': en_cn_str}
        # test
        if num_exps > 1:
            #print word
            pass
    return words_d


strip_first_two_chars_fun = lambda _str: _str[2:]


def process_all_syns(words_d):
    path_to_syns = [('all','',True),('key','usages',False),('all','',True),('key','syns',False)]
    for word, usage_index, syns_str in iter_through_general(words_d, path_to_syns):
        usage_d = words_d[word]['usages'][usage_index]
        usage_d['syns'] = strip_first_two_chars_fun(syns_str)
    return words_d

def main(file_name=None):
    if file_name is None:
        file_name = file_new_3000
    # for module call
    if not os.path.isfile(file_name):
        return
    new3000_base_str = codecs_open_r_utf8(file_new_3000)
    new3000_base_list_data_l = extract_content_between(new3000_base_str, match_new3000_list_start_re)
    new3000_base_list_data_l[30] = strip_last_list(new3000_base_list_data_l[30])
    new3000_base_unit_data_l_l = map(functools.partial(extract_content_between, 
                                                       match_re=match_unit_start_re), 
                                     new3000_base_list_data_l)
    new3000_base_d = get_new3000_base_d(new3000_base_unit_data_l_l)
    # revise
    subset_to_revise_d = {word:deepcopy(new3000_base_d[word]) for word in ['anarchist', 'compliment', 'antediluvian', 'anecdote']}
    subset_to_revise_d = revise_word_base_data(subset_to_revise_d)
    new3000_base_d.update(subset_to_revise_d)
    del subset_to_revise_d, new3000_base_list_data_l, new3000_base_unit_data_l_l, new3000_base_str
    revise_entry_name(new3000_base_d)
    complex_ders_d, new3000_base_d = gen_usages_for_all_words(new3000_base_d)
    new3000_base_d.update(complex_ders_d)
    del complex_ders_d
    new3000_base_d = process_exp_field_for_all_words(new3000_base_d)
    new3000_base_d = revise_no_sep(new3000_base_d)
    new3000_base_d = process_examples(new3000_base_d)
    new3000_base_d['enfranchise']['usages'][1]['ants'] = new3000_base_d['enfranchise']['usages'][1]['ants'].replace(u'subdue; enthrall', u'subdue, enthrall')
    new3000_base_d = process_all_ants(new3000_base_d)
    new3000_base_d = process_all_syns(new3000_base_d)
    with codecs.open('new3000_base_d.txt', 'w', encoding='utf-8') as f:
        json.dump(new3000_base_d, f)
if __name__ == '__main__':
    main()