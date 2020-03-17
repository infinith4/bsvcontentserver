# https://github.com/trezor/python-mnemonic

import mnemonic ##pip3 install mnemonic
from bsvbip32 import Bip32
import hashlib
import hmac
import sys

class Bip39Mnemonic(object):
    def __init__(self, bsvmnemonic, passphrase="", network = 'main'):
        seed = mnemonic.Mnemonic.to_seed(bsvmnemonic, passphrase)
        #self.masterkey = mnemonic.Mnemonic.to_hd_master_key(seed)
        self.masterkey = self.to_hd_master_key(seed, network)
        print(self.masterkey)
        tprv = Bip32(self.masterkey)
        self.privatekey_wif = tprv.wif()  ## it is privatekey wif format.


    @classmethod
    def to_hd_master_key(self, seed, network):
        if len(seed) != 64:
            raise ValueError("Provided seed should have length of 64")

        # Compute HMAC-SHA512 of seed
        seed = hmac.new(b"Bitcoin seed", seed, digestmod=hashlib.sha512).digest()

        # Serialization format can be found at: https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki#Serialization_format
        if network == 'main':
            xprv = b"\x04\x88\xad\xe4"  # Version for private mainnet
        elif network == 'test':
            xprv = b"\x04\x35\x83\x94"  # Version for private testnet
        xprv += b"\x00" * 9  # Depth, parent fingerprint, and child number
        xprv += seed[32:]  # Chain code
        xprv += b"\x00" + seed[:32]  # Master key

        # Double hash using SHA256
        hashed_xprv = hashlib.sha256(xprv).digest()
        hashed_xprv = hashlib.sha256(hashed_xprv).digest()

        # Append 4 bytes of checksum
        xprv += hashed_xprv[:4]

    @classmethod
    def b58encode(self, v):
        alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

        p, acc = 1, 0
        for c in reversed(v):
            if sys.version < "3":
                c = ord(c)
            acc += p * c
            p = p << 8

        string = ""
        while acc:
            acc, idx = divmod(acc, 58)
            string = alphabet[idx : idx + 1] + string
        return string
