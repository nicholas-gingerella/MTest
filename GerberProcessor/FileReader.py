def get_file_coordinate_units(gerberFileName):
	try:
		with open(gerberFileName, "r") as GbrFile:
			for line in GbrFile:
				if "MOIN" in line:
					return "INCHES"
				elif "MOMM" in line:
					return "MILLIMETERS"
	except IOError:
		return -1
		
	# Failed to find a mode 
	return None 


def get_file_zero_format(gerberFileName):
	try:
		with open(gerberFileName) as GrbFile:
			for line in GrbFile:
				if "FS" in line:
					if "L" in line:
						return "T"  # leading 0 suppression (trailing 0 mode)
					elif "T" in line:
						return "L"  # trailing 0 suppression (leading 0 mode)
	except IOError:
		return -1
	
	# Failed to find a format
	return None


def get_file_coordinate_format(gerberFileName):
	try:
		with open(gerberFileName) as GrbFile:
			for line in GrbFile:
				if "FS" in line:
					cmdTermPos = line.find('*')
					coordFormat = "X##Y##"
					return line[cmdTermPos - len(coordFormat):cmdTermPos]
	except IOError:
		return -1
	
	# Failed to find format
	return None


def get_file_point_coordinates(gerberFileName):
	coord_list = []
	try:
		with open(gerberFileName) as GrbFile:
			for line in GrbFile:
				if line.endswith("D03*\n") is True:
					if "X" in line and "Y" in line:
						dCmdPos = line.find("D03*")
						coord = line[:dCmdPos]
						if coord.find("X") is not 0:
							coord = coord[coord.find("X"):]
						coord_list.append(coord)
	except IOError:
		return -1
	
	return coord_list


# def get_translated_point_coordinates(GbrFileName):
# 	unit_mode = get_file_coordinate_units(GbrFileName)
# 	if unit_mode is -1:
# 		return -1
# 	coord_format = get_file_coordinate_format(GbrFileName)
# 	if coord_format is -1:
# 		return -1
# 	zero_format = get_file_zero_format(GbrFileName)
# 	if zero_format is -1:
# 		return -1
# 	raw_coords = get_file_point_coordinates(GbrFileName)
# 	if raw_coords is -1:
# 		return -1
# 	
# 	converted_coords = []
# 	for c in raw_coords:
# 		converted_coords.append(convert_raw_point_coordinate(c, coord_format, unit_mode, zero_format))
# 
# 	return converted_coords
