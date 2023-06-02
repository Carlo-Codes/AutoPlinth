import Rhino
import scriptcontext
from generateFingers import Generatefingers
from selections import Selection



## adding ribs!!

selection =  Selection()
topIntersctions = Generatefingers(selection.topFace, selection.sideFaces,10, 2,20,50)
print("test")