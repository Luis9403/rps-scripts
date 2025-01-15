# Imports
from pprint import pprint
from Autodesk.Revit.DB import (ViewSchedule, 
							   BuiltInCategory, 
							   Category, 
							   Transaction, 
							   ScheduleFilter, 
							   ScheduleFilterType,
							   ScheduleSortGroupField,
							   ScheduleHorizontalAlignment,
							   ScheduleVerticalAlignment)

# Functions
def get_parameters(parameters):
	dis = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_DetailComponents)\
											 .WhereElementIsNotElementType()\
											 .ToElements()
	
	out_parameters = []
	for di in dis:
		for parameter in parameters:
			params = di.GetParameters(parameter)
			if not params:
				break
			else:
				out_parameters.append(params[0])
				
		else:
			break
			
	return out_parameters


def add_instance_fields(schedule_definition, parameters):
	for param in parameters:
		schedule_definition.AddField(ScheduleFieldType.Instance, param.Id)


def get_all_filtration_diagrams(document):
	dvs = FilteredElementCollector(document).OfClass(ViewDrafting).WhereElementIsNotElementType().ToElements()
	fds = [x for x in dvs if "FD" in x.Name]
	
	return fds

# Main
doc = __revit__.ActiveUIDocument.Document
trans = Transaction(doc)

param_names = [
	"BWR_DI_Equipment_Schedule_Index",
	"BWR_DI_Equipment_System ID",
	"BWR_DI_Equipment ID",
	"BWR_DI_Equipment Description",
	"BWR_DI_Equipment Load",
	"BWR_DI_Equipment Weight",
	"BWR_DI_Equipment Noise"
]

params = get_parameters(param_names)

dtc = Category.GetCategory(doc, BuiltInCategory.OST_DetailComponents).Id

vss = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Schedules).WhereElementIsNotElementType().ToElements()
vst = None
for vs in vss:
	if vs.IsTemplate and vs.Name == "BWR_Schedule_Filtration_Diagram":
		vst = vs
		break
	
print("Schedule Template: ", vst)
fds = sorted(get_all_filtration_diagrams(doc), key = lambda x: x.Name)

trans.Start("a")
for fd in fds:
	fd_name = fd.Name.split("_")
	sh_name = "BWR_FD_Equipment Schedule_{0}_{1}".format(fd_name[1], fd_name[2])
	schedule = ViewSchedule.CreateSchedule(doc, dtc)
	schedule.Name = sh_name
	
	print("View Schedule: ", schedule)
	
	schedule_definition = schedule.Definition
	add_instance_fields(schedule_definition, params)
	equipment_id = schedule_definition.GetField(2)
	system_id = schedule_definition.GetField(1)
	
	sf1 = ScheduleFilter(equipment_id.FieldId, ScheduleFilterType.HasParameter)
	sf2 = ScheduleFilter(system_id.FieldId, ScheduleFilterType.Equal, "{0}_{1}".format(fd_name[1], fd_name[2]))
	schedule_definition.AddFilter(sf1)
	schedule_definition.AddFilter(sf2)
	
	schedule_index = schedule_definition.GetField(0)
	
	sort1 = ScheduleSortGroupField(schedule_index.FieldId)
	sort2 = ScheduleSortGroupField(equipment_id.FieldId)
	
	schedule_definition.AddSortGroupField(sort1)
	schedule_definition.AddSortGroupField(sort2)
	
	schedule_definition.IsItemized = False
	schedule_definition.ShowTitle = False
	
	schedule_index.IsHidden = True
	system_id.IsHidden = True
	
	# Rename Columns
	id = schedule_definition.GetField(2)
	pi = schedule_definition.GetField(3)
	kw = schedule_definition.GetField(4)
	kg = schedule_definition.GetField(5)
	db = schedule_definition.GetField(6)
	
	
	id.ColumnHeading = "ID"
	pi.ColumnHeading = "PLANTROOM IDENTIFICATION"
	kw.ColumnHeading = "kW"
	kg.ColumnHeading = "WEIGHT(KG)"
	db.ColumnHeading = "dB(A)"
	
	id.HorizontalAlignment = ScheduleHorizontalAlignment.Center
	kw.HorizontalAlignment = ScheduleHorizontalAlignment.Center
	kg.HorizontalAlignment = ScheduleHorizontalAlignment.Center
	db.HorizontalAlignment = ScheduleHorizontalAlignment.Center
	
	id.VerticalAlignment = ScheduleVerticalAlignment.Middle
	kw.VerticalAlignment = ScheduleVerticalAlignment.Middle
	kg.VerticalAlignment = ScheduleVerticalAlignment.Middle
	db.VerticalAlignment = ScheduleVerticalAlignment.Middle
	
	schedule.ViewTemplateId = vst.Id
trans.Commit()
