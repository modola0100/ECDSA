import tkinter as tk
from tkinter import scrolledtext, ttk
from config.settings import Settings
from gui.components.result_dialog import ResultDialog

class ActionPanel(tk.Frame):
    def __init__(self, parent, sign_cmd, verify_cmd, test_cmd, selected_sig_id, update_sig_cmd):
        super().__init__(parent, bg=Settings.SECTION_BG, padx=15, pady=15, relief="raised", bd=2)
        self.sign_cmd = sign_cmd
        self.verify_cmd = verify_cmd
        self.test_cmd = test_cmd
        self.selected_sig_id = selected_sig_id
        self.update_sig_cmd = update_sig_cmd
        self.create_widgets()
    
    def create_widgets(self):
        tk.Label(
            self, 
            text="Actions", 
            font=("Helvetica", 16, "bold"), 
            fg="#ffffff", 
            bg=Settings.SECTION_BG
        ).pack(anchor="w", pady=(0, 10))

        action_frame = tk.Frame(self, bg=Settings.SECTION_BG)
        action_frame.pack(fill="x")

        tk.Button(action_frame, text="Sign Message/File", command=self.sign_cmd, **Settings.BUTTON_STYLE).pack(side="left", padx=5)
        tk.Button(action_frame, text="Verify Signature", command=self.verify_cmd, **Settings.BUTTON_STYLE).pack(side="left", padx=5)
        tk.Button(action_frame, text="Run ECDSA Tests", command=self.test_cmd, **Settings.BUTTON_STYLE).pack(side="left", padx=5)

        tk.Label(
            action_frame, 
            text="Select Signature:", 
            font=("Helvetica", 12), 
            fg="#ffffff", 
            bg=Settings.SECTION_BG
        ).pack(side="left", padx=(20, 5))
        
        self.sig_dropdown = ttk.Combobox(action_frame, textvariable=self.selected_sig_id, font=("Helvetica", 12))
        self.sig_dropdown.pack(side="left", padx=5)
        self.sig_dropdown.bind('<<ComboboxSelected>>', self.update_sig_cmd)

        tk.Label(
            self, 
            text="Signature:", 
            font=("Helvetica", 14, "bold"), 
            fg="#ffffff", 
            bg=Settings.SECTION_BG
        ).pack(anchor="w", pady=(10, 5))
        
        self.signature_display = scrolledtext.ScrolledText(
            self, 
            height=2, 
            width=80, 
            font=("Helvetica", 12), 
            bg=Settings.TEXT_BG, 
            fg=Settings.TEXT_FG
        )
        self.signature_display.pack(fill="x", pady=5)
        self.signature_display.insert(tk.END, "Signature will appear here...\n")
        self.signature_display.config(state='disabled')
    
    def update_sig_dropdown(self, sig_list, selected_sig):
        self.sig_dropdown['values'] = sig_list
        self.selected_sig_id.set(selected_sig)
    
    def update_signature_display(self, signature):
        self.signature_display.config(state='normal')
        self.signature_display.delete(1.0, tk.END)
        self.signature_display.insert(tk.END, f"Selected Signature: {signature.hex()}\n")
        self.signature_display.config(state='disabled')
    
    def show_result_dialog(self, message):
        ResultDialog(self.winfo_toplevel(), message)