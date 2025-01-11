# YouTube Video Transcriber

This project is a **Streamlit** application for transcribing YouTube video audio using YouTube APIs and audio processing libraries. The application also supports generating **VTT** files for subtitles.

The application is running online and can be accessed at: [https://video-transcript-app.streamlit.app/](https://video-transcript-app.streamlit.app/)

---

## 🚀 Features

- **Download audio** from YouTube videos using `yt-dlp`.
- **Split audio** into segments based on silence.
- **Automatic audio transcription** using Google Speech Recognition.
- Generate **VTT** subtitle files.
- Support for multiple languages for subtitles and transcription.

---

## 🛠️ Project Structure

```plaintext
.
├── app.py                    # Main Streamlit interface
├── backend.py                # Core logic and API integration
├── utils.py                  # Utility functions for validation and executable search
├── YouTubeTranscriber.py     # Main class for audio processing and transcription
├── data/                     # Directory to store intermediate data
│   ├── audio/                # Downloaded audio files from YouTube
│   ├── chunks/               # Audio fragments after splitting
│   ├── output/               # Output files (e.g., VTT subtitles)
```

### Details of the `data` Directory:
- **`audio/`**: Contains audio files downloaded from YouTube in `.mp3` format.
- **`chunks/`**: Contains audio fragments resulting from silence-based splitting.
- **`output/`**: Contains generated subtitle files in `.vtt` format.

---

## ⚙️ Setup

1. **Prerequisites**:
   - Python 3.8 or higher.
   - ffmpeg installed on the system.
   - Dependencies listed in the `requirements.txt` file.

2. **Install Dependencies**:
   In the project's root directory, run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure YouTube API Credentials**:
   - Add your `client_secret.json` file for OAuth2 authentication.
   - Define your Google API key in the `.env` file:
     ```
     GOOGLE_API_KEY=your_google_api_key
     ```

4. **Configure ffmpeg**:
   - Ensure ffmpeg is installed and available in the `PATH`.
   - The `utils.encontrar_ffmpeg` script automates locating the executable.

---

## 📦 How to Use

1. **Run Locally**:
   Start the application with the command:
   ```bash
   streamlit run app.py
   ```

2. **Application Workflow**:
   - Enter the YouTube video ID or URL.
   - Select the video language and transcription language.
   - Click **Transcribe Video** to generate subtitles.

3. **Generated Files**:
   - `.vtt` files will be saved in the `data/output/` directory.

---

## ⚙️ Dependencies

- **Streamlit**: User interface.
- **yt-dlp**: For downloading audio from YouTube.
- **pydub**: For audio manipulation and splitting.
- **speech_recognition**: For audio transcription.
- **ffmpeg**: For audio conversion.

---

## 🛠️ Modular Structure

### **`app.py`**
- Manages the Streamlit interface and interacts with the `backend.py` and `utils.py` modules.

### **`backend.py`**
- Implements the main functions for YouTube API integration and transcription.

### **`utils.py`**
- Provides helper functions like URL validation and ffmpeg location.

### **`YouTubeTranscriber.py`**
- Main class for downloading, splitting, and transcribing audio.

---

## 👨‍💻 Contributing

1. Fork the repository.
2. Create your branch:
   ```bash
   git checkout -b my-feature
   ```
3. Make your changes and commit:
   ```bash
   git commit -m "Feature description"
   ```
4. Push your changes:
   ```bash
   git push origin my-feature
   ```
5. Open a Pull Request.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

🌟 **Feel free to contribute and improve this project!**

## Final Notes

This project was developed as an educational tool. Feel free to use!

## Thank You for Your Support! 🌟

We hope you find our services helpful and enjoyable! If you feel like showing some extra appreciation, why not buy us a coffee? 

🍵 Your support not only energizes our team but also helps us keep improving what we do.

To make a small contribution, you can send us a coffee's worth of USDT or Brazilian Instant Payment (PIX) to our QR code. Every coffee counts and keeps us brewing more ideas!

### Here's how you can send a USDT coffee:

![Coffee QR Code](https://raw.githubusercontent.com/dadosnapratica/buy_a_coffe_qrcodes/refs/heads/main/qr_code_usdt_enus_200px.png)

or send USDT to address:
```text
0x3db4d1dd10b60c278f27bd1b2e2bd888d0f99f85
```

1. **Scan the QR Code:** Open your crypto wallet and scan our USDT QR code.
2. **Enter the amount:** The cost of a coffee - usually around $3 to $5.
3. **Send your support:** Hit send and make our day!

### Here's how you can send a PIX coffee:

![Coffee QR Code](https://raw.githubusercontent.com/dadosnapratica/buy_a_coffe_qrcodes/refs/heads/main/qr_code_pix_bradesco.png)

1. **Scan the QR Code:** Open your bank account app and scan our PIX QR code.
2. **Enter the amount:** The cost of a coffee - usually around $3 to $5.
3. **Send your support:** Hit send and make our day!

PIX is a digital payment system in Brazil that allows instant payments 24/7 via mobile phones. If you found this project helpful, please consider buying me a coffee.

Thank you once again for your incredible support and for being a part of our community. Your contribution fuels our passion and commitment.



## Author

**Flavio Lopes** Spreading practical data knowledge for decision making.

## Contact

Questions, suggestions, or improvements? Contact me or contribute directly to the repository.

-   **GitHub**: [dadosnapratica](https://github.com/orgs/dadosnapratica)
-   **LinkedIn**: [Flavio Lopes](https://www.linkedin.com/in/flavionlopes/)
-   **Email**: [flavio.lopes@ideiasfactory.tech](mailto:flavio.lopes@ideiasfactory.tech)
-   **Instagram**: [@dadosnapratica](https://www.instagram.com/dadosnapratica/)