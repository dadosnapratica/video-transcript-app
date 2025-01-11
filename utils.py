import re
import requests
import logging
import os
from dotenv import load_dotenv
import shutil
import platform

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
