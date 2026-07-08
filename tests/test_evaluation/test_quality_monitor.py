from src.evaluation.quality_monitor import QualityMonitor



class FakeEvaluator:


    def evaluate(
        self,
        question,
        answer
    ):

        return {

            "score": 1.0,

            "quality": "good",

            "issues": []

        }



class FakeHistory:


    def __init__(self):

        self.saved = []



    def save(
        self,
        data
    ):

        self.saved.append(
            data
        )



        return data



class TestQualityMonitor:


    def test_quality_evaluation(self):


        monitor = QualityMonitor(

            evaluator=FakeEvaluator(),

            history=FakeHistory()

        )


        result = monitor.evaluate(

            "Quantos produtos existem?",

            "Existem 3 produtos.",

            "analysis"

        )


        assert result["score"] == 1.0

        assert result["quality"] == "good"

        assert result["route"] == "analysis"