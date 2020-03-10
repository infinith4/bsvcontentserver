

deactivate
python3 -m venv herokuenv
source herokuenv/bin/activate

pip3 freeze

pip3 install flask
pip3 install gunicorn
pip3 install requests

pip3 freeze > requirements.txt

pip3 install -r requirements.txt


echo python-3.7.6 > runtime.txt
echo web: gunicorn run:app > Procfile  #run is python filename
wget -qO- https://cli-assets.heroku.com/install-ubuntu.sh | sh
heroku login
heroku --version
#heroku/7.39.0 linux-x64 node-v12.13.0

heroku create bsvstorserver
# https://dashboard.heroku.com/apps

#git init
heroku git:remote -a bsvstorserver
git add .
git commit -am "deploy heroku"

git push heroku master

https://bsvcontentserver.herokuapp.com/