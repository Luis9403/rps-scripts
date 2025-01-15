# Imports
from pprint import pprint
from collections import OrderedDict
from Autodesk.Revit.DB import ViewDrafting, Transaction, BuiltInCategory, Element

# Fucntions
# Get filtration diagrams detail views from the document
def get_fd_views(document):
	dvs = FilteredElementCollector(document).OfClass(ViewDrafting)\
										   .WhereElementIsNotElementType()\
										   .ToElements()
	
	fds = [x for x in dvs if isinstance(x, ViewDrafting) and "FD" in x.Name]
	return fds

# Renumber and adjust data for pumps
def renumber_pumps_in_view(document, view, st_index):
	
	groups = OrderedDict([
			("BWR_DI_Main Pump", []),
			("BWR_DI_Weir_Pump", []),
			("BWR_DI_Feature_Pump", []),
			("BWR_DI_Dosing Booster_Pump", []),
			("BWR_DI_Heat Exchanger_Pump", []),
			("BWR_DI_Heat Pump_Pump", [])
	])
	
	dis = FilteredElementCollector(document, view.Id).OfCategory(BuiltInCategory.OST_DetailComponents)\
												  .WhereElementIsNotElementType()\
												  .ToElements()
												  
	pumps = [x for x in dis if x.Symbol.FamilyName == "BWR_DI_MEP_Pump"]
	
	for pump in pumps:
		for key in groups.keys():
			param = pump.GetParameters(key)[0].AsInteger()
			if param == 1:
				groups[key].append(pump)
	
	groups["BWR_DI_Main Pump"] = sorted(groups["BWR_DI_Main Pump"], key = lambda x: x.Location.Point.Y)
	groups["BWR_DI_Weir_Pump"] = sorted(groups["BWR_DI_Weir_Pump"], key = lambda x: x.Location.Point.Y)
	groups["BWR_DI_Feature_Pump"] = sorted(groups["BWR_DI_Feature_Pump"], key = lambda x: x.Location.Point.Y)
	
	for key, value in groups.items():
		if value:
			start_l = "a"
			if len(value) > 1:
				for pump in value:
					param = pump.GetParameters("BWR_DI_Equipment ID")[0].Set("P" + str(st_index).zfill(2))
					param = pump.GetParameters("BWR_DI_Equipment Sub ID")[0].Set(start_l)
					start_l = chr(ord(start_l) + 1)
				st_index += 1
			else:
				for pump in value:
					param = pump.GetParameters("BWR_DI_Equipment ID")[0].Set("P" + str(st_index).zfill(2))
					param = pump.GetParameters("BWR_DI_Equipment Sub ID")[0].Set(" ")
				st_index += 1
	
	
	for key, value in groups.items():
		if value:
			load = value[0].Symbol.GetParameters("BWR_DI_Pump_Load")[0].AsString()
			weight = value[0].Symbol.GetParameters("BWR_DI_Pump_Weight")[0].AsString()
			
			if key == "BWR_DI_Main Pump":
				if len(value) > 2:
					for pump in value:
						pump.GetParameters("BWR_DI_Equipment Description")[0].Set("{0} x MAIN CIRCULATING PUMP ({1} DUTY + 1 STANDBY)".format(len(value), len(value) - 1))
						pump.GetParameters("BWR_DI_Equipment Weight")[0].Set("{0} x {1}".format(len(value), weight))
						pump.GetParameters("BWR_DI_Equipment Load")[0].Set("{0} x {1}".format(len(value) - 1, load))
				else:
					for pump in value:
						pump.GetParameters("BWR_DI_Equipment Description")[0].Set("MAIN CIRCULATING PUMP (1 DUTY + 1 STANDBY)")
						pump.GetParameters("BWR_DI_Equipment Weight")[0].Set("{0} x {1}".format(len(value), weight))
						pump.GetParameters("BWR_DI_Equipment Load")[0].Set(load)
			
			elif key == "BWR_DI_Weir_Pump":
				if len(value) > 1:
					for pump in value:
						pump.GetParameters("BWR_DI_Equipment Description")[0].Set("{0} x WEIR PUMP)".format(len(value)))
						pump.GetParameters("BWR_DI_Equipment Weight")[0].Set("{0} x {1}".format(len(value), weight))
						pump.GetParameters("BWR_DI_Equipment Load")[0].Set("{0} x {1}".format(len(value), load))
				else:
					for pump in value:
						pump.GetParameters("BWR_DI_Equipment Description")[0].Set("WEIR PUMP")
						pump.GetParameters("BWR_DI_Equipment Weight")[0].Set(weight)
						pump.GetParameters("BWR_DI_Equipment Load")[0].Set(load)
			
			elif key == "BWR_DI_Feature_Pump":
				if len(value) > 1:
					for pump in value:
						pump.GetParameters("BWR_DI_Equipment Description")[0].Set("{0} x FEATURE PUMP".format(len(value)))
						pump.GetParameters("BWR_DI_Equipment Weight")[0].Set("{0} x {1}".format(len(value), weight))
						pump.GetParameters("BWR_DI_Equipment Load")[0].Set("{0} x {1}".format(len(value), load))
				else:
					for pump in value:
						pump.GetParameters("BWR_DI_Equipment Description")[0].Set("FEATURE PUMP")
						pump.GetParameters("BWR_DI_Equipment Weight")[0].Set(weight)
						pump.GetParameters("BWR_DI_Equipment Load")[0].Set(load)
			
			elif key == "BWR_DI_Dosing Booster_Pump":
				if len(value) > 1:
					for pump in value:
						pump.GetParameters("BWR_DI_Equipment Description")[0].Set("{0} x BOOSTER PUMP FOR CHEMICAL DOSING)".format(len(value)))
						pump.GetParameters("BWR_DI_Equipment Weight")[0].Set("{0} x {1}".format(len(value), weight))
						pump.GetParameters("BWR_DI_Equipment Load")[0].Set("{0} x {1}".format(len(value), load))
				else:
					for pump in value:
						pump.GetParameters("BWR_DI_Equipment Description")[0].Set("BOOSTER PUMP FOR CHEMICAL DOSING")
						pump.GetParameters("BWR_DI_Equipment Weight")[0].Set(weight)
						pump.GetParameters("BWR_DI_Equipment Load")[0].Set(load)
			
			elif key == "BWR_DI_Heat Exchanger_Pump":
				if len(value) > 1:
					for pump in value:
						pump.GetParameters("BWR_DI_Equipment Description")[0].Set("{0} x BOOSTER PUMP FOR HEAT EXCHANGER)".format(len(value)))
						pump.GetParameters("BWR_DI_Equipment Weight")[0].Set("{0} x {1}".format(len(value), weight))
						pump.GetParameters("BWR_DI_Equipment Load")[0].Set("{0} x {1}".format(len(value), load))
				else:
					for pump in value:
						pump.GetParameters("BWR_DI_Equipment Description")[0].Set("BOOSTER PUMP FOR HEAT EXCHANGER")
						pump.GetParameters("BWR_DI_Equipment Weight")[0].Set(weight)
						pump.GetParameters("BWR_DI_Equipment Load")[0].Set(load)
			
			elif key == "BWR_DI_Heat Pump_Pump":
				if len(value) > 1:
					for pump in value:
						pump.GetParameters("BWR_DI_Equipment Description")[0].Set("{0} x BOOSTER PUMP FOR HEAT PUMP)".format(len(value)))
						pump.GetParameters("BWR_DI_Equipment Weight")[0].Set("{0} x {1}".format(len(value), weight))
						pump.GetParameters("BWR_DI_Equipment Load")[0].Set("{0} x {1}".format(len(value), load))
				else:
					for pump in value:
						pump.GetParameters("BWR_DI_Equipment Description")[0].Set("BOOSTER PUMP FOR HEAT PUMP")
						pump.GetParameters("BWR_DI_Equipment Weight")[0].Set(weight)
						pump.GetParameters("BWR_DI_Equipment Load")[0].Set(load)

	
	hypo_pump = next(x for x in dis if x.Symbol.Name == "Hypo_Dosing_Pump")
	hypo_pump.GetParameters("BWR_DI_Equipment ID")[0].Set("P" + str(st_index).zfill(2))
	st_index += 1
	
	acid_pump = next(x for x in dis if x.Symbol.Name == "Acid_Dosing_Pump")
	acid_pump.GetParameters("BWR_DI_Equipment ID")[0].Set("P" + str(st_index).zfill(2))
	st_index += 1
	
	return st_index


# Renumber Filters and adjust data
def renumber_filters(document, view, st_index):
	dis = FilteredElementCollector(document, view.Id).OfCategory(BuiltInCategory.OST_DetailComponents)\
												  .WhereElementIsNotElementType()\
												  .ToElements()
												  
	filters = [x for x in dis if x.Symbol.FamilyName == "BWR_DI_MEP_Sand Filter"]
	sorted_filters = sorted(filters, key = lambda x: x.Location.Point.X)
	
	filter_no = len(sorted_filters)
	size = filters[0].Name.split("-")[-1]
	description = str(filter_no) + " x" + size + " SAND FILTER"
	weight = filters[0].Symbol.GetParameters("BWR_DI_Sand Filter_Weight")[0].AsString()
	start_l = "a"
	for filter in sorted_filters:
		filter.GetParameters("BWR_DI_Equipment ID")[0].Set("PV" + str(st_index).zfill(2))
		filter.GetParameters("BWR_DI_Equipment Sub ID")[0].Set(start_l)
		filter.GetParameters("BWR_DI_Equipment Description")[0].Set(description)
		filter.GetParameters("BWR_DI_Equipment Weight")[0].Set("{0} x {1}".format(len(filters), weight))
		start_l = chr(ord(start_l) + 1)


# Renumber UV units
def renumber_UV(document, view, st_index):
	dis = FilteredElementCollector(document, view.Id).OfCategory(BuiltInCategory.OST_DetailComponents)\
												  .WhereElementIsNotElementType()\
												  .ToElements()
												  
	uvs = [x for x in dis if x.Symbol.FamilyName == "BWR_DI_MEP_UV Unit"]
	
	for uv in uvs:
		uv.GetParameters("BWR_DI_Equipment ID")[0].Set("UV" + str(st_index).zfill(2))


# Renumber sample boards
def renumber_sample_board(document, view, st_index):
	dis = FilteredElementCollector(document, view.Id).OfCategory(BuiltInCategory.OST_DetailComponents)\
												  .WhereElementIsNotElementType()\
												  .ToElements()
												  
	sbs = [x for x in dis if x.Symbol.FamilyName == "BWR_DI_MEP_Sample Board"]
	
	for sb in sbs:
		sb.GetParameters("BWR_DI_Equipment ID")[0].Set("SB" + str(st_index).zfill(2))


# Get name for general data tag
def name_general_data(document, view):
	dis = FilteredElementCollector(document, view.Id).OfCategory(BuiltInCategory.OST_GenericAnnotation)\
												  .WhereElementIsNotElementType()\
												  .ToElements()
												  
	gdb = next(x for x in dis if x.Symbol.FamilyName == "BWR_DI_FD_General Data")
	name = gdb.GetParameters("BWR_DI_FD_Name")[0]
	
	view_name = view.Name.split("_")[-1]
	name.Set(view_name)


# Adjust backwash diameter and flow
def adjust_backwash_data(document, view):
	dis = FilteredElementCollector(document, view.Id).OfCategory(BuiltInCategory.OST_DetailComponents)\
												  .WhereElementIsNotElementType()\
												  .ToElements()
												  
	filter = next(x for x in dis if x.Symbol.FamilyName == "BWR_DI_MEP_Sand Filter")
	symbol = filter.Symbol
	bw_diameter = symbol.GetParameters("BWR_DI_Filter Connection Diameter")[0]
	bw_flow = symbol.GetParameters("BWR_DI_Backwash Flow")[0].AsDouble()

	gas = FilteredElementCollector(document, view.Id).OfCategory(BuiltInCategory.OST_GenericAnnotation)\
												  .WhereElementIsNotElementType()\
												  .ToElements()
	bw_tags = [x for x in gas if x.Symbol.FamilyName == "BWR_DI_Tag_Line Diameter" and Element.Name.__get__(x) == "Backwash_Water"]
	for tag in bw_tags:
		tag.GetParameters("BWR_Line_Diameter")[0].Set(float(bw_diameter.AsValueString()))
	
	
	bw = next(x for x in dis if x.Symbol.FamilyName == "BWR_DI_MEP_Backwash Drain")
	bw.GetParameters("BWR_DI_Backwash Drain_Diameter")[0].Set(bw_diameter.AsDouble())
	bw.GetParameters("BWR_DI_Backwash Drain_Flow")[0].Set(float(bw_flow))
	
	ft_tags = [x for x in gas if x.Symbol.FamilyName == "BWR_DI_Tag_Sand Filter_Line Diameter"]
	for tag in ft_tags:
		tag.GetParameters("BWR_Line_Diameter")[0].Set(float(bw_diameter.AsValueString()))


# Renumber Strainers
def renumber_strainers(document, view, st_index):
	strainer_groups = OrderedDict([
					("Main Pump_Strainer", []),
					("Weir Pump_Strainer", []),
					("Feature Pump_Strainer", [])
	])
	
	dis = FilteredElementCollector(document, view.Id).OfCategory(BuiltInCategory.OST_DetailComponents)\
													 .WhereElementIsNotElementType()\
													 .ToElements()
														   
	strainers = [x for x in dis if x.Symbol.FamilyName == "BWR_DI_MEP_Strainer"]
	
	for strainer in strainers:
		for key in strainer_groups.keys():
			if strainer.Name == key:
				strainer_groups[key].append(strainer)
				break
	
	
	strainer_groups["Main Pump_Strainer"] = sorted(strainer_groups["Main Pump_Strainer"], key = lambda x: x.Location.Point.Y)
	strainer_groups["Weir Pump_Strainer"] = sorted(strainer_groups["Weir Pump_Strainer"], key = lambda x: x.Location.Point.Y)
	strainer_groups["Feature Pump_Strainer"] = sorted(strainer_groups["Feature Pump_Strainer"], key = lambda x: x.Location.Point.Y)
	
	for key, value in strainer_groups.items():
		if value:
			start_l = "a"
			if len(value) > 1:
				for strainer in value:
					strainer.GetParameters("BWR_DI_Equipment ID")[0].Set("ST" + str(st_index).zfill(2))
					strainer.GetParameters("BWR_DI_Equipment Sub ID")[0].Set(start_l)
					start_l = chr(ord(start_l) + 1)
				st_index += 1
			else:
				for strainer in value:
					strainer.GetParameters("BWR_DI_Equipment ID")[0].Set("ST" + str(st_index).zfill(2))
					strainer.GetParameters("BWR_DI_Equipment Sub ID")[0].Set(" ")
				st_index += 1
	
	
	for key, value in strainer_groups.items():
		if value:
			if key == "Main Pump_Strainer":
				if len(value) > 1:
					for strainer in value:
						strainer.GetParameters("BWR_DI_Equipment Description")[0].Set("{0} x STRAINER FOR CIRCULATION PUMPS".format(len(value)))
						strainer.GetParameters("BWR_DI_Equipment Weight")[0].Set("{0} x 10".format(len(value)))
				else:
					value[0].GetParameters("BWR_DI_Equipment Description")[0].Set("STRAINER FOR CIRCULATION PUMPS")
					value[0].GetParameters("BWR_DI_Equipment Weight")[0].Set("10")
						
			elif key == "Weir Pump_Strainer":
				if len(value) > 1:
					for strainer in value:
						strainer.GetParameters("BWR_DI_Equipment Description")[0].Set("{0} x STRAINER FOR WEIR PUMPS".format(len(value)))
						strainer.GetParameters("BWR_DI_Equipment Weight")[0].Set("{0} x 10".format(len(value)))
				else:
					value[0].GetParameters("BWR_DI_Equipment Description")[0].Set("STRAINER FOR WEIR PUMPS")
					value[0].GetParameters("BWR_DI_Equipment Weight")[0].Set("10")
			
			elif key == "Feature Pump_Strainer":
				if len(value) > 1:
					for strainer in value:
						strainer.GetParameters("BWR_DI_Equipment Description")[0].Set("{0} x STRAINER FOR FEATURE PUMPS".format(len(value)))
						strainer.GetParameters("BWR_DI_Equipment Weight")[0].Set("{0} x 10".format(len(value)))
				else:
					value[0].GetParameters("BWR_DI_Equipment Description")[0].Set("STRAINER FOR FEATURE PUMPS")
					value[0].GetParameters("BWR_DI_Equipment Weight")[0].Set("10")
	
	
	return st_index


# Adjust data for variable speed drives
def vsd_adjust_weight(document, view):
	dis = FilteredElementCollector(document, view.Id).OfCategory(BuiltInCategory.OST_DetailComponents)\
												  .WhereElementIsNotElementType()\
												  .ToElements()
												  
	vsds = [x for x in dis if x.Symbol.FamilyName == "BWR_DI_MEP_Variable Speed Drive"]
	
	for vsd in vsds:
		vsd.GetParameters("BWR_DI_Equipment Description")[0].Set("{0} x VARIABLE SPEED DRIVE".format(len(vsds)))
		vsd.GetParameters("BWR_DI_Equipment Weight")[0].Set("{0} x 0.5".format(len(vsds)))


# Renumber heat pump
def renumber_heat_pumps(document, view, st_index):
	dis = FilteredElementCollector(document, view.Id).OfCategory(BuiltInCategory.OST_DetailComponents)\
												  .WhereElementIsNotElementType()\
												  .ToElements()
												  
	hps = [x for x in dis if x.Symbol.FamilyName == "BWR_DI_MEP_Heat Pump"]
	if hps:
		sorted_hps = sorted(hps, key = lambda x: x.Location.Point.X)
		
		description = "HEAT/COOL PUMP ({0})".format(hps[0].Name)
		weight = str(hps[0].Symbol.GetParameters("BWR_DI_Heat Pump_Weight")[0].AsDouble())
		load = str(hps[0].Symbol.GetParameters("BWR_DI_Heat Pump_Heating Power Input")[0].AsValueString().split()[0])
		
		if len(hps) > 1:
			description = "{0} x HEAT/COOL PUMP ({1})".format(len(hps), hps[0].Name)
			weight = "{0} x {1}".format(len(hps), weight)
			load = "{0} x {1}".format(len(hps), weight)
			
		
		start_l = "a"
		for hp in sorted_hps:
			hp.GetParameters("BWR_DI_Equipment ID")[0].Set("HP" + str(st_index).zfill(2))
			hp.GetParameters("BWR_DI_Equipment Sub ID")[0].Set(start_l)
			hp.GetParameters("BWR_DI_Equipment Description")[0].Set(description)
			hp.GetParameters("BWR_DI_Equipment Weight")[0].Set(weight)
			hp.GetParameters("BWR_DI_Equipment Load")[0].Set(load)
		return True
	else:
		return False
		
		
# Renumber chiller pump
def renumber_chiller_units(document, view, st_index):
	dis = FilteredElementCollector(document, view.Id).OfCategory(BuiltInCategory.OST_DetailComponents)\
												  .WhereElementIsNotElementType()\
												  .ToElements()
												  
	cus = [x for x in dis if x.Symbol.FamilyName == "BWR_DI_MEP_Chiller Unit"]
	if cus:
		sorted_cus = sorted(cus, key = lambda x: x.Location.Point.X)
		
		description = "CHILLER UNIT ({0})".format(cus[0].Name)
		weight = str(cus[0].Symbol.GetParameters("BWR_DI_Chiller Unit_Weight")[0].AsDouble())
		load = str(cus[0].Symbol.GetParameters("BWR_DI_Chiller Unit_Cooling Power Input")[0].AsValueString().split()[0])
		
		if len(cus) > 1:
			description = "{0} x CHILLER UNIT ({1})".format(len(cus), cus[0].Name)
			weight = "{0} x {1}".format(len(cus), weight)
			load = "{0} x {1}".format(len(cus), load)
			
		
		start_l = "a"
		for cu in sorted_cus:
			cu.GetParameters("BWR_DI_Equipment ID")[0].Set("CH" + str(st_index).zfill(2))
			cu.GetParameters("BWR_DI_Equipment Sub ID")[0].Set(start_l)
			cu.GetParameters("BWR_DI_Equipment Description")[0].Set(description)
			cu.GetParameters("BWR_DI_Equipment Weight")[0].Set(weight)
			cu.GetParameters("BWR_DI_Equipment Load")[0].Set(load)
		return True
	else:
		return False

# Renumber heat exchangers
def renumber_heat_exchangers(document, view, st_index):
	dis = FilteredElementCollector(document, view.Id).OfCategory(BuiltInCategory.OST_DetailComponents)\
												  .WhereElementIsNotElementType()\
												  .ToElements()
												  
	cus = [x for x in dis if x.Symbol.FamilyName == "BWR_DI_MEP_Heat Exchanger"]
	if cus:
		sorted_cus = sorted(cus, key = lambda x: x.Location.Point.X)
		
		description = "HEAT/COOL HEAT EXCHANGER ({0})".format(cus[0].Name)
		weight = str(cus[0].Symbol.GetParameters("BWR_DI_Heat Exchanger_Weight")[0].AsDouble())
		
		if len(cus) > 1:
			description = "{0} x HEAT/COOL HEAT EXCHANGER ({1})".format(len(cus), cus[0].Name)
			weight = "{0} x {1}".format(len(cus), weight)
			
		
		start_l = "a"
		for cu in sorted_cus:
			cu.GetParameters("BWR_DI_Equipment ID")[0].Set("HX" + str(st_index).zfill(2))
			cu.GetParameters("BWR_DI_Equipment Sub ID")[0].Set(start_l)
			cu.GetParameters("BWR_DI_Equipment Description")[0].Set(description)
			cu.GetParameters("BWR_DI_Equipment Weight")[0].Set(weight)
		return True
	else:
		return False


# Main
doc = __revit__.ActiveUIDocument.Document
trans = Transaction(doc)
av = doc.ActiveView

fds = sorted(get_fd_views(doc), key = lambda x: x.Name)

trans.Start("ad")
pump_index = 1
filter_index = 1
UV_index = 1
sb_index = 1
st_index = 1
hp_index = 1
cu_index = 1
hx_index = 1

for fd in fds:
	t = renumber_pumps_in_view(doc, fd, pump_index)
	pump_index = t
	
	renumber_filters(doc, fd, filter_index)
	filter_index += 1
	
	renumber_UV(doc, fd, UV_index)
	UV_index += 1
	
	renumber_sample_board(doc, fd, sb_index)
	sb_index += 1
	
	name_general_data(doc, fd)
	
	adjust_backwash_data(doc, fd)
	
	st = renumber_strainers(doc, fd, st_index)
	st_index = st
	
	vsd_adjust_weight(doc, fd)
	
	if renumber_heat_pumps(doc, fd, hp_index):
		hp_index += 1
	
	if renumber_chiller_units(doc, fd, cu_index):
		cu_index += 1
		
	if renumber_heat_exchangers(doc, fd, hx_index):
		hx_index += 1
	
trans.Commit()




