from pprint import pprint
from Autodesk.Revit.DB import FilteredElementCollector, ViewSheet, Transaction

#Functions
def get_flow_diagram_from_sheet(document, sheet):
	views = [document.GetElement(x) for x in sheet.GetAllPlacedViews()]
	
	drafting_view = None
	for view in views:
		if isinstance(view, ViewDrafting) and "FD" in view.Name:
			drafting_view = view
			break
			
	return drafting_view

def get_general_data_tag(doc, view):
	gas = FilteredElementCollector(doc, view.Id).OfCategory(BuiltInCategory.OST_GenericAnnotation)\
											 .WhereElementIsNotElementType()\
											 .ToElements()
											 
	ga = next(x for x in gas if x.Symbol.FamilyName == "BWR_DI_FD_General Data")
	
	return ga
	
def get_plant_flow_from_sheet(doc, view):
	pfs = FilteredElementCollector(doc, view.Id).OfCategory(BuiltInCategory.OST_GenericAnnotation)\
											 .WhereElementIsNotElementType()\
											 .ToElements()
											 
	pf = next(x for x in pfs if x.Symbol.FamilyName == "BWR_DI_FD_Plant Flow_Data")
	
	return pf

# Main
doc = __revit__.ActiveUIDocument.Document
trans = Transaction(doc)

sheets = FilteredElementCollector(doc).OfClass(ViewSheet).WhereElementIsNotElementType().ToElements()

trans.Start("a")
for sheet in sheets:
	fd = get_flow_diagram_from_sheet(doc, sheet)
	if fd:
		ga = get_general_data_tag(doc, fd)
		pf = get_plant_flow_from_sheet(doc, sheet)
		
		name = ga.GetParameters("BWR_DI_FD_Name")[0].AsString()
		flow = ga.GetParameters("BWR_DI_FD_Flow Rate")[0].AsDouble()
		turn_over = ga.GetParameters("BWR_DI_FD_Turnover")[0].AsDouble()
		
		# Plant Flow parameters
		pf.GetParameters("BWR_FD_Note_Plant Flow_Name")[0].Set(name.upper())
		pf.GetParameters("BWR_FD_Note_Plant Flow_Flow")[0].Set(flow)
		pf.GetParameters("BWR_FD_Note_Plant Flow_Turnover")[0].Set(turn_over)
	
trans.Commit()
	
	
	
	
			
	
			