# -*- coding: utf-8 -*-

import pprint
import binascii
import mnemonic
import bip32utils

def bip39(mnemonic_words):
    mobj = mnemonic.Mnemonic("english")
    seed = mobj.to_seed(mnemonic_words)
    #print("seed:" + seed)
    bip32_root_key_obj = bip32utils.BIP32Key.fromEntropy(seed, testnet=True)
    #print("bip32_root_key_obj:" + bip32_root_key_obj)
    bip32_child_key_obj = bip32_root_key_obj.ChildKey(
        44 + bip32utils.BIP32_HARDEN
    ).ChildKey(
        0 + bip32utils.BIP32_HARDEN
    ).ChildKey(
        0 + bip32utils.BIP32_HARDEN
    ).ChildKey(0).ChildKey(0)

    # return {
    #     'mnemonic_words': mnemonic_words,
    #     'bip32_root_key': bip32_root_key_obj.ExtendedKey(),
    #     'bip32_extended_private_key': bip32_child_key_obj.ExtendedKey(),
    #     'bip32_derivation_path': "m/44'/0'/0'/0",
    #     'bip32_derivation_addr': bip32_child_key_obj.Address(),
    #     'coin': 'BTC'
    # }

    return {
        'mnemonic_words': mnemonic_words,
        # 'bip32_root_key': bip32_root_key_obj.ExtendedKey(),
        # 'bip32_extended_private_key': bip32_child_key_obj.ExtendedKey(),
        # 'path': "m/44'/0'/0'/0",
        'addr': bip32_child_key_obj.Address(),
        'publickey': binascii.hexlify(bip32_child_key_obj.PublicKey()).decode(),
        'privatekey': bip32_child_key_obj.WalletImportFormat(),
        'coin': 'BTC'
    }


if __name__ == '__main__':
    #mnemonic_words = "aware report movie exile buyer drum poverty supreme gym oppose float elegant"
    mnemonic_words = ""
    pprint.pprint(bip39(mnemonic_words))