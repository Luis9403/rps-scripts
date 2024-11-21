# IMPORTS
from Autodesk.Revit.DB import FilteredElementCollector, CategoryType
# MAIN

doc = __revit__.ActiveUIDocument.Document
av = doc.ActiveView
collector = FilteredElementCollector(doc)

cats = doc.Settings.Categories
i = 0
for cat in cats:
	if (cat.CategoryType == CategoryType.Model and
		cat.IsVisibleInUI and
		cat.CanAddSubcategory):
		i += 1
		print(cat.Name)
print(i)
me = collector.WhereElementIsNotElementType().ToElements()

for i in me:
	if (None != i.Category and
		i.Category.CategoryType == CategoryType.Model and
		i.Category.IsVisibleInUI and
		i.Category.CanAddSubcategory):
		
		print(i.Category.Name)
		

