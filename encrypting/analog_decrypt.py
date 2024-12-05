import numpy as np
from scipy.signal import chirp


def decode_analog_message(encrypted_signal, sample_rate=1000, modulation_index=10, duration=1):
    # FME Decryption
    t = np.linspace(0, len(encrypted_signal) / sample_rate, len(encrypted_signal))

    # Directly reverse
    recovered_signal = encrypted_signal / np.cos(2 * np.pi * modulation_index * np.sin(2 * np.pi * t))

    # Convert analog signal back to digital message
    step_size = int(sample_rate * duration)  # Length of one signal segment (duration per character)
    num_segments = len(recovered_signal) // step_size  # Total number of segments
    message = ""

    for i in range(num_segments):
        segment = recovered_signal[i * step_size:(i + 1) * step_size]

        # Estimate frequency of the segment (using a simple method)
        freq = estimate_frequency(segment, step_size, duration)
        # Adjustment paremeter
        freq = np.ceil(freq) - 3

        if freq > 100:  # Only consider valid frequencies (100 and above)
            char = chr(int(abs(freq - 100)))  # Reverse the frequency-to-character mapping
            message += char

    return message


# Estimate the dominant frequency of a signal segment
def estimate_frequency(segment, step_size, duration):
    t = np.linspace(0, duration, step_size)

    # Perform Fast Fourier Transform (FFT) to identify dominant frequency
    spectrum = np.fft.fft(segment)
    freqs = np.fft.fftfreq(len(segment), d=t[1] - t[0])

    # Find the frequency with the highest magnitude in the positive frequency range
    positive_freqs = freqs[freqs > 0]
    positive_spectrum = np.abs(spectrum[freqs > 0])

    dominant_freq = positive_freqs[np.argmax(positive_spectrum)]
    return dominant_freq