# main.py

from analog_encrypt import digital_to_analog, fme_encryption
from digital_encrypt import aes_encryption
from analog_decrypt import decode_analog_message
from digital_decrypt import aes_decryption
import os

# Function to generate a random message for testing
def generate_random_message(length=16):
    import random
    import string
    message = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    return message

# Function to save data to a file
def save_to_folder(folder_name, file_name, data):
    os.makedirs(folder_name, exist_ok=True)  # Create folder if it doesn't exist
    file_path = os.path.join(folder_name, file_name)
    with open(file_path, 'wb') as file:
        file.write(data)
    print(f"Data saved to {file_path}")

# Main execution starts here
if __name__ == "__main__":
    # Generate random message for testing
    message = generate_random_message()
    print(f"Message length: {len(message)} \n ",
          f"Original Message: {message}")

    # Step 1: Convert the message to analog signal
    analog_signal = digital_to_analog(message)

    # Step 2: Encrypt the analog signal using FME
    fme_encrypted_signal = fme_encryption(analog_signal)
    save_to_folder('encrypted_files', 'fme_encrypted_signal.bin', fme_encrypted_signal)

    # Step 3: Encrypt the message using AES
    aes_key, aes_encrypted_signal = aes_encryption(message)
    save_to_folder('encrypted_files', 'aes_encrypted_signal.bin', aes_encrypted_signal)
    save_to_folder('encrypted_files', 'aes_key', aes_key)


