from backend.core.models import Game


PERIOD_LENGTH_SECONDS = 20 * 60


class Metric:
    key: str
    maximize: bool

    def compute(self, game: Game) -> float:
        raise NotImplementedError

    def score(self, game: Game) -> float:
        value = self.compute(game)
        return value if self.maximize else -value


class TotalGoalsMetric(Metric):
    key = "total_goals"
    maximize = True

    def compute(self, game: Game) -> float:
        return len(game.goals)


class FinalGoalDifferentialMetric(Metric):
    key = "final_goal_diff"
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


class LeadChangesMetric(Metric):
    key = "lead_changes"
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


class MaxLeadMetric(Metric):
    key = "max_lead"
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
    
class MaxTimeBetweenGoalsMetric(Metric):
    key = "max_time_between_goals"
    maximize = False

    def compute(self, game: Game) -> float:
        max_time_btwn = 0

        prev_time = 0
        for goal in game.goals:
            gap = goal.time_elapsed_seconds - prev_time
            if gap > max_time_btwn:
                max_time_btwn = gap
            prev_time = goal.time_elapsed_seconds

        # consider time between last goal and end of game
        if len(game.goals) < 1:
            print(game)
        if game.goals[-1].time_elapsed_seconds < PERIOD_LENGTH_SECONDS: # exclude overtime
            gap = PERIOD_LENGTH_SECONDS - game.goals[-1].time_elapsed_seconds
            if gap > max_time_btwn:
                max_time_btwn = gap
        
        return max_time_btwn
    

ALL_METRIC_KEYS = [
    "total_goals",
    "final_goal_diff",
    "lead_changes",
    "max_lead",
    "max_time_between_goals"
]

KEY_TO_METRIC = {
    "total_goals": TotalGoalsMetric(),
    "final_goal_diff": FinalGoalDifferentialMetric(),
    "lead_changes": LeadChangesMetric(),
    "max_lead": MaxLeadMetric(),
    "max_time_between_goals": MaxTimeBetweenGoalsMetric()
}