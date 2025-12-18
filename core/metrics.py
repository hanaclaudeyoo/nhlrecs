from core.models import Game


class Metric:
    name: str

    def compute(self, game: Game) -> float:
        raise NotImplementedError


class TotalGoalsMetric(Metric):
    name = "total_goals"

    def compute(self, game: Game) -> float:
        if "total_goals" in game.summary:
            return game.summary["total_goals"]
        return len(game.goals)