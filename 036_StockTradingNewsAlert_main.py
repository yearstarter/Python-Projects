from datetime import date, timedelta
import requests


account_sid = os.environ['YOUR_TWILIO_SID']
auth_token = os.environ['YOUR_TWILIO_TOKEN']

stock_url = "https://www.alphavantage.co/query?"

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_APIKEY = "YOUR_STOCK_API" 
NEWS_LIMIT = 3


today = date(2024, 3, 16)
yesterday = today - timedelta(days=1)
before_yesterday = yesterday - timedelta(days=1)
# today = date.today()
print(yesterday, before_yesterday)


# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
#TODO: 1. check if in .csv is easier to get data from the last actual date (in case of weekends)
def get_stock_price(stock):
    stock_parameters = {
        "function": "TIME_SERIES_DAILY",
        "symbol": stock,
        "apikey": STOCK_APIKEY
    }
    response = requests.get(url=stock_url, params=stock_parameters)
    response.raise_for_status()
    stock_data = response.json()
    yesterday_price = float(stock_data["Time Series (Daily)"][str(yesterday)]["4. close"])
    before_yesterday_price = float(stock_data["Time Series (Daily)"][str(before_yesterday)]["4. close"])
    price_change = yesterday_price/before_yesterday_price

    print(yesterday_price, before_yesterday_price)
    return price_change


def get_news(stock, price_change):
    news_params = {
        "function": "NEWS_SENTIMENT",
        "tickers": stock,
        "sort": "LATEST",
        "limit": NEWS_LIMIT,
        "apikey": STOCK_APIKEY
    }
    response = requests.get(url=stock_url, params=news_params)
    news_data = response.json()
    news = news_data["feed"]
    price_change_percent = (price_change - 1) * 100
    news_text = f"{STOCK}: {price_change_percent}%"
    for i in range(3):
        each_news = news[i]
        news_text += f"""
            Timestamp: {each_news["time_published"]}
            Title: {each_news["title"]}. 
            Summary: {each_news["summary"]}
        """
    return news_text


def send_sms(text):
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
            body=text,
            from_='YOUR_TWILIO_NUMBER',
            to='NUMBER_TO_SEND'
    )


stock_price_change = get_stock_price(STOCK)

if not 0.95 < stock_price_change < 1.05:
    stock_news = get_news(STOCK, stock_price_change)
    send_sms(stock_news)
else:
    print(f"the price on {yesterday} is {stock_price_change} from the price on {before_yesterday}")
