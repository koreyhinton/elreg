#!/usr/bin/env python3
import sys
import os

def tokenize(s):
    # example:
    #     (?:/|\\)
    #     =>
    #     \\(?:/\\|\\\\\\)
    s = s.replace(")", "elregcloseparen")  # ) => \\)
    s = s.replace("(", "elregopenparen")  # ( => \\(
    s = s.replace("|", "elregpipe")  # | => \\|
    s = s.replace("\\\\", "elregbackslashbackslash")  # \\ => \\\\
    s = s.replace("\\n", "elregbacknewline")  # \n => \n
    s = s.replace("\\.", "elregescapeddot")  # \. => \\.
    s = s.replace("{", "elregopencurly")  # { => \\{
    s = s.replace("}", "elregclosecurly")  # } => \\}
    # print(s, file=sys.stderr)
    return s

def escape_for_elisp(s):
    # example:
    #     (?:/|\\)
    #     =>
    #     \\(?:/\\|\\\\\\)
    s = s.replace("elregcloseparen", "\\\\)")  # ) => \\)
    s = s.replace("elregopenparen", "\\\\(")  # ( => \\(
    s = s.replace("elregpipe", "\\\\|")  # | => \\|
    s = s.replace("elregbackslashbackslash", "\\\\\\\\")  # \\ => \\\\
    s = s.replace("elregbacknewline", "\\n")  # \n => \n
    s = s.replace("elregescapeddot", "\\\\.")  # \. => \\.
    s = s.replace("elregopencurly", "\\\\{")  # { => \\{
    s = s.replace("elregclosecurly", "\\\\}")  # } => \\}
    # print(s, file=sys.stderr)
    #     s = s.replace('(?:', '\\\\(?:')
    #     s = s.replace('(', '\\\\(').replace(')', '\\\\)')
    #     s = s.replace('{', '\\{').replace('}', '\\}')
    #     s = s.replace('\\n', '__NL__')
    #     s = s.replace('\\', '\\\\')
    #     s = s.replace('__NL__', '\\\\n')
    #     s = s.replace('"', '\\"')
    return s # (re-search-backward "\\(?:~\\|\n\\)")

def basename_no_ext(path):
    return os.path.splitext(os.path.basename(path))[0]

def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} app-prefix file1.reg [file2.reg ...]", file=sys.stderr)
        sys.exit(1)

    prefix = sys.argv[1]
    files = sys.argv[2:]

    print(";;; This file is auto-generated by elreg.py")
    print(";;; Do not edit this file manually.\n")

    for filepath in files:
        varname = f"{prefix}-elreg-{basename_no_ext(filepath)}"
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read().strip()
        escaped = escape_for_elisp(tokenize(content))
        print(f'(setq {varname} "{escaped}")\n')

if __name__ == "__main__":
    main()
