import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

# Load the audio file
audio_path = "./Sample_Audio.wav"
y, sr = librosa.load(audio_path, sr=None)  # Load with original sample rate

# Compute the duration of the audio
duration = librosa.get_duration(y=y, sr=sr)

# Phoneme breakdown with approximate time mapping based on sentence length
sentence = "This is an example text to demonstrate the use of spectrogram in converting speech to text."
phonemes = [
    ("/ðis/ This", 0.0, 0.4),  # "This"
    ("/ɪz/ is", 0.4, 0.6),  # "is"
    ("/æn/ an", 0.6, 0.8),  # "an"
    ("/ɪɡzæmpəl/ example", 0.8, 1.5),  # "example"
    ("/tɛkst/ text", 1.5, 2.0),  # "text"
    ("/tu/ to", 2.0, 2.3),  # "to"
    ("/dɛmənstreɪt/ demonstrate", 2.3, 3.1),  # "demonstrate"
    ("/ðə/ the", 3.1, 3.3), # "the"
    ("/jusʌv/ use of", 3.3, 3.7), # "use of"
    ("/spɛktrəɡræm/ spectrogram", 3.7, 4.3),  # "spectrogram"
    ("/ɪn/ in", 4.3, 4.5),  # "in"
    ("/kənvɝtɪŋ/ converting", 4.5, 5.0), # "converting"
    ("/spiːtʃ/ speech", 5.0, 5.2),  # "speech"
    ("/tətɛkst/ to text", 5.2, 5.6)  # "to text"
]

# Plot the spectrogram again with phoneme time markers
plt.figure(figsize=(12, 6))
D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
librosa.display.specshow(D, sr=sr, x_axis="time", y_axis="log", cmap="inferno")

# Add phoneme markers
# Add phoneme markers with adjusted positioning
for phoneme, start, end in phonemes:
    mid_time = (start + end) / 2  # Center position of phoneme
    plt.axvline(x=start, color="cyan", linestyle="--", alpha=0.7)  # Dashed line at start
    plt.text(mid_time, sr // 30, phoneme, color="white", fontsize=10, rotation=90, ha="center")

# Add labels and title
plt.colorbar(format="%+2.0f dB")
plt.title("Spectrogram with Phoneme Timeline")
plt.xlabel("Time (s)")
plt.ylabel("Frequency (Hz)")
plt.show()
