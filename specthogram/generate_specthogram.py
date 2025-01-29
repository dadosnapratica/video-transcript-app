# Import required libraries
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display

# Define the correct file path for the new upload
audio_path = "./Sample_Audio.wav"

# Load the audio file
y, sr = librosa.load(audio_path, sr=None)  # Load with original sample rate

# Generate the spectrogram
plt.figure(figsize=(12, 6))
D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
librosa.display.specshow(D, sr=sr, x_axis="time", y_axis="log", cmap="inferno")

# Add labels and title
plt.colorbar(format="%+2.0f dB")
plt.title("Spectrogram of Sample Audio")
plt.xlabel("Time (s)")
plt.ylabel("Frequency (Hz)")
plt.show()
