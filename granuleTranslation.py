#Find the centers between C1:suntag-mRNA and C3:scfv-GFP.
#Find the closest granule point to each center point and plot distances

import numpy as np
import csv
from scipy.spatial.distance import cdist

def getPoints(filename):
    x = list(); y = list(); z = list()
    with open (filename, 'r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader (csv_file)
        for line in csv_reader:
                x.append(line[0]); y.append(line[1]); z.append(line[2])
    x = np.array(x); y = np.array(y); z = np.array(z)
    x = x.astype(float);y = y.astype(float);z = z.astype(float)
    arr = np.stack((x, y, z), axis=-1)
    arr = arr.astype(float)
    #print(arr)
    return (arr)

arr1 = getPoints('FQ3DCoordinatesC1.csv')#suntag-mRNA
arr2 = getPoints('3DCoordinatesC2Bio.csv')#granules
arr3 = getPoints('FQ3DCoordinatesC3.csv')#scfv-GFP

#STEP 1 - Find center point between each pair of C1 and C3 points. 
C1C3centers = list()
for c1,c3 in zip(arr1, arr3): C1C3centers.append((c1 + c3)/2)
C1C3centers = np.array(C1C3centers, dtype = float)
#print(C1C3centers)
 
#STEP 2 - Find the granule point that each center point is closest to and make a plot of distances. 
closestC2s = list()
for c in C1C3centers:
    closestC2s.append(arr2[cdist([c], arr2).argmin()])
closestC2s = np.array(closestC2s, dtype = float)
print(closestC2s)
 

#D = spdist.cdist(, verts)


#def closest_granule(node, nodes):
#    return nodes[cdist([node], nodes).argmin()]


