import secrets
import hashlib
import binascii
print()

# entropy
print("Random Entropy in 128 bits: ")
entropy_hex = secrets.token_hex(16)
entropy_bin = bin(int(entropy_hex, 16))[2:].zfill(8)
if(len(entropy_bin) < 128):
    d = 128 - len(entropy_bin)
    for i in range(d):
       entropy_bin = "0"+entropy_bin

print(entropy_bin)
print()

# get checksum (first 4 bits of entropy -> sha256)
print("sha256: ")
entropy_string = binascii.a2b_hex(entropy_bin)
sha256 = hashlib.sha256(entropy_string).hexdigest()
sha256_bin = bin(int(sha256, 16))[2:].zfill(8)
if(len(sha256_bin) < 256):
    d = 256 - len(sha256_bin)
    for i in range(d):
       sha256_bin = "0"+sha256_bin
print(sha256_bin)
print()

print("seed (entropy + checksum): ")
seed = entropy_bin + sha256_bin[0:4]
print(seed)

print()
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
print(words, end="\n\n") 
