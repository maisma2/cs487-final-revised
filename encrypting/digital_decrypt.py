# digital_decrypt.py

from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad
import sys


# AES Decryption
def aes_decryption(encrypted_data, key=None):
    if key is None:
        print("Error: AES decryption requires a valid key!")
        sys.exit(1)  # Exit the program with error code 1

    iv = encrypted_data[:16]  # First 16 bytes is the IV
    ciphertext = encrypted_data[16:]  # The rest is the ciphertext
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_data.decode()

