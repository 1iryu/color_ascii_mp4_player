import os
import sys
import time


class Reprint():
    def __init__(self):
        self.first = False
        self.lines_length = 0
        os.system("")

    def cursor_up(self, length: int):
        print("\033[F" * length, end="")

    def cursor_down(self, length: int):
        print("\n" * length, end="")

    def do(self, list_text: list):
        if(self.first == False):
            self.first = True
            self.lines_length = len(list_text)
            for text in list_text:
                print(text)
        if self.lines_length == len(list_text):
            list_text.reverse()
            for i in range(len(list_text)):
                self.cursor_up(i+1)
                print(list_text[i], end="")
                self.cursor_down(i+1)
        else:
            print("It's not the same as the number on the first list you gave you.")
