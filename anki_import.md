
# 说明

这个notebook展示了如何将一个json对象转换为可导入Anki的文件。重点在于Anki中NoteType的设计。内容上承接explore_all_in_one.ipynb。

《GRE核心词汇考法精析》、《GRE核心词汇助记与精练》以及从网上找到的《不择手段背单词》对应NoteType为GreWord。
《GRE高分必备短语搭配》对应NoteTpye为GrePhrase。

notebook执行完后，会自动生成两个脚本，名字参见变量file_name_greword，file_name_grephrase。单独运行两个脚本也可完成转换，只要有python就可使用。

子章节《处理发音文件》和《添加文件》，需要许多定制文件。所以没有导出到转换脚本。如果没有对应文件的话，直接运行这个notebook而会报错。所以如果只想得到无发音无笔记版本的导入文件，请运行那两个转换脚本。

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
import os
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

## 核心转换函数


```python
%%sync_to_file $configCreAnkiImpGreWord
def add_field_audio_and_mynotes():
    if no_data_new3000:
        print 'New3000 data file does not exists! Nothing can be done...'
        return
    iter_path = [('all','',False), ('key','usages',False),('all','',False)]
    for usage_d, in iter_through_general(new3000_base_d, iter_path):
        usage_d['audio'] = ''
        usage_d['mynotes'] = ''
```


```python
add_field_audio_and_mynotes()
```


```python
# test
#pprint(new3000_base_d['abandon'])
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
```

上面的函数构建了基本的Anki导入文件。现在还需要将发音文件的指针添加进去。  
如果是更新原有的note，那么还需要将原有note的mynotes字段取出来，放到output_list的对应位置。  
所以先不执行下面的函数。等到数据补充齐全后再运行。


```python
%%sync_to_file $configCreAnkiImpGreWord
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
```


```python
%%sync_to_file $configCreAnkiImpGreWord -p
if __name__ == '__main__':
    main()
```

## 处理发音文件的思路

Anki中，添加发音文件的语法是`[sound:发音文件指针]`。发音文件指针即发音文件的文件名。所有相关文件必须放在Anki自己的`collection.media`文件夹里。所以路径应该使用相对引用。

接下来，从各个发音库抽取文件指针，并且将相应文件拷贝到Anki的`collection.media`文件夹下，同时将指针添加到new3000_base_d中。

## 再要你命3000中的多音词


```python
print new3000_base_d['addict']['usages'][0].keys()
```

    [u'exp_d', u'pspeech', u'ph_symbl', u'ants_d', u'der', u'ants', 'mynotes', u'examples', u'examples_d', u'exp', 'audio', u'syns']
    


```python
path_to_pron = [('all','',True), ('key','usages',False), ('all','',True),('key','ph_symbl',False)]
pre_word_pron = None
multi_pron_word_set = set()
for word, usage_index, word_pron in iter_through_general(new3000_base_d, deepcopy(path_to_pron)):
    if usage_index > 0:
        if word_pron != pre_word_pron:
            multi_pron_word_set.add(word)
    else:
        pre_word_pron = word_pron
```


```python
print multi_pron_word_set
```

    set([u'incarnate', u'articulate', u'appropriate', u'incense', u'subordinate', u'animate', u'surmise', u'content', u'duplicate', u'escort', u'moderate', u'compliment', u'entrance', u'intimate', u'addict', u'compound', u'aggregate', u'discharge', u'diffuse', u'convert', u'elaborate', u'exploit', u'contract', u'project', u'initiate', u'ally', u'alloy', u'intrigue'])
    

## 来源：dsl格式字典

dsl格式的Longman Pronunciation Dictionary 3rd Ed.

关于处理dsl的基本知识，参考[Full Text Search in GoldenDict](https://lisok3ajr.wordpress.com/2012/09/18/full-text-search-in-goldendict/)

### 读取数据


```python
import gzip
```


```python
file_pronunciation = 'D:\Eudict\dsl\En-En_Longman_Pronunciation3\En-En-Longman_Pronunciation.dsl.dz'
dsl_str = gzip.open(file_pronunciation, mode='r').read().decode('utf-16')
print dsl_str[100:400]
```

    sh"
    
    A
    	[m1][b]A, a[/b] [i] name of letter[/i] [p]BrE[/p] [s]uk_ld44a.wav[/s] [p]AmE[/p] [s]us_l3a-2.wav[/s] [c mediumblue]eɪ[/c][/m]
    	[m1]▷ [b]A's, As, a's[/b] [c mediumblue]eɪz[/c][i] —Communications code name:[/i][c darkmagenta] Alfa[/c][/m]
    	[m1]▶[b][c blue]ˌ[/c]A[c blue]ˈ[/c]1[c blue]◂[/c], [c 
    


```python
match_word_fun = lambda word: re.search('^(%s)[ \t]*$(.*?)(?=^[^ \t])'%word, dsl_str, re.M|re.S)
findall_word_fun = lambda word: re.findall('^(%s)[ \t]*$(.*?)(?=^[^ \t])'%word, dsl_str, re.M|re.S)
match_us_pron_re = re.compile('\[s\](us.*?)\[/s\]')
```

有的单词，其下属派生词，以▷标识，也有自己的音标。这部分中可能出现斜体字，以[i]..[/i]标识。只有主释义单词后面的斜体才是音标。


```python
match_pspeech_re = re.compile('^[ \t]*?\[m1\]\[b\].*?\[/b\] \[i\] ([a-z, ]+).*?\[/i\]', re.M)
```


```python
# test
def unit_test():
    result = match_word_fun('content')
    result_str = result.group()
    print result_str
    print 'All pronunciation files: ', match_us_pron_re.findall(result_str)
    print 'All part of speech: ', match_pspeech_re.findall(result_str)
#unit_test()    
del unit_test
```

### 将dsl_str转换为dict


```python
extract_word_block_re = re.compile(ur'^([a-z-]+)[ \t]*$(.*?)(?=^[^ \t])', re.M|re.S|re.I)
```


```python
# test
#extract_word_block_re.findall(dsl_str[0:5000])
```


```python
dsl_pron_d = {}
for one_match_obj in extract_word_block_re.finditer(dsl_str):
    word = one_match_obj.group(1)
    if word in dsl_pron_d:
        print '%s already exists!'%word
    one_word_d = {}
    word_block = one_match_obj.group(2)
    one_word_d['word_block'] = word_block
    one_word_d['pspeech_l'] = match_pspeech_re.findall(word_block)
    one_word_d['ph_symbol_l'] = match_us_pron_re.findall(word_block)  
    if word in multi_pron_word_set:
        #print 'check pspeech'
        #print word, one_word_d['pspeech_l']
        pass
    dsl_pron_d[word] = one_word_d
```


```python
# example
iter_print(dsl_pron_d['content'])
```

     word_block
       	{{Roman}}I{{/Roman}}
       	[m1][b]con|tent[/b] [i] adjective, verb, noun 'contentment'[/i] [p]BrE[/p] [s]uk_ld44content.wav[/s] [p]AmE[/p] [s]us_l3content2.wav[/s] [c mediumblue]kən |ˈtent[/c] [p]§[/p]\ [sub]([/sub]ˌ[sub])[/sub]kɒn-[/m]
       	[m1]▷ [b]con|tented[/b] [c mediumblue]ˈtent ɪd[/c] -əd [p]AmE[/p]\ [c mediumblue]ˈten[i]t̬[/i] əd[/c][/m]
       	[m1]▷ [b]con|tenting[/b] [c mediumblue]ˈtent ɪŋ[/c] [p]AmE[/p]\ [c mediumblue]ˈten[i]t̬[/i] ɪŋ[/c][/m]
       	[m1]▷ [b]con|tents[/b] [c mediumblue]ˈten[i]t[/i]s[/c][/m]
       	{{Roman}}II{{/Roman}}
       	[m1][b]content[/b] [i] noun 'matter contained'[/i] [p]BrE[/p] [s]uk_content2.wav[/s] [p]AmE[/p] [s]us_l3content.wav[/s] [c mediumblue]ˈkɒn tent[/c] [p]AmE[/p]\ [c mediumblue]ˈkɑːn-[/c][/m]
       	[m1]▷ [b]content|s[/b] [c mediumblue]s[/c][/m]
     ph_symbol_l
       0
         us_l3content2.wav
       1
         us_l3content.wav
     pspeech_l
       0
         adjective, verb, noun 
       1
         noun 
    

### 统计词性对应关系


```python
def summary_pspeech():
    #dsl
    dsl_pspeech_set = set()
    for word, word_d in dsl_pron_d.iteritems():
        dsl_pspeech_l = word_d['pspeech_l']
        for pspeech in dsl_pspeech_l:
            dsl_pspeech_set.add(pspeech)
    # new3000
    new3000_pspeech_set = set()
    path_to_pspeech = path_to_pron = [('all','',True), ('key','usages',False), ('all','',False),('key','pspeech',False)]
    for word, pspeech in iter_through_general(new3000_base_d, path_to_pspeech):
        for sub_pspeech in pspeech.split('/'):
            new3000_pspeech_set.add(sub_pspeech)
        stripped_pspeech = pspeech.strip('.')
        if word in dsl_pron_d:
            for dsl_pspeech in dsl_pron_d[word]['pspeech_l']:
                if dsl_pspeech.startswith(stripped_pspeech):
                    break
            else:
                if len(dsl_pron_d[word]['ph_symbol_l']) > 1:
                    #print 'pspeech of %s in new3000 not match with dsl'%word
                    # a lot!
                    pass
    print dsl_pspeech_set
    print new3000_pspeech_set
```


```python
# summary_pspeech()
```

dsl_pron_n中的有效词性类别：adjective verb pronoun preposition adverb  
所以，只要看看dsl_pron_n中的词性是不是以new3000_base_d中的开头就可以。

## 再要你命3000同dsl_d比较

将西欧字符转换为普通字符，即éï转为ei


```python
def check_pron_in_new3000_and_dsl(word, print_only_bad_result = True):
    word_converted = word.replace(u'é', 'e').replace(u'ï', 'i').split('/')[0]
    return_message_l = []
    not_found = False
    if not (word_converted in dsl_pron_d):
        return_message_l.append('**%s** not found in dsl'%word)
        not_found = True
    else:
        pron_in_dsl_l = dsl_pron_d[word_converted]['ph_symbol_l']
        pspeech_in_dsl_l = dsl_pron_d[word_converted]['pspeech_l']
        pron_new3000_l = []
        pspeech_new3000_l = []
        for usage_d in new3000_base_d[word]['usages']:
            pron_new3000_l.append(usage_d['ph_symbl'])
            pspeech_new3000_l.append(usage_d['pspeech'])
        diff_pron_new3000_set = set(pron_new3000_l)
        if len(pron_in_dsl_l) < len(diff_pron_new3000_set):
            message = '**%s** in dsl has less pron'%word
            message += '\n' + str(len(pron_in_dsl_l)) + ', ' + str(len(diff_pron_new3000_set))
            message += '\n' + ','.join(pron_in_dsl_l)
            message += '\n' + ','.join(pron_new3000_l)
            return_message_l.append(message)
        else:
            if not print_only_bad_result:
                 return_message_l.append('**%s** in dsl has enough pron'%word)
    return '\n'.join(return_message_l), not_found
```


```python
result_l = []
not_found_word_l = []
for word in new3000_base_d.iterkeys():
    message_str, not_found = check_pron_in_new3000_and_dsl(word)
    if message_str != '':
        result_l.append(message_str)
    if not_found:
        not_found_word_l.append(word)
        if word in multi_pron_word_set:
            print 'Warning! **%s** in multi_pron_word_set'%word
```


```python
with codecs.open('temp_check_pron_log.txt', 'w', encoding='utf-8') as f:
    json.dump(result_l, f, indent=5)
    json.dump(not_found_word_l, f, indent=2)
```


```python
print '%d words not found'%len(not_found_word_l)
```

    153 words not found
    

虽然还有153个没找到，但注意到，多音词都在其中。

## 用韦氏发音库补充

从网上找的韦氏发音库，网址：http://blog.emagic.org.cn/content/i1931.html

ed2k链接

        ed2k://|file|%E9%9F%A6%E6%B0%8F%E5%B8%B8%E7%94%A8%E5%8D%95%E8%AF%8D%E8%AF%AD%E9%9F%B3%E5%BA%93.rar|315458082|88b70fe90a6658cec689352f66a7af6c|h=4rblspftuskt5gfvmpbnfkdvhi2ey3fn|/


```python
path_of_media_source = 'D:\\mvoice\\'
word_list_file = 'word_list.txt'
```


```python
media_path_dict = {}
match_word = r'([a-z1-9 ~]+)\.mp3'
match_word_re = re.compile(match_word, re.I|re.M)
with codecs.open(path_of_media_source + word_list_file, encoding='utf-8') as f:
    for line in f:
        result = match_word_re.search(line)
        if not (result is None):
            media_path_dict[result.group(1)] = line.strip()
        else:
            #print line
            pass
```


```python
print media_path_dict['habit']
```

    D:\mvoice\h\habit.mp3
    


```python
count = 0
still_not_found_word_l = []
for word in not_found_word_l:
    word_converted = word.replace(u'é', 'e').replace(u'ï', 'i').split('/')[0]
    if word_converted in media_path_dict:
        count += 1
        #print 'found', word
    else:
        still_not_found_word_l.append(word)
print 'found %d of %d'%(count, len(not_found_word_l))
```

    found 57 of 153
    

## 用mdict补充

使用朗文当代第5版的mdx和mdd文件

使用插件 https://bitbucket.org/xwang/mdict-analysis



```python
from readmdict import MDX, MDD
from bs4 import BeautifulSoup
file_to_longman_mdx = "D:\Eudict\Frequent\Longman Dictionary of Contemporary English.mdx"
mdx = MDX(file_to_longman_mdx)
longman_mdx_iter = mdx.items()
longman_in_new3000_d = {}
for word, word_block in longman_mdx_iter:
    if word in new3000_base_d:
        longman_in_new3000_d[word] = word_block
print 'In longman, found %d words of new3000 (%d in total)'%(len(longman_in_new3000_d), len(new3000_base_d))
```

    In longman, found 2954 words of new3000 (3145 in total)
    

抽取音频地址


```python
# this is the pattern we gonna use
soup = BeautifulSoup(longman_in_new3000_d['abandon'],"lxml")
print soup.find_all(href=re.compile('sound.*?US'))[0]['href'][8:]
```

    US_abandon1.spx
    


```python
count = 0
still_still_not_found_word_l = []
longman_found_word_d = {}
for word in still_not_found_word_l:
    founded = False
    word_converted = word.replace(u'é', 'e').replace(u'ï', 'i').split('/')[0]
    if word_converted in longman_in_new3000_d:
        soup = BeautifulSoup(longman_in_new3000_d[word_converted],"lxml")
        find_result = soup.find_all(href=re.compile('sound.*?US'))
        if len(find_result) != 0:
            count += 1
            #print word
            founded = True
            longman_found_word_d[word] = find_result[0]['href'][8:]
    if not founded:
        still_still_not_found_word_l.append(word)
print 'found %d of %d'%(count, len(still_not_found_word_l))
```

    found 52 of 96
    


```python
# example
longman_found_word_d['ingratiating']
```




    'US_ingratiating.spx'




```python
# unzip the mdd mdx file. 
# Warning! This take a lot of time. I have already unpacked it, so commend the next line
#! python readmdict.py -x "D:\Eudict\Frequent\Longman Dictionary of Contemporary English.mdx"
```

## 添加音频指针


```python
import shutil
```


```python
anki_media_collection = os.path.expanduser('~\\Documents\\Anki\\xiaohang\\collection.media')
dsl_source_media_path = 'D:\Eudict\dsl\En-En_Longman_Pronunciation3\En-En-Longman_Pronunciation.dsl.dz.files'
longman_source_media_path = 'D:\Eudict\Frequent\data'
```


```python
def add_audio_pointer(word):
    word_converted = word.replace(u'é', 'e').replace(u'ï', 'i').split('/')[0]
    word_d = new3000_base_d[word]
    for usage_d in word_d['usages']:
        usage_d['audio'] = ''
        source_audio_file_name = None
        first_pspeech_match_obj = re.search('^([a-z]+)\.', usage_d['pspeech'])
        if first_pspeech_match_obj is None:
            print '%s has no pspeech'%word
            new3000_pspeech = ''
        else:
            new3000_pspeech = first_pspeech_match_obj.group(1)
        if new3000_pspeech in ['vt', 'vi']:
            new3000_pspeech = 'v'
        new_audio_pointer_without_ext = word_converted + '_' + new3000_pspeech
        new_audio_file_name_without_ext = anki_media_collection + '\\' + new_audio_pointer_without_ext
        new_audio_pointer_without_ext = '[sound:' + new_audio_pointer_without_ext
        existed = False
        for file_ext in ['.wav', '.mp3', '.spx']:
            if os.path.isfile(new_audio_file_name_without_ext + file_ext):
                # print 'existed!'
                existed = True
                usage_d['audio'] = new_audio_pointer_without_ext + file_ext + ']'
                break
        if existed:
            continue
        if word_converted in dsl_pron_d:
            dsl_word_d = dsl_pron_d[word_converted]
            if word in multi_pron_word_set:
                # check pspeech
                for index, dsl_pspeech in enumerate(dsl_word_d['pspeech_l']):
                    for dsl_sub_pspeech in dsl_pspeech.split(','):
                        if dsl_sub_pspeech.strip().startswith(new3000_pspeech):
                            source_audio_file_name = dsl_source_media_path + '\\' + dsl_word_d['ph_symbol_l'][index]
                            break
                else:
                    print 'no match of pspeech, word %s'%word
                    print dsl_word_d['pspeech_l'], new3000_pspeech
                    pass
            else:
                # use the first audio pointer
                source_audio_file_name = dsl_source_media_path + '\\' + dsl_word_d['ph_symbol_l'][0] 
            if not (source_audio_file_name is None):
                new_audio_pointer = new_audio_pointer_without_ext + '.wav]'
                new_audio_file_name = new_audio_file_name_without_ext + '.wav'
        else:
            # the not found word
            if word_converted in media_path_dict:
                # try webster
                source_audio_file_name = media_path_dict[word_converted]
                new_audio_pointer = new_audio_pointer_without_ext + '.mp3]'
                new_audio_file_name = new_audio_file_name_without_ext + '.mp3'
            elif word in longman_found_word_d:
                # try longman
                source_audio_file_name = longman_source_media_path + '\\' + longman_found_word_d[word]
                new_audio_pointer = new_audio_pointer_without_ext + '.spx]'
                new_audio_file_name = new_audio_file_name_without_ext + '.spx'
        if not (source_audio_file_name is None):
            usage_d['audio'] = new_audio_pointer
            shutil.copy(source_audio_file_name, new_audio_file_name)
```


```python
for word in new3000_base_d:
    add_audio_pointer(word)
```


```python
# example
word = 'compendium'
for index, usage_d in enumerate(new3000_base_d[word]['usages']):
    print usage_d['audio']
```

    [sound:compendium_n.wav]
    [sound:compendium_n.wav]
    

## 转换为mp3

到这里，电脑上已经可以发音了。但手机只支持mp3格式，所以要将collection.media中的wav和spx转换为mp3。

使用pydub+ffmpeg

参考[Pydub ](https://github.com/jiaaro/pydub/)


```python
from pydub import AudioSegment
import glob
```


```python
def convert_to_mp3():
    owd = os.getcwd()
    os.chdir(anki_media_collection)
    extension_list = ('*.wav', '*.spx')
    for extension in extension_list:
        for audio in glob.glob(extension):
            mp3_filename = os.path.splitext(os.path.basename(audio))[0] + '.mp3'
            if not os.path.isfile(mp3_filename):
                AudioSegment.from_file(audio).export(mp3_filename, format='mp3')
    os.chdir(owd)
```


```python
convert_to_mp3()
```


```python
def modify_audio_pointer():
    path_to_usage_d = path_to_pron = [('all','',False), ('key','usages',False), ('all','',False)]
    for usage_d, in iter_through_general(new3000_base_d, path_to_usage_d):
        old_audio_name = usage_d['audio']
        new_audio_name = os.path.splitext(os.path.basename(old_audio_name))[0] + '.mp3]'
        usage_d['audio'] = new_audio_name
```


```python
modify_audio_pointer()
```


```python
# test
#iter_print(new3000_base_d['chaperone'])
```

## 添加笔记


```python
old_anki_GreWord_file_name = 'old_anki_greword.txt'
```


```python
def add_mynotes():
    if not os.path.isfile(old_anki_GreWord_file_name):
        return
    old_data_line_l = codecs_open_r_utf8(old_anki_GreWord_file_name).split('\n')
    for line in old_data_line_l:
        field_l = line.split('\t')
        word = field_l[1]
        usage_index = int(field_l[2])
        my_note = field_l[6]
        if my_note != '':
            new3000_base_d[word]['usages'][usage_index-1]['mynotes'] = my_note
```


```python
add_mynotes()
```

## 生成文件


```python
greword_import_data_l = convert_to_GreWord()
with codecs.open(output_file_GreWord, 'w', encoding='utf-8') as f:
    for one_line in greword_import_data_l:
        one_string = u'\t'.join(one_line) + '\n'
        f.write(one_string)
```


```python
# test
#iter_print(new3000_base_d['hike'])
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
        my_notes = ''
        for phrase_uid, phrase_dict in duanyu_base_d.iteritems():
            one_line = [phrase_uid, phrase_dict['phrase'], phrase_dict['usage_index'], my_notes,
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
    if not (duanyu_base_d is None):
        convert_to_GrePhrase()
```


```python
! jupyter nbconvert anki_import.ipynb --to markdown
! jupyter nbconvert anki_import.ipynb -- to html
```

    [NbConvertApp] WARNING | Collisions detected in jupyter_nbconvert_config.py and jupyter_nbconvert_config.json config files. jupyter_nbconvert_config.json has higher priority: {
      "Exporter": {
        "template_path": "['.', 'C:\\\\Users\\\\xiaohang\\\\AppData\\\\Roaming\\\\jupyter\\\\templates'] ignored, using [u'C:\\\\Users\\\\xiaohang\\\\AppData\\\\Roaming\\\\jupyter\\\\templates']"
      }
    }
    C:\Users\xiaohang\Anaconda\lib\site-packages\IPython\nbconvert.py:13: ShimWarning: The `IPython.nbconvert` package has been deprecated. You should import from ipython_nbconvert instead.
      "You should import from ipython_nbconvert instead.", ShimWarning)
    [NbConvertApp] Converting notebook anki_import.ipynb to markdown
    [NbConvertApp] Writing 31332 bytes to anki_import.md
    [NbConvertApp] WARNING | Collisions detected in jupyter_nbconvert_config.py and jupyter_nbconvert_config.json config files. jupyter_nbconvert_config.json has higher priority: {
      "Exporter": {
        "template_path": "['.', 'C:\\\\Users\\\\xiaohang\\\\AppData\\\\Roaming\\\\jupyter\\\\templates'] ignored, using [u'C:\\\\Users\\\\xiaohang\\\\AppData\\\\Roaming\\\\jupyter\\\\templates']"
      }
    }
    [NbConvertApp] WARNING | pattern u'to' matched no files
    [NbConvertApp] WARNING | pattern u'html' matched no files
    C:\Users\xiaohang\Anaconda\lib\site-packages\IPython\nbconvert.py:13: ShimWarning: The `IPython.nbconvert` package has been deprecated. You should import from ipython_nbconvert instead.
      "You should import from ipython_nbconvert instead.", ShimWarning)
    [NbConvertApp] Converting notebook anki_import.ipynb to html
    [NbConvertApp] Writing 294465 bytes to anki_import.html
    
