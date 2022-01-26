import os
import random
import textfile_editor

os.system('')


def rgb(x, y, z):
	return f'\x1b[38;2;{x};{y};{z}m'


def print_with_color(text: str, x, y, z):
	value = rgb(x, y, z)
	print(f"{value}" + text , end="")


def return_color_text_string(text: str, x, y, z):
	value = rgb(x, y, z)
	return(value + text)


def raw(_text):
	return r'{}'.format(_text)





