# receive-depreciated.py

import numpy as np

# Function to simulate packet reception and reassemble signal from packets
def receive_packets(transmitted_packets, original_length):
    """Simulate receiving of packets and reassemble the signal"""
    
    # Check if transmitted_packets is empty
    if not transmitted_packets:
        raise ValueError("No packets received.")
    
    # Remove any empty packets (if they exist) before concatenating
    transmitted_packets = [packet for packet in transmitted_packets if packet.size > 0]
    
    if not transmitted_packets:
        raise ValueError("No valid packets to reassemble.")
    
    # Reassemble signal from received packets
    received_signal = np.concatenate(transmitted_packets)

    # If there is missing data (due to dropped packets), pad the signal with zeros
    if len(received_signal) < original_length:
        print("Warning: Some packets were lost during transmission. Padding with zeros.")
        missing_length = original_length - len(received_signal)
        received_signal = np.pad(received_signal, (0, missing_length), mode='constant')

    return received_signal

