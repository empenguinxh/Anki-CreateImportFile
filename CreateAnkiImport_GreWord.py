# coding:utf-8
import json
import codecs
import os
from my_helpers import *
file_name_new3000 = 'new3000_base_d.txt'
file_name_zhuji = 'zhuji_base_d.txt'
file_name_bzsdbdc = 'base_data\\bzsdbdc_dic.txt'
output_file_GreWord = 'AnkiImportData_GreWord.txt'
new3000_base_d = None
zhuji3000_base_d = None
bzsdbdc_data = None
new3000_base_d = is_file_and_json_load(file_name_new3000)
zhuji3000_base_d = is_file_and_json_load(file_name_zhuji)
bzsdbdc_data = is_file_and_json_load(file_name_bzsdbdc)
no_data_new3000 = new3000_base_d is None
no_data_zhuji = zhuji3000_base_d is None
no_data_bzsdbdc = bzsdbdc_data is None
def add_field_audio_and_mynotes():
    if no_data_new3000:
        print 'New3000 data file does not exists! Nothing can be done...'
        return
    iter_path = [('all','',False), ('key','usages',False),('all','',False)]
    for usage_d, in iter_through_general(new3000_base_d, iter_path):
        usage_d['audio'] = ''
        usage_d['mynotes'] = ''
def convert_to_GreWord():
    if no_data_new3000:
        print 'New3000 data file does not exists! Nothing can be done...'
        return
    if no_data_zhuji:
        print 'No data of zhuji!'
    if no_data_bzsdbdc:
        print 'No data of bzsdbdc!'
    output_list = []
    None_repr = u''
    join_by_line_break = u'<br>'.join
    replace_with_br = lambda _str: _str.replace('\n', '<br>')
    tag_pos_prefix = ' in_'
    for word in new3000_base_d:
        # new 3000 part
        """
        the structure of a word of new3000_base_d.txt

        {'phon': u"[\u02cc\xe6d'l\u026ab]",
         'pos': (1, 6),
         'usages': [{'ants': u'\u53cd\u3000considered, planned, premeditated, rehearsed \u9884\u5148\u8ba1\u5212\u7684',
                     'ants_d': {'cn': u'\u9884\u5148\u8ba1\u5212\u7684',
                                'en': u'considered, planned, premeditated, rehearsed ',
                                'en_cn': u'considered, planned, premeditated, rehearsed \u9884\u5148\u8ba1\u5212\u7684'},
                     'der': '',
                     'examples': u'content...',
                                    'en': u'not bad for an ad-lib comedy routine',
                                    'en_cn': u'content...'},
                     'exp': u'*adj.* \u5373\u5174\u7684\uff1amade or done **without previous thought or preparation**',
                     'exp_d': {'cn': u'\u5373\u5174\u7684',
                               'en': u'made or done **without previous thought or preparation**',
                               'en_cn': u'\u5373\u5174\u7684\uff1amade or done **without previous thought or preparation**'},
                     'ph_symbl': u"[\u02cc\xe6d'l\u026ab]",
                     'pspeech': u'adj.',
                     'syns': u'content...'}
        """
        one_new3000_word_d = new3000_base_d[word]
        word_pos_L, word_pos_U = one_new3000_word_d['pos']
        word_pos = u'L' + unicode(word_pos_L) + u' U' + unicode(word_pos_U)
        num_usages = len(one_new3000_word_d['usages'])
        usages_tag = unicode(num_usages) + u'_usage'

        for usage_index, usage in enumerate(one_new3000_word_d['usages']):
            word_phs = usage['ph_symbl'] 
            word_tags = usages_tag + tag_pos_prefix + 'zaiyaoniming3000'
            if not no_data_zhuji:
                if word in zhuji3000_base_d:
                    word_tags += tag_pos_prefix + 'zhuji3000'
            if not no_data_bzsdbdc:
                if word in bzsdbdc_data:
                    word_tags += tag_pos_prefix + 'bzsdbdc'
            usage_index = unicode(usage_index+1)
            word_uid = unicode(word) + usage_index
            ph_symbl = usage['ph_symbl']
            word_Audio = usage['audio']
            pspeech = usage['pspeech']
            exp_en = usage['exp_d']['en']
            exp_cn = usage['exp_d']['cn']
            exp_en_cn = usage['exp_d']['en_cn']
            # combine other explanation
            #usage_index_l = range(num_usages)
            #usage_index_l.remove(usage_index)
            #exp_other = ['**考法%d**:'%(i+1) + one_new3000_word_d['usages'][i]['exp_d']['en_cn'] +'\n' for i in usage_index_l]
            # use word_block_str as all explanation
            exp_all = one_new3000_word_d['word_block_str']
            examples_en = usage['examples_d']['en']
            examples_cn = usage['examples_d']['cn']
            examples_en_cn = usage['examples_d']['en_cn']
            examples_others = ''
            ants_en = usage['ants_d']['en']
            ants_cn = usage['ants_d']['cn']
            ants_en_cn = usage['ants_d']['en_cn']
            syns = usage['syns']
            # der from the book zaiyaoniming3000
            der_new3000 = usage['der']
            
            # bzsdbdc part
            how_to_mem_bzsdbdc = None_repr
            if not no_data_bzsdbdc:
                if word in bzsdbdc_data:
                    how_to_mem_bzsdbdc = bzsdbdc_data[word]['combined']         

            # zhuji3000 part
            how_to_mem_zhuji3000, eytma_gr, eytma_gr_exp, eytma_cognates = None_repr, None_repr, None_repr, None_repr
            '''
            the structure of a word of zhuji3000_base_d
            {'content': u'[\u6839] per- [through] + vad [go] + -e [v.], go through, \u904d\u5e03 \u2192 vt. \u5f25\u6f2b\uff0c\u5145\u6ee1\n',
            'ety': 'vad, vag, ced',
            'etyma_cognates_l': u'pervade, evasive, extravagant, vague, cessation, incessant',
            'etyma_group_explanation': u'group explanation content',
            'phon': u"[p\u0259r've\u026ad]",
            'pos': u'6, 7',
            'summary': u'summary content',
            'word': u'pervade'}
            '''
            if not no_data_zhuji:
                if word in zhuji3000_base_d:
                    how_to_mem_zhuji3000 = zhuji3000_base_d[word]['content']
                    eytma_gr = zhuji3000_base_d[word]['ety']
                    eytma_gr_exp = zhuji3000_base_d[word]['etyma_group_explanation']
                    eytma_cognates = zhuji3000_base_d[word]['etyma_cognates_l']
            mynotes = usage['mynotes']
            """
            Anki GreWord Structure
            word_uid  word  usage_index  ph_symbl  word_audio  pspeech  mynotes
            exp_en exp_cn exp_en_cn exp_all
            examples_en examples_cn examples_encn examples_others
            ants_en ants_cn ants_encn
            syns der_new3000 
            how_to_mem_bzsdbdc how_to_mem_zhuji3000 
            etyma_group etyma_group_exp etyma_cognates
            position tags
            """
            one_line = [word_uid, word, usage_index, ph_symbl, word_Audio, pspeech, mynotes, 
                        exp_en, exp_cn, exp_en_cn, exp_all, 
                        examples_en, examples_cn, examples_en_cn, examples_others,
                        ants_en, ants_cn, ants_en_cn] +\
                       [syns, der_new3000, how_to_mem_bzsdbdc, how_to_mem_zhuji3000,
                        eytma_gr, eytma_gr_exp, eytma_cognates, word_pos, word_tags]
            for index, _str in enumerate(one_line):
                _str = replace_with_br(collapse_blank_line(_str).strip(' \n'))
                one_line[index] = custom_html_element(_str)
            output_list.append(one_line)
    output_list.sort(key=lambda x: x[0])
    return output_list
def main():
    add_field_audio_and_mynotes()
    output_list = convert_to_GreWord()
    if output_list is None:
        return
    with codecs.open(output_file_GreWord, 'w', encoding='utf-8') as f:
        for one_line in output_list:
            one_string = u'\t'.join(one_line) + '\n'
            f.write(one_string) 
    del output_list
if __name__ == '__main__':
    main()
