import re
import os

from collections import namedtuple
from sys import stdin, argv

from parse import find_parser
from term import input_one_char, clear, choose, read_current_screen

StackTrace = namedtuple('StackTrace', ['kind', 'refs'])


def collect_stacktraces(stream):
    iter_stream = iter(stream)
    st = None
    parser = None
    for line in iter_stream:
        res = find_parser(line)
        if res:
            if st:
                yield st
            st = StackTrace(res.kind, [])
            parser = res.fn
        if parser:
            parsed = parser(line, iter_stream)
            if parsed:
                st.refs.append(parsed)
    if st:
        yield st


def cache_files(filenames):
    contents = {}
    for filename in filenames:
        if filename not in contents:
            with open(filename, 'r') as f:
                content =  list(f.readlines())
                contents[filename] = content
    return contents

DEBUG = False

def display_line_context(content, focus_line):
    before_lines = 10
    after_lines = 10
    first_line = max(0, focus_line-before_lines)
    last_line = min(len(content), focus_line+before_lines)

    for i, line in zip(range(first_line, last_line), content[first_line:last_line]):
        cur_line = i - first_line + 1
        prefix = '--> ' if cur_line == focus_line else '    '
        debug = '%s %s' % (focus_line, i) if DEBUG else ''
        print('%s%s%s %s' % (debug, prefix, cur_line, line.rstrip()))

    print()


def display_refs(refs, cur_ref):
    for i, stackref in enumerate(refs):
        print('-->' if i == cur_ref else '   ', stackref.stacktrace_line) 
    print()


def choose_stacktrace(stacktraces):
    print(stacktraces)
    if len(stacktraces) == 1:
        return stacktraces[0]
    choices = [
        {
            'label': '\n'.join([ref.stacktrace_line for ref in stacktrace.refs]),
            'value': stacktrace
        }
        for stacktrace in stacktraces
    ]
    return choose({
        'title': 'Several stacktraces found, please choose one (use arrow keys)',
        'choices': choices
    })


def display_ref_info(ref):
    print('%s:%s' % (ref.filename, ref.line_number))
    print(ref.stacktrace_line)


def navigate_stacktrace(stacktrace, cache):
    cur_ref = 0
    refs = stacktrace.refs

    while True:
        ref = refs[cur_ref]
        clear()

        content = cache[ref.filename]
        display_ref_info(ref)
        display_line_context(content, ref.line_number)
        display_refs(refs, cur_ref)

        try:
            question = '[Next n] [Previous p] [Edit e] ? '
            c = input_one_char(question)
            if c == 'p' or c == 'UP':
                direction = 1
            elif c == 'n' or c == 'DOWN':
                direction = -1
            elif c == 'e':
                sp.call('vi %s +%s' % (filename, line_number), shell=True)
            elif c == 'LEFT':
                return
            else:
                direction = 0
            cur_ref = min(max(cur_ref - direction, 0), len(refs) - 1)

        except SyntaxError:
            pass


def navigate_stacktrace_from_lines(lines):
    stacktraces = list(collect_stacktraces(lines))

    if len(stacktraces) == 0:
        print('No stacktrace found')
        return

    stacktrace = choose_stacktrace(stacktraces)
    filenames = set([ref.filename for ref in stacktrace.refs])
    cache = cache_files(list(filenames))
    navigate_stacktrace(stacktrace, cache)


def get_lines(argv):
    lines = None
    if len(argv) > 1:
        filename = argv[1]
        with open(filename) as f:
            lines = f.readlines()
    else:
        lines = read_current_screen()
    return lines


def main():
    lines = get_lines(argv)
    try:
        if lines:
            navigate_stacktrace_from_lines(lines)
        else:
            print('Could not find stacktrace source, please indicate a file or use kitty shell')
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
