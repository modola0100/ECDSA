import os
import datetime
from ecdsa import SigningKey, VerifyingKey, SECP256k1

class FileHandler:
    def __init__(self, data_dir):
        self.data_dir = data_dir
    
    def initialize_data_dir(self):
        try:
            if not os.path.exists(self.data_dir):
                os.makedirs(self.data_dir)
            return True
        except Exception:
            return False
    
    def get_file_path(self, filename):
        return os.path.join(self.data_dir, filename)
    
    def get_timestamp(self):
        return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def save_key(self, filename, key_data):
        try:
            with open(self.get_file_path(filename), 'w') as f:
                f.write(key_data)
            return True
        except Exception:
            return False
    
    def save_signature(self, filename, signature_data):
        try:
            with open(self.get_file_path(filename), 'w') as f:
                f.write(signature_data)
            return True
        except Exception:
            return False
    
    def save_message(self, filename, message):
        try:
            with open(self.get_file_path(filename), 'w', encoding='utf-8') as f:
                f.write(message)
            return True
        except Exception:
            return False
    
    def load_file_content(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                return f.read()
        except Exception:
            return None
    
    def load_private_key(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                private_key_bytes = f.read()
            return SigningKey.from_string(bytes.fromhex(private_key_bytes.decode()), curve=SECP256k1)
        except Exception:
            return None
    
    def load_public_key(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                public_key_bytes = f.read()
            return VerifyingKey.from_string(bytes.fromhex(public_key_bytes.decode()), curve=SECP256k1)
        except Exception:
            return None
    
    def load_latest_signature(self):
        try:
            sig_files = [f for f in os.listdir(self.data_dir) if f.endswith('.sig')]
            if not sig_files:
                return None
            latest_sig_file = max([self.get_file_path(f) for f in sig_files], key=os.path.getctime)
            with open(latest_sig_file, 'r') as f:
                signature_hex = f.read().strip()
            return bytes.fromhex(signature_hex)
        except Exception:
            return None