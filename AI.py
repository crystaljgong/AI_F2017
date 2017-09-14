import collections

variables = collections.OrderedDict()
facts = []
rules = []

def add_definition(name, definition, root, fact):
	variables[name] = (definition, root, fact)

def List(variables, facts, rules):
	#print root vars
	print("Root Variables")
	for key, value in variables.iteritems():
		if value[1]:
			print("    {} = {}".format(key, value[0]))

	#print learned vars
	#this not v efficient b/c looping twice but whatever
	print("Learned Variables")
	for key, value in variables.iteritems():
		poop = []
		if not value[1]:
			print("    {} = {}".format(key, value[0]))

	#print facts
	print("Facts")
	for fact in facts:
		print("    {}".format(fact))	

	#print Rules
	print("Rules")
	for rule in rules:
		print("    {}".format(rule))	




def main():
	add_definition("S", "Sam likes ice cream", True, True)
	add_definition("V", "Today is Sunday", True, True)
	add_definition("EAT", "Sam will eat ice cream", False, True)
	add_definition("F", "Python is fun", False, True)

	#somehow only let this append a fact if the key exists in variables
	facts.append("S")
	facts.append("V")
	facts.append("EAT")
	facts.append("F")

	rules.append("S&V -> EAT")

	List(variables, facts, rules)


if __name__ == "__main__":
    main()