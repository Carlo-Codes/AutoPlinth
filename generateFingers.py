import rhinoscriptsyntax as rs

class Generatefingers:
    def __init__(self, topOrBottom, sides):
        intersection = rs.BooleanIntersection(topOrBottom, sides, delete_input=False)
        self.splitIntersections = []
        for side in sides:
            self.splitIntersections += rs.BooleanIntersection (intersection, side, delete_input= False)
        rs.DeleteObjects(intersection)




            

