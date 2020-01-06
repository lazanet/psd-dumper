<?php
/*
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>


*/

	header("Content-Type: text/plain");
	ini_set('zlib.output_compression', 0);
	ob_start();
	ob_implicit_flush(true);
	ob_end_clean();

	ini_set('display_errors', 1);
	ini_set('display_startup_errors', 1);
	error_reporting(E_ERROR);

	$PATH_TO_DATA = "./data/";

	
	function getTeamIds($teamNameSearch)
	{
		global $PATH_TO_DATA; 
		$innerHTML = "";

		$teamsJSON = json_decode(file_get_contents($PATH_TO_DATA."championships.json"));
		foreach ($teamsJSON as $regionName => $region)
			foreach ($region as $leagueName => $league)
				foreach($league as $teamName => $teamId)
					if (strpos(strtolower($teamName), strtolower($teamNameSearch)) !== FALSE)
						$innerHTML .= $teamId ."; ".$teamName."\n";
		return $innerHTML;
	}
	function getTeamPlayers($teamId)
	{
		global $PATH_TO_DATA; 
		$innerHTML = "\n\n";

		$teamPlayers = json_decode(file_get_contents($PATH_TO_DATA."squads/$teamId.json"));
		foreach ($teamPlayers as $id => $name)
			if (is_numeric($id))
				$innerHTML .= $name ."; ".$id."\n";
		return $innerHTML;
	}
	
	function findPlayers($nameSearch)
	{
		global $PATH_TO_DATA; 
		$innerHTML = "";

		$playersJSON = json_decode(file_get_contents($PATH_TO_DATA."all_players.json"));
		foreach ($playersJSON as $id => $name)
			if (strpos(strtolower($name), strtolower($nameSearch)) !== FALSE)
				$innerHTML .= $name ."; ".$id."; ; ;\n";
		return $innerHTML;
	}

	function getPlayerStats($id, $num)
	{
		global $PATH_TO_DATA; 

		$player = json_decode(file_get_contents($PATH_TO_DATA."players/$id.json"), true);
		if ($num < 13) $num = 6;
		if (!in_array($num, array(6, 14, 15, 16, 17))) $num = 999;
		
		return str_replace("\n\n","\n",$player["$num"]);
	}

	if (empty($_GET))
	{
		echo "PSD MIRROR API\n";
		echo "Usage: \n Get request \n Parameters: \n\n !important! \n * v = ??? - GAME VERSION (INTEGER, 6=pes6, 2018=pes18)\n\n One of rest:\n * p = ??? - playerId to fetch \n * s = ??? - playerName to search\n * t = ??? - teamId to fetch\n * n = ??? - teamName to search\n";
		exit();
	}
	
	if (isset($_GET['p']))
		echo getPlayerStats($_GET['p'], intval($_GET['v']));
	else if (isset($_GET['s']))
		echo findPlayers($_GET['s']);
	else if (isset($_GET['t']))
		echo getTeamPlayers($_GET['t']);
	else if (isset($_GET['n']))
		echo getTeamIds($_GET['n']);
	else	
		echo "Wrong parameter!";

?>
