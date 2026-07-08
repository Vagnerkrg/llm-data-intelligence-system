import json

from pathlib import Path

from src.monitoring.dashboard_metrics import DashboardMetrics


def test_dashboard_summary(tmp_path):

    metrics = [

        {

            "route": "analysis",

            "execution_time": 0.10,

            "status": "success"

        },

        {

            "route": "rag",

            "execution_time": 0.30,

            "status": "success"

        },

        {

            "route": "unknown",

            "execution_time": 0.20,

            "status": "error"

        }

    ]


    file = tmp_path / "metrics.jsonl"


    with open(
        file,
        "w",
        encoding="utf-8"
    ) as f:

        for item in metrics:

            f.write(
                json.dumps(item)
                + "\n"
            )


    dashboard = DashboardMetrics(
        file
    )


    summary = dashboard.summary()


    assert summary["total_requests"] == 3

    assert summary["routes"]["analysis"] == 1

    assert summary["routes"]["rag"] == 1

    assert summary["routes"]["unknown"] == 1

    assert summary["success_rate"] == 0.6667

    assert summary["error_rate"] == 0.3333

    assert summary["average_execution_time"] == 0.2