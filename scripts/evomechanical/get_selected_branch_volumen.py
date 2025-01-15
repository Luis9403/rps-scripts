from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory

def calculate_volume(inside_diameter, length):
	area = (3.14 * inside_diameter**2) / 4
	return (area * length) * 7.48
	
	

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

sel_els = uidoc.Selection.GetElementIds()
pipes = FilteredElementCollector(doc, sel_els).OfCategory(BuiltInCategory.OST_PipeCurves).ToElements()

volume = 0
for pipe in pipes:
	inside_diameter = pipe.Parameter[BuiltInParameter.RBS_PIPE_INNER_DIAM_PARAM].AsDouble()
	print(inside_diameter)
	length = pipe.Parameter[BuiltInParameter.CURVE_ELEM_LENGTH].AsDouble()
	print(length)
	volume += calculate_volume(inside_diameter, length)
	
print("Volume: ", volume)
	