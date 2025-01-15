from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.DB import ElementTransformUtils

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
trans = Transaction(doc)
length = 5.4

pipe_ref = uidoc.Selection.PickObject(ObjectType.Element, "Pick Pipe")
pipe = doc.GetElement(pipe_ref.ElementId)
picked_point = pipe_ref.GlobalPoint

pipe_connectors = pipe.ConnectorManager.Connectors

closest_connector = sorted(pipe_connectors, key=lambda x: x.Origin.DistanceTo(picked_point))[0]
connected_connector = [x for x in closest_connector.AllRefs if x.Owner.Id != closest_connector.Owner.Id][0]
connected_element = connected_connector.Owner
print(connected_element)
pipe_length = pipe.Location.Curve.Length

delta_l = length - pipe_length

conn_origin = closest_connector.Origin
traslation = closest_connector.CoordinateSystem.BasisZ * delta_l

trans.Start("Move connector")
ElementTransformUtils.MoveElement(doc, connected_element.Id, traslation)
trans.Commit()
