from flask import Flask, render_template, redirect, request, url_for

from models import Url

app = Flask(__name__)

@app.route("/<short_url>+")
def info_page(short_url):
    url = Url(short_url)
    return render_template('info.html', url=url)

@app.route("/<short_url>")
def to_long_url(short_url):
    url = Url(short_url, request=request)
    return redirect(url.long_url)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create/', methods=['POST',])
def add_url():
    long_url = request.form['long_url']
    short_url = request.form['short_url']
    new_url = Url()
    short_url = new_url.shorten(long_url, short_url)
    return redirect(url_for('info_page', short_url=short_url))
