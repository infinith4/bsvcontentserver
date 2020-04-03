# -*- coding: utf-8 -*-

import pprint
import binascii
import mnemonic
import bip32utils
BIP32_HARDEN    = 0x80000000 # choose from hardened set of child keys
#http://pydoc.net/bip32utils/0.3.post3/bip32utils.BIP32Key/

def bip39(mnemonic_words):
    mobj = mnemonic.Mnemonic("english")
    seed = mobj.to_seed(mnemonic_words)
    #print("seed:" + seed)
    m = bip32utils.BIP32Key.fromEntropy(seed, testnet=True)
    print("* [Chain m]")
    m.dump()

    print("* [Chain m/0h]")
    m = m.ChildKey(0+BIP32_HARDEN)
    m.dump()

    print("* [Chain m/0h/1]")
    m = m.ChildKey(1)
    m.dump()
    
    print("* [Chain m/0h/1/2h]")
    m = m.ChildKey(2+BIP32_HARDEN)
    m.dump()

    print("* [Chain m/0h/1/2h/2]")
    m = m.ChildKey(2)
    m.dump()

    print("* [Chain m/0h/1/2h/2/1000000000]")
    m = m.ChildKey(1000000000)
    m.dump()


    return {
        'mnemonic_words': mnemonic_words,
        # 'bip32_root_key': bip32_root_key_obj.ExtendedKey(),
        # 'bip32_extended_private_key': bip32_child_key_obj.ExtendedKey(),
        # 'path': "m/44'/0'/0'/0",
        'addr': m.Address(),
        'publickey': binascii.hexlify(m.PublicKey()).decode(),
        'privatekey': m.WalletImportFormat(),
        'coin': 'BTC'
    }

import yaml

if __name__ == '__main__':
    #mnemonic_words = "aware report movie exile buyer drum poverty supreme gym oppose float elegant"

    with open('./flaskapp/bip32test/config.yaml', 'r') as yml:
        config = yaml.load(yml)
        
    mnemonic_words = config["testnet"]["mnemonic"]
    pprint.pprint(bip39(mnemonic_words))