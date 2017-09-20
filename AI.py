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

def createNewRule(lhs, rhs): #TODO: fix this so it deals with complex expressions A&B|!C
	if lhs and rhs in variables:
		rules[lhs] = rhs

def Learn():
	listOperator = []
	listOperand = []
	temp = ""
	for condition, result in rules.items():
		for i in condition: # add to 2 lists
			if i.isalpha() or i == '_':
				temp += i
			elif i == '!' or i == '&' or i == '|' and listOperator.count() == 0:
				if temp != "": # append operand
					listOperand.append(temp)
					temp = ""
				listOperator.append(i)
			elif i == '(' or i == '!':
				if temp != "": # append operand
					listOperand.append(temp)
					temp = ""
				listOperator.append(i)
			elif i == ')':
				if temp != "": # append operand
					listOperand.append(temp)
					temp = ""
				while listOperator[len(listOperator)-1] == '(':
					operator = listOperator.pop()
			
					if operator == '!':
						operand1 = listOperand.pop()
						listOperand.append(not variables[operand1][1]) # append true or false to operand list

					elif operator == '|':
						operand1 = listOperand.pop()
						operand2 = listOperand.pop()
						listOperand.append(variables[operand1][1] or variables[operand2][1])
					else:
						operand1 = listOperand.pop()
						operand2 = listOperand.pop()
						listOperand.append(variables[operand1][1] and variables[operand2][1])
				listOperator.pop()
			elif i == '&' or i == '|':
				if operator == '|':
					operand1 = listOperand.pop()
					operand2 = listOperand.pop()
					listOperand.append(variables[operand1][1] or variables[operand2][1])
				else:
					operand1 = listOperand.pop()
					operand2 = listOperand.pop()
					listOperand.append(variables[operand1][1] and variables[operand2][1])
		
		while(listOperator.count()>0):
			operator = listOperator.pop()
			
			if operator == '!':
				operand1 = listOperand.pop()
				listOperand.append(not variables[operand1][1]) # append true or false to operand list

			elif operator == '|':
				operand1 = listOperand.pop()
				operand2 = listOperand.pop()
				listOperand.append(variables[operand1][1] or variables[operand2][1])
			else:
				operand1 = listOperand.pop()
				operand2 = listOperand.pop()
				listOperand.append(variables[operand1][1] and variables[operand2][1])
		
		if listOperand.count() == 1:
			operand = listOperand.pop()
		#fix this to work with parenthesis etc
		if variables[operand][1] and result not in facts:
			facts.append(result)

def Query(goal):
	#TRY TO PROVE IT
	#goal is in list of facts
	if goal in facts:
		print("true")
	#backwards chaining
	else: #look for antecedetnt in rules
		for key, value in rules.items():
			if value == goal: #if you find it
				print("key: {}, value: {}".format(key, value))
				Query(key)
				#if key in facts:
				#	print("{} is in facts and {} -> {}, therefore {} is true".format(key, key, value, value))

	#if goal is not in facts, #look for antecedent in rules
			#if you find antecedent
				#TRY TO PROVE IT
				#try to look for antecedent in facts
					#if found, goal is true
					#if not found, look for antecedent in rules

			#if you don't find antecedent
				#cannot prove rule
	

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
			print("#Why(inp[1])")




if __name__ == "__main__":
    main()