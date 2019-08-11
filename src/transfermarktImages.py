from util import *

url = "https://www.transfermarkt.com/schnellsuche/ergebnis/schnellsuche?query="

with open(os.path.join("..", "data", 'all_players.json')) as json_file:
	    players = json.load(json_file)

for curr_id, player_name in players.items():
	curr_url = url+urllib.parse.quote(player_name).replace(" ","+")
	
	target = os.path.join("..", "data", "player_photos", curr_id)
	if (os.path.isfile(target + ".jpg") or os.path.isfile(target + ".png")):
		continue
	print (target)
	
	print(curr_url)
	data = fetch_url(curr_url)
	soup = BeautifulSoup(data, "lxml")
	found = False
	for img in soup.select("img.bilderrahmen-fixed"):
		link = img.get("src").replace("mediumfotos", "spielerfotos").replace("small", "header").split("?")[0]
		extension = link.split(".")[-1]
		target = target + "." + extension
		download_url(link, target)
		found = True
		break
	if not found:
		copy(os.path.join("..", "data", 'player_photos', "no_img.jpg"), target+".png")
	print("Done {}!".format(player_name))
	
