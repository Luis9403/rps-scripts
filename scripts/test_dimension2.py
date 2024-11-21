from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.DB import Transaction, XYZ, Line, ReferenceArray


uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
active_view = doc.ActiveView
trans = Transaction(doc)

grid_ref = uidoc.Selection.PickObject(ObjectType.Element, "Pick grid")
print(grid_ref.ConvertToStableRepresentation(doc))

sl_ref = uidoc.Selection.PickObject(ObjectType.Element, "Pick sleeve")
sl = doc.GetElement(sl_ref.ElementId)
sl_center_ref = sl.GetReferences(FamilyInstanceReferenceType.StrongReference)[0]
print(sl_center_ref.ConvertToStableRepresentation(doc))

refs = ReferenceArray()
refs.Append(grid_ref)
refs.Append(sl_center_ref)

# Create dimension position line
p1 = grid_ref.GlobalPoint
direction = XYZ(0,1,0)
line = Line.CreateUnbound(p1, direction)

trans.Start("Create dimension")
doc.Create.NewDimension(active_view, line, refs)
trans.Commit()