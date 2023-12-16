### What is it?
- A toy project to summarize financial video with ChatGPT
- Sample output
```
# notice market condition can change and output does not reflect my view/recommendation
poetry run python youtube_api_lab/main.py --playlist PL6iyqX0myJ2GvKOpg5kPsqReuehAfzRgs
Video: [zLa6qdMAP6A] [2023-12-14T21:54:29Z], title: [Fed Blow Off Top, Semi's Trade Levels, Crypto Action, Gold, Silver & Stocks]
StockSentiment(name='Market', sentiment=<SentimentEnum.NEUTRAL: 'NEUTRAL'>)
StockSentiment(name='Jerome Powell', sentiment=<SentimentEnum.BEARISH: 'BEARISH'>)
StockSentiment(name='Williams', sentiment=<SentimentEnum.NEUTRAL: 'NEUTRAL'>)
-------------------
Video: [t9w0wgDyP8E] [2023-12-13T23:41:44Z], title: [Dovish Fed Triggered Epic Market Rally, Mega Tech Warns, Gold, Silver and Crypto]
StockSentiment(name='Market', sentiment=<SentimentEnum.BULLISH: 'BULLISH'>)
StockSentiment(name='silver', sentiment=<SentimentEnum.BULLISH: 'BULLISH'>)
StockSentiment(name='Federal Reserve', sentiment=<SentimentEnum.BULLISH: 'BULLISH'>)
StockSentiment(name='US dollar', sentiment=<SentimentEnum.BEARISH: 'BEARISH'>)
StockSentiment(name='S&P 500', sentiment=<SentimentEnum.BULLISH: 'BULLISH'>)
StockSentiment(name='gold', sentiment=<SentimentEnum.NEUTRAL: 'NEUTRAL'>)
StockSentiment(name='Bitcoin', sentiment=<SentimentEnum.NEUTRAL: 'NEUTRAL'>)
StockSentiment(name='uranium', sentiment=<SentimentEnum.BULLISH: 'BULLISH'>)
StockSentiment(name='VIX', sentiment=<SentimentEnum.BEARISH: 'BEARISH'>)
-------------------
```

### How to run?
- create `.env` file
```
cp .env.template .env
# filling in API Keys
```
- run it
```
poetry install
poetry run youtube_api_lab/main.py --playlist <youtube playlist id>
```

## How to run unit test?
```
poetry run pytest
```