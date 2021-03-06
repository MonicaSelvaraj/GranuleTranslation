#Find the centers between C1:suntag-mRNA and C3:scfv-GFP.
#Find the closest granule point to each center point and plot distances
#Plot the center point, granules, and closest point on the granule

import numpy as np
import csv
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl

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
arr2 = getPoints('3DCoordinatesC2.csv')#granules
arr3 = getPoints('FQ3DCoordinatesC3.csv')#scfv-GFP

#STEP 1 - Find center point between each pair of C1 and C3 points. 
C1C3centers = list()
for c1,c3 in zip(arr1, arr3): C1C3centers.append((c1 + c3)/2)
C1C3centers = np.array(C1C3centers, dtype = float)
#print(C1C3centers)
 
#STEP 2 - Find the granule point and its index that each center point is closest to
closestC2s = list() #List of the closest granule point
minindex = list() #List of closest granule index
for c in C1C3centers:
    curindex = cdist([c], arr2).argmin()
    minindex.append(curindex)
    closestC2s.append(arr2[curindex])
minindex = np.array(minindex, dtype = int)
closestC2s = np.array(closestC2s, dtype = float)

#STEP 3 - Find and plot distance between closest granule points and center points
mindist = list()
for c2,center in zip(closestC2s, C1C3centers): mindist.append(np.linalg.norm(c2-center))
mindist = np.array(mindist, dtype = float)
print(mindist)
#Plot distances
plt.plot(mindist)
plt.show()
plt.hist(mindist, bins='auto')
plt.show()

#Creating a widget for 3D plotting 
app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.show()
sp1 = gl.GLScatterPlotItem(pos=closestC2s, color = [1,0,0,0], pxMode=True, size = 10)
sp1.setGLOptions('opaque')
w.addItem(sp1)
sp2 = gl.GLScatterPlotItem(pos=arr2, color = [0,0,1,0], pxMode=True, size = 5)
sp2.setGLOptions('opaque')
w.addItem(sp2)
sp3 = gl.GLScatterPlotItem(pos=C1C3centers, color = [0,1,0,0], pxMode=True, size = 10)
sp3.setGLOptions('opaque')
w.addItem(sp3)
# Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    QtGui.QApplication.instance().exec_()


