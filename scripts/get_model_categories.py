# IMPORTS
from Autodesk.Revit.DB import CategoryType


doc = __revit__.ActiveUIDocument.Document

categories = doc.Settings.Categories
model_cat = []

for cat in categories:
	if (cat.CategoryType == CategoryType.Model and 
		cat.IsVisibleInUI):
		model_cat.append(cat)

sorted_cat = sorted(model_cat, key= lambda x: x.Name)

print(len(sorted_cat))
for i in sorted_cat:
	print(i.Name,"\t", i.BuiltInCategory)