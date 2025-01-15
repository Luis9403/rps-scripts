# Imports
from pprint import pprint
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, FilledRegion, ViewDrafting, Transaction

# Main
doc = __revit__.ActiveUIDocument.Document
trans = Transaction(doc)

frs = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_DetailComponents)\
								  .OfClass(FilledRegion)\
								  .WhereElementIsNotElementType()\
								  .ToElements()

pool_frs = [x for x in frs if doc.GetElement(x.GetTypeId()).Name == "BWR_WaterFeature_Fill"]

dvs = FilteredElementCollector(doc).OfClass(ViewDrafting)\
								   .WhereElementIsNotElementType()\
								   .ToElements()

fds = [x for x in dvs if "FD" in x.Name]

trans.Start("fill ga")
for pool in pool_frs:
	pool_name = pool.GetParameters("BWR_FR_Name")[0].AsString()
	pool_area = pool.GetParameters("BWR_FR_Area")[0].AsDouble()
	pool_depth = pool.GetParameters("BWR_FR_Depth")[0].AsDouble()
	pool_volume = pool.GetParameters("BWR_FR_Volume")[0].AsDouble()
	pool_turnover = pool.GetParameters("BWR_FR_Pool_Turnover")[0].AsDouble()
	pool_flow_rate = pool.GetParameters("BWR_FR_Pool_Flow")[0].AsDouble()
	for fd in fds:
		fd_name = fd.Name.split("_")[-1]
		if pool_name == fd_name:
			gas = FilteredElementCollector(doc, fd.Id).OfCategory(BuiltInCategory.OST_GenericAnnotation)\
									   .WhereElementIsNotElementType()\
									   .ToElements()
			gd = next(x for x in gas if x.Name == "BWR_DI_FD_General Data")
			gd.GetParameters("BWR_DI_FD_Area")[0].Set(pool_area)
			gd.GetParameters("BWR_DI_FD_Depth")[0].Set(pool_depth)
			gd.GetParameters("BWR_DI_FD_Volume")[0].Set(pool_volume)
			gd.GetParameters("BWR_DI_FD_Turnover")[0].Set(pool_turnover)
			gd.GetParameters("BWR_DI_FD_Flow Rate")[0].Set(pool_flow_rate)
			break
			
trans.Commit()