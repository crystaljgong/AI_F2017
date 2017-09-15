def main():
   s = input('Enter a command: ')
   input = s.split()

   if input[0] == "Teach":
       if input[2] == "=":
           if input[1] in facts: #?learned var?
                print("Error: cannot set a learned variable directly")
           else:
           # observeRootVar(input[1], input[3])
                facts.append(input[1])
       elif input[2] == "->":
           if input[3] in facts:
            # createNewRule(input[1], input[3])

       else:
           string = s.split("=")
           add_definition(input[2], string[1], input[1], false) #root is ARG?


    elif input[0] == "List":
        List()
    elif input[0] == "Learn":
        # Learn()
    elif input[0] == "Query":
        # Query(input[1])
    elif input[0] == "Why":
        # Why(input[1])

    
