
# coding: utf-8

# In[81]:


import json

cuisine_probs = dict() 
ingredient_probs = dict()
ingredient_given_cuisine = dict()
num_ingredient_per_cuisine = dict()

with open("training.json", encoding='utf-8') as ins:
    array = []
    for line in ins:
        array.append(line)
    for elem in array:
        current = json.loads(elem)
        
        #get cuisine probabilities
        c = current['cuisine']
        ingredients = current['ingredients']
        
        if c not in cuisine_probs:
            cuisine_probs[c] = 1/1794
            num_ingredient_per_cuisine[c] = len(ingredients)
        else:
            cuisine_probs[c] += 1/1794
            num_ingredient_per_cuisine[c] += len(ingredients)
            
        
        #get ingredient probabilities
        for i in ingredients:
            if i not in ingredient_probs:
                ingredient_probs[i] = 1/19561
            else:
                ingredient_probs[i] += 1/19561
                
            #get conditional ingredients given cuisine
            if (c,i) not in ingredient_given_cuisine:
                ingredient_given_cuisine[(c,i)] = 1
            else:
                ingredient_given_cuisine[(c,i)] += 1

#calculate conditional probabilities for ingredients given cuisine
for x in ingredient_given_cuisine:
    cuis = x[0]
    num_cuis = num_ingredient_per_cuisine[cuis]
    ingredient_given_cuisine[x] /= num_cuis


    
print(ingredient_given_cuisine)
print(ingredient_probs)
print(cuisine_probs)


# In[106]:

#print(ingredient_given_cuisine)
#print(ingredient_probs)
#print(cuisine_probs)


#calculate cuisine given ingredients
import heapq

ings = ["chicken broth","ground red pepper","hot sauce","monterey jack","quickcooking grits","worcestershire sauce","baking soda","corn oil","food colouring","self rising flour","softened butter","sirloin tip roast","steak","granulated sugar","vegetable shortening"]

cuis_preds = []

for c in cuisine_probs:
    p_cuisine = cuisine_probs[c] #init probability that these ingredients = our cuisine of interest
    
    for ing in ings:
        if ingredient_given_cuisine.get((c,ing)) is None:
            p_cuisine *= 0
            break
        else:
            p_cuisine *= ingredient_given_cuisine.get((c,ing)) 
    heapq.heappush(cuis_preds, (p_cuisine*-100000000000, c))
print(cuis_preds)
    

                
        
    
    


# In[82]:

2/633

