from application import app, db
from flask import render_template, redirect, request, url_for, flash
from application.models import Crypto
import json, requests

# crypto page (initial page)
@app.route('/', methods=['GET', 'POST'])
def crypto():
    # create an empty crypto list
    crypto_list = []
    # query the database and return all cryptos
    cryptos = Crypto.query.all()
    # for loop through all cryptos in database
    if len(cryptos) > 0:
        for crypto in cryptos:
            # API url
            url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=eur&ids="+crypto.name+"&order=market_cap_desc&per_page=100&page=1&sparkline=false&price_change_percentage=24h"
            # make the url json format
            json = requests.get(url, headers={'Accept': 'application/json'}).json()
            # if the user entered a coin name that does not exist, it will return an error
            # so we have to check if the length of the json response is > 0 to prevent the error
            if len(json) > 0:
            # create a coin object
                coin = {
                    'id': crypto.id,
                    'image': json[0]['image'],
                    'name': json[0]['name'],
                    'symbol': json[0]['symbol'],
                    'percentage': json[0]['price_change_percentage_24h'],
                    'price': json[0]['current_price']
                }
                # append new coin object to list
                crypto_list.append(coin)      

    # if the form button is submitted
    if request.method == 'POST':
        # get the cryptocurrency added to the database
        crypto_name = request.form['name'].lower()
        # create a new crypto object with the name entered 
        new_crypto = Crypto(name=crypto_name)
        # check if it already exists in the database
        existing_crypto = Crypto.query.filter_by(name=crypto_name).first()
        if existing_crypto:
            # if the crypto is in database, flash a message
            flash('Cryptocurrency is already in the database.')
        else:
            # if it does not exist, add and commit it to the database
            db.session.add(new_crypto)
            db.session.commit()
            # flash a message 
            flash('Cryptocurrency added successfully!')
            # reload the page
            return redirect(url_for('crypto'))
    return render_template('crypto.html', coins=crypto_list)

# delete a coin 
@app.route('/delete-coin/<id>', methods=["GET", "POST"])
def delete_coin(id):
    # query the database to retrieve the coin via the coin id
    coin = Crypto.query.filter_by(id=id).first()
    # delete the coin from the database
    db.session.delete(coin)
    db.session.commit()
    # flash message
    flash("Coin deleted successfully")
    # reload the page above to see the changes
    return redirect(url_for('crypto'))

# financial page
@app.route('/financial', methods=['GET', 'POST'])
def financial():
    return render_template('financial.html')

# bmi page
@app.route('/bmi', methods=['GET', 'POST'])
def bmi():
    return render_template('bmi.html')