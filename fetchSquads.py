from util import *

with open(os.path.join("data",'championships.json')) as json_file:
    nations = json.load(json_file)

all_players = {}

for nation in nations:
	for championship in nations[nation]:
		for club in nations[nation][championship]:
			club_id = nations[nation][championship][club]

			squad = dump_players(club_id)
			all_players.update(squad)

			squad["info"] = "{} >> {}".format(nation, championship)
			squad["name"] = club
			save(exp_json(squad), os.path.join("data","squads","{}.json".format(club_id)))

save(exp_json(all_players), os.path.join("data","all_players.json"))
