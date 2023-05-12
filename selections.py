import rhinoscriptsyntax as rs

class Selection:
    def __init__(self):
        self.topFace = rs.GetObjects(message= "Select The Top Faces", filter=16, maximum_count= 1)
        rs.LockObject(self.topFace)
        self.bottomFace = rs.GetObjects(message= "Select The Bottom faces", filter=16, maximum_count= 1)
        rs.LockObject(self.bottomFace)
        self.ribs = rs.GetObjects(message="Select Ribs", filter=16)
        if self.ribs:
            rs.LockObjects(self.ribs)
        self.sideFaces = rs.GetObjects(message= "Select The Side Faces", filter=16, minimum_count= 2)

        
        rs.UnlockObjects(self.topFace)
        rs.UnlockObjects(self.bottomFace)
        if self.ribs:
            rs.UnlockObjects(self.ribs)
        
