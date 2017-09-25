import sys
import GerberProcessor.FileReader
import GerberProcessor.LineReader

GerberFileName = "./Files/art010.pho"
TestPointFileName = "./Files/art010-TestPoints.csv"

GerberFormatInfo = {
"UnitMode"         : GerberProcessor.FileReader.get_file_coordinate_units(GerberFileName),
"CoordinateMode"   : GerberProcessor.FileReader.get_file_coordinate_mode(GerberFileName),
"CoordFormat"      : GerberProcessor.FileReader.get_file_coordinate_format(GerberFileName),
"ZeroFormat"       : GerberProcessor.FileReader.get_file_zero_format(GerberFileName)
}

# If we couldn't find the necessary format data from
# the file, close the program
for key, value in GerberFormatInfo.items(): 
  if value is None:
    print(key, " not found")
    print("Failed to find all necessary format Information")
    print("Closing program")
    sys.exit()

if GerberFormatInfo["ZeroFormat"] is "T":
  ZeroFormatString = "Trailing 0 Format"
elif GerberFormatInfo["ZeroFormat"] is "L":
  ZeroFormatString = "Leading 0 Format"
else:
  ZeroFormatString = "No 0 Format Detected"
print("UNIT MODE:", GerberFormatInfo["UnitMode"])
print("COORDINATE_MODE:", GerberFormatInfo["CoordinateMode"])
print("COORDINATE FORMAT:", GerberFormatInfo["CoordFormat"])
print("TRAILING/LEADING 0 FORMAT:", ZeroFormatString)

# Look at point coordinates found in gerber file (D03 aperture flashes)
PointCoordinates = GerberProcessor.FileReader.get_file_point_coordinates(GerberFileName)
print("Total Points Identified:", len(PointCoordinates))
#print("Raw Point -> Translated Point")

TranslatedCoordinates = []
for point in PointCoordinates:
  newCoordX, newCoordY = GerberProcessor.LineReader.convert_raw_point_coordinate(
    point,
    GerberFormatInfo["CoordFormat"],
    GerberFormatInfo["UnitMode"],
    GerberFormatInfo["ZeroFormat"])
  print(point + " -> ",newCoordX,newCoordY)
  TranslatedCoordinates.append((newCoordX, newCoordY))

apertures = GerberProcessor.FileReader.get_file_aperture_definitions(GerberFileName)
print("Found Aperture Defs:",len(apertures))
for a in apertures:
  print(a)

# compare a csv of test points to a gerber file
# TODO: Create a get_file_test_points function that
#       returns a float coordinate tuple
test_coords = GerberProcessor.FileReader.get_file_test_points('Files/art010-TestPoints.csv')

num_test_coords = len(test_coords)
found_count = 0
not_found_count = 0
missing_coords = []
for t in test_coords:
  if t not in TranslatedCoordinates:
    missing_coords.append(t)
  else:
    found_count = found_count + 1

not_found_count = num_test_coords - found_count
print("Total Test Points:", num_test_coords)
print("Number of matching test coordinates:", found_count)
print("Number of missing test coordinates:", not_found_count)
print("Missing Coordinates")
for m in missing_coords:
  print(m)
  

# Look at point coordinates found in gerber file (D03 aperture flashes)
PointCoordinates = GerberProcessor.FileReader.get_file_point_coordinates("WTMLYR4.art")
print("Total Points Identified:", len(PointCoordinates))
#print("Raw Point -> Translated Point")

TranslatedCoordinates = []
for point in PointCoordinates:
  newCoordX, newCoordY = GerberProcessor.LineReader.convert_raw_point_coordinate(
    point,
    GerberFormatInfo["CoordFormat"],
    GerberFormatInfo["UnitMode"],
    GerberFormatInfo["ZeroFormat"])
  #print(point + " -> ",newCoordX,newCoordY)
  TranslatedCoordinates.append((newCoordX, newCoordY))
test_coord1 = GerberProcessor.FileReader.get_file_test_points("TestPointsFor1-11-17.csv", "MILS")
num_test_coords = len(test_coord1)
found_count = 0
not_found_count = 0
missing_coords = []
for t in test_coord1:
  if t not in TranslatedCoordinates:
    missing_coords.append(t)
  else:
    found_count = found_count + 1

not_found_count = num_test_coords - found_count
print("Total Test Points:", num_test_coords)
print("Number of matching test coordinates:", found_count)
print("Number of missing test coordinates:", not_found_count)
print("Missing Coordinates")
for m in missing_coords:
  print(m)