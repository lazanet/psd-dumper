from util import *
from fetchPlayers import fetch_player

if __name__ == '__main__':

	playersToFetch = []

	with open(os.path.join("..", "data", 'last_time_players.json')) as json_file:
	    last = json.load(json_file)
	now = time()
	url = host+"/PSD/Select/Updates/Updates.php?Nation=global&Year={}&Month={}".format(now["Y"], now["m"])
	data = links_extract(url)
	for a in data:
		
		if a.has_attr('name'):
			date = a.get('name').split('-')
			print(date)
			if (int(date[2]) != last["y"] or date[1] != last["M"] or int(date[0]) >= last["d"]):
				continue
			break
		if a.has_attr('href'):
			curr_id = a.get('href')
			if "Players.php" in curr_id:
				continue # Club name

			curr_id = int(curr_id.replace("Player.php?Id=", "").split("&")[0])
			playersToFetch.append(curr_id)
	
	with Pool() as pool: 
		pool.starmap(fetch_player, [(curr_id, True) for curr_id in playersToFetch])	
	
	save(exp_json(time()), os.path.join("..", "data", 'last_time_players.json'))		
	
