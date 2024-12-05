# analog_encrypt.py

import numpy as np
from scipy.signal import chirp

# Translate digital message to analog message using simple
def digital_to_analog(message, sample_rate=1000, duration=1):
    t = np.linspace(0, duration, int(sample_rate * duration))
    analog_signal = np.zeros_like(t)
    
    # Give every character different frequency
    for i, char in enumerate(message):
        freq = 100 + ord(char)
        signal_segment = chirp(t, f0=freq, f1=freq + 10, t1=duration, method='linear')
        analog_signal += signal_segment

    return analog_signal

# Frequency Modulation Encryption
def fme_encryption(analog_signal, sample_rate=1000, modulation_index=10):
    t = np.linspace(0, len(analog_signal) / sample_rate, len(analog_signal))
    
    # Apply frequency modulation: modulate the signal based on the input analog signal
    modulated_signal = analog_signal * np.cos(2 * np.pi * modulation_index * np.sin(2 * np.pi * t))

    return modulated_signal
