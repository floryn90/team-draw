cp players.json players_$(date +%F).json
sudo systemctl restart  football-draw
sudo systemctl status football-draw