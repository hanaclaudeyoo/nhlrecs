from core.models import Game


class Metric:
    name: str

    def compute(self, game: Game) -> float:
        raise NotImplementedError


class TotalGoalsMetric(Metric):
    name = "total_goals"

    def compute(self, game: Game) -> float:
        if self.name in game.summary:
            return game.summary[self.name]
        
        return len(game.goals)


class FinalGoalDifferentialMetric(Metric):
    name = "final_goal_diff"

    def compute(self, game: Game) -> float:
        if self.name in game.summary:
            return game.summary[self.name]
        
        away_score = 0
        home_score = 0
        for goal in game.goals:
            if goal.team == game.away_team:
                away_score += 1
            elif goal.team == game.home_team:
                home_score += 1
            else:
                raise ValueError(f"Unknown team {goal.team}, expected {game.away_team} or {game.home_team}")
        return abs(away_score - home_score)
