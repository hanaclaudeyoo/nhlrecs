from core.metrics import Metric
from core.models import Game


class Scorer:
    def __init__(
        self,
        metrics: list[Metric],
        weights: dict[str, float] = None,
    ):
        self.metrics = metrics

        if weights is None:
            num_metrics = len(self.metrics)
            self.weights = {m.name: 1.0/num_metrics for m in metrics}
        else:
            self.weights = weights
            s = sum(self.weights.values())
            assert abs(1.0 - s) < 1e-6, f"Metric weights must sum to 1.0, got {s}"
    

    def percentile_normalize(self, values: list[float]) -> list[float]:
        n = len(values)
        if n <= 1:
            return [0.0] * n

        sorted_vals = sorted(values)
        percentiles: dict[float, float] = {}
        i = 0
        while i < n:
            j = i
            while j < n and sorted_vals[j] == sorted_vals[i]:
                j += 1 # skip duplicates

            avg_rank = (i + j - 1) / 2 # average rank for ties
            percentiles[sorted_vals[i]] = avg_rank / (n - 1)

            i = j
        return [percentiles[v] for v in values]


    def score_games(self, games: list[Game]) -> dict[str, float]: # returns {game ID: score}
        # calculate score per metric
        scores_metric: dict[str, list[float]] = {}
        for metric in self.metrics:
            scores_metric[metric.name] = [metric.score(g) for g in games]
        
        # normalize scores per metric
        scores_normal: dict[str, list[float]] = {}
        for metric, scores in scores_metric.items():
            scores_normal[metric] = self.percentile_normalize(scores)
        
        # combine into one weighted aggregate score
        scores_weighted: dict[str, float] = {}
        for i, g in enumerate(games):
            score = sum([self.weights[m.name] * scores_normal[m.name][i] for m in self.metrics])
            scores_weighted[g.game_id] = score
        return scores_weighted
        

    def rank_games(self, games: list[Game]) -> list[Game]:
        scores = self.score_games(games)
        return sorted(
            games,
            key=lambda g: (-scores[g.game_id], g.date),
        )
