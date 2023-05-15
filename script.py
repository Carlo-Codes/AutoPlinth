import Rhino
import scriptcontext
from selections import Selection
from generateFingers import Generatefingers


## adding ribs!!

selection =  Selection()
topIntersctions = Generatefingers(selection.topFace, selection.sideFaces)
