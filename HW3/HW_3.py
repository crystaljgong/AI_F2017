#Crystal Gong(cjg5uw), Cynthia Zheng(xz7uy)
import collections
import numpy as np
from itertools import product


def main():
	###EDIT CASE HERE###
	case = 2
	###EDIT CASE HERE###

	pts = np.zeros((7,7))

	iters = 0
	modified = True
	neighborVal = 0

	#these are in x, y, which is opposite from the (i, j) which goes row, column
	#0 down, 1 downright, 2 right, 3 upright, 4 up, 5 upleft, 6 left, 7 downleft, 8 down, 9 downright, 10 right
	allNeighbors = [[0, 1], [1,1], [1,0], [1,-1], [0,-1], [-1, -1], [-1, 0], [-1, 1], [0, 1], [1,1], [1,0]]
      
	while iters <= 1000 and modified:
	    iters += 1
	    modified = False

	    for i, j in product(range(7), range(7)):
   	    	reward = -1
   	    	if i == 3 and j == 6:
   	    		reward = 0

        	maxAction = pts[i,j]

        	#top row
        	if i == 0:
        		#top middle
        		if j != 0 and j != 6: #left, downleft, down, downright, right
        			neighbors = allNeighbors[6:]
        		#top left
        		if j == 0: #down, downright, 
        			neighbors = allNeighbors[:3]
        		#top right
        		if j == 6: #left, downleft, down
        			neighbors = allNeighbors[6:9]
        		
        	#bottom row
        	elif i == 6:
        		#bottom middle
        		if j != 0 and j != 6: #right, upright, up, upleft, left
        			neighbors = allNeighbors[2:7]
        		#bottom left
        		if j == 0: #right, upright, up
        			neighbors = allNeighbors[2:5]
        		#bottom right
        		elif j ==6:  #up, upleft, left
        			neighbors = allNeighbors[4:7]

        	#middle rows
        	else: #i != 0 and != 6
        		#properly in the middle
        		if j != 0 and j != 6:
        			neighbors = allNeighbors[:8]
        		#left side
        		if j == 0:
        			neighbors = allNeighbors[:5]
        		#right side
        		elif j == 6:
        			neighbors = allNeighbors[4:9]
        	
        	
        	#calculate s'
    		for n in neighbors: 
    			col = j + n[0]
    			row = i + n[1]
    				
    			if case == 3:
    				if j > 2 and j < 6: #between 3 and 5
    					print("case 3")
    					row = i + n[1] - 2
    					if row < 0:
							row = 0

    			if case == 2:
					if j > 2 and j < 6: #between 3 and 5
						print("case 2")
						row = i + n[1] - 1
						if row < 0:
							row = 0
    			
    			neighborVal = pts[row, col]

    			if neighborVal > maxAction:
    				maxAction = neighborVal

        	#if the difference between the current utility of the state and the new utility of the state >= 0.001
		if abs(pts[i,j]-(reward + maxAction)) >= 0.001:
			# update the utility of the state
			pts[i,j] = reward + maxAction
			modified = True

	print(pts)

if __name__ == "__main__":
    main()
