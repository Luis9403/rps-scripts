from Autodesk.Revit.UI.Selection import ObjectType

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

ref1 = uidoc.Selection.PickObject(ObjectType.Face, "a")
print(ref1,)

elid = ref1.ElementId
print(elid)
el = doc.GetElement(elid)
print(el,)

face = el.GetGeometryObjectFromReference(ref1)
print(face)

picked_point = ref1.UVPoint
print(picked_point)
print(face.XVector)
print(face.YVector)
