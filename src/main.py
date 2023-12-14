from config import TRADE_API_KEY, TRADE_API_SECRET_KEY, BASE_URL
import sentiment_analysis as sa
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.stream import TradingStream
def main():

    client = TradingClient(TRADE_API_KEY, TRADE_API_SECRET_KEY, paper = True)
    account = dict(client.get_account())
    # for k,v in account.items():
    #     print(f"{k:30}{v}")
    
    news_articles = sa.get_latest_news()

    sentiment_score = 0

    for article in news_articles:
        sentiment = sa.get_sentiment(article['content'])
        print(f"Title: {article['title']}")
        print(f"Sentiment: {sentiment}")

        sentiment_score += sentiment

    avg_sentiment = sentiment_score / len(news_articles)
    print(f"Average sentiment score: {avg_sentiment} on the most recent {len(news_articles)}")
    if avg_sentiment > 0.1:
        order_details = MarketOrderRequest(
            symbol = "NVDA",
            qty = 100,
            side = OrderSide.BUY,
            time_in_force = TimeInForce.GTC
        )

        order = client.submit_order(order_data=order_details)
        print(order)
        
    elif avg_sentiment < - 0.1:
        order_details = MarketOrderRequest(
            symbol = "NVDA",
            qty = 100,
            side = OrderSide.SELL,
            time_in_force = TimeInForce.GTC
        )

        order = client.submit_order(order_data=order_details)
        print(order)
    trades = TradingStream(TRADE_API_KEY, TRADE_API_SECRET_KEY, paper = True)
    async def trade_status(data):
        print(data)

    trades.subscribe_trade_updates(trade_status)
    trades.run()


if __name__ == "__main__":
    main()
