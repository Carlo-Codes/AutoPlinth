import rhinoscriptsyntax as rs
import operator
import copy
import Util
import System
from Util import trimCurveFromBothSides



class Generatefingers:
    def __init__(self, topOrBottom, sides, sheetThickness, fingerTolerance, edgeOffset,minFingLen):
        self.fingerCrossSections = {}
        self.fingers = {} #fingers and he curve they're on
        self.splitOutIntersections(topOrBottom,sides)
        for intersection in self.splitIntersections:
            self.makefingerCrossSections(intersection)
        self.generateFingerArray(self.fingerCrossSections,minFingLen,edgeOffset)
        
            
    
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

        sortedPoints = Util.sortPointsByDistance(unsortedPoints[0],unsortedPoints)
        
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
        rs.DeleteObjects([extrusionStartPoint,extrusionEndPoint])
        return finger
        

    def arrayFingers(self, finger, crv, n, edgeOffset = 0):
        newcrv = trimCurveFromBothSides(crv, edgeOffset)
        divisionPts = rs.DivideCurve(crv, n , create_points=True, return_points=True)
        centrePt = rs.CurveMidPoint(newcrv)
        fingers = []

        for pt in divisionPts[1:-1]:
            movementVector = rs.VectorCreate(pt, centrePt)
            fingerToAdd = rs.CopyObject(finger, movementVector)
            fingers.append(fingerToAdd)
        
        rs.DeleteObjects([finger, crv])
        
        return fingers


    def generateFingerArray(self,  crossSectionDict, minimumFingerLength, edgeOffset):
        for key, value in crossSectionDict.items():
             nFingers = 1
             midpoint = rs.CurveMidPoint(value)
             curveLength = rs.CurveLength(value)

             if curveLength / 2 < minimumFingerLength:
                 finger = self.makeFinger(key,value,minimumFingerLength)

             elif curveLength / 3 < minimumFingerLength:
                 fingerlength = curveLength / 3
                 finger = self.makeFinger(key,value,fingerlength)
                 fingers = self.arrayFingers(finger,value,2,edgeOffset)
                 
             elif curveLength / 4 < minimumFingerLength:
                 fingerlength = curveLength / 4
                 finger = self.makeFinger(key,value,fingerlength)
                 fingers = self.arrayFingers(finger,value,3,edgeOffset)
                 
             else:
                fingerlength = curveLength / 5
                finger = self.makeFinger(key,value,fingerlength)
                fingers = self.arrayFingers(finger,value,4,edgeOffset)
            
