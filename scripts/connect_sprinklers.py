# Imports
from Autodesk.Revit.DB import Transaction, XYZ, Line
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.DB.Plumbing import Pipe, PlumbingUtils

# Functions
def set_pipe_diameter(pipe, diameter):
	diameter_param = pipe.get_Parameter(BuiltInParameter.RBS_PIPE_DIAMETER_PARAM)
	diameter_param.Set(diameter/12)
	
def set_system_type(pipe, system_type):
	system_type_param = pipe.get_Parameter(BuiltInParameter.RBS_PIPING_SYSTEM_TYPE_PARAM)
	system_type_param.Set(system_type)
	
def get_closest_connectors(connector_set1, connector_set2):
	min_distance = float("inf")
	connector1 = None
	connector2 = None
	
	for conn1 in connector_set1:
		conn1_origin = conn1.Origin
		for conn2 in connector_set2:
			conn2_origin = conn1.Origin
			distance = conn1_origin.DistanceTo(conn2_origin)
			if distance < min_distance:
				connector1 = conn1
				connector2 = conn2
				min_distance = distance
	
	return connector1, connector2
	

# Main
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
trans = Transaction(doc)

# Pick sprinkler and pipe
spk_ref = uidoc.Selection.PickObject(ObjectType.Element,"Pick Sprinkler")
sprinkler = doc.GetElement(spk_ref.ElementId)

pipe_ref = uidoc.Selection.PickObject(ObjectType.Element,"Pick Pipe")
pipe = doc.GetElement(pipe_ref.ElementId)

# Get sprinkler connector
spk_conns = sprinkler.MEPModel.ConnectorManager.Connectors
conn_iter = iter(spk_conns)
spk_conn = next(conn_iter)

# Get Connector location and direction
spk_conn_origin = spk_conn.Origin

spk_conn_direction = spk_conn.CoordinateSystem.BasisZ

# Get Pipe curve
pipe_line = pipe.Location.Curve

# Get closest point on pipe to sprinkler connector
point = pipe_line.Project(spk_conn_origin).XYZPoint

# Connection Route
point1 = spk_conn_origin
point2 = XYZ(spk_conn_origin.X, spk_conn_origin.Y, point.Z)
point3 = point

# Get Level Id, pipeTypeId and systemTypeId
level_id = pipe.LevelId
pipe_type_id = pipe.PipeType.Id
system_type_id = pipe.MEPSystem.GetTypeId()

# Create Pipes
trans.Start("Create Pipes")
pipe1 = Pipe.Create(doc, pipe_type_id, level_id, spk_conn, point2)
set_pipe_diameter(pipe1, 1)
set_system_type(pipe1, system_type_id)
pipe2 = Pipe.Create(doc, system_type_id, pipe_type_id, level_id, point2, point3)
set_pipe_diameter(pipe2, 1)

# split main pipe
new_pipe = PlumbingUtils.BreakCurve(doc, pipe_ref.ElementId, point)
trans.Commit()

trans.Start("Connect Pipes1")
pipe1_conns = pipe1.ConnectorManager.Connectors
pipe2_conns = pipe2.ConnectorManager.Connectors
closest_connectors1 = get_closest_connectors(pipe1_conns, pipe2_conns)
print(closest_connectors1)
new_elbow = doc.Create.NewElbowFitting(closest_connectors1[0], closest_connectors1[1])
trans.Commit()

trans.Start("Connect Pipes2")
new_pipe_conns = new_pipe.ConnectorManager.Connectors
pipe_conns = pipe.ConnectorManager.Connectors
closest_connectors2 = get_closest_connectors(new_pipe_conns, pipe_conns)
closest_connectors3 = get_closest_connectors(pipe2_conns, new_pipe_conns)
doc.Create.NewTeeFitting(closest_connectors2[1], closest_connectors2[0], closest_connectors3[0])
trans.Commit()
