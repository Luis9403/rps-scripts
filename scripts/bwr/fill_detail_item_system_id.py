from Autodesk.Revit.DB import ViewDrafting, Transaction

doc = __revit__.ActiveUIDocument.Document
trans = Transaction(doc)

dvs = FilteredElementCollector(doc).OfClass(ViewDrafting).WhereElementIsNotElementType().ToElements()

trans.Start("Mod")
for dv in dvs:
	if isinstance(dv, ViewDrafting):
		name = dv.Name
		if "FD" in name:
			splited = name.split("_")
			di_id = splited[1] + "_" + splited[2]
			
			dis = FilteredElementCollector(doc, dv.Id).OfCategory(BuiltInCategory.OST_DetailComponents)\
			.WhereElementIsNotElementType().ToElements()
			
			for di in dis:
				system_id = di.GetParameters("BWR_DI_Equipment_System ID")[0].Set(di_id)

trans.Commit()
		