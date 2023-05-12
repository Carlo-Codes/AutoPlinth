import Rhino
import scriptcontext
from selections import Selection
from generateFingers import Generatefingers
import rhinoscriptsyntax as rs

## adding ribs!!

selection =  Selection()
topIntersctions = Generatefingers(selection.topFace, selection.sideFaces)
