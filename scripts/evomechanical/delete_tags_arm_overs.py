"""Remove tags from armover pipes """
from Autodesk.Revit.DB.Plumbing import Pipe

doc = __revit__.ActiveUIDocument.Document
active_view = doc.ActiveView

trans = Transaction(doc)

collector = FilteredElementCollector(doc, active_view.Id)

tags = collector.OfClass(IndependentTag).WhereElementIsNotElementType().ToElements()

trans.Start("Delete tags")
for a in tags:
	e = a.GetTaggedLocalElements()
	if isinstance(e[0], Pipe):
		pipes_type= e[0].PipeType
		if pipes_type.Name == "Hcad1 FP Arms to Thrd Lines":
			doc.Delete(a.Id)
		
trans.Commit()