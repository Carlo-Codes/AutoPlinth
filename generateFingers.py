import rhinoscriptsyntax as rs
import operator
import copy
import sortPointsByDistance
import System

class Generatefingers:
    def __init__(self, topOrBottom, sides, sheetThickness, fingerTolerance):
        self.fingerCrossSections = {}
        self.splitOutIntersections(topOrBottom,sides)
        for intersection in self.splitIntersections:
            self.makefingerCrossSections(intersection)
        self.generateFingerArray(self.fingerCrossSections,100)
        
            
    
    def splitOutIntersections(self, topOrBottom, sides):
        intersection = rs.BooleanIntersection(topOrBottom, sides, delete_input=False)
        self.splitIntersections = []
        for side in sides:
            self.splitIntersections += rs.BooleanIntersection (intersection, side, delete_input= False)
        rs.DeleteObjects(intersection)

    def makefingerCrossSections(self, intersection):
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

        ##sorting points
        unsortedPoints = [point1,point2, point3, point4]

        sortedPoints = sortPointsByDistance.sortPointsByDistance(unsortedPoints[0],unsortedPoints)
        
        ##crosssection
        crossSection = rs.AddPolyline(sortedPoints+[sortedPoints[0]])
        self.fingerCrossSections [crossSection] = sortedEdgeLength[-1][0] #edge to keep
        
        ##edges to delete
        edgesToDelete=[]
        for i in range(len(sortedEdgeLength)):
            if sortedEdgeLength[i] != sortedEdgeLength[-1]:
                edgesToDelete.append(sortedEdgeLength[i][0])
        ###
        
        toDelete = surfaces + edgesToDelete + [intersection]
        rs.DeleteObjects(toDelete)
        

    def moveCrossSectionToStart(self, crossSectionDict, sheetThickness, fingerEdgeTolerance):
        
        for key, value in crossSectionDict.items():
            
            midpoint = rs.CurveMidPoint(value)
            endpont = rs.CurveEndPoint(value)
            startPoint = rs.CurveStartPoint(value)
            curveLength = rs.CurveLength(value)

            neededVectorLength = curveLength - ((sheetThickness + fingerEdgeTolerance)*2)
            vectorScaleFactor = neededVectorLength / curveLength
        
            movementVect = rs.VectorCreate(endpont, midpoint)
            scaledMovementVect = rs.VectorScale(movementVect, vectorScaleFactor)

            rs.MoveObject(key, scaledMovementVect)
           
        
                  

    def makeFinger(self, crossSection, crv, etrusionLength):
        midpoint = rs.CurveMidPoint(crv)
        endpont = rs.CurveEndPoint(crv)
        startPoint = rs.CurveStartPoint(crv)
        curveLength = rs.CurveLength(crv)

        extrusionVectL = rs.VectorCreate(endpont, midpoint)
        extrusionVectR = rs.VectorCreate(startPoint, midpoint)

        vectorScaleFactor = etrusionLength / curveLength

        scaledMovementVectL = rs.VectorScale(extrusionVectL, vectorScaleFactor)
        scaledMovementVectR = rs.VectorScale(extrusionVectR, vectorScaleFactor)

        rs.MoveObject(crossSection,scaledMovementVectL)
        extrusionStartPoint = rs.CopyObject(midpoint,scaledMovementVectL)
        extrusionEndPoint = rs.CopyObject(midpoint, scaledMovementVectR)
        finger = rs.ExtrudeCurveStraight(crossSection, extrusionStartPoint,extrusionEndPoint)
        rs.CapPlanarHoles(finger)
        
        

                 


    def arrayFingers(self):
        pass

    def generateFingerArray(self,  crossSectionDict, multiFingerThreashold):
        for key, value in crossSectionDict.items():
            #  nFingers = 1
            #  midpoint = rs.CurveMidPoint(value)
            #  curveLength = rs.CurveLength(value)
            #  if curveLength > multiFingerThreashold:
            #      pass
            #  else:
            #      pass
            self.makeFinger(key,value,50)
