import asyncio
import os
import webbrowser
import scrython
import urllib.request, json
import csv
from flask import Flask, Blueprint, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'T:/Python_Practice/Dragon Lookup/uploads'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

cards = []

@app.route("/", methods = ['POST', 'GET'])
def home():
    header = "Welcome to Dragon Lookup"
    subtitle = "This tool was designed to take the existing card inventory from our cases and digitize them for you to browse. Here you can request to have cards pulled from the case and set aside for you behind the counter."
    
    # Check that Inventory File is Present
    if os.path.isfile(UPLOAD_FOLDER + "/case_inventory.csv"):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Set Preview Card List
        cards.clear()
        card_strings = []

        # Retrieve File List from Uploaded CSV
        ifile  = open(UPLOAD_FOLDER + "/case_inventory.csv", "rt", encoding="utf8")
        read = csv.reader(ifile)
        next(read, None)
        size = read.line_num
        for row in read:
            row = str(row)
            row = row[2:size - 3]
            scryCard = scrython.cards.Named(fuzzy=row)
            card_strings.append(scryCard.name())

        #card_strings = ["Bitterbow Sharpshooter", "Ambush Paratrooper", "Calamaty's Wake", "Bitterbow Sharpshooter", "Ambush Paratrooper", "Calamaty's Wake", "Bitterbow Sharpshooter", "Ambush Paratrooper"]

        # For each card in the string, run a search and come back with Scryfall Information
        for card in card_strings:
            card_data = scrython.cards.Named(fuzzy=card)
            cards.append(card_data)
        return render_template("index.html", header=header, subtitle=subtitle, len = len(cards), cards=cards)
    else:
        return redirect(url_for("upload"))

@app.route("/upload", methods = ['POST', 'GET'])
def upload():
    header = "Upload an Inventory List Here"
    subtitle = "Here you can upload a Delver Lens file and update the catalog on this website."

    if request.method == 'POST': #Post
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'case_inventory.csv'))
        return render_template("upload-complete.html", header=header, subtitle=subtitle)
    else: #Get
        return render_template("upload.html", header=header, subtitle=subtitle)

@app.route("/search", methods = ['POST', 'GET'])
def search():
    header = "Search For A Card"
    subtitle = "Here you can search for a specific card in our inventory."

    return render_template("search.html", header=header, subtitle=subtitle)

@app.route("/lookup/", methods = ['POST', 'GET'])
def lookup():
    header = "Lookup A Card on Scryfall"
    subtitle = "Here you can search for a specific card on Scryfall. Listed Cards may not be in our inventory."

    set_code  = request.args.get('set_code', None)
    col_id  = request.args.get('col_id', None)

    if set_code != None:
        with urllib.request.urlopen('https://api.scryfall.com/cards/' + set_code.lower() + "/" + col_id) as url:
            card = json.load(url)
    else:
        card = ""
    
    return render_template("lookup.html", 
        header=header,
        subtitle=subtitle,
        card=card,
        set_code=set_code
    )

@app.route("/json")
def get_json():
    return jsonify({'name': 'tim', 'coolness': 10})

@app.route("/data")
def get_data():
    data = request.json
    return jsonify(data)

@app.route("/go-to-home")
def go_to_home():
    return redirect(url_for("app.home"))

# Methods ----------
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def open_url(url):
    return webbrowser.open_new_tab(url)

# Boilerplate Application Security ----------
if __name__ == '__main__':
    app.run(port=80, host="0.0.0.0")