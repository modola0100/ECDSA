class TestHandler:
    def __init__(self, ecdsa_handler):
        self.ecdsa_handler = ecdsa_handler
    
    def run_tests(self, file_handler):
        result_message = ""
        
        # Test 1: Message Signing and Tampering Detection
        result_message += "Test 1: Message Signing and Tampering Detection\n"
        message = "This is a test message for ECDSA."
        private_key, public_key = self.ecdsa_handler.generate_key_pair()
        signature = self.ecdsa_handler.sign_message(message, private_key)
        
        is_valid = self.ecdsa_handler.verify_message(message, signature, public_key)
        result_message += f"Original Message: {message}\n"
        result_message += f"Verification: {'Success' if is_valid else 'Failed'}\n"
        
        tampered_message = message + " Tampered!"
        is_tampered_valid = self.ecdsa_handler.verify_message(tampered_message, signature, public_key)
        result_message += f"Tampered Message: {tampered_message}\n"
        result_message += f"Tampered Verification: {'Success' if is_tampered_valid else 'Failed'}\n"
        result_message += "Expected: Tampered verification should fail.\n\n"
        
        # Test 2: File Signing and Tampering Detection
        result_message += "Test 2: File Signing and Tampering Detection\n"
        test_file_content = "This is a test file content."
        test_file_path = file_handler.get_file_path("test_file.txt")
        tampered_file_path = file_handler.get_file_path("test_file_tampered.txt")
        
        file_handler.save_message("test_file.txt", test_file_content)
        file_handler.save_message("test_file_tampered.txt", test_file_content + " Tampered!")
        
        signature = self.ecdsa_handler.sign_message(test_file_content, private_key)
        
        is_valid = self.ecdsa_handler.verify_message(test_file_content, signature, public_key)
        result_message += f"Original File Verification: {'Success' if is_valid else 'Failed'}\n"
        
        tampered_content = file_handler.load_file_content(tampered_file_path).decode('utf-8', errors='ignore')
        is_tampered_valid = self.ecdsa_handler.verify_message(tampered_content, signature, public_key)
        result_message += f"Tampered File Verification: {'Success' if is_tampered_valid else 'Failed'}\n"
        result_message += "Expected: Tampered file verification should fail.\n\n"
        
        # Test 3: Verification with Wrong Public Key
        result_message += "Test 3: Verification with Wrong Public Key\n"
        wrong_private_key, wrong_public_key = self.ecdsa_handler.generate_key_pair()
        
        signature = self.ecdsa_handler.sign_message(message, private_key)
        is_valid_wrong_key = self.ecdsa_handler.verify_message(message, signature, wrong_public_key)
        result_message += f"Verification with Wrong Key: {'Success' if is_valid_wrong_key else 'Failed'}\n"
        result_message += "Expected: Verification with wrong key should fail.\n"
        
        return result_message