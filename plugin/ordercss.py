import re, collections

CSS_PROPERTIES_LIST = [
    'border-top',
    'z-index',
    'overflow',
    'border',
]

CSS_PROPERTIES_MAP = collections.defaultdict(lambda: None)

PROPERTY_REGEX = re.compile('^\s*([-\w]+):.*;\s*$')

for index in range(len(CSS_PROPERTIES_LIST)):
    CSS_PROPERTIES_MAP[CSS_PROPERTIES_LIST[index]] = -index

def get_line_index(line):
    word_match = PROPERTY_REGEX.match(line).group(1)
    return CSS_PROPERTIES_MAP[word_match]

def cmp_lines(a, b):
    match_a = get_line_index(a)
    match_b = get_line_index(b)
    return -cmp(match_a, match_b)

def find_end(lines, index):
    cur_result = index
    while index < len(lines):
        if len(lines[index].strip()) == 0:
            pass
        elif PROPERTY_REGEX.match(lines[index]):
            cur_result = index
        else:
            break
        index += 1
    return cur_result

def transform(lines):
    cur_line = 0

    result_block = []

    while cur_line < len(lines):
        if PROPERTY_REGEX.match(lines[cur_line]):
            block_end = find_end(lines, cur_line)

            new_block = sorted([line for line in lines[cur_line:block_end + 1] if len(line) > 0], cmp = cmp_lines)
            result_block.extend(new_block)

            cur_line = block_end + 1
        else:
            result_block.append(lines[cur_line])
            cur_line += 1

    return result_block

import vim

first_line = int(vim.eval('a:firstline'))
last_line =  int(vim.eval('a:lastline'))

lines = list(vim.current.buffer.range(first_line, last_line))

vim.current.buffer[first_line - 1:last_line] = transform(lines)
