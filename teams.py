# team.py

class Team:
    def __init__(self, league, team_index: int):
        self.league = league
        self.team_index = team_index

    def get_roster(self):
        team = self.league.teams[self.team_index]
        return [f"{player.name} ({player.position})" for player in team.roster]

    def get_team_name(self):
        return self.league.teams[self.team_index].team_name
    
    print(get_roster, get_team_name)
