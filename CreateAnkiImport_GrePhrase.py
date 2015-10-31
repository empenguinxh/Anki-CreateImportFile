# coding:utf-8
import json
import codecs
import os.path
from my_helpers import *
file_name_duanyu = 'duanyu_base_d.txt'
duanyu_base_d = is_file_and_json_load(file_name_duanyu)
output_file_GrePhrase = 'AnkiImportData_GrePhrase.txt'
def convert_to_GrePhrase():
    with codecs.open(output_file_GrePhrase, 'w', encoding='utf-8') as f:
        for phrase_uid, phrase_dict in duanyu_base_d.iteritems():
            one_line = [phrase_uid, phrase_dict['phrase'], phrase_dict['usage_index'],
                        phrase_dict['en_exp'], phrase_dict['cn_exp'], 
                        phrase_dict['example'], phrase_dict['gre_example_cn'],
                        phrase_dict['gre_example_en']]
            one_line = '\t'.join(one_line) + '\n'
            f.write(one_line)
if __name__ == '__main__':
    convert_to_GrePhrase()
