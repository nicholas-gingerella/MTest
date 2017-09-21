import re

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
