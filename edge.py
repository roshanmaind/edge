#!/usr/bin/env python3

from sys import argv, stdout
from PIL import Image

R = 0
G = 1
B = 2

def find_edges(img):
	size = img.size
	ret = Image.new('RGB', size)
	ret_pm = ret.load()
	progress = [0, "000"]
	for i in range(size[0]):
		for j in range(size[1]):
			try:
				t, b = img.getpixel((i, j - 1)), img.getpixel((i, j + 1))
				l, r = img.getpixel((i - 1, j)), img.getpixel((i + 1, j))
				diff_v = sum([abs(t[i] - b[i]) for i in range(3)])
				diff_h = sum([abs(l[i] - r[i]) for i in range(3)])
				diff = diff_v + diff_h
				diff = diff / 1530 				# normalizing to make a ratio (a value b/w 0 and 1)
				r, g, b = img.getpixel((i, j))
				ret_pm[i, j] = int(r * diff), int(g * diff), int(b * diff)

			except IndexError:
				ret_pm[i, j] = 0, 0, 0
			progress[0] = ((i * size[1] + j) / (size[0] * size[1])) * 100
			progress[1] = ("0" * (3 - len(str(progress[0])))) + str(progress[0])
			stdout.write("Progress: %s%%   \r" % progress[1])
			stdout.flush()


	return ret

if len(argv) == 1:
	print("Use: ./edge <path/input_image.extension> <path/output_image.extension>")
	image = Image.open("test.jpg").convert('RGB')
	op = "res.png"
else:
	image = Image.open(argv[1]).convert('RGB')
	op = argv[2]

rgb = image.convert('RGB')

res = find_edges(image)
res.save(op)
