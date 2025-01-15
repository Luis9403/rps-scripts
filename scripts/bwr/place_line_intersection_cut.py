import clr
clr.AddReference("System.Core")
from System.Collections.Generic import List, HashSet
from pprint import pprint
from Autodesk.Revit.DB import (BuiltInCategory,
							   FilteredElementCollector, 
							   DetailLine, 
							   IntersectionResultArray, 
							   SetComparisonResult, 
							   Line, 
							   Transaction)
from Autodesk.Revit.DB import DetailElementOrderUtils as deu

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
av = doc.ActiveView
trans = Transaction(doc)

# Get All masks in view
dcs = FilteredElementCollector(doc, av.Id).OfCategory(BuiltInCategory.OST_DetailComponents)\
										.WhereElementIsNotElementType()\
										.ToElements()

masks = [x for x in dcs if x.Symbol.FamilyName == "BWR_DI_Test_Mask"]

# Get test mask family symbol
dcts = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_DetailComponents)\
										.WhereElementIsElementType()\
										.ToElements()

mask_sym = next(x for x in dcts if x.FamilyName == "BWR_DI_Test_Mask")
mask_sym.Activate()


# Get all detail lines
dls = FilteredElementCollector(doc, av.Id).OfCategory(BuiltInCategory.OST_Lines)\
										.WhereElementIsNotElementType()\
										.ToElements()
										
dls = [x for x in dls if isinstance(x.Location.Curve, Line) and x.LineStyle.Name != "BWR_FD_Pool Section Line"]




checked = dls.copy()
checked.pop(0)

intersection_results = []
for i in range(0, len(dls)-1):
	for c in checked:
		curve1 = dls[i].Location.Curve
		curve2 = c.Location.Curve
		
		interest_p = [
		curve1.GetEndPoint(0),
		curve1.GetEndPoint(1),
		curve2.GetEndPoint(0),
		curve2.GetEndPoint(1)
		]
		
		inter_array = clr.Reference[IntersectionResultArray](IntersectionResultArray())
		result = curve1.Intersect(curve2, inter_array)
		
		if result == SetComparisonResult.Overlap:
			intersection = inter_array.Item[0].XYZPoint
			for p in interest_p:
				if p.IsAlmostEqualTo(intersection):
					break
			else:
				intersection_results.append((intersection, dls[i], c))
		
	checked.pop(0)	
				

trans.Start("a")
for mask in masks:
	doc.Delete(mask.Id)
	
for p in intersection_results:
	new_mask = doc.Create.NewFamilyInstance(p[0], mask_sym, av)
	order = deu.GetDrawOrderForDetails(av, HashSet[ElementId]([p[1].Id, p[2].Id, new_mask.Id]))
	py_list = [x for x in order]
	
	deu.BringToFront(doc, av, p[1].Id)
	deu.SendToBack(doc, av, new_mask.Id)
	deu.SendToBack(doc, av, p[2].Id)
		
trans.Commit()
