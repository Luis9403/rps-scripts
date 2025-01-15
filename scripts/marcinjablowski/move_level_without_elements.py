import clr
from System.Collections.Generic import List
from Autodesk.Revit.UI import Selection

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
trans = Transaction(doc)
trans_group = TransactionGroup(doc) 

def levelId(document, name):
	levels = FilteredElementCollector(document).OfClass(Level).ToElements()
	for level in levels:
		if level.Name == name:
			return level.Id
	return None


def getElementLocations(elements):
	locations = []
	for el in elements:
		if isinstance(el.Location, LocationCurve) and el.Location != None:
			locations.append(el.Location.Curve.Clone())
		elif el.Location != None:
			locations.append(el.Location.Point)
			
	return locations


def changeLevelElevation(document, level_id, offset):
	level = document.GetElement(level_id)
	new_level_elevation = level.Elevation + offset
	level.Elevation = new_level_elevation
	
def foundElementInGroups(element, groups):
	for group in groups:
		for member_id in group.GetMemberIds():
			if element.Id == member_id:
				return True
	return False
	
def removeGroupElementsFromList(elements):
	new_elements = [x for x in elements if not isinstance(x, Group)]
	groups = [x for x in elements if isinstance(x, Group)]
	filtered_elements = []
	
	for element in new_elements:
		if not foundElementInGroups(element, groups):
			filtered_elements.append(element)
	
	return filtered_elements
	


# MAIN
collector = FilteredElementCollector(doc)

level_id = levelId(doc, "(A2) LEVEL 20")

level_filter = ElementLevelFilter(level_id)

elements_in_level = collector.WherePasses(level_filter).ToElements()
for i in elements_in_level:
	print(i)
print(len(elements_in_level))

filtered_elements = removeGroupElementsFromList(elements_in_level)
for i in filtered_elements:
	print(i)
el_ids = [x.Id for x in filtered_elements]

uidoc.Selection.SetElementIds(List[ElementId](el_ids))


'''
a = 0
for i in elements_in_level:
	print(i.Location)
	a += 1
print(a)

elements_locations = getElementLocations(elements_in_level)
for i in elements_locations:
	print(i)

trans_group.Start("b")
trans.Start("Change Level Elevation")
changeLevelElevation(doc, level_id, 5)
trans.Commit()

trans.Start("a")
for i in range(len(elements_in_level)):
	if isinstance(elements_in_level[i].Location, LocationCurve):
		elements_in_level[i].Location.Curve = elements_locations[i]
	else:
		elements_in_level[i].Location.Point = elements_locations[i]
trans.Commit()
trans_group.Assimilate()
'''











