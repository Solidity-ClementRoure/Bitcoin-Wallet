import binascii
import secrets
import hashlib
import unicodedata
import base58check
print()

# entropy
print("Random Entropy in 128 bits: ")
#entropy_hex = secrets.token_hex(16)
entropy_hex = "0c1e24e5917779d297e14d45f14e1a1a"

print(entropy_hex, end="\n")
print()

# generate hash with sha256
print("sha256: ")
sha256 = hashlib.sha256(bytes.fromhex(entropy_hex)).hexdigest()

print(sha256)
print()

# generate seed by adding checksum
print("seed (entropy + checksum): ")
seed_hex = entropy_hex + sha256[0]

print(seed_hex)
print()

# convert seed from hex to binary
seed = bin(int(seed_hex, 16))[2:].zfill(8)
if(len(seed) < 132):
    d = 132 - len(seed)
    for i in range(d):
       seed = "0"+seed

print("132 bits seed: ")
i = 0
for bit in seed:
    if i < 10:
       print(bit, end = '')
       i+=1
    else:
       i=0
       print(bit + " ", end = '')
print()

with open("assets/words.txt", "r") as f:
         wordlist = [w.strip() for w in f.readlines()]

print()
words= []
for i in range(len(seed)//11):
    indx = int(seed[11*i:11*(i+1)],2)
    words.append(wordlist[indx])

print("12 mnemonic words:") 
phrase = " ".join(words)
print(phrase,end="\n\n")

############ PART 2 ###########

# 1) Passer des 12 mots en une valeur hexa (optionnel)

words_bin = ""

for word in words:
    with open("assets/words.txt") as myFile:
        for num, line in enumerate(myFile, 0):
            if word.strip() == line.strip():
                b = bin(num)[2:].zfill(11)
                words_bin+=b 
                print(b, end=" ")
print()

print()
words_hex = hex(int(words_bin, 2))[2:] # seed from mnemonic
print(words_hex)
print()

# 2) 

normalized_mnemonic = unicodedata.normalize("NFKD", phrase)
password = "" # optional
normalized_passphrase = unicodedata.normalize("NFKD", password)
passphrase = "mnemonic" + normalized_passphrase
mnemonic = normalized_mnemonic.encode("utf-8")
passphrase = passphrase.encode("utf-8")

# root seed in hexa
bin_seed = hashlib.pbkdf2_hmac("sha512", mnemonic, passphrase, 2048).hex()
print("512-bits Seed:")
print(bin_seed)
print()

# root seed in binary

# bin_seed = bin(int(bin_seed, 16))[2:].zfill(8)
# if(len(bin_seed) < 512):
#     d = 512 - len(bin_seed)
#     for i in range(d):
#        bin_seed = "0"+bin_seed

# 3)

# HMAC-SHA512
bin_seed = hashlib.pbkdf2_hmac("sha512", bin_seed.encode("utf-8"), "Bitcoin seed".encode("utf-8"), 1).hex() #hashlib.sha512(bin_seed).hexdigest()
bin_seed = bin(int(bin_seed, 16))[2:].zfill(8)
if(len(bin_seed) < 512):
    d = 512 - len(bin_seed)
    for i in range(d):
       bin_seed = "0"+bin_seed

print("HMAC-SHA512 hash:")
print(bin_seed)
print()

# right / left parts
masterPrivateKey_bin = bin_seed[:256]
masterChainKey_bin = bin_seed[256:]

masterPrivateKey=hex(int(masterPrivateKey_bin, 2))[2:]
masterChainKey=hex(int(masterChainKey_bin, 2))[2:]
if len(masterPrivateKey) % 2 != 0:
    masterPrivateKey= "0"+masterPrivateKey
if len(masterChainKey) % 2 != 0:
    masterChainKey= "0"+masterChainKey

# base 58 encoding
masterPrivateKey_b58=base58check.b58encode(bytes.fromhex(masterPrivateKey)).decode('utf-8')
masterChainKey_b58=base58check.b58encode(bytes.fromhex(masterChainKey)).decode('utf-8')

print("Master Private Key:")
print(masterPrivateKey_b58)
print()
print("Master Chain Key:")
print(masterChainKey_b58)
print()


