from flask import Flask, render_template, redirect

from models import Url

app = Flask(__name__)

@app.route("/<short_url>+")
def info_page(short_url):
    url = Url(short_url)
    return render_template('info.html', url=url)

@app.route("/<short_url>")
def to_long_url(short_url):
    url = Url(short_url)
    return redirect(url.long_url)

@app.route('/')
def index():
    return render_template('index.html')
