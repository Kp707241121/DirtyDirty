from espn_api.baseball.box_score import H2HCategoryBoxScore as BaseH2HCategoryBoxScore

# Your stat mapping
STATS_MAP = {
    20: 'R',
    5: 'HR',
    21: 'RBI',
    17: 'OBP',
    23: 'SB',
    48: 'K',
    53: 'W',
    57: 'SV',
    47: 'ERA',
    41: 'WHIP',
}

class H2HCategoryBoxScore(BaseH2HCategoryBoxScore):
    def __init__(self, data, pro_schedule, year, scoring_period=all):
        print("✅ Using custom H2HCategoryBoxScore")  # optional debug line
        super().__init__(data, pro_schedule, year, scoring_period)

    def _process_team(self, team_data, is_home_team):
        super()._process_team(team_data, is_home_team)

        team_stats = {}

        if team_data:
            score_by_stat = team_data.get("cumulativeScore", {}).get("scoreByStat", {})
            for stat_id_str, result in score_by_stat.items():
                stat_id = int(stat_id_str)
                stat_name = STATS_MAP.get(stat_id)
                if stat_name:
                    team_stats[stat_name] = {
                        "value": result.get("score"),
                        "result": result.get("result")
                    }

        if is_home_team:
            self.home_stats = team_stats
        else:
            self.away_stats = team_stats
