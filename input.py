def main():
	s = input('Enter a command: ')
	input = s.split()

	if input[0] == "Teach":
		if input[2] == "=":
			if input[1] in facts:
				print("Error: cannotset a learned variable directly")
			else:
				#observeRootVar(input[1], input[3])
				facts.append(input[1])
		elif input[2] == "->":
			if input[3] in facts:
				print("ah")
				#createNewRule(input[1], input[3])
		else:
			string = s.split("=")
			add_definition(input[2], string[1], input[1], false)

	elif input[0] == "List":
		List()
	elif input[0] == "Learn":
		print("Learn()")
	elif input[0] == "Query":
		print("#Query(input[1])")
	elif input[0] == "Why":
		print("#Why(input[1])")
    
