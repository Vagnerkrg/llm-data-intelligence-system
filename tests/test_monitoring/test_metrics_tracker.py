import json
from pathlib import Path

from src.monitoring.metrics_tracker import MetricsTracker



class TestMetricsTracker:


    def test_record_metric(self, tmp_path):

        metrics_file = (
            tmp_path /
            "metrics.jsonl"
        )


        tracker = MetricsTracker(
            metrics_file
        )


        tracker.start_timer()


        result = tracker.record(
            route="analysis"
        )


        assert result["route"] == "analysis"

        assert result["status"] == "success"

        assert result["execution_time"] >= 0


        assert metrics_file.exists()


        lines = (
            metrics_file
            .read_text()
            .splitlines()
        )


        assert len(lines) == 1


        data = json.loads(
            lines[0]
        )


        assert data["route"] == "analysis"