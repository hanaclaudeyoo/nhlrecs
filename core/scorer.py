from core.metrics import Metric
from core.models import Game


class Scorer:
    def __init__(
        self,
        metrics: list[Metric],
        weights: dict[str, float] = None,
    ):
        self.metrics = metrics
        self.weights = weights

        assert sum(weights.values()) == 1.0

        if weights is None:
            num_metrics = len(self.metrics)
            self.weights = {m.name: 1.0/num_metrics for m in metrics}
    

    def percentile_normalize(self, values: list[float]):
        n = len(values)
        if n <= 1:
            return [0] * n
        
        sorted_vals = sorted(values)
        return [sorted_vals.index(v) / (n - 1) for v in values]


    def score_games(self, games: list[Game]) -> dict[str, float]: # returns {game ID: score}
        # calculate score per metric
        scores_metric: dict[str, list[float]] = {}
        for metric in self.metrics:
            scores_metric[metric.name] = [metric.compute(g) for g in games]
        
        # normalize scores per metric
        scores_normal: dict[str, list[float]] = {}
        for metric, scores in scores_metric:
            scores_normal[metric] = self.percentile_normalize(scores)
        
        # combine into one weighted aggregate score
        scores_weighted = dict[str, float] = {}
        for i, g in enumerate(games):
            score = sum([self.weights[m] * scores_normal[m][i] for m in self.metrics])
            scores_weighted[g.game_id] = score
        return scores_weighted
        

    def rank_games(self, games: list[Game]) -> list[Game]:
        scores = self.score_games(games)
        return sorted(
            games,
            key=lambda g: scores[g.game_id],
            reverse=True
        )