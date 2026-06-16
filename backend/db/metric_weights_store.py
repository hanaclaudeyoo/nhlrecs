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

        metric_weight_dict = {
            metric: 1.0 / len(KEY_TO_METRIC)
            for metric in KEY_TO_METRIC.values()
        }

        for row in metric_weight_rows:
            metric = KEY_TO_METRIC[row["metric_key"]]
            metric_weight_dict[metric] = row["weight"]
        
        return metric_weight_dict


def write_metric_weights(
    profile_id: int,
    weights_by_key: dict[str, float]
) -> None:
    with get_connection() as conn:
        conn.executemany(
            """
            INSERT INTO metric_weights (profile_id, metric_key, weight)
            VALUES (?, ?, ?)
            ON CONFLICT(profile_id, metric_key)
            DO UPDATE SET weight = excluded.weight
            """,
            [
                (profile_id, metric_key, weight)
                for metric_key, weight in weights_by_key.items()
            ]
        )
        conn.commit()
