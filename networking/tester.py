"""
Utility script for testing HW5 solutions under user set conditions.
"""
import time
import argparse
import subprocess
import hashlib
import pathlib
import sys
import os
import signal
import logging
import homework5.logging
import homework5.utils

DESC = sys.modules[globals()['__name__']].__doc__
PARSER = argparse.ArgumentParser(description=DESC)
PARSER.add_argument('-p', '--port', type=int, default=9999,
                    help="The port to simulate the lossy wire on (defaults to 9999).")
PARSER.add_argument('-l', '--loss', type=float, default=0.0,
                    help="The percentage of packets to drop.")
PARSER.add_argument('-d', '--delay', type=float, default=0.0,
                    help="The number of seconds, as a float, to wait before forwarding a packet on.")
PARSER.add_argument('-b', '--buffer', type=int, default=2,
                    help="The size of the buffer to simulate (defaults to 2 packets).")
PARSER.add_argument('-f', '--file', default=None,
                    help="The specific file to send over the wire. If not provided, all files in 'encrypted_files' will be processed.")
PARSER.add_argument('-r', '--receive', default=None,
                    help="The path to write the received file to. If not provided, the results will be written to a temp file.")
PARSER.add_argument('-s', '--summary', action="store_true",
                    help="Print a one-line summary of whether the transaction was successful, instead of a more verbose description of the result.")
PARSER.add_argument('-v', '--verbose', action="store_true",
                    help="Enable extra verbose mode.")
ARGS = PARSER.parse_args()

LOGGER = homework5.logging.get_logger("hw5-tester")
if ARGS.verbose:
    LOGGER.setLevel(logging.DEBUG)

PYTHON_BINARY = sys.executable
SERVER_ARGS = [PYTHON_BINARY, "server.py"]

if ARGS.verbose:
    SERVER_ARGS.append("-v")

for AN_ARG in ("port", "loss", "delay", "buffer"):
    SERVER_ARGS.append("--" + AN_ARG)
    SERVER_ARGS.append(str(getattr(ARGS, AN_ARG)))

SERVER_PROCESS = None
RECEIVING_PROCESS = None

# Ensure proper cleanup on termination
def on_end(signal, frame):
    for a_process in (SERVER_PROCESS, RECEIVING_PROCESS):
        if a_process is None:
            continue
        try:
            a_process.kill()
        except Exception:
            pass

for A_SIGNAL in (signal.SIGTERM, signal.SIGINT):
    signal.signal(A_SIGNAL, on_end)


# Helper function to get files for processing
def get_files_to_process(directory):
    """Get all files in the directory that don't contain 'key'."""
    files = []
    for file_name in os.listdir(directory):
        if "key" not in file_name.lower():  # Skip files containing 'key'
            file_path = os.path.join(directory, file_name)
            if os.path.isfile(file_path):  # Only process regular files
                files.append(file_path)
    return files


def process_file(file_path):
    """Process a single file."""
    global RECEIVING_PROCESS, SERVER_PROCESS

    INPUT_PATH = pathlib.Path(file_path)
    INPUT_LEN, INPUT_HASH = homework5.utils.file_summary(INPUT_PATH)

    if ARGS.receive:
        DEST_FILE_PATH = ARGS.receive
    else:
        DEST_FILE_PATH = os.path.join("../encrypting/received_files", os.path.basename(file_path))



    RECEIVING_ARGS = [PYTHON_BINARY, "receiver.py",
                      "--port", str(ARGS.port),
                      "--file", DEST_FILE_PATH]

    if ARGS.verbose:
        RECEIVING_ARGS.append("-v")

    RECEIVING_PROCESS = subprocess.Popen(RECEIVING_ARGS)
    LOGGER.info("Starting receiving process: {}".format(RECEIVING_PROCESS.pid))
    time.sleep(1)

    SENDER_ARGS = [PYTHON_BINARY, "sender.py",
                   "--port", str(ARGS.port),
                   "--file", file_path]

    if ARGS.verbose:
        SENDER_ARGS.append("-v")

    LOGGER.info(f"Starting sending process for file: {file_path}")
    START_TIME = time.time()
    subprocess.run(SENDER_ARGS, check=True)
    END_TIME = time.time()

    time.sleep(ARGS.delay)
    RECEIVING_PROCESS.terminate()
    RECEIVING_PROCESS = None

    RECV_PATH = pathlib.Path(DEST_FILE_PATH)
    RECV_LEN, RECV_HASH = homework5.utils.file_summary(RECV_PATH)

    IS_SUCCESS = RECV_HASH == INPUT_HASH
    NUM_SECONDS = END_TIME - START_TIME
    RATE = round(((RECV_LEN / NUM_SECONDS) / 1000), 2)
    TEMPLATE = "[{}] latency={}ms, packet loss={}%, buffer={}, throughput={} Kb/s"

    if ARGS.summary:
        SUMMARY = TEMPLATE.format(
            "SUCCESS" if IS_SUCCESS else "INCORRECT",
            round(ARGS.delay * 1000),
            round(ARGS.loss * 100, 2),
            ARGS.buffer,
            RATE
        )
        print(SUMMARY)
    else:
        print("\n")
        print("Success" if IS_SUCCESS else "Incorrect")
        print("===\n")

        print("Input")
        print("---")
        print(f"File: {file_path}\nLength: {INPUT_LEN}\nHash: {INPUT_HASH}")

        print("\nReceived")
        print("---")
        print(f"File: {DEST_FILE_PATH}\nLength: {RECV_LEN}\nHash: {RECV_HASH}")

        print("\nStats")
        print("---")
        print(f"Time: {round(NUM_SECONDS, 2)} secs\nRate: {RATE} kB/s")


# Main Execution
SERVER_PROCESS = subprocess.Popen(SERVER_ARGS)
LOGGER.info("Starting wire process: {}".format(SERVER_PROCESS.pid))
time.sleep(1)

try:
    if ARGS.file:
        process_file(ARGS.file)
    else:
        LOGGER.info("No file specified. Processing all files in 'encrypted_files'...")
        encrypted_files_dir = "../encrypting/encrypted_files"
        files_to_process = get_files_to_process(encrypted_files_dir)
        for file in files_to_process:
            process_file(file)

except subprocess.CalledProcessError as e:
    LOGGER.error(f"Error during subprocess execution: {e}")
finally:
    if SERVER_PROCESS:
        SERVER_PROCESS.terminate()
