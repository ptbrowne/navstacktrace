from os import getenv, popen
import subprocess as sp
from getch import getch

def get_terminal_size():
    rows, columns = os.popen('stty size', 'r').read().split()
    return rows, columns


def input_one_char(question=None):
    if question:
        print(question)
    c = getch()
    if c == '\033':
        getch()
        n = getch()
        if n == 'A':
            return 'UP'
        elif n == 'B':
            return 'DOWN'
        elif n == 'C':
            return 'RIGHT'
        elif n == 'D':
            return 'LEFT'
    if c == '\r' or c == '\n':
        return 'ENTER'
    return c

def clear():
    sp.call('clear',shell=True)


def choose(options):
    title = options.get('title')
    choices = options['choices']

    cur = 0
    while True:
        clear()
        if title:
            print(title)
        for i, choice in enumerate(options['choices']):
            lines = choice['label'].split('\n')
            for j, line in enumerate(lines):
                prefix = '-->' if cur == i and j == 0 else '   '
                print('%s %s' % (prefix, line))
            print()

        c = input_one_char()
        if c == 'UP':
            cur = max(cur - 1, 0)
        elif c == 'DOWN':
            cur = min(cur + 1, len(choices) - 1)
        elif c == 'RIGHT' or c == 'ENTER':
            return choices[cur]['value']


def kitty_screen_readlines():
    return popen('kitty @ get-text ', 'r').read().split('\n')


def tmux_screen_readlines():
    return popen('tmux capture-pane -pS -100', 'r').read().split('\n')


def is_kitty():
    term_info = getenv('TERMINFO')
    return 'kitty' in term_info


def is_tmux():
    return getenv('TMUX')


def read_current_screen():
    if is_kitty():
        return kitty_screen_readlines()
    elif is_tmux():
        return tmux_screen_readlines()
    else:
        return []

if __name__ == '__main__':
    # while True:
    #     print(input_one_char())
    print(kitty_screen_readlines())
