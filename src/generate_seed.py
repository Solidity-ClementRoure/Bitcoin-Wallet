import secrets
import hashlib
import binascii
print()

# entropy
print("Random Entropy in 128 bits: ")
entropy_hex = secrets.token_hex(16)
#entropy_hex = "656d338db7c217ad57b2516cdddd6d06"

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
for word in words:
    print(word, end=" ") 
print("",end="\n\n")
