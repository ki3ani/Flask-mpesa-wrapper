# Flask-mpesa-wrapper

This Flask application provides a simple wrapper around the M-Pesa API, allowing you to easily integrate M-Pesa payments into your applications. It handles the STK push process, providing a seamless experience for your users.

### Prerequisites
To use this wrapper, you'll need:

-Python 3.6 or later
-A Safaricom Developer Account
-M-Pesa API credentials (Consumer Key and Consumer Secret)  
Mpsea link: [m-pesa](https://developer.safaricom.co.ke/)

### Installation
Clone the repository:

`git clone https://github.com/yourusername/mpesa-flask-wrapper.git`

Change to the project directory:

`cd mpesa-flask-wrapper`

Install the required dependencies:

`pip install -r requirements.txt'`

Create a .env file in the project directory and add your M-Pesa API credentials:

```CONSUMER_KEY=your_consumer_key
CONSUMER_SECRET=your_consumer_secret
PASSKEY=your_lipa_na_mpesa_passkey
```
Make sure to replace your_consumer_key, your_consumer_secret, and your_lipa_na_mpesa_passkey with your actual M-Pesa API credentials.

### Usage
Run the Flask application:

`python app.py`

The application will initiate an STK push to the user's phone, prompting them to enter their M-Pesa PIN to complete the transaction.

Once the transaction is completed, you'll receive a callback at the /mpesa_callback endpoint. You can process the callback data and update your application state accordingly.


## M-Pesa API Documentation
For more information about the M-Pesa API and its capabilities, please refer to the official M-Pesa API documentation.[Doc](https://developer.safaricom.co.ke/docs)




`




