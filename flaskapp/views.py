from flaskapp import app
from flask import request, redirect, url_for, render_template, flash, make_response
import requests
import json
import binascii
# import logging
# logging.basicConfig(filename='example.log',level=logging.DEBUG)
# logger = logging.getLogger(__name__)

@app.route('/')
def index():
    #logger.error("warn test")
    app.logger.info('%s failed to log in')
    html = render_template('index.html', title="Home")
    return html

@app.route('/newlayout')
def newlayout():
    html = render_template('newlayout.html', title="HelloaaTitle")
    return html

@app.route('/download', defaults={'qtxid': ""}, methods=["GET", "POST"])
@app.route("/download/<string:qtxid>", methods=["GET", "POST"])
def download(qtxid=''):
    try:
        print(request.method)
        if request.method == "GET":
            html = render_template('download.html', title="download", transaction=qtxid)
            return html
        elif request.method == "POST":
            txid = request.form["transaction"]
            url = "https://api.whatsonchain.com/v1/bsv/test/tx/hash/" + txid
            headers = {"content-type": "application/json"}
            r = requests.get(url, headers=headers)
            data = r.json()
            op_return = data['vout'][0]['scriptPubKey']['opReturn']
            upload_data = data['vout'][0]['scriptPubKey']['asm'].split()[3] ##uploaddata (charactor)
            upload_mimetype = op_return['parts'][1] ##MEDIA_Type:  image/png, image/jpeg, text/plain, text/html, text/css, text/javascript, application/pdf, audio/mp3
            upload_charset = op_return['parts'][2] ##ENCODING: binary, utf-8 (Definition polyglot/upload.py)
            upload_filename = op_return['parts'][3] ##filename
            print("upload_mimetype: " + upload_mimetype)
            print("upload_charset: " + upload_charset)
            print("upload_filename: " + upload_filename)
            response = make_response()
            if upload_charset == 'binary':  #47f0706cdef805761a975d4af2a418c45580d21d4d653e8410537a3de1b1aa4b
                #print(binascii.hexlify(upload_data))
                response.data = binascii.unhexlify(upload_data)
            elif upload_charset == 'utf-8':  #cc80675a9a64db116c004b79d22756d824b16d485990a7dfdf46d4a183b752b2
                response.data = op_return['parts'][0]
            else:
                print('upload_charset' + upload_charset)
                response.data = ''
            downloadFilename = upload_filename
            response.headers["Content-Disposition"] = 'attachment; filename=' + downloadFilename
            response.mimetype = upload_mimetype
            return response
    except Exception as e:
        print(e)