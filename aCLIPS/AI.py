#Crystal Gong (cjg5uw) and Cynthia Zheng (xz7uy)

import collections
import re

variables = collections.OrderedDict()
facts = []
rules = collections.OrderedDict()


def parse(condition):
	expression = re.split("([^a-zA-Z_])", condition)
	for i in range(len(expression)):
		if expression[i] in variables:
			if checkFacts(expression[i], False):
				expression[i] = 'True'
			else:
				expression[i] = 'False'

	joinedValid = (''.join(expression)).replace('!', ' not ').replace('|', ' or ').replace('&', ' and ')
	return eval(joinedValid)

def add_definition(name, definition, root):
	variables[name] = [definition, root]

def List(variables, facts, rules):
	# print root vars
	print("Root Variables: ")
	for key, value in variables.items():
		if value[1]:
			print("\t{} = {}".format(key, value[0]))

	# print learned vars
	print("\nLearned Variables: ")
	for key, value in variables.items():
		if not value[1]:
			print("\t{} = {}".format(key, value[0]))

	# print facts
	print("\nFacts: ")
	for fact in facts:
		print("\t{}".format(fact))	

	# print Rules
	print("\nRules: ")
	for key, values in rules.items():
		for v in values:
			print("\t{} -> {}".format(key, v))	

def createNewRule(lhs, rhs): 
	lhsIsValid = True
	vars = re.split("[^a-zA-Z_]", lhs)
	vars = filter(None, vars)

	#see if all the vars are in variables. if one of them isn't, valid evaluates to False.
	for v in vars:
		if v not in variables:
			lhsIsValid = False

	#actually put the rule in the dict
	if lhsIsValid and rhs in variables and not variables[rhs][1]: #if both these variables are defined and rhs is a learned variable
		if lhs in rules and rhs not in rules[lhs]: #if lhs is already a key and rhs is not already a value for it
			rules[lhs].append(rhs)
		else: #lhs is not already a key
			rules[lhs] = []
			rules[lhs].append(rhs)

def Learn():
	operand = ""

	addedSomething = True
	while addedSomething:
		addedSomething = False
		for condition, result in rules.items():
			operand = parse(condition)

			if operand:# and result not in facts:
				for r in result:
					if r not in facts:
						facts.append(r)
						addedSomething = True			

def exp2Words(expression):
	expression = re.split("([^a-zA-Z_])", expression)
	for i in range(len(expression)):
		if expression[i] in variables:
			expression[i] = variables[expression[i]][0]
			if "\"" in expression[i]: #if there are quotes around it, remove the quotes
				expression[i] = expression[i][1:-1]
			
	joinedValid = (''.join(expression)).replace('!', ' NOT ').replace('|', ' OR ').replace('&', ' AND ')
	return joinedValid

def Query(goal, original, why):
	expression = re.split("([^a-zA-Z_])", goal)
	for i in range(len(expression)):
		if expression[i] in variables:
			if checkFacts(expression[i], why):
				expression[i] = 'True'				
			else:
				expression[i] = str(backChain(expression[i], original, why))
	
	joinedValid = (''.join(expression)).replace('!', ' not ').replace('|', ' or ').replace('&', ' and ')
	retval= eval(joinedValid)

	if goal == original:
		if retval:
			if why: print("I THUS KNOW THAT {}".format(exp2Words(goal)))
			else: print('true')

		else:
			if why: print("THUS I CANNOT PROVE {}".format(exp2Words(goal)))
			else: print('false')

	return str(retval)

def checkFacts(goal, why): #only ever take a single var
	if goal in facts:
		if why: print("I KNOW THAT {} ".format(exp2Words(goal)))
		return True
	else: return False
	
def backChain(goal, original, why): #goal is only ever a single var, never an expression
	found = False
	#look for goal in rules
	for key, values in rules.items():
		if goal in values: #if you find it
			found = True
			retval = Query(key, original, why)

			if why: print("BECAUSE {}{} {}{}".format(("" if eval(retval) else "IT IS NOT TRUE THAT "), exp2Words(key), ("I KNOW THAT " if eval(retval) else "I CANNOT PROVE "), exp2Words(goal))) #I KNOW THAT/I CANNOT PROVE)
	if not found:
		retval = False

		if why: print("I KNOW IT IS NOT TRUE THAT {}".format(exp2Words(goal)))

	return retval

def Why(goal):
	Query(goal, goal, False)
	Query(goal, goal, True)
	
def editFact(var, truthVal):
	if var not in variables:
		print("variable not defined")
	elif variables[var][1] is False: #if not a root var
		print("You cannot set the truth value of learned variable")
	else: #okay to set
		if truthVal == "true":
			if var not in facts:
				facts.append(var)
		elif truthVal == "false":
			if var in facts:
				facts.remove(var)
		for fact in facts:
			if variables[fact][1] == False: #for any learned variables in facts
				facts.remove(fact) #remove it from the fact list


def main():

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
				string = s.split(" = ")
				if(inp[2] not in variables):
					if(inp[1] == "-R"):
						add_definition(inp[2], string[1], True)
					else:
						add_definition(inp[2], string[1], False)

		elif inp[0] == "List":
			List(variables, facts, rules)
		elif inp[0] == "Learn":
			Learn()
		elif inp[0] == "Query":
			Query(inp[1], inp[1], False)
		elif inp[0] == "Why":
			Why(inp[1])


if __name__ == "__main__":
    main()
