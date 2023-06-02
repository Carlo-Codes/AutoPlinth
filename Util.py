import rhinoscriptsyntax as rs
import operator

def sortPointsByDistance(point1, points, sortedPoints = None):
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
    
    sortPointsByDistance(closestPoint, points, sortedPoints)
    return sortedPoints

# points = rs.GetObjects("sel Points", 1)

# sortedPoints = sortPointsByDistance(points[0], points)
# print(len(sortedPoints))

# rs.AddPolyline(sortedPoints+[sortedPoints[0]])

def trimCurveFromBothSides(crv, trimAmount):
    
    originalLength = rs.CurveLength(crv)
    edgeDomain = trimAmount/originalLength
    domain = rs.CurveDomain(crv)
    
    domain[0] = edgeDomain * domain[0] ## i think this isnt trimming the curve right (i know)
    domain[1] = (1 - edgeDomain) * domain[1]
    newCurve = rs.TrimCurve(crv, domain)
    return newCurve


# crv = rs.GetObject("crv")

# trimCurveFromBothSides(crv, 20)

