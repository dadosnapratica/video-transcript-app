from googleapiclient.discovery import build
#from google.cloud import speech
import io
import enum
import os
import googleapiclient.discovery
from cachetools import cached, TTLCache
import requests
import logging
from dotenv import load_dotenv
import utils
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from YouTubeTranscriber import YouTubeTranscriber as youtube_transcriber

load_dotenv()



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

# Get YouTube client for APIKey authentication
def get_youtube_client_apikey():
    
    # Build the YouTube client
    return googleapiclient.discovery.build(api_service_name, 
                                              api_version, 
                                              developerKey = google_api_key)

    


# Get YouTube client for OAuth2 authentication
def get_youtube_client_oauth():
    # The scope tells the script what permissions it has on the user's data
    SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

    # Load credentials from the downloaded OAuth client configuration    
    client_secrets_file='client_secret.json'

    # Get credentials and create an API client
    flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, 
                                                     SCOPES)
    credentials = flow.run_local_server(host='localhost', port=8051)

    # Build the YouTube client
    youtube = build('youtube', 'v3', credentials=credentials)

    return youtube

@cached(cache)
def get_language_data():
    logging.debug("Fetching new data from the server...")
    url = "https://raw.githubusercontent.com/dadosnapratica/language-code-table/refs/heads/main/data/dadosnapratica_language_code.json"
    response = requests.get(url)
    response.raise_for_status()  # Vai levantar uma exceção se a requisição não for bem-sucedida
    return response.json()

def obter_transcricao_youtube(video_id, video_lang, trans_lang):
    if utils.is_url(video_id):
        video_id=utils.extract_video_id(video_id)

    youtube = get_youtube_client_apikey()
    
    # Tenta recuperar as legendas disponíveis
    request = youtube.captions().list(
        part='snippet',
        videoId=video_id
    )
    response = request.execute()
    logging.info('Google Video API Response')
    logging.info(response)

    # Verifica se há legendas no idioma desejado
    #for item in response.get('items', []):
    #    if 1==1: #item['snippet']['language'] == video_lang.value:
    #        # Baixe e retorne a transcrição
    #        download_request = youtube.captions().download(
    #            id=item['id'],
    #            tfmt='srt'  # Formato das legendas
    #        )
    #        subtitle_file = io.BytesIO()
    #        download_response=download_request.execute()
    #        logging.info('Download Caption Response')
    #        logging.info(download_response)
    #        return "" #subtitle_file.getvalue().decode('utf-8')

    # Se não houver legendas, faça a transcrição no idioma desejado
    return transcrever_video(f'https://www.youtube.com/watch?v={video_id}', video_id, trans_lang)

#TODO: Future Implementation Translate the video 
def transcrever_video(video_url, video_id, trans_lang):    
    transcriber = youtube_transcriber(video_url, video_id)
    transcriber.download_audio_yt_dlp()    
    chunks = transcriber.split_audio()
    text_entries = transcriber.transcribe_audio(chunks)
    vtt_text=transcriber.create_vtt(text_entries)
    transcriber.cleanup()

    return vtt_text
    # raise NotImplementedError('Feature not implemented yet')
