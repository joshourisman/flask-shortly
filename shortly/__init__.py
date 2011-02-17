from flask import Flask, render_template, redirect

app = Flask(__name__)

def expand(short_url):
    return 'http://www.google.com/'

@app.route("/<short_url>+")
def to_info_page(short_url):
    return render_template('template.html', short_url=short_url)

@app.route("/<short_url>")
def to_long_url(short_url):
    return redirect(expand(short_url))

