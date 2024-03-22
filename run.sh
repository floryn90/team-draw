if [ "$1" = "monitor-restart" ]; then
  nohup python3 check_release_date.py 2>&1 &
fi

cp favorites.json favorites_backup.json
sudo systemctl restart myproject
sudo systemctl status myproject