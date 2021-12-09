import numpy as np
import csv
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
    print(arr)
    return (arr)

arr1 = getPoints('FQ3DCoordinatesC1.csv')#suntag-mRNA
arr2 = getPoints('3DCoordinatesC2Bio.csv')#granules
arr3 = getPoints('FQ3DCoordinatesC3.csv')#scfv-GFP


#Creating a widget for 3D plotting 
app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.show()
sp1 = gl.GLScatterPlotItem(pos=arr1, color = [1,0,0,0], pxMode=True, size = 10)
sp1.setGLOptions('opaque')
w.addItem(sp1)
sp2 = gl.GLScatterPlotItem(pos=arr2, color = [0,0,1,0], pxMode=True, size = 5)
sp2.setGLOptions('opaque')
w.addItem(sp2)
sp3 = gl.GLScatterPlotItem(pos=arr3, color = [0,1,0,0], pxMode=True, size = 10)
sp3.setGLOptions('opaque')
w.addItem(sp3)
# Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    QtGui.QApplication.instance().exec_()
