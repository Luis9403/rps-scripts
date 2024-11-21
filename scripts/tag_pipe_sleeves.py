''' Tag all penetrations in active view '''

# IMPORTS
from Autodesk.Revit.DB import (FilteredElementCollector,
								BuiltInCategory,
								IndependentTag,
								Transaction,
								TagOrientation)

# FUNCTIONS
def get_sleeves_in_active_view(document, sleeve_name):
	active_view = document.ActiveView
	pipe_accesories = FilteredElementCollector(document, active_view.Id)\
						.OfCategory(BuiltInCategory.OST_PipeAccessory)\
						.WhereElementIsNotElementType()\
						.ToElements()
	sleeves = [x for x in pipe_accesories if x.Name == sleeve_name]
	print("Sleeves in active view: ok")
	return sleeves


def get_family_symbol_by_name(doc, family_name, type_name):
	tags = FilteredElementCollector(doc)\
			.OfCategory(BuiltInCategory.OST_PipeAccessoryTags)\
			.WhereElementIsElementType()\
			.ToElements()
			
	tag = next(x for x in tags if x.FamilyName == family_name and x.Name == type_name)
	print("Family Symbol by name: ok")
	return tag

def transfer_associated_height(sleeve):
	print(sleeve.Id)
	pipe = sleeve.Host
	print(pipe)
	elevation = pipe.LevelOffset
	elevation_param = next(x for x in sleeve.Parameters if x.Definition.Name == "EVO_Sleeve_Height_TOS")
	elevation_param.Set(elevation)
	print("Transfer associated height: ok")

def transfer_associated_level_elevation(sleeve):
	pipe = sleeve.Host
	level = pipe.ReferenceLevel
	elevation = level.Elevation
	level_el_param = next(x for x in sleeve.Parameters if x.Definition.Name == "EVO_Sleeve_TOS")
	level_el_param.Set(elevation)
	print("Transfer associated level: ok")

def assign_fp_system(document, sleeve):
	pipe = sleeve.Host
	system_name = document.GetElement(pipe.MEPSystem.GetTypeId()).Name
	system_param = next(x for x in sleeve.Parameters if x.Definition.Name == "EVO_Sleeve_FP_System")
	
	if system_name == "02_FP_WET_SPRINKLER":
		system_param.Set("FP-SPK")
	elif system_name == "00_FP_WET_STAND PIPE":
		system_param.Set("FP-STP")
	elif system_name == "04_FP_DRY_SPRINKLER":
		system_param.Set("FP-DRY")
	elif system_name == "01_FP_STAND PIPE_DRAINAGE":
		system_param.Set("FP-DR")
	print("FP system assign: ok")
		
def offset_point(point, offset_x, offset_y):
	offset_vector = XYZ(offset_x, offset_y, 0)
	print(point)
	print(offset_vector)
	new_point = point.Add(offset_vector)
	print(new_point)
	return new_point
	print("Point offset: ok")
		
# MAIN	
PIPE_SLEEVE_NAME = "Pipe_Sleeve"
SLEEVE_TAG_NAME = "EVO_Sleeve_Tag"

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
trans = Transaction(doc)
av = doc.ActiveView

sleeves = get_sleeves_in_active_view(doc, PIPE_SLEEVE_NAME)
valid_sleeves = [x for x in sleeves if x.Host != None]

# Fill parameters for sleeve instances
trans.Start("Transfer height")
for sl in valid_sleeves:
	transfer_associated_height(sl)
	transfer_associated_level_elevation(sl)
	assign_fp_system(doc, sl)

trans.Commit()

# Place sleeves tags in active view
sleeve_tag = get_family_symbol_by_name(doc, SLEEVE_TAG_NAME, "Horizontal")

trans.Start("Tag sleeves")
for sl in valid_sleeves:
	sleeve_loc = sl.Location.Point
	coord = offset_point(sleeve_loc, 2, 2)
	elbow_loc = offset_point(coord, -1, 0)
	ref = Reference(sl)
	tag = IndependentTag.Create(doc, 
								sleeve_tag.Id, 
								av.Id,
								ref,
								True,
								TagOrientation.Horizontal,
								sleeve_loc)
	tag.TagHeadPosition = coord
	tag.SetLeaderElbow(ref, elbow_loc)
trans.Commit()
	
	
	





