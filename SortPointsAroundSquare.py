import rhinoscriptsyntax as rs
import operator

def sortPointsAroundSquare(point1, points, sortedPoints = None):
    if sortedPoints == None:
        sortedPoints = []
        sortedPoints.append(points[0])
    
    if len(points) == 1:
        sortedPoints.append(points[0])
        points.remove(points[0])
        return sortedPoints
    
    
    measurementDict = {}

    if point1 in points:
        points.remove(point1)
        

    for point in points:
        measurementDict[point] = rs.Distance(point1, point)
    

    sortedMeasurmentDict = sorted(measurementDict.items(), key=operator.itemgetter(1))
    closestPoint = sortedMeasurmentDict[0][0]
    sortedPoints.append(closestPoint)
    points.remove(closestPoint)
    
    sortPointsAroundSquare(closestPoint, points, sortedPoints)
    return sortedPoints

points = rs.GetObjects("sel Points", 1)

sortedPoints = sortPointsAroundSquare(points[0], points)
print(len(sortedPoints))

rs.AddPolyline(sortedPoints)

