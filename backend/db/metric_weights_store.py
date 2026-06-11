from backend.core.metrics import Metric, KEY_TO_METRIC
from backend.db.connection import get_connection


def read_metric_weights(
    profile_id: int
) -> dict[Metric, float]:
    with get_connection() as conn:
        metric_weight_rows = conn.execute(
            """
            SELECT metric_key, weight
            FROM metric_weights
            WHERE profile_id = ?
            """,
            (profile_id,)
        ).fetchall()

        metric_weight_dict = {}

        if not metric_weight_rows:
            for metric in KEY_TO_METRIC.values():
                metric_weight_dict[metric] = 1.0 / len(KEY_TO_METRIC)
        else:
            for row in metric_weight_rows:
                metric = KEY_TO_METRIC[row["metric_key"]]
                metric_weight_dict[metric] = row["weight"]
        
        return metric_weight_dict
