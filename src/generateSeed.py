
import secrets
import hashlib

entropy = secrets.token_hex(16)
print("Generated entropy in hexadecimal :")
print(entropy)

entropy_bin=bin(int(entropy,16))[2:]

print(entropy_bin)
while len(entropy_bin)!=128:
    entropy_bin="0"+entropy_bin

print("Generated entropy in binary :")
print(entropy_bin)



hash_hex = hashlib.sha256(entropy_bin.encode()).hexdigest()

print()
hash_bit=bin(int(hash_hex,16))[2:]


hash_bit4=hash_bit[:4]

print(hash_bit)
print(hash_bit4)

seed_bin=entropy_bin+hash_bit4
print(seed_bin)
print(len(seed_bin))

with open("/Users/antoinerevel/PycharmProjects/Bitcoin-Wallet/assets/words.txt", "r") as f:
   wordlist = [w.strip() for w in f.readlines()]


seed=[]
for i in range(12):
    segment=seed_bin[i*11:(i+1)*11]
    #print(segment)
    index=int(segment,2)
    #print(index)
    seed.append(wordlist[index])
print(seed)
