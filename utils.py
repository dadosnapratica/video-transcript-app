import re
import requests
import logging
import os
from dotenv import load_dotenv
import shutil
import platform
# used to run shell commands to validate prerequisites
import subprocess
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from pathlib import Path


load_dotenv()
google_api_key=os.getenv('GOOGLE_API_KEY')


def is_url(input_string):
    # This regular expression is designed to match YouTube video URLs and extract the video ID
    url_regex = r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([a-zA-Z0-9_-]+)'
    match = re.match(url_regex, input_string)
    if match:
        return True
    else:
        return False
    
def extract_video_id(input_string):
    # This regular expression is designed to match YouTube video URLs and extract the video ID
    url_regex = r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([a-zA-Z0-9_-]+)'
    match = re.match(url_regex, input_string)
    logging.info(match)
    if match:
        return match.group(1)
    return input_string

def validate_video_id(video_id):
    global google_api_key
    logging.debug(f"Google API Key {google_api_key}")
    """ Validate the video ID by attempting to retrieve video details from YouTube API. """
    api_key = google_api_key  # Replace with your actual YouTube Data API key
    url = f"https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={api_key}&part=id"
    response = requests.get(url)
    if response.json().get('pageInfo', {}).get('totalResults', 0) > 0:
        return True
    return False

def validate_url(url):
    """ Validate the YouTube URL by sending a head request to check if the URL is accessible. """
    try:
        response = requests.head(url)
        if response.status_code == 200:
            return True
        return False
    except requests.RequestException:
        return False
    

def encontrar_ffmpeg():
    """
    Procura e retorna o caminho do executável `ffmpeg` no sistema operacional.
    Adaptado para Linux, macOS e Windows.
    """
    sistema = platform.system()  # Detecta o sistema operacional
    
    # Primeiro tenta encontrar no PATH
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        return ffmpeg_path
    
    # Busca por padrão em locais comuns para cada sistema operacional
    caminhos_comuns = []
    if sistema == "Windows":
        caminhos_comuns = [
            "C:\\Program Files\\FFmpeg\\bin\\ffmpeg.exe",
            "C:\\FFmpeg\\bin\\ffmpeg.exe",
            "C:\\ffmpeg\\bin\\ffmpeg.exe"
        ]
    elif sistema == "Darwin":  # macOS
        caminhos_comuns = [
            "/usr/local/bin/ffmpeg",
            "/opt/homebrew/bin/ffmpeg",  # Brew no Apple Silicon
            "/usr/bin/ffmpeg"
        ]
    elif sistema == "Linux":
        caminhos_comuns = [
            "/usr/bin/ffmpeg",
            "/usr/local/bin/ffmpeg",
            "/snap/bin/ffmpeg"
        ]
    
    # Verifica os caminhos comuns
    for caminho in caminhos_comuns:
        if os.path.isfile(caminho) and os.access(caminho, os.X_OK):  # Verifica se é executável
            return caminho
    
    # Retorna erro se não for encontrado
    raise FileNotFoundError("O executável `ffmpeg` não foi encontrado. Certifique-se de que está instalado e no PATH.")

def validate_prereq():
    results = []
    ffmeg_ok=False
    google_api_key_ok=False
    google_api_ok=False
    folder_data_ok=False

    # Validar FFmpeg
    try:
        #subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if len(encontrar_ffmpeg())>0:
            results.append(" FFmpeg: ✅ |")
            ffmeg_ok=True
        else:
            results.append(" FFmpeg: ❌ |")
   
    except subprocess.CalledProcessError:
        results.append(" FFmpeg: ❌ |")

    # Validar Google API Key
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        results.append(" Google API Key: ✅ |")
        google_api_key_ok=True
        # Testar acesso à API do Google
        try:
            youtube = build('youtube', 'v3', developerKey=api_key)
            youtube.channels().list(part="id", id="UC_x5XG1OV2P6uZZ5FSM9Ttw").execute()
            results.append(" API do Google: ✅ |")
            google_api_ok=True
        except Exception as e:
            results.append(" API do Google: ❌ |")
    else:
        results.append(" Google API Key: ❌ |")
        results.append(" API do Google: ❌ |")

    # Validar acesso para gravação na pasta data
    try:
        test_file_path = Path("data/test_write.txt")
        with test_file_path.open("w") as f:
            f.write("test")
        test_file_path.unlink()  # Remover o arquivo de teste
        results.append(" Folder data: ✅")
        folder_data_ok=True
    except IOError:
        results.append(" Folder data: ❌")

    status_checks = "\n".join(results)
    if ffmeg_ok or not google_api_key_ok or not google_api_ok or not folder_data_ok:
        status_checks+='\n\nThere are some pre-requirements error, please check links bellow to correct it.' 
    
    if ffmeg_ok:
        status_checks+='\n\n[ffmpeg install instructions](https://github.com/dadosnapratica/video-transcript-app#-how-to-use)'

    return status_checks

