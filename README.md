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

### Details of the `data` Directory

- **`audio/`**: Contains audio files downloaded from YouTube in `.mp3` format.
- **`chunks/`**: Contains audio fragments resulting from silence-based splitting.
- **`output/`**: Contains generated subtitle files in `.vtt` format.

---

## ⚙️ Setup

Before you begin, ensure that Python 3.10 is installed on your system. Additionally, you will need FFmpeg for video and audio processing.

### **Prerequisites**

- Python 3.10 or higher.
- ffmpeg installed on the system.
- Create Google API Key for free use of YouTube Data API
- Write permission for ./data path
- Install Dependencies listed in the `requirements.txt` file.

#### 1. **Install Python 3.10**

##### Windows and macOS

Download and install Python 3.10 from the [official Python website](https://www.python.org/downloads/release/python-3100/). Be sure to check the option "Add Python 3.10 to PATH" during installation on Windows.

##### Linux

Use the package manager to install Python 3.10 on Ubuntu. For example, on Ubuntu, run:

##### Install Pre-reqs and Update APT

```bash
sudo apt update
sudo apt install software-properties-common -y
```

##### Add custom APT repository

```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
```

##### Install Python

```bash
sudo apt install python3.10 python3.10-venv python3.10-dev
python3 --version
```

##### Check installed version

```bash
python3 --version
```

#### MacOS

```bash
   brew install python@3.10
```

#### 2. **Configure ffmpeg**

##### Check if ffmpeg is installed

```bash
ffmepg --version
```

##### On Linux

```bash
sudo apt update
sudo apt install ffmpeg
```

##### On MacOS

```bash
brew install ffmpeg
```

##### On Windows

###### Download FFmpeg

- Go to the official FFmpeg website: https://ffmpeg.org/download.html. 
- Under "Get packages & executable files", select "Windows" and choose the latest "Windows - Builds by BtbN" option.
- Download the appropriate zip file for your system. 

###### Extract the files

- Locate the downloaded zip file. 
- Right-click on it and select "Extract All". 
- Choose a destination folder, ideally creating a new folder named "FFmpeg" on your C drive.

** Ensure ffmpeg is installed and available in the `PATH`.

#### 3. **Configure YouTube API Credentials**:

- Create a project on the Google Cloud Console at https://console.cloud.google.com/.
- Enable the YouTube Data API v3 by navigating to "APIs & Services" > "Library", search for "YouTube Data API v3" and enable it.
- Create credentials (API Key) by going to "Credentials", click on "Create Credentials", and select "API key".
- Restrict the key to specific APIs (YouTube Data API v3).
- Create an .env file at the root of your project and add the key as follows

```envfile
GOOGLE_API_KEY=your_key_here
```

#### 4. **Install Dependencies**:

   In the project's root directory, run:

   ```bash
   pip install -r requirements.txt
   ```

## 📦 How to Use

1. **Run Locally**:
   Start the application with the command:

   ```bash
   streamlit run app.py
   ```

2. **Application Workflow**:
   - Enter the YouTube video ID or URL.
   - Click **Transcribe Video** to generate subtitles.

   ** There are Language dropdowns for future translate feature

3. **Generated Files**:
   - `.vtt` files will be saved in the `data/output/` directory.

4. **VTT content are avaliabel in a text area**
---

## ⚙️ Dependencies

- **Streamlit**: User interface.
- **yt-dlp**: For downloading audio from YouTube.
- **pydub**: For audio manipulation and splitting.
- **speech_recognition**: For audio transcription.
- **Google Youtube Data API**: For get video metadata and validate existence of youtube url or id inputed.
- **ffmpeg**: For audio conversion and split.

---

## 🛠️ Project Modular Architecture

### Application Layers

- **Presentation Layer**

   #### **`app.py`**

   - Manages the Streamlit interface and interacts with the `backend.py` and `utils.py` modules.

- **Backend Layer**, for interact with external services, eg. language table

   #### **`backend.py`**

   - Implements the main functions for YouTube API integration and transcription.

   #### **`utils.py`**

   - Provides helper functions like URL validation and ffmpeg location.

   #### **`YouTubeTranscriber.py`**

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

### Here's how you can send a USDT coffee

![Coffee QR Code](https://raw.githubusercontent.com/dadosnapratica/buy_a_coffe_qrcodes/refs/heads/main/qr_code_usdt_enus_200px.png)

or send USDT to address:

```text
0x3db4d1dd10b60c278f27bd1b2e2bd888d0f99f85
```

1. **Scan the QR Code:** Open your crypto wallet and scan our USDT QR code.
2. **Enter the amount:** The cost of a coffee - usually around $3 to $5.
3. **Send your support:** Hit send and make our day!

### Here's how you can send a PIX coffee

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

- **GitHub**: [dadosnapratica](https://github.com/orgs/dadosnapratica)
- **LinkedIn**: [Flavio Lopes](https://www.linkedin.com/in/flavionlopes/)
- **Email**: [flavio.lopes@ideiasfactory.tech](mailto:flavio.lopes@ideiasfactory.tech)
- **Instagram**: [@dadosnapratica](https://www.instagram.com/dadosnapratica/)
