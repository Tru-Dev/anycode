import rollbar
import re


rollbar.init('4594787cdcb848a9b6eee3758ec0507e')


def parse(code):
    keywords = {'if', 'else', 'elif', 'func', 'for', 'return', 'print', 'class',
                'and', 'or', 'not'
                }
    symbols = [
        ('string',     r'"(?:\\"|\w?|\W?|[^"])*"'),
        ('number',     r'\d+(\.\d*)?'),
        ('relop',      r'(==|>|<|>=|<=|!=)'),
        ('assignop',   r'[+\-*/%^]='),
        ('assign',     r'='),
        ('end',        r';'),
        ('id',         r'[A-Za-z]\w*'),
        ('op',         r'[+\-*/%^]'),
        ('newline',    r'\n'),
        ('whitespace', r'[ \t]+'),
        ('block',      r'[{}]'),
        ('invalid',    r'.')
    ]
    regexp = '|'.join('(?P<%s>%s)' % pair for pair in symbols)
    line_num = 1
    line_start = 0
    for m in re.finditer(regexp, code):
        mtype = m.lastgroup
        value = m.group(mtype)
        if mtype == 'newline':
            line_start = m.end()
            line_num += 1
        elif mtype == 'whitespace':
            pass
        elif mtype == 'invalid':
            raise RuntimeError(f'{value!r} on line {line_num}')
        else:
            if mtype == 'id' and value in keywords:
                mtype = value
            yield (mtype, value, line_num, m.start() - line_start)


test = r'''
if x == "goodfory\"ouuu\"" {
    lol = 2
    foo = lol / 2 * 0.5
}
'''


for m in parse(test):
    print(m)