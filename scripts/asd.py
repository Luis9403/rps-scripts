import math
from Autodesk.Revit.UI.Selection import ObjectType

class Dlf():
	def __init__(self, a, b):
		self.a = a
		self.b = b
	
	def evaluate(self, x):
		return self.a * x + self.b


def get_secondary_connectors(duct):
	
	secondary_connectors = []
	connector_set = duct.ConnectorManager.Connectors
	duct_line = duct.Location.Curve
	start_point = duct_line.GetEndPoint(0)
	end_point = duct_line.GetEndPoint(1)
	
	for conn in connector_set:
		conn_loc = conn.Origin
		if not(conn_loc.IsAlmostEqualTo(start_point)) and not(conn_loc.IsAlmostEqualTo(end_point)):
			secondary_connectors.append(conn)
	
	return secondary_connectors
	
def get_inserts_range(duct, range):
	ranges = []
	sec_conns = get_secondary_connectors(duct)
	sec_conns_loc = [x.Origin for x in sec_conns]
	
	dsp = duct.Location.Curve.GetEndPoint(0)
	
	for loc in sec_conns_loc:
		dist = dsp.DistanceTo(loc)
		ranges.append((dist - range, dist + range))
		
	return ranges
		
	
	
####### MAIN #######
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

duct_ref = uidoc.Selection.PickObject(ObjectType.Element, "Pick it")
duct_el = doc.GetElement(duct_ref.ElementId)

duct_line = duct_el.Location.Curve
trams = []

length = duct_line.Length
tram_length = 3
n = math.floor(length / tram_length)
min_dist_to_end = 1
min_dist_to_inserts = 1
m = 1

inserts_range = get_inserts_range(duct_el, 1)

b = tram_length
dlf = Dlf(tram_length, b)

for i in range(n):
	tram = dlf.evaluate(i)
	for ir in inserts_range:
		if tram > ir[0] and tram < ir[1]:
			rest = tram - ir[0]
			b = b - rest
			if b <= min_dist_to_end:
				trams.append(min_dist_to_end)
				b = m * min_distance_to_end + tram_length
				dlf.b = b
		    	m = m + 1
		    	n = n - 1
		    	i = 0
		    	
			






