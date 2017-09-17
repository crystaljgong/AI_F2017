import collections

variables = collections.OrderedDict()
facts = []
rules = collections.OrderedDict()

def add_definition(name, definition, root, fact):
	variables[name] = (definition, root, fact)
	if fact:
		facts.append(name)

def List(variables, facts, rules):
	#print root vars
	print("Root Variables")
	for key, value in variables.items():
		if value[1]:
			print("    {} = {}".format(key, value[0]))

	#print learned vars
	#this not v efficient b/c looping twice but whatever
	print("Learned Variables")
	for key, value in variables.items():
		poop = []
		if not value[1]:
			print("    {} = {}".format(key, value[0]))

	#print facts
	print("Facts")
	for fact in facts:
		print("    {}".format(fact))	

	#print Rules
	print("Rules")
	for key, value in rules.items():
		print("    {} -> {}".format(key, value))	

def createNewRule(lhs, rhs):
	print("creating new rule")
	rules[lhs] = rhs

def Learn():
	for condition, result in rules.items():
		#fix this to work with parenthesis etc
		if condition:
			facts.append(result)



def main():

	add_definition("S", "\"Sam likes ice cream\"", True, True)
	add_definition("V", "\"Today is Sunday\"", True, False)
	createNewRule("S", "V")

	while(True):
		s = input('Enter a command: ')
		inp = s.split()

		if inp[0] == "Teach":
			if inp[2] == "=":
				if inp[1] in facts:
					print("Error: cannot set a learned variable directly")
				else:
					#observeRootVar(inp[1], inp[3])
					facts.append(inp[1])
			elif inp[2] == "->":
				if inp[1] and inp[3] in variables:
					createNewRule(inp[1], inp[3])
			else:
				string = s.split("=")
				if(inp[2] not in variables):
					if(inp[1] == "-R"):
						add_definition(inp[2], string[1], True, False)
					else:
						add_definition(inp[2], string[1], False, False)

		elif inp[0] == "List":
			List(variables, facts, rules)
		elif inp[0] == "Learn":
			Learn()
		elif inp[0] == "Query":
			print("#Query(inp[1])")
		elif inp[0] == "Why":
			print("#Why(inp[1])")




if __name__ == "__main__":
    main()