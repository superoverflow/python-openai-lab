import textwrap
from unittest.mock import Mock
from youtube_api_lab.services.chatgpt import (
    ChatGPTService,
    summary_to_sentiment,
    StockSentiment,
)
from openai.types.chat import ChatCompletionMessage, ChatCompletion
from openai.types.chat.chat_completion import Choice

import pytest


@pytest.fixture
def mock_chat_completion() -> ChatCompletion:
    mock_choice = Choice(
        finish_reason="stop",
        index=0,
        message=ChatCompletionMessage(
            content='{\n    "market_sentiment": "Neutral",\n    "single_names": [\n        {\n            "name": "Jerome Powell",\n            "sentiment": "Neutral"\n        },\n        {\n            "name": "Fed President Williams",\n            "sentiment": "Neutral"\n        },\n        {\n            "name": "NASDAQ 100",\n            "sentiment": "Neutral"\n        },\n        {\n            "name": "S&P 500",\n            "sentiment": "Neutral"\n        },\n        {\n            "name": "Microsoft",\n            "sentiment": "Bearish"\n        },\n        {\n            "name": "Broadcom",\n            "sentiment": "Bearish"\n        },\n        {\n            "name": "SMH",\n            "sentiment": "Neutral"\n        },\n        {\n            "name": "KBH",\n            "sentiment": "Bearish"\n        },\n        {\n            "name": "Natural Gas",\n            "sentiment": "Bullish"\n        },\n        {\n            "name": "Bitcoin",\n            "sentiment": "Neutral"\n        },\n        {\n            "name": "Gold",\n            "sentiment": "Neutral"\n        },\n        {\n            "name": "Silver",\n            "sentiment": "Neutral"\n        },\n        {\n            "name": "Oil",\n            "sentiment": "Neutral"\n        },\n        {\n            "name": "VIX",\n            "sentiment": "Neutral"\n        }\n    ]\n}',
            role="assistant",
            function_call=None,
            tool_calls=None,
        ),
        logprobs=None,
    )

    return ChatCompletion(
        id="random-id",
        choices=[mock_choice],
        created=1631412345,
        model="gpt-3.5-turbo-16k",
        object="chat.completion",
    )


@pytest.fixture
def mock_chatgpt_client(mock_chat_completion) -> Mock:
    mock_client = Mock()
    mock_client.chat.completions.create.return_value = mock_chat_completion
    yield mock_client


def test_convert_chat_completion_to_sentiments():
    mock_summary = textwrap.dedent(
        """
        {
            "market_sentiment": "Bullish",
            "single_names": [
                {
                    "name": "SPY",
                    "sentiment": "Bullish"
                },
                {
                    "name": "GOLD",
                    "sentiment": "Bearish"
                },
                {
                    "name": "OIL",
                    "sentiment": "Neutral"
                }
            ]
        }
        """
    )

    result = summary_to_sentiment(mock_summary)
    expected = [
        StockSentiment(name="Market", sentiment="BULLISH"),
        StockSentiment(name="SPY", sentiment="BULLISH"),
        StockSentiment(name="GOLD", sentiment="BEARISH"),
        StockSentiment(name="OIL", sentiment="NEUTRAL"),
    ]
    assert result == expected


def test_parse_chat_completion_message_to_str(mock_chatgpt_client):
    summary = ChatGPTService(client=mock_chatgpt_client).summarize_transcript(
        "nothing important"
    )
    assert summary == [
        StockSentiment(name="Market", sentiment="NEUTRAL"),
        StockSentiment(name="Jerome Powell", sentiment="NEUTRAL"),
        StockSentiment(name="Fed President Williams", sentiment="NEUTRAL"),
        StockSentiment(name="NASDAQ 100", sentiment="NEUTRAL"),
        StockSentiment(name="S&P 500", sentiment="NEUTRAL"),
        StockSentiment(name="Microsoft", sentiment="BEARISH"),
        StockSentiment(name="Broadcom", sentiment="BEARISH"),
        StockSentiment(name="SMH", sentiment="NEUTRAL"),
        StockSentiment(name="KBH", sentiment="BEARISH"),
        StockSentiment(name="Natural Gas", sentiment="BULLISH"),
        StockSentiment(name="Bitcoin", sentiment="NEUTRAL"),
        StockSentiment(name="Gold", sentiment="NEUTRAL"),
        StockSentiment(name="Silver", sentiment="NEUTRAL"),
        StockSentiment(name="Oil", sentiment="NEUTRAL"),
        StockSentiment(name="VIX", sentiment="NEUTRAL"),
    ]
