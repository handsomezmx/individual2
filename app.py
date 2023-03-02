
from flask import Flask, jsonify, request
import requests
app = Flask(__name__)

def change(amount):
    # calculate the resultant change and store the result (res)
    res = []
    coins = [1,5,10,25] # value of pennies, nickels, dimes, quarters
    coin_lookup = {25: "quarters", 10: "dimes", 5: "nickels", 1: "pennies"}

    # divide the amount*100 (the amount in cents) by a coin value
    # record the number of coins that evenly divide and the remainder
    coin = coins.pop()
    num, rem  = divmod(int(amount*100), coin)
    # append the coin type and number of coins that had no remainder
    res.append({num:coin_lookup[coin]})

    # while there is still some remainder, continue adding coins to the result
    while rem > 0:
        coin = coins.pop()
        num, rem = divmod(rem, coin)
        if num:
            if coin in coin_lookup:
                res.append({num:coin_lookup[coin]})
    return res

def paychange(pay,price):
    if pay<price:
        return False
    return change(pay-price)



@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    print("I am inside hello world")
    return 'Dear user! i can give you the weather of the city you want to check: /weather/cityname'

# @app.route('/weather/<city>')
# def getweather(city):

#     result = f"Weather of {city}"
#     return result
@app.route('/weather', methods=['GET'])
def get_weather():
    # Get the 'city' query parameter from the request URL
    city = request.args.get('city')

    # Make a request to the weather API using the 'city' parameter
    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=9abe65e7ec4b7402e7eac470654a4ae4')

    # Check if the API request was successful
    if response.status_code == 200:
        # Extract the temperature from the API response and convert it to Celsius
        temperature = response.json()['main']['temp'] - 273.15

        # Return the temperature as a JSON response
        return jsonify({'temperature': temperature})
    else:
        # Return an error message as a JSON response
        return jsonify({'error': 'Failed to retrieve weather data'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
