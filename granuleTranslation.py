#This script finds the center between C1:suntag-mRNA and C3:scfv-GFP

import numpy as np
import csv

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
#arr2 = getPoints('3DCoordinatesC2Bio.csv')#granules
arr3 = getPoints('FQ3DCoordinatesC3.csv')#scfv-GFP

#STEP 1 - Find center point between each pair of C1 and C3 points. 
C1C3center = list()
for c1,c3 in zip(arr1, arr3): C1C3center.append((c1 + c3)/2)
C1C3center = np.array(C1C3center, dtype = float)
print(C1C3center)
 



