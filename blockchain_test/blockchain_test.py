# from bitcoin import *
# tom_private_key = random_key()
# print("Private Key: %s\n"%tom_private_key)

# tom_public_key = privtopub(tom_private_key)
# print("Public Key: %s\n"%tom_public_key)

# tom_bitcoin_address = pubtoaddr(tom_public_key)
# print("Wallet Address: %s\n"%tom_bitcoin_address)
    
# dan_private_key1 = random_key()
# dan_private_key2 = random_key()
# dan_private_key3 = random_key()

# dan_public_key1 = privtopub(dan_private_key1)
# dan_public_key2 = privtopub(dan_private_key2)
# dan_public_key3 = privtopub(dan_private_key3)

# dan_multi_sig = mk_multisig_script(dan_private_key1, dan_private_key2, dan_private_key3, 1, 3)
# dan_multi_address = scriptaddr(dan_multi_sig)
                              
# print('Multisignature Address: %s\n'%dan_multi_address)

""" from collections import OrderedDict
import binascii

import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

private_key = RSA.importKey(
    binascii.unhexlify(
        '3082025d02010002818100bed3063a3fd50d171d48f10e6c31d16872fd11d6db333f6fcff93326cacf42e04623c5fcd07fe3ab41631d5e5ce0677a1ad537ad85a0175adcef1fa606032fefac0627bd61a772746885aec870ede8d29f313845b6edd52b3a2a7e1be1dda4b9f4a00be751683d03790a5a0c501e206df13c0b2e39c11a1c5cf05b0e759352c70203010001028180576c252fbd7bb5561018113bcacc9e03ec9e4d3472530dae8388c6eaf0423900b7917f0c9e56e0ee5df3f309fea1de363e21cdb2c503bd7f66b57479e2ca46048bc54c5d53d8278be951663ac65ece642b3c8594f02c1430dabcfbae54451fcb00e35506169fe679128d5f8d94147e3a6c382ea89fbd375488467dcc6191c40d024100cb8340e716e98eb2080908ad8575258e785186a770a31fd46a4c0d8de92aaebce162aa89850409d1c20a706d08a160c566398f713a018e870f14c439f7dc818d024100f00a07ddfe66ab8c72e258c2ceb5137957af86908fdfcf66890422ac0b5e3208d195778e94ad0a3890c8f132c23c905446ff8af48a68e0dca2852937535baea30240080fb6ee7075e7f51d645e37a165b68b2230f8888169b4c51140d9f89917dbbc17a174e7e5a0f7529bc1161afb9088e8c8d7d6dac1557673db211374c860afb1024100dd2e20f9a94529a58ce68c2b5514fd10be7f7a5b1277844052d880aa4eff48d35f6b7e72df04637aa3cec491a4f0f17cf6bed96763722860a550561e28ad3e49024100bafded188f592d0e959c644889fd0804fa5251396cf4f02e5c3167e09a41e414ddd2039c45293a1ff7c55d6820e2df6fe128a5b85b597a83a3610dac94bfb289'
        )
)
signer = PKCS1_v1_5.new(private_key)
h = SHA.new(str(OrderedDict({'transaction_type':'medical_record'})).encode('utf8'))
sig =  binascii.hexlify(signer.sign(h)).decode('ascii')
#print(provider_private_key)
print('private key: {} {}'.format(type(private_key), private_key))
print('h: {} {}'.format(type(h), h))
print('signature: {} {}'.format(type(sig), sig))
 """

from binascii import hexlify
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol import *
from Crypto.Protocol.SecretSharing import Shamir

key = get_random_bytes(16)
print('key from random: {}'.format(key))
shares = Shamir.split(2, 5, key)
source_shares = shares
for idx, share in shares:
    print("Index #{}: {}".format(idx, hexlify(share)))

fi = open("blockchain_test/clear_file.txt", "rb")
fo = open("blockchain_test/enc_file.txt", "wb")

cipher = AES.new(key, AES.MODE_EAX)
nonce = cipher.nonce
print('cipher: {}'.format(cipher))
print('nonce: {}'.format(nonce))
inputdata = fi.read()
print('original file: {}'.format(inputdata))
ct, tag = cipher.encrypt_and_digest(inputdata)
fo.write(nonce + tag + ct)
fo.close()
print('Written to encrypted file: {} {} {}'.format(nonce, tag, ct))
from binascii import unhexlify
from Crypto.Cipher import AES
from Crypto.Protocol.SecretSharing import Shamir

shares = []
""" for x in range(2):
    in_str = input("Enter index and share separated by comma: ")
    idx, share = in_str.split(",")
    print(unhexlify(share))
    shares.append((idx, unhexlify(share)))
 """
shares.append(source_shares[3])
shares.append(source_shares[4])
key = Shamir.combine(shares)
print('key from shares: {}'.format(key))
fi = open("blockchain_test/enc_file.txt", "rb")
# encrypted_data = fi.read(16)
# print(encrypted_data)
nonce, tag = [ fi.read(16) for x in range(2) ]
print('nonce + tag: {} {}'.format(nonce, tag))
cipher = AES.new(key, AES.MODE_EAX, nonce)
try:
    result = cipher.decrypt(fi.read())
    cipher.verify(tag)
    with open("blockchain_test/clear_file2.txt", "wb") as fo:
        fo.write(result)
    print("The shares were correct")
except ValueError:
    print("The shares were incorrect")