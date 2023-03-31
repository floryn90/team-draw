from flask import Flask, render_template, request, redirect, jsonify
from list import save_data, load_data
import json

app = Flask(__name__)

# Home page
@app.route('/')
def home():
    data = load_data()
    return render_template('index.html', favorites=data['favorites'])

# Add favorite TV show
@app.route('/add_favorite', methods=['POST'])
def add_favorite():
    data = load_data()
    index = request.form['index']
    title = request.form['title']
    season = request.form['season']
    releaseDate = request.form['releaseDate']
    streamer = request.form['streamer']

    new_favorite = {'index': index, 'title': title, 'season': season, 'releaseDate': releaseDate, 'streamer': streamer}
    data['favorites'].append(new_favorite)
    save_data(data)
    return redirect('/')

@app.route('/favorites/<int:index>', methods=['PUT'])
def update_favorite(index):
    with open('favorites.json', 'r') as f:
        favorites = json.load(f)

    favorite = favorites['favorites'][index]
    favorite['title'] = request.json['title']
    favorite['season'] = request.json['season']
    favorite['releaseDate'] = request.json['releaseDate']
    favorite['streamer'] = request.json['streamer']

    with open('favorites.json', 'w') as f:
        json.dump(favorites, f)

    return jsonify(favorite)


