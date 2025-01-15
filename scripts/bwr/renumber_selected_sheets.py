from Autodesk.Revit.DB import ViewSheet, BuiltInCategory, Transaction, Viewport

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
trans = Transaction(doc)

number = 100000

sheet_ids = uidoc.Selection.GetElementIds()
sheets = sorted([doc.GetElement(x) for x in sheet_ids],key = lambda x: x.SheetNumber)

trans.Start("Create sheet")
for sheet in sheets:
	sheet.SheetNumber = str(number)
	number += 1
trans.Commit()

