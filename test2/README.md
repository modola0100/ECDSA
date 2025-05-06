ECDSA Secure Signer
A Python application for signing and verifying messages/files using the ECDSA algorithm with a modern Tkinter GUI.
Features

Generate ECDSA key pairs (SECP256k1 curve).
Sign messages or files with a private key.
Verify signatures using a public key.
Load/save keys and signatures from/to files.
Run automated tests to validate ECDSA functionality.
User-friendly GUI with dark theme.

Project Structure
ecdsa_signer/
├── src/
│   ├── main.py               # Application entry point
│   ├── config/              # Configuration settings
│   ├── gui/                 # GUI components
│   ├── core/                # ECDSA logic and tests
│   ├── utils/               # Utility functions
├── tests/                   # Unit tests
├── requirements.txt         # Dependencies
├── README.md               # Documentation
└── .gitignore              # Git ignore file

Installation

Clone the repository:git clone <repository-url>
cd ecdsa_signer


Create a virtual environment and install dependencies:python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt


Run the application:python src/main.py



Requirements

Python 3.6+
Tkinter (included with standard Python)
ecdsa (pip install ecdsa)

Usage

Generate Key Pair: Click "Generate Key Pair" to create a new private-public key pair.
Load Keys: Use "Load Private Key" or "Load Public Key" to import existing keys.
Sign Message/File: Enter a message or load a file, then click "Sign Message/File".
Verify Signature: Load a message/file and select a signature, then click "Verify Signature".
Run Tests: Click "Run ECDSA Tests" to validate the signing/verification process.

Running Tests
python -m unittest discover tests

Contributing
Contributions are welcome! Please submit a pull request or open an issue.
License
MIT License
