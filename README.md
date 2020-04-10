[![Build Status](https://travis-ci.org/tys-hiroshi/bsvcontentserver.svg?branch=develop)](https://travis-ci.org/tys-hiroshi/bsvcontentserver)

### heroku app

https://bsvstorserver.herokuapp.com


```
sudo apt install python3.7
sudo apt-get install python3-venv
sudo apt-get install pylint

deactivate
python3 -m venv herokuenv
source herokuenv/bin/activate

pip3 freeze

pip3 install flask
pip3 install gunicorn
pip3 install requests
pip3 install flask-bootstrap4
pip3 install pyyaml
pip3 install base58
pip3 install bitsv
pip3 install polyglot-bitcoin
pip3 install numpy
pip3 install flask-pymongo

pip3 freeze | grep -v "pkg-resources" > requirements.txt

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
```

https://bsvstorserver.herokuapp.com/

https://test.whatsonchain.com/
sudo apt-get install pylint/v1/bsv/test/tx/hash/47f0706cdef805761a975d4af2a418c45580d21d4d653e8410537a3de1b1aa4b

txid:

binary
https://api.whatsonchain.com/v1/bsv/test/tx/hash/47f0706cdef805761a975d4af2a418c45580d21d4d653e8410537a3de1b1aa4b

text
cc80675a9a64db116c004b79d22756d824b16d485990a7dfdf46d4a183b752b2

93a91010b9223ba4c64e8d8522a7ed75b68abd38060c4700f8b4a5809ac7ceaf

# heroku

```
heroku logs --tail
```

## bootstrap

```
pip3 install wheel
pip3 install flask-bootstrap4
```


## Config

https://msiz07-flask-docs-ja.readthedocs.io/ja/latest/config.html

```
export FLASK_CONFIG_FILE=[absolute config.py path]

echo $FLASK_CONFIG_FILE
```

## on heroku 

```
$ heroku run bash

pwd
/app
```

環境変数一覧表示

```
$heroku config

$heroku config:set FLASK_CONFIG_FILE=/app/config.py
```

### pip3 install via git

pip3 install git+https://github.com/AustEcon/bsvbip32


private key testnet

\x04\x35\x83\x94


### mongodb

https://cloud.mongodb.com/v2/5e883d9adf26162d6e9c774d#clusters/connect?clusterId=Cluster0


https://cloud.mongodb.com/v2/5e8a9ff9457adb4794eb8c6c


```
mongo "mongodb+srv://cluster0-mmmko.mongodb.net/test"  --username [username]

```


```
from flask_pymongo import PyMongo

```



