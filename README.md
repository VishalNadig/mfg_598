# Cryptocurrency Trading using FastAPI

This project is Cryptocurrency Trading bot I coded using python for a project for my Graduate degree course in MFG 598 - Engineering Computing with Python at Arizona State University.

# TRADING BOT DOCUMENTATION

# GENERAL INFORMATION
1. You will need to have the config files with you. The megamind_config file is ideal.
2. You will also need to install and setup poetry first.
3. Make sure the keys of the user are in the config file. Else add them.
4. Make sure to install and update all dependencies using poetry install and poetry update.
5. Make sure the path of the config file matches the path given by paths.py in paths folder.

# FUNCTIONS
## get_keys(first_name: str = "", last_name: str = "", user: str = "") -> tuple:
    """Get API key and secret key for the specified user. If user is not mentioned then, first name and last name of the user can be used to retrieve the keys.

    Args:
        first_name (str, optional): First name of the user. Defaults to "".
        last_name (str, optional): Last name of the user. Defaults to "".
        user (str, optional): Username to retrieve the keys. Defaults to "".

    Returns:
        tuple: The API key and the secret key.
    """

## add_keys(first_name: str = "", last_name: str = "", api_key: str = "", secret_key: str = "") -> None:
    """Add API key and the secret key for a new user. If the user already exists. Return exception.

    Args:
        first_name (str, optional): First name of the user. Defaults to "".
        last_name (str, optional): Last name of the user. Defaults to "".

    Returns: None
    """

## get_market_data(user: str = "", currency: list = []) -> pd.DataFrame:
    """Get market data and information. We can get the market data and the information of all the currencies or only the specified currencies if they are passed as the argument to this function.

    Args:
        user (str, optional): _description_. Defaults to "".
        currency (str, optional): _description_. Defaults to "".

    Returns:
        pd.DataFrame: _description_
    """


## place_buy_limit_order(user: str, market: str, price: float, total_quantity: float) -> None:

    Args:
        user (str): Username of the account to place the order in.
        market (str): The market pair to place the order. Eg: BTCUSDT, TATAINR.
        price (float): The price at which to buy.
        total_quantity (float): The number of stocks or coins to buy.

    Returns: None.
    """

## place_sell_limit_order(user: str, market: str, price: float, total_quantity: float) -> None:
    """Place a buy limit order on the market pair specified.

    Args:
        user (str): Username of the account to place the order in.
        market (str): The market pair to place the order. Eg: BTCUSDT, TATAINR.
        price (float): The price at which to sell.
        total_quantity (float): The number of stocks or coins to sell.

    Returns: None.
    """

## place_market_buy_order(user: str, market: str, total_quantity: float) -> None:
    """Place a buy market order on the market pair specified. The order is placed at the current market price. This order gets executed immediately.

    Args:
        user (str): Username of the account to place the order in.
        market (str): The market pair to place the order. Eg: BTCUSDT, TATAINR.
        total_quantity (float): The number of stocks or coins to buy.

    Returns: None.
    """

## place_market_sell_order(user: str, market: str, total_quantity: float) -> None:
    """Place a sell market order on the market pair specified. The order is placed at the current market price. This order gets executed immediately.

    Args:
        user (str): Username of the account to place the order in.
        market (str): The market pair to place the order. Eg: BTCUSDT, TATAINR.
        total_quantity (float): The number of stocks or coins to buy.

    Returns: None.
    """
## create_multiple_orders(user: str, orders: list = []) -> None:
    """Create multiple orders at once.

    Args:
        user (str): The username of the account to place the order in.
    """

## active_orders(user: str) -> dict:
    """Get the current buy or sell active orders for the user.

    Args:
        user (str): The username of the account to get the active orders from.

    Returns:
        dict: List of all the active orders
    """

## account_trade_history(user: str) -> dict:
    """Get the account trade history of the user.

    Args:
        user (str): The username of the account for which the trade history is to be fetched.

    Returns:
        dict: The history of trades made by the user.
    """
## cancel_order(user: str, ids) -> None:
    """Cancel a particular order of the user.

    Args:
        user (str): The username of the account for whom the order needs to be cancelled.
        id (_type_): The order id.
    """


## cancel_all_orders(user: str) -> None:
    """Cancel all the active orders of the user.

    Args:
        user (str): The username of the account for which the order needs to be cancelled.
    """

## cancel_multiple_by_ids(user: str, ids: list) -> None:
    """Cancel multiple orders given by the list of ids for a particular user.

    Args:
        user (str): The username of the account for which the orders need to be cancelled.
        ids (list): The list of order ids to cancel.
    """

## edit_price_of_orders(user: str, ids, price: float) -> None:
    """Edit the buy or sell price of the orders.

    Args:
        user (str): The username of the account for which the price needs to be edited.
        ids (_type_): The order id for which the price needs to be edited
        price (float): _description_
    """
## auto_trader(user: str, symbol: str, market: str, screener_name: str, interval: str) -> None:
    """Execute trades automatically 24/7 based on input parameters

    Args:
        user (str): The username of the account to auto_trade in.
        symbol (str): Ticker Ex: "CIPLA", "TATAMOTORS", "XVGBTC", "BTCUSDT".
        market (str): he name of the exchange ("NSE", "BSE", "Binance").
        screener_name (str): Either "India" or "Crypto".
        interval (str): Interval of chart "1m", "5m", "30m", "1h", "2h", "4h", "1d", "1W", "1M
    """
## get_account_balance(user: str = "VishalNadig") -> dict:
    """Get the account balance of the user.

    Args:
        user (str, optional): The username of the account to get the balance of. Defaults to "VishalNadig".

    Returns:
        dict: The dictionary of the account balances of all the currencies.
    """

## get_candles(market: str, coin1: str, coin2: str, limit: int = 100, interval: str = "4h")-> pd.DataFrame:
    """Get historical candle data of a cryptocurrency for price prediction and analysis.

    Args:
        market (str): B- Binance, I- CoinDCX, HB- HitBTC, H- Huobi, BM- BitMex.
        coin1 (str): Symbol of coin1 (BTC, XRP, SHIB, DOGE, ADA)
        coin2 (str): Symbol of coin2 (BTC, USDT).
        limit (int, optional): maximum 1000 candles.
        interval (str, optional): [1m   5m  15m 30m 1h  2h  4h  6h  8h  1d  3d  1w  1M] m -> minutes, h -> hours, d -> days, w -> weeks, M -> months. Defaults to "4h".

    Returns:
        pd.DataFrame: The historical candle data of the coin market pair.
    """

## indicator_data(symbol, market: str, screener_name: str = "Crypto", interval: str = "4h") -> list:
    """Get complete indicator data from Trading View.

    Args:
        symbol (_type_): Ticker Ex: "CIPLA", "TATAMOTORS", "XVGBTC", "BTCUSDT"
        market (str): Exchange ("NSE", "BSE", "Binance")
        screener_name (str, optional): Either "India" or "Crypto". Defaults to "Crypto".
        interval (str, optional): Interval of chart "1m", "5m", "30m", "1h", "2h", "4h", "1d", "1W", "1M". Defaults to "4h".

    Returns:
        list: The indicator data for the market pair in an exchange.
    """

## parser_activated_bot() -> None:
    """A CLI to spin up an instance of the bot.
    """

## add_keys_cli() -> None:
    """Add keys via the interactive terminal.
    """

## plot_historical_data(coin_1: str = "BTC", coin_2: str = "USDT", interval: str = "1d", limit: int = 100) -> pyplot:
    """Plot the historical price of any cryptocurreny to perform technical and fundamental analysis

    Args:
        coin_1 (str, optional): Ticker symbol of the crypto. Defaults to "BTC".
        coin_2 (str, optional): Ticker symbol of the comparison crypto. Defaults to "USDT".
        interval (str, optional): Time interval to get the price of the crypto. Defaults to "1d".
        limit (int, optional): The number of candles to fetch. Max limit = 1000. Defaults to 100.

    Returns:
        pyplot: Plot of the data
    """

## send_mail(message: str) -> None:
    """Send mail function to send a mail and deliver the message.

    Args:
        message (str): The message to be sent through the mail.
    """

## price_tracker(coin_1: str = "BTC", coin_2: str = "USDT", price: float = 0.0, mail: bool = False) -> str:
    """Get the current price of the coin_1 and send a mail

    Args:
        coin_1 (str, optional): The price of the coin you want to check. Defaults to "BTC".
        coin_2 (str, optional): The coin you want to check the price against. Defaults to "USDT".
        price (float, optional): The price above which if the price of coin_1 reaches you want to send the mail. Defaults to 0.0.
        mail (boolm optional): Set to True to send mail of the price. Defaults to False.
    """

## generate_plot(coin_1: str = "BTC", coin_2: str = "USDT", interval: str = "1d", limit: int = 100) -> bytes:
    """Generate the plot for the endpoint /plot_historical_data

    Args:
        coin_1 (str, optional): The price of the coin you want to check. Defaults to "BTC".
        coin_2 (str, optional): The coin you want to check the price against. Defaults to "USDT".
        interval (str, optional): The time interval you need to plot the data. Defaults to 1d.
        limit (boolm optional): The number of datapoints you want to plot. Defaults to 100.
    """

# API DOCUMENTATION

# ENDPOINTS

## BASE URL: https://192.168.0.207:6969


 ## /GET /trading_bot/get_keys"

    """first_name: First name of the user.
       last_name: Last name of the user.
       user: The Username of the user. Optional.
    """

## /POST /trading_bot/add_keys"

    first_name: First name of the user.
    last_name: Last name of the user.
    api_key: API key of the user.
    secret_key: Secret key of the user.
    email: Email of the user.
    google_auth_key: Google auth key of the user.



## /PATCH /trading_bot/update_keys"

    first_name: First name of the user.
    last_name: Last name of the user.
    api_key: API key of the user.
    secret_key: Secret key of the user.
    email: Email of the user.
    google_auth_key: Google auth key of the user.


## /DELETE /trading_bot/delete_keys"

    first_name: First name of the user.
    last_name: Last name of the user.
    user: Username of the user



## /GET /trading_bot/get_ticker"

    coin_1: Coin to get the ticker details.
    coin_2: The base currency.
    coins_list: The lst of coins to get the ticker details of.


## /GET /trading_bot/market_details"

    coin_1: Coin to get the market details of.
    coin_2: The base currency.
    coins_list: The list of coins to get the market details of.
    all_coins: Flag to get market details of all coins or just coin_2. Defaults to False.



## /GET /trading_bot/place_buy_limit_order"

    user: Username of the user. Optional.
    coin_1: Coin to place the buy order for.
    coin_2: The base currency.
    price: THe price to buy the crypto at.
    total_quantity: The total quantity of crypto to trade.



## /GET /trading_bot/place_sell_limit_order"

    user: Username of the user. Optional.
    coin_1: Coin to get the
    coin_2: The base currency.
    price: The price to sell the crypto at.
    total_quantity: The total quantity to sell.



## /GET /trading_bot/place_market_buy_order"

    user: Username of the user. Optional.
    coin_1: Coin to place the market buy order.
    coin_2: The base currency.
    total_quantity: The total quantity to buy.



## /GET /trading_bot/place_market_sell_order"

    user: Username of the user. Optional.
    coin_1: Coin to place the market sell order.
    coin_2: The base currency.
    total_quantity: The total quantity to sell.



## /GET /trading_bot/create_multiple_orders"

    user: Username of the user. Optional.
    orders: The order IDs to place.



## /GET /trading_bot/get_active_orders"

    user: Username of the user. Optional.



## /GET /trading_bot/account_trade_history"

    user: Username of the user. Optional.



## /GET /trading_bot/cancel_order"

    user: Username of the user. Optional.
    ids: The order id to cancel.



## /GET /trading_bot/cancel_all_orders"

    user: Username of the user. Optional.


## /GET /trading_bot/cancel_multiple_by_ids"

    user: Username of the user. Optional.
    ids: The order ids to cancel them.


## /GET /trading_bot/edit_price_of_orders"

    user: Username of the user. Optional.
    ids: The order ids to edit the price of.
    price: The price to set the orders.


## /GET /trading_bot/get_account_balance"

    user: Username of the user. Optional.


## /GET /trading_bot/get_candles"

    coin_1: Coin to get the candle data of.
    coin_2: The base currency.
    limit: The number of datapoints to get the data of.
    interval: The time period to get the datapoints of.



## /GET /trading_bot/indicator_data"

    coin_1: Coin to get the indicator data.
    coin_2: The base currency.
    market: The exchange to trade in.
    screener_name: The stock market to trade in. Defaults to "Crypto".
    interval: "4h"


## /GET /trading_bot/plot_historical_data"

    coin_1: Coin to plot the historical data.
    coin_2: The base currency.
    interval: The time interval to get the data. Defaults to 4h.
    limit: The number of datapoints to plot.


## /GET /trading_bot/send_mail"

    message: The message to send to the user.
    receiver: The reciever email ID.


## /GET /trading_bot/price_tracker"

    coin_1: Coin to get the
    coin_2: The base currency.
    price: The price at which you want the alert.
    mail: Flag to send the mail or not.
    receiver: The reciever email ID.


## /GET /trading_bot/buy_sell_recommendation"

    coin_1: Coin to get the recommendation of.
    coin_2: The base currency.
    market: The exchange to use. Defaults to Binance.
    screener_name: The market to trade in. Crypto or India. Defaults to Crypto.
    interval: The time interval to get the recommendation.
    all_coins: Get recommendation of all coins or only coin_2. Defaults to false.
