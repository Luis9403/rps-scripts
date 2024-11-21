"""Convert ups and downs to evo up and downs"""

doc = __revit__.ActiveUIDocument.Document
active_view = doc.ActiveView

trans = Transaction(doc)

collector_active_view = FilteredElementCollector(doc, active_view.Id)
collector = FilteredElementCollector(doc)

tags_types = collector.OfCategory(BuiltInCategory.OST_PipeTags).WhereElementIsElementType().ToElements()
tags = collector_active_view.OfClass(IndependentTag).WhereElementIsNotElementType().ToElements()


def get_pipe_tag_type(tags, family_name, name):
	for e in tags:
		if e.FamilyName == family_name and e.Name == name:
			return e

tag_up = get_pipe_tag_type(tags_types, "EVO_Drop_Pipe_Size_Cut_Length_Tag", "00_NE_UP")
tag_dn = get_pipe_tag_type(tags_types, "EVO_Drop_Pipe_Size_Cut_Length_Tag", "01_NE_DN")


trans.Start("Convert pipe tags")
for a in tags:
	if "UP" in a.TagText:
		parameter = a.LookupParameter("Type")
		parameter.Set(tag_up.Id)
	elif "DN" in a.TagText:
		parameter = a.LookupParameter("Type")
		parameter.Set(tag_dn.Id)
		
trans.Commit()