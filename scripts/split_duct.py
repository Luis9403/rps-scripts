from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.DB.Mechanical import MechanicalUtils

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
trans = Transaction(doc)

duct_ref = uidoc.Selection.PickObject(ObjectType.Element, "Pick a Duct")
print(duct_ref)

duct_id = duct_ref.ElementId
print(duct_id)
duct_el = doc.GetElement(duct_id)
print(duct_el)

duct_line = duct_el.Location.Curve
print(duct_line)

number_of_cuts = 8
line_length = duct_line.Length
print("Line Length:", line_length)

tram_length = line_length / number_of_cuts
tram_length_norm = tram_length / line_length
print("Tram Length:", tram_length)
print("Tram Length Normalized:",tram_length_norm)

cut_points = []
tram = tram_length_norm
print(tram)
for i in range(number_of_cuts-1):
	point = duct_line.Evaluate(tram, True)
	cut_points.append(point)
	tram = tram + tram_length_norm
	print(point)
	print(tram)
	
trans.Start("a")
for point in cut_points:
	new_duct = MechanicalUtils.BreakCurve(doc, duct_id, point)	
trans.Commit()
	