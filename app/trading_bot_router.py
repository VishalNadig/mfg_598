from fastapi import APIRouter
import trading_bot
import database_handler
import yaml
from fastapi import Response
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
import matplotlib.pyplot as plt

with open(r"/home/megamind/megamind_config.yaml", "r") as file:
    CONFIG = yaml.safe_load(file)

router = APIRouter()


@router.get("/trading_bot/get_keys", tags=["trading_bot"])
def get_keys(first_name: str = "", last_name: str = "", user: str = ""):
    return database_handler.get_credentials(username=user, first_name=first_name, last_name=last_name)


@router.post("/trading_bot/add_keys", tags=["trading_bot"])
def add_keys(
    first_name: str = "",
    last_name: str = "",
    api_key: str = "",
    secret_key: str = "",
    email: str = "",
    google_auth_key: str = "",
):
    return database_handler.add_user(first_name=first_name, last_name=last_name, api_key=api_key, secret_key=secret_key, email=email, google_auth_key=google_auth_key
                       )


@router.patch("/trading_bot/update_keys", tags=["trading_bot"])
def update_keys(first_name: str = "",
    last_name: str = "",
    api_key: str = "",
    secret_key: str = "",
    email: str = "",
    google_auth_key: str = "",):
    return database_handler.update_user(first_name=first_name, last_name=last_name, api_key=api_key, secret_key=secret_key, email=email, google_auth_key=google_auth_key)


@router.delete("/trading_bot/delete_keys", tags=["trading_bot"])
def delete_keys(first_name: str, last_name: str, user: str):
    return database_handler.delete_user(first_name=first_name, last_name=last_name, username=user)



@router.get("/trading_bot/get_ticker", tags=["trading_bot"])
def get_ticker(coin_1: str = "BTC", coin_2: str = "USDT"):
    return trading_bot.get_ticker(coin_1, coin_2)


@router.get("/trading_bot/market_details", tags=["trading_bot"])
def get_markets_details(coin_1: str = "BTC", coin_2: str = "USDT"):
    return trading_bot.get_markets_details(coin_1=coin_1, coin_2=coin_2)


@router.get("/trading_bot/place_buy_limit_order", tags=["trading_bot"])
def place_buy_limit_order(user: str = "", coin_1: str = "BTC", coin_2: str = "USDT", price: float = 0.023, total_quantity: float = 450):
    return trading_bot.place_buy_limit_order(user=user, coin_1=coin_1, coin_2=coin_2, price=price, total_quantity=total_quantity)


@router.get("/trading_bot/place_sell_limit_order", tags=["trading_bot"])
def place_sell_limit_order(user: str = CONFIG['Owner']['alt_username'], coin_1: str = "BTC", coin_2: str = "USDT", price: float = 0.25, total_quantity: float = 450.0):
    return trading_bot.place_sell_limit_order(user=user, coin_1=coin_1, coin_2=coin_2, price=price, total_quantity=total_quantity)


@router.get("/trading_bot/place_market_buy_order", tags=["trading_bot"])
def place_market_buy_order(user: str = CONFIG['Owner']['alt_username'], coin_1: str = "BTC", coin_2: str = "USDT", total_quantity: float = 450):
    return trading_bot.place_market_buy_order(user=user, coin_1=coin_1, coin_2=coin_2, total_quantity=total_quantity)


@router.get("/trading_bot/place_market_sell_order", tags=["trading_bot"])
def place_market_sell_order(user: str = CONFIG['Owner']['alt_username'], coin_1: str = "BTC", coin_2: str = "USDT", total_quantity: float = 450.0):
    return trading_bot.place_market_sell_order(user=user, coin_1=coin_1, coin_2=coin_2, total_quantity=total_quantity)


@router.get("/trading_bot/create_multiple_orders", tags=["trading_bot"])
def create_multiple_orders(user: str = CONFIG['Owner']['alt_username'], orders: list = []):
    return trading_bot.create_multiple_orders(user=user, orders=orders)


@router.get("/trading_bot/get_active_orders", tags=["trading_bot"])
def get_active_orders(user: str = CONFIG['Owner']['alt_username']):
    return trading_bot.get_active_orders(user=user)


@router.get("/trading_bot/account_trade_history", tags=["trading_bot"])
def account_trade_history(user: str = CONFIG['Owner']['alt_username']):
    return trading_bot.account_trade_history(user=user)


@router.get("/trading_bot/cancel_order", tags=["trading_bot"])
def cancel_order(user: str = CONFIG['Owner']['alt_username'], ids: str = ""):
    return trading_bot.cancel_order(user=user, ids=ids)


@router.get("/trading_bot/cancel_all_orders", tags=["trading_bot"])
def cancel_all_orders(user: str = CONFIG['Owner']['alt_username']):
    return trading_bot.cancel_all_orders(user=user)


@router.get("/trading_bot/cancel_multiple_by_ids", tags=["trading_bot"])
def cancel_multiple_by_ids(user: str = CONFIG['Owner']['alt_username'], ids: list = []):
    return trading_bot.cancel_multiple_by_ids(user=user, ids=ids)


@router.get("/trading_bot/bot_trader", tags=["trading_bot"])
def auto_trader(user: str = CONFIG['Owner']['alt_username'], coin_1: str = "BTC", coin_2: str = "USDT", market: str = "Binance", screener_name: str = "Crypto", interval: str = "4h"):
    return trading_bot.bot_trader(user = user, coin_1 = coin_1, coin_2 = coin_2, market = market, screener_name=screener_name, interval=interval)


@router.get("/trading_bot/edit_price_of_orders", tags=["trading_bot"])
def edit_price_of_orders(user: str = CONFIG['Owner']['alt_username'], ids: list = [], price: float = ""):
    return trading_bot.edit_price_of_orders(user=user, ids=ids, price=price)


@router.get("/trading_bot/get_account_balance", tags=["trading_bot"])
def get_account_balance(user: str = CONFIG['Owner']['alt_username']):
    return trading_bot.get_account_balance(user=user)


@router.get("/trading_bot/get_candles", tags=["trading_bot"])
def get_candles(coin_1: str = "BTC",
    coin_2: str = "USDT",
    limit: int = 100,
    interval: str = "4h",
):
    return trading_bot.get_candles(coin_1=coin_1, coin_2=coin_2, limit=limit, interval=interval)


@router.get("/trading_bot/indicator_data", tags=["trading_bot"])
def indicator_data(
    coin_1: str = "BTC", coin_2: str = "USDT", market: str= "Binance", screener_name: str = "Crypto", interval: str = "4h"
):
    return trading_bot.indicator_data(coin_1=coin_1, coin_2=coin_2, market=market, screener_name=screener_name, interval=interval)


def generate_plot(coin_1: str = "BTC", coin_2: str = "USDT", interval: str = "1d", limit: int = 100) -> bytes:
    # create a sample dataframe
    candle_data = get_candles(coin_1=coin_1, coin_2=coin_2, interval=interval, limit=limit)
    # create the plot
    fig, ax = plt.subplots()
    ax.plot(candle_data['time'], candle_data['close'])
    ax.set_xlabel("Time")
    ax.set_ylabel(f"{coin_1}{coin_2} Close Price")
    # save the plot as a PNG image
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return buf.read()


@router.get("/trading_bot/plot_historical_data", tags=["trading_bot"])
def plot_historical_data(response: Response, coin_1: str = "BTC", coin_2: str = "USDT", interval: str = "1d", limit: int = 100):
    return Response(content=generate_plot(coin_1=coin_1, coin_2=coin_2, interval=interval, limit=limit), media_type="image/png")


@router.get("/trading_bot/send_mail", tags=["trading_bot"])
def send_mail(message: str, receiver: str):
    return trading_bot.send_mail(message=message, receiver=receiver)


@router.get("/trading_bot/price_tracker", tags=["trading_bot"])
def price_tracker(coin_1: str = "BTC", coin_2: str = "USDT", price: float = 0.0, mail: bool = False, receiver: str = "nadigvishal@gmail.com"):
    return trading_bot.price_tracker(coin_1=coin_1, coin_2=coin_2, price=price, mail=mail, receiver=receiver)


@router.get("/trading_bot/buy_sell_recommendation", tags=["trading_bot"])
def buy_sell_recommendation(coin_1: str = "", coin_2: str = "", market: str = "Binance", screener_name: str = "Crypto", interval: str = "4h", all_coins: bool = False):
    return trading_bot.buy_sell_recommendation(coin_1=coin_1, coin_2=coin_2, market=market, screener_name=screener_name, interval=interval,all_coins=all_coins)
