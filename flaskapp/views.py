from flaskapp import app
from flask import request, redirect, url_for, render_template, flash, make_response
import requests
import json
import binascii

@app.route('/')
def index():
    html = render_template('index.html', a = 'aaaa', title="HelloTitle")
    return html


@app.route("/download", methods=["GET", "POST"])
def download():
    if request.method == "GET":
        html = render_template('download.html', title="download")
        return html
    elif request.method == "POST":
        txid = request.form["transaction"]
        url = "https://api.whatsonchain.com/v1/bsv/test/tx/hash/" + txid
        headers = {"content-type": "application/json"}
        r = requests.get(url, headers=headers)
        data = r.json()
        print(json.dumps(data, indent=4))
        op_return = data['vout'][0]['scriptPubKey']['opReturn']
        print(json.dumps(op_return, indent=4))  ## bcat.bico.media
        print(op_return['parts'][0])
        upload_data = data['vout'][0]['scriptPubKey']['asm'].split()[3] ##uploaddata (charactor)
        upload_mimetype = op_return['parts'][1] ##MEDIA_Type:  image/png, image/jpeg, text/plain, text/html, text/css, text/javascript, application/pdf, audio/mp3
        upload_charset = op_return['parts'][2] ##ENCODING: binary, utf-8 (Definition polyglot/upload.py)
        upload_filename = op_return['parts'][3] ##filename
        print("upload_mimetype: " + upload_mimetype)
        print("upload_charset: " + upload_charset)
        print("upload_filename: " + upload_filename)
        
        #download_path = './application/download'
        # if not os.path.isdir(download_path):
        #     os.mkdir(download_path)
        # path_w = os.path.join(download_path, txid)
        # with open(path_w, mode='wb') as f:
        #     f.write(binascii.unhexlify(binary))
        response = make_response()
        if upload_charset == 'binary':  #c09f039ca4a919aec0d33fbf3931c35989240892b3f29da11fc66ed65695f967
            #print(binascii.hexlify(upload_data))
            response.data = binascii.unhexlify(upload_data)
        elif upload_charset == 'utf-8':  #cc80675a9a64db116c004b79d22756d824b16d485990a7dfdf46d4a183b752b2
            response.data = op_return['parts'][0]
        else:
            response.data = ''
        downloadFilename = upload_filename
        response.headers["Content-Disposition"] = 'attachment; filename=' + downloadFilename
        response.mimetype = upload_mimetype
        return response