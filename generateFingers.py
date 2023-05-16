import rhinoscriptsyntax as rs
import operator

class Generatefingers:
    def __init__(self, topOrBottom, sides):
        self.splitOutIntersections(topOrBottom,sides)
        for intersection in self.splitIntersections:
            self.makeFingerCrossSection(intersection)
            
    
    def splitOutIntersections(self, topOrBottom, sides):
        intersection = rs.BooleanIntersection(topOrBottom, sides, delete_input=False)
        self.splitIntersections = []
        for side in sides:
            self.splitIntersections += rs.BooleanIntersection (intersection, side, delete_input= False)
        rs.DeleteObjects(intersection)

    def makeFingerCrossSection(self, intersection):
        intersectionEdges =  rs.DuplicateEdgeCurves(intersection)
        if len(intersectionEdges) > 12:
            rs.MessageBox("One of the intersections isnt a cuboid", buttons=0, title="Error")
            pass
        edgesLength = {}
        for curve in intersectionEdges:
            edgesLength[curve] = rs.CurveLength(curve)
        sortedEdgeLength = sorted(edgesLength.items(), key=operator.itemgetter(1))
        print(sortedEdgeLength)
        point1 = rs.CurveMidPoint(sortedEdgeLength[-4][0])
        point2 = rs.CurveMidPoint(sortedEdgeLength[-3][0])
        point3 = rs.CurveMidPoint(sortedEdgeLength[-2][0])
        point4 = rs.CurveMidPoint(sortedEdgeLength[-1][0])
    
        crossSectionpoints = [point1,point2,point3,point4]
        print(crossSectionpoints)
        crossSectionCurve = rs.AddPolyline(crossSectionpoints+[crossSectionpoints[0]])
        rs.DeleteObjects([intersectionEdges])

                  

    def makeFinger(self):
        pass

    def arrayFingers(self):
        pass
