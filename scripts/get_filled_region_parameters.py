from Autodesk.Revit.DB import FilledRegion, BuiltInParameter
from Autodesk.Revit.UI.Selection import ObjectType

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

DEPTH = 0.3

fr_refs = uidoc.Selection.PickObjects(ObjectType.Element, "Pick Filled Regions")

frs = [doc.GetElement(x.ElementId) for x in fr_refs]

areas = [x.get_Parameter(BuiltInParameter.HOST_AREA_COMPUTED) for x in frs]

for fr in frs:
	curve_loop = fr.GetBoundaries()
	for line in lines:
		pass


