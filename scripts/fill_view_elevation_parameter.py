uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

collector = FilteredElementCollector(doc)

views = collector.OfCategory(BuiltInCategory.OST_Views).WhereElementIsNotElementType().ToElements()

floorplan_views = [x for x in views if x.ViewType == ViewType.FloorPlan and not x.IsTemplate ]

levels = [x.GenLevel for x in floorplan_views]

elevations = []
for level in levels:
	for param in level.Parameters:
		if param.Definition.Name == "Elevation":
			elevations.append(param.AsValueString())

i = 0
for view in floorplan_views:
	for param in view.Parameters:
		if param.Definition.Name == "EVO_View_Level_Elevation":
			param.SetValueString(elevations[i])
	i += 1

			
			
