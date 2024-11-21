from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.Exceptions import InvalidOperationException
from Autodesk.Revit.DB import FamilyInstance, MEPCurve, Domain, ConnectorType, MEPModel
from Autodesk.Revit.DB.Mechanical import MechanicalEquipment
from System.Collections.Generic import List

###### FUNCTIONS ######

def get_connectors(element):
	
		if isinstance(element, FamilyInstance):
			if element.MEPModel:
				return element.MEPModel.ConnectorManager.Connectors
			else:
				raise Exception("The element don't have MEP model")
		
		return element.ConnectorManager.Connectors
	
def get_connected_elements(element):
	connected_elements = []
	connectors = get_connectors(element)
	for connector in connectors:
		if not connector.IsConnected or connector.Domain != Domain.DomainHvac:
			continue
		
		connected_connectors = connector.AllRefs
		for conn in connected_connectors:
			if conn.Owner.Id != element.Id and conn.ConnectorType != ConnectorType.Logical:
				connected_elements.append(conn.Owner)
		
	return connected_elements
	

def get_connected_graph(element):
	elements_graph = []
	visited = set()
	stack = [element]
	
	while stack:
	    current_element = stack.pop()
	    if current_element.Id not in visited:
	        visited.add(current_element.Id)
	        elements_graph.append(current_element)
	        connected_elements = get_connected_elements(current_element)
	        for ce in connected_elements:
	            if ce.Id not in visited:
	                stack.append(ce)
	
	return elements_graph
			

def enumerate_hvac_elements(elements):
	
	tag_list = []
	fn = 0
	dn = 0
	for i in range(len(elements)):
		if isinstance(elements[i], FamilyInstance):
			if elements[i].Category.Name == "Duct Fittings":
				tag_list.append(fn)
				fn += 1
			continue
			
		tag_list.append(dn)
		dn += 1
		
	return tag_list

def compare_duct_fittings(duct_fitting1, duct_fitting2):
	
	duct_fitting_size1 = duct_fitting1.GetParameters("Size")
	duct_fitting_size2 = duct_fitting2.GetParameters("Size")
	

###### MAIN ######

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

ref1 = uidoc.Selection.PickObject(ObjectType.Element, "Pick")
print(ref1)
first_el = doc.GetElement(ref1.ElementId)
print(first_el)

connected_graph = get_connected_graph(first_el)
el_ids = [x.Id for x in connected_graph]

		
el_collection = List[ElementId](el_ids)

labels = enumerate_hvac_elements(connected_graph)
print(len(labels))

for i in labels:
	print(i)
	
	
	



	
	
	
	
