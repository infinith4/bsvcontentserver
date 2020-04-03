from mnemonic import Mnemonic

mn = Mnemonic("english")
entropy = mn.to_entropy("")

print(entropy)

from bitsv.format import bytes_to_wif
print(bytes_to_wif(entropy))

