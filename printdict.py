#!/usr/bin/python
import sys
last = 0
with open(sys.argv[1],"r") as f:
	for line in f:
		items = line.split()
		if(len(items)>2):
			print(items[0] + ':' + items[1] + ':' + str(last))
			last+= int(items[2])
