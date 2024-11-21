''' THis script dimensions all sleeve in active view'''


# IMPORTS
import math
from Autodesk.Revit.DB import Transaction, FilteredElementCollector, ReferenceArray, Line, XYZ
from Autodesk.Revit.UI.Selection import ObjectType

# FUNCTIONS
def get_sleeves_in_active_view(document):

	sleeves = []
	active_view = document.ActiveView
	collector = FilteredElementCollector(document, active_view.Id)
	pipe_accesories = collector.OfCategory(BuiltInCategory.OST_PipeAccessory)\
							   .WhereElementIsNotElementType()\
							   .ToElements()
	
	for pipe_accessory in pipe_accesories:
		if pipe_accessory.Name == "Pipe_Sleeve":
			sleeves.append(pipe_accessory)
	
	return sleeves
	
def get_grids_in_active_view(document):
	active_view = document.ActiveView
	collector = FilteredElementCollector(document, active_view.Id)
	grids = collector.OfCategory(BuiltInCategory.OST_Grids)\
							   .WhereElementIsNotElementType()\
							   .ToElements()
	
	return grids
	
def get_closest_parallel_grid(sleeve, grids):
	sl_dir = sleeve.FacingOrientation
	coord = sleeve.Location.Point
	parallel_grids = []
	
	for grid in grids:
		grid_line = grid.Curve
		grid_direction = grid_line.Direction
		angle = sl_dir.AngleTo(grid_direction)
		
		if MathComparisonUtils.IsAlmostEqual(angle, 0) or MathComparisonUtils.IsAlmostEqual(angle, math.pi):
			parallel_grids.append(grid)
	
	dist_min = float("inf")
	closest_grid = None
	for grid in parallel_grids:
		grid_line = grid.Curve
		dist = grid_line.Project(coord).Distance
		
		if dist_min > dist:
			dist_min = dist
			closest_grid = grid
			
	return closest_grid, closest_grid.Curve.Project(coord).XYZPoint

# MAIN
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
av = doc.ActiveView
trans = Transaction(doc)

sleeves = get_sleeves_in_active_view(doc)
grids = get_grids_in_active_view(doc)

sl_ref = sleeves[0].GetReferences(FamilyInstanceReferenceType.StrongReference)[0]
closest_grid, point_on_grid = get_closest_parallel_grid(sleeves[0], grids)
grid_ref = Reference(closest_grid)
print(closest_grid.Name)

refs = ReferenceArray()
refs.Append(grid_ref)
print(sl_ref.ConvertToStableRepresentation(doc))
refs.Append(sl_ref)
print(grid_ref.ConvertToStableRepresentation(doc))

point1 = sleeves[0].Location.Point
print(point1)
direction = XYZ(0,-1,0)
point2 = point_on_grid
point = point2
line = Line.CreateUnbound(point, direction)
print(point2)

trans.Start("a")
doc.Create.NewDimension(av, line, refs)
trans.Commit()




