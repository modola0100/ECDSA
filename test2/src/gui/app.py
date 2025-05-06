import tkinter as tk
from tkinter import messagebox
from config.settings import Settings
from gui.components.key_management import KeyManagementSection
from gui.components.message_input import MessageInputSection
from gui.components.action_panel import ActionPanel
from utils.file_handler import FileHandler
from core.ecdsa_handler import ECDSAHandler
from utils.uuid_generator import generate_uuid

class ECDSASignerApp:
    def __init__(self, root):
        self.root = root
        self.root.title(Settings.WINDOW_TITLE)
        self.root.geometry(Settings.WINDOW_SIZE)
        self.root.configure(bg=Settings.BG_COLOR)
        
        self.ecdsa_handler = ECDSAHandler()
        self.file_handler = FileHandler(Settings.DATA_DIR)
        self.key_pairs = {}
        self.signatures = {}
        self.selected_key_id = tk.StringVar()
        self.selected_sig_id = tk.StringVar()
        self.current_signature = None
        self.private_key = None
        self.public_key = None
        
        if not self.file_handler.initialize_data_dir():
            messagebox.showerror("Error", "Failed to create data directory")
            return
        
        self.create_gui()
    
    def create_gui(self):
        main_frame = tk.Frame(self.root, bg=Settings.BG_COLOR, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        title_label = tk.Label(
            main_frame, 
            text="ECDSA Secure Signer", 
            font=("Helvetica", 24, "bold"), 
            fg="#ffffff", 
            bg=Settings.BG_COLOR
        )
        title_label.pack(pady=(0, 20))

        self.key_section = KeyManagementSection(
            main_frame, 
            self.generate_key_pair, 
            self.load_private_key, 
            self.load_public_key, 
            self.selected_key_id, 
            self.update_selected_key
        )
        self.key_section.pack()

        self.message_section = MessageInputSection(
            main_frame, 
            self.load_file, 
            self.load_file_to_verify, 
            self.clear_input
        )
        self.message_section.pack()

        self.action_section = ActionPanel(
            main_frame, 
            self.sign_message_or_file, 
            self.verify_signature, 
            self.run_ecdsa_tests, 
            self.selected_sig_id, 
            self.update_selected_signature
        )
        self.action_section.pack()
    
    def clear_input(self):
        self.message_section.message_entry.delete(1.0, tk.END)
    
    def generate_key_pair(self):
        private_key, public_key = self.ecdsa_handler.generate_key_pair()
        key_id = generate_uuid()
        self.key_pairs[key_id] = {'private': private_key, 'public': public_key}
        
        timestamp = self.file_handler.get_timestamp()
        private_file = f"private_key_{timestamp}_{key_id}.prv"
        public_file = f"public_key_{timestamp}_{key_id}.pub"
        
        if not self.file_handler.save_key(private_file, private_key.to_string().hex()) or \
           not self.file_handler.save_key(public_file, public_key.to_string().hex()):
            messagebox.showerror("Error", "Failed to save keys")
            return
        
        self.key_section.update_key_dropdown(list(self.key_pairs.keys()), key_id)
        self.update_selected_key(None)
    
    def update_selected_key(self, event):
        key_id = self.selected_key_id.get()
        if key_id in self.key_pairs:
            self.private_key = self.key_pairs[key_id].get('private')
            self.public_key = self.key_pairs[key_id].get('public')
            self.key_section.update_key_display(key_id)
    
    def load_private_key(self):
        file_path = self.key_section.open_file_dialog("Private Key Files", "*.prv")
        if file_path:
            private_key = self.file_handler.load_private_key(file_path)
            if private_key:
                public_key = private_key.get_verifying_key()
                key_id = generate_uuid()
                self.key_pairs[key_id] = {'private': private_key, 'public': public_key}
                self.key_section.update_key_dropdown(list(self.key_pairs.keys()), key_id)
                self.update_selected_key(None)
                messagebox.showinfo("Success", "Private key loaded successfully!")
            else:
                messagebox.showerror("Error", "Failed to load private key")
    
    def load_public_key(self):
        file_path = self.key_section.open_file_dialog("Public Key Files", "*.pub")
        if file_path:
            public_key = self.file_handler.load_public_key(file_path)
            if public_key:
                key_id = generate_uuid()
                self.key_pairs[key_id] = {'public': public_key}
                self.key_section.update_key_dropdown(list(self.key_pairs.keys()), key_id)
                self.update_selected_key(None)
                messagebox.showinfo("Success", "Public key loaded successfully!")
            else:
                messagebox.showerror("Error", "Failed to load public key")
    
    def load_file(self):
        file_path = self.message_section.open_file_dialog()
        if file_path:
            content = self.file_handler.load_file_content(file_path)
            if content:
                self.message_section.update_message_entry(content.decode('utf-8', errors='ignore'))
                messagebox.showinfo("Success", "File loaded into message box!")
    
    def load_file_to_verify(self):
        file_path = self.message_section.open_file_dialog()
        if file_path:
            content = self.file_handler.load_file_content(file_path)
            if content:
                self.message_section.update_message_entry(content.decode('utf-8', errors='ignore'))
                messagebox.showinfo("Success", "File loaded for verification!")
    
    def sign_message_or_file(self):
        if not self.private_key:
            messagebox.showerror("Error", "Select or generate a private key first!")
            return
        
        message = self.message_section.get_message()
        if not message:
            messagebox.showerror("Error", "Enter a message or load a file to sign!")
            return
        
        try:
            signature = self.ecdsa_handler.sign_message(message, self.private_key)
            sig_id = generate_uuid()
            self.signatures[sig_id] = signature
            self.current_signature = signature
            
            timestamp = self.file_handler.get_timestamp()
            sig_file = f"signature_{timestamp}_{sig_id}.sig"
            msg_file = f"message_{timestamp}_{sig_id}.txt"
            
            if not self.file_handler.save_signature(sig_file, signature.hex()) or \
               not self.file_handler.save_message(msg_file, message):
                messagebox.showerror("Error", "Failed to save signature/message")
                return
            
            self.action_section.update_sig_dropdown(list(self.signatures.keys()), sig_id)
            self.update_selected_signature(None)
            
            messagebox.showinfo("Success", f"Message signed and saved as:\nSignature: {sig_file}\nMessage: {msg_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to sign message: {str(e)}")
    
    def update_selected_signature(self, event):
        sig_id = self.selected_sig_id.get()
        if sig_id in self.signatures:
            self.current_signature = self.signatures[sig_id]
            self.action_section.update_signature_display(self.current_signature)
    
    def verify_signature(self):
        if not self.public_key:
            messagebox.showerror("Error", "Select or generate a public key first!")
            return
        
        message = self.message_section.get_message()
        if not message:
            messagebox.showerror("Error", "Enter a message or load a file to verify!")
            return
        
        sig_id = self.selected_sig_id.get()
        if sig_id and sig_id in self.signatures:
                signature = self.signatures[sig_id]
        elif self.current_signature:
            signature = self.current_signature
        else:
            signature = self.file_handler.load_latest_signature()
            if not signature:
                messagebox.showerror("Error", "No signature files found or failed to load!")
                return
        
        try:
            is_valid = self.ecdsa_handler.verify_message(message, signature, self.public_key)
            result_message = "Signature is valid! The message/file has not been tampered with.\n" if is_valid else "Signature is invalid! The message/file may have been tampered with.\n"
            self.action_section.show_result_dialog(result_message)
        except Exception as e:
            self.action_section.show_result_dialog(f"Signature verification failed: {str(e)}\n")
    
    def run_ecdsa_tests(self):
        result_message = self.ecdsa_handler.run_tests(self.file_handler)
        self.action_section.show_result_dialog(result_message)