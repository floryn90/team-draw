from flask import Flask, render_template, request, redirect, jsonify
from list import save_data, load_data
import math
import random
import os
from shutil import copyfile
from datetime import datetime

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
            calculate_average_stars(player)

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

@application.route('/reset-voting', methods=['POST'])
def reset_voting():
    players_data = load_data()
    players = players_data['players']

    # Create a backup of the existing players data file
    backup_filename = f"players_{datetime.now().strftime('%d_%m_%Y_%H_%M')}.json"
    backup_path = os.path.join(os.getcwd(), backup_filename)
    copyfile('players.json', backup_path)

    # Reset voting and stars for each player
    for player in players:
        player['votes'] = 0
        player['stars'] = 1
        player['starVotes'] = []

    # Save the updated data
    save_data(players_data)

    return jsonify({'message': 'Voting and stars reset successfully.', 'backup': backup_filename})
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

    balance_teams(team1, team2, team3)

    # Return the selected teams
    return jsonify({'team1': team1, 'team2': team2, 'team3': team3})


def balance_teams(team1, team2, team3):
    # Calculate average stars for each team
    avg_team1 = sum(player['stars'] for player in team1) / len(team1)
    avg_team2 = sum(player['stars'] for player in team2) / len(team2)
    avg_team3 = sum(player['stars'] for player in team3) / len(team3)

    # Find the team with the highest and lowest average stars
    highest_avg_team = max(avg_team1, avg_team2, avg_team3)
    lowest_avg_team = min(avg_team1, avg_team2, avg_team3)

    # Check if the difference in average stars is >= 0.5
    if highest_avg_team - lowest_avg_team >= 0.4:
        # Determine which team has the highest difference and the corresponding lowest team
        if highest_avg_team == avg_team1:
            lowest_team = team3
            highest_team = team1
        elif highest_avg_team == avg_team2:
            lowest_team = team1
            highest_team = team2
        else:
            lowest_team = team1
            highest_team = team3

        # Get the players with the lowest and highest stars in the lowest average team
        lowest_player = min(lowest_team, key=lambda x: x['stars'])
        target_stars = lowest_player['stars'] + 2
        potential_players = [player for player in highest_team if player['stars'] == target_stars]

        # If there are potential players in the highest team, select one randomly
        if potential_players:
            chosen_player = random.choice(potential_players)

        # Swap the lowest player with the highest player
        highest_team.remove(chosen_player)
        lowest_team.remove(lowest_player)
        highest_team.append(lowest_player)
        lowest_team.append(chosen_player)

        print(f'highest player {chosen_player   } switched with {lowest_player}')
        print("Teams have been balanced successfully.")
    else:
        print("The difference in average stars between the top and bottom teams is not >= 0.5.")

def calculate_average_stars(player):
    total_stars = sum(player['starVotes'])
    total_votes = player['votes']
    if total_votes > 0:
        average_stars = total_stars / total_votes
        decimal_part = average_stars - math.floor(average_stars)
        if decimal_part >= 0.5:
            player['stars'] = math.ceil(average_stars)
        else:
            player['stars'] = math.floor(average_stars)

# Calculate average stars for all players when the application starts
def calculate_average_stars_for_all_players():
    players = load_data()
    for player in players['players']:
        calculate_average_stars(player)
    save_data(players)

if __name__ == "__main__":
    # Calculate average stars for all players when the application starts
    calculate_average_stars_for_all_players()

    application.run(host='0.0.0.0', debug=True)


