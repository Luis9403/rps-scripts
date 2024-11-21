from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.DB import Transaction

uiapp = __revit__
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
trans = Transaction(doc)

def get_closest_connectors(connector_set1, connector_set2):
	min_distance = float("inf")
	closest_connectors = [0, 0]
	
	for conn1 in connector_set1:
		conn_loc1 = conn1.Origin
		for conn2 in connector_set2:
			conn_loc2 = conn2.Origin
			dist = conn_loc1.DistanceTo(conn_loc2)
			
			if dist < min_distance:
				min_distance = dist
				closest_connectors[0] = conn1
				print("a")
				closest_connectors[1] = conn2
				
	return closest_connectors
			

#**** Main ****#
ref1 = uidoc.Selection.PickObject(ObjectType.Element, "Pick ref1")
ref2 = uidoc.Selection.PickObject(ObjectType.Element, "Pick ref2")

el1 = doc.GetElement(ref1.ElementId)
el2 = doc.GetElement(ref2.ElementId)

connector_set1 = el1.ConnectorManager.Connectors
connector_set2 = el2.ConnectorManager.Connectors

closest_connectors = get_closest_connectors(connector_set1, connector_set2)
for i in closest_connectors: print(i)

trans.Start("a")
doc.Create.NewTransitionFitting(closest_connectors[0], closest_connectors[1])
trans.Commit()