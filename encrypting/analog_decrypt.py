import numpy as np
from scipy.signal import chirp


def decode_analog_message(encrypted_signal, sample_rate=1000, modulation_index=10, duration=1):
    # Step 1: FME Decryption
    t = np.linspace(0, len(encrypted_signal) / sample_rate, len(encrypted_signal))
    recovered_signal = encrypted_signal / np.cos(2 * np.pi * modulation_index * np.sin(2 * np.pi * t))

    # Step 2: Convert analog signal back to digital message
    step_size = int(sample_rate * duration)  # Length of one signal segment
    num_segments = len(recovered_signal) // step_size  # Total segments
    message = ""

    for i in range(num_segments):
        segment = recovered_signal[i * step_size:(i + 1) * step_size]

        # Estimate frequency of the segment
        freq = estimate_frequency(segment, step_size, duration)
        char = chr(int(freq - 100))  # Reverse the frequency-to-character mapping
        message += char

    return message


# Estimate the dominant frequency of a signal segment
def estimate_frequency(segment, step_size, duration):
    t = np.linspace(0, duration, step_size)
    spectrum = np.fft.fft(segment)
    freqs = np.fft.fftfreq(len(segment), d=t[1] - t[0])
    dominant_freq = freqs[np.argmax(np.abs(spectrum))]
    return abs(dominant_freq)

