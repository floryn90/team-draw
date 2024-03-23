### How to start the app locally

#### Issues with password on ssh
```commandline
sudo nano /etc/ssh/sshd_config
PasswordAuthentication from 'no' to 'yes'
sudo systemctl restart sshd
```
```commandline
python3 -m venv venv
# Windows: 
venv\Scripts\activate.bat
# macOS/Linux: 
source venv/bin/activate
pip install -r requirements.txt
```

#### Linux
```commandline
export FLASK_APP=app.py
```
#### Windows
```commandline
set FLASK_APP=app.py
set FLASK_ENV=development
# development does auto hot swap
```
Then run
```commandline
flask run
# to exit venv un 
deactivate 
```
Follow: 
http://127.0.0.1:5000/b799dd88-e819-44df-8bcb-e577a2735096

#### How to run on centos
```commandline
run.sh

# if above not already setup do the following 

sudo nano /etc/systemd/system/myflaskapp.service
[Unit]
Description=Gunicorn instance to serve myproject
After=network.target

[Service]
User=aurelianap
Group=aurelianap
WorkingDirectory=/home/aurelianap/workspace/tv-series-notification
Environment="PATH=/home/aurelianap/workspace/tv-series-notification/myprojectenv/bin"
ExecStart=/home/aurelianap/workspace/tv-series-notification/myprojectenv/bin/gunicorn --workers 3 --bind 0.0.0.0:9090 -m 007 wsgi

[Install]
WantedBy=multi-user.target

sudo systemctl daemon-reload
sudo systemctl start myflaskapp
sudo systemctl status myflaskapp

# If you want the Flask app to start automatically at boot, enable the service:
sudo systemctl enable myflaskapp

sudo yum install -y glibc-common
nohup python check_release_dates.py > scheduler.log 2>&1 &
```
```commandline
How to setup flask on the server
https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-centos-7

virtualenv myprojectenv
source myprojectenv/bin/activate
pip install gunicorn flask

1. Create the WSGI Entry Point
nano ~/myproject/wsgi.py
from myproject import app

if __name__ == "__main__":
    app.run()
2. cd ~/myproject
#test
gunicorn --bind 0.0.0.0:9091 wsgi
deactivate
3. copy /etc/systemd/system/flaskencryptor.service
4. sudo systemctl start myproject
sudo systemctl enable myproject
5. full logs
sudo journalctl -u flaskencryptor.service
```

```commandline
cp football-draw.service /etc/systemd/system/football-draw.service
sudo systemctl enable football-draw
virtualenv myprojectenv
source myprojectenv/bin/activate
pip install gunicorn flask
gunicorn --bind 0.0.0.0:9091 wsgi
deactivate
sudo chmod 0755 run.sh
./run.sh
```