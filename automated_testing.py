import os
import subprocess
import hashlib
import argparse
import tempfile
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger("automated-test")

PYTHON_BINARY = "python3"  # Update as needed

def calculate_hash(file_path):
    """Calculate SHA-256 hash of a file."""
    with open(file_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def main():
    parser = argparse.ArgumentParser(description="Automated testing script for encryption and networking.")
    parser.add_argument("-f", "--file", required=True, help="Path to the input file (e.g., tester.py).")
    parser.add_argument("-p", "--port", type=int, default=9999, help="Port to use for networking.")
    parser.add_argument("--encrypt-mode", choices=["digital", "analog"], default="digital", help="Encryption mode.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging.")
    args = parser.parse_args()

    if args.verbose:
        LOGGER.setLevel(logging.DEBUG)

    # Paths for intermediate files
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        encrypted_file = temp_file.name
    decrypted_file = tempfile.mktemp()
    key_file = tempfile.mktemp()

    try:
        # Step 1: Encrypt the file
        if args.encrypt_mode == "digital":
            LOGGER.info("Encrypting file using digital encryption...")
            encrypt_script = os.path.join("encrypting", "digital_encrypt.py")
            encrypt_args = [PYTHON_BINARY, encrypt_script, "--input", args.file, "--output", encrypted_file, "--key", key_file]
        else:  # Analog encryption
            LOGGER.info("Encrypting file using analog encryption...")
            encrypt_script = os.path.join("encrypting", "analog_encrypt.py")
            encrypt_args = [PYTHON_BINARY, encrypt_script, "--input", args.file, "--output", encrypted_file]

        subprocess.run(encrypt_args, check=True)

        # Verify the encrypted file exists
        if not os.path.exists(encrypted_file):
            raise FileNotFoundError(f"Encrypted file not found: {encrypted_file}")

        LOGGER.debug(f"Encrypted file path: {encrypted_file}")

        # Step 2: Send the encrypted file
        LOGGER.info("Sending the encrypted file...")
        sender_script = os.path.join("networking", "sender.py")
        sender_args = [PYTHON_BINARY, sender_script, "--port", str(args.port), "--file", encrypted_file]
        subprocess.run(sender_args, check=True)

        # Step 3: Receive the file
        LOGGER.info("Receiving the file...")
        receiver_script = os.path.join("networking", "receiver.py")
        received_file = tempfile.mktemp()
        receiver_args = [PYTHON_BINARY, receiver_script, "--port", str(args.port), "--file", received_file]
        subprocess.run(receiver_args, check=True)

        # Step 4: Decrypt the received file
        if args.encrypt_mode == "digital":
            LOGGER.info("Decrypting file using digital decryption...")
            decrypt_script = os.path.join("encrypting", "digital_decrypt.py")
            decrypt_args = [PYTHON_BINARY, decrypt_script, "--input", received_file, "--output", decrypted_file, "--key", key_file]
        else:  # Analog decryption
            LOGGER.info("Decrypting file using analog decryption...")
            decrypt_script = os.path.join("encrypting", "analog_decrypt.py")
            decrypt_args = [PYTHON_BINARY, decrypt_script, "--input", received_file, "--output", decrypted_file]

        subprocess.run(decrypt_args, check=True)

        # Step 5: Validate the result
        original_hash = calculate_hash(args.file)
        decrypted_hash = calculate_hash(decrypted_file)
        LOGGER.info(f"Original Hash: {original_hash}")
        LOGGER.info(f"Decrypted Hash: {decrypted_hash}")

        if original_hash == decrypted_hash:
            LOGGER.info("SUCCESS: The decrypted file matches the original!")
        else:
            LOGGER.error("FAILURE: The decrypted file does not match the original!")

    except subprocess.CalledProcessError as e:
        LOGGER.error(f"Error during subprocess execution: {e}")
    except FileNotFoundError as e:
        LOGGER.error(f"File not found: {e}")
    finally:
        # Clean up temporary files
        for temp_file in [encrypted_file, decrypted_file, key_file]:
            if os.path.exists(temp_file):
                os.remove(temp_file)

if __name__ == "__main__":
    main()
