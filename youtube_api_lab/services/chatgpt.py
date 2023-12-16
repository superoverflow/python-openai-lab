from dataclasses import dataclass
from enum import StrEnum
import json
from textwrap import dedent
from openai import OpenAI
from openai.types.chat import ChatCompletion


class SentimentEnum(StrEnum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    NEUTRAL = "NEUTRAL"


@dataclass(frozen=True, kw_only=True)
class StockSentiment:
    name: str
    sentiment: SentimentEnum


class ChatGPTService:
    def __init__(self, client: OpenAI):
        self.client = client

    def summarize_transcript(self, transcript: str) -> list[StockSentiment]:
        summary = self._summarize_transcript(transcript)
        summary_str = summary.choices[0].message.content
        return summary_to_sentiment(summary_str)

    def _summarize_transcript(
        self, transcript: str, model="gpt-3.5-turbo-16k"
    ) -> ChatCompletion:
        result = self.client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": dedent(
                        """
                        You analyze speech and summarize in json format:
                        {
                            "market_sentiment": "<Bullish/Neutral/Bearish>",
                            "single_names": [
                                {
                                    "name": "<name>",
                                    "sentiment": "<bullish/bearish>"
                                },
                                ...
                            ]
                        }
                        """
                    ),
                },
                {
                    "role": "user",
                    "content": transcript,
                },
            ],
        )
        return result


def summary_to_sentiment(summary: str) -> list[StockSentiment]:
    results = []
    json_summary = json.loads(summary)
    market_sentiment = json_summary["market_sentiment"]
    results.append(
        StockSentiment(name="Market", sentiment=SentimentEnum(market_sentiment.upper()))
    )

    single_names = json_summary["single_names"]
    for sentiment in single_names:
        results.append(
            StockSentiment(
                name=sentiment["name"],
                sentiment=SentimentEnum(sentiment["sentiment"].upper()),
            )
        )

    return results
