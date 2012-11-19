import simplejson
import ast

WIDTH = 2158;
HEIGHT = 1080;
LOCATION = "asset/map";
COMPRESSED_MAP = "asset/compressed_map"
JSON_MAP = "asset/json_map"
WORLD_MAP = [None]*HEIGHT

def main():
	initMapFromBinary()
	# initMapFromList()

#TODO finish it
def initMapFromList():
	with open(COMPRESSED_MAP, 'r') as map_file:
		line = map_file.readline()
	map_list = ast.literal_eval(line)
	for row in map_list:
		for sector in row:
			pass


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

def getSection(x=0, y=0, width=2158, height=1080, json=False):
	result = []
	for i in xrange(y, y+height):
		last_tile = WORLD_MAP[i][x]
		last_count = 0
		row_data = []
		for j in xrange(x, x+width):
			if WORLD_MAP[i][j] == last_tile:
				last_count += 1
			else:
				if json:
					row_data.append({last_tile: last_count})
				else:
					row_data.append((last_tile, last_count))
				last_count = 1
				last_tile = WORLD_MAP[i][j]
		if json:
			row_data.append({last_tile: last_count})
		else:
			row_data.append((last_tile, last_count))
		result.append(row_data)
	return result

if __name__ == "__main__":
    main()
    with open(JSON_MAP, 'w') as map_file:
  		map_file.write(simplejson.dumps(str(getSection(json=True))))