import tkinter as tk
from tkinter import filedialog
from config.settings import Settings

class MessageInputSection(tk.Frame):
    def __init__(self, parent, load_file_cmd, load_verify_cmd, clear_cmd):
        super().__init__(parent, bg=Settings.SECTION_BG, padx=15, pady=15, relief="raised", bd=2)
        self.load_file_cmd = load_file_cmd
        self.load_verify_cmd = load_verify_cmd
        self.clear_cmd = clear_cmd
        self.create_widgets()
    
    def create_widgets(self):
        tk.Label(
            self, 
            text="Message / File Input", 
            font=("Helvetica", 16, "bold"), 
            fg="#ffffff", 
            bg=Settings.SECTION_BG
        ).pack(anchor="w", pady=(0, 10))

        self.message_entry = tk.Text(
            self, 
            height=5, 
            font=("Helvetica", 12), 
            bg=Settings.TEXT_BG, 
            fg=Settings.TEXT_FG
        )
        self.message_entry.pack(fill="x", pady=5)

        file_frame = tk.Frame(self, bg=Settings.SECTION_BG)
        file_frame.pack(fill="x")

        tk.Button(file_frame, text="Load File to Sign", command=self.load_file_cmd, **Settings.BUTTON_STYLE).pack(side="left", padx=5)
        tk.Button(file_frame, text="Load File to Verify", command=self.load_verify_cmd, **Settings.BUTTON_STYLE).pack(side="left", padx=5)
        tk.Button(file_frame, text="Clear Input", command=self.clear_cmd, **Settings.BUTTON_STYLE).pack(side="left", padx=5)
    
    def get_message(self):
        return self.message_entry.get(1.0, tk.END).strip()
    
    def update_message_entry(self, content):
        self.message_entry.delete(1.0, tk.END)
        self.message_entry.insert(tk.END, content)
    
    def open_file_dialog(self):
        return filedialog.askopenfilename()