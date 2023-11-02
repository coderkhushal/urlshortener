from flask import Flask, render_template, redirect, url_for, request
import random
import string
import json

app = Flask(_name_)

shortned_url = {}

def get_short_url(length=6):
    chars = string.ascii_letters + string.digits
    short_url = "".join(random.choice(chars) for _ in range(length))
    return short_url

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == 'POST':
        long_url = request.form["long_url"]
        short_url = get_short_url()
        while short_url in shortned_url:
            short_url = get_short_url()
        shortned_url[short_url] = long_url
        with open("short_urls.json", "w") as file:
            json.dump(shortned_url, file)
        return f"Shortned URL: {request.url_root}{short_url}"
    return render_template("index.html")


@app.route("/<short_url>")
def redirect_url(short_url):
    long_url = shortned_url.get(short_url)
    if long_url:
        return redirect(long_url)
    else:
        return "URL Not Found...", 404 
    
if __name__ == "__main__":
    with open("short_urls.json", "r") as file:
        shortned_url = json.load(file)
    app.run(debug=True)