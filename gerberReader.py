# ask to open a gerber file
import sys
import re
import csv

def GrbFile_GetUnitMode(gerberFileName):
	# Attempt to open the file
	unitMode = None
	try:
		with open(gerberFileName,"r") as GbrFile:
			for line in GbrFile:
				if "MOIN" in line:
					unitMode = "INCHES"
				elif "MOMM" in line:
					unitMode = "MILLIMETERS"
	except IOError:
		return -1
		
	return unitMode

def GrbFile_getZeroFormat(gerberFileName):
	try:
		with open(gerberFileName) as GrbFile:
			for line in GrbFile:
				if "FS" in line:
					if "L" in line:
						return "T" #leading 0 suppression (trailing 0 mode)
					elif "T" in line:
						return "L" #trailing 0 suppression (leading 0 mode)
	except IOError:
		return -1

	
def GrbFile_GetCoordFormat(gerberFileName):
	try:
		with open(gerberFileName) as GrbFile:
			for line in GrbFile:
				if "FS" in line:
					cmdTermPos=line.find('*')
					coordFormat="X##Y##"
					return line[cmdTermPos-len(coordFormat):cmdTermPos]
	except IOError:
		return -1

def GrbFile_GetD03Coords(gerberFileName):
	coord_list = []
	try:
		with open(gerberFileName) as GrbFile:
			for line in GrbFile:
				xCoord = ""
				yCoord = ""
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


def GrbLine_GetAperture(line):
	# Find Aperture settings that occur before 
	# D03 aperture flashes
	match = re.search('^G54(D[1-9]+)|(^D[1-9]+)',line)
	if match is not None:
		return match.group(1)
	else:
		return None


def	GrbLine_ConvertCoord(coord, c_format, units, z_format):
	x_unit = c_format[1:3]
	y_unit = c_format[4:6]
	x_coord = coord[coord.find("X")+1:coord.find("Y")]
	y_coord = coord[coord.find("Y")+1:]
	#print(coord, x_coord, y_coord)
	#print(c_format)
	#print(z_format)
	#print(x_unit)
	#print(y_unit)
	
	#full inches/mm before decimal point
	x_before_decimal = int(x_unit[0])
	#partial inches/mm after decimal point
	x_after_decimal = int(x_unit[1])
	x_total_digits = x_before_decimal + x_after_decimal
	
	y_before_decimal = int(y_unit[0])
	y_after_decimal = int(y_unit[1])
	y_total_digits = y_before_decimal + y_after_decimal
	
	if z_format is "T":
		new_x_coord = "0"*(x_total_digits - len(x_coord)) + x_coord
		new_y_coord = "0"*(y_total_digits - len(y_coord)) + y_coord
		
		#insert the decimal point
		converted_x = (new_x_coord[:x_before_decimal] + "." + new_x_coord[x_before_decimal:]).lstrip("0")
		converted_y = (new_y_coord[:y_before_decimal] + "." + new_y_coord[y_before_decimal:]).lstrip("0")
		return converted_x + "," + converted_y
		
	elif z_format is "L":
		print("format for Leading 0 mode")

		
def GrbFile_GetConvertedCoords(GbrFileName):
	unit_mode = GrbFile_GetUnitMode(GbrFileName)
	if unit_mode is -1:
		return -1
	coord_format = GrbFile_GetCoordFormat(GbrFileName)
	if coord_format is -1:
		return -1
	zero_format = GrbFile_getZeroFormat(GbrFileName)
	if zero_format is -1:
		return -1
	raw_coords = GrbFile_GetD03Coords(GbrFileName)
	if raw_coords is -1:
		return -1
	
	converted_coords = []
	for c in raw_coords:
		converted_coords.append(GrbLine_ConvertCoord(c, coord_format, unit_mode, zero_format))

	return converted_coords

	
# Prompt user for a file name
while True:
	GbrFileName = input("Enter Name of Gerber File: ")
	if GbrFileName is not "":
		break
		
# Get gerber file UNITS
print("Getting Unit Mode")
UNIT_MODE = GrbFile_GetUnitMode(GbrFileName)
ZERO_FORMAT = GrbFile_getZeroFormat(GbrFileName)
if UNIT_MODE is -1:
	print("Failed to Open File")
elif UNIT_MODE is "":
	print("No Unit mode found in File")
else:
	print("Successfully found unit mode:",UNIT_MODE)


# Get gerber file Coord Format
print("Getting Coordinate Format")
COORD_FORMAT = GrbFile_GetCoordFormat(GbrFileName)
if COORD_FORMAT is -1:
	print("Failed to Open File")
elif COORD_FORMAT is "":
	print("No Unit mode found in File")
else:
	print("Successfully found unit mode:",COORD_FORMAT)

gerber_coordinates = GrbFile_GetConvertedCoords(GbrFileName)

test_coords = []
with open("TestPoints.csv") as csvTestPoints:
	reader = csv.reader(csvTestPoints)
	for row in reader:
		test_coords.append(','.join(row))

test_coords.sort()

num_test_coords = len(test_coords)
found_count = 0
not_found_count = 0
for t in test_coords:
	if t not in gerber_coordinates:
		print(t + " -> " + "NOT FOUND")
	else:
		print(t + " -> " + "FOUND")
		found_count = found_count + 1

not_found_count = num_test_coords - found_count

print("Total Test Points:", num_test_coords)
print("Number of matching test coordinates:", found_count)
print("Number of missing test coordinates:", not_found_count)