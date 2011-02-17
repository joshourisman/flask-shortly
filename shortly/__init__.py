from flask import Flask, render_template, redirect

from models import Url

app = Flask(__name__)

@app.route("/<short_url>+")
def to_info_page(short_url):
    url = Url(short_url)
    return render_template('template.html', short_url=url.short_url)

@app.route("/<short_url>")
def to_long_url(short_url):
    url = Url(short_url)
    return redirect(url.long_url)

