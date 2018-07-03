# -*- encoding: utf-8 -*-
import struct
import pickle
import matplotlib.pyplot as plt    
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pprint


def loadData(binData):
    
    charList = [] 
    for x in range(0,80):
        if binData[x] != 0:
            charList.append(struct.unpack('c', bytearray([binData[x]]))[0].decode('utf-8'))
        else:
            pass    
    
    description = ''.join(charList) 
    

    number = [binData[80], binData[81], binData[82], binData[83]]     
    triangleNum = struct.unpack('I', bytearray(number))[0]

    normalVectorList = []
    triangleVerteciesList = []
    for i in range(0, triangleNum):
        
        # for each triangle
        singleTriangleVerteciesList = []

        for j in range(0, 4):    
            if j == 0:
                # the normal vector for each triangle
                nxBytes = [binData[84 + i * 50], binData[85 + i * 50], binData[86 + i * 50], binData[87 + i * 50]]
                nyBytes = [binData[88 + i * 50], binData[89 + i * 50], binData[90 + i * 50], binData[91 + i * 50]]
                nzBytes = [binData[92 + i * 50], binData[93 + i * 50], binData[94 + i * 50], binData[95 + i * 50]]

                nx = struct.unpack('f', bytearray(nxBytes))[0]
                ny = struct.unpack('f', bytearray(nyBytes))[0]
                nz = struct.unpack('f', bytearray(nzBytes))[0]

                normalVectorList.append([nx, ny, nz])
                
            else:        
                # the three vertecis of each triangle
                pxBytes = [binData[84 + j * 12+ i * 50], binData[85 + j * 12 + i * 50], binData[86 + j * 12+ i * 50], binData[87 + j * 12+ i * 50]]
                pyBytes = [binData[88 + j * 12+ i * 50], binData[89 + j * 12 + i * 50], binData[90 + j * 12+ i * 50], binData[91 + j * 12+ i * 50]]
                pzBytes = [binData[92 + j * 12+ i * 50], binData[93 + j * 12 + i * 50], binData[94 + j * 12+ i * 50], binData[95 + j * 12+ i * 50]]

                px = struct.unpack('f', bytearray(pxBytes))[0]
                py = struct.unpack('f', bytearray(pyBytes))[0]
                pz = struct.unpack('f', bytearray(pzBytes))[0]
                
                singleTriangleVerteciesList.append([px, py, pz])

            
        triangleVerteciesList.append(singleTriangleVerteciesList)
    
    text = dataToASCII(description, triangleNum, normalVectorList, triangleVerteciesList)
    
    return text
    

def drawLines(triangleVerteciesList):
    ax = plt.axes(projection = '3d')
    x = []
    y = []
    z = []
    for triangle in triangleVerteciesList:
        for vertex in triangle:
            x.append(vertex[0])
            y.append(vertex[1])
            z.append(vertex[2])
        X = np.asarray(x)
        Y = np.asarray(y)
        Z = np.asarray(z)
        #ax.scatter(x, y, z)

    ax.plot3D(X, Y, Z, 'gray')
    plt.show()

def dataToASCII(description, triangleNum, normalVectorList, triangleVerteciesList):
    
    
    text = 'solid ' + description + '\n'
    
    for i in range(triangleNum):
        text = text + '  facet normal ' + str(normalVectorList[i][0]) + ' ' + str(normalVectorList[i][1]) + ' ' + str(normalVectorList[i][2]) + '\n'
        text = text + '    outer loop\n'
        text = text + '      vertex ' + str(triangleVerteciesList[i][0][0]) + ' ' + str(triangleVerteciesList[i][0][1]) + ' ' + str(triangleVerteciesList[i][0][2]) + '\n'
        text = text + '      vertex ' + str(triangleVerteciesList[i][1][0]) + ' ' + str(triangleVerteciesList[i][1][1]) + ' ' + str(triangleVerteciesList[i][1][2]) + '\n'
        text = text + '      vertex ' + str(triangleVerteciesList[i][2][0]) + ' ' + str(triangleVerteciesList[i][2][1]) + ' ' + str(triangleVerteciesList[i][2][2]) + '\n'
        
        text = text + '    endloop\n'
        text = text + '  endfacet\n'
        
    text = text + 'endsolid'
    
    return text


def main():
    filesList = ['graduation.stl']
    
    for fileName in filesList:
        with open(fileName, 'rb') as inFile:
            binData = inFile.read()
            if binData != None:
                text = loadData(binData)   
                
                print('Extract Data')
            else:
                print("Open Error")
            
        if '.stl' in fileName:
            outFileName = fileName.replace('.stl', '_ascii.stl')
        else: 
            outFileName = fileName.replace('.STL', '_ascii.stl')
            
        with open(outFileName, 'w') as outFile: 
            outFile.write(text) 
            

main()