import clr
from Autodesk.Revit.DB import Transaction, FamilyInstanceReferenceType, ReferenceArray, XYZ, Line, IntersectionResultArray
from Autodesk.Revit.UI.Selection import ObjectType

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
active_view = doc.ActiveView
trans = Transaction(doc)

grid_ref1 = uidoc.Selection.PickObject(ObjectType.Element, "Pick grid1")
grid_ref2 = uidoc.Selection.PickObject(ObjectType.Element, "Pick grid2")
grid_ref3 = uidoc.Selection.PickObject(ObjectType.Element, "Pick grid3")

grid1 = doc.GetElement(grid_ref1.ElementId)
grid2 = doc.GetElement(grid_ref2.ElementId)
grid3 = doc.GetElement(grid_ref3.ElementId)

dimension_refs = ReferenceArray()
dimension_refs.Append(grid_ref1)
dimension_refs.Append(grid_ref2)
dimension_refs.Append(grid_ref3)

line_start_point = grid_ref1.GlobalPoint
print(line_start_point)
line_direction = XYZ(0,1,0)

dimension_line = Line.CreateUnbound(line_start_point, line_direction)

trans.Start("a")
doc.Create.NewDimension(active_view, dimension_line, dimension_refs)
trans.Commit()





