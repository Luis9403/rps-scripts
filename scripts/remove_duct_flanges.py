##### IMPORTS #####
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.DB import Transaction, PartType

##### GLOBALS #####
uiapp = __revit__
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
trans = Transaction(doc)

##### FUNCTIONS #####

def get_connected_elements(connector_set):
	
	connected_el = []
	
	for conn1 in connector_set:
		if conn1.IsConnected:
			connected_set = conn1.AllRefs
			for conn2 in connected_set:
				if conn1.Owner.Id != conn2.Owner.Id:
					connected_el.append(conn2.Owner)
				
	return connected_el
	
def get_connected_connector(connector):
	connectors = connector.AllRefs
	for conn in connectors:
		if connector.Owner.Id != conn.Owner.Id:
			return conn


##### MAIN #####
duct_ref1 = uidoc.Selection.PickObject(ObjectType.Element, "a")
duct1 = doc.GetElement(duct_ref1.ElementId)

duct1_conn = duct1.ConnectorManager.Connectors
duct1_conn_el = get_connected_elements(duct1_conn)

# get unions
unions = []
for el in duct1_conn_el:
	if el.MEPModel != None and el.MEPModel.PartType == PartType.Union:
		unions.append(el)


# get outer ducts
outer_ducts = []
for union in unions:
	connector_set = union.MEPModel.ConnectorManager.Connectors
	connected_el = get_connected_elements(connector_set)
	for el in connected_el:
		if el.Id != duct1.Id:
			print(el)
			outer_ducts.append(el)

conns = []
i = 0
for duct in outer_ducts:
	connector_set = duct.ConnectorManager.Connectors
	for conn in connector_set:
		if conn.IsConnected:
			connected_conn = get_connected_connector(conn)
			if connected_conn.Owner.Id != unions[i].Id:
				print(conn)
				conns.append(connected_conn)
		else:
			print(conn)
			conns.append(conn.Origin)
	
	i += 1

trans.Start("remove unions and ducts")
el_remove = unions + outer_ducts
for el in el_remove:
	doc.Delete(el.Id)
trans.Commit()

	
trans.Start("Merge Duct")
duct_conn = [x for x in duct1_conn]
for i in range(len(duct_conn)):
	try:
		if isinstance(conns[i], Connector):
			duct_conn[i].Origin = conns[i].Origin
			duct_conn[i].ConnectTo(conns[i])
		else:
			duct_conn[i].Origin = conns[i]
	except:
		break
trans.Commit()


	

