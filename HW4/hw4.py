# Cynthia Zheng(xz7uy), Crystal Gong(cjg5uw)

import json

with open("training.json", encoding='utf-8') as ins:
	array = []
	for line in ins:
		array.append(line)
	for elem in array:
		current = json.loads(elem)
		#print(current)
