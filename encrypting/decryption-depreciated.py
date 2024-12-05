# decryption-depreciated.py

from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad
import numpy as np
import sys

# AES Decryption
def aes_decryption(encrypted_data, key=None):
    # If key not given, Error
    if key is None:
        print("Error: AES decryption requires a valid key!")
        sys.exit(1)

    iv = encrypted_data[:16]  # First 16 bytes is the IV
    ciphertext = encrypted_data[16:]  # The rest is the ciphertext
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_data.decode()

# FME Decryption (for simplicity, this is a placeholder function)
def fme_decryption(modulated_signal, sample_rate=1000):
    # Placeholder for FME decryption logic
    # In practice, this requires reverse engineering the modulation process
    return "Decoded message from FME"
