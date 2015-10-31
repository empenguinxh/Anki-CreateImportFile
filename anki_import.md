
# 说明

这个notebook展示了如何将一个json对象转换为可导入Anki的文件。重点在于Anki中NoteType的设计。内容上承接explore_all_in_one.ipynb。

《GRE核心词汇考法精析》、《GRE核心词汇助记与精练》以及从网上找到的《不择手段背单词》对应NoteType为GreWord。
《GRE高分必备短语搭配》对应NoteTpye为GrePhrase。

notebook执行完后，会自动生成两个脚本，名字参见变量file_name_greword，file_name_grephrase。单独运行两个脚本也可完成转换，只要有python就可使用。

转换出的Anki导入文件，名字参见变量output_file_GreWord，output_file_GrePhrase。


```python
%run sync_to_file_magic_command.py
```


```python
file_name_greword = 'CreateAnkiImport_GreWord.py'
file_name_grephrase = 'CreateAnkiImport_GrePhrase.py'
configCreAnkiImpGreWord = file_name_greword
configCreAnkiImpGrePhrase = file_name_grephrase
configMyHelpers = 'my_helpers.py'
```

# 补充两个辅助函数


```python
%%sync_to_file $configMyHelpers
def custom_html_element(_str):
    """
    convert the markdown notations in a string to html tags
    currently, only two kinds of markdown notation exist in all the strings
    ** and *
    """
    formatted_str = _str
    # format double asterisk
    match_double_asterisk_re = re.compile(u'\*\*(.*?)\*\*')
    # replace **...** with <strong>...</strong>
    #formatted_str = match_double_asterisk_re.sub(r'<strong>\1</strong>', formatted_str)
    # replace **...** with <ins>...</ins>
    formatted_str = match_double_asterisk_re.sub(r'<ins>\1</ins>', formatted_str)
    # format single asterisk
    # replace *...* with <i>...</i>
    match_single_asterisk_re = re.compile(u'\*(.*?)\*')
    formatted_str = match_single_asterisk_re.sub(r'<i>\1</i>', formatted_str)
    return formatted_str
```


```python
%%sync_to_file $configMyHelpers
def is_file_and_json_load(file_name_str):
    if os.path.isfile(file_name_str):
        with codecs.open(file_name_str, 'r', encoding='utf-8') as f:
            json_d = json.load(f)
        return json_d
```


```python
%%sync_to_file $configCreAnkiImpGreWord $configCreAnkiImpGrePhrase -m o

# coding:utf-8
import json
import codecs
import os.path
from my_helpers import *
```

# GreWord


```python
# example
test_str = 'to **put an end to**(something planned or previously agreed to)'
print custom_html_element(test_str)
del test_str
```

    to <ins>put an end to</ins>(something planned or previously agreed to)
    


```python
%%sync_to_file $configCreAnkiImpGreWord
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
```


```python
%%sync_to_file $configCreAnkiImpGreWord
no_data_new3000 = new3000_base_d is None
no_data_zhuji = zhuji3000_base_d is None
no_data_bzsdbdc = bzsdbdc_data is None
```


```python
%%sync_to_file $configCreAnkiImpGreWord
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
            word_Audio = ''
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
            mynotes = None_repr
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
    
    with codecs.open(output_file_GreWord, 'w', encoding='utf-8') as f:
        for one_line in output_list:
            one_string = u'\t'.join(one_line) + '\n'
            f.write(one_string)  
```


```python
convert_to_GreWord()
```


```python
%%sync_to_file $file_name_greword -p

if __name__ == '__main__':
    convert_to_GreWord()
```

# GrePhrase


```python
%%sync_to_file $configCreAnkiImpGrePhrase
file_name_duanyu = 'duanyu_base_d.txt'
duanyu_base_d = is_file_and_json_load(file_name_duanyu)
output_file_GrePhrase = 'AnkiImportData_GrePhrase.txt'
```


```python
print 'The structure of duanyu_base_d'
pprint(duanyu_base_d['under one\'s control1'])
```

    The structure of duanyu_base_d
    {u'cn_exp': u'\u5728\u2026\u2026\u7684\u63a7\u5236\u4e4b\u4e0b',
     u'en_exp': u'If something is **under** your **control**, you have the **power to make** all the important **decisions** about the way that it is run.',
     u'example': u'The current protest doesn\u2019t look likely to be brought under government\u2019s control any time soon.',
     u'gre_example_cn': u'\u5f53\u5fb7\u514b\u8428\u65af\u5dde\u8fd8\u5904\u4e8e\u58a8\u897f\u54e5\u7684\u7ba1\u8f96\u4e2d\u65f6\uff0c\u5c3d\u7ba1\u58a8\u897f\u54e5\u653f\u5e9c\u6781\u529b\u529d\u963b\u6765\u81ea\u7f8e\u56fd\u7684\u79fb\u6c11\uff0c\u5fb7\u5dde\u7684\u4eba\u53e3\u8fd8\u662f\u7ffb\u4e86\u4e24\u756a\u3002',
     u'gre_example_en': u'While Texas was under Mexican control, the population of Texas quadrupled, in spite of the fact that Mexico discouraged immigration from the United States.',
     u'phrase': u"under one's control",
     u'pos': 7,
     u'usage_index': u'1'}
    


```python
%%sync_to_file $configCreAnkiImpGrePhrase
def convert_to_GrePhrase():
    with codecs.open(output_file_GrePhrase, 'w', encoding='utf-8') as f:
        for phrase_uid, phrase_dict in duanyu_base_d.iteritems():
            one_line = [phrase_uid, phrase_dict['phrase'], phrase_dict['usage_index'],
                        phrase_dict['en_exp'], phrase_dict['cn_exp'], 
                        phrase_dict['example'], phrase_dict['gre_example_cn'],
                        phrase_dict['gre_example_en']]
            one_line = '\t'.join(one_line) + '\n'
            f.write(one_line)
```


```python
convert_to_GrePhrase()
```


```python
%%sync_to_file $file_name_grephrase -p

if __name__ == '__main__':
    convert_to_GrePhrase()
```


```python
! jupyter nbconvert anki_import.ipynb --to markdown
! jupyter nbconvert anki_import.ipynb -- to html
```

    [NbConvertApp] Converting notebook anki_import.ipynb to markdown
    [NbConvertApp] Writing 12102 bytes to anki_import.md
    [NbConvertApp] WARNING | pattern u'to' matched no files
    [NbConvertApp] WARNING | pattern u'html' matched no files
    [NbConvertApp] Converting notebook anki_import.ipynb to html
    [NbConvertApp] Writing 209433 bytes to anki_import.html
    


```python

```
