import ccxt
import time
from flask import Flask, jsonify

app = Flask(__name__)

# define trading function
def trade():
    # instantiate the exchange object with your API key and secret
    exchange = ccxt.crypto_com({
        'apiKey': 'api key',
        'secret': 'api secret',
    })

    # set trading parameters
    symbol = 'ETH/USDT'
    amount = 0.005563
    stop_loss = 0.0035
    take_profit = 0.0075

    # get current price
    ticker = exchange.fetch_ticker(symbol)
    price = ticker['last']

    # place buy order
    order = exchange.create_order(symbol, 'limit', 'buy', amount, price)

    # place stop loss and take profit orders
    stop_loss_price = price * stop_loss
    take_profit_price = price * take_profit
    exchange.create_order(symbol, 'stop_loss_limit', 'sell', amount, stop_loss_price, {'stopPrice': stop_loss_price})
    exchange.create_order(symbol, 'limit', 'sell', amount, take_profit_price)

    print('Trade executed')
    print(order)

# Define a Flask route function to handle incoming requests
@app.route('/api/trade')
def handle_trade_request():
    # Call the trade() function to execute your trading logic
    trade()
    
    # Return a message as the response
    return jsonify({'message': 'Trading executed successfully'})

# Run the Flask app if this file is executed directly
if __name__ == '__main__':
    app.run()
