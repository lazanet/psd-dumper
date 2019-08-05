from util import *

def handle(curr_id):
	with count.get_lock():
		count.value += 1
		print("{:8.4f}% id={} ".format(count.value*100/listLen, curr_id), end="")
	
	if os.path.isfile(os.path.join("..", "data", "players", "{}.json".format(curr_id))):
		print("skip")
		return

	print("working")

	tmp = {}
	for version in [6, 14, 15, 16, 17, 999]:
		tmp[version] = dump_stats(curr_id, version)
	save(exp_json(tmp), os.path.join("..", "data", "players", "{}.json".format(curr_id)))
	print("")
	return

def init_globals(cnt, ln):
	global count
	global listLen
	count = cnt
	listLen = ln

if __name__ == '__main__':
	with open(os.path.join("..", "data", 'all_players.json')) as json_file:
	    data = json.load(json_file)
	
	count = Value('i', -1)
	init_globals(count, len(data))

	with Pool(initializer=init_globals, initargs=(count, len(data), )) as pool: 
		pool.map(handle, data.keys())
	
	#for key in data:
	#	handle(data[key])	
	
