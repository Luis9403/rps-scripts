from System.Collections.Generic import List
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.DB import ElementTransformUtils, Transaction, CopyPasteOptions, ElementId

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
trans = Transaction(doc)
av = doc.ActiveView

sc = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_VolumeOfInterest).WhereElementIsNotElementType().ToElements()
print(sc)
el_ref = uidoc.Selection.PickObject(ObjectType.LinkedElement, "Pick element to copy")
el_id = el_ref.LinkedElementId

link = doc.GetElement(el_ref.ElementId)
link_doc = link.GetLinkDocument()
t = link.GetTransform()
print(link_doc)

el_ids = [el_id]
copy_opt = CopyPasteOptions()

trans.Start("Copy")
ElementTransformUtils.CopyElements(link_doc, List[ElementId](el_ids), doc, t, copy_opt)
trans.Commit()