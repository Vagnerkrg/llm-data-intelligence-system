from src.agents.router.tool_scorer import ToolScorer
from src.agents.tools.tool_metadata import ToolMetadata



def test_tool_scorer_matches_capability():

    scorer = ToolScorer()


    tools = [

        ToolMetadata(

            name="analytics",

            description="Data analysis tool",

            capabilities=[

                "statistics",

                "aggregation"

            ]

        )

    ]


    result = scorer.score(
        "execute statistics analysis",
        tools
    )


    assert len(result) == 1

    assert result[0][0].name == "analytics"

    assert result[0][1] > 0



def test_tool_scorer_returns_empty_when_no_match():

    scorer = ToolScorer()


    tools = [

        ToolMetadata(

            name="analytics",

            description="Data analysis tool",

            capabilities=[

                "statistics"

            ]

        )

    ]


    result = scorer.score(
        "explain a story",
        tools
    )


    assert result == []



def test_tool_scorer_orders_by_score():

    scorer = ToolScorer()


    tools = [

        ToolMetadata(

            name="basic",

            description="Basic tool",

            capabilities=[

                "statistics"

            ]

        ),

        ToolMetadata(

            name="advanced",

            description="Advanced tool",

            capabilities=[

                "statistics",

                "aggregation"

            ]

        )

    ]


    result = scorer.score(
        "statistics aggregation",
        tools
    )


    assert result[0][0].name == "advanced"

    assert (
        result[0][1]
        >
        result[1][1]
    )