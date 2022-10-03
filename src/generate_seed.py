import secrets
import hashlib
import unicodedata
import base58check
import hmac
import codecs
import ecdsa
print()

# entropy
print("Random Entropy in 128 bits: ")
entropy_hex = secrets.token_hex(16)
#entropy_hex = "0c1e24e5917779d297e14d45f14e1a1a"

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

# 1) Passer des 12 mots en une valeur hexa

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
if len(words_hex) % 2 == 0:
    words_hex="0"+words_hex
print(words_hex)
print()

# 2) 

normalized_mnemonic = unicodedata.normalize("NFKD", phrase)
password = "" # optional
normalized_passphrase = unicodedata.normalize("NFKD", password)
passphrase = "mnemonic" + normalized_passphrase
mnemonic = normalized_mnemonic.encode("utf-8")
passphrase = passphrase.encode("utf-8")

# root seed
bin_seed = hashlib.pbkdf2_hmac("sha512", mnemonic, passphrase, 2048)
print("512-bits Seed:")
print(bin_seed.hex())
print()

# HMAC-SHA512
I = hmac.new(b"Bitcoin seed", bin_seed, hashlib.sha512).digest()
Il,Ir = I[:32], I[32:]

# base 58 encoding
masterPrivateKey_b58=base58check.b58encode(Il).decode('utf-8')
masterChainKey_b58=base58check.b58encode(Ir).decode('utf-8')

print("Master Private Key:")
print(codecs.encode(Il, 'hex').decode('utf-8'))
#print(masterPrivateKey_b58)
print()
print("Master Chain Key:")
print(codecs.encode(Ir, 'hex').decode('utf-8'))
#print(masterChainKey_b58)
print()

# Generating a public key in bytes using SECP256k1 & ecdsa library
public_key_raw = ecdsa.SigningKey.from_string(Il, curve=ecdsa.SECP256k1).verifying_key
public_key_bytes = public_key_raw.to_string()
# Hex encoding the public key from bytes
public_key_hex = codecs.encode(public_key_bytes, 'hex')
# Bitcoin public key begins with bytes 0x04 so we have to add the bytes at the start
public_key = (b'04' + public_key_hex).decode("utf-8")

# Checking if the last byte is odd or even
if (ord(bytearray.fromhex(public_key[-2:])) % 2 == 0):
    public_key_compressed = '02'
else:
    public_key_compressed = '03'
    
# Add bytes 0x02 to the X of the key if even or 0x03 if odd
public_key_compressed += public_key[2:66]
print("Public Key (hex):")
print(public_key_compressed)
print()

print("Public Key (base 58):")
public_key_compressed = base58check.b58encode(bytes.fromhex(public_key_compressed)).decode('utf-8')
print(public_key_compressed)

print()


