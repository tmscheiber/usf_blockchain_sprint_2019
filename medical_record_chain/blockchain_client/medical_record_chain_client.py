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

import binascii

import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

import requests
from flask import Flask, jsonify, request, render_template


class MedicalRecord:

    def __init__(self,
                 patient_address,
                 provider_address,
                 provider_private_key,
                 provider_employee_address,
                 provider_employee_private_key,
                 document_ipfs_address):
        self.patient_address = patient_address
        self.provider_address = provider_address
        self.provider_private_key = provider_private_key
        self.provider_employee_address = provider_employee_address
        self.provider_employee_private_key = provider_employee_private_key
        self.document_ipfs_address = document_ipfs_address

    def __getattr__(self, attr):
        return self.data[attr]

    def to_dict(self):
        return OrderedDict({'transaction_type':'medical_record',
                            'patient_address': self.patient_address,
                            'provider_address': self.provider_address,
                            'provider_employee_address': self.provider_employee_address,
                            'document_ipfs_address': self.document_ipfs_address})

    def sign_medical_record_creation(self):
        """
        Sign transaction with private key
        """
        private_key = RSA.importKey(binascii.unhexlify(self.provider_private_key))
        signer = PKCS1_v1_5.new(private_key)
        h = SHA.new(str(self.to_dict()).encode('utf8'))
        return binascii.hexlify(signer.sign(h)).decode('ascii')



app = Flask(__name__)

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
	random_gen = Crypto.Random.new().read
	private_key = RSA.generate(1024, random_gen)
	public_key = private_key.publickey()
	response = {
		'private_key': binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'),
		'public_key': binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii')
	}

	return jsonify(response), 200

@app.route('/generate/medical/record', methods=['POST'])
def generate_medical_record():
	patient_address = request.form['patient_address']
	print('patient_address: '+patient_address)
	provider_address = request.form['provider_address']
	print('provider_address: '+provider_address)
	provider_private_key = request.form['provider_private_key']
	print('provider_private_key: '+provider_private_key)
	provider_employee_address = request.form['provider_employee_address']
	print('provider_employee_address: '+provider_employee_address)
	provider_employee_private_key = request.form['provider_employee_private_key']
	print('provider_employee_private_key: '+provider_employee_private_key)
	document_ipfs_address = request.form['document_ipfs_address']
	print('document_ipfs_address: '+document_ipfs_address)

	medical_record = MedicalRecord(patient_address
                                , provider_address
                                , provider_private_key
                                , provider_employee_address
                                , provider_employee_private_key
                                , document_ipfs_address)

	response = {'medical_record': medical_record.to_dict(), 'signature': medical_record.sign_medical_record_creation()}
	print("test")
    
	return jsonify(response), 200


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=8080, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='127.0.0.1', port=port)