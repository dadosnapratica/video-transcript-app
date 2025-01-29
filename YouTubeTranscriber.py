import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
import speech_recognition as sr
from youtube_dl import YoutubeDL
import logging
import utils
import platform

logging.getLogger('YouTubeTranscriber')

class YouTubeTranscriber:
    def __init__(self, video_url, video_id, base_dir="data"):
        self.base_dir = base_dir
        self.audio_dir = os.path.join(base_dir, "audio")
        self.chunks_dir = os.path.join(base_dir, "chunks")
        self.output_dir = os.path.join(base_dir, "output")
        self.setup_directories()
        
        self.video_url=video_url
        self.video_id=video_id

    def setup_directories(self):
        for path in [self.audio_dir, self.chunks_dir, self.output_dir]:
            if not os.path.exists(path):
                os.makedirs(path)
    
    def download_audio_yt_dlp(self):
        import yt_dlp

        audio_path = os.path.join(self.audio_dir, f"{self.video_id}".lower())
        ffmpeg_path=os.path.dirname(utils.encontrar_ffmpeg())

        # Video URL
        video_url = f"https://www.youtube.com/watch?v={self.video_id}"
        
        # Define the options to match your command-line parameters
        ydl_opts = {
            'format': 'bestaudio/best',  # Extract best available audio
            'outtmpl': audio_path,  # Save with video ID as filename
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',  # Convert to mp3
                'preferredquality': '192',
            }],
            'ffmpeg_location': ffmpeg_path,  # Specify FFmpeg path
        }

        logging.info(f'Working in audio file {audio_path}')
        
        try:
            logging.info('Executing download audio with yt-dlp')
        
            # Run yt-dlp with specified options
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            logging.info("Download completed successfully.")
        except Exception as e:
            logging.info(f"An error occurred: {e}")
            
    
    def download_video_audio(self, audio_format="mp3"):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': audio_format,
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(self.audio_dir, '%(id)s.%(ext)s')
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.video_url])

    from pydub import AudioSegment

    def split_audio_fixed_intervals(self, audio_path, chunk_length_ms=60000):
        """
        Splits an audio file into fixed-length chunks.

        :param audio_path: Path to the input audio file.
        :param chunk_length_ms: Length of each chunk in milliseconds (default: 60 sec).
        :return: List of audio chunks.
        """
        #audio_pathx = "./data/audio/myteaiq7ipe.mp3"
        sound = AudioSegment.from_file(audio_path)  # Load audio
        logging.debug(f"Len of sound {len(sound)}")
        logging.debug(f"audio_path: {audio_path}, chunk_length: {chunk_length_ms}")
        chunks = [sound[i:i + chunk_length_ms] for i in range(0, len(sound), int(chunk_length_ms))]

        return chunks

    def split_audio(self):
        logging.info('Spliting Audio...')
        audio_path = os.path.join(self.audio_dir, f"{self.video_id}.wav".lower())  # Adjust filename as needed        
        logging.info(f'Working in audio file {audio_path}')
        ffmpeg_bin_path=os.path.dirname(utils.encontrar_ffmpeg())
        # Get the current PATH environment variable
        original_path = os.environ.get('PATH', '')
        os.environ['PATH'] = ffmpeg_bin_path + os.pathsep + original_path
        #logging.info('Get Env Vars')
        #logging.info(os.getenv('PATH'))
        # Explicitly setting the path to ffmpeg and ffprobe
        #AudioSegment.converter = r"C:\Program Files\ffmpeg\bin\ffmpeg.exe"
        AudioSegment.ffmpeg = utils.encontrar_ffmpeg()
        sistema = platform.system()
        if sistema == "Windows":
            executavel_ffprobe="ffprobe.exe"
        else:
            executavel_ffprobe="ffprobe"    
        AudioSegment.ffprobe = os.path.dirname(utils.encontrar_ffmpeg()) + '/' + executavel_ffprobe
                
        # Normalize the audio to a consistent level
        # normalized_sound = sound.normalize()
        
        # Alternative to Split on Silent Interval
        #chunks = split_on_silence(
        #    sound,
        #    min_silence_len=2000,
        #    silence_thresh=-30
        #)
        logging.info(f"Spliting Audio {audio_path}")
        chunks=self.split_audio_fixed_intervals(audio_path)
        logging.info(f'Split Audio in {len(chunks)} chunks...')
        return chunks

    def transcribe_audio(self, chunks):
        logging.info('Transcribing audio...')
        
        recognizer = sr.Recognizer()
        
        full_text = []
        for i, chunk in enumerate(chunks):
            chunk_file=f"{self.video_id}_chunk_{i}.wav".lower()
            chunk_path = os.path.join(self.chunks_dir, chunk_file)
            logging.info(f'Processing chunk {i}. Exporting to file {chunk_file}')
            chunk.export(chunk_path, format="wav")
            with sr.AudioFile(chunk_path) as source:
                audio = recognizer.record(source)
                try:
                    text = recognizer.recognize_google(audio, language="pt-BR")
                    full_text.append((text, source.DURATION))
                except sr.UnknownValueError:
                    logging.error('Segment Unintelligible')
                    full_text.append(("Unintelligible", 0))
                except sr.RequestError as e:
                    erro_message=f"API Error: {e}"
                    logging.error(erro_message)
                    full_text.append((erro_message, 0))
        return full_text

    def create_vtt(self, text_entries):
        output_filename=f"{self.video_id}.vtt".lower()
        output_path = os.path.join(self.output_dir, output_filename)
        logging.info(f'Creating VTT in outputfile {output_filename}')
        with open(output_path, 'w') as f:
            f.write("WEBVTT\n\n")
            start = 0
            for text, duration in text_entries:
                end = start + duration
                f.write(f"{self.format_timestamp(start)} --> {self.format_timestamp(end)}\n")
                f.write(f"{text}\n\n")
                start = end
        
        with open(output_path, 'r') as f:
            vtt_text=f.read()
        
        logging.info('VTT Created!')
        return vtt_text

    @staticmethod
    def format_timestamp(seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:06.3f}"

    def cleanup(self):
        for folder in [self.chunks_dir, self.audio_dir]:
            for file in os.listdir(folder):
                os.remove(os.path.join(folder, file))
        logging.info("Cleaned up intermediate files.")
