from flaskapp import app, mongo, bootstrap
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
import time

from flaskapp.lib.whats_on_chain_lib import WhatsOnChainLib

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
import multiprocessing

@app.route('/note', defaults={'qaddr': ""}, methods=["GET", "POST"])
@app.route('/note/<string:qaddr>', methods=["GET", "POST"])
def note(qaddr=''):
    try:
        if request.method == "GET":
            ## get bsv text list
            html = render_template('note.html', title="note")
            if qaddr == '':
                return html
            trans_list = []
            transaction_list = mongo.db.transaction.find()
            startindex = 0
            maxtakecount = 5  ##5 items
            if transaction_list.count() > 0:
                for i in range(startindex, maxtakecount):
                    trans_list.append(transaction_list[i]["txid"])
            res_get_textdata = []

            #処理前の時刻
            t1 = time.time()
            if len(trans_list) > 0:
                for i in range(startindex, len(trans_list), maxtakecount):
                    txs = trans_list[i:maxtakecount+i]
                    print(txs)
                    p = multiprocessing.Pool(6) # プロセス数を6に設定
                    result = p.map(WhatsOnChainLib.get_textdata, txs)  ## arg must be array
                    #print(result)
                    for item in result:
                        #print("item")
                        if item is not None and item.mimetype == "text/plain":
                            res_get_textdata.append(item.data)
            else:
                network_api = bitsv.network.NetworkAPI(network='test')
                transactions = network_api.get_transactions(qaddr)
                for i in range(startindex, maxtakecount):
                    txs = transactions[i:maxtakecount+i]
                    print(txs)
                    p = multiprocessing.Pool(6) # プロセス数を6に設定
                    result = p.map(WhatsOnChainLib.get_textdata, txs)  ## arg must be array
                    #print(result)
                    for item in result:
                        #print("item")
                        if item is not None and item.mimetype == "text/plain":
                            #print(item.data)
                            mongo.db.transaction.insert({"txid": item.txid})
                            res_get_textdata.append(item.data)
            print(len(res_get_textdata))

            
            # 処理後の時刻
            t2 = time.time()
            
            # 経過時間を表示
            elapsed_time = t2-t1
            print(f"経過時間：{elapsed_time}")
            # print(res_get_textdata)
            # for item in res_get_textdata:
            #     if item is not None:
            #         print(item)
            # for i in range(0, len(transactions), maxcount):
            #     res_get_textdata = get_transactions_datalist(transactions[i:maxcount+i])
            html = render_template('note.html', title="note", textdata_list=res_get_textdata)
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
                res_get_textdata = WhatsOnChainLib.get_textdata(txid)
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
        json_data = json.dumps({"txids" : ["2a566f32c51227d56ba9bdebe42d9857aeeb50cff074fc553c0d08bc250e0f7c"]})
        print(json_data)

        r = requests.post(url, json_data, headers=headers)
        data = r.json()
        print(json.dumps(data, indent=4))
        for i in range(len(data)):
            op_return = data[i]['vout'][0]['scriptPubKey']['opReturn']
            upload_data = data[i]['vout'][0]['scriptPubKey']['asm'].split()[3] ##uploaddata (charactor)
            if op_return != None:
                textdata = binascii.unhexlify(upload_data)
                print(textdata)
                # parts = op_return['parts']
                # if parts != None:
                #     upload_mimetype = parts[1] ##MEDIA_Type:  image/png, image/jpeg, text/plain, text/html, text/css, text/javascript, application/pdf, audio/mp3
                #     upload_charset = parts[2] ##ENCODING: binary, utf-8 (Definition polyglot/upload.py)
                #     upload_filename = parts[3] ##filename
                #     print("upload_mimetype: " + upload_mimetype)
                #     print("upload_charset: " + upload_charset)
                #     print("upload_filename: " + upload_filename)
                #     response = make_response()
                #     if upload_charset == 'binary':  #47f0706cdef805761a975d4af2a418c45580d21d4d653e8410537a3de1b1aa4b
                #         #print(binascii.hexlify(upload_data))
                #         response.data = binascii.unhexlify(upload_data)
                #     elif upload_charset == 'utf-8':  #cc80675a9a64db116c004b79d22756d824b16d485990a7dfdf46d4a183b752b2
                #         response.data = op_return['parts'][0]
                #     else:
                #         print('upload_charset' + upload_charset)
                #         response.data = ''
                #     downloadFilename = upload_filename
                #     response.headers["Content-Disposition"] = 'attachment; filename=' + downloadFilename
                #     response.mimetype = upload_mimetype
                #     print(response.data)
        return None
    except Exception as e:
        print(e)

# http://127.0.0.1:5000/api/tx/mnoTQaiqDBjUG6WWAUwhFycirbrKYUMgmU?start_index=3&cnt=5
@app.route('/api/tx', defaults={'addr': ''}, methods=["GET"])
@app.route('/api/tx/<string:addr>', methods=["GET"])
def get_tx(addr = ''):
    try:
        start_index_str = request.args.get('start_index')
        if start_index_str == "":
            start_index = 0
        else: 
            start_index = int(start_index_str)
        cnt_str = request.args.get('cnt')
        if cnt_str == "":
            cnt = 5
        else:
            cnt = int(cnt_str)
        print("addr: %s; start_index:%s;cnt: %s" % (addr, start_index, cnt))
        # search mongodb transaction records from start_index to cnt.
        trans_list = []
        transaction_list = mongo.db.transaction.find()
        if transaction_list.count() > 0:
            for i in range(start_index, start_index + cnt):
                trans_list.append(transaction_list[i]["txid"])

        res_get_textdata = []
        print(trans_list)
        if len(trans_list) > 0:
            txs = trans_list[i:len(trans_list)-1]
            print(txs)
            p = multiprocessing.Pool(6) # プロセス数を6に設定
            result = p.map(WhatsOnChainLib.get_textdata, txs)  ## arg must be array

            for item in result:
                if item is not None and item.mimetype == "text/plain":
                    res_get_textdata.append(item.data)
        return ""
    except Exception as e:
        print(e)
        return ""