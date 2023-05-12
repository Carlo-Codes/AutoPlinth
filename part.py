import rhinoscriptsyntax as rs

class part:
    def __init__(self):
        self.mainGeometry = None
        self.fingers = None

    def merge(self):
        allElements = self.mainGeometry + self.fingers
        rs.BooleanUnion(allElements, delete_input=True)

    def addFingers(self, fingers):
        self.fingers+=fingers
    
    def addMainGeometry(self, geometry):
        self.mainGeometry = geometry
    

