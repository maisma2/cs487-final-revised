# digital_encrypt.py

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

# AES Encryption
def aes_encryption(message):
    # Generate a random AES key (256-bit)
    key = get_random_bytes(32)  # 32 bytes for AES-256
    iv = get_random_bytes(16)  # 16 bytes for IV (Initialization Vector)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(message.encode(), AES.block_size)
    ciphertext = cipher.encrypt(padded_message)

    # Return the encrypted message along with the IV and key (for decryption)
    return key, iv + ciphertext
