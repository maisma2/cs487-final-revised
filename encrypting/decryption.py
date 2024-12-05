from analog_decrypt import decode_analog_message
from digital_decrypt import aes_decryption
import os
import pickle
import numpy as np

# Paths
RECEIVED_FILES_DIR = "received_files"
ENCRYPTED_KEY_FILE = "encrypted_files/aes_key"
DECRYPTED_MESSAGES_DIR = "decrypted_messages"

# Ensure the output directory exists
os.makedirs(DECRYPTED_MESSAGES_DIR, exist_ok=True)


def process_received_files():
    """Process all files in the received files directory."""
    # Load the AES key
    try:
        with open(ENCRYPTED_KEY_FILE, 'rb') as key_file:
            aes_key = key_file.read()  # Read the key as raw binary
        print("AES key loaded successfully.")
    except FileNotFoundError:
        print(f"Error: AES key file not found at {ENCRYPTED_KEY_FILE}")
        return

    for file_name in os.listdir(RECEIVED_FILES_DIR):
        file_path = os.path.join(RECEIVED_FILES_DIR, file_name)

        # Skip directories or non-binary files
        if not os.path.isfile(file_path):
            continue

        print(f"Processing file: {file_name}")

        with open(file_path, "rb") as f:
            file_data = f.read()

        try:
            # Determine the encryption type and decrypt
            if file_name.startswith("fme_"):
                print("Detected FME-encrypted signal.")

                # Convert binary data to NumPy array
                signal_array = np.frombuffer(file_data, dtype=np.float64)
                decrypted_message = decode_analog_message(signal_array)

                # Save the decrypted message
                output_file = os.path.join(DECRYPTED_MESSAGES_DIR, f"{file_name}_decrypted.txt")
                with open(output_file, "w") as out_f:
                    out_f.write(decrypted_message)
                print(f"Decrypted FME message saved to: {output_file}")

            elif file_name.startswith("aes_"):
                print("Detected AES-encrypted signal.")
                decrypted_message = aes_decryption(file_data, aes_key)

                # Save the decrypted message
                output_file = os.path.join(DECRYPTED_MESSAGES_DIR, f"{file_name}_decrypted.txt")
                with open(output_file, "w") as out_f:
                    out_f.write(decrypted_message)
                print(f"Decrypted AES message saved to: {output_file}")

            else:
                print(f"Unknown encryption type for file: {file_name}. Skipping.")

        except Exception as e:
            print(f"Error processing {file_name}: {e}")


if __name__ == "__main__":
    process_received_files()
