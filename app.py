from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_restful import Resource, Api
import requests
import base64
import datetime
from dotenv import load_dotenv
import os
from requests.exceptions import RequestException, JSONDecodeError

# Load environment variables
load_dotenv()

app = Flask(__name__)
api = Api(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stk_push', methods=['POST'])
def stk_push():
    customer_phone = request.form.get('phone')

    # Set your credentials
    consumer_key = os.getenv('CONSUMER_KEY')
    consumer_secret = os.getenv('CONSUMER_SECRET')
    lipa_na_mpesa_online_passkey = os.getenv('PASSKEY')
    lipa_na_mpesa_online_shortcode = 174379

    # Generate the access token
    api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    try:
        response = requests.get(api_url, auth=(consumer_key, consumer_secret))
        response.raise_for_status()
    except RequestException as e:
        return {"error": str(e)}, 500

    try:
        access_token = response.json().get('access_token')
    except JSONDecodeError:
        return {"error": "Failed to decode the access token response"}, 500

    # Generate the password
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    password = base64.b64encode(str(lipa_na_mpesa_online_shortcode).encode() + lipa_na_mpesa_online_passkey.encode() + timestamp.encode()).decode('utf-8')

    # Set up the STK push request
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    payload = {
        "BusinessShortCode": lipa_na_mpesa_online_shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": customer_phone,
        "PartyB": lipa_na_mpesa_online_shortcode,
        "PhoneNumber": customer_phone,
        "CallBackURL": "https://d352-41-90-180-226.ngrok-free.app/mpesa_callback",
        "AccountReference": "CompanyXLTD",
        "TransactionDesc": "Payment of X"
    }
    stk_push_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'

    try:
        response = requests.post(stk_push_url, json=payload, headers=headers)
        response.raise_for_status()
    except RequestException as e:
        print(response.content)
        return {"error": str(e)}, 500

    try:
        return jsonify(response.json())
    except JSONDecodeError:
        return {"error": "Failed to decode the STK push response"}, 500

@app.route('/mpesa_callback', methods=['POST'])
def mpesa_callback():
    # Process the callback data here and update your application state accordingly
    # You can parse the JSON data and store it in your database or send notifications to users
    callback_data = request.json
    print(callback_data)
    return jsonify({"result": "success"})

if __name__ == '__main__':
    app.run(debug=True)
