from pprint import pprint
from collections import OrderedDict
from Autodesk.Revit.DB import FilteredElementCollector, ViewDrafting, BuiltInCategory, Transaction, UnitUtils, UnitTypeId


def get_fd_views(document):
	dvs = FilteredElementCollector(document).OfClass(ViewDrafting)\
										   .WhereElementIsNotElementType()\
										   .ToElements()
	
	fds = [x for x in dvs if isinstance(x, ViewDrafting) and "FD" in x.Name]
	return fds

def general_data_family(document, view):
	dis = FilteredElementCollector(document, view.Id).OfCategory(BuiltInCategory.OST_GenericAnnotation)\
												.WhereElementIsNotElementType()\
												.ToElements()
												
	gd = next(x for x in dis if x.Symbol.FamilyName == "BWR_DI_FD_General Data")

	return gd

def get_suction_tags(doc, view):

	suction_side = [
		"Sump_Outlet",
		"Balance_Tank"
	]
	
	dis = FilteredElementCollector(doc, view.Id).OfCategory(BuiltInCategory.OST_GenericAnnotation)\
												.WhereElementIsNotElementType()\
												.ToElements()
												
	sts = []
	for di in dis:
		for s in suction_side:
			family_name = di.Symbol.FamilyName
			instance_name = di.Name
			
			if family_name == "BWR_DI_Tag_Line Diameter" and instance_name == s:
				sts.append(di)
	
	return sts

def get_discharge_tags(doc, view):

	discharge_side = [
		"Untreated_Water",
		"Filtered_Water"
	]
	
	dis = FilteredElementCollector(doc, view.Id).OfCategory(BuiltInCategory.OST_GenericAnnotation)\
												.WhereElementIsNotElementType()\
												.ToElements()
												
	dts = []
	for di in dis:
		for s in discharge_side:
			family_name = di.Symbol.FamilyName
			instance_name = di.Name
			
			if family_name == "BWR_DI_Tag_Line Diameter" and instance_name == s:
				dts.append(di)
	
	return dts

	
# Main
doc = __revit__.ActiveUIDocument.Document
trans = Transaction(doc)

diameters = OrderedDict([
	("40", (7.52, 12.53)),
	("50", (11.82, 19.71)),
	("80", (27.48, 45.81)),
	("100", (45.61, 76.01)),
	("150", (99.02, 165.04)),
	("200", (171.1, 285.01))
])


fds = get_fd_views(doc)
# Adjust diamter as per flow

trans.Start("a")
for fd in fds:
	print("View Name: ", fd.Name)
	gd = general_data_family(doc, fd)
	print("General Data: ", gd)
	flow = float(gd.GetParameters("BWR_DI_FD_Flow Rate")[0].AsValueString().split()[0])
	print("Flow: ", flow)
	
	discharge_diameter = 0
	suction_diameter = 0
	
	
	for key, value in diameters.items():
		if value[0] > flow:
			suction_diameter = float(key)
			break
	
	
			
	for key, value in diameters.items():
		if value[1] > flow:
			discharge_diameter = float(key)
			break

	
	
	if suction_diameter == discharge_diameter:
		temp = iter(diameters)
		for key in temp:
			if key == str(int(suction_diameter)):
				suction_diameter = next(temp)	
	

	suction_tags = get_suction_tags(doc, fd)
	discharge_tags = get_discharge_tags(doc, fd)
	print("Suction Diameter: ", suction_diameter)
	print("Discharge Diameter: ", discharge_diameter)
	
	for st in suction_tags:
		st.GetParameters("BWR_Line_Diameter")[0].Set(float(suction_diameter))
	
	for dt in discharge_tags:
		dt.GetParameters("BWR_Line_Diameter")[0].Set(float(discharge_diameter))
		
trans.Commit()



