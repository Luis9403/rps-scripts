"""
Filters level by building story and creates 3rd views between levels base
on selected scope box
"""
from Autodesk.Revit.Exceptions import ArgumentException
from Autodesk.Revit.DB import BoundingBoxXYZ

BOUNDINGBOX_NAME = "Overall Building"
VIEW_3D_TEMPLATE_NAME = "FP_3D_NWC_EXP"

def create_level_3d_view(document, view_type, level, level_above, scope_box):
	
	level_el = level.Elevation
	level_above_el = level_above.Elevation
	
	sb_min = scope_box.Min
	sb_max = scope_box.Max
	
	lower_corner = XYZ(sb_min.X, sb_min.Y, level_el)
	upper_corner = XYZ(sb_max.X, sb_max.Y, level_above_el)
	
	new_bb = BoundingBoxXYZ()
	new_bb.Max = upper_corner
	new_bb.Min = lower_corner
	
	view_threed = View3D.CreateIsometric(document, view_type.Id)
	
	view_threed.SetSectionBox(new_bb)
	
	return view_threed
	

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
trans = Transaction(doc)
active_view = doc.ActiveView


levels = FilteredElementCollector(doc).OfClass(Level).WhereElementIsNotElementType().ToElements()

building_story_levels = []

for level in levels:
	building_story = level.get_Parameter(BuiltInParameter.LEVEL_IS_BUILDING_STORY)
	
	if building_story.AsInteger():
		building_story_levels.append(level)
		print("Is Building Story: ", building_story.AsValueString())

		
sorted_levels = sorted(building_story_levels, key = lambda x:x.Elevation)

view_types = FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements()
view_3d_type = next(x for x in view_types if x.ViewFamily == ViewFamily.ThreeDimensional)


scope_boxes = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_VolumeOfInterest).WhereElementIsNotElementType().ToElements()
overall_sb_el = next(x for x in scope_boxes if x.Name == BOUNDINGBOX_NAME)
print("Scope Box: ", overall_sb_el.Name)


views = FilteredElementCollector(doc).OfClass(View).ToElements()
view_templates = [x for x in views if x.IsTemplate]
view_3d_template_id = next(x.Id for x in view_templates if x.Name == VIEW_3D_TEMPLATE_NAME)
print("View Template: ", doc.GetElement(view_3d_template_id).Name)

a = len(str(len(sorted_levels)))+1


for i in range(len(sorted_levels)-1):
	try:
		trans.Start("a")
		new_3d_view = create_level_3d_view(doc,
										   view_3d_type,
										   sorted_levels[i],
										   sorted_levels[i+1],
										   overall_sb_el.get_BoundingBox(active_view))

		new_3d_view.Name =  "FP_3D_" + str(i).zfill(a) + "_" + sorted_levels[i].Name + "_NWC_EXP"

		new_3d_view.ViewTemplateId = view_3d_template_id
		trans.Commit()
	except Exception as e:
		print(e)
		trans.RollBack()
		continue









		


