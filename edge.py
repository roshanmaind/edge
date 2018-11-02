#!/usr/bin/env python3

from sys import argv
from PIL import Image

if len(argv) == 1:
	print(open("usage.txt", 'r').read())
