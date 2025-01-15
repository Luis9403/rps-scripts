from pprint import pprint
from Autodesk.Revit.DB import Transaction, FilteredElementCollector, ViewSheet

doc = __revit__.ActiveUIDocument.Document
trans = Transaction(doc)

new_no = 120011
sheets = FilteredElementCollector(doc).OfClass(ViewSheet).WhereElementIsNotElementType().ToElements()

sort_sheets = sorted(sheets, key = lambda x: x.SheetNumber)

end_no = new_no
sheets_change = []
for sheet in sort_sheets:
	try:
		number = int(sheet.SheetNumber)
		if number == int(end_no):
			sheets_change.append(sheet)
			end_no += 1
	except:
		pass
		
sheets_change = sheets_change[::-1]

trans.Start("a")
for sheet in sheets_change:
	sheet.SheetNumber = str(end_no)
	end_no -= 1
	
trans.Commit()
	
		
		

