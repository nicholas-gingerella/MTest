import re 
import csv
import Utilities.UnitConversion

# Unit Mode Return Values
GERBER_UNIT_MODE_INCHES="INCHES"
GERBER_UNIT_MODE_MILLIMETERS="MILLIMETERS"

# Zero Format Return Values
ZERO_FORMAT_LEADING = "L"
ZERO_FORMAT_TRAILING = "T"

# Coordinate Mode Values
COORDINATE_MODE_ABSOLUTE = "A"
COORDINATE_MODE_INCREMENTAL = "I"

def get_file_coordinate_units(gerberFileName):
  try:
    with open(gerberFileName, "r") as GbrFile:
      for line in GbrFile:
        if "MOIN" in line:
          return GERBER_UNIT_MODE_INCHES
        elif "MOMM" in line:
          return GERBER_UNIT_MODE_MILLIMETERS
  except IOError:
    return -1
    
  # Failed to find a mode 
  return None 


def get_file_coordinate_mode(gerberFileName):
  try:
    with open(gerberFileName, "r") as GrbFile:
      for line in GrbFile:
        if "FS" in line:
          if "A" in line:
            return COORDINATE_MODE_ABSOLUTE
          elif "I" in line:
            return COORDINATE_MODE_INCREMENTAL
  except IOError:
    return -1
  
  # Failed to find mode
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

#TODO: Implement coordinate parsing for incremental mode
#      Currently assumes absolute mode for coordinates
def get_file_point_coordinates(gerberFileName):
  coord_list = []
  latestXYCoord = 0

  try:
    with open(gerberFileName) as GrbFile:
      for line in GrbFile:
        # clean off any whitespace or newline chars
        coordLine = line.strip()

        # is this an aperture flash? if so, it should
        # end with flash code D03
        if coordLine.endswith("D03*"):
          # flash identified, now start cleaning
          # up the line so only the XY coordinate
          # is left
          coordLine = coordLine.replace("D03*","")
          if "G01" in coordLine:
            coordLine = coordLine.replace("G01","")
          #should have a clean coordinate line at this point
          if "X" in coordLine and "Y" in coordLine:
            latestXYCoord = coordLine
          elif "X" in coordLine and "Y" not in coordLine:
            #use last Y coord with this X coord
            match = re.search("(Y[0-9]+)",latestXYCoord)
            if match is not None:
              coordLine = coordLine + match.group(1)
          elif "X" not in coordLine and "Y" in coordLine:
            #use last X coord with this Y coord
            match = re.search("(X[0-9]+)",latestXYCoord)
            if match is not None:
              coordLine = match.group(1) + coordLine

          coord_list.append(coordLine)
  except IOError:
    return -1
  
  return coord_list

def get_file_aperture_definitions(gerberFileName):
  apertures = []
  with open(gerberFileName) as GrbFile:
    for line in GrbFile:
      match = re.search('AD(D[0-9]+)(C),(.*)\*', line)
      if match is not None:
        aperInfo = (match.group(0), match.group(1), match.group(2), match.group(3))
        apertures.append(aperInfo)
  
  if len(apertures) > 0:
    return apertures
  else:
    return None


def get_file_test_points(csvTestFile, units="INCHES"):
  coord_list = []
  with open(csvTestFile) as TestPoints:
    reader = csv.reader(TestPoints)
    for row in reader:
      x_coord = float(row[0])
      y_coord = float(row[1])
      
      if units is "MILS":
        x_coord = Utilities.UnitConversion.mils_to_inches(x_coord)
        y_coord = Utilities.UnitConversion.mils_to_inches(y_coord)

      coord_list.append((x_coord, y_coord))
  return coord_list 



def main():
  test_points = get_file_test_points('../Files/art010-TestPoints.csv')
  print(test_points)
  test_points = get_file_test_points('../TestPointsFor1-11-17.csv', "MILS")
  print(test_points)




if __name__ == "__main__":
  # stuff only to run when not called via 'import' here
  main()
# def get_translated_point_coordinates(GbrFileName):
#   unit_mode = get_file_coordinate_units(GbrFileName)
#   if unit_mode is -1:
#     return -1
#   coord_format = get_file_coordinate_format(GbrFileName)
#   if coord_format is -1:
#     return -1
#   zero_format = get_file_zero_format(GbrFileName)
#   if zero_format is -1:
#     return -1
#   raw_coords = get_file_point_coordinates(GbrFileName)
#   if raw_coords is -1:
#     return -1
#   
#   converted_coords = []
#   for c in raw_coords:
#     converted_coords.append(convert_raw_point_coordinate(c, coord_format, unit_mode, zero_format))
# 
#   return converted_coords
