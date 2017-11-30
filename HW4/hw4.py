
# coding: utf-8

# In[2]:

import random
import json
import math

with open("training.json", encoding='utf-8') as ins:
    array = []
    for line in ins:
        array.append(line)

#shuffle array in place
random.shuffle(array)


# In[3]:

def count_num_ingredients(dataset):
    count = 0
    for elem in dataset:
        current = json.loads(elem)
        count += len(current['ingredients'])
    return count


# In[4]:

def predict_cuisine(ingredients): 
    #calculate cuisine given ingredients
    import heapq

    cuis_preds = []

    for c in cuisine_probs:
        p_cuisine = math.log(cuisine_probs[c]) #init probability that these ingredients = our cuisine of interest
        #p_cuisine = cuisine_probs[c] #init probability that these ingredients = our cuisine of interest
        #print("cuisine is {}".format(c))
        for ing in ingredients:
            #print("ingredients is {}".format(ingredients))
            if ingredient_given_cuisine.get((c,ing)) is None:
                ##PERHAPS DO LAPLACE SMOOTHING HERE INSTEAD
                #https://stats.stackexchange.com/questions/108797/in-naive-bayes-why-bother-with-laplacian-smoothing-when-we-have-unknown-words-i
                p_cuisine += math.log(0.00000000000000000001) #a hacky way to do laplace smoothing
                #p_cuisine *= 0.00000000000000000000001 #a hacky way to do laplace smoothing
                #print("{} given {} not there".format(c, ing))
            else:
                #print("{} given {} there".format(c, ing))
                p_cuisine += math.log(ingredient_given_cuisine.get((c,ing))) #use log numbers don't get too small
                #p_cuisine *= ingredient_given_cuisine.get((c,ing)) #use log numbers don't get too small
                #log(Prob(Ci)) + log(Prob(T1|Ci)) + log(Prob(T2|Ci)) + ... + log(Prob(Tm|Ci))
        heapq.heappush(cuis_preds, (p_cuisine*-1, c))
    #print("\n")
    #print(cuis_preds)
    return cuis_preds[0][1], cuis_preds


# In[5]:

def get_accuracy(validation):

    total = len(validation)
    incorrect = 0
    correct = 0
    for item in validation:
        current = json.loads(item)
        prediction, cuisine_preds = predict_cuisine(current['ingredients'])
        if prediction != current['cuisine']:
            incorrect += 1
            #print(cuisine_preds)
            #print("prediction: {}".format(prediction))
            #print("actual: {}\n".format(current['cuisine']))
            #print(current['ingredients'])

        else:
            correct += 1

    accuracy = correct*100/total
    print("correct: {}".format(correct))
    print("incorrect: {}".format(incorrect))
    print("accuracy = {}".format(accuracy))
    print("error: {}".format(100-accuracy))
    return accuracy


# In[8]:

accuracies = list()
len_data = len(array)

#6 fold
for iteration in range(0,6):
    cuisine_probs = dict() #p(c)
    ingredient_probs = dict() #p(i)
    ingredient_given_cuisine = dict() #p(i|c)
    num_ingredient_per_cuisine = dict() # #i/c
    
    a = int(len_data/6*iteration)
    b = int(len_data/6*(iteration+1))

    validation = array[a:b]
    training = array[b:]+array[:a]

    num_ingredients = count_num_ingredients(training)
    
    for elem in training:
        current = json.loads(elem)
        #print("current: {}".format(current))
        #get cuisine probabilities
        c = current['cuisine']
        ingredients = current['ingredients']
        #print(ingredients)

        #get cuisine probabilities (cuisine_probs)
        if c not in cuisine_probs:
            cuisine_probs[c] = 1/len(training)
            num_ingredient_per_cuisine[c] = len(ingredients)
        else:
            cuisine_probs[c] += 1/len(training)
            num_ingredient_per_cuisine[c] += len(ingredients)


            #get ingredient probabilities (ingredient_probs)
        for i in ingredients:
            if i not in ingredient_probs:
                ingredient_probs[i] = 1/num_ingredients
            else:
                ingredient_probs[i] += 1/num_ingredients

                #get conditional ingredients given cuisine 
            if (c,i) not in ingredient_given_cuisine:
                ingredient_given_cuisine[(c,i)] = 1
            else:
                ingredient_given_cuisine[(c,i)] += 1

    #calculate conditional probabilities for ingredients given cuisine (ingredient_given_cuisine)
    for x in ingredient_given_cuisine:
        cuis = x[0]
        num_cuis = num_ingredient_per_cuisine[cuis]
        ingredient_given_cuisine[x] /= num_cuis
        
    #model complete! time to validate
    print(iteration)
    count = 0
    
    accuracies.append(get_accuracy(validation))

    #print("ingredient given cuisine (curry, indian): {}".format(ingredient_given_cuisine[('indian', 'curry leaves')]))
    #print("ingredient prob curry leaves: {} ".format(ingredient_probs['curry leaves']))
    #print("cuisine prob indian: {}".format(cuisine_probs['indian']))

average_error = sum([(100-i) for i in accuracies])/len(accuracies)
print(average_error)


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



