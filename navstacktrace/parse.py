import re
from collections import namedtuple

StackRef = namedtuple('StackRef', ['filename', 'line_number', 'stacktrace_line'])
StackParser = namedtuple('StackParser', ['kind', 'fn', 'matcher'])

def parse_js_stacktrace_line(line, stream):
    file_line = re.search(r'\(((?:/[a-zA-Z-0-9\.]+)+):([0-9]+)', line)
    if file_line:
        filename = file_line.groups()[0]
        line_number = file_line.groups()[1]
        return StackRef(filename, int(line_number), line.strip())


def parse_py_stacktrace_line(line, stream):
    file_line = re.search(r'"((?:/[a-zA-Z-0-9\.]+)+)", line ([0-9]+)', line)
    if file_line:
        filename = file_line.groups()[0]
        line_number= file_line.groups()[1]
        line = next(stream).strip()
        return StackRef(filename, int(line_number), line.strip())


def js_matcher(line):
    return re.search('^.*Error:', line)


def py_matcher(line):
    return line.startswith('Traceback')


parsers = [
    StackParser('js', parse_js_stacktrace_line, js_matcher),
    StackParser('py', parse_py_stacktrace_line, py_matcher),
]


def find_parser(line):
    for parser in parsers:
        if parser.matcher(line):
            return parser
