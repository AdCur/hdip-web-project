from application import app, db
from flask import render_template, redirect, request, url_for, flash
from application.models import Crypto, Bmi
import json, requests
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64

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

#draw graph with retrieved database coin history
@app.route('/draw-graph/<id>',methods=["GET","POST"])
def draw_graph(id):
    # create empty list
    price_list=[]
    # name needs to be lowercase
    name = id.lower()
    # xrp does not work, fix:
    if name == 'xrp':
        name = 'ripple'
    # call API
    url = "https://api.coingecko.com/api/v3/coins/"+ name +"/market_chart?vs_currency=usd&days=7&interval=daily"
    # make the url json format
    json = requests.get(url, headers={'Accept': 'application/json'}).json()
    # append prices to price list
    for x,y in json['prices']:
        price_list.append(y)
    #creating the days list for the x axis
    days = [1,2,3,4,5,6,7,8]
    x_axis = days 
    y_axis = price_list
    img = BytesIO()
    plt.plot(x_axis,y_axis)
    plt.xlabel('days')
    plt.ylabel('prices')
    plt.title('weekly price')
    #img = BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode('utf8')
    return render_template('graph.html', graph_url=graph_url, id=id)

# financial page
@app.route('/financial', methods=['GET', 'POST'])
def financial():
    return render_template('financial.html')

# bmi page
@app.route('/bmi', methods=['GET', 'POST'])
def bmi():
    # create an empty bmi list
    bmi_list = []
    # query the database and return all bmi's
    bmi = Bmi.query.all()
    for x in bmi:
        bmi_obj = {
            'id': x.id,
            'height': x.height,
            'weight': x.weight,
            
        }
        bmi_list.append(bmi_obj)
    # if the form button is submitted
    if request.method == 'POST':
        # get the weight and height from form
        weight = request.form['weight']
        height = request.form['height']
        # create a new bmi object with the name entered 
        bmi = Bmi(weight=weight, height=height)
        #add and commit it to the database
        url = "https://body-mass-index-bmi-calculator.p.rapidapi.com/metric"

        querystring = {"weight":weight,"height": height}

        headers = {
            "X-RapidAPI-Key": "6214e17d92msh20d7503d6a121b4p190dfejsn4a50b3733c49",
            "X-RapidAPI-Host": "body-mass-index-bmi-calculator.p.rapidapi.com"
        }

        json_r = requests.request("GET", url, headers=headers, params=querystring).json()
        
        bmi.bmi_result =json_r['bmi']
            #'result':json_r['bmi'],

        #adding and commiting values to the database
        db.session.add(bmi)
        db.session.commit()
        
        # flash a message 
        flash('Body Mass Index added successfully!')
        # reload the page
        return redirect(url_for('bmi'))
    return render_template('bmi.html', bmi=bmi_list)



@app.route('/delete-Bmi/<id>', methods=["GET", "POST"])
def delete_BMi(id):
    # query the database to retrieve the bmi via the coin id
    bmi = Bmi.query.get(id)
    # delete the bmi from the database
    db.session.delete(bmi)
    db.session.commit()
    # flash message
    flash("Bmi deleted successfully")
    # reload the page above to see the changes
    return redirect(url_for('bmi'))

@app.route('/gen-visual/<id>', methods=["GET", "POST"])
def gen_visual(id):
    bmi = Bmi.query.get(id)
    if bmi.bmi_result <18.5:
        print('skinny')
    elif bmi.bmi_result >=18.5 and bmi.bmi_result<24.9:
        print('ideal weight')
    elif bmi.bmi_result >=24.9 and bmi.bmi_result< 29.9:
        print('slightly over')
    elif bmi.bmi_result >=29.9 and bmi.bmi_result< 34.9:
        print('chubby')
    elif bmi.bmi_result >=34.9 and bmi.bmi_result< 39.9:
        print('chubby')
    elif bmi.bmi_result >=40:
        print('severly obese')
    else:
        print('error with finding bmi')
        
    

    
    print("connection working")

    return redirect(url_for('bmi'))
