import sys
import GerberProcessor.FileReader
import GerberProcessor.LineReader

GerberFileName = "./Files/test.pho"

GerberFormatInfo = {
"UnitMode"         : GerberProcessor.FileReader.get_file_coordinate_units(GerberFileName),
"CoordFormat"      : GerberProcessor.FileReader.get_file_coordinate_format(GerberFileName),
"ZeroFormat"       : GerberProcessor.FileReader.get_file_zero_format(GerberFileName)
}

# If we couldn't find the necessary format data from
# the file, close the program
for key,value in GerberFormatInfo.items(): 
  if value is None:
    print(key," not found")
    print("Failed to find all necessary format Information")
    print("Closing program")
    sys.exit()

if GerberFormatInfo["ZeroFormat"] is "T":
  ZeroFormatString = "Trailing 0 Format"
elif GerberFormatInfo["ZeroFormat"] is "L":
  ZeroFormatString = "Leading 0 Format"
else:
  ZeroFormatString = "No 0 Format Detected"
print("UNIT MODE:",GerberFormatInfo["UnitMode"])
print("COORDINATE FORMAT:",GerberFormatInfo["CoordFormat"])
print("TRAILING/LEADING 0 FORMAT:",ZeroFormatString)

# Look at point coordinates found in gerber file (D03 aperture flashes)
PointCoordinates = GerberProcessor.FileReader.get_file_point_coordinates(GerberFileName)
print("Total Points Identified:",len(PointCoordinates))
print("Raw Point -> Translated Point")

TranslatedCoordinates = []
for point in PointCoordinates:

  newCoord = GerberProcessor.LineReader.convert_raw_point_coordinate(
    point,
    GerberFormatInfo["CoordFormat"],
    GerberFormatInfo["UnitMode"],
    GerberFormatInfo["ZeroFormat"])
  
  TranslatedCoordinates.append(newCoord)

  print(point + " -> " + newCoord)