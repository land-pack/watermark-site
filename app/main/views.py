from datetime import datetime
from flask import render_template, session, redirect, url_for, abort, flash, request, current_app, make_response
from flask.ext.login import login_required, current_user
from . import main


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/user/<username>')
def user(username):
    return render_template('user.html')


@main.route('/contact')
def contact():
    return render_template("contact.html")
