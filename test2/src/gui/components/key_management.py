import tkinter as tk
from tkinter import filedialog, ttk
from config.settings import Settings

class KeyManagementSection(tk.Frame):
    def __init__(self, parent, generate_cmd, load_private_cmd, load_public_cmd, selected_key_id, update_key_cmd):
        super().__init__(parent, bg=Settings.SECTION_BG, padx=15, pady=15, relief="raised", bd=2)
        self.generate_cmd = generate_cmd
        self.load_private_cmd = load_private_cmd
        self.load_public_cmd = load_public_cmd
        self.selected_key_id = selected_key_id
        self.update_key_cmd = update_key_cmd
        self.create_widgets()
    
    def create_widgets(self):
        tk.Label(
            self, 
            text="Key Management", 
            font=("Helvetica", 16, "bold"), 
            fg="#ffffff", 
            bg=Settings.SECTION_BG
        ).pack(anchor="w", pady=(0, 10))

        key_frame = tk.Frame(self, bg=Settings.SECTION_BG)
        key_frame.pack(fill="x")

        tk.Button(key_frame, text="Generate Key Pair", command=self.generate_cmd, **Settings.BUTTON_STYLE).pack(side="left", padx=5)
        tk.Button(key_frame, text="Load Private Key", command=self.load_private_cmd, **Settings.BUTTON_STYLE).pack(side="left", padx=5)
        tk.Button(key_frame, text="Load Public Key", command=self.load_public_cmd, **Settings.BUTTON_STYLE).pack(side="left", padx=5)

        tk.Label(
            key_frame, 
            text="Select Key Pair:", 
            font=("Helvetica", 12), 
            fg="#ffffff", 
            bg=Settings.SECTION_BG
        ).pack(side="left", padx=(20, 5))
        
        self.key_dropdown = ttk.Combobox(key_frame, textvariable=self.selected_key_id, font=("Helvetica", 12))
        self.key_dropdown.pack(side="left", padx=5)
        self.key_dropdown.bind('<<ComboboxSelected>>', self.update_key_cmd)

        self.key_display = tk.Text(
            self, 
            height=2, 
            width=80, 
            font=("Helvetica", 12), 
            bg=Settings.TEXT_BG, 
            fg=Settings.TEXT_FG
        )
        self.key_display.pack(fill="x", pady=5)
        self.key_display.insert(tk.END, "Key status will appear here...\n")
        self.key_display.config(state='disabled')
    
    def update_key_dropdown(self, key_list, selected_key):
        self.key_dropdown['values'] = key_list
        self.selected_key_id.set(selected_key)
    
    def update_key_display(self, key_id):
        self.key_display.config(state='normal')
        self.key_display.delete(1.0, tk.END)
        self.key_display.insert(tk.END, f"Selected key pair: {key_id}\n")
        self.key_display.config(state='disabled')
    
    def open_file_dialog(self, file_type, extension):
        return filedialog.askopenfilename(filetypes=[(file_type, extension)])