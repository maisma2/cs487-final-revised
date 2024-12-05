"""
Original Author(s): Ajay Kshemkalyani <ajay@uic.edu>, Rohan Vardekar <rvarde2@uic.edu>
Created for CS450, Fall 2024

Purpose: To simulate a lossy, constrained network with corruption, but no packet drops
            To then rework functions to create a stable TCP connection with package managers,
            error checking, and RTT calculations

Amended for CS487 Fall 2024, changed hw5.py to allow for "corrupted" files and unstable
        connections. Also amended tester.py script to allow for corruption arguments,
        and declaring default file destinations along with changes to server.py for sending
        the same corruption arguments. The rest of the files are unchanged from the original
        commit from the CS450 repository.

Date: 12/1/2024
"""


import socket
import io
import time
import typing
import struct
import random
import homework5
import homework5.logging


def send(sock: socket.socket, data: bytes, corruption_value: float):
    """
    Simulated sending logic for a lossy, constrained network with corruption, but no packet drops.
    """
    import random
    logger = homework5.logging.get_logger("hw5-sender")
    chunk_size = homework5.MAX_PACKET
    pause = 0.1
    corruption_probability = corruption_value  # 10% chance to corrupt a packet
    offsets = range(0, len(data), homework5.MAX_PACKET)

    for chunk in [data[i:i + chunk_size] for i in offsets]:
        # Simulate corruption
        if random.random() < corruption_probability:
            corrupted_chunk = bytearray(chunk)
            index = random.randint(0, len(corrupted_chunk) - 1)
            corrupted_chunk[index] ^= 0xFF  #One byte gets flipped
            chunk = bytes(corrupted_chunk)
            logger.warning("Corrupting a packet at index %d", index)

        sock.send(chunk)
        logger.info("Sent a packet of size %d bytes. Pausing for %f seconds", len(chunk), pause)
        time.sleep(pause)


def recv(sock: socket.socket, dest: io.BufferedIOBase) -> int:
    """
    Implementation of the receiving logic for receiving data over a slow,
    lossy, constrained network.

    Args:
        sock -- A socket object, constructed and initialized to communicate
                over a simulated lossy network.

    Return:
        The number of bytes written to the destination.
    """
    logger = homework5.logging.get_logger("hw5-receiver")
    # Naive solution, where we continually read data off the socket
    # until we don't receive any more data, and then return.
    num_bytes = 0
    while True:
        data = sock.recv(homework5.MAX_PACKET)
        if not data:
            break
        logger.info("Received %d bytes", len(data))
        dest.write(data)
        num_bytes += len(data)
        dest.flush()
    return num_bytes