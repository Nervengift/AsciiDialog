#!/usr/bin/env python

import curses.wrapper
import sys
import os
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Shows a message as a pretty ASCII-style ncurses dialog. '
                                                 + 'Optionally make it even prettier with figlet.')
    parser.add_argument('text', metavar='TEXT', type=str, nargs='*', default="-",
                        help='text to show, "-" for stdin')
    parser.add_argument('-c', '--color', dest='color', type=str, default="default", 
                        choices=["green", "red", "blue", "white", "default"],
                        help='foreground color. may be "green", "red", "blue", "white" or "default"')
    parser.add_argument('-f', '--figlet', dest='figlet', action='store_true', 
                        help='run figlet on the input (obviously needs figlet)')
    parser.add_argument('-a', '--figlet-args', dest='fargs', type=str, default="-t", 
                        help='arguments to pass to figlet (defaults to "-t")')
    args = parser.parse_args()

    color = {"default":0, "green":1, "red":2, "blue":3, "white":4}.get(args.color)
    text = process_text_input(args.text, args.figlet, args.fargs)

    return text, color

def process_text_input(text, figlet, fargs):
    if "".join(text) == "-":
        if not sys.stdin.isatty():
            text = sys.stdin.readlines()
            f=open("/dev/tty")             # reopen terminal to connect
            os.dup2(f.fileno(), 0)         # to its input (stdin) (close pipe)
        else:
            text = ['You should give me something to say :P', 'Try "asciidialog -h" for help']
    if figlet:
        text = figletify(" ".join(text), "".join(fargs))
    return text

def figletify(text, args):
    return os.popen("figlet " + args + " " + text).read().strip("\n").split("\n")

class AsciiDialog():

    def __call__(self, stdscr, text, color):
        self.stdscr = stdscr
        curses.curs_set(0)
        self.init_colors()

        self.draw(text, color = curses.color_pair(color))
        stdscr.timeout(-1)
        stdscr.getkey()

    def init_colors(self):
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)

    def draw(self, text, color=0, pw=False):
        length = self.max_length(text) + 6
        row, col = self.center(length, len(text))
        if row < 0 or col < 0:
            sys.stderr.write("Error! Not enough terminal space!")
            sys.exit(1)
        self.stdscr.addstr(row, col, self.gen_top_bottom_border("//", "=", "\\\\", length), color)
        row += 1
        for line in text:
            self.stdscr.addstr(row, col, self.line_border(line.strip("\n"),"|" ,length), color)
            row += 1
        self.stdscr.addstr(row, col, self.gen_top_bottom_border("\\\\", "=", "//", length), color)
        row += 1
        self.stdscr.refresh()

    def max_length(self, lines):
        length = 0
        for line in lines:
            line = line.strip("\n")
            if len(line) > length:
                length = len(line)
        return length

    def gen_top_bottom_border(self, corner_l, border, corner_r, length):
        border = corner_l + ("=" * (length - len(corner_l) - len(corner_r))) + corner_r
        return border

    def line_border(self, line, border, length):
        margin_l = int((length - 2*len(border) - len(line)) / 2)
        margin_r = length - 2*len(border) - len(line) - margin_l
        line = border + (" " * margin_l) + line + (" " * margin_r) + border
        return line

    def center(self, linelength, lines):
        cols = curses.tigetnum('cols')
        rows = curses.tigetnum('lines')
        col = int((cols - linelength) / 2)
        row = int((rows - lines) /2)
        return row, col

if __name__ == "__main__":
    dialog = AsciiDialog()
    text, color = parse_args()
    curses.wrapper(dialog, text, color)
