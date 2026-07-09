from src.agents.router.adaptive_policy import (
    AdaptiveRoutingPolicy
)



def test_adjust_score_with_good_performance():

    policy = AdaptiveRoutingPolicy()


    result = policy.adjust_score(

        base_score=0.80,

        tool_name="analytics",

        performance={

            "analytics": 0.90

        }

    )


    assert result > 0.80



def test_adjust_score_with_bad_performance():

    policy = AdaptiveRoutingPolicy()


    result = policy.adjust_score(

        base_score=0.80,

        tool_name="analytics",

        performance={

            "analytics": 0.20

        }

    )


    assert result < 0.80



def test_adjust_score_without_history():

    policy = AdaptiveRoutingPolicy()


    result = policy.adjust_score(

        base_score=0.80,

        tool_name="analytics",

        performance={}

    )


    assert result < 0.80



def test_rank_tools():

    policy = AdaptiveRoutingPolicy()


    tools = [

        (

            type(
                "Tool",
                (),
                {
                    "name": "analytics"
                }
            )(),

            0.70,

            "base score"

        ),

        (

            type(
                "Tool",
                (),
                {
                    "name": "search"
                }
            )(),

            0.80,

            "base score"

        )

    ]


    result = policy.rank_tools(

        tools,

        {

            "analytics": 1.0,

            "search": 0.2

        }

    )


    assert result[0][0].name == "analytics"