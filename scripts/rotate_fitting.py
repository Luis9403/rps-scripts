from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.DB import ElementTransformUtils, Transaction

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
trans = Transaction(doc)

ref1 = uidoc.Selection.PickObject(ObjectType.Element, "Pick element")

el = doc.GetElement(ref1.ElementId)

connector_set = el.MEPModel.ConnectorManager.Connectors
axis = 0

for conn in connector_set:
	if conn.IsConnected:
		transform = conn.CoordinateSystem
		z = transform.BasisZ
		point1 = conn.Origin
		vector = z.Multiply(10)
		point2 = point1.Add(vector)
		
		axis = Line.CreateBound(point1, point2)


trans.Start("a")
ElementTransformUtils.RotateElement(doc, ref1.ElementId, axis, -0.5)
trans.Commit()