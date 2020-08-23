#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 21:50:16 2020

@author: adam
"""

import numpy as np
from math import fabs
import matplotlib.pyplot as plt
from numpy import linalg as LA
import os

def GregsCircles(matrix):
    eigenv = LA.eig(matrix)[0]
    if isSquare(matrix) != True:
        print('Your input matrix is not square!')
        return []
    circles = []
    for x in range(0,len(matrix)):
        radius = 0
        piv = matrix[x][x]
        for y in range(0,len(matrix)):
            if x != y:
                radius += fabs(matrix[x][y])
        circles.append([piv,radius])
    return (circles, eigenv)

def plotCircles(matrixData, run_id, title, name):
    circles, eigenv = matrixData
    index, radi = zip(*circles)
    Xupper = max(index) + np.std(index)
    Xlower = min(index) - np.std(index)
    Ylimit = max(radi) + np.std(index)
    fig, ax = plt.subplots()
    ax = plt.gca()
    ax.cla()
    ax.set_xlim((Xlower,Xupper))
    ax.set_ylim((-Ylimit,Ylimit))
    plt.xlabel('Real Axis')
    plt.ylabel('Imaginary Axis')
    plt.title('Gershgorin circles')
    for x in range(0,len(circles)):
        circ = plt.Circle((index[x],0), radius = radi[x])
        ax.add_artist(circ)
    for eigen in eigenv:
        circ = plt.Circle((eigen, 0), radius = 0.1, color='red')
        ax.add_artist(circ)
    ax.plot([Xlower,Xupper],[0,0],'k--')
    ax.plot([0,0],[-Ylimit,Ylimit],'k--')
    
    if not os.path.exists('graph_with_one_added_potential_edge'):
        os.makedirs('graph_with_one_added_potential_edge')
    if not os.path.exists('graph_with_one_added_potential_edge/' + str(run_id)):
        os.makedirs('graph_with_one_added_potential_edge/' + str(run_id))
    if not os.path.exists('graph_with_one_added_potential_edge/' + str(run_id) + '/' + str(title)):
        os.makedirs('graph_with_one_added_potential_edge/' + str(run_id) + '/' + str(title))
    if not os.path.exists('graph_with_one_added_potential_edge/' + str(run_id) + '/' + str(title) + '/gershgorin'):
        os.makedirs('graph_with_one_added_potential_edge/' + str(run_id) + '/' + str(title) + '/gershgorin')
    fig.savefig('./graph_with_one_added_potential_edge/' + str(run_id) + '/' + str(title) + '/' + 'gershgorin/' + str(name) + '.png')
    plt.close(fig)
    plt.clf()
    
def isSquare(m):
    cols = len(m)
    for row in m:
        if len(row) != cols:
            return False
    return True

"""
def main():
    test = np.array([[10,-1,0,1],[0.2,8,0.2,0.2],[1,1,2,1],[-1,-1,-1,-11]])
    temp = GregsCircles(test, 11, 11)
    plotCircles(temp,11,11)

if __name__ == '__main__':
    main()
"""