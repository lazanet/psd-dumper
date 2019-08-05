from util import *

nations = dump_nations()
for nation in nations:
	champs = dump_championships(nations[nation])
	for ch in champs:
		champs[ch] = dump_clubs(champs[ch])
	nations[nation] = champs

save(exp_json(nations), os.path.join("data", "championships.json"))

