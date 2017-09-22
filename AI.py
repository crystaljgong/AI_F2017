import collections
import re

variables = collections.OrderedDict()
facts = []
rules = collections.OrderedDict()


def parse(condition):
	temp = ""
	listOperator = []
	listOperand = []
	operand = ""

	for i in condition:  # add to 2 lists
			# print("operands: {}".format(listOperand))
			# print("operators: {}".format(listOperator))
			# print("condition: " + condition)
		if i.isalpha() or i == '_':
			temp += i

		elif (i == '&' or i == '|'):
			if temp != "":  # append operand
				listOperand.append(variables[temp][1])
				temp = ""

			if len(listOperator) == 0 or listOperator[-1] == '(':
				listOperator.append(i)

			elif i == '&' and (listOperator[-1] != '!' or listOperator[-1] != '&'):
				listOperator.append(i)
			elif i == '&' and (listOperator[-1] == '!' or listOperator[-1] == '&'):
				operand1 = listOperand.pop()
				operand2 = listOperand.pop()
				operator1 = listOperator.pop()
				joinedValid = (''.join((str(operand1), operator1, str(operand2)))).replace('!', ' not ').replace('|', ' or ').replace('&', ' and ')
				listOperand.append(joinedValid)
				listOperator.append(i)
			elif i == '|' and (listOperator[-1] == '|' or listOperator[-1] == '&' or listOperator[-1] == '!'):
				operand1 = listOperand.pop()
				operand2 = listOperand.pop()
				operator1 = listOperator.pop()			
				joinedValid = (''.join((str(operand1), operator1, str(operand2)))).replace('!', ' not ').replace('|', ' or ').replace('&', ' and ')		
				listOperand.append(joinedValid)
				listOperator.append(i)
		elif i == '(' or i == '!':
			if temp != "":  # append operand
				listOperand.append(variables[temp][1])
				temp = ""
			listOperator.append(i)
		elif i == ')':
			if temp != "":  # append operand
				listOperand.append(variables[temp][1])
				temp = ""
			while listOperator[-1] != '(':
				operator = listOperator.pop()

				if operator == '!':
					operand1 = listOperand.pop()
					listOperand.append(not operand)  # append true or false to operand list

				elif operator == '|':
					operand1 = listOperand.pop()
					operand2 = listOperand.pop()
					listOperand.append(operand1 or operand2)
				else:
					operand1 = listOperand.pop()
					operand2 = listOperand.pop()
					listOperand.append(operand1 and operand2)
			listOperator.pop()


		if temp != "": # append operand
			listOperand.append(variables[temp][1])
			temp = ""
		
		while(len(listOperator) > 0):
			operator = listOperator.pop()
			
			if operator == '!':
				operand1 = listOperand.pop()
				if operand1 == 'True':
					listOperand.append('False') # append true or false to operand list
				elif operand1 == 'False':
					listOperand.append('True')
				else: 
					listOperand.append(not operand1)

			elif operator == '|':
				operand1 = listOperand.pop()
				operand2 = listOperand.pop()
				listOperand.append(operand1 or operand2)
			else:
				operand1 = listOperand.pop()
				operand2 = listOperand.pop()
				listOperand.append(operand1 and operand2)
		
		if temp != "":
			operand = variables[temp][1]
			temp = ""
			

		if len(listOperand) == 1:
			operand = listOperand.pop()
		return operand

def add_definition(name, definition, root, fact):
	variables[name] = [definition, root, fact]
	if fact:
		facts.append(name)

def List(variables, facts, rules):
	# print root vars
	print("Root Variables")
	for key, value in variables.items():
		if value[1]:
			print("    {} = {}".format(key, value[0]))

	# print learned vars
	# this not v efficient b/c looping twice but whatever
	print("Learned Variables")
	for key, value in variables.items():
		if not value[1]:
			print("    {} = {}".format(key, value[0]))

	# print facts
	print("Facts")
	for fact in facts:
		print("    {}".format(fact))	

	# print Rules
	print("Rules")
	for key, values in rules.items():
		for v in values:
			print("    {} -> {}".format(key, v))	

def createNewRule(lhs, rhs): #TODO: fix this so it deals with complex expressions A&B|!C
	lhsIsValid = True
	vars = re.split("[^a-zA-Z_]", lhs)
	print("split: {}".format(vars))
	#see if all the vars are in variables. if one of them isn't, valid evaluates to False.
	for v in vars:
		if v not in variables:
			lhsIsValid = False

	#actually put the rule in the dict
	if lhsIsValid and rhs in variables: #if both these variables are defined
		if lhs in rules and rhs not in rules[lhs]: #if lhs is already a key and rhs is not already a value for it
			rules[lhs].append(rhs)
		else: #lhs is not already a key
			rules[lhs] = []
			rules[lhs].append(rhs)

def Learn():
	operand = ""
	for condition, result in rules.items():
		operand = parse(condition)

		if operand and result not in facts:
			for r in result:
				if r not in facts:
					facts.append(r)

def Query(goal, original):
	expression = re.split("([^a-zA-Z_])", goal)
	#print("expression before parsing: {}".format(expression))
	for i in range(len(expression)):
		#print(expression[i])
		if expression[i] in variables:
			#print("expression[i] in variables: {}".format(expression[i]))
			if checkFacts(expression[i]):
				expression[i] = 'True'				
			else:
				expression[i] = str(backChain(expression[i], original))
			#print("expression[i] value {}".format(expression[i]))
	#print("expression after parsing: {}".format(expression))

	joinedValid = (''.join(expression)).replace('!', ' not ').replace('|', ' or ').replace('&', ' and ')
	#print("joinedValid: {}".format(joinedValid))
	retval= eval(joinedValid)

	if goal == original:
		if retval:
			print('true')
		else:
			print("I THUS CANNOT PROVE ")
			print('false')

	return str(retval)

def checkFacts(goal): #only ever take a single var
	if goal in facts:
		#print("{} is in facts".format(goal))
		print("I KNOW THAT {} ".format(variables[goal][0]))
		return True
	

def backChain(goal, original): #goal is only ever a single var, never an expression
	found = False
	# backwards chaining
	#look for goal in rules
	#print("{} is not in facts. looking for a rule to prove it...".format(goal))
	for key, values in rules.items():
		if goal in values: #if you find it
			#print("found a matching rule! key: {}, value: {}".format(key, goal))
			found = True
			retval = Query(key, original)
			print("BECAUSE {}{}".format("" if retval else "IT IS NOT TRUE THAT ", variables[goal][0]))
	if not found:
		#print("could not prove {}".format(goal))
		print("I CANNOT PROVE {}".format(variables[goal][0]))
		retval = False

	return retval


def Why(goal):
	Query(goal)

	#True or False
	#if true:

		#if in facts
			#I KNOW THAT ...

		#if there is rule (use the fact to find the rule)
			#BECAUSE ... I KNOW THAT ...

		#if goal contains & or | or ! (spell out the input)
			#I THUS KNOW THAT ... AND ...
			#I THUS KNOW THAT ... OR ...
			#I THUS KNOW THAT ... NOT ...

	#else:
		#I KNOW IT IS NOT TRUE THAT ...
		#BECAUSE IT IS NOT TRUE THAT ... I CANNOT PROVE ...
		#THUS I CANNOT PROVE ... AND ...
	

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
			# variables[var][2] = False
			variables[var][2]
			facts.remove(var)
		for fact in facts:
			if variables[fact][1] == False: #for any learned variables in facts
				variables[fact][1] == False #set that learned variable to false
				facts.remove(fact) #and remove it from the fact list



def main():

	add_definition("S", "\"Sam likes ice cream\"", True, True)
	add_definition("V", "\"Today is Sunday\"", True, False)
	add_definition("Test", "This is Test", False, False)
	createNewRule("S", "V")

	while(True):
		s = input('Enter a command: ')
		inp = s.split()

		if inp[0] == "Teach":
			# Teach S = true
			if inp[2] == "=":
				editFact(inp[1], inp[3])
			# Teach a rule
			elif inp[2] == "->":
				createNewRule(inp[1], inp[3])
			# Teach -R S = "Blah"
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
			Query(inp[1], inp[1])
		elif inp[0] == "Why":
			Why(inp[1])




if __name__ == "__main__":
    main()
