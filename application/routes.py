from application import app, db
from flask import render_template, request, redirect, url_for, flash
from application.models import Crypto
from application.forms import CryptoForm

@app.route('/', methods=['GET', 'POST'])
def index():
    form = CryptoForm()
    if form.validate_on_submit():
        new_crypto = Crypto(name = form.name.data)
        db.session.add(new_crypto)
        db.session.commit()
    return render_template('index.html', form=form)

