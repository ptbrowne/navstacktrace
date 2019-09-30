# Navstacktrace

When your program crashes outputting a stacktrace, it is possible that you
want to inspect the stacktrace and look at the lines easily.

navstacktrace acts as a crude debugger where you can navigate between all
the files present in the stacktrace, seeing each line of the stacktrace
in context.

## Features

- Navigate stacktrace lines with arrows (up, down)
- Open an editor at the line you're currently viewing
- Automatic discovery of stacktraces in current screen (only for kitty shell
  since it's based on `kitty @ get-text`, ie the ability of kitty shell to give
  you the content of the current terminal screen)


## Installation

```
git clone github.com/ptbrowne/navstacktrace

# Create symbolic link in a directory contained in your path for
# easy invocation
ln -s $(pwd)/navstacktrace/navstacktrace/navstacktrace.py ~/bin/ss
```

## Usage

```
cd navstacktrace
python navstacktrace/navstacktrace.py sample-stacktrace.txt
```
