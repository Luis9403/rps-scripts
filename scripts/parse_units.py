from Autodesk.Revit.DB import SpecTypeId, UnitFormatUtils

doc = __revit__.ActiveUIDocument.Document

units = doc.GetUnits()
text = "0 6"

a, b = UnitFormatUtils.TryParse(units, SpecTypeId.Length, text,)
print(a)
print(b)

