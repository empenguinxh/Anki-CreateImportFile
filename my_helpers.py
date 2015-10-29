
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
def iter_through_and_sample_k(obj_iter, k, path):
    obj_iter_follow_path = iter_through_general(obj_iter, path)
    return reservoir_sample_k(obj_iter_follow_path, k)
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
def is_file_and_json_load(file_name_str):
    if os.path.isfile(file_name_str):
        with codecs.open(file_name_str, 'r', encoding='utf-8') as f:
            json_d = json.load(f)
        return json_d