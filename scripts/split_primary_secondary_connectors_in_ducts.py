from Autodesk.Revit.UI.Selection import *

uiapp = __revit__
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

duct_ref = uidoc.Selection.PickObject(ObjectType.Element, "Pick Duct")

duct_el = doc.GetElement(duct_ref.ElementId)

duct_conns = duct_el.ConnectorManager.Connectors
duct_line = duct_el.Location.Curve

sp = duct_line.GetEndPoint(0)
ep = duct_line.GetEndPoint(1)

main_conns = []
secondary_conns = []

for conn in duct_conns:
	if conn.Origin.IsAlmostEqualTo(sp) or conn.Origin.IsAlmostEqualTo(ep):
		main_conns.append(conn)
		
	else:
		secondary_conns.append(conn)
		
for i in secondary_conns:
	u = duct_line.Project(i.Origin).Parameter / duct_line.Length
	print(u)
		