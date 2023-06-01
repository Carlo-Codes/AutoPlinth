import rhinoscriptsyntax as rs
import operator
import copy
import sortPointsByDistance

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
        surfaces = rs.ExplodePolysurfaces(intersection)
        surfaceArea = {}
        for surface in surfaces:
            surfaceArea[surface] = rs.Area(surface)
        
        sortedSurfaceArea = sorted(surfaceArea.items(), key=operator.itemgetter(1))
        crossSecton = sortedSurfaceArea[-1][0]

        intersectionEdges =  rs.DuplicateEdgeCurves(intersection)
        edgesLength = {}
        for curve in intersectionEdges:
            edgesLength[curve] = rs.CurveLength(curve)

        sortedEdgeLength = sorted(edgesLength.items(), key=operator.itemgetter(1))
        edge1 = sortedEdgeLength[-1][0]
        edge2 = sortedEdgeLength[-2][0]
        edge3 = sortedEdgeLength[-3][0]
        edge4 = sortedEdgeLength[-4][0]
        point1 = rs.CurveMidPoint(edge1)
        point2 = rs.CurveMidPoint(edge2)
        point3 = rs.CurveMidPoint(edge3)
        point4 = rs.CurveMidPoint(edge4)

        unsortedPoints = [point1,point2, point3, point4]

        sortedPoints = sortPointsByDistance.sortPointsByDistance(unsortedPoints[0],unsortedPoints)


        crossSections = rs.AddSrfPt(sortedPoints)
        
        self.fingerCrossSection = crossSections

        toDelete = surfaces + intersectionEdges + [intersection]
        rs.DeleteObjects(toDelete)


         
        
                  

    def makeFinger(self):
        pass

    def arrayFingers(self):
        pass
