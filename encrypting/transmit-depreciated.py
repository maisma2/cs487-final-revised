# transmit-depreciated.py

import numpy as np

# Function to simulate packet transmission with a certain drop probability
def transmit_packets(signal, packet_size=1000, drop_probability=0.2):
    """Simulate transmission of packets, with a drop probability"""
    num_packets = len(signal) // packet_size
    if len(signal) % packet_size != 0:
        num_packets += 1  # If there is leftover signal data, create an additional packet

    transmitted_packets = []
    
    for i in range(num_packets):
        start = i * packet_size
        end = (i + 1) * packet_size
        packet = signal[start:end]
        
        # Simulate packet loss based on drop probability
        if np.random.rand() > drop_probability:
            transmitted_packets.append(packet)
        else:
            print(f"Packet {i+1} dropped.")

    return transmitted_packets

