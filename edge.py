#!/usr/bin/env python3

from sys import argv, stdout
from PIL import Image

R = 0
G = 1
B = 2

def normal(x):
	return x / 3060

def find_edges(img, intensity):
	size = img.size
	ret = Image.new('RGB', size)
	ret_pm = ret.load()
	progress = 0
	for i in range(size[0]):
		for j in range(size[1]):
			try:
				t, b = img.getpixel((i, j - 1)), img.getpixel((i, j + 1))
				l, r = img.getpixel((i - 1, j)), img.getpixel((i + 1, j))
				tl, tr = img.getpixel((i - 1, j - 1)), img.getpixel((i + 1, j - 1))
				bl, br = img.getpixel((i - 1, j + 1)), img.getpixel((i + 1, j + 1))
				diff_v = sum([abs(t[x] - b[x]) for x in range(3)])
				diff_h = sum([abs(l[x] - r[x]) for x in range(3)])
				diff_d1 = sum([abs(tl[x] - br[x]) for x in range(3)])
				diff_d2 = sum([abs(tr[x] - bl[x]) for x in range(3)])
				diff = diff_v + diff_h + diff_d1 + diff_d2
				diff = round(normal(diff) * intensity, 2) 				# normalizing to make a ratio (a value b/w 0 and 1)
				r, g, b = img.getpixel((i, j))
				ret_pm[i, j] = min(int(r * diff), 255), min(int(g * diff), 255), min(int(b * diff), 255)

			except IndexError:
				ret_pm[i, j] = 0, 0, 0
			progress = ((i * size[1] + j) / (size[0] * size[1])) * 100
			stdout.write("\rProgress: %.2f%%" % progress)
			stdout.flush()
	print("\nDone!")
	return ret

if len(argv) == 1:
	print("Use: ./edge <path/input_image.extension> <path/output_image.extension> <highlighting intensity[normal:1]>")
	response = input("Process test image? (Y/n) ")
	if response.upper() != "Y":
		exit()
	image = Image.open("test.jpg").convert('RGB')
	op = "res.png"
	intensity = 8
	print('''
input image = test.jpg
output image = res.png
highlighting intensity = 8''')

else:
	image = Image.open(argv[1]).convert('RGB')
	op = argv[2]
	intensity = float(argv[3])

rgb = image.convert('RGB')

res = find_edges(image, intensity)
res.save(op)
