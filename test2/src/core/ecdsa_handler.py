import hashlib
import os
from ecdsa import SigningKey, VerifyingKey, SECP256k1, BadSignatureError
from ecdsa.util import sigencode_der, sigdecode_der, randrange_from_seed__trytryagain
from core.test_handler import TestHandler

class ECDSAHandler:
    def __init__(self):
        self.test_handler = TestHandler(self)
    
    def generate_key_pair(self):
        private_key = SigningKey.generate(curve=SECP256k1)
        public_key = private_key.get_verifying_key()
        return private_key, public_key
    
    def hash_message(self, message):
        if isinstance(message, str):
            message = message.encode('utf-8')
        hash_obj = hashlib.sha256(message)
        return hash_obj.digest()
    
    def sign_message(self, message, private_key):
        message_hash = self.hash_message(message)
        k = randrange_from_seed__trytryagain(os.urandom(32), SECP256k1.order)
        signature = private_key.sign(message_hash, k=k, sigencode=sigencode_der)
        return signature
    
    def verify_message(self, message, signature, public_key):
        message_hash = self.hash_message(message)
        try:
            return public_key.verify(signature, message_hash, sigdecode=sigdecode_der)
        except BadSignatureError:
            return False
    
    def run_tests(self, file_handler):
        return self.test_handler.run_tests(file_handler)