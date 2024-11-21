""" This script assign color to selected items"""

from Autodesk.Revit.DB import OverrideGraphicSettings, Color, FilteredElementCollector

colors = {"Yellow": Color(255,255,0), 
		  "Red": Color(255,0,0), 
		  "Blue": Color(0,0,255),
		  "Magenta": Color(255,0,255),
		  "Cyan": Color(0,255,255),
		  "Green": Color(0,255,0)}

COLOR = colors["Green"]

app = __revit__.Application
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
trans = Transaction(doc)

collector = FilteredElementCollector(doc)
fill_patterns = collector.OfClass(FillPatternElement).ToElements()
solid_fill = fill_patterns[0]

active_view = doc.ActiveView


ogs = OverrideGraphicSettings()

ogs.SetSurfaceForegroundPatternColor(COLOR)
ogs.SetSurfaceForegroundPatternId(solid_fill.Id)
ogs.SetSurfaceForegroundPatternVisible(True)


el_ids = uidoc.Selection.GetElementIds()

trans.Start("Coloring")
for el_id in el_ids:
	active_view.SetElementOverrides(el_id, ogs)
trans.Commit()



	



