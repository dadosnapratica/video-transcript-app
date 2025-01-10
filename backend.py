from googleapiclient.discovery import build
#from google.cloud import speech
import io
import enum
import os
import googleapiclient.discovery
from cachetools import cached, TTLCache
import requests

# Cache que expira após 1 dia (86400 segundos)
cache = TTLCache(maxsize=100, ttl=86400)

# Configuração da API do YouTube
google_api_key=os.getenv('GOOGLE_API_KEY')
# youtube = build('youtube', 'v3', developerKey=google_api_key)

# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = google_api_key
# Configuração da API Google Cloud Speech
#client = speech.SpeechClient()

@cached(cache)
def get_language_data():
    url = "https://raw.githubusercontent.com/dadosnapratica/language-code-table/refs/heads/main/data/dadosnapratica_language_code.json"
    response = requests.get(url)
    response.raise_for_status()  # Vai levantar uma exceção se a requisição não for bem-sucedida
    return response.json()

def obter_transcricao_youtube(video_id, video_lang, trans_lang):
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)
    
    # Tenta recuperar as legendas disponíveis
    request = youtube.captions().list(
        part='snippet',
        videoId=video_id
    )
    response = request.execute()

    # Verifica se há legendas no idioma desejado
    for item in response.get('items', []):
        if item['snippet']['language'] == video_lang.value:
            # Baixe e retorne a transcrição
            download_request = youtube.captions().download(
                id=item['id'],
                tfmt='srt'  # Formato das legendas
            )
            subtitle_file = io.BytesIO()
            download_request.execute(stream=subtitle_file)
            return subtitle_file.getvalue().decode('utf-8')

    # Se não houver legendas, faça a transcrição no idioma desejado
    return None #transcrever_video(video_id, trans_lang)

#TODO: Future Implementation for Transcrible Video
def transcrever_video(video_id, trans_lang):
    #audio = ...  # Suponha que "audio" é um objeto de áudio processado
    #response = client.recognize(config={
    #    "language_code": trans_lang.value
    #3}, audio=audio)
    
    # Concatena a transcrição
    #transcription = ''.join([result.alternatives[0].transcript for result in response.results])
    #return transcription
    raise NotImplementedError('Feature not implemented yet')
