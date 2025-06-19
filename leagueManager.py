import os
import json
from dotenv import load_dotenv
from espn_api.baseball import League
from custom_box_score import H2HCategoryBoxScore
import statsapi
from collections import defaultdict
from typing import Union

class LeagueManager:
    def __init__(self, league_id: int, year: int):
        load_dotenv()
        self.espn_s2 = os.getenv("ESPN_S2")
        self.swid = os.getenv("SWID")
        self.league_id = league_id
        self.year = year
        self._connect()

    def _connect(self):
        self.league = League(
            league_id=self.league_id,
            year=self.year,
            espn_s2=self.espn_s2,
            swid=self.swid
        )
        self._patch_box_score_class()  # ✅ now called correctly

    def _patch_box_score_class(self):
        self.league._box_score_class = H2HCategoryBoxScore  # ✅ your custom one

    def get_league(self):
        return self.league

    def list_teams(self):
        print("\n📋 League Teams:")
        for idx, team in enumerate(self.league.teams):
            print(f"[{idx}] {team.team_name} (Team ID: {team.team_id})")
            
            

class FreeAgents:
    def __init__(self, league_manager: LeagueManager):
        self.manager = league_manager
        self.league = league_manager.get_league()

    def get_free_agents(self):
        positions = {"OF": 5, "DH": 11, "SP": 14, "RP": 15, "IF": 19}
        agents = {}
        for position, pos_id in positions.items():
            fa_pool = self.league.free_agents(size=100, position_id=pos_id)
            names = [name.strip("()") for name in str(fa_pool).replace("Player", "").strip("[]").split(", ") if name]
            player_details = FreeAgents.lookup_players(names)
            agents[position] = {
                p["id"]: p["fullName"] for p in player_details if "id" in p and "fullName" in p
            }
        return agents

    @staticmethod
    def lookup_players(names):
        players = []
        for name in names:
            try:
                result = statsapi.lookup_player(name)
                if result:
                    players.extend(result)
            except Exception as e:
                print(f"⚠️ Lookup failed for '{name}': {e}")
        return players
    
if __name__ == "__main__":
    manager = LeagueManager(league_id=121531, year=2025)
    league = manager.get_league()
    manager.list_teams()

    # Save teams
    team_dict = {team.team_id: team.team_name for team in league.teams}
    with open("teams.json", "w") as f:
        json.dump(team_dict, f, indent=4)
    print("✅ Saved to teams.json")

    # ✅ Get and display free agents
    fa = FreeAgents(manager)
    free_agents = fa.get_free_agents()
    print("\n🆓 Free Agents by Position:")
    for pos, players in free_agents.items():
        print(f"{pos}: {list(players.values())[:5]}")  # show first 5 per position

    # ✅ Utility function
    def get_free_agents_by_position(manager: LeagueManager) -> dict:
        return FreeAgents(manager).get_free_agents()

