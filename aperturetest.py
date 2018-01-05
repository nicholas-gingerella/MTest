import sys
import GerberProcessor.FileReader
import GerberProcessor.LineReader
GerberFileName = "./Files/Gerber/art010.pho"
TestPointFileName = "./Files/CSV/art010-TestPoints.csv"

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

print("found necessary info")

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

apertures = GerberProcessor.FileReader.get_file_aperture_definitions(GerberFileName)
print("Found Aperture Defs:",len(apertures))
for a in apertures:
  print(a)

# tool select brings up more than the number of apertures, but this is fine, since
# the tool select is also picking up rectangle flashes, but we only care about
# circular flashes (for drill holes)
tool_selects = GerberProcessor.FileReader.get_file_tool_selects(GerberFileName)
print("tool selects:",len(tool_selects))
for t in tool_selects:
  print(t)
  

def get_circle_apertures(aprtrList, toolList):
  #use a dictionary to find whether the tool dcodes 
  #exist within the defined circle aperture Table
  toolDict = {}
  for a in toolList:
    toolDict[a[1]]=0
  
  #we now have a dict of circle apertures,
  #lets see if the items in the tool list
  #are found among the circle defs
  for a in aprtrList:
    if a[1] in toolDict:
      toolDict[a[1]]=1
  
  circleToolSelectList = []
  for key,value in toolDict.items():
    print(key, value)
    
    if value is 1:
      circleToolSelectList.append(key)
  
  return circleToolSelectList
  
print("tool selects that refer to circular apertures:")
validTools = get_circle_apertures(apertures, tool_selects)
gcodeDefs = {}
for t in validTools:
  print(t)
  gcodeDefs[t] = None
  
#Now that we have a list of tool selects that refer to circular apertures,
#Find the flash commands and see which xy coordinate points are associated
#with them. Should be a series of xy coordinates after the G54 command, once
#another G code command appears, that is the end of the flashes for this
#particular aperture

for tool in validTools:
  if tool in gcodeDefs:
    gcodeDefs[tool] = GerberProcessor.FileReader.get_aperture_flashes(GerberFileName, tool)
  else:
    print("tool not found in defined gcodes. did the get aperture flashes method pick up a bad Gcode defintion?")

for g,points in gcodeDefs.items():
  print("Aperture " + g)
  print(len(points))
  print(points)
  
  #gcodeDefs is now a dictionary, where the key is the G54Dcode, and the the value is a list of 
  #coordinate flashes for that particular aperture. We now have a grouping of points to a particulare
  #drill size (the aperture size), we just need to look up the aperture size of the Gcode to to know
  #what size drill that group of points will need
  