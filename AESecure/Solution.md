## Solution

We are given code.py which looks like  
```python
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from Crypto.Random import get_random_bytes

key = get_random_bytes(16)
iv = get_random_bytes(16)

flag = open('flag','rb').read().strip()

def encrypt_data(data):
    cipher = AES.new(key, AES.MODE_CBC,iv)
    enc = cipher.encrypt(pad(data,16,style='pkcs7'))
    return enc.hex()

def decrypt_data(encryptedParams):
    cipher = AES.new(key, AES.MODE_CBC,iv)
    paddedParams = cipher.decrypt(bytearray.fromhex(encryptedParams))
    return unpad(paddedParams,16,style='pkcs7')

msg = "success=0"
print("Current message is : " + msg)
print("Encryption of message in hex : " + iv.hex() + encrypt_data(msg.encode('utf-8')))
enc_msg = input("Give me the encypted message (in hex) to get the flag\n")
try:
    final_dec_msg = decrypt_data(enc_msg)
    if b"success=1" in final_dec_msg:
        print('Whoa!! you got it!! Now its time for a reward!!')
        print(flag)
    else:
        print('keep trying')
        exit()
except:
    print('Try Again!!')
```

And a web interface  
![web](https://i.imgur.com/vr8M2Wm.png)

Having a first look at the code, we see something strange  
We are given *success=0* but the validation check is for *success=1*  
So there must be a way to alter this value.  

First a bit of information on how AES-CBC works  
![img1](https://dr3dd.gitlab.io/favicon/902px-CBC_encryption.svg.jpg)

![img2](https://dr3dd.gitlab.io/favicon/902px-CBC_encryption.svg.jpg)

The main vulnerable part of CBC is that it uses previous block of ciphertext to encrypt next block of plaintext.  
Similarly, in decryption second block of ciphertext after being decrypted by AES, is XORed with previous block of ciphertext.  
On analysing this, we can understand that if we change some bits of the previous block of ciphertext then the next block of plaintext will also be affected.  
Also in CBC encryption and decryption, since for the first block there is no previous block, a randomly generated iv is used.  

Our message is: *success=0*  
CBC block size: 16  
Message after pkcs7 padding: *success=0\t\t\t\t\t\t\t*

Our target is to change the encrypted data so that the message becomes *success=1*  

Let's say for example one of the encrypted messages is **eeb4728809aaf307f2d49f4f757fde0a6c59e1a7df46921a4a148199bb9c9803**
![code1](https://i.imgur.com/kVXwsoq.png)

So, here the first block is the iv: \xee\xb4r\x88\t\xaa\xf3\x07\xf2\xd4\x9fOu\x7f\xde\n  
Second block is the encrypted message: lY\xe1\xa7\xdfF\x92\x1aJ\x14\x81\x99\xbb\x9c\x98\x03  

Index of the byte we have to change in message(*success=0*): 8  
So to change the byte from 0 to 1, we XOR it with 1
> bmsg[8] = bmsg[8] ^ 1

Now we get our new encrypted message **eeb4728809aaf307f3d49f4f757fde0a6c59e1a7df46921a4a148199bb9c9803**

Supplying this in the prompt gives us our flag: **flag{b1t_fl1pp1ng_4tt4ck_esdtjf}**
