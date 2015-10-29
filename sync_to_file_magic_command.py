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