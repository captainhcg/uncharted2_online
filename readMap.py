import simplejson
import ast

WIDTH = 2158;
HEIGHT = 1080;
LOCATION = "asset/map";
COMPRESSED_MAP = "asset/compressed_map"
PATH_MAP = "asset/path_map"
JSON_MAP = "asset/json_map"
WORLD_MAP = [None]*HEIGHT

def main():
	initMapFromBinary()
	createPathMap()
	# initMapFromList()
	# with open(COMPRESSED_MAP, 'w') as map_file:
	#	map_file.write(simplejson.dumps(str(getSection(json=True))))

def createPathMap():
	blocks = set((1, 6, 7, 9, 10, 16, 30, 31, 32, 33, 34, 35, 36, 37, 38, 46, 47, 48, 49, 50, 52, 55, 56, 57, 59, 60))
	path_map = [None]*HEIGHT
	for i in xrange(HEIGHT):
		row = [None]*WIDTH
		for j in xrange(WIDTH):
			row[j] = 0 if WORLD_MAP[i][j] in blocks else 1
		path_map[i] = row
	with open(PATH_MAP, 'w') as map_file:
		map_file.write(simplejson.dumps(str(getSection(json=True, source_map=path_map))))

#TODO finish it
def initMapFromList():
	with open(COMPRESSED_MAP, 'r') as map_file:
		line = map_file.readline()
	map_list = ast.literal_eval(line)
	return map_list

def initMapFromBinary():
	world_array = bytearray()
	with open(LOCATION, 'rb') as map_file:
		for line in map_file.readlines():
			world_array += bytearray(line)	
	ptr = iter(world_array)
	for i in xrange(HEIGHT):
		row = [None]*WIDTH
		for j in xrange(WIDTH):
			ch = ptr.next()
			row[j] = ch
		WORLD_MAP[i] = row

def getSection(x=0, y=0, width=2158, height=1080, json=False, source_map=WORLD_MAP):
	result = []
	for i in xrange(y, y+height):
		last_tile = source_map[i][x]
		last_count = 0
		row_data = []
		for j in xrange(x, x+width):
			if source_map[i][j] == last_tile:
				last_count += 1
			else:
				if json:
					row_data.append({last_tile: last_count})
				else:
					row_data.append((last_tile, last_count))
				last_count = 1
				last_tile = source_map[i][j]
		if json:
			row_data.append({last_tile: last_count})
		else:
			row_data.append((last_tile, last_count))
		result.append(row_data)
	return result

if __name__ == "__main__":
    main()
