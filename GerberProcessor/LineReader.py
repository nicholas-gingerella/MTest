# ask to open a gerber file
import re

def get_aperture_code(line):
  # Find Aperture settings that occur before 
  # D03 aperture flashes
  match = re.search('^G54(D[1-9]+)|(^D[1-9]+)', line)
  if match is not None:
    return match.group(1)
  else:
    return None


# A raw coordinate point is the point as it appears in the Gerber file
# X####Y####D03*, this returns a converted point in decimal format
def convert_raw_point_coordinate(coord, c_format, units, z_format):
  x_unit = c_format[1:3]
  y_unit = c_format[4:6]
  x_coord = coord[coord.find("X") + 1:coord.find("Y")]
  y_coord = coord[coord.find("Y") + 1:]
  # full inches/mm before decimal point
  x_before_decimal = int(x_unit[0])
  # partial inches/mm after decimal point
  x_after_decimal = int(x_unit[1])
  x_total_digits = x_before_decimal + x_after_decimal
  
  y_before_decimal = int(y_unit[0])
  y_after_decimal = int(y_unit[1])
  y_total_digits = y_before_decimal + y_after_decimal
  
  if z_format is "T":
    new_x_coord = "0"*(x_total_digits - len(x_coord)) + x_coord
    new_y_coord = "0"*(y_total_digits - len(y_coord)) + y_coord
    
    # insert the decimal point
    converted_x = (new_x_coord[:x_before_decimal] + "." + new_x_coord[x_before_decimal:]).lstrip("0")
    converted_y = (new_y_coord[:y_before_decimal] + "." + new_y_coord[y_before_decimal:]).lstrip("0")

    if "-" in converted_x:
      converted_x = converted_x.replace("-","")
      converted_x = "-"+converted_x
      
    if "-" in converted_y:
      converted_y = converted_y.replace("-","")
      converted_y = "-"+converted_y

    return float(converted_x), float(converted_y)
    
  elif z_format is "L":
    new_x_coord = x_coord + "0"*(x_total_digits - len(x_coord))
    new_y_coord = y_coord + "0"*(y_total_digits - len(y_coord))
    
    # insert the decimal point
    converted_x = (new_x_coord[:x_before_decimal] + "." + new_x_coord[x_before_decimal:]).lstrip("0")
    converted_y = (new_y_coord[:y_before_decimal] + "." + new_y_coord[y_before_decimal:]).lstrip("0")

    if "-" in converted_x:
      converted_x = converted_x.replace("-","")
      converted_x = "-"+converted_x
      
    if "-" in converted_y:
      converted_y = converted_y.replace("-","")
      converted_y = "-"+converted_y

    return float(converted_x), float(converted_y)
