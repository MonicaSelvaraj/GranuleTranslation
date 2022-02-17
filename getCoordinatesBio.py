import numpy as np
import csv
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl

'''
Reads and stores the intensity matrix for one z-slice 
Cuts off first row and first column
'''
def GetSliceIntensities(path):
	with open(path, 'r') as csv_file:
		matrix = []
		csv_reader = csv.reader (csv_file)
		for row in csv_reader:
			matrix.append(row)
		I = np.array(matrix)
		I = I[1:,1:] #cuts off first row and first column
		I = [[float(y) for y in x] for x in I]
		I = np.array(I)
	return I

'''
Returns x,y,z coordinates of fluorescence in current z-slice given the matrix of 
intensity values and which Z slice it is 
Temporary data (in micro meters): Pixel width,height: 0.0313030, Voxel depth: 0.1095510
'''
def getCoordinates(I,slice):
    y,x = I.nonzero() #y-rows, x-cols
    zlen = (len(y))
    z = [slice]*zlen
    x = np.array(x, dtype = float);y = np.array(y, dtype = float);z = np.array(z, dtype = float)
    #Scaling to biological size
    x = x*42.5; y = y*42.5; z = z*150
    return(x,y,z)

#Getting the coordinates for all the z-slices and storing it in an array called pos
pos = np.zeros((1,3)) #Making pos the same dimensions as the slice coordinates to allow for concatenation 
pos = pos.astype(float)
for i in range(0,35,1):#CHANGE NUMBER OF SLICES
    I = GetSliceIntensities("Data/C2_CROPuas-suntag-nos_nosgal4_scfvgfpnls_nos590_suntag670_aligned_1/ZResults/Results"+str(i)+".csv") #I is the matrix of intensities #CHANGE PATH TO ZRESULTS
    AxisLim = I.shape[0]#Number of rows/columns
    x,y,z = getCoordinates(I,i)
    size = len(z)
    SlicePos = np.dstack((x,y,z))
    SlicePos = SlicePos[0]
    SlicePos = SlicePos.astype(float)
    pos = np.vstack((pos, SlicePos))
pos = np.delete(pos,0,0) #Deleting the [0,0,0] used for initialization
print(pos)

#Creating a widget for 3D plotting 
app = QtGui.QApplication([])
w = gl.GLViewWidget()
#w = gl.setGLOptions('opaque')
w.show()
sp2 = gl.GLScatterPlotItem(pos=pos, color = [0,0,1,0], pxMode=True, size = 1)
sp2.setGLOptions('opaque')
w.addItem(sp2)
# Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    QtGui.QApplication.instance().exec_()

#Saving coordinates to file 
data = np.hsplit(pos,3)
X = np.array(data[0], dtype = float);Y = np.array(data[1], dtype = float);Z = np.array(data[2], dtype = float)
np.savetxt('3DCoordinatesC2.csv', np.column_stack((X, Y, Z)), delimiter=",", fmt='%s')#CHANGE COORDINATE FILE NAME
