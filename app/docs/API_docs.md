# API DOCUMENTATION

# ENDPOINTS

## BASE URL: https://192.168.0.82:6969


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
