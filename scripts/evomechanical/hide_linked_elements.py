""" Selects elements in links and hides them in the active view"""

import clr
clr.AddReference("System.Collections")

from System.Collections.Generic import List
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.UI import RevitCommandId, PostableCommand
from Autodesk.Revit.DB import FilteredElementCollector

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
trans = Transaction(doc)

active_view = doc.ActiveView

selected_refs = uidoc.Selection.PickObjects(ObjectType.LinkedElement, "Pick Elements")
link_el = 0

for i in selected_refs:
	if isinstance(doc.GetElement(i.ElementId), RevitLinkInstance):
		print(doc.GetElement(i.ElementId))
		link_el = doc.GetElement(i.ElementId)
		break
		
linked_doc = link_el.GetLinkDocument()
print(linked_doc.IsLinked)

selected_el_ids = [x.LinkedElementId for x in selected_refs]

for i in selected_el_ids:
	print(linked_doc.GetElement(i), linked_doc.GetElement(i).CanBeHidden(active_view))
	
uidoc.Selection.SetReferences(selected_refs)

uidoc.Application.PostCommand(RevitCommandId.LookupPostableCommandId(PostableCommand.HideElements))

