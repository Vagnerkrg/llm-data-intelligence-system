from typing import Dict, List



class AnswerEvaluator:
    """
    Evaluates generated answers from RAG executions.

    Measures answer quality using local metrics:
    - answer length
    - context availability
    - keyword overlap
    - faithfulness approximation
    - completeness approximation
    """


    def evaluate(
        self,
        question: str,
        answer: str,
        documents: List[Dict]
    ) -> Dict:
        """
        Generates answer quality metrics.
        """


        context = " ".join(

            [
                item.get(
                    "document",
                    ""
                )

                for item in documents

            ]

        ).lower()



        answer_text = answer.lower()



        question_words = self._extract_words(
            question
        )


        answer_words = self._extract_words(
            answer_text
        )


        context_words = self._extract_words(
            context
        )



        relevance_score = self._calculate_overlap(
            question_words,
            context_words
        )



        faithfulness_score = self._calculate_overlap(
            answer_words,
            context_words
        )



        completeness_score = min(
            len(answer_words) / 100,
            1.0
        )



        quality_score = round(

            (
                relevance_score
                +
                faithfulness_score
                +
                completeness_score

            )
            /
            3,

            4

        )



        return {

            "question": question,

            "answer_length": len(
                answer_words
            ),

            "documents_used": len(
                documents
            ),

            "context_relevance": round(
                relevance_score,
                4
            ),

            "faithfulness": round(
                faithfulness_score,
                4
            ),

            "completeness": round(
                completeness_score,
                4
            ),

            "quality_score": quality_score

        }



    def _extract_words(
        self,
        text: str
    ) -> set:
        """
        Extracts normalized words.
        """


        words = (

            text

            .replace(
                "\n",
                " "
            )

            .replace(
                ".",
                " "
            )

            .replace(
                ",",
                " "
            )

            .split()

        )


        return set(

            word.strip()

            for word in words

            if len(word.strip()) > 3

        )



    def _calculate_overlap(
        self,
        first_set: set,
        second_set: set
    ) -> float:
        """
        Calculates semantic approximation
        using word overlap.
        """


        if not first_set:

            return 0.0



        intersection = (

            first_set

            &
            
            second_set

        )



        return len(intersection) / len(first_set)