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


        crossSections = rs.AddSrfPt([point1,point2, point3, point4])

        self.fingerCrossSection = crossSections

        toDelete = surfaces + intersectionEdges
        rs.DeleteObjects(toDelete)

    def sortPointsAroundSquare(self, points):
        for i in range(len(points)):
            for j in range(len(points)):
                if i != j:
                    ##start here. need ot make an algo rythm that checks distance of each point against every othe rpoint, store it in a list of objects that store optionss


        
                  

    def makeFinger(self):
        pass

    def arrayFingers(self):
        pass
