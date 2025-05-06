import unittest
from src.core.ecdsa_handler import ECDSAHandler

class TestECDSAHandler(unittest.TestCase):
    def setUp(self):
        self.ecdsa = ECDSAHandler()
    
    def test_sign_verify(self):
        message = "Test message"
        private_key, public_key = self.ecdsa.generate_key_pair()
        signature = self.ecdsa.sign_message(message, private_key)
        self.assertTrue(self.ecdsa.verify_message(message, signature, public_key))
    
    def test_tampered_message(self):
        message = "Test message"
        private_key, public_key = self.ecdsa.generate_key_pair()
        signature = self.ecdsa.sign_message(message, private_key)
        tampered_message = message + " Tampered"
        self.assertFalse(self.ecdsa.verify_message(tampered_message, signature, public_key))

if __name__ == '__main__':
    unittest.main()