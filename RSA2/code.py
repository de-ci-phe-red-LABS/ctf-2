from Crypto.Util.number import*
from Hidden.secret import flag,xor_string
import hashlib

ciphertext = bytes_to_long(flag.encode()) ^ bytes_to_long(xor_string.encode())

def sign(string,d,n):
    temp = hashlib.md5(string.encode()).digest()
    return pow(bytes_to_long(temp),d,n)

def make_key():
    p = getPrime(256)
    q = getPrime(256)
    n = p*q
    e = 65537
    phin = (p-1)*(q-1)
    d = inverse(e,phin)
    assert pow(pow(17,e,n),d,n) == 17
    print("Works! Key generated!")
    string = "n = {}\ne = {}\nd = {}\np = {}\nq = {}\n\n".format(n,e,d,p,q)
    print(string)
    open('./key.txt','w').write(string)
    return n,e,d

n,e,d = make_key()
key_sign = sign(xor_string,d,n)
public = "n = {}\ne = {}\nkey_sign = {}\nciphertext = {}\n".format(n,e,key_sign,ciphertext)
print(public)
open('./public.txt','w').write(public)
