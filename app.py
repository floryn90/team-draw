from flask import Flask, render_template, request, redirect, jsonify
from list import save_data, load_data
import math
import random

application = Flask(__name__, static_url_path='/static')

# Home page
@application.route('/fotbal-luni-db')
def home():
    data = load_data()
    return render_template('index.html', players=data['players'])

# Add favorite TV show
@application.route('/add_player', methods=['POST'])
def add_player():
    data = load_data()
    players = data['players']

    name = request.json.get('name')  # Get player name from request

    # Check if the name already exists
    if any(player['name'] == name for player in players):
        return jsonify({'error': 'Player name already exists.'}), 400

    # Find the last index and increment by one
    if players:
        last_index = max(player['index'] for player in players)
        index = last_index + 1
    else:
        index = 1

    # Create new player object
    new_player = {'index': index, 'name': name, 'stars': 1, 'starVotes': [], 'votes': 0}

    # Add the new player to the list of players
    players.append(new_player)

    # Save the updated data
    save_data(data)

    return redirect('/fotbal-luni-db')


@application.route('/players/<int:index>', methods=['PUT'])
def update_favorite(index):
    players = load_data()

    for player in players['players']:
        if int(player['index']) == index:
            player['name'] = request.json['name']
            player['starVotes'].append(int(request.json['stars']))  # Push new star vote
            player['votes'] += 1  # Increment vote count

            # Calculate average stars
            total_stars = sum(player['starVotes'])
            total_votes = player['votes']
            if total_votes > 0:
                average_stars = total_stars / total_votes
                player['stars'] = math.ceil(average_stars)

            save_data(players)

            return jsonify(player)

    return jsonify({'error': 'Player not found.'}), 404


@application.route('/players/<int:index>', methods=['DELETE'])
def remove_player(index):
    players = load_data()

    player = None
    for f in players['players']:
        if int(f['index']) == index:
            player = f
            break

    if not player:
        return jsonify({'error': 'Payer not found.'}), 404
    players['players'].remove(player)
    save_data(players)

    return jsonify({'success': True, 'message': f'Removed player: {player["name"]}'})

@application.route('/draw', methods=['POST'])
def draw_teams():
    players_data = load_data()  # Load players data
    players = players_data['players']
    indexes = request.json['indexes']

    # Group players by star rating
    star_ratings = {'high': [], 'medium': [], 'low': []}
    for player in players:
        if str(player['index']) not in indexes:
            continue

        stars = player['stars']
        if stars >= 4:
            star_ratings['high'].append(player)
        elif stars <= 2:
            star_ratings['medium'].append(player)
        else:
            star_ratings['low'].append(player)

    # Initialize teams and the total number of players drawn
    team1 = []
    team2 = []
    team3 = []
    total_players_drawn = 0

    for players_list in star_ratings.values():
        random.shuffle(players_list)

    # Function to select a player from each star rating group
    def select_player():
        for stars in sorted(star_ratings.keys(), reverse=True):
            if star_ratings[stars]:
                player_selected = star_ratings[stars].pop()
                # Shuffle players within each star rating group
                for players_list in star_ratings.values():
                    random.shuffle(players_list)
                return player_selected

    # Distribute players among teams, alternating between top and bottom players
    while total_players_drawn < len(indexes):
        team1.append(select_player())
        team2.append(select_player())
        team3.append(select_player())
        total_players_drawn += 3

    # Return the selected teams
    return jsonify({'team1': team1, 'team2': team2, 'team3': team3})



if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)


