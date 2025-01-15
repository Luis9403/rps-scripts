from Autodesk.Revit.DB import BuiltInCategory, Transaction, UnitUtils, UnitTypeId

doc = __revit__.ActiveUIDocument.Document
trans = Transaction(doc)

frs = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_DetailComponents)\
								  .OfClass(FilledRegion)\
								  .WhereElementIsNotElementType()\
								  .ToElements()
								  

# get area parameter
trans.Start("Fill Areas")
for fr in frs:
	area = fr.get_Parameter(BuiltInParameter.HOST_AREA_COMPUTED).AsDouble()
	depth = fr.GetParameters("BWR_FR_Depth")[0].AsDouble()
	fr.GetParameters("BWR_FR_Volume")[0].Set(depth * area)
	fr.GetParameters("BWR_FR_Area")[0].Set(area)
	volume = fr.GetParameters("BWR_FR_Volume")[0].AsDouble()
	turnover = fr.GetParameters("BWR_FR_Pool_Turnover")[0].AsDouble()
	fr.GetParameters("BWR_FR_Pool_Flow")[0].Set(volume / turnover)
	

trans.Commit()

# get perimeter
trans.Start("Fill Perimeters")
for fr in frs:
	curve_loops = fr.GetBoundaries()
	total_length = 0
	for curve_loop in curve_loops:
		for line in curve_loop:
			total_length += line.Length
			
	custom_per = fr.GetParameters("BWR_FR_Perimeter")[0].Set(total_length)
	
trans.Commit()
		