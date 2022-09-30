import hashlib
import binascii
import secrets
print()

entropy = secrets.token_hex(32)
print("random generated entropy (in hexa): " + entropy, end="\n\n")

# convert hexa to bytes
data = binascii.unhexlify(entropy)

<<<<<<< HEAD
# generate hash with sha256
print("sha256: ")
sha256 = hashlib.sha256(bytes.fromhex(entropy_hex)).hexdigest()
=======
h = hashlib.sha256(data).hexdigest()
print("entropy after sha-256: " + h, end="\n\n")
>>>>>>> 6f6b2be2dd75fa5956dd998ffc0c597d6ea1a19c

b = bin(int(binascii.hexlify(data),16))[2:].zfill(len(data)*8) + bin(int(h,16))[2:].zfill(256)[: len(data)* 8//32]

print("132 bits: ")
i = 0
for bit in b:
    if i < 11:
       print(bit, end = '')
       i+=1
    else:
       i=0
       print(" ", end = '')
print()

with open("assets/words.txt", "r") as f:
         wordlist = [w.strip() for w in f.readlines()]
print()

seed = []
for i in range(len(b)//11):
    indx = int(b[11*i:11*(i+1)],2)
    seed.append(wordlist[indx])
print("12 mnemonic code:") 
print(seed, end="\n\n") 
