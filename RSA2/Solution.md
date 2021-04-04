## Solution
We are given two files along with the challenge.  
This is what code.py looks like  
```python
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
```
public.txt contains our data for RSA decryption  
```
n = 6785566917491685284241443735115074758771958209534131717149280428547380601238612447568933874152062912753901525459575380055778243283099595163311000031192351
e = 65537
key_sign = 2199661886630193100887057902508171560525565555260697780442813364916039973300340234386554973221809172425505607380092435658248554111577169696678641650547846
ciphertext = 164587995846552196756222528960347216486156857750585447823186963
```

The *make_key()* function just generates RSA key.


Looking at **sign()**, it gives the RSA signature of the input string.\

RSA signature is different from RSA encoding, it follows
> s = x<sup>d</sup> mod n\
> x = s<sup>e</sup> mod n

We see that 
> key_sign = pow(temp,d,n)\
> temp = pow(key_sign,e,n)


Since *temp* is an md5 hash\
We decrypt it and get our **xor_string** 
> encryption

We also see that
> ciphertext = flag ^ xor_string


Therefore
> flag = ciphertext ^ xor_string

This gives us our flag: **flag{w0w_y0u_cr4ck3d_th1s}**
