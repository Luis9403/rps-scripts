from Autodesk.Revit.DB import FilteredElementCollector, RevitLinkInstance, BuiltInCategory, Document, ElementId, Level
from Autodesk.Revit.DB.Structure import StructuralType
from Autodesk.Revit.UI.Selection import ObjectType, ISelectionFilter

BUILT_IN_CATEGORY = BuiltInCategory.OST_Sprinklers

class RevitLinkSelectionFilter(ISelectionFilter):

	def AllowElement(self, element):
		if isinstance(element, RevitLinkInstance):
			return True
		return False
		
	def AllowReference(self, reference):
		return False
		

def get_level_above(document, level):
	collector = FilteredElementCollector(document)
	levels = collector.OfCategory(BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements()
	
	level_el = level.ProjectElevation
	min_level = 0
	min_distance = float("inf")
	for other_level in levels:
		if other_level.ProjectElevation > level_el:
			distance = other_level.ProjectElevation - level_el
			if distance < min_distance:
				min_level = other_level
				min_distance = distance
	
	return min_level

def get_spk_between_levels(spks, current_level, above_level):
	current_level_el = current_level.ProjectElevation
	above_level_el = above_level.ProjectElevation
	
	filtered_spks = []
	for spk in spks:
		spk_el = spk.Location.Point.Z
		if spk_el < above_level_el and spk_el > current_level_el:
			filtered_spks.append(spk)
			
	return filtered_spks
	
def get_spk_first_family_symbol(document):
	collector = FilteredElementCollector(document)
	
	spk_types = collector.OfCategory(BuiltInCategory.OST_Sprinklers).WhereElementIsElementType().ToElements()
	
	return spk_types

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
trans = Transaction(doc)

link_selection_filter = RevitLinkSelectionFilter()
active_view = doc.ActiveView

current_level = active_view.GenLevel
above_level = get_level_above(doc, current_level)



link_ref = uidoc.Selection.PickObject(ObjectType.Element, link_selection_filter, "Pick a Link")
print(link_ref)

revit_link_doc = doc.GetElement(link_ref.ElementId)
print(revit_link_doc)


link_collector = FilteredElementCollector(revit_link_doc.GetLinkDocument())

spk_heads = link_collector.OfCategory(BUILT_IN_CATEGORY).WhereElementIsNotElementType().ToElements()

spk_heads_in_view = get_spk_between_levels(spk_heads, current_level, above_level)
elev = XYZ(0,0,current_level.ProjectElevation)

spk_coords = [x.Location.Point - elev for x in spk_heads_in_view]



spk_types = get_spk_first_family_symbol(doc)

trans.Start("Create new heads")

for coord in spk_coords:
	doc.Create.NewFamilyInstance.Overloads[XYZ, FamilySymbol, Level, StructuralType](coord, spk_types[1], current_level, StructuralType.NonStructural)
	
trans.Commit()






