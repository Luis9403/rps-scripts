# Imports
import math
from Autodesk.Revit.DB import Transaction, BuiltInCategory, BuiltInParameter
from Autodesk.Revit.DB import MathComparisonUtils as mcu

# Fucntions
def get_plane_line_intersection(plane, line):
	plane_origin = plane.Origin
	line_origin = line.GetEndPoint(0)
	plane_normal = plane.Normal
	line_direction = line.Direction
	d = ((plane_origin - line_origin).DotProduct(plane_normal))/(line_direction.DotProduct(plane_normal))
	return line_origin + line_direction.Multiply(d)
	
	
# Main
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
trans = Transaction(doc)
av = doc.ActiveView

# Get all pipes in view
av_collector = FilteredElementCollector(doc, av.Id)
pipes = list(av_collector.OfCategory(BuiltInCategory.OST_PipeCurves).WhereElementIsNotElementType().ToElements())

# Get active view normal direction
view_dir = av.ViewDirection

# Filter the pipes that are facing the view
front_pipes = []
parallel_pipes = []
for pipe in pipes:
	direction = pipe.Location.Curve.Direction
	angle = direction.AngleTo(view_dir)
	if mcu.IsAlmostZero(angle) or mcu.IsAlmostEqual(angle, math.pi):
		front_pipes.append(pipe)
	else:
		parallel_pipes.append(pipe)

# Create plane at view location and get pipe lines
origin = av.Origin
normal = view_dir
plane = Plane.CreateByNormalAndOrigin(normal, origin)


# Get Family symbol
collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_DetailComponents).WhereElementIsElementType().ToElements()
symbol = next(x for x in collector if isinstance(x, FamilySymbol) and x.FamilyName == "a")

trans.Start("Place Detail")
for pipe in front_pipes:
	line = pipe.Location.Curve
	pipe_diameter = pipe.get_Parameter(BuiltInParameter.RBS_PIPE_OUTER_DIAMETER).AsDouble()
	intersection_point = get_plane_line_intersection(plane, line)
	detail_instance = doc.Create.NewFamilyInstance(intersection_point, symbol, av)
	detail_diameter_param = detail_instance.GetParameters("Diameter")[0].Set(pipe_diameter)
trans.Commit()
