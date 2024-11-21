uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

def GetAllMEPElements(elements):
	mep_elements = []
	for e in elements:
		if isinstance(e, FamilyInstance) and e.MEPModel != None or isinstance(e, MEPCurve):
			mep_elements.append(e)
			print(e)	
	return mep_elements
	
def GetAllGroups(elements):
	all_groups = []
	for e in elements:
		if isinstance(e, Group):
			all_groups.append(e)
	return all_groups

def GetAllAssemblies(elements):
	all_assemblies = []
	for e in elements:
		if isinstance(e, AssemblyInstance):
			all_assemblies.append(e)
	return all_assemblies
	
def SortLevelsByProjectEevation(levels):
	
	for i in range(len(levels)):
		sorted_levels = [x for x in levels]
		min_idx = i
		for j in range(i+1, len(sorted_levels)):
			if sorted_levels[min_idx].ProjectElevation > sorted_levels[j].ProjectElevation:
				min_idx = j
				
		sorted_levels[min_idx], sorted_levels[i] = sorted_levels[i], sorted_levels[min_idx]
		
	return sorted_levels
		
	
	
collector = FilteredElementCollector(doc)	

all_elements = collector.WhereElementIsNotElementType()
levels = collector.OfClass(Level).ToElements()

mep_elements = GetAllMEPElements(all_elements)
groups = GetAllGroups(all_elements)
assemblies = GetAllAssemblies(all_elements)

sorted_levels = SortLevelsByProjectEevation(levels)

for i in range(len(sorted_levels)):
	lower_level = sorted_levels[i]
	upper_level = sorted_levels[i + 1]
	
	for e in mep_elements:
		if isintance(e.Location, LocationPoint) and lower_level.ProjectElevation <= e.Location.Point.Z < upper_level.ProjectElevation:
			
			


for i in sorted_levels:
	print(i.ProjectElevation)



