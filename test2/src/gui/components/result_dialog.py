import tkinter as tk
from tkinter import scrolledtext
from config.settings import Settings

class ResultDialog(tk.Toplevel):
    def __init__(self, parent, message):
        super().__init__(parent)
        self.title("Test Results")
        self.geometry("600x400")
        self.configure(bg=Settings.SECTION_BG)
        self.create_widgets(message)
    
    def create_widgets(self, message):
        tk.Label(
            self, 
            text="ECDSA Test Results", 
            font=("Helvetica", 16, "bold"), 
            fg="#ffffff", 
            bg=Settings.SECTION_BG
        ).pack(pady=(10, 10))
        
        result_text = scrolledtext.ScrolledText(
            self, 
            height=15, 
            width=70, 
            font=("Helvetica", 12), 
            bg=Settings.TEXT_BG, 
            fg=Settings.TEXT_FG,
            wrap=tk.WORD
        )
        result_text.pack(padx=10, pady=10, fill="both", expand=True)
        result_text.insert(tk.END, message)
        result_text.config(state='disabled')
        
        tk.Button(
            self, 
            text="Close", 
            command=self.destroy, 
            **Settings.BUTTON_STYLE
        ).pack(pady=10)