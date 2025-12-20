from core.models import Game


class Metric:
    name: str
    maximize: bool

    def compute(self, game: Game) -> float:
        raise NotImplementedError

    def score(self, game: Game) -> float:
        value = self.compute(game)
        return value if self.maximize else -value


class TotalGoalsMetric(Metric):
    name = "total_goals"
    maximize = True

    def compute(self, game: Game) -> float:
        return len(game.goals)


class FinalGoalDifferentialMetric(Metric):
    name = "final_goal_diff"
    maximize = False

    def compute(self, game: Game) -> float:
        away_score = 0
        home_score = 0
        for goal in game.goals:
            if goal.team == game.away_team:
                away_score += 1
            else:
                home_score += 1
        return abs(away_score - home_score)


class LeadChanges(Metric):
    name = "lead_changes"
    maximize = True

    def compute(self, game: Game) -> float:
        num_lead_changes = 0
        leader = None
        away_score = 0
        home_score = 0
        for goal in game.goals:
            if goal.team == game.away_team:
                away_score += 1
            else:
                home_score += 1

            if away_score > home_score:
                new_leader = game.away_team
            elif home_score > away_score:
                new_leader = game.home_team
            else:
                new_leader = None  # tie

            if leader and new_leader and new_leader != leader:
                num_lead_changes += 1
            leader = new_leader
        return num_lead_changes


class MaxLead(Metric):
    name = "max_lead"
    maximize = False

    def compute(self, game: Game) -> float:
        max_lead = 0
        away_score = 0
        home_score = 0
        for goal in game.goals:
            if goal.team == game.away_team:
                away_score += 1
            else:
                home_score += 1
            if abs(away_score - home_score) > max_lead:
                max_lead = abs(away_score - home_score)
        return max_lead