import collections

variables = collections.OrderedDict()
facts = []
rules = collections.OrderedDict()

def add_definition(name, definition, root, fact):
	variables[name] = [definition, root, fact]
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
		if not value[1]:
			print("    {} = {}".format(key, value[0]))

	#print facts
	print("Facts")
	for fact in facts:
		print("    {}".format(fact))	

	#print Rules
	print("Rules")
	for key, values in rules.items():
		for v in values:
			print("    {} -> {}".format(key, v))	

def createNewRule(lhs, rhs): #TODO: fix this so it deals with complex expressions A&B|!C
	if lhs in variables and rhs in variables: #if both these variables are defined
		if lhs in rules and rhs not in rules[lhs]: #if lhs is already a key and rhs is not already a value for it
			rules[lhs].append(rhs)
		else: #lhs is not already a key
			rules[lhs] = []
			rules[lhs].append(rhs)

def Learn():
	for condition, result in rules.items():
		#fix this to work with parenthesis etc
		if condition and result not in facts: 
			facts.append(result)

def Query(goal):
	#TRY TO PROVE IT
	#goal is in list of facts
	found = False
	foundKey = ''
	if goal in facts:
		print("true")
		foundKey = goal
	#backwards chaining
	else: #look for antecedetnt in rules
		for key, values in rules.items():
			if goal in values: #if you find it
				print("key: {}, value: {}".format(key, goal))
				found = True
				foundKey = Query(key)
		if not found:
			print("false")

	print("foundKey: {}".format(foundKey))
	return foundKey

def Why(goal):
	Query(goal)
	

def editFact(var, truthVal):
	if var not in variables:
		print("variable not defined")
	elif variables[var][1] is False: #if not a root var
		print("You cannot set the truth value of learned variable")
	else: #okay to set
		if truthVal == "true":
			variables[var][2] = True
			facts.append(var)
		elif truthVal == "false":
			#variables[var][2] = False
			variables[var][2]
			facts.remove(var)
		for fact in facts:
			if variables[fact][1] == False: #for any learned variables in facts
				variables[fact][1] == False #set that learned variable to false
				facts.remove(fact) #and remove it from the fact list



def main():

	add_definition("S", "\"Sam likes ice cream\"", True, True)
	add_definition("V", "\"Today is Sunday\"", True, False)
	add_definition("Test", "Test", False, False)
	createNewRule("S", "V")

	while(True):
		s = input('Enter a command: ')
		inp = s.split()

		if inp[0] == "Teach":
			#Teach S = true
			if inp[2] == "=":
				editFact(inp[1], inp[3])
			#Teach a rule
			elif inp[2] == "->":
				createNewRule(inp[1], inp[3])
			#Teach -R S = "Blah"
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
			Query(inp[1])
		elif inp[0] == "Why":
			Why(inp[1])




if __name__ == "__main__":
    main()