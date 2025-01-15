from Autodesk.Revit.DB import ViewSheet, BuiltInCategory, Transaction, Viewport

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
trans = Transaction(doc)

title_block = "M1-WTA-XX-BIM-XXX-XXX-XX-TEM-900047-R5_DESIGN REVIT TITLEBLOCK FAMILY TEMPLATE (1)"
number = 120039

tbs = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_TitleBlocks).WhereElementIsElementType().ToElements()
tb = next(x for x in tbs if x.Name == title_block)

view_ids = uidoc.Selection.GetElementIds()
views = sorted([doc.GetElement(x) for x in view_ids],key = lambda x: x.Name)

trans.Start("Create sheet")
for view in views:
	sheet = ViewSheet.Create(doc, tb.Id)
	sheet.Name = view.Name
	sheet.SheetNumber = str(number)
	Viewport.Create(doc, sheet.Id, view.Id, XYZ(0,0,0))
	number += 1
trans.Commit()

