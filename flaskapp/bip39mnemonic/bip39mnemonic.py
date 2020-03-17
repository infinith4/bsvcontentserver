# https://github.com/trezor/python-mnemonic

import mnemonic ##pip3 install mnemonic
from bsvbip32 import Bip32

class Bip39Mnemonic(object):
    def __init__(self, bsvmnemonic, passphrase="", network = 'main'):
        seed = mnemonic.Mnemonic.to_seed(bsvmnemonic, passphrase)
        #self.masterkey = mnemonic.Mnemonic.to_hd_master_key(seed)
        self.masterkey = mnemonic.Mnemonic.to_hd_master_key(seed, network)
        print(self.masterkey)
        tprv = Bip32(self.masterkey)
        self.privatekey_wif = tprv.wif()  ## it is privatekey wif format.
