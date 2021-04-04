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
