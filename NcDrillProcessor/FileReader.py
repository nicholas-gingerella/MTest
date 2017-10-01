import re 
import csv

# Unit Mode Return Values
NC_UNIT_MODE_INCHES="INCHES"
NC_UNIT_MODE_MILLIMETERS="MILLIMETERS"

# Zero Format Return Values
ZERO_FORMAT_LEADING = "L"
ZERO_FORMAT_TRAILING = "T"

# Coordinate Mode Values
COORDINATE_MODE_ABSOLUTE = "A"
COORDINATE_MODE_INCREMENTAL = "I"

def get_file_coordinate_units(gerberFileName):
  headerStart = False
  headerEnd = False
  unit = None
  try:
    with open(gerberFileName, "r") as GbrFile:
      for line in GbrFile:
        # Does this file start with a proper header definition
        if headerStart is False:
          if "M48" not in line:
            return None # Header wasn't defined correctly
          else: # Start of the header was found
            headerStart = True

        # if this is a comment, skip the line
        match = re.search("^;",line)
        if match is not None:
          continue #skip this line
        
          
        match = re.search("^(M95|%)",line)
        if match is not None :
          headerEnd = True
          break
        
        match = re.search("^(INCH|METRIC),",line)
        if match is not None:
          if match.group(1) == "INCH":
            unit = NC_UNIT_MODE_INCHES
            break
          elif match.group(1) == "METRIC":
            unit = NC_UNIT_MODE_MILLIMETERS
            break
  except IOError:
    return -1

  return unit 


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




def main():
  mode = get_file_coordinate_units('../Files/NC/DrillSimple.nc')
  print(mode)




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
