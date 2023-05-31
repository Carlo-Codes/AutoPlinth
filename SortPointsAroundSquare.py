import rhinoscriptsyntax as rs
import operator

def sortPointsAroundSquare(point1, points, sortedPoints = None):
    if sortedPoints == None:
        sortedPoints = []
    
    measurementDict = {}

    for point in points:
        measurementDict[points[1]] = rs.Distance(point1, point)

    sortedMeasurmentDict = sorted(measurementDict.items(), key=operator.itemgetter(1))
    sortedPoints.append(sortedMeasurmentDict[0])
    points.remove(sortedMeasurmentDict[0])
    
    sortPointsAroundSquare(sortedMeasurmentDict[0], points, sortedPoints)