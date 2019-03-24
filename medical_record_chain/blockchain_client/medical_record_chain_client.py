'''
title           : medical_record_chain.py
description     : A blockchain client implemenation to support secure management of medical records with an
                  intense focus on patient ownership and control of those records. Features include:
                  - Wallets generation using Public/Private key encryption (based on RSA algorithm)
                  - Recording o medical record previously stored on IPFS by the client applicaiton   
                  - Retrteving the medical record by the patient or authorized proxy or medical provider
                  - management of rights to the medical record by patient or authorized proxies
                  - management of right to treat the patient by the patient or authorized proxies
                  - management of relationship between a provider it's authorized patient care actors (employee)

                  Heavily based on example work done by Adil Moujanid
author          : Tom Scheiber
date_created    : 20190303
date_modified   : 20190303
version         : 0.1
usage           : python3 medical_record_chain_cleint.py
                  python3 medical_record_chain_client.py -p 8080
                  python3 medical_record_chain_client.py --port 8080
python_version  : 3.7.2
Comments        : Wallet generation and transaction signature is based on [1]
References      : [1] https://github.com/julienr/ipynb_playground/blob/master/bitcoin/dumbcoin/dumbcoin.ipynb
'''

from collections import OrderedDict

from binascii import hexlify
from binascii import unhexlify
import hashlib

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto import Random
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA3_256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

import requests
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

def encrypt_document_path_step(document_path, hex_key):
    """
    encrypt the key-ipfs combo. May already be encrypted once
    https://pycryptodome.readthedocs.io/en/latest/src/examples.html
    """

    key = RSA.import_key(unhexlify(hex_key))
 
    # Encrypt the session key with the public RSA key
    session_key = get_random_bytes(16)
    cipher_rsa = PKCS1_OAEP.new(key)
    enc_session_key = cipher_rsa.encrypt(session_key)

    # Encrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(document_path)
    return enc_session_key+cipher_aes.nonce+tag+ciphertext

def encrypt_document_path(document_ipfs_address,
                            document_key,
                            patient_public_key,
                            provider_private_key):
    """
    encrypt reference to encyrpted medical record
    """
    key_doc = document_key+document_ipfs_address
    key_doc_enc_1 = encrypt_document_path_step(key_doc.encode('utf-8'), provider_private_key)
    key_doc_enc_2 = encrypt_document_path_step(str(key_doc_enc_1).encode('utf-8'), patient_public_key)

    return str(key_doc_enc_2).encode('utf-8')



class MedicalRecord:

    def __init__(self,
                 patient_address,
                 patient_public_key,
                 provider_address,
                 provider_private_key,
                 document_key,
                 document_ipfs_address):
        self.patient_address = patient_address
        self.patient_public_key = patient_public_key
        self.provider_address = provider_address
        self.provider_private_key = provider_private_key
        self.document_key = document_key
        self.document_ipfs_address = document_ipfs_address

        self.document_reference = encrypt_document_path(document_ipfs_address,
                                                        document_key,
                                                        patient_public_key,
                                                        provider_private_key)

    def __getattr__(self, attr):
        return self.data[attr]

    def to_dict(self):
        return OrderedDict({'transaction_type':'medical_record',
                            'patient_address': self.patient_address,
                            'provider_address': self.provider_address,
                            'document_reference': self.document_reference})

    def sign_medical_record_creation(self):
        """
        Sign transaction with private key
        """
        private_key = RSA.importKey(unhexlify(self.provider_private_key))
        signer = PKCS1_v1_5.new(private_key)
        h = SHA3_256.new(str(self.to_dict()).encode('utf8'))
        return hexlify(signer.sign(h)).decode('ascii')

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
	return render_template('./index.html')

@app.route('/make/medical/record')
def make_medical_record():
    return render_template('./make_medical_record.html')

@app.route('/view/medical/record')
def view_medical_record():
    return render_template('./view_medical_record.html')

@app.route('/wallet/new', methods=['GET'])
def new_wallet():
    random_gen = Random.new().read
    private_key = RSA.generate(1024, random_gen)
    public_key = private_key.publickey()
    wallet_address = hashlib.sha256(str(public_key).encode('utf8'))
    response = {
        'private_key': hexlify(private_key.exportKey(format='DER')).decode('ascii'),
        'public_key': hexlify(public_key.exportKey(format='DER')).decode('ascii'),
        'wallet_address': wallet_address.hexdigest()
    }

    return jsonify(response), 200

@app.route('/generate/medical/record', methods=['POST'])
def generate_medical_record():
    print('enter generate medical records')
    patient_address = request.form['patient_address']
    patient_public_key = request.form['patient_public_key']
    provider_address = request.form['provider_address']
    provider_private_key = request.form['provider_private_key']
    document_key = request.form['document_key']
    document_ipfs_address = request.form['document_ipfs_address']

    medical_record = MedicalRecord(patient_address,
                                   patient_public_key,
                                   provider_address,
                                   provider_private_key,
                                   document_key,
                                   document_ipfs_address
                                 )

    print(medical_record.to_dict())
    response = {'medical_record': medical_record.to_dict(), 'signature': medical_record.sign_medical_record_creation()}
    
    return jsonify(response), 200


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=8080, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)