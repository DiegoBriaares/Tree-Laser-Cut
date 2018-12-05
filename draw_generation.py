# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 18:30:18 2018
@author: Diego González Hernández
"""

import operator
import random
import math
import sys
import os

try:
    import dxfwrite
except ImportError:
    curdir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.abspath(os.path.join(curdir, os.path.pardir)))

import dxfwrite
from dxfwrite import DXFEngine as dxf

edges = []
num_edges = 0
num_points = 100
plane_limit = 21
name = 'tree.dxf'
dwg = dxf.drawing(name)
painted = [0 for i in range(0, num_points + 1)]
points_X = [0 for i in range(0, num_points + 1)]
points_Y = [0 for i in range(0, num_points + 1)]
used_points = [ [0 for j in range (0, 1001)] for i in range (0, 1001)]
Tree = [ [] for i in range (0, num_points)]

class DisjoinSet(object):
    def __init__(self, n):
        self.padre = [x for x in range(n)]
        self.rank = [0 for x in range(n)]

    def find(self, x):
        if(self.padre[x]!=x):
            self.padre[x]=self.find(self.padre[x])
        return self.padre[x]

    def union(self, x, y):
        xRaiz = self.find(x)
        yRaiz = self.find(y)
        if(xRaiz == yRaiz):
            return
        if self.rank[xRaiz] < self.rank[yRaiz]:
            self.padre[xRaiz] = yRaiz
        elif self.rank[xRaiz] > self.rank[yRaiz]:
            self.padre[yRaiz] = xRaiz
        else:
            self.padre[yRaiz] = xRaiz
            self.rank[xRaiz]+=1

def draw(a, b):
    if painted[a] == 0:
        dwg.add(dxf.circle(center=(points_X[a],points_Y[a]), radius = .14, color = 141))
        painted[a] = 1
    if painted[b] == 0:
        dwg.add(dxf.circle(center=(points_X[b],points_Y[b]), radius = .14, color = 141))
        painted[b] = 1
    r_1 = r_2 = r_3 = r_4 = 0
    if points_X[a] <= points_X[b]:
        r_1 = 0.1
        r_3 = -0.1
    else :
        r_1 = -0.1
        r_3 = 0.1
    if points_Y[a] <= points_Y[b]:
        r_2 = 0.1
        r_4 = -0.1
    else :
        r_2 = -0.1
        r_4 = 0.1
    dwg.add(dxf.line((points_X[a] + r_1, points_Y[a] + r_2), (points_X[b] + r_3, points_Y[b] + r_4), color=61))

random.seed(a = None)
for i in range(0, num_points):
    points_X[i] = random.randint(1, plane_limit)
    points_Y[i] = random.randint(1, plane_limit)
    while used_points[points_X[i]][points_Y[i]] == 1:
        points_X[i] = random.randint(1, plane_limit)
        points_Y[i] = random.randint(1, plane_limit)
    used_points[points_X[i]][points_Y[i]] = 1
for i in range(0, num_points):
    for j in range(0, num_points):
        if i != j:
            x = (points_X[i] - points_X[j])
            y = (points_Y[i] - points_Y[j])
            edges.append((math.sqrt(x * x + y * y), i, j))
            num_edges += 1
edges.sort(key=operator.itemgetter(0))
G = DisjoinSet(num_points)
for i in range(num_edges):
    for cost, i, j in edges:
        root_x = G.find(i)
        root_y = G.find(j)
        if root_x != root_y:
            G.union(i, j)
            Tree[i].append(j)
for i in range(0, num_points):
    for node in Tree[i]:
        a = i
        b = node
        draw(a, b)
dwg.save()
print ("Drawed :)")
