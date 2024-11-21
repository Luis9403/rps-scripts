from Autodesk.Revit.UI.Selection import ObjectType

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
trans = Transaction(doc)

ref = uidoc.Selection.PickObject(ObjectType.Element, "Pick Object")

trans.Start("Delete")
doc.Delete(ref.ElementId)
trans.Commit()