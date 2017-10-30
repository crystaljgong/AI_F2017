#Crystal Gong(cjg5uw), Cynthia Zheng(xz7uy)
import collections
import numpy as np


def main():
    matrix = [[0 for x in range(7)] for y in range(7)] # initialize matrix
    points = collections.OrderedDict() # dictionary of points

    for y in range(7):
        # initialize dictionary
        for x in range(7):
            points[y, x] = 0

    # calculate the utility of each state
    iters = 0
    modified = True

    while iters <= 1000 and modified:
        iters += 1
        modified = False
        reward = -1

        for p in points:

            reward = -1

            maxAction = points[p]

            if p[0] == 0 and p[1] == 0: ############################# top left corner
                if points[0,1] > maxAction:
                    maxAction = points[0,1]

                if points[1,1] > maxAction:
                    maxAction = points[1,1]

                if points[1,0] > maxAction:
                    maxAction = points[1,0]
                
         
            elif p[0] == 0 and p[1] == 6: ############################# top right corner
                if points[1,6] > maxAction:
                    maxAction = points[1,6]

                if points[1,5] > maxAction:
                    maxAction = points[1,5]

                if points[0,5] > maxAction:
                    maxAction = points[0,5]
                

            elif p[0] == 6 and p[1] == 0: ############################# bottom left corner
                if points[5,0] > maxAction:
                    maxAction = points[5,0]

                if points[5,1] > maxAction:
                    maxAction = points[5,1]

                if points[6,1] > maxAction:
                    maxAction = points[6,1]
                

            elif p[0] == 6 and p[1] == 6: ############################# bottom right corner
                if points[6,5] > maxAction:
                    maxAction = points[6,5]

                if points[5,5] > maxAction:
                    maxAction = points[5,5]

                if points[5,6] > maxAction:
                    maxAction = points[5,6]
                

            elif p[0] == 0: ############################# top edge
                if points[p[0],p[1]+1] > maxAction:
                    maxAction = points[p[0],p[1]+1]

                if points[p[0]+1,p[1]+1] > maxAction:
                    maxAction = points[p[0]+1,p[1]+1]

                if points[p[0]+1,p[1]] > maxAction:
                    maxAction = points[p[0]+1,p[1]] 

                if points[p[0]+1,p[1]-1]  > maxAction:
                    maxAction = points[p[0]+1,p[1]-1]

                if points[p[0],p[1]-1] > maxAction:
                    maxAction = points[p[0],p[1]-1]
            
            elif p[0] == 6: ############################# bottom edge
                if points[p[0]-1,p[1]-1] > maxAction:
                    maxAction = points[p[0]-1,p[1]-1]

                if points[p[0]-1,p[1]] > maxAction:
                    maxAction = points[p[0]-1,p[1]]

                if points[p[0]-1,p[1]+1] > maxAction:
                    maxAction = points[p[0]-1,p[1]+1]
                
                if points[p[0],p[1]+1] > maxAction:
                    maxAction = points[p[0],p[1]+1]

                if points[p[0],p[1]-1] > maxAction:
                    maxAction = points[p[0],p[1]-1]
            
            elif p[1] == 0: ############################# left edge
                if points[p[0]-1,p[1]] > maxAction:
                    maxAction = points[p[0]-1,p[1]]

                if points[p[0]-1,p[1]+1] > maxAction:
                    maxAction = points[p[0]-1,p[1]+1]
                
                if points[p[0],p[1]+1] > maxAction:
                    maxAction = points[p[0],p[1]+1]

                if points[p[0]+1,p[1]+1] > maxAction:
                    maxAction = points[p[0]+1,p[1]+1]

                if points[p[0]+1,p[1]] > maxAction:
                    maxAction = points[p[0]+1,p[1]] 
            
            elif p[1] == 6: ############################# right edge
                if p[0] == 3: # reward is zero at this point
                    reward = 0

                if points[p[0]-1,p[1]-1] > maxAction:
                    maxAction = points[p[0]-1,p[1]-1]

                if points[p[0]-1,p[1]] > maxAction:
                    maxAction = points[p[0]-1,p[1]]

                if points[p[0]+1,p[1]] > maxAction:
                    maxAction = points[p[0]+1,p[1]] 

                if points[p[0]+1,p[1]-1]  > maxAction:
                    maxAction = points[p[0]+1,p[1]-1]

                if points[p[0],p[1]-1] > maxAction:
                    maxAction = points[p[0],p[1]-1]


            else: ############################# points in the center
                if points[p[0]-1,p[1]-1] > maxAction:
                    maxAction = points[p[0]-1,p[1]-1]

                if points[p[0]-1,p[1]] > maxAction:
                    maxAction = points[p[0]-1,p[1]]

                if points[p[0]-1,p[1]+1] > maxAction:
                    maxAction = points[p[0]-1,p[1]+1]
                
                if points[p[0],p[1]+1] > maxAction:
                    maxAction = points[p[0],p[1]+1]

                if points[p[0]+1,p[1]+1] > maxAction:
                    maxAction = points[p[0]+1,p[1]+1]

                if points[p[0]+1,p[1]] > maxAction:
                    maxAction = points[p[0]+1,p[1]] 

                if points[p[0]+1,p[1]-1]  > maxAction:
                    maxAction = points[p[0]+1,p[1]-1]

                if points[p[0],p[1]-1] > maxAction:
                    maxAction = points[p[0],p[1]-1]

            # if the difference between the current utility of the state and the new utility of the state >= 0.001
            if abs(points[p]-(reward + maxAction)) >= 0.001:
                # update the utility of the state
                points[p] = reward + maxAction
                modified = True

    # update the matrix
    for p in points:      
        matrix[p[0]][p[1]] = points[p]
    

    print(np.matrix(matrix))        
    

if __name__ == "__main__":
    main()
