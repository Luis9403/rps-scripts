from Autodesk.Revit.UI.Selection import ObjectType

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

pipe_ids = uidoc.Selection.GetElementIds()

pipes = [doc.GetElement(x) for x in pipe_ids]

length = 0
for pipe in pipes:
	length += pipe.Location.Curve.Length
	
print(length)

