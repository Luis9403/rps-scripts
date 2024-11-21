from Autodesk.Revit.UI.Selection import ObjectType, ISelectionFilter
from Autodesk.Revit.Exceptions import OperationCanceledException


class PipeAccesorySelectionFilter(ISelectionFilter):
	def AllowElement(self, element):
		if element.Category.Name == "Pipe Accessories":
			return True
		else:
			return False
	
	def AllowReference(self, reference):
		return False


def transfer_associated_height(sleeve):
	pipe = sleeve.Host
	elevation = pipe.LevelOffset
	elevation_param = next(x for x in sleeve.Parameters if x.Definition.Name == "EVO_Sleeve_Height_TOS")
	elevation_param.Set(elevation)


def transfer_associated_level_elevation(sleeve):
	pipe = sleeve.Host
	level = pipe.ReferenceLevel
	elevation = level.Elevation
	level_el_param = next(x for x in sleeve.Parameters if x.Definition.Name == "EVO_Sleeve_TOS")
	level_el_param.Set(elevation)

def assign_fp_system(document, sleeve):
	pipe = sleeve.Host
	system_name = document.GetElement(pipe.MEPSystem.GetTypeId()).Name
	print(system_name)
	system_param = next(x for x in sleeve.Parameters if x.Definition.Name == "EVO_Sleeve_FP_System")
	
	if system_name == "02_FP_WET_SPRINKLER":
		system_param.Set("FP-SPK")
	elif system_name == "00_FP_WET_STAND PIPE":
		system_param.Set("FP-STP")
	elif system_name == "04_FP_DRY_SPRINKLER":
		system_param.Set("FP-DRY")


uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
trans = Transaction(doc)
pipe_a_filter = PipeAccesorySelectionFilter()

while True:
	try:
		ref = uidoc.Selection.PickObject(ObjectType.Element, pipe_a_filter, "Pick sleeve")
		sleeve = doc.GetElement(ref.ElementId)
		
		trans.Start("Change parameter value")
		transfer_associated_height(sleeve)
		transfer_associated_level_elevation(sleeve)
		assign_fp_system(doc, sleeve)
		trans.Commit()
	
	except OperationCanceledException:
		break


