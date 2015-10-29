
# 使用说明


## 简介

在之前的《Anki系列-用Anki准备GRE》中，我承诺提供转换用的脚本文件。旧版本的脚本使用起来很麻烦，所以重写了一份，精简代码结构，并且将全文以markdown的方式分享到简书，方便感兴趣的人与我讨论。

这个notebook展示了处理kindle版《GRE核心词汇考法精析》、《GRE核心词汇助记与精练》、《GRE高分必备短语搭配》的过程。目的是生成可以导入Anki的txt文档。《GRE核心词汇考法精析》、《GRE核心词汇助记与精练》生成的导入文件对应的Note结构为GreWord，《GRE高分必备短语搭配》生成的则对应PhraseGRE。 

首先你要从Amazon.cn购买者三本书的电子版（[1](http://www.amazon.cn/GRE/dp/B00GWD2L4W/)、[2](http://www.amazon.cn/dp/B00NXCXBSK)、[3](http://www.amazon.cn//dp/B00SMNMHDK/)）。你并不需要拥有一台Kindle才能购买上述电子书。只需要在电脑上下载Kindle的客户端，安装后登陆你的Amazon账号即可。然后，你需要利用[Calibre](http://calibre-ebook.com/)将书籍转换为txt格式以便让python处理。转换过程中，需要在“TXT Output”那里将Formatting设置为markdown，以便提取原书中的一些格式信息；“Line ending style”选择unix；“Output Encoding”选择'utf-8'。

转换后，默认文档名分别为

    "GREHe Xin Ci Hui Kao Fa Jing Xi  (Xin Dong Fang Da Yu Ying Yu Xue Xi Cong Shu ) - Chen Qi.txt"
    "GREHe Xin Ci Hui Zhu Ji Yu Jing - Cao Tian Cheng.txt"
    "GREGao Fen Bi Bei Duan Yu Da Pe - Yan Yu Zhen ,Gao Yu ,Chen Qi.txt"
    
假定你没有修改文件名，并且按照相对路径将这3个txt放到了与该notebook相同路径的"base_data"文件夹中。如果你安装了jupyter notebook，可以打开并运行这个.ipynb文件。它会自动在当前目录下生成三个`_base_d`文件，对应三个txt源文件，可以被AnkiImport脚本调用。另外还会生成三个py脚本文件，可以独立使用，功能都是读入txt源文件并转换，生成对应的`_base_d`文件。这些脚本文件以及AnkiImport脚本会在《Anki系列-用Anki准备GRE》的更新版本中提供，敬请期待。

本notebook后续会用三个章节分别处理这三个源文档。  
第一步当然是将源文档的内容读入为字符串。  
每个章节，代码的最终目的都是将读入的字符串以单词释义为单位，转换为python中的字典结构。这之间需要将字符串一步步切分（split），剔除掉不必要的信息。切分的规则通过观察txt文档并寻找规律得来。 


## 勘误

处理过程中可能会发现源文档中的错误。发现方法是程序辅助、手动在txt源文档中定位。  
至于处理方法，尽管直接修改txt源文件可能更方便，本文为了自动化所有流程，还是选择了费事些的方法，即手工编写规则，让程序自动处理内存中的对象，同时也可避免修改txt源文件。  
所有涉及到勘误的地方，都可通过搜索关键词“【勘误】”而定位到相关的文字说明，搜索“revise”加上所修改单词的拼写可以看到代码上的实现。有时发现【勘误】后需要返回前面修改代码，所以文字说明和代码可能有错位。

## 变量命名规则

以易于理解为第一目标。一个变量通常由表示变量意义的主体加上表示变量类别的后缀组成。  
后缀用来表明变量的数据类型，具体规则：
+ `_l、_d` 分别代表列表、字典
+ `_str` 代表字符串。由于涉及到中文的处理，一般会将字符串转变为对应的unicode对象，而后者在操作上又与一般的字符串没有区别。所以也用该后缀代表unicode对象。另外，使用`_str`可以强调该变量的文本意义，尽管在程序内部可能是一个unicode。
+ `_uni` 特别强调该变量代表一个unicode对象
+ `_re` 表示编译后的正则表达式
+ `_fun` 表示变量内存放的是一个函数
+ `_boo` 表示布尔变量
+ `_iter` 泛指一个可以顺序遍历的对象
+ 后缀可以互相组合，表示嵌套的数据结构，左侧后缀嵌套于右侧后缀。比如双重后缀`_str_l`表示一个存放字符串的列表，`_l_l`表示一个嵌套列表，即一个列表的每个元素本身即是一个列表。像`_l_l`这种后缀，意义在于强调该如何使用变量。假如不存在强调的目的，就会只使用`_l`表示一个嵌套列表，也可能不使用后缀。

## 函数命名规则

更加灵活，前面的变量后缀也可能用于函数中，但可能出现在任意位置。主要目的是提示函数的用途、返回值的数据类型等。  
函数的参数命名规则与变量命名规则相同。

## test, check, example

+ test  
一个功能实现完了，不知道能不能用，所以找个简单的例子试一下。test可以帮助修复一些简单的bug，近似于草稿本上的演算步骤。因为是草稿，所以确认无误后会注释掉，节省空间。  
还有一种情况，写程序时，想知道某个变量的具体值是什么。一般会选择`print`这个变量。这部分信息可以辅助程序编写，而写好后为了节省空间，一般会注释掉`print`语句。为了方便后续的检查，以及未来可能的修改，只注释引起程序输出的语句，保留起条件判断的。  
总之，注释test语句的原则是，尽量减少未来需要再次test时需要重写的代码数量。

+ check  
调用了之前实现的某个函数，检查下返回结果是否达到预期。check可以帮助发现一些不明显的bug，同时保证返回结果的正确性，以备后续使用。  
一般希望展示check部分的输出结果，所以不会注释掉相关代码。

+ example  
一个功能实现完了，确信没问题，以示例展示如何使用或者某些输入值的输出。

## 在其他脚本中import

notebook可以导出为py，然后被其他py脚本import，以调用写在notebook中的函数。  
但notebook中会有大量实验性的代码，你不希望这些代码在notebook作为module导入时被执行。  
那么可不可以选择性的导出某些cell呢？

* ipython有一系列magic command，跟刚才的需求相关的是%%writefile，但功能有限，而且不能同时执行cell中的代码。
* 但是我们可以自己定义magic command，实现上述功能。使用`self.shell.run_cell(cell)`执行cell中代码，然后再写入文件。
* 有时候，可能希望在同一个文档中的不同地方写入代码，而不是一味的追加在末尾。下面的这个magic command，已经能实现如下功能：在某个字符串之前加入cell中的代码，并且可以指定统一的缩进空格数。
* 为何不实现在某个字符串之后加入代码的功能呢？未来加入～


```python
#%%writefile "sync_to_file_magic_command.py"
# This code can be put in any Python module, it does not require IPython
# itself to be running already.  It only creates the magics subclass but
# doesn't instantiate it yet.
from IPython.core.magic import (Magics, magics_class, line_magic,
                                cell_magic, line_cell_magic)

# The class MUST call this class decorator at creation time
@magics_class
class MyMagics(Magics):

    @cell_magic
    def sync_to_file(self, line, cell):
        line = line.strip()
        if line == '':
            raise ValueError('No File to Sync!')
        # run the code
        self.shell.run_cell(cell)
        # write to file
        import codecs
        import re
        import os.path
        #print repr(line)
        # parse args
        file_name_l = None
        place_after = None
        place_before = None
        indent = 0
        overwrite = False
        # match whether_to_overwrite
        match_w_re = re.compile(ur'^(.*?)-w$')
        match_result = match_w_re.match(line)
        if match_result:
            overwrite = True
            line = match_w_re.sub(r'\1', line).strip()
        # match the after arg
        match_place_after_re = re.compile(ur'^(.*?)(-after )(.*?)(-.*$|$)')
        match_result = match_place_after_re.match(line)
        if match_result:
            place_after = match_result.group(3).strip()
            if place_after == '':
                place_after = None
            line = match_place_after_re.sub(r'\1\4', line)
        # match the before arg
        match_place_before_re = re.compile(ur'^(.*?)(-before )(.*?)(-.*$|$)')
        match_result = match_place_before_re.match(line)
        if match_result:
            place_before = match_result.group(3).strip()
            if place_before == '':
                place_before = None
            line = match_place_before_re.sub(r'\1\4', line).strip()
        # match the indent arg
        match_indent_re = re.compile(ur'^(.*?)(-indent )(\d+)$')
        match_result = match_indent_re.match(line)
        if match_result:
            indent = int(match_result.group(3))
            line = match_indent_re.sub(r'\1', line).strip()
        # match the file_name arg
        match_file_names_re = re.compile(ur'(?<=-f ).*?(?=-f|$)')
        file_name_l = match_file_names_re.findall(line)
        file_name_l = [file_name.strip() for file_name in file_name_l]
        # add indentation
        cell_line_l = cell.split('\n')
        cell_line_l = [' '*indent + cell_line for cell_line in cell_line_l]
        cell = '\n'.join(cell_line_l)
        # begin to sync file
        overwrite = True if not os.path.isfile(file_name_l[0]) else overwrite
        if overwrite:
            for file_name in file_name_l:
                with codecs.open(file_name, 'w', encoding='utf-8') as f:
                    f.write(cell)            
        elif place_before is None:
            for file_name in file_name_l:
                with codecs.open(file_name, 'a', encoding='utf-8') as f:
                    f.write('\n')
                    f.write(cell)
        else:
            for file_name in file_name_l:
                with codecs.open(file_name, 'r', encoding='utf-8') as f:
                    file_str = f.read()
                match_the_before_str_re = re.compile(place_before)
                match_result = match_the_before_str_re.search(file_str)
                if match_result:
                    before_index = match_result.start()
                    file_str = file_str[:before_index] + '\n' + cell + '\n'*2 + file_str[before_index:]
                else:
                    pass
                with codecs.open(file_name, 'w', encoding='utf-8') as f:
                    f.write(file_str)            

# In order to actually use these magics, you must register them with a
# running IPython.  This code must be placed in a file that is loaded once
# IPython is up and running:
ip = get_ipython()
# You can register the class itself without instantiating it.  IPython will
# call the default constructor on it.
ip.register_magics(MyMagics)
```

## sync_to_file参数

之前写了magic command `%%sync_to_file`，下面指定一些该命令的常用参数，通过`%%sync_to_file $var`来调用。


```python
configMyHelpers = '-f my_helpers.py'
```


```python
before_main_arg = ' -before def main\(file_name=None\):'
```


```python
new3000_convert_script_name = 'new3000_convert.py'
configNew3000 = '-f ' + new3000_convert_script_name
configNew3000BeforeMain = configNew3000 + before_main_arg
configNew3000AfterMain = configNew3000 + ' -indent 4'
```


```python
zhuji_convert_script_name = 'zhuji_convert.py'
configZhuji = '-f ' + zhuji_convert_script_name
configZhujiBeforeMain = configZhuji + before_main_arg
configZhujiAfterMain = configZhuji + ' -indent 4'
```


```python
duanyu_convert_script_name = 'duanyu_convert.py'
configDy = '-f ' + duanyu_convert_script_name
configDyBeforeMain = configDy + before_main_arg
configDyAfterMain = configDy + ' -indent 4'
```


```python
%%sync_to_file $configNew3000 $configMyHelpers $configZhuji $configDy -w

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
```


```python
with codecs.open(new3000_convert_script_name, 'a', encoding='utf-8') as f:
    f.write('\nfrom my_helpers import *')
```


```python
with codecs.open(zhuji_convert_script_name, 'a', encoding='utf-8') as f:
    f.write('\nfrom my_helpers import *')
```


```python
with codecs.open(duanyu_convert_script_name, 'a', encoding='utf-8') as f:
    f.write('\nfrom my_helpers import *')
```

## txt源文件所在相对路径

每个自动生成的转换脚本都有一个主函数，还有一堆写在主函数上面（外面）的辅助函数。主函数的作用是，先判断指定文件是否存在，如果存在，在顺序执行后续语句。后文中，一些代码需要出现在主函数之前，一些需要出现在之后。下面的三个cell分别向三个转换脚本中写入各自的主函数开头，同时为后续代码写入提供主函数的位置依据。


```python
%%sync_to_file $configNew3000
file_new_3000 = "base_data\GREHe Xin Ci Hui Kao Fa Jing Xi  (Xin Dong Fang Da Yu Ying Yu Xue Xi Cong Shu ) - Chen Qi.txt"
def main(file_name=None):
    if file_name is None:
        file_name = file_new_3000
    # for module call
    if not os.path.isfile(file_name):
        return
```


```python
%%sync_to_file $configZhuji
file_zhuji = "base_data\GREHe Xin Ci Hui Zhu Ji Yu Jing - Cao Tian Cheng.txt"
def main(file_name=None):
    if file_name is None:
        file_name = file_zhuji
    # for module call
    if not os.path.isfile(file_name):
        return
```


```python
%%sync_to_file $configDy
file_duanyu = "base_data\GREGao Fen Bi Bei Duan Yu Da Pe - Yan Yu Zhen ,Gao Yu ,Chen Qi.txt"
def main(file_name=None):
    if file_name is None:
        file_name = file_duanyu
    # for module call
    if not os.path.isfile(file_name):
        return
```

# 辅助函数

## 全角转半角


```python
%%sync_to_file $configMyHelpers
def strF2H(ustring):
    '''
    convert full width character to half width
    input: a unicode object
    return: a unicode object
    '''
    h_ustring = u""
    assert isinstance(ustring, unicode)
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 12288:
            #  white space
            inside_code = 32
        elif 65281 <= inside_code <= 65374:
            #  other characters
            inside_code -= 65248

        h_ustring += unichr(inside_code)
    return h_ustring
```


```python
# exmple
test_str = '全角字符：＋－！Ｆｕｌｌ　Ｗｉｄｔｈ　ｃｈａｒ！'.decode('utf-8')
print test_str, type(test_str)
test_str = strF2H(test_str)
print test_str, type(test_str)
del test_str
```

    全角字符：＋－！Ｆｕｌｌ　Ｗｉｄｔｈ　ｃｈａｒ！ <type 'unicode'>
    全角字符:+-!Full Width char! <type 'unicode'>
    

## print_if_main_call

通过将print封装在print_if_main_call中，只在被notebook自身调用时才print输入的参数


```python
def print_if_main_call(*_str):
    if __name__ == "__main__":
        for a_str in _str:
            print a_str,
```

## recursive print

无论是`pprint`还是`print`，都不能将嵌套结构中的unicode解码后的字符打印出来，所以有了下面这个`iter_print`函数


```python
%%sync_to_file $configMyHelpers
# pretty print the embedded unicode of list or dict
def iter_print(obj_iter, indent=0, increment=2, max_top_level_print=None, 
               top_level=True, top_level_extra_line_feed=False, print_list_index=True):
    if not hasattr(obj_iter, '__iter__'):
        if isinstance(obj_iter, basestring):
            if obj_iter == u'':
                pass
            elif '\n' in obj_iter:
                for line in obj_iter.split('\n'):
                    if line:
                        print ' '*indent, line
            else:
                print ' '*indent, obj_iter
        else:
            print ' '*indent, obj_iter
        return
    print_count = 0
    if isinstance(obj_iter, dict):
        for key, iter_sub_obj in obj_iter.iteritems():
            print ' '*indent, key
            iter_print(iter_sub_obj, indent+increment, increment, None, False, False, print_list_index)
            if top_level:
                print_count += 1
                if max_top_level_print:
                    if print_count >= max_top_level_print:
                        break
                if top_level_extra_line_feed:
                    print '\n'
    else:
        for list_index, sub_obj_iter in enumerate(obj_iter):
            if print_list_index:
                print ' '*indent, list_index
            iter_print(sub_obj_iter, indent+increment, increment, None, False, False, print_list_index)
            if top_level:
                print_count += 1
                if max_top_level_print:
                    if print_count >= max_top_level_print:
                        break
                if top_level_extra_line_feed:
                    print '\n'
```

## 分隔字符串

在切割字符串的过程中，经常遇到这样一个需求：给定一个文本模式，在一个字符串中会遇到该模式若干次，依次提取每两次相遇之间的内容，以及最后一次相遇直到字符串结尾的内容。  
比如，依次提取"List 1"到"List 2"之间、"List 2"到"List 3"之间、"List 3"到字符串结尾的内容。  
这一需求被抽象后实现为如下函数。


```python
%%sync_to_file $configMyHelpers
def extract_content_between(obj_str, match_re, return_str_before_first_match=False):
    '''
    extract content between the start of two equal pattern found in a str,
    also extract the content after the last match
    input: obj_str, the string to extract content from, must be a unicode object
           match_re, the pattern to be matched
    return: a list of str
    return_str_before_first_match: whether to return the str before the first match of the given patter
    '''
    assert isinstance(obj_str, unicode)
    retype = type(re.compile(r'a str'))
    assert isinstance(match_re, retype)
    
    match_results_iter = match_re.finditer(obj_str)
    returned_str_l = []
    start_index = None
    end_index = None
    first_start_index = None
    for match_result in match_results_iter:
        if first_start_index is None:
            first_start_index = match_result.start()
        if not (start_index is None):
            end_index = match_result.start()
            returned_str_l.append(obj_str[start_index:end_index])
        start_index = match_result.start()
    returned_str_l.append(obj_str[start_index:])
    if return_str_before_first_match:
        returned_str_l = [obj_str[:first_start_index]] + returned_str_l
    return returned_str_l
```


```python
# exmple
test_str = u'a/b/c'
test_re = re.compile(u'/')
print extract_content_between(test_str, test_re)
del test_str, test_re
```

    [u'/b', u'/c']
    

## 遍历嵌套变量

写代码时，经常需要遍历一些结构非常复杂的嵌套变量。比如，对于一个`_d_d`变量，遍历顶层字典的每一个键值对，但对于第二层的字典，只取某一个键值对。下面的代码遍历一个结构为`_d_l_d_d`的变量。


```python
%%sync_to_file $configMyHelpers
def iter_value_of_key_through_d_l_d_d(obj_d_l_d_d, key_2nd_level, key_4th_level, 
                                      expected_draw=1.0, yield_top_key=False, yield_list_index=False):
    '''
    a function that return a generator
    it will iter through all the values of the first level dict with every value being themself a dict
    for every such value dict,
        a key specified by key_2nd_level is used to access a list
        for every elment of the list
            a key specified by key_4th_level is used to access the corresponding value
    so in total it is a two level nested loop
    
    key_2nd_level: what it points to must be a list 
    
    expected_draw: roughly control the proportion of the innermost values to be sampled
                   can be an integar, which will be converted to the corresponding probability
    
    yield_top_key: whether to include the top key
    yield_list_index: whether to include the list index
    note that (yield_top_key=False, yield_list_index=True) is a useless combination, so raise an ValueError
    '''
    if isinstance(expected_draw, int):
        expected_draw = float(expected_draw)/len(obj_d_l_d_d)
    assert isinstance(expected_draw, float)
    for top_key, value_d_l_d in obj_d_l_d_d.iteritems():
        assert isinstance(value_d_l_d[key_2nd_level], list)
        for _list_index, value_d in enumerate(value_d_l_d[key_2nd_level]):
            if random() <= expected_draw:
                if (not yield_top_key) and (not yield_list_index):
                    yield value_d[key_4th_level]
                elif yield_top_key and (not yield_list_index):
                    yield top_key, value_d[key_4th_level]
                elif yield_top_key and yield_list_index:
                    yield top_key, _list_index, value_d[key_4th_level]
                else:
                    raise ValueError('Invalid Combination of yield_top_key and yield_list_index')
```

对上述代码进一步抽象得到


```python
%%sync_to_file $configMyHelpers
def iter_through_general(obj_iter, path, yield_flags=True, final_yield_object=None):
    '''
    iter through an object following the given path
    yield_flags: control whether to yield the flags indicating the path at the global level
    final_yield_object: internal parameter, don't modify
    obj_iter: an iterable variable
    path: a sequence, each element has the following structure
        (how_to_iter, what_to_iter, yield_flag)
        how_to_iter: a str, accept the following values
            'all' or 'all_values': iter through key-value pair for dict, and all elements for other type
                if yield_flag is True, attach key or index to the final yield object
            'all_keys', only iter through the keys of a dict
                obj_iter must be a dict
            'key', iter through the value of a given key
                what_to_iter must be a str representing a key in obj_iter
                if yield_flag is True, attach key to the final yield object
                ignored when obj_iter is not dict
            'keys', iter through the values of a given set of keys
                what_to_iter must be a tuple with elements reprenting keys in obj_iter
                if yield_flag is True, attach key to the final yield object
                ignored when obj_iter is not dict
            'index', iter through a given element
                what_to_iter must be an int within bound
                if yield_flag is True, attach index to the final yield object
                ignored when obj_iter is dict
            'indexes', iter through the elements with given indexes
                what_to_iter must be an list of int within bound
                if yield_flag is True, attach key to the final yield object
                ignored when obj_iter is dict
        what_to_iter: content decided by how_to_iter
            ignored for the following values of how_to_iter
                all, all_values, all_keys
        yield_flag: True or False
            True: depending on how_to_iter, attch different flags to the final result
            False: no flag wil be yield
            ignored for the following values of how_to_iter
                all_keys
    '''
    is_dict = isinstance(obj_iter, dict)
    if final_yield_object is None:
        final_yield_object = []
    if len(path) == 0:
        if yield_flags:
            final_yield_object.append(obj_iter)
            yield final_yield_object
        else:
            yield obj_iter
    else:
        how_to_iter, what_to_iter, yield_flag = path.pop(0)
        assert isinstance(how_to_iter, basestring)
        if how_to_iter in [u'all', u'all_values', u'keys', u'indexes']:
            if how_to_iter in [u'keys', u'indexes']:
                assert hasattr(what_to_iter, '__iter__')
                for item in what_to_iter:
                    if is_dict:
                        assert how_to_iter == u'keys'
                        assert isinstance(item, basestring)
                        assert item in obj_iter
                    else:
                        assert how_to_iter == u'indexes'
                        assert isinstance(item, int)
                        assert item < len(obj_iter)
                temp_iterator = ((item, obj_iter[item]) for item in what_to_iter)
            else:
                temp_iterator = obj_iter.iteritems() if is_dict else enumerate(obj_iter)
            for flag, sub_obj_iter in temp_iterator:
                final_yield_object_copy = deepcopy(final_yield_object)
                if yield_flag:
                    final_yield_object_copy.append(flag)
                for value in iter_through_general(sub_obj_iter, deepcopy(path), yield_flags, final_yield_object_copy):
                    yield value
        elif how_to_iter == u'all_keys':
            assert is_dict
            for key in obj_iter.iterkeys():
                if yield_flags:
                    final_yield_object.append(key)
                    yield final_yield_object
                else:
                    yield key
        elif how_to_iter in [u'key', u'index']:
            if is_dict:
                assert how_to_iter == u'key'
                assert isinstance(what_to_iter, basestring)
                assert what_to_iter in obj_iter
            else:
                assert how_to_iter == u'index'
                assert isinstance(what_to_iter, int)
                assert what_to_iter < len(obj_iter)     
            sub_obj_iter = obj_iter[what_to_iter]
            if yield_flag:
                final_yield_object.append(what_to_iter)
            for value in iter_through_general(sub_obj_iter, deepcopy(path), yield_flags, final_yield_object):
                yield value
        else:
            raise ValueError('Invalid path')
```


```python
# example
def unit_test():
    test_dic = {'a':['a-a',2,3], 'b':['b-a',3,4], 'c':['c-a',2,3]}
    print 'PATH ONE'
    for value in iter_through_general(test_dic, [('all','',True),('indexes',[0,1],False)]):
        print value,
    print '\nPATH TWO'
    for value in iter_through_general(test_dic, [('keys', ['a', 'b'], False)]):
        print value,
unit_test()
del unit_test
```

    PATH ONE
    ['a', 'a-a'] ['a', 2] ['c', 'c-a'] ['c', 2] ['b', 'b-a'] ['b', 3] 
    PATH TWO
    [['a-a', 2, 3]] [['b-a', 3, 4]]
    

## Reservoir_sampling

批处理完后，需要随机的查看一些结果，检查批处理中是否有bug。下面这个函数按照reservoir sampling的方法，从一个未知长度的遍历对象中随机选取k个元素。

参见 https://en.wikipedia.org/wiki/Reservoir_sampling


```python
%%sync_to_file $configMyHelpers
def reservoir_sample_k(obj_iter, k):
    assert isinstance(k, int)
    assert hasattr(obj_iter, '__iter__')
    # fit into k items
    sampled_l = []
    for _ in range(k):
        sampled_l.append(obj_iter.next())
    i = k
    for item in obj_iter:
        i += 1
        j = randint(1, i)
        if j <= k:
            sampled_l[j-1] = item
    return sampled_l
```

同前面的`iter_through_general`函数结合产生


```python
%%sync_to_file $configMyHelpers
def iter_through_and_sample_k(obj_iter, k, path):
    obj_iter_follow_path = iter_through_general(obj_iter, path)
    return reservoir_sample_k(obj_iter_follow_path, k)
```

## 其他


```python
%%sync_to_file $configMyHelpers
strip_white_space = lambda _str: _str.replace(' ', '')
new_line_join = lambda str_l: '\n'.join(str_l)
def codecs_open_r_utf8(file_path):
    with codecs.open(file_path, 'r', 'utf-8') as f:
        returned_str = f.read()
    return returned_str
# merge blank lines
def collapse_blank_line(base_str):
    match_double_line_feed_re = re.compile(r'\n\n')
    while match_double_line_feed_re.search(base_str):
        base_str = match_double_line_feed_re.sub(r'\n', base_str)
    return base_str
```

# 处理《GRE核心词汇考法精析》

读入"GREHe Xin Ci Hui Kao Fa Jing Xi - Chen Qi.txt"，生成`new3000_base_d`


```python
%%sync_to_file $configNew3000AfterMain
new3000_base_str = codecs_open_r_utf8(file_new_3000)
```


```python
print 'Note the type of new3000_base_str is', type(new3000_base_str)
```

    Note the type of new3000_base_str is <type 'unicode'>
    

## 按List提取

每个List以 "`# List`"+一个空格+一个数字 开始。两个开始位置之间的内容即为一个List。某些List第一行的结尾还会出现"`\*`"


```python
%%sync_to_file $configNew3000BeforeMain
match_new3000_list_start_re = re.compile(ur'^# List \d+', re.M)
```


```python
%%sync_to_file $configNew3000AfterMain
new3000_base_list_data_l = extract_content_between(new3000_base_str, match_new3000_list_start_re)
```


```python
# check
print len(new3000_base_list_data_l), 'lists extracted out'
print '\nThe start of one list:\n', new3000_base_list_data_l[1][0:200]
```

    31 lists extracted out
    
    The start of one list:
    # List 2
    
    “壮丽的诗篇要以信念作为舞台，融着几多苦乐的拼搏历程是我想要延续的抚慰和寄托。”
    
    （金宇航，Verbal 720，Quantitative 800，  
    录取院校：哈佛大学工程与应用科学）
    
    ## Unit 1
    
    ■ AMORPHOUS　■ ANALGESIC　■ ANARCHIST　■ ANATHEMA　■ ANCILLARY
    
    ■ ANECDOTE　■ ANEMIC　■ 
    

最后一个List直接匹配到字符串末尾，通过观察txt文档，发现List31匹配到大量无关内容，需单独处理。


```python
%%sync_to_file $configNew3000BeforeMain
def strip_last_list(list_data):
    strip_start_re = re.compile(ur'# Word List 1　与说有关的词根构成的单词(.|\n)*$')
    return strip_start_re.sub('', list_data)
```


```python
%%sync_to_file $configNew3000AfterMain
new3000_base_list_data_l[30] = strip_last_list(new3000_base_list_data_l[30])
```

## 按Unit提取

每个Unit以 "`## Unit`"+空格+一个数字+"`\n`" 开始，两个开始位置之间的内容即为一个Unit


```python
%%sync_to_file $configNew3000BeforeMain
match_unit_start_re = re.compile(ur'^## Unit \d+', re.M)
```


```python
%%sync_to_file $configNew3000AfterMain
new3000_base_unit_data_l_l = map(functools.partial(extract_content_between, 
                                                   match_re=match_unit_start_re), 
                                 new3000_base_list_data_l)
```


```python
# check
print 'the number of unit in a list\n', map(len, new3000_base_unit_data_l_l)
print '\nthe start part of one unit\n', new3000_base_unit_data_l_l[9][9][0:200]
```

    the number of unit in a list
    [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 8]
    
    the start part of one unit
    ## Unit 10
    
    ■ FROTHY　■ FROWSY　■ FRUGAL　■ FRUSTRATE　■ FULL-BODIED
    
    ■ FULMINATE　■ FUMBLE　■ FUROR　■ FURTIVE　■ FURY
    
    **frothy**［'frɔ:θi］
    
    【考法1】*adj.* 用轻薄材料制作的：made of **light** thin material
    
    例　a frothy l
    

## 按单词提取

每个单词以  
"`**`"+英文单词+"`**`"+一个空格+全角字符"`［`"+若干音标字符+全角字符"`］`"  
开始，两个开始位置之间的内容即为一个单词  

英文单词部分的规律如下：
+ 基本都是由a至z的小写字母组成
+ 某些GRE单词是从法语演变来的。比如cliché这种。按理说应该匹配所有的西欧字符，但由于GRE单词书中貌似只出现过éï，所以其他的就不用匹配。
+ 有些单词涉及到连字符"`-`"

音标部分，匹配"`［`"与"`］`"之间的所有字符即可。有的多音单词，比如addict（List1Unit6），单词后并没有音标，但每个释义后面有音标


```python
%%sync_to_file $configNew3000BeforeMain
match_word_block_start = re.compile(ur'^\*\*(?P<word>[a-z\-éï]+)\*\*(?P<phon>［.+］)?', re.U|re.M)
# phon represent phonetic symbol
```


```python
# test
def unit_test():
    for result in match_word_block_start.finditer(new3000_base_unit_data_l_l[0][5]):
        print result.group('word'),
        print result.group('phon')
# unit_test()
del unit_test
```


```python
%%sync_to_file $configNew3000BeforeMain
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
```


```python
# example
test_d = get_word_of_one_unit(new3000_base_unit_data_l_l[0][5], 1, 6)
iter_print(test_d, max_top_level_print=2)
del test_d
```

     ad-lib
       word_block_str
         【考法】*adj.* 即兴的：made or done **without previous thought or preparation**
         例　not bad for an ad-lib comedy routine 对即兴喜剧表演来说已经不错了
         近　extemporary, impromptu, improvisational, offhanded
         反　considered, planned, premeditated, rehearsed 预先计划的
       pos
         0
           1
         1
           6
       phon
         [ˌæd'lɪb]
     adhere
       word_block_str
         【考法1】*v.* 依附，粘着：to cause to **stick** fast
         例　adhere to the surface 附着在表面
         近　cleave, cling, hew
         反　detach 分离
         【考法2】*v.* 服从，遵守：to act **according to the commands** of
         例　adhere to the rules 遵守规定
         近　cling to, hew to, stand by, stick to, comply with
         反　defy, disobey, rebel against 不服从，反抗
         【考法3】*v.* 坚定地支持：to give **steadfast support** to
         例　Our coach adheres to the belief that we can win this game if we just have a positive attitude. 我们的教练坚定地相信，只要我们有积极的态度，就能拿下比赛。
         近　keep to, stand by, stick to or with
         反　defect from 叛变
         派　adherent *n.* 追随者：a follower of a leader, party, or profession
         反　forerunner 先行者
       pos
         0
           1
         1
           6
       phon
         [əd'hɪr]
    


```python
%%sync_to_file $configNew3000BeforeMain
def get_new3000_base_d(base_unit_data_l_l):
    _new3000_base_d = {}
    for list_index, unit_data_l in enumerate(base_unit_data_l_l):
        for unit_index, unit_data in enumerate(unit_data_l):
            _new3000_base_d.update(get_word_of_one_unit(unit_data, list_index+1, unit_index+1))
    return _new3000_base_d
```


```python
%%sync_to_file $configNew3000AfterMain
new3000_base_d = get_new3000_base_d(new3000_base_unit_data_l_l)
```


```python
# check
print 'Total words: ', len(new3000_base_d)
```

    Total words:  3063
    

## 检视word_block内部结构

### 示例


```python
print '单义情形：'
iter_print(new3000_base_d['dodge']['word_block_str'])
print '\n多义情形：'
iter_print(new3000_base_d['addict']['word_block_str'])
```

    单义情形：
     【考法】*v.* 躲避：to **avoid**（a blow, for example）by moving or shifting quickly aside
     例　dodge a storm of bullets 躲避枪林弹雨‖He dodged the first punch but was hit by the second. 他躲过了第一次打击，但是没有躲过第二次。
     近　avoid, escape, shirk, malinger, goldbrick, evade, parry, sidestep, circumvent, fence, hedge, avert, elude, shun, skirt, bilk, eschew, weasel
    
    多义情形：
     【考法1】［ə'dɪkt］ *v.* 沉溺，上瘾：to devote or **surrender**（oneself）to something habitually or **obsessively**
     例　be addicted to drug/alcohol 沉溺于毒品、酒
     【考法2】［'ædɪkt］ *n.* 对某事上瘾的人：a person with a strong and **habitual liking** for something
     例　science-fiction addicts who eagerly await each new installment in the series 科幻小说爱好者，等待着系列的每一次更新
     近　devotee, enthusiast, fanatic, maniac
     反　nonfan 非粉丝
    

### 统计每行第一个字符


```python
def count_line_start_char():
    from collections import Counter
    temp_start_types = Counter()
    for value in new3000_base_d.itervalues():
        word_block_str = value['word_block_str']
        word_block_lines = word_block_str.split('\n')
        for line in word_block_lines:
            if line == '' or line == '\n':
                continue
            temp_start_types[line[0]] += 1
            if line[0] == ' ' or line[0] == '*':
                #print line
                continue
            if line[0] == 'a' or line[0] == 'H':
                #print line
                continue
    for key, value in temp_start_types.iteritems():
        print key, value, ',',
count_line_start_char()
del count_line_start_char
```

    如 3 , （ 1 , 例 4238 , 同 1 , 我 1 , 【 4371 , — 17 , 生 1 ,   1 , 困 1 , * 17 , 人 2 , 派 781 , a 1 , H 1 , 反 3412 , 每 2 , 近 4135 , 教 1 , 凡 1 , 勤 1 , 只 1 , 杰 1 ,
    

+ 正常情形下，一行应该以"【"、"例"、"近"、"反"、"派"开始。异常字符往往代表需要特殊处理的地方。
+ 通过检视原文档，发现：
  - 如3，`（`1，，我1，`—`17，生1，困1，人2，每2，教1，凡1，勤1，只1，杰1：出现在List结尾处的名人名言中，比如某些名人名言的中文翻译以“如”开头。对于这些字符，忽略即可。
  - 同1：单词anarchist独有，后面跟了两个同义词。而且通过这个单词，可以发现一个单词的派生词也有自己完整的结构。
  - 一个空格字符1：compliment这个单词，单词起始行为“`**compliment** *n.*［'kɑ:mplɪmənt］ *v.*［'kɑ:mplɪment］`”，特例。根据前面的正则规则替换，将“`**compliment**`”拿走后，省下了一个以空白字符起始的行。
  - `*`18：大部分存在于名人名言中。唯一的例外是由compliment造成的，前面提到过。
  - a1：单词antediluvian，考法1，两个例句分占两行
  - H1：单词anecdote，两个例句分占两行
+ 【勘误】处理方法：
  - anarchist，将同改为近
  - compliment，单词块第一行，将音标提取出来，组成一个list，第一个元素是名词音标，第二个元素是动词音标。后面处理考法时，两个音标连成一个字符串给考法1，第二个音标给考法2
  - antediluvian、anecdote，将第二次遇到的两个连续的'\n'替换为"‖"


```python
%%sync_to_file $configNew3000BeforeMain
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
```


```python
%%sync_to_file $configNew3000AfterMain
# revise
subset_to_revise_d = {word:deepcopy(new3000_base_d[word]) for word in ['anarchist', 'compliment', 'antediluvian', 'anecdote']}
subset_to_revise_d = revise_word_base_data(subset_to_revise_d)
```


```python
# check
print subset_to_revise_d['anarchist']['word_block_str'][0:150], '\n'
print subset_to_revise_d['compliment']['word_block_str'][0:50]
print subset_to_revise_d['compliment']['phon'], '\n'
print subset_to_revise_d['antediluvian']['word_block_str'][0:210], '\n'
print subset_to_revise_d['anecdote']['word_block_str']
```

    
    
    【考法】*n.* 反抗权威的人：a person who **rebels against any authority**, established order, or ruling power
    
    近　rebel, insurgent
    
    派　anarchy *n.* 混乱：a state of  
    
    
    【考法1】*n./vt.* 称赞，恭维：an expression of **praise**, 
    [u"['k\u0251:mpl\u026am\u0259nt]", u"['k\u0251:mpl\u026ament]"] 
    
    
    
    【考法1】*adj.* 非常古老的；过时的：**extremely old** and **antiquated**
    
    例　He has antediluvian notions about the role of women in the workplace. 他对职场女性抱有老掉牙的看法。‖an antediluvian automobile 古董级的汽车
    
    近　aged, age-old, prehisto 
    
    
    
    【考法】*n.* 短小有趣的故事：a usually **short narrative** of an **interesting, amusing**, or biographical incident
    
    例　He told us all sorts of humorous anecdotes about his childhood. 他告诉了我们所有关于他童年的奇闻趣事。‖He is a master raconteur with endless anecdotes. 他是讲故事的超级高手，总有讲不完的奇闻趣事。
    
    
    


```python
%%sync_to_file $configNew3000AfterMain
new3000_base_d.update(subset_to_revise_d)
del subset_to_revise_d, new3000_base_list_data_l, new3000_base_unit_data_l_l, new3000_base_str
```

### 单词骨架示意

word|单词

* usages: list #单词的所有考法
 * usages[i]: dict {exp, examples, syn, ant, der, part of speech, ph_symbl} #单词第i个考法，包括{解释，例句，同义词，反义词，派生词，词性，用法专属的音标}
   + exp: dict {cn: str, en: str} #explanation expressed as cn and en | 单词用法释义，包括中英文
   + examples: list
      * examples[j]: dict {cn: str, en: str}
   + syns: list
      * syns[j]: str
   + ants: list
      * ants[j]: dict {cn: str, en: list}
   + der: str #需要单独处理
   + pspeech: str #part of speech | 词性
   + ph_symbl : str #phonetic symbols
* pos: (int, int) #(List, Unit) | existed
* ph_symbl: str #phonetic symbols | 音标，existed


## 初步构造

+ 需要将每个单词的'word_block_str'字段转换为'usages'
+ 处理考法时，有些单词的音标在考法后面；另外，单词compliment需要特殊处理
+ 将派生词当作一个独立的新词对待

### 存放各类判断函数的字典

* 比如'examples'字段存放着判断这行是不是例句的函数
* 注意闭包陷阱


```python
%%sync_to_file $configNew3000BeforeMain
character_start = {'examples': '例', 
                   'syns': '近', 
                   'ants': '反', 
                   'der': '派'}
```


```python
%%sync_to_file $configNew3000BeforeMain
is_str_start_with_character_fun_d = {}
for key, value in character_start.iteritems():
    def gen_match_fun_closure(_value):
        return lambda s: s[0] == _value.decode('utf-8')
    is_str_start_with_character_fun_d[key] = gen_match_fun_closure(value)
```


```python
# an incorrect implementation
incorrect_implementation = {key: lambda s: s[0] == value.decode('utf-8') for key, value in character_start.iteritems()}
# pitfall: value is a global variable and ischanging dynamically, 
# so finally all lambda will refer to the last value, in this case it is syns!
```


```python
# example
syn_str = u'近 wild, bizarre'
print 'Should be True, in fact is', incorrect_implementation['syns'](syn_str)
print 'Should be True, in fact is', is_str_start_with_character_fun_d['syns'](syn_str)
# anoter example
example_str = u'例 abstract the 135-page'
print 'Should be True, in fact is', incorrect_implementation['examples'](example_str)
print 'Should be True, in fact is', is_str_start_with_character_fun_d['examples'](example_str)
del syn_str, example_str
```

    Should be True, in fact is True
    Should be True, in fact is True
    Should be True, in fact is False
    Should be True, in fact is True
    

### 将`word_block_str`转变为`usages`结构

* 初步转换，即把行对应到字典的字段
* 将`word_block_str`按照考法拆分为释义列表
* 对每个释义，按`\n`拆分为若干行
* 对每行使用函数`is_str_start_with_character_d`判断该行属于哪个字段
* 某些单词的派生词很复杂，从以“派”开头的一行开始，之后的行，都属于该派生词，而非源单词。如compendium、anarchist
* 对于复杂派生词，将相关字段（出现在派生词所在行之后）组合成一个字符串，以便利用已有函数处理
* 复杂派生词独立为新词条处理
* 通过观察所有的复杂派生词，发现如下特点：
  - 有词性，没有音标
  - 派生词的拼写：以派开头的那行，匹配第一个空格后的连续几个英文字符即可，涉及到特殊字符"/"
  - 派生词的第一行是解释，中英文以“:”间隔，只有中文时没有间隔符
  - 某些单词一个释义下有多个并列的复杂派生词，比如digress。对于这种情况，用函数`extract_content_between`先拆分再处理
* 【勘误】处理过程中发现
  - 单词plumb的释义3中，例标成了派
  - 单词daunt的两个派生词以逗号加一个空格相连


```python
%%sync_to_file $configNew3000BeforeMain
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
```


```python
%%sync_to_file $configNew3000AfterMain
revise_entry_name(new3000_base_d)
```


```python
%%sync_to_file $configNew3000BeforeMain
match_usage_start_re = re.compile(ur'^【考(?:法|点)\d?】(.*)$', re.M|re.U)
match_der = re.compile(ur'^')
```


```python
%%sync_to_file $configNew3000BeforeMain
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
```


```python
# test
def unit_test():
    _, result = wb_str_2_usages_d_l(new3000_base_d['anarchist']['word_block_str'])
    iter_print(result, 0, 4)
#unit_test()
del unit_test
```

【勘误】  
已经考虑过复杂派生词的前提下，应该一个field占据一行。通过检查是否有多行field，发现：  
* random，第二个例应该为近，返回到处理word_block_str之前更正
* sordid，考法2，第一个近应为例，返回到处理word_block_str之前更正


```python
%%sync_to_file $configNew3000BeforeMain
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
```


```python
%%sync_to_file $configNew3000AfterMain
complex_ders_d, new3000_base_d = gen_usages_for_all_words(new3000_base_d)
new3000_base_d.update(complex_ders_d)
del complex_ders_d
```


```python
# test
#iter_print(new3000_base_d['compliment'])
# example
print 'An example of the structure of a word dictionary'
pprint(new3000_base_d['addict'])
iter_print(new3000_base_d['addict'])
```

    An example of the structure of a word dictionary
    {'phon': u'',
     'pos': (1, 6),
     'usages': [{'ants': '',
                 'der': '',
                 'examples': u'\u4f8b\u3000be addicted to drug/alcohol \u6c89\u6eba\u4e8e\u6bd2\u54c1\u3001\u9152',
                 'exp': u"\uff3b\u0259'd\u026akt\uff3d *v.* \u6c89\u6eba\uff0c\u4e0a\u763e\uff1ato devote or **surrender**\uff08oneself\uff09to something habitually or **obsessively**",
                 'syns': ''},
                {'ants': u'\u53cd\u3000nonfan \u975e\u7c89\u4e1d',
                 'der': '',
                 'examples': u'\u4f8b\u3000science-fiction addicts who eagerly await each new installment in the series \u79d1\u5e7b\u5c0f\u8bf4\u7231\u597d\u8005\uff0c\u7b49\u5f85\u7740\u7cfb\u5217\u7684\u6bcf\u4e00\u6b21\u66f4\u65b0',
                 'exp': u"\uff3b'\xe6d\u026akt\uff3d *n.* \u5bf9\u67d0\u4e8b\u4e0a\u763e\u7684\u4eba\uff1aa person with a strong and **habitual liking** for something",
                 'syns': u'\u8fd1\u3000devotee, enthusiast, fanatic, maniac'}],
     'word_block_str': u"\n\n\u3010\u8003\u6cd51\u3011\uff3b\u0259'd\u026akt\uff3d *v.* \u6c89\u6eba\uff0c\u4e0a\u763e\uff1ato devote or **surrender**\uff08oneself\uff09to something habitually or **obsessively**\n\n\u4f8b\u3000be addicted to drug/alcohol \u6c89\u6eba\u4e8e\u6bd2\u54c1\u3001\u9152\n\n\u3010\u8003\u6cd52\u3011\uff3b'\xe6d\u026akt\uff3d *n.* \u5bf9\u67d0\u4e8b\u4e0a\u763e\u7684\u4eba\uff1aa person with a strong and **habitual liking** for something\n\n\u4f8b\u3000science-fiction addicts who eagerly await each new installment in the series \u79d1\u5e7b\u5c0f\u8bf4\u7231\u597d\u8005\uff0c\u7b49\u5f85\u7740\u7cfb\u5217\u7684\u6bcf\u4e00\u6b21\u66f4\u65b0\n\n\u8fd1\u3000devotee, enthusiast, fanatic, maniac\n\n\u53cd\u3000nonfan \u975e\u7c89\u4e1d\n\n"}
     usages
       0
         exp
           ［ə'dɪkt］ *v.* 沉溺，上瘾：to devote or **surrender**（oneself）to something habitually or **obsessively**
         der
         examples
           例　be addicted to drug/alcohol 沉溺于毒品、酒
         ants
         syns
       1
         exp
           ［'ædɪkt］ *n.* 对某事上瘾的人：a person with a strong and **habitual liking** for something
         der
         examples
           例　science-fiction addicts who eagerly await each new installment in the series 科幻小说爱好者，等待着系列的每一次更新
         ants
           反　nonfan 非粉丝
         syns
           近　devotee, enthusiast, fanatic, maniac
     word_block_str
       【考法1】［ə'dɪkt］ *v.* 沉溺，上瘾：to devote or **surrender**（oneself）to something habitually or **obsessively**
       例　be addicted to drug/alcohol 沉溺于毒品、酒
       【考法2】［'ædɪkt］ *n.* 对某事上瘾的人：a person with a strong and **habitual liking** for something
       例　science-fiction addicts who eagerly await each new installment in the series 科幻小说爱好者，等待着系列的每一次更新
       近　devotee, enthusiast, fanatic, maniac
       反　nonfan 非粉丝
     pos
       0
         1
       1
         6
     phon
    

## 处理释义

* 每次都把字符串中已经匹配的内容删除
* 先把词性匹配出来
* 再看释义是否包括音标。如果包括，匹配出来。如果不包括，留空，未来输出时，如果发现用法下面的音标项为空，就显示主词的音标。注意单独处理compliment的音标。
* 中英文划分的大概规则：以分词符“:”来区分中英文释义，左侧为中文，右侧为英文；如果没有分词符，那么只有中文释义
* 注意，对于冒号字符来说，中文全角、中文半角、英文全角在unicode中是等价的。所以先用函数`strF2H`将冒号统一为英文半角即可


```python
# check unicode
print 'cn_f:', repr(u'：'), 'cn_h:', repr(u'：')
print 'en_f:', repr(u'：'), 'en_h:', repr(u':')
# example
print 'Some examples of the raw string of the explanation field'
_ = map(iter_print, iter_value_of_key_through_d_l_d_d(new3000_base_d, 'usages', 'exp', 5))
```

    cn_f: u'\uff1a' cn_h: u'\uff1a'
    en_f: u'\uff1a' en_h: u':'
    Some examples of the raw string of the explanation field
     *vt.* 伪装（防止被认出）：to modify the manner or appearance of in order to **prevent recognition**
     *adj.* 极为神圣的，不可侵犯的：**most sacred** or holy
     *vt.* 废除，取消：to **make void**
     *n.* 扩荒者，先驱者：one of the **first to settle** in a territory
     *n.* 切断，分离，分裂：a **division** or split in a group or union: schism
     *vt.* 限制：to **limit** narrowly; restrict
     *vt.* 使消遣：to cause（someone）to pass the time **agreeably** occupied
     *adj.* 浑浊的，不清晰的：**lacking** in **clarity** or brightness
     *vi.* 为了给人留下印象而表演，哗众取宠：to play or act so as to **impress** onlookers
    


```python
%%sync_to_file $configNew3000BeforeMain
match_phon_re = re.compile(ur'［.*］', re.U)
match_pspeech_re = re.compile(ur'\*([a-z\/.]+\.)\*')
has_cn_char_fun = lambda _str: re.compile(ur'[\u4e00-\u9fa5]').search(_str) is not None
```


```python
# test
def unit_test():
    test_str = u"［ə'laɪ］ *v.* 加入联盟：to **enter** into an alliance"
    print match_pspeech_re.search(test_str).group(1)
    print match_phon_re.search(test_str).group()
    print has_cn_char_fun(test_str)
#unit_test()
del unit_test
```


```python
%%sync_to_file $configNew3000BeforeMain
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
```

分隔符最多有2个。当有两个分隔符时，拆分后的列表中，一般是后两个str对应英文释义，少数情形下前两个str对应中文释义。例外：
* abuse：考法2有两对中英文释义
* 【勘误】disaffected派生词的释义行，包含了两个派生词，disaffect和disaffection，以“;”间隔。  
其中disaffect是个复杂派生词，已经独立成词条，以disaffect索引。而disaffection本身是一个简单派生词，所以忽略掉这部分解释即可。


```python
%%sync_to_file $configNew3000BeforeMain
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
```


```python
%%sync_to_file $configNew3000AfterMain
new3000_base_d = process_exp_field_for_all_words(new3000_base_d)
```


```python
# test
#iter_print(new3000_base_d['ensconce'], print_list_index=True)
# check
_ = map(pprint, iter_through_and_sample_k(new3000_base_d, 5, [('all','',True), ('key','usages',False),
                                                              ('all','',False), ('key', 'exp_d', False),
                                                              ('key', 'en', False)]))
```

    [u'puissance', u'**power**; might']
    [u'repel', u'to **fight against**; resist']
    [u'strut', u'to **walk** with a **pompous** and affected air']
    [u'aphorism',
     u'a **short witty** sentence which expresses a general truth or comment']
    [u'gainsay', u'to **declare false**']
    

## 处理例句

### 示例

* 一个例句  
例　an audacious plan 一个冒进的计划

* 多个例句以“‖”(`\u2016`)间隔  
例　a bevy of ever-smiling aspirants for the Miss America title 一群想当美国小姐的少女‖Envy can make oneself backward; self-confidence can tell oneself to be an aspirant. 妒忌能使自己落后，自信能使自己上进。

* 中文符号出现在英文中  
“‘Frankenstein’...‘Dracula’...‘Dr. Jekyll and Mr. Hyde’... the archetypes that have influenced all subsequent horror stories”（New York Times）“‘弗兰肯斯坦’…‘德拉库拉’…‘杰基尔博士和海德先生’是影响了所有继之而来的恐怖故事的原型”（《纽约时报》）

* 缺少分隔符  
例　He became apoplectic about wasteful government spending. 他对政府的浪费开销感到怒不可遏。 The coach was so apoplectic when the player missed the free throw that he threw his clipboard onto the court. 教练对球员罚篮不进非常恼怒，把战术板扔到了球场上。


```python
# test
path_to_example = [('all', '', True), ('key', 'usages', False), ('all','',False),('key','examples',False)]
_ = map(functools.partial(iter_print, print_list_index=False), 
        iter_through_and_sample_k(new3000_base_d, 5, path_to_example))
del path_to_example
```

       grandeur
       例　the glory that was Greece and the grandeur that was Rome 希腊的荣耀和罗马的辉煌
       compound
       例　compound a felony 私了案件
       enamored
       例　Many teenage girls became enamored of the movie idol for her boyish good looks. 很多年轻的女孩子因为该影星男性化的帅气面庞而对她深深迷恋。
       ethics
       例　an old-fashioned work ethics 传统的工作行为规范
       trepidation
       例　trepidation about starting a new career 对开创一项新事业感到恐惧
    

### 判断缺少分隔符的情形
 
首先，[之前](#统计每行第一个字符)已经修正过两个例句占两行的情形。  
假定所有的例句，英文都出现在中文之前。如果一行内包含多个例句却没有分隔符，那么一定满足

* 如果一个字符串中包含多组中文字符串，那么除最后一组外，每组中文字符串后一定会跟一句英文
* 英文句子至少由两个单词构成，所以用`(?=[a-z]+ [a-z]+)`来匹配一个后面是英文句子的位置，同时编译模式选择忽略大小写
* 最后一组中文字符串一定可以匹配一个行尾字符
* 匹配模式要允许句首出现中文标点（比如引号），英文单词（一般是专有名词）或数字
* 中文半角逗号、中文全角逗号、英文全角逗号，unicode中是一个字符`\uff0c`
* `[\u4e00-\u9fa5]`匹配常见的中文字符，不包括标点符号


```python
%%sync_to_file $configNew3000BeforeMain
match_all_cn_re = ur' ?[a-z0-9：。；，“”（）、？《》]*?[\u4e00-\u9fa5]+.*?(?=$|[a-z]+ [a-z]+)'
match_all_cn_re = re.compile(match_all_cn_re, re.I)
```


```python
# example
test_str = u'He became apoplectic about wasteful government spending. 他对政府的浪费开销感到怒不可遏。 \
            The coach was so apoplectic when the player missed the free throw that he threw his clipboard onto the court.\
            教练对球员罚篮不进非常恼怒，把战术板扔到了球场上。'
results = match_all_cn_re.findall(test_str)
for sen in results:
    print sen
del results, test_str
```

     他对政府的浪费开销感到怒不可遏。             
     教练对球员罚篮不进非常恼怒，把战术板扔到了球场上。
    


```python
def detect_no_split_symbol(sentences_str):
    if sentences_str == '':
        return
    if sentences_str.startswith(u'例'):
        sentences_str = sentences_str[1:]
    else:
        print 'Warning! Not start with 例:', sentences_str
        return
    if u'\u2016' not in sentences_str:
        results = match_all_cn_re.findall(sentences_str)
        if len(results) > 1:
            for sentence in results:
                print sentence
            print sentences_str
            print '***********'
            
```


```python
def all_that_without_splt_symbol():
    path_to_example = [('all', '', False), ('key', 'usages', False), ('all','',False),('key','examples',False)]
    _ = map(detect_no_split_symbol, iter_through_general(new3000_base_d, path_to_example, False))
all_that_without_splt_symbol()
del all_that_without_splt_symbol
```

     通灵者的说法很快就遭到了科学家的反对。
     谴责对于性的过分重视
    　Scientists were quick to decry the claims of the psychic. 通灵者的说法很快就遭到了科学家的反对。decry the excessive emphasis on sex 谴责对于性的过分重视
    ***********
     在炎热潮湿的城市中行走使得她略显憔悴。
     在前所未有的疲劳面前，他开始变得脑力衰弱。
    　She had wilted a bit after walking around the hot and humid city. 在炎热潮湿的城市中行走使得她略显憔悴。His brain wilted from hitherto unprecedented weariness. 在前所未有的疲劳面前，他开始变得脑力衰弱。
    ***********
     低利率对于商业而言应该是有利的。
     善意的警告
    　The low interest rates should have a salutary effect on business. 低利率对于商业而言应该是有利的。a salutary warning 善意的警告
    ***********
     一个时常被粉丝起哄的有争议的歌手
     不少示威者在集会上起哄让发言者难堪。
    　a controversial singer who was constantly heckled by the fans 一个时常被粉丝起哄的有争议的歌手Several protesters were heckling the speaker at the rally. 不少示威者在集会上起哄让发言者难堪。
    ***********
     他对政府的浪费开销感到怒不可遏。 
     教练对球员罚篮不进非常恼怒，把战术板扔到了球场上。
    　He became apoplectic about wasteful government spending. 他对政府的浪费开销感到怒不可遏。 The coach was so apoplectic when the player missed the free throw that he threw his clipboard onto the court. 教练对球员罚篮不进非常恼怒，把战术板扔到了球场上。
    ***********
     锯末与胶水的味道弥漫了整个工厂。
     充斥在社会每个阶层中的腐败
    　The mixed smell of sawdust and glue pervaded the whole factory. 锯末与胶水的味道弥漫了整个工厂。the corruption that pervades every stratum of society 充斥在社会每个阶层中的腐败
    ***********
     大火过后整个房子只剩下被烧焦的骨架了。
     在报告发表之前，我们看到了他的整体框架。
    　Only the charred skeleton of the house remained after the fire. 大火过后整个房子只剩下被烧焦的骨架了。We saw a skeleton of the report before it was published. 在报告发表之前，我们看到了他的整体框架。
    ***********
     在豪华游轮上享受着无忧旅途的乘客
     春假期间无忧无虑的大学生
    　passengers on a luxury cruise ship enjoying a carefree vacation 在豪华游轮上享受着无忧旅途的乘客carefree college students on spring break 春假期间无忧无虑的大学生
    ***********
     那个纨绔子弟愿意花数千美元，只为他的女朋友买
     Birkin的包包。
    　That dandy was willing to spend thousands of dollars just to get the Hermes Birkin for his girlfriend. 那个纨绔子弟愿意花数千美元，只为他的女朋友买Hermes Birkin的包包。
    ***********
     就品位而言，艺术赞助人和收藏家
     Guggenheim是一个狂热者：她总是倾向于最新奇、最让人满意和最独特的佳品。
    　In matters of taste, the art patron and collector Peggy Guggenheim was a zealot: she was for the strangest, the most surprising, the most satisfying, the best, the unique. 就品位而言，艺术赞助人和收藏家Peggy Guggenheim是一个狂热者：她总是倾向于最新奇、最让人满意和最独特的佳品。
    ***********
     他总是三个小孩里最不听话的一个。
     过去行为上有些问题的调皮小孩
    　He had always been the most wayward of their three children. 他总是三个小孩里最不听话的一个。wayward children with a history of behavioral problems 过去行为上有些问题的调皮小孩
    ***********
     你介意晚饭时放一些令人愉快的音乐吗？
     因为感慨自然之美稍纵即逝而产生的令人愉悦的忧伤
    　Would you mind putting on some agreeable music for dinner? 你介意晚饭时放一些令人愉快的音乐吗？the agreeable melancholy resulting from a sense of the transitoriness of natural beauty 因为感慨自然之美稍纵即逝而产生的令人愉悦的忧伤
    ***********
     学生们为他们在世界中的角色感到迷茫。
     instructions因为不明确的指示而受挫
    　Students have ambiguous feelings about their role in the world. 学生们为他们在世界中的角色感到迷茫。frustrated by ambiguous instructions因为不明确的指示而受挫
    ***********
     理清思路;
     澄清某一问题
     clarify his mind 理清思路;clarify a subject 澄清某一问题
    ***********
     确保你在面试时的回答简短而恰当。
     你需要携带所有的相关证明。
    　Make sure your answers during the interview are short and relevant. 确保你在面试时的回答简短而恰当。You need to bring all the relevant certificates with you. 你需要携带所有的相关证明。
    ***********
     我不觉得他们做了室友之后能和谐相处。
     一个与对远古人类的已有知识不存在矛盾的理论
    　I don't think that they could be compatible as roommates. 我不觉得他们做了室友之后能和谐相处。a theory that is compatible with what we already know about early man 一个与对远古人类的已有知识不存在矛盾的理论
    ***********
    

【勘误】对于没有分隔符但却出现多段中文字符的句子  
* 匹配一个中文句号或中文问号，再加一个英文字符，在中文符号后加分隔符
* 对于单词heckle、carefree，匹配一个中文字符加英文字符，在中文字符后加分隔符
* 对于单词clarity，将“;”替换为分隔符


```python
%%sync_to_file $configNew3000BeforeMain
match_cn_punc_with_en_char_fun = lambda _str: re.search(ur'[。？]( )?(?=[a-z])', _str, re.I)
```


```python
# example
test_str = u"I don't think that they could be compatible as roommates. 我不觉得他们做了室友之后能和谐相处。a theory that is compatible with what we already know about early man 一个与对远古人类的已有知识不存在矛盾的理论"
cn_pun_index = match_cn_punc_with_en_char_fun(test_str).end()
print test_str[:cn_pun_index] + u'\u2016' + test_str[cn_pun_index:]
del test_str, cn_pun_index
```

    I don't think that they could be compatible as roommates. 我不觉得他们做了室友之后能和谐相处。‖a theory that is compatible with what we already know about early man 一个与对远古人类的已有知识不存在矛盾的理论
    


```python
%%sync_to_file $configNew3000BeforeMain
match_cn_char_with_en_char_fun = lambda _str: re.search(ur'[\u4e00-\u9fa5](?=[a-z])', _str, re.I)
```


```python
# example
test_str = u'passengers on a luxury cruise ship enjoying a carefree vacation 在豪华游轮上享受着无忧旅途的乘客carefree college students on spring break 春假期间无忧无虑的大学生'
cn_char_index = match_cn_char_with_en_char_fun(test_str).end()
print test_str[:cn_char_index] + u'\u2016' + test_str[cn_char_index:]
del test_str, cn_char_index
```

    passengers on a luxury cruise ship enjoying a carefree vacation 在豪华游轮上享受着无忧旅途的乘客‖carefree college students on spring break 春假期间无忧无虑的大学生
    


```python
%%sync_to_file $configNew3000BeforeMain
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
```


```python
%%sync_to_file $configNew3000AfterMain
new3000_base_d = revise_no_sep(new3000_base_d)
```


```python
# check
def unit_test():
    path_to_example = [('all', '', False), ('key', 'usages', False), ('all','',False),('key','examples',False)]
    _ = map(detect_no_split_symbol, iter_through_general(new3000_base_d, path_to_example, False))
unit_test()
del unit_test
```

     那个纨绔子弟愿意花数千美元，只为他的女朋友买
     Birkin的包包。
     That dandy was willing to spend thousands of dollars just to get the Hermes Birkin for his girlfriend. 那个纨绔子弟愿意花数千美元，只为他的女朋友买Hermes Birkin的包包。
    ***********
     就品位而言，艺术赞助人和收藏家
     Guggenheim是一个狂热者：她总是倾向于最新奇、最让人满意和最独特的佳品。
     In matters of taste, the art patron and collector Peggy Guggenheim was a zealot: she was for the strangest, the most surprising, the most satisfying, the best, the unique. 就品位而言，艺术赞助人和收藏家Peggy Guggenheim是一个狂热者：她总是倾向于最新奇、最让人满意和最独特的佳品。
    ***********
    

至此，多个例句应该都有分隔符间隔了。

### 拆分中英文

将每个例句的中英文分隔开。直接匹配英文部分即可。  


```python
%%sync_to_file $configNew3000BeforeMain
match_sentence_en_part_re = re.compile(ur'[a-z0-9éï\'";:,?!%()$ⅠⅡ.*/\- —　‘’“”（）]+(?=[＜《〈\u4e00-\u9fa5])', re.I)
```


```python
# example
test_str = u'     　add spices to the stew with complete abandon 肆无忌惮地向炖菜里面加调料'
print match_sentence_en_part_re.match(test_str).group()
del test_str
```

         　add spices to the stew with complete abandon 
    

上面的匹配规则，可能导致中文部分的内容也被匹配。比如  
`A GPA of 1.0 flusters him. 1.0的绩点让他很慌乱。`会被匹配为`A GPA of 1.0 flusters him. 1.0`  
注意到，错误匹配的部分，一定会与一个属于中文部分的字符紧密相连。  

如果匹配正确，这个紧密相连的部分应该是空格、英文句号、中文的右引号`”`、右括号`）`  
如果没匹配正确，那么可能是一个中文左引号`“`、数字、英文人名、专有名词等
* 数字，经过检查，确定方案如下。匹配的字符串从右至左遍历至第一个空格，取空格左侧的内容
* `GRE`、`IT`、`DNA`、`Jason`，处理方法同数字
* `“`、`“‘`，取字符组合左侧的字符串即可


```python
%%sync_to_file $configNew3000BeforeMain
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
```


```python
# test
#iter_print(sep_en_cn_sentence(new3000_base_d['abandon']['usages'][0]['examples']))
```


```python
%%sync_to_file $configNew3000BeforeMain
def process_examples(words_d):
    path_to_example = [('all', '', True), ('key', 'usages', False), ('all','',True),('key','examples',False)]
    example_iter = iter_through_general(words_d, path_to_example)
    for word, usage_index, example_str in example_iter:
        examples_en, examples_cn, examples_encn = sep_en_cn_sentence(example_str)
        words_d[word]['usages'][usage_index]['examples_d'] = {'en': examples_en, 'cn': examples_cn, 'en_cn': examples_encn}
    return words_d
```


```python
%%sync_to_file $configNew3000AfterMain
new3000_base_d = process_examples(new3000_base_d)
```


```python
# test
path_to_example_d = [('all', '', False), ('key', 'usages', False), ('all','',False),('key','examples_d',False)]
#_ = map(iter_print, iter_through_and_sample_k(new3000_base_d, 1, path_to_example_d))
del path_to_example_d
# check
iter_print(new3000_base_d['abandon']['usages'][0])
```

     exp_d
       en
         carefree, freedom from **constraint**
       cn
         放纵
       en_cn
         放纵：carefree, freedom from **constraint**
     pspeech
       n.
     ph_symbl
       [ə'bændən]
     examples_d
       en
         add spices to the stew with complete abandon
       cn
         肆无忌惮地向炖菜里面加调料
       en_cn
         add spices to the stew with complete abandon 肆无忌惮地向炖菜里面加调料
     der
     ants
     examples
       例 add spices to the stew with complete abandon 肆无忌惮地向炖菜里面加调料
     exp
       *n.* 放纵：carefree, freedom from **constraint**
     syns
       近　unconstraint, uninhibitedness, unrestraint
    

## 处理反义词

### 示例

* 反　timid, cowardice, cravenness, dastardliness, poltroonery 胆小，懦弱


```python
# test
path_to_ants = [('all','',False),('key','usages',False),('all','',False),('key','ants',False)]
#_ = map(iter_print, iter_through_and_sample_k(new3000_base_d, 2, path_to_ants))
del path_to_ants
```

### 拆分中英文


```python
%%sync_to_file $configNew3000BeforeMain
match_ants_en_part_re = re.compile(ur'[a-zéï][a-zéï ,-/]+(?=[　\u4e00-\u9fa5（]|$)', re.I)
```


```python
# example
test_str = u'unthreatening 没有威胁的；reassuring 令人安心的'
print test_str
iter_print(match_ants_en_part_re.findall(test_str))
```

    unthreatening 没有威胁的；reassuring 令人安心的
     0
       unthreatening 
     1
       reassuring 
    


```python
%%sync_to_file $configNew3000BeforeMain
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
```


```python
%%sync_to_file $configNew3000BeforeMain
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
```

【勘误】
* enfranchise考法2，`subjugate, subdue; enthrall`替换为`subjugate, subdue, enthrall`
* clan，反义词条目应该是派生词，因为在这之前处理的派生词，所以必须去前面更正


```python
%%sync_to_file $configNew3000AfterMain
new3000_base_d['enfranchise']['usages'][1]['ants'] = new3000_base_d['enfranchise']['usages'][1]['ants'].replace(u'subdue; enthrall', u'subdue, enthrall')
```


```python
%%sync_to_file $configNew3000AfterMain
new3000_base_d = process_all_ants(new3000_base_d)
```


```python
# test
path_to_ants = [('all','',False),('key','usages',False),('all','',False),('key','ants_d',False)]
#_ = map(iter_print, iter_through_and_sample_k(new3000_base_d, 10, path_to_ants))
del path_to_ants
#iter_print(new3000_base_d['polished'])
```

## 处理同义词

基本不用处理


```python
%%sync_to_file $configNew3000BeforeMain
strip_first_two_chars_fun = lambda _str: _str[2:]
```


```python
%%sync_to_file $configNew3000BeforeMain
def process_all_syns(words_d):
    path_to_syns = [('all','',True),('key','usages',False),('all','',True),('key','syns',False)]
    for word, usage_index, syns_str in iter_through_general(words_d, path_to_syns):
        usage_d = words_d[word]['usages'][usage_index]
        usage_d['syns'] = strip_first_two_chars_fun(syns_str)
    return words_d
```


```python
%%sync_to_file $configNew3000AfterMain
new3000_base_d = process_all_syns(new3000_base_d)
```


```python
%%sync_to_file $configNew3000AfterMain
with codecs.open('new3000_base_d.txt', 'w', encoding='utf-8') as f:
    json.dump(new3000_base_d, f)
```

## 最终结果


```python
# example
#iter_print(new3000_base_d['ad-lib'])
iter_print(new3000_base_d['salutary'])
#iter_print(new3000_base_d['fawn'])
```

     usages
       0
         exp_d
           en
             beneficial, **promoting health**
           cn
             有益健康的
           en_cn
             有益健康的：beneficial, **promoting health**
         ants_d
           en
             debilitating, deleterious, noxious, virulent 
           cn
             有害的，有毒的
           en_cn
             debilitating, deleterious, noxious, virulent 有害的，有毒的
         pspeech
           adj.
         ph_symbl
           ['sæljəteri]
         examples_d
           en
             salutary exercise
           cn
             有益健康的锻炼
           en_cn
             salutary exercise 有益健康的锻炼
         der
         ants
           反　debilitating, deleterious, noxious, virulent 有害的，有毒的
         examples
           例 salutary exercise 有益健康的锻炼
         exp
           *adj.* 有益健康的：beneficial, **promoting health**
         syns
           good, healthy, restorative, salubrious, tonic, wholesome
       1
         exp_d
           en
             **promoting** or contributing to personal or social **well-being**
           cn
             有利的,利好的
           en_cn
             有利的，利好的：**promoting** or contributing to personal or social **well-being**
         ants_d
           en
             bad, disadvantageous, unfavorable, unfriendly, unhelpful, unprofitable 
           cn
             不利的
           en_cn
             bad, disadvantageous, unfavorable, unfriendly, unhelpful, unprofitable 不利的
         pspeech
           adj.
         ph_symbl
           ['sæljəteri]
         examples_d
           en
             The low interest rates should have a salutary effect on business.
             a salutary warning
           cn
             低利率对于商业而言应该是有利的。
             善意的警告
           en_cn
             The low interest rates should have a salutary effect on business. 低利率对于商业而言应该是有利的。
             a salutary warning 善意的警告
         der
         ants
           反　bad, disadvantageous, unfavorable, unfriendly, unhelpful, unprofitable 不利的
         examples
           例 The low interest rates should have a salutary effect on business. 低利率对于商业而言应该是有利的。‖a salutary warning 善意的警告
         exp
           *adj.* 有利的，利好的：**promoting** or contributing to personal or social **well-being**
         syns
           advantageous, benefic, beneficent, benignant, favorable, friendly, helpful, kindly, profitable
     word_block_str
       【考法1】*adj.* 有益健康的：beneficial, **promoting health**
       例　salutary exercise 有益健康的锻炼
       近　good, healthy, restorative, salubrious, tonic, wholesome
       反　debilitating, deleterious, noxious, virulent 有害的，有毒的
       【考法2】*adj.* 有利的，利好的：**promoting** or contributing to personal or social **well-being**
       例　The low interest rates should have a salutary effect on business. 低利率对于商业而言应该是有利的。a salutary warning 善意的警告
       近　advantageous, benefic, beneficent, benignant, favorable, friendly, helpful, kindly, profitable
       反　bad, disadvantageous, unfavorable, unfriendly, unhelpful, unprofitable 不利的
     pos
       0
         22
       1
         4
     phon
       ['sæljəteri]
    

# 处理《GRE核心词汇助记与精练》


```python
%%sync_to_file $configZhujiAfterMain
zhuji_base_str = codecs_open_r_utf8(file_zhuji)
```

由于转换格式选择了markdown，所以会有大量的转义字符。比如`\[`、`\(`等。统一剔除前面的转义符。


```python
%%sync_to_file $configZhujiBeforeMain
match_escape_char_re = re.compile(r'\\(?=[\[\]()*+])')
```


```python
%%sync_to_file $configZhujiAfterMain
zhuji_base_str = match_escape_char_re.sub('', zhuji_base_str)
```


```python
%%sync_to_file $configZhujiAfterMain
zhuji_base_str = collapse_blank_line(zhuji_base_str)
```

将合并空行后的文本输出到临时文件。之后以该临时文件为寻找文本规律的依据。


```python
%%sync_to_file $configZhujiAfterMain
with codecs.open('temp_zhuji_base_str.txt', 'w', encoding='utf-8') as f:
    f.write(zhuji_base_str)
```

## 提取思路

+ 前言部分说明了词条的结构

        三、单个词条的编排

        词条结构

        每一个单词的第一行是拼写和音标，接下来是对这个单词的助记法。有可能是以下五种之一：

        （1）[根]词根词缀记忆法；

        （2）[联]联想助记法；

        （3）[源]通过词源解释单词；

        （4）[记]其他助记法；

        （5）[参]提供相关词助记；

        此外，每条助记法在词条的最后可能有[注]，给出一些对理解和记忆单词有帮助的内容。
    
 所以，每个单词块以英文单词为起始，以下一个单词的开始为结束


+ 单词块包含在List里，先识别List块，再识别单词块。  
List以“### List”加一个空格加一个数字开始

## Extract List Block

只处理第一篇的内容


```python
%%sync_to_file $configZhujiAfterMain
zhuji_base_str = zhuji_base_str.split(u'# 第二篇 核心词汇练习')[0]
```


```python
%%sync_to_file $configZhujiBeforeMain
match_zhuji_list_start_re = re.compile(ur'### List \d+', re.M)
```


```python
%%sync_to_file $configZhujiAfterMain
zhuji_base_list_l = extract_content_between(zhuji_base_str, match_zhuji_list_start_re)
```


```python
# check
print 'Should have 39 Lists. Extract', len(zhuji_base_list_l)
# test
#print zhuji_base_list_l[38]
```

    Should have 39 Lists. Extract 39
    

## 提取etyma_block

+ 先把list_block 按照 “小结&复习” 拆分成两部分，然后只处理第一部分
    
+ 匹配一个词根块（etyma_block）的起始    
行首一个数字加符号“.”，然后匹配任意字符到行尾。对于List37-List39，匹配行首Unit。

+ 每个词根块匹第一行配出词根，并且筛选掉无意义的词根

+ List 36的词根应该加上前缀“与动物有关的单词”


```python
%%sync_to_file $configZhujiBeforeMain
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
```


```python
%%sync_to_file $configZhujiAfterMain
zhuji_base_d_l_l = get_etyma_block_d_l_l(zhuji_base_list_l)
```


```python
# check
print 'In total', len(zhuji_base_d_l_l), 'lists'
```

    In total 39 lists
    


```python
%%sync_to_file $configZhujiBeforeMain
def revise_miss_etyma(base_d_l_l):
    # revise list 25 etyma 3 revise tum
    base_d_l_l[25-1][3-1]['ety'] = 'tum'
    # revise list 5 etyma 4 revise post, pound
    base_d_l_l[5-1][4-1]['ety'] = 'post, pound'
    # revise list 6 etyma 7 revise vad, vag, ced
    base_d_l_l[6-1][7-1]['ety'] = 'vad, vag, ced'
```


```python
%%sync_to_file $configZhujiAfterMain
revise_miss_etyma(zhuji_base_d_l_l)
```


```python
# example
iter_print(zhuji_base_d_l_l[24][2])
```

     ety
       tum
     summary
       contumacious形容 [-acious] “像 (肿瘤 [tumor] 一样) 完全 [con-] 凸起 [tum]”, 比喻不服从的，倔强的 (肿瘤不服从正常的细胞分化规律, 不易根治)。tumult指社会“肿胀 [tum] 起来, 一些人煽动、使动荡”, 即骚乱，暴动 (像肿瘤一样不断膨胀，对人、社会危害极大)。
     pos
       0
         25
       1
         3
     ety_block_str
       词根tum表示swell [肿胀] , 构成单词tumor [n. 肿瘤]。
       contumacious [ˌkɑ:ntju'meɪʃəs]
       [根] con- [加强语气] + tum [swell] + -acious [a.], swell completely, 像肿瘤一样肿胀、凸起 → a. 不服从的，倔强的
       tumult ['tjuːmʌlt]
       [根] tum [swell] + -ult [n.], swell [肿胀], 不平静 → n. 骚动，暴动
    

## 处理ety_block_str

* 之前提取的ety_block_str里包含了对词根组的解释（etyma_group_explanation），以及所有的同根词（cognate_block）。
* cognate_block以单词加上音标为起始，第一个cognate_block之前的就是etyma_group_explanation，两个开始位置只间的就是一个cognate_block


```python
%%sync_to_file $configZhujiBeforeMain
match_cognate_block_start_re = re.compile(ur'^([a-zéï-]+)(.*?)(\[.*\])$', re.M|re.I)
```


```python
# example
iter_print(extract_content_between(zhuji_base_d_l_l[1-1][6-1]['ety_block_str'], match_cognate_block_start_re, True))
```

     0
       verb作为单词是“动词”的意思，作为词根指一般的单词，即word。
     1
       verbatim [vɜːr'beɪtɪm]
       [根] verb [word] + a + tim (e), (a) word a time → ad.逐字地 (抄写) → 一字不差地
     2
       verbose [vɜːr'boʊs]
       [根] verb [word] + -ose [a., full of], full of words → a.冗长的，嗦的
       [注] 同义词wordy [a. 冗长的，嗦的]
     3
       reverberate [rɪ'vɜːrbəreɪt]
       [根] re- [back] + verb [word, sound] + er + -ate [v.],sound back → vi. 回荡，回响
       [注] 也可以参考vibrate [v. 震动] ，将reverberate理解成 (声波的) 回震，即回荡、回响
    


```python
%%sync_to_file $configZhujiBeforeMain
def process_ety_block_str(base_d_l_l):
    path_to_ety_block_str = [('all','',True),('all','',True),('key','ety_block_str',False)]
    for list_index, ety_index, ety_block_str in iter_through_general(base_d_l_l, 
                                                                     path_to_ety_block_str):
        etyma_block_d = base_d_l_l[list_index][ety_index]
        returned_l = extract_content_between(ety_block_str, match_cognate_block_start_re, True)
        ety_group_exp = returned_l.pop(0).strip()
        etyma_block_d['etyma_group_explanation'] = ety_group_exp
        etyma_block_d['cognate_block_str_l'] = returned_l
```


```python
%%sync_to_file $configZhujiAfterMain
process_ety_block_str(zhuji_base_d_l_l)
```


```python
# test
#iter_print(zhuji_base_d_l_l[26-1][3-1])
```

## 处理cognate_block_str

一个cognate_block，可以从首行提取出word，音标（phon）  
之后，每行应该以“[”开始。以此标准，查看例外。查看后，发现如下特例。

* 【勘误】“源”没有被包括在“[]”中
* 单词facilitate中包含了大量的额外内容，整合到一起就可以了
* 【勘误】 词根`surg, cit`，以`(1)`、`(2)`分了两部分。去前面[提取etyma_block](#提取etyma_block)中更正
* List 26, 第2个词根，所有单词只有简单的释义，不用修改。  
【勘误】该词根块的最后一个单词，rejoice的最后一行应该加到ety_group_explanation后。  
去前面[提取etyma_block](#提取etyma_block)中更正
* List 2, 第6个词根，行“`以下两个单词中的ord和cant与“说”没有关系`”没有用。忽略了。
* 【勘误】 List 13, 第3个词根  
`以下的4个单词可以将scru按照读音联想成“四顾”，表示“ (顾虑地) 看”。`应该将scru提取出来，作为后4个单词的词根。


```python
%%sync_to_file $configZhujiBeforeMain
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
```


```python
%%sync_to_file $configZhujiAfterMain
revise_scru(zhuji_base_d_l_l)
```


```python
%%sync_to_file $configZhujiBeforeMain
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
```


```python
%%sync_to_file $configZhujiBeforeMain
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
```


```python
%%sync_to_file $configZhujiAfterMain
zhuji_base_word_d = process_all_cognate_block(zhuji_base_d_l_l)
```

    Warning! word already exists! scruple
    Warning! word already exists! scrupulous
    Warning! word already exists! scrutable
    Warning! word already exists! scrutinize
    Warning! word already exists! noisome
    Warning! word already exists! understate
    

## 添加同根词列表

依据cognate_block_str_l给每个单词添加同根词列表。只对有意义的词根添加。


```python
%%sync_to_file $configZhujiBeforeMain
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
```


```python
%%sync_to_file $configZhujiAfterMain
add_etyma_cognates_l(zhuji_base_word_d, zhuji_base_d_l_l)
```

* 【勘误】List 25 第3个词根，应该是tum，在[处理ety_block_str](#处理ety_block_str)之前修订
* 【勘误】List 5 第4个词根，应该是“post, pound”，在[处理ety_block_str](#处理ety_block_str)之前修订
* 【勘误】List 6 第7个词根，应该是“vad, vag, ced”，在[处理ety_block_str](#处理ety_block_str)之前修订


```python
%%sync_to_file $configZhujiAfterMain
with codecs.open('zhuji_base_d.txt', 'w', encoding='utf-8') as f:
    json.dump(zhuji_base_word_d, f)
```

## 最终成果


```python
# example
pprint(zhuji_base_word_d['pervade'])
iter_print(zhuji_base_word_d['pervade'])
```

    {'content': u'[\u6839] per- [through] + vad [go] + -e [v.], go through, \u904d\u5e03 \u2192 vt. \u5f25\u6f2b\uff0c\u5145\u6ee1\n',
     'ety': 'vad, vag, ced',
     'etyma_cognates_l': u'pervade, evasive, extravagant, vague, cessation, incessant',
     'etyma_group_explanation': u'(1) \u8bcd\u6839vad\u548cvas\u8868\u793ago [\u8d70]\u3002invade [v. \u4fb5\u7565\uff0c\u540d\u8bcd\u5f62\u5f0finvasion] \u7684\u5b57\u9762\u4e49\u5c31\u662f\u201c\u8d70 [vad] \u5165 [in-] \u4ed6\u56fd\u9886\u571f\u201d\u3002\n(2) \u8bcd\u6839vag\u8868\u793awander\u3002\u53ef\u4ee5\u53c2\u8003wag [\u6447\u6446] \u4ee5\u53ca\u4e0a\u4e00\u6761\u8bcd\u6839vad/vas\u52a0\u6df1\u8bb0\u5fc6\u3002\n(3) \u8bcd\u6839ced\u548ccess\u9664\u4e86\u8868\u793ago [\u8d70] \u4e4b\u5916, \u5728\u5176\u6784\u6210\u7684\u5c11\u91cf\u5355\u8bcd\u4e2d\u8fd8\u8868\u793a\u201c\u8d70\u5f00\u201d\uff0c\u5373\u79bb\u5f00\uff0c\u5f15\u7533\u51fa\u505c\u6b62\u7684\u542b\u4e49\u3002',
     'phon': u"[p\u0259r've\u026ad]",
     'pos': u'6, 7',
     'summary': u'\n\u8bcd\u6839vad\u8868\u793ago [\u8d70]\uff1ainvade [\u4fb5\u7565] \u662f\u6307\u201c (\u672a\u7ecf\u5141\u8bb8\u7684\u60c5\u51b5\u4e0b) \u8d70 [vad] \u8fdb [in-]\u201d\uff1bpervade\u6307\u201c\u8d70 [vad] \u904d [per-]\u201d, \u5f53\u6c14\u4f53\u6216\u6c1b\u56f4\u201c\u8d70\u904d\u201d\u7a7a\u95f4\u7684\u6bcf\u4e00\u4e2a\u89d2\u843d\uff0c\u5373\u5f25\u6f2b\uff0c\u5145\u6ee1\uff1bevasive\u5f62\u5bb9\u4e8b\u7269\u201c(\u4ece\u4eba\u4eec\u7684\u89c6\u7ebf\u3001\u638c\u5fc3\u4e2d) \u8d70 [vas] \u6389 [e-=ex-] \u7684 [-ive]\u201d, \u5373\u96be\u4ee5\u53d1\u73b0\u3001\u6355\u6349\u3001\u5206\u79bb\u7684\uff0c\u4e5f\u6307\u8bf4\u8bdd\u65f6\u201c\u56de\u907f [go [vas] away [e-]] \u7684 [-ive]\u201d, \u5373\u542b\u7cca\u5176\u8f9e\u7684\u3002vague\u5f62\u5bb9\u201c\u98d8\u5ffd\u4e0d\u5b9a [vag, wander] \u7684 [-ue]\u201d, \u5373\u542b\u4e49\u4e0a\u8868\u8fbe\u4e0d\u6e05\u7684\uff0c\u89c6\u89c9\u4e0a\u8f6e\u5ed3\u4e0d\u6e05\u6670\u7684\uff0c(\u53ef\u6982\u62ec\u6210\u201c\u6a21\u7cca\u7684\u201d); extravagant\u8868\u793a\u201c\u8fc7\u5ea6 [wander [vag] outside [extra-]] \u7684 [-ant] \u201d\uff0c\u4e5f\u7279\u6307\u201c\u82b1\u94b1\u8fc7\u5ea6\u7684\u201d, \u5373\u6325\u970d\u7684\u3002cessation [\u7ec8\u6b62\uff0c\u6682\u505c], \u6765\u81ea\u8bcd\u6839cess\u7531\u201c\u8d70\u5f00\u201d\u5f15\u7533\u51fa\u7684\u201c\u505c\u6b62\u201d; incessant\u8868\u793a\u201c\u4e0d [in-] \u505c\u6b62 [cess] \u7684 [-ant]\u201d, \u5373\u65e0\u95f4\u65ad\u7684\u3002\n',
     'word': u'pervade'}
     word
       pervade
     etyma_group_explanation
       (1) 词根vad和vas表示go [走]。invade [v. 侵略，名词形式invasion] 的字面义就是“走 [vad] 入 [in-] 他国领土”。
       (2) 词根vag表示wander。可以参考wag [摇摆] 以及上一条词根vad/vas加深记忆。
       (3) 词根ced和cess除了表示go [走] 之外, 在其构成的少量单词中还表示“走开”，即离开，引申出停止的含义。
     ety
       vad, vag, ced
     pos
       6, 7
     summary
       词根vad表示go [走]：invade [侵略] 是指“ (未经允许的情况下) 走 [vad] 进 [in-]”；pervade指“走 [vad] 遍 [per-]”, 当气体或氛围“走遍”空间的每一个角落，即弥漫，充满；evasive形容事物“(从人们的视线、掌心中) 走 [vas] 掉 [e-=ex-] 的 [-ive]”, 即难以发现、捕捉、分离的，也指说话时“回避 [go [vas] away [e-]] 的 [-ive]”, 即含糊其辞的。vague形容“飘忽不定 [vag, wander] 的 [-ue]”, 即含义上表达不清的，视觉上轮廓不清晰的，(可概括成“模糊的”); extravagant表示“过度 [wander [vag] outside [extra-]] 的 [-ant] ”，也特指“花钱过度的”, 即挥霍的。cessation [终止，暂停], 来自词根cess由“走开”引申出的“停止”; incessant表示“不 [in-] 停止 [cess] 的 [-ant]”, 即无间断的。
     content
       [根] per- [through] + vad [go] + -e [v.], go through, 遍布 → vt. 弥漫，充满
     etyma_cognates_l
       pervade, evasive, extravagant, vague, cessation, incessant
     phon
       [pər'veɪd]
    

# 处理《GRE高分必备短语搭配》

## 文本结构分析

+ 每一章都以“# Unit”加上空格和数字开头
+ 第n次匹配的结尾到第n+1次匹配的开头之间，就是一个单元的内容
+ 每个单元，只拆分“检测练习”之前的内容，匹配“## 检测练习”
+ 每个单元内部，每一个词组的第一行都以“`**`”开始和结束。
+ 第一行内，一般包含词组英文拼写和中文解释。有的词组多个释义，所以首行只有拼写。
+ 每个词组下，有三个条目，释，例，题。释和例都单独成行，题占了三行

## 提取基本内容

+ 去除转义字符
+ 按单元提取
+ 处理索引
+ 按词组提取。


```python
%%sync_to_file $configDyAfterMain
dy_base_str = codecs_open_r_utf8(file_duanyu)
```


```python
%%sync_to_file $configDyAfterMain
match_escape_char_re = re.compile(r'\\(?=[\[\]()*+])')
dy_base_str = match_escape_char_re.sub('', dy_base_str)
```


```python
%%sync_to_file $configDyBeforeMain
def extract_dy_unit(base_str):
    base_str = base_str.split(u"# 索引\n")[0]
    match_dy_unit_start_re = re.compile(ur'^# Unit \d+', re.M)
    base_unit_str_l = extract_content_between(base_str, match_dy_unit_start_re)
    base_unit_str_l = [base_unit_str.split(u'## 检测练习\n')[0] for base_unit_str in base_unit_str_l]
    return base_unit_str_l
```


```python
%%sync_to_file $configDyAfterMain
dy_base_unit_str_l = extract_dy_unit(dy_base_str)
```


```python
# check
print len(dy_base_unit_str_l), "units extracted"
# print dy_base_unit_str_l[35]
```

    36 units extracted
    


```python
%%sync_to_file $configDyBeforeMain
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
```


```python
%%sync_to_file $configDyAfterMain
dy_index_d = extract_dy_index_content(dy_base_str)
```


```python
# check
print len(dy_index_d), 'phrases in total'
print dy_index_d['a barrage of']
```

    365 phrases in total
    大量的  
    


```python
%%sync_to_file $configDyBeforeMain
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
```


```python
%%sync_to_file $configDyAfterMain
dy_phrase_d = extract_dy_phrase_d(dy_base_unit_str_l)
```


```python
# example
print len(dy_phrase_d)
iter_print(dy_phrase_d['so far'])
```

    365
     exp_cn
     pos
       8
     phrase_block_str
       **1. 到目前为止**
       **释** If you tell or ask someone what has happened **so far**, you are telling or asking them what has happened **up until the present point** in a situation or story, and often implying that something different might happen later.
       **例** So far there has been no word from the missing aircraft that disappeared from the radar four hours ago.
       **题** It is not particularly surprising that some earlier scholarship concerning such cultures has so far gone unchallenged.
       关于这些文化的一些早期学说一直没有被人质疑，这并不是一件特别奇怪的事情。
       **2. 有限地**
       **释** If you say that something only goes **so far** or can only go so far, you mean that its extent, effect, or influence is **limited**.
       **例** The church can only go so far in secular matters.
       **题** In pollen dating, geologic happenings are dated in terms of each other, and one can get just so far by matching independent sequences; but in radiocarbon dating the scale of time is measured in absolute terms of centuries or years.
       在孢粉定年法中，地质历史上的事件是通过彼此的顺序确定的，因此我们只能有限地匹配不同的独立序列；而放射性碳同位素断年技术则能精确到世纪甚至是日历年的时间尺度。
    

## 依据index校订


```python
for word in dy_index_d:
    if word not in dy_phrase_d:
        print word
print '****'
for word in dy_phrase_d:
    if word not in dy_index_d:
        print word
```

    under one's control
    on one's own
    ****
    under one’s control
    on one’s own
    

【勘误】上面两个单词，将中文的单引号替换为英文


```python
%%sync_to_file $configDyAfterMain
# revise ’'
dy_phrase_d['under one\'s control'] = dy_phrase_d[u'under one’s control']
dy_phrase_d['on one\'s own'] = dy_phrase_d[u'on one’s own']
del dy_phrase_d[u'under one’s control'], dy_phrase_d[u'on one’s own']
```


```python
# check
for word in dy_index_d:
    if word not in dy_phrase_d:
        print word
```

## 处理phrase_block_str

+ 先判断该词组是否多义，即词组是否有中文释义。
+ 如果多个释义，每个释义块的第一行都以数字加英文句号`.`开始
+ 对于每个释义，除却中文释义外，释对应英文释义，占1行，例对应例句，占1行，题对应GRE例句，占3行


```python
%%sync_to_file $configDyBeforeMain
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
```


```python
%%sync_to_file $configDyAfterMain
dy_phrase_processed_d = process_dy_phrase_block_str(dy_phrase_d)
```


```python
%%sync_to_file $configDyAfterMain
with codecs.open('duanyu_base_d.txt', 'w', encoding='utf-8') as f:
    json.dump(dy_phrase_processed_d, f)
```


```python
# example
iter_print(dy_phrase_processed_d['so far2'])
```

     gre_example_cn
       在孢粉定年法中，地质历史上的事件是通过彼此的顺序确定的，因此我们只能有限地匹配不同的独立序列；而放射性碳同位素断年技术则能精确到世纪甚至是日历年的时间尺度。
     pos
       8
     cn_exp
       有限地
     gre_example_en
       In pollen dating, geologic happenings are dated in terms of each other, and one can get just so far by matching independent sequences; but in radiocarbon dating the scale of time is measured in absolute terms of centuries or years.
     en_exp
       If you say that something only goes **so far** or can only go so far, you mean that its extent, effect, or influence is **limited**.
     example
       The church can only go so far in secular matters.
    
