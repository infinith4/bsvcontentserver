from flaskapp import app
from flask import request, redirect, url_for, render_template, flash, make_response
import requests
import json
import binascii
import bitsv
from flaskapp.bip39mnemonic import Bip39Mnemonic
import os
# ファイル名をチェックする関数
from werkzeug.utils import secure_filename
import polyglot  # pip3 install polyglot-bitcoin
import requests
import json
import datetime

# import logging
# logging.basicConfig(filename='example.log',level=logging.DEBUG)
# logger = logging.getLogger(__name__)

@app.route('/')
def index():
    #logger.error("warn test")
    app.logger.debug('debug test')
    app.logger.info('info failed to log in')
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


@app.route('/mnemonic', methods=["GET", "POST"])
def mnemonic():
    if request.method == "GET":
        html = render_template('mnemonic.html', title="mnemonic")
        return html
    elif request.method == "POST":
        mnemonic = request.form["mnemonic"]  #app.config['TESTNET_MNEMONIC']
        bip39Mnemonic = Bip39Mnemonic(mnemonic, passphrase="", network="test")
        privateKey = bitsv.Key(bip39Mnemonic.privatekey_wif, network = 'test')
        address = privateKey.address
        balance_satoshi = privateKey.get_balance()
        balance_bsv = float(balance_satoshi) / float(100000000)
        html = render_template(
            'mnemonic.html',
            privatekey_wif = bip39Mnemonic.privatekey_wif,
            address = address,
            balance_satoshi = balance_satoshi,
            balance_bsv = balance_bsv,
            title="mnemonic")
        return html

@app.route("/upload", methods=["GET"])
def upload_file():
    if request.method == 'GET':
        html = render_template('upload.html', title="upload")
        return html
    # リクエストがポストかどうかの判別
    elif request.method == 'POST':
        bsv_mnemonic = request.form["mnemonic"]  #app.config['TESTNET_MNEMONIC']
        bip39Mnemonic = Bip39Mnemonic(bsv_mnemonic, passphrase="", network="test")
        
        # ファイルがなかった場合の処理
        if 'file' not in request.files:
            print('ファイルがありません')
            flash('ファイルがありません')
            return redirect(request.url)
        # データの取り出し
        req_file = request.files['file']
        print(req_file)
        stream = req_file.stream
        #img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)

        # ファイル名がなかった時の処理
        if req_file.filename == '':
            flash('ファイルがありません')
            return redirect(request.url)
        # ファイルのチェック
        if req_file and allwed_file(req_file.filename):
            # 危険な文字を削除（サニタイズ処理）
            #filename = secure_filename(req_file.filename)
            # ファイルの保存
            #filepath = os.path.join(app.config['UPLOAD_FOLDER'], req_file.filename)
            #req_file.save(filepath)
            uploader = polyglot.Upload(bip39Mnemonic.privatekey_wif, 'test')
            print(uploader.network)
            req_file_bytearray = bytearray(stream.read())
            print(req_file_bytearray)
            #transaction = uploader.bcat_parts_send_from_binary(req_file_bytearray)
            media_type = uploader.get_media_type_for_file_name(req_file.filename)
            encoding = uploader.get_encoding_for_file_name(req_file.filename)
            print(media_type)
            print(encoding)
            rawtx = uploader.b_create_rawtx_from_binary(req_file_bytearray, media_type, encoding, req_file.filename)
            txid = uploader.send_rawtx(rawtx)
            #transaction = uploader.upload_b(filepath)
            #['5cd293a25ecf0b346ede712ceb716f35f1f78e2c5245852eb8319e353780c615']
            print(txid)
            # アップロード後のページに転送
            html = render_template(
                'uploaded.html', 
                transaction = txid, 
                privatekey_wif = bip39Mnemonic.privatekey_wif,
                title="mnemonic")

            return html
        else:
            html = render_template(
                'uploaded.html', 
                transaction = "error", 
                privatekey_wif = bip39Mnemonic.privatekey_wif,
                title="mnemonic")
            return html

# アップロードされる拡張子の制限
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif', 'txt'])

def allwed_file(filename):
    # .があるかどうかのチェックと、拡張子の確認
    # OKなら１、だめなら0
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

from io import StringIO
@app.route('/note', defaults={'qaddr': ""}, methods=["GET", "POST"])
@app.route('/note/<string:qaddr>', methods=["GET", "POST"])
def note(qaddr=''):
    try:
        if request.method == "GET":
            ## get bsv text list
            html = render_template('note.html', title="note")
            if qaddr != '':
                network_api = bitsv.network.NetworkAPI(network='test')
                transactions = network_api.get_transactions(qaddr)
                res_get_textdata = []
                maxcount = 20
                for i in range(0, len(transactions), maxcount):
                    res_get_textdata = get_transactions_datalist(transactions[i:maxcount+i])
                html = render_template('note.html', title="note", textdata_list=[])
            return html
        elif request.method == "POST":
            mnemonic_words = request.form["mnemonic_words"]
            bip39Mnemonic = Bip39Mnemonic(mnemonic_words, passphrase="", network="test")
            privateKey = bitsv.Key(bip39Mnemonic.privatekey_wif, network = 'test')
            transactions = privateKey.get_transactions()
            print("transactions")
            print(transactions)

            textdata_list = []
            for txid in reversed(transactions):
                res_get_textdata = get_textdata(txid)
                if res_get_textdata != None and res_get_textdata.mimetype == 'text/plain':
                    textdata_list.append(res_get_textdata.data.decode('utf-8'))
            print("textdata_list")
            print(textdata_list)


            message = request.form["message"]
            bip39Mnemonic = Bip39Mnemonic(mnemonic_words, passphrase="", network="test")
            #stream = StringIO(message)
            #stream = message.stream

            encoding = "utf-8"
            print("bip39Mnemonic.privatekey_wif")
            print(bip39Mnemonic.privatekey_wif)
            uploader = polyglot.Upload(bip39Mnemonic.privatekey_wif, network='test')
            #req_file_bytearray = bytearray()
            #req_file_bytearray.extend(map(ord, message))
            #req_file_bytearray = bytearray(stream.read())
            #print(req_file_bytearray)
            message_bytes = message.encode(encoding)
            message_bytes_length = len(message_bytes)
            print(message_bytes_length)
            if(message_bytes_length >= 100000):   #more less 100kb = 100000bytes.
                html = render_template('note.html', title="note", error_msg="text data have to be 100kb or less")
                return html

            req_bytearray = bytearray(message_bytes)
            #transaction = uploader.bcat_parts_send_from_binary(req_file_bytearray)
            media_type = "text/plain"
            print(media_type)
            print(encoding)
            file_name = format(datetime.date.today(), '%Y%m%d')
            print(uploader.filter_utxos_for_bcat())
            rawtx = uploader.b_create_rawtx_from_binary(req_bytearray, media_type, encoding, file_name)
            txid = uploader.send_rawtx(rawtx)
            #transaction = uploader.upload_b(filepath)
            #['5cd293a25ecf0b346ede712ceb716f35f1f78e2c5245852eb8319e353780c615']
            print("upload txid")
            print(txid)
            # アップロード後のページに転送
            # html = render_template(
            #     'uploaded.html', 
            #     transaction = txid, 
            #     #privatekey_wif = bip39Mnemonic.privatekey_wif,
            #     title="mnemonic")

            # return html
            if txid == "":
                html = render_template('note.html', title="note", error_msg="upload failed")
                return html

                
            html = render_template('note.html', title="note", uploaded_message=message, textdata_list=textdata_list)
            return html
    except Exception as e:
        print(e)


def get_transactions_datalist(txids):
    try:
        url = "https://api.whatsonchain.com/v1/bsv/test/txs"
        headers = {"content-type": "application/json"}
        json_data = json.dumps({"txids" : txids})
        print(json_data)

        r = requests.post(url, json_data, headers=headers)
        data = r.json()
        print(json.dumps(data, indent=4))
        for i in range(len(data)):
            op_return = data[i]['vout'][0]['scriptPubKey']['opReturn']
            upload_data = data[i]['vout'][0]['scriptPubKey']['asm'].split()[3] ##uploaddata (charactor)
            if op_return != None:
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
                print(response.data)
        return response
    except Exception as e:
        print(e)

def get_textdata(txid):
    try:
        print("txid")
        print(txid)
        if txid != "":
            url = "https://api.whatsonchain.com/v1/bsv/test/tx/hash/" + txid
            headers = {"content-type": "application/json"}
            r = requests.get(url, headers=headers)
            data = r.json()
            print(json.dumps(data, indent=4))
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
            print(response.data)
            return response
    except Exception as e:
        print(e)