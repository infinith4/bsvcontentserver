
import requests
from .Models import ResponseTx
import binascii

class WhatsOnChainLib(object):
    def __init__(self, txid):
        self.txid = txid
    
    @classmethod
    def get_textdata(self, txid):
        try:
            #print("txid")
            #print(txid)
            #time.sleep(0.1)
            if txid != "":
                url = "https://api.whatsonchain.com/v1/bsv/test/tx/hash/" + txid
                headers = {"content-type": "application/json"}
                r = requests.get(url, headers=headers)
                data = r.json()
                op_return = data['vout'][0]['scriptPubKey']['opReturn']
                if op_return is None:
                    return None
                hex_upload_data = data['vout'][0]['scriptPubKey']['asm'].split()[3] ##uploaddata (charactor)
                parts = op_return['parts']
                if parts is None:
                    return None
                upload_mimetype = parts[1] ##MEDIA_Type:  image/png, image/jpeg, text/plain, text/html, text/css, text/javascript, application/pdf, audio/mp3
                upload_charset = parts[2] ##ENCODING: binary, utf-8 (Definition polyglot/upload.py)
                upload_filename = parts[3] ##filename
                # print("upload_mimetype: " + upload_mimetype)
                # print("upload_charset: " + upload_charset)
                # print("upload_filename: " + upload_filename)
                # print("hex_upload_data: " + hex_upload_data)
                # response = make_response()
                if upload_charset == 'binary':  #47f0706cdef805761a975d4af2a418c45580d21d4d653e8410537a3de1b1aa4b
                    #print(binascii.hexlify(upload_data))
                    upload_data = binascii.unhexlify(hex_upload_data)
                elif upload_charset == 'utf-8':  #cc80675a9a64db116c004b79d22756d824b16d485990a7dfdf46d4a183b752b2
                    upload_data = parts[0]
                else:
                    #print('upload_charset' + upload_charset)
                    upload_data = ''
                # downloadFilename = upload_filename
                # response.headers["Content-Disposition"] = 'attachment; filename=' + downloadFilename
                # response.mimetype = upload_mimetype
                #print(upload_data)
                # return response]
                return ResponseTx(txid, upload_data, upload_mimetype, upload_charset, upload_filename)
        except Exception as e:
            # TODO: To Logger
            print(e)
            return None

