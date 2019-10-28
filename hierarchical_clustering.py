import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import pdb

file = ""
xValues = []
yValues = []
groups = []

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "[" + str(self.x) + ", " + str(self.y) + "]"

    def getDistance(self, otherPoint):
        return abs(self.x - otherPoint.x) + abs(self.y - otherPoint.y)

class Group:
    def __init__(self):
        self.points = []

    def setPoints(self, points):
        self.points = points

    def mergeGroup(self, otherGroup):
        newPoints = []
        for point in self.points:
            newPoints.append(point)
        for point in otherGroup.points:
            newPoints.append(point)

        newGroup = Group()
        newGroup.setPoints(newPoints)
        return newGroup

    def distanceToGroup(self, otherGroup):
        smallestDistance = 999

        for point in self.points:
            for point2 in otherGroup.points:
                dist = point.getDistance(point2)
                if dist < smallestDistance:
                    smallestDistance = dist

        return smallestDistance

def main():
    file = open("B.txt", "r")
    for line in file.readlines():
        xValues.append(float(line[0:6]))
        yValues.append(float(line[7:13]))

    # Puts each point into a group by itself to begin with
    for i in range(0, len(xValues)):
        thisPoint = Point(xValues[i], yValues[i])
        thisGroup = Group()
        pointList = []
        pointList.append(thisPoint)
        thisGroup.setPoints(pointList)
        groups.append(thisGroup)

    # We are clustering until there are 3 groups remaining:
    # One parent group and two main child groups
    while(len(groups) > 3):
        smallestDistance = 999
        groupsToMerge = []
        for group1 in groups:
            for group2 in groups:
                dist = group1.distanceToGroup(group2)
                if(dist != 0 and dist < smallestDistance):
                    smallestDistance = dist
                    groupsToMerge = []
                    groupsToMerge.append(group1)
                    groupsToMerge.append(group2)

        newGroup = groupsToMerge[0].mergeGroup(groupsToMerge[1])

        groups.append(newGroup)
        groups.remove(groupsToMerge[0])
        groups.remove(groupsToMerge[1])

    group1x = []
    group1y = []
    group2x = []
    group2y = []
    for point in groups[1].points:
        group1x.append(point.x)
        group1y.append(point.y)

    for point in groups[2].points:
        group2x.append(point.x)
        group2y.append(point.y)

    df = pd.DataFrame({
        'x': group1x,
        'y': group1y
    })
    df2 = pd.DataFrame({
        'x': group2x,
        'y': group2y
    })
    plotPoints(df, df2)

def plotPoints(df, df2):
    fig = plt.figure(figsize=(5, 5))
    plt.scatter(df['x'], df['y'], label='Cluster 1', color='r', s=10)
    plt.scatter(df2['x'], df2['y'], label='Cluster 2', color='g', s=10)
    colmap = {0: 'k', 1: 'k', 2: 'k'}
    plt.xlim(0, 2)
    plt.ylim(0, 2)
    plt.legend(loc=2)
    plt.show()

main()
