import clr
from Autodesk.Revit.DB import (Transaction,
							   FamilyInstanceReferenceType,
							   ReferenceArray,
							   XYZ,
							   Line,
							   IntersectionResultArray,
							   ViewDetailLevel,
							   Solid,
							   Curve,
							   Point,
							   Reference)
from Autodesk.Revit.UI.Selection import ObjectType

def get_instance_ref(elem_ref):

	elem = doc.GetElement(elem_ref.ElementId)
	print(elem)
	
	geo_options = doc.Application.Create.NewGeometryOptions()
	geo_options.ComputeReferences = True
	geo_options.DetailLevel = ViewDetailLevel.Undefined
	geo_options.IncludeNonVisibleObjects = True
	
	geo_elem = elem.get_Geometry(geo_options)
	print(geo_elem, "\n")
	
	geo_inst = next(x for x in geo_elem if isinstance(x, GeometryInstance))
	print(geo_inst, "\n")
	
	geo_symbols = geo_inst.GetSymbolGeometry()
	stable_ref = 0
	
	for geo_obj in geo_symbols:
		if isinstance(geo_obj, Solid):
			print("Is solid")
			faces = geo_obj.Faces
			faces_enum = iter(faces)
			stable_ref = next(faces_enum).Reference.ConvertToStableRepresentation(doc)
			break
		
		elif isinstance(geo_obj, Curve):
			print("Is curve")
			stable_ref = geo_obj.Reference.ConvertToStableRepresentation(doc)
			break
			
		elif isinstance(geo_obj, Point):
			print("Is point")
			stable_ref = geo_obj.Reference.ConvertToStableRepresentation(doc)
			break
	
	print(stable_ref)
	
	ref_tokens = stable_ref.split(":")
	ref_tokens[-2] = "29"
	custom_stable_ref = ":".join(ref_tokens[0:-1]) + ":SURFACE"
	print(custom_stable_ref)
	
	index_ref = Reference.ParseFromStableRepresentation(doc, custom_stable_ref)
	print(index_ref)
	return index_ref

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
active_view = doc.ActiveView
trans = Transaction(doc)

grid_ref = uidoc.Selection.PickObject(ObjectType.Element, "Pick grid1")
elem_ref = uidoc.Selection.PickObject(ObjectType.Element, "Pick sl")

sl_ref = get_instance_ref(elem_ref)

refs = ReferenceArray()
refs.Append(grid_ref)
refs.Append(sl_ref)

point = grid_ref.GlobalPoint
direction  = XYZ(0,1,0)
line = Line.CreateUnbound(point, direction)

trans.Start("a")
doc.Create.NewDimension(active_view, line, refs)
trans.Commit()




			
	


