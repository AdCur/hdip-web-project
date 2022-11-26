from application import app, db
from flask import render_template, request, redirect, url_for, flash
from application.models import Crypto
from application.forms import CryptoForm
import json, requests

@app.route('/', methods=['GET', 'POST'])
def index():
    form = CryptoForm()
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '1f9a613b-ffd6-4113-bc87-dc1f833dca02',
    }
    params = {
    'convert':'USD'
    }
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    crypto_list = []
    cryptos = Crypto.query.all()
    for crypto in cryptos:
        json = requests.get(url.format(crypto.name), params=params, headers=headers).json()
        coin = {
            'name': crypto.name,
            'price': json['data'][0]['quote']['USD']['price']
        }
        crypto_list.append(coin)

    if form.validate_on_submit():
        new_crypto = Crypto(name = form.name.data)
        db.session.add(new_crypto)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('index.html', form=form, data=crypto_list)

