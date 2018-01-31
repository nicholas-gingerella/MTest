import sys
import GerberProcessor.FileReader
import GerberProcessor.LineReader


def filter_tool_list( aprtrList, toolList ):
    # use a dictionary to find whether the tool dcodes
    # exist within the defined circle aperture Table
    toolDict = {}
    for a in toolList:
        toolDict[a[1]] = 0
    
    # we now have a dict of circle apertures,
    # lets see if the items in the tool list
    # are found among the circle defs
    for a in aprtrList:
        if a[1] in toolDict:
            toolDict[a[1]] = 1
    
    circleToolSelectList = []
    for key, value in toolDict.items():
        # print(key, value)
    
        if value is 1:
            circleToolSelectList.append( key )
    
    return circleToolSelectList


GerberFileName = "./Files/Gerber/art010.pho"
TestPointFileName = "./Files/CSV/art010-TestPoints.csv"

GerberFormatInfo = {
    "UnitMode": GerberProcessor.FileReader.get_file_coordinate_units( GerberFileName ),
    "CoordinateMode": GerberProcessor.FileReader.get_file_coordinate_mode( GerberFileName ),
    "CoordFormat": GerberProcessor.FileReader.get_file_coordinate_format( GerberFileName ),
    "ZeroFormat": GerberProcessor.FileReader.get_file_zero_format( GerberFileName )
}

# If we couldn't find the necessary format data from
# the file, close the program
for key, value in GerberFormatInfo.items():
    if value is None:
        print( key, " not found" )
        print( "Failed to find all necessary format Information" )
        print( "Closing program" )
        sys.exit()

# Generate a human readable string describing the detected
# Zero Format of the gerber file
if GerberFormatInfo["ZeroFormat"] is "T":
    ZeroFormatString = "Trailing 0 Format"
elif GerberFormatInfo["ZeroFormat"] is "L":
    ZeroFormatString = "Leading 0 Format"
else:
    ZeroFormatString = "No 0 Format Detected"

# Output basic formatting information
print( "UNIT MODE:", GerberFormatInfo["UnitMode"] )
print( "COORDINATE_MODE:", GerberFormatInfo["CoordinateMode"] )
print( "COORDINATE FORMAT:", GerberFormatInfo["CoordFormat"] )
print( "TRAILING/LEADING 0 FORMAT:", ZeroFormatString )

# Now determine what order to gather information
# 1. Get aperture definitions: These definitions define G54 tool selects
#    that we use to group aperture flashes with a certain aperture size
# 2. Get the tool selects (G54) that correspond to circle apertures. That is,
#    get all the tool selects, and then cross reference the DCode with the
#    aperture table

# 1. Get apertures
# aperture definitions are found near the beginning of the file, these definitions
# define the DCodes used in G54 tool selects later on in the file
# NOTE: apertures is a tuple, 0 being he original strings, and 1 beng the Dcode
apertures = GerberProcessor.FileReader.get_file_aperture_definitions( 
    GerberFileName )
print( "Found Aperture Defs:", len( apertures ) )
# for a in apertures:
#  print(a)

# 2. Get tool selects
# tool select brings up more than the number of apertures, but this is fine, since
# the tool select is also picking up rectangle flashes, but we only care about
# circular flashes (for drill holes)
# NOTE: tool_selects is a tuple, with 0 being the original string, and 1 bing the
#       Dcode
tool_selects = GerberProcessor.FileReader.get_file_tool_selects( GerberFileName )
print( "tool selects:", len( tool_selects ) )
# for t in tool_selects:
#  print(t)

drill_tools = filter_tool_list( apertures, tool_selects )
print( len( drill_tools ), "are drill tools" )

# Look at point coordinates found in gerber file (D03 aperture flashes)
rawApertureFlashCoordinates = GerberProcessor.FileReader.get_file_point_coordinates( 
    GerberFileName )
print( "Total Points Identified:", len( rawApertureFlashCoordinates ) )

# Convert the raw coordinate format found in the gerber file to a human
# readable format
translatedApertureFlashCoordinates = []
for point in rawApertureFlashCoordinates:
    newCoordX, newCoordY = GerberProcessor.LineReader.convert_raw_point_coordinate( 
        point,
        GerberFormatInfo["CoordFormat"],
        GerberFormatInfo["UnitMode"],
        GerberFormatInfo["ZeroFormat"] )
    # print(point + " -> ",newCoordX,newCoordY)
    translatedApertureFlashCoordinates.append( ( newCoordX, newCoordY ) )
# print("Point coordinates translation complete")

# We have now gathered the following information:
# 1. The coordinate format (absolute/incremental and Zero Format)
# 2. The unit mode (Inches or Millimeters)
# 3. A list of the all the D03 codes in the file (flashes/points)
# 4. A list of the D03 points in a human readable format
# 5. A list of aperture definitions (us

# compare a csv of test points to a gerber file
# TODO: Create a get_file_test_points function that
#       returns a float coordinate tuple
# test_coords = GerberProcessor.FileReader.get_file_test_points(TestPointFileName)
#
# num_test_coords = len(test_coords)
# found_count = 0
# not_found_count = 0
# missing_coords = []
# for t in test_coords:
#   if t not in translatedApertureFlashCoordinates:
#     missing_coords.append(t)
#   else:
#     found_count = found_count + 1
#
# not_found_count = num_test_coords - found_count
# print("Total Test Points:", num_test_coords)
# print("Number of matching test coordinates:", found_count)
# print("Number of missing test coordinates:", not_found_count)
# print("Missing Coordinates")
# for m in missing_coords:
#   print(m)
#
#
# # Look at point coordinates found in gerber file (D03 aperture flashes)
# rawApertureFlashCoordinates = GerberProcessor.FileReader.get_file_point_coordinates(GerberFileName)
# print("Total Points Identified:", len(rawApertureFlashCoordinates))
# #print("Raw Point -> Translated Point")
#
# translatedApertureFlashCoordinates = []
# for point in rawApertureFlashCoordinates:
#   newCoordX, newCoordY = GerberProcessor.LineReader.convert_raw_point_coordinate(
#     point,
#     GerberFormatInfo["CoordFormat"],
#     GerberFormatInfo["UnitMode"],
#     GerberFormatInfo["ZeroFormat"])
#   #print(point + " -> ",newCoordX,newCoordY)
#   translatedApertureFlashCoordinates.append((newCoordX, newCoordY))
# test_coord1 = GerberProcessor.FileReader.get_file_test_points(TestPointFileName, "MILS")
# num_test_coords = len(test_coord1)
# found_count = 0
# not_found_count = 0
# missing_coords = []
# for t in test_coord1:
#   if t not in translatedApertureFlashCoordinates:
#     missing_coords.append(t)
#   else:
#     found_count = found_count + 1
#
# not_found_count = num_test_coords - found_count
# print("Total Test Points:", num_test_coords)
# print("Number of matching test coordinates:", found_count)
# print("Number of missing test coordinates:", not_found_count)
# print("Missing Coordinates")
# for m in missing_coords:
#   print(m)
