import tkinter as tk
from gui.app import ECDSASignerApp

def main():
    root = tk.Tk()
    app = ECDSASignerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()